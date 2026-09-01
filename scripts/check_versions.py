#!/usr/bin/env python3
"""Fail when the files that declare a version disagree about which one it is.

Three files carry sepia's version today: the Claude and Codex plugin manifests
and the canonical SKILL.md's frontmatter. They have never disagreed. This is a
guard for later, not a fix for now.

It matters because the failure would be silent. Nothing breaks at install time
when one manifest is a version behind; the wrong number just gets advertised,
and a version number is exactly the claim a reader uses to judge whether a
project is still maintained.

Two rules, covering the two ways this can rot:

1. Discovery. Any file named plugin.json or marketplace.json is read wherever
   it sits, for a top-level `version` and for one on each entry of a `plugins`
   array, and every SKILL.md's frontmatter is read for `metadata.version`. A
   manifest that gains a version later is checked from that moment. A `version`
   key that exists but is not a non-empty string fails: a field someone edited
   into a number or an empty value is a mistake, not an absence.

2. A required core. The three files that declare the version today must keep
   declaring it. Without this, deleting one of them would just shrink the
   agreeing set and the check would stay green, which is precisely the silent
   failure it exists to catch.

Files that declare nothing and are not required are listed, not failed: absent
is a legitimate state there, and printing them keeps the scan's reach visible.
Discovery finding nothing at all is likewise a failure, not a pass.

Standard library only, by design. The repository has no lockfiles and this
should not be the reason it gets one.

    python3 scripts/check_versions.py

Exit status is 0 when every declaration agrees and the required files all
declare, 1 otherwise. The unit tests live in tests/test_check_versions.py.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Directories that never hold a manifest worth checking.
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache"}

# Any file with one of these names is treated as a packaging manifest, wherever
# it sits. That is the point: a manifest added in a new directory is found.
MANIFEST_NAMES = {"plugin.json", "marketplace.json"}

# The files that carry the version today. Discovery still scans everything;
# these additionally MUST declare one, so a deleted or mistyped field fails
# instead of quietly shrinking the agreeing set. When the layout changes on
# purpose, change this list in the same commit.
REQUIRED = (
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    "skills/sepia/SKILL.md",
)


def _iter_files(root):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        # Only the directories BELOW root count: a repository checked out at
        # /work/venv/sepia must not have every file skipped because an
        # ancestor happens to be named venv (review round 5).
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts[:-1]):
            continue
        yield path


def _valid(value):
    """A well-formed declaration: a non-empty string with no surrounding
    whitespace. " 0.4.0 " is not the same advertised version as "0.4.0", and
    normalizing it away would hide a manifest that differs from its siblings,
    so it is reported instead of stripped (review round 4)."""
    return isinstance(value, str) and value != "" and value == value.strip()


def _frontmatter_scalar(raw, rel):
    """(version_or_None, invalid) for one frontmatter version value.

    The shared value rules for both block and flow style. A quoted value is
    taken literally (minus the quotes) and then held to the same
    no-surrounding-whitespace rule as the JSON manifests. An unquoted value
    is invalid, full stop, with instructions to quote it. The first cut tried
    to enumerate what YAML reads as non-strings and the enumeration had no
    natural end (1.0, then true and null, then 0b10, then sexagesimal), so per
    review the rule is inverted: quoting is the requirement, and this whole
    class of finding closes permanently.
    """
    raw = raw.split(" #")[0].strip()
    if raw == "":
        return None, [(rel, "metadata.version is present but empty")]
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        value = raw[1:-1]
        if value.strip() == "":
            return None, [(rel, "metadata.version is present but empty")]
        if value != value.strip():
            return None, [(rel, f"metadata.version {value!r} has surrounding whitespace")]
        return value, []
    return None, [(rel, f"metadata.version {raw} is unquoted; quote it")]


def read_json_versions(path, rel):
    """(declared, invalid) for one JSON manifest.

    declared: [(label, version)] for every well-formed declaration.
    invalid:  [(label, reason)] for every `version` key that exists but is not
              a non-empty string. Present-but-wrong is an error, never an
              absence: treating it as absence is how a deleted or mistyped
              field slips through.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [], [(rel, f"unreadable: {exc}")]

    declared, invalid = [], []
    if isinstance(data, dict):
        if "version" in data:
            if _valid(data["version"]):
                declared.append((rel, data["version"]))
            else:
                invalid.append((rel, f"version is {data['version']!r}, not a non-empty string without surrounding whitespace"))
        for index, entry in enumerate(data.get("plugins") or []):
            if isinstance(entry, dict) and "version" in entry:
                label = f"{rel} → plugins[{index}]"
                if _valid(entry["version"]):
                    declared.append((label, entry["version"]))
                else:
                    invalid.append((label, f"version is {entry['version']!r}, not a non-empty string without surrounding whitespace"))
    return declared, invalid


def read_frontmatter_version(path, rel):
    """(version_or_None, invalid) for one SKILL.md.

    Only a `version:` that is a DIRECT child of a block-style top-level
    `metadata:` counts. Inline metadata (flow mappings, scalars) is refused
    with instructions to use block style: two review rounds of quoted-span and
    nested-brace edge cases traced back to hand-parsing flow, and the refusal
    is loud and names its own fix. A line scan rather than a YAML parser, carrying two pieces of
    state: entering the frontmatter's `metadata:` key opens the block and the
    next top-level key closes it, and the block's first child fixes the
    indentation that direct children must sit at. Anything deeper belongs to a
    nested key (say `metadata.compatibility.version`) and anything named
    version under some other top-level key belongs to that key, so neither is
    the skill's version. Blank lines carry no structure and are skipped rather
    than being mistaken for a top-level key.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [(rel, f"unreadable: {exc}")]

    # An editor-added UTF-8 BOM is invisible and tolerated by real
    # frontmatter loaders; without stripping it the first line reads as
    # \ufeff--- and a valid required file goes red on an invisible byte.
    if text.startswith("\ufeff"):
        text = text[1:]

    # Delimiters must be exactly --- as whole lines. Prefix matching let
    # ---oops open and ---- close a "frontmatter" that a real YAML loader
    # would refuse, keeping the required-core guard green after the
    # declaration was broken (review round 7).
    lines = text.splitlines()
    if not lines or lines[0].rstrip() != "---":
        return None, []
    close = next((i for i in range(1, len(lines)) if lines[i].rstrip() == "---"), None)
    if close is None:
        return None, []

    in_metadata = False
    child_indent = None
    for line in lines[1:close]:
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            # A comment carries no structure at any indentation; an unindented
            # one between metadata: and its children must not read as a new
            # top-level key that closes the block (review round 4).
            continue
        if not line[:1].isspace():
            head, sep, rest = line.partition(":")
            if head.strip() == "metadata" and sep:
                rest = rest.split(" #")[0].strip()
                if rest:
                    # An inline value (flow mapping or scalar) is refused, not
                    # parsed. The flow parser this replaces produced two review
                    # findings of its own (nested braces, then quoted spans),
                    # and the failure a formatter causes here is loud and names
                    # its own fix, while a hand-parsed flow mapping fails
                    # quietly and wrong (review round 6).
                    return None, [(rel,
                        "metadata is declared inline; flow-style metadata is "
                        "not supported, use block style")]
                in_metadata = True
            else:
                in_metadata = False
            child_indent = None
            continue
        if not in_metadata:
            continue
        indent = len(line) - len(line.lstrip())
        if child_indent is None:
            child_indent = indent
        if indent != child_indent:
            continue
        stripped = line.strip()
        if stripped.startswith("version:"):
            return _frontmatter_scalar(stripped[len("version:"):], rel)
    return None, []


def scan(root):
    """Walk the repository once. Returns (declared, silent, invalid)."""
    declared, silent, invalid = [], [], []

    for path in _iter_files(root):
        rel = path.relative_to(root).as_posix()  # forward slashes on Windows too
        if path.name in MANIFEST_NAMES:
            found, bad = read_json_versions(path, rel)
            invalid.extend(bad)
            if found:
                declared.extend(found)
            elif not bad:
                silent.append(rel)
        elif path.name == "SKILL.md":
            version, bad = read_frontmatter_version(path, rel)
            invalid.extend(bad)
            if version:
                declared.append((rel, version))
            elif not bad:
                silent.append(rel)

    return declared, silent, invalid


def run(root, required=REQUIRED):
    """The whole check, as (exit_code, report_text). main() just prints it."""
    declared, silent, invalid = scan(root)
    lines, failures = [], []

    labels = [label for label, _ in declared]
    width = max((len(label) for label in labels + silent), default=0)
    for label, version in declared:
        lines.append(f"  {label.ljust(width)}  {version}")
    for label in silent:
        lines.append(f"  {label.ljust(width)}  (no version declared)")

    for label, reason in invalid:
        failures.append(f"{label}: {reason}")

    for rel in required:
        if rel not in labels:
            failures.append(
                f"{rel}: required to declare a version and does not. If the layout "
                "changed on purpose, update REQUIRED in scripts/check_versions.py."
            )

    if not declared and not failures:
        failures.append(
            "no file declares a version. Either the manifests moved or this "
            "script's discovery is out of date."
        )

    versions = {version for _, version in declared}
    if len(versions) > 1:
        failures.append(
            f"{len(versions)} different versions declared: {', '.join(sorted(versions))}. "
            "Every file that states a version must state the same one."
        )

    if failures:
        lines.append("")
        lines.append("version check: FAILED")
        lines.extend(f"  - {failure}" for failure in failures)
        return 1, "\n".join(lines)

    lines.append("")
    lines.append(f"version check: OK, {len(declared)} declarations, all {versions.pop()}.")
    return 0, "\n".join(lines)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv in (["-h"], ["--help"]):
        print(__doc__.strip())
        return 0
    if argv:
        print(f"version check: takes no arguments, got {' '.join(argv)}", file=sys.stderr)
        return 2

    code, report = run(ROOT)
    print(report, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
