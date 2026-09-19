#!/usr/bin/env python3
"""Validate a sepia persona profile against the template contract.

A persona profile (`skills/sepia/references/voices/PERSONA-TEMPLATE.md`) is a
Markdown file with a fixed sequence of H2 sections, a Status block of six
keyed lines, a three-column table of the sepia rules the persona overrides,
and a Prohibitions section carrying two fixed lines. The prose may be in any
language; this script checks structure and contract, never style.

What it enforces, and why each rule exists (`voice-skills.md`, persona
section):

- Section order: the executor reads the body top to bottom, and the
  prescriptive sections ("Every piece", the override table, "Prohibitions")
  must come after the descriptive ones, or the persona is read as a
  description and its moves are eaten by sepia's rules.
- Rule tokens: the override table names rules with a restricted grammar so
  the body and the review's `Persona cost:` line use the same identifiers, and
  so the non-yielding rules can be refused by identity rather than by guessing
  at free text. Domain tells and SKILL.md guardrails are outside the grammar:
  no persona overrides them.
- Non-yielding rules: uniformity (`style-pass.md §5`, `professional-pass.md
  check 9`, `languages/zh.md §2 flat-sentence-length`, `discourse-pass.md §3`)
  and never-invent (`professional-pass.md check 5`, and the domain rules that
  restate the guardrail: `domains/journalism.md rule 1`,
  `domains/tech-articles.md rule 1`, `domains/postmortems.md rule 2`) cannot
  be overridden by any persona; nor can `domains/journalism.md rule 3`, which
  restates the quoted-material guardrail. `languages/zh.md §2` must name a
  row, so the whole section cannot be listed around its uniformity row.
- Fenced code blocks are ignored when reading sections, so sample text in
  ``` cannot stand in for the override table, the Every piece list or the
  Prohibitions list items.
- Consent: one of five contributable forms, or `private study, not for
  distribution` for a profile held locally. `CONTRIBUTING.md` forbids that
  last value in a contributed profile; the value exists so a private profile
  does not have to misstate its consent to pass this check.
- Fixed prohibition lines: defined once here (ASCII apostrophes) and quoted
  into the template and CONTRIBUTING; the comparison normalises curly quotes.
- Quoted examples: no span inside 「」, 『』 or a paired double quote may exceed
  20 characters, so a profile carries shapes, not reusable text. Single quotes
  and apostrophes are not quotation marks for this purpose; the Status and
  Blind-test record sections are exempt because their quotes are metadata.

Standard library only. Usage:

    python3 scripts/check_persona.py [--root REPO_ROOT] FILE [FILE ...]

Exit status 1 when any file has an ERROR; warnings do not fail.
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

SECTIONS = (
    "Status",
    "One sentence",
    "Beat and themes",
    "Metric fingerprint",
    "Moves by frequency",
    "Negatives",
    "Meaning for sepia",
    "Every piece",
    "Only with facts",
    "Sentence shape",
    "Rules this persona overrides",
    "Prohibitions",
    "Boundary",
    "Blind-test record",
)

STATUS_KEYS = ("Name", "Routes", "Opt-in phrase", "Provenance", "Consent", "Tested")
ROUTES = {"professional", "fiction", "any"}
TESTED = {"tested", "untested"}
# Consent takes one of these forms; the dated form needs an ISO date.
CONSENT_RE = re.compile(
    r"(own style|public-domain author|fictional persona|brand persona|"
    r"private study, not for distribution|"
    r"consent from the person, \d{4}-\d{2}-\d{2})"
)
# The whole Opt-in phrase field: the English form, optionally followed by the
# Chinese form for the same name. Nothing else is an affirmative opt-in. The
# two names are captured separately rather than matched with a backreference,
# because a backreference is case-sensitive and the phrase is not: the halves
# are compared below with the same caseless test the Name check uses.
OPTIN_RE = re.compile(r"apply persona ([^/「」]+?)(?: / 「套用 persona ([^「」]+)」)?")
# One blind-test entry per line: date — judge — compared — outcome.
RECORD_RE = re.compile(r"^\s*(?:[-*]\s+)?(\d{4}-\d{2}-\d{2}) — judge: \S.* — compared: \S.* — outcome: \S.*$", re.M)
MOVE_RE = re.compile(r"^\s*\d+\.\s+(\S.*?)\s*\(overrides: ([^)]+)\)\s*$")
ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
STATUS_LINE_RE = re.compile(r"^([A-Za-z -]+):\s*(.*)$")
MIN_MOVES, MAX_MOVES = 3, 8
TABLE_HEADER = ("Rule", "How the persona departs", "Expected cost")
# Sections whose quoted text is metadata (a source title, a compared passage),
# not example phrases; the 20-character rule does not apply there.
QUOTE_SCAN_EXEMPT = {"Status", "Blind-test record"}

PROHIBITION_LINES = (
    "Do not reuse this file's example phrases verbatim; they are shapes, not a word list.",
    "Never invent facts, gestures, adverbs, or emotions; a missing fact is a TODO.",
)

MAX_QUOTE = 20
MAX_OVERRIDES_BEFORE_WARN = 8

# Rule-token grammar. Each entry: (regex, file under skills/sepia/references/,
# allowed identifiers or None for "any integer within range").
ZH_SECTIONS = {"0", "1", "1b", "1c", "2", "3", "4", "5", "6"}
ZH_ROWS = {
    "connective-stacking",
    "second-person",
    "disyllabic-padding",
    "flat-sentence-length",
    "manner-adverb",
}
SECTION_RANGES = {
    "style-pass.md": range(1, 8),
    "discourse-pass.md": range(1, 6),
    "narrative-pass.md": range(1, 8),
}
CHECK_RANGE = range(1, 11)

NON_YIELDING = {
    # uniformity: sections whose whole content is uniformity. The Reviewing
    # table's uniformity row stays at full strength regardless of any token
    # (a formula ending named under narrative-pass.md §3 is still reported).
    "style-pass.md §5",
    "professional-pass.md check 9",
    "languages/zh.md §2 flat-sentence-length",
    "discourse-pass.md §3",
    # never invent: the "real" requirement and the domain rules that restate
    # the guardrail for their venue
    "professional-pass.md check 5",
    "domains/journalism.md rule 1",
    "domains/tech-articles.md rule 1",
    "domains/postmortems.md rule 2",
    # quoted material is load-bearing (SKILL.md guardrail restated for the venue)
    "domains/journalism.md rule 3",
}

_TOKEN_RES = (
    ("section", re.compile(r"^(style-pass\.md|discourse-pass\.md|narrative-pass\.md) §(\d+)$")),
    ("zh", re.compile(r"^languages/zh\.md §(0|1|1b|1c|2|3|4|5|6)(?: ([a-z-]+))?$")),
    ("check", re.compile(r"^professional-pass\.md check (\d+)$")),
    ("domain", re.compile(r"^domains/([a-z0-9-]+\.md) rule (\d+)$")),
)


def normalise(text: str) -> str:
    """Fold curly quotes and apostrophes to their ASCII forms.

    The fixed prohibition lines and the consent forms are compared after
    this, so a body written with typographic punctuation passes the same
    checks as one written with ASCII.
    """
    return (
        text.replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
    )


def parse_token(cell: str, root: Path) -> tuple[str | None, str | None]:
    """Return (canonical token, error). Exactly one of the two is None."""
    cell = cell.strip().strip("`")
    refs = root / "skills" / "sepia" / "references"
    for kind, rx in _TOKEN_RES:
        m = rx.match(cell)
        if not m:
            continue
        if kind == "section":
            fname, n = m.group(1), int(m.group(2))
            if n not in SECTION_RANGES[fname]:
                return None, f"{fname} has no §{n}"
            if not (refs / fname).exists():
                return None, f"{fname} not found under references/"
            return f"{fname} §{n}", None
        if kind == "zh":
            sec, row = m.group(1), m.group(2)
            if not (refs / "languages" / "zh.md").exists():
                return None, "languages/zh.md not found under references/"
            if row is not None:
                if sec != "2":
                    return None, "a row name is allowed only on languages/zh.md §2"
                if row not in ZH_ROWS:
                    return None, f"unknown zh.md §2 row '{row}'"
                return f"languages/zh.md §2 {row}", None
            if sec == "2":
                return None, "languages/zh.md §2 must name a row (one of " + ", ".join(sorted(ZH_ROWS)) + ")"
            return f"languages/zh.md §{sec}", None
        if kind == "check":
            n = int(m.group(1))
            if n not in CHECK_RANGE:
                return None, f"professional-pass.md has no check {n}"
            if not (refs / "professional-pass.md").exists():
                return None, "professional-pass.md not found under references/"
            return f"professional-pass.md check {n}", None
        if kind == "domain":
            fname, n = m.group(1), int(m.group(2))
            path = refs / "domains" / fname
            if not path.exists():
                return None, f"domains/{fname} not found under references/"
            rules = _numbered_rules(path.read_text(encoding="utf-8"))
            if not 1 <= n <= rules:
                return None, f"domains/{fname} has {rules} numbered rules, no rule {n}"
            return f"domains/{fname} rule {n}", None
    return None, "rule cell is not a recognised rule token"


def _numbered_rules(text: str) -> int:
    """Count the numbered items under a domain file's Rules heading.

    Only the first rule is bolded in most domain files, so the count takes
    every `<n>. ` line in that section, not only the bolded ones.
    """
    m = re.search(r"^## Rules[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    body = m.group(1) if m else text
    return len(re.findall(r"^\d+\. ", body, re.M))


def split_sections(text: str) -> tuple[list[str], dict[str, str]]:
    """H2 headings in order, and body text per heading.

    Lines inside fenced code blocks are dropped from the bodies: a table, a
    numbered list or a list item inside ``` is sample text, not structure,
    and must not satisfy the structural checks. A block closes only on a
    marker of the same character and at least the opener's length, so a
    ``` block quoting a ~~~ line does not end early and leak its sample
    text back into the structure.
    """
    order: list[str] = []
    bodies: dict[str, list[str]] = {}
    current = None
    fence: str | None = None
    for line in text.splitlines():
        mf = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if mf:
            marker, rest = mf.group(1), mf.group(2)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not rest.strip():
                fence = None
            continue
        if fence is not None:
            continue
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            current = m.group(1).strip()
            order.append(current)
            bodies[current] = []
        elif current is not None:
            bodies[current].append(line)
    return order, {k: "\n".join(v) for k, v in bodies.items()}


def table_rows(body: str) -> tuple[list[list[str]], str | None]:
    """Data rows of the override table, or (rows, error).

    The first pipe row must be the exact three-column header and the second the
    separator; otherwise a malformed table could hide a forbidden token in a row
    that a naive "drop the first row" would discard.
    """
    pipe_rows = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("|"):
            # remove exactly one outer delimiter on each side; a doubled edge
            # pipe leaves an empty cell and fails the width checks below
            inner = s[1:-1] if s.endswith("|") else s[1:]
            pipe_rows.append([c.strip() for c in inner.split("|")])
    if not pipe_rows:
        return [], "override table has no rows"
    if tuple(pipe_rows[0]) != TABLE_HEADER:
        return [], "override table header must be exactly | Rule | How the persona departs | Expected cost |"
    if len(pipe_rows) < 2 or len(pipe_rows[1]) != len(TABLE_HEADER) or not all(re.fullmatch(r":?-{3,}:?", c) for c in pipe_rows[1]):
        return [], "override table header must be followed by a three-column separator row"
    return pipe_rows[2:], None


_QUOTE_RE = re.compile(r"「([^」]*)」|『([^』]*)』|\"([^\"]*)\"")


def long_quotes(text: str) -> list[str]:
    """Quoted spans over MAX_QUOTE characters, paired within one line only.

    「」 and 『』 pair by their distinct delimiters; straight or curly double
    quotes (normalised to straight) pair by alternation on the same line, so an
    unmatched quote on a line is ignored rather than paired across lines or
    table cells. Single quotes and apostrophes are not quotation marks here.
    """
    found = []
    for line in normalise(text).splitlines():
        for m in _QUOTE_RE.finditer(line):
            span = next(g for g in m.groups() if g is not None)
            if len(span) > MAX_QUOTE:
                found.append(span)
    return found


def check_file(path: Path, root: Path) -> list[str]:
    """Check one persona body against the template contract.

    Returns one ``<path>: ERROR|WARN: <message>`` line per finding, in the
    order the contract is read: section sequence, Status block, override
    table, Every piece moves, Prohibitions, quoted examples. ``root`` is the
    repository whose ``skills/sepia/references/`` the rule tokens resolve
    against.
    """
    findings: list[str] = []
    err = lambda msg: findings.append(f"{path}: ERROR: {msg}")
    warn = lambda msg: findings.append(f"{path}: WARN: {msg}")
    text = path.read_text(encoding="utf-8")

    order, bodies = split_sections(text)
    missing = [s for s in SECTIONS if s not in order]
    unexpected = [s for s in order if s not in SECTIONS]
    dups = sorted({s for s in order if order.count(s) > 1})
    for s in missing:
        err(f"missing section '## {s}'")
    for s in unexpected:
        err(f"unexpected section '## {s}' (the template's H2 sequence is fixed)")
    for s in dups:
        err(f"duplicate section '## {s}'")
    if not (missing or unexpected or dups) and tuple(order) != SECTIONS:
        err("sections are not in template order")

    status = bodies.get("Status", "")
    for l in status.splitlines():
        if not l.strip():
            continue
        m = STATUS_LINE_RE.match(l)
        if not m or m.group(1).strip() not in STATUS_KEYS:
            err(f"Status may contain only the six 'Key: value' lines; found: {l.strip()[:60]}")
    values = {}
    for key in STATUS_KEYS:
        ms = re.findall(rf"^{re.escape(key)}:\s*(.*)$", status, re.M)
        if len(ms) > 1:
            err(f"Status has {len(ms)} '{key}:' lines; exactly one is allowed")
        elif not ms or not ms[0].strip():
            err(f"Status is missing a non-empty '{key}:' line")
        else:
            values[key] = ms[0].strip()
    if "Routes" in values and values["Routes"] not in ROUTES:
        err(f"Routes must be one of {sorted(ROUTES)}, got '{values['Routes']}'")
    if "Tested" in values and values["Tested"] not in TESTED:
        err(f"Tested must be 'tested' or 'untested', got '{values['Tested']}'")
    if "Consent" in values:
        cm = CONSENT_RE.fullmatch(normalise(values["Consent"]))
        if not cm:
            err("Consent must be one of: own style | public-domain author | fictional persona | "
                "brand persona | private study, not for distribution | "
                "consent from the person, YYYY-MM-DD")
        elif cm.group(1).startswith("consent from the person"):
            try:
                datetime.date.fromisoformat(cm.group(1)[-10:])
            except ValueError:
                err(f"Consent date is not a calendar date: {cm.group(1)[-10:]}")
    if "Opt-in phrase" in values:
        m = OPTIN_RE.fullmatch(values["Opt-in phrase"])
        if not m:
            err("Opt-in phrase must be exactly 'apply persona <name>' optionally followed by ' / 「套用 persona <name>」'")
        elif m.group(2) is not None and m.group(2).casefold() != m.group(1).casefold():
            err(f"Opt-in phrase names '{m.group(1)}' in the English form but '{m.group(2)}' in the Chinese form")
        elif "Name" in values and m.group(1).casefold() != values["Name"].casefold():
            err(f"Opt-in phrase names '{m.group(1)}' but Name is '{values['Name']}'")
    if values.get("Tested") == "tested":
        lines = [l for l in bodies.get("Blind-test record", "").splitlines() if l.strip()]
        if not lines:
            err("Tested: tested requires at least one Blind-test record line of the form "
                "'YYYY-MM-DD — judge: … — compared: … — outcome: …'")
        for l in lines:
            m = RECORD_RE.match(l)
            if not m:
                err("Blind-test record line is not of the form 'YYYY-MM-DD — judge: … — compared: … — outcome: …': "
                    + l.strip()[:60])
                continue
            fields = [f.strip() for f in re.split(r" — (?:judge|compared|outcome): ", l)[1:]]
            if any(re.fullmatch(r"(TODO|none|not run|pending|n/a)", f, re.I) for f in fields):
                err(f"Blind-test record field is a placeholder: {l.strip()[:60]}")
            try:
                datetime.date.fromisoformat(m.group(1))
            except ValueError:
                err(f"Blind-test record date is not a calendar date: {m.group(1)}")

    rows, terr = table_rows(bodies.get("Rules this persona overrides", ""))
    if terr:
        err(terr)
    elif not rows:
        err("override table has no data rows")
    declared: set[str] = set()
    for i, row in enumerate(rows, 1):
        if len(row) != 3 or not all(row):
            err(f"override row {i} must have three non-empty cells")
            continue
        token, terr = parse_token(row[0], root)
        if terr:
            err(f"override row {i}: {terr} ({row[0]})")
        elif token in NON_YIELDING:
            err(f"override row {i}: {token} never yields to a persona")
        else:
            declared.add(token)

    # Every piece: 3–8 numbered moves, each ending in "(overrides: <token>)" or
    # "(overrides: none)", and a named token must be in the table above.
    moves = [l for l in bodies.get("Every piece", "").splitlines() if re.match(r"^\s*\d+\.\s", l)]
    if not MIN_MOVES <= len(moves) <= MAX_MOVES:
        err(f"Every piece must list {MIN_MOVES}–{MAX_MOVES} numbered moves, found {len(moves)}")
    for l in moves:
        m = MOVE_RE.match(l)
        if not m:
            err(f"Every piece move needs move text and a trailing '(overrides: <rule token>|none)': {l.strip()[:60]}")
            continue
        ref = m.group(2).strip().strip("`")
        if ref == "none":
            continue
        token, terr = parse_token(ref, root)
        if terr:
            err(f"Every piece move overrides an unrecognised token: {ref}")
        elif token not in declared:
            err(f"Every piece move overrides {token}, which is not in the override table")
    if len(rows) > MAX_OVERRIDES_BEFORE_WARN:
        warn(f"{len(rows)} override rows; more than {MAX_OVERRIDES_BEFORE_WARN} reads as a house style")

    prohibition_lines = {
        m.group(1).strip()
        for l in bodies.get("Prohibitions", "").splitlines()
        for m in [re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", normalise(l))]
        if m
    }
    for line in PROHIBITION_LINES:
        if line not in prohibition_lines:
            err(f"Prohibitions is missing the fixed line (as its own list item, verbatim): {line}")

    for section, body in bodies.items():
        if section in QUOTE_SCAN_EXEMPT:
            continue
        for span in long_quotes(body):
            err(f"quoted example longer than {MAX_QUOTE} characters in '{section}': {span[:30]}…")

    return findings


def main(argv=None) -> int:
    """Check every file named on the command line; exit 1 if any has an ERROR."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("files", nargs="+", type=Path)
    args = ap.parse_args(argv)
    all_findings: list[str] = []
    for f in args.files:
        all_findings.extend(check_file(f, args.root))
    for line in all_findings:
        print(line)
    errors = sum(1 for l in all_findings if ": ERROR: " in l)
    print(f"persona check: {'FAIL' if errors else 'OK'}, {len(args.files)} file(s), {errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
