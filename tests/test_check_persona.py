"""Unit tests for scripts/check_persona.py.

Each test builds a minimal `skills/sepia/references/` tree in a temp directory
and a persona body, runs the checker against them, and asserts on the exit
code and the report text. The negative cases are the ways a persona could
claim override rights it must not have, or drift from the template shape the
executor depends on.

Standard library only, like the script:  python3 -m unittest discover -s tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_persona  # noqa: E402

REFS = {
    "style-pass.md": "# style\n",
    "discourse-pass.md": "# discourse\n",
    "narrative-pass.md": "# narrative\n",
    "professional-pass.md": "# professional\n",
    "languages/zh.md": "# zh\n",
    "domains/journalism.md": "# j\n" + "".join(f"{i}. **Rule {i}.** text\n" for i in range(1, 9)),
    "domains/tickets.md": "# t\n" + "".join(f"{i}. **Rule {i}.** text\n" for i in range(1, 6)),
    # only the first rule bolded, as most real domain files do
    "domains/release-notes.md": "# r\n\n## Rules\n\n1. **Rule 1.** text\n2. Rule 2 plain\n3. Rule 3 plain\n\n## After\n\n4. not a rule\n",
    "domains/tech-articles.md": "# ta\n" + "".join(f"{i}. **Rule {i}.** text\n" for i in range(1, 7)),
    "domains/postmortems.md": "# pm\n" + "".join(f"{i}. **Rule {i}.** text\n" for i in range(1, 7)),
}

SECTIONS = check_persona.SECTIONS


def every_piece(overrides):
    """3–8 numbered moves: one per override token (up to seven), then one with no override."""
    lines = [f"{i}. Move {i} (overrides: {tok.strip('`')})" for i, (tok, _, _) in enumerate(overrides[:7], 1)]
    lines.append(f"{len(lines) + 1}. Open on a number (overrides: none)")
    while len(lines) < 3:
        lines.append(f"{len(lines) + 1}. Another plain move (overrides: none)")
    return "\n".join(lines)


def persona(overrides=None, prohibitions=None, status=None, drop=None, extra=None, order=None):
    """Build a valid persona body, then apply the requested deviations."""
    status = status or {
        "Name": "sample",
        "Routes": "professional",
        "Opt-in phrase": "apply persona sample",
        "Provenance": "12 pieces read in full",
        "Consent": "own style",
        "Tested": "untested",
    }
    overrides = overrides if overrides is not None else [
        ("`style-pass.md §3`", "idioms in narration", "§3 idiom hits reported as Persona cost"),
        ("`professional-pass.md check 4`", "a verdict sentence ends each section", "check 4 findings as Persona cost"),
    ]
    prohibitions = prohibitions if prohibitions is not None else [
        "Do not reuse this file’s example phrases verbatim; they are shapes, not a word list.",
        "Never invent facts, gestures, adverbs, or emotions; a missing fact is a TODO.",
    ]
    bodies = {
        "Status": "\n".join(f"{k}: {v}" for k, v in status.items()),
        "One sentence": "A writer who ends each section on the narrator's verdict and keeps a persona's idioms.",
        "Beat and themes": "Labour and policy; the writer's concerns enter narration directly.",
        "Metric fingerprint": "none measured; the close reading notes a long sentence mean.",
        "Moves by frequency": "- Ending verdict sentence, 10/12 pieces\n- Idiom in narration, 9/12",
        "Negatives": "No scene openings.",
        "Meaning for sepia": "check 4 and style-pass §3 would remove the two signatures.",
        "Every piece": every_piece(overrides),
        "Only with facts": "- A dated document quoted with its time, when the material has one.",
        "Sentence shape": "mean 50–60 characters, SD about 30; both ends present.",
        "Rules this persona overrides": "| Rule | How the persona departs | Expected cost |\n|---|---|---|\n"
        + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in overrides),
        "Prohibitions": "\n".join(f"- {p}" for p in prohibitions),
        "Boundary": "Like the writer: the verdict follows the facts. Like a model: the verdict precedes them.",
        "Blind-test record": "none yet",
    }
    if extra:
        for k, v in extra.items():
            bodies[k] = bodies[k] + "\n" + v
    seq = list(order or SECTIONS)
    if drop:
        seq = [s for s in seq if s != drop]
    out = ["# Persona — sample", ""]
    for s in seq:
        out += [f"## {s}", "", bodies[s], ""]
    return "\n".join(out)


class CheckPersonaCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for rel, content in REFS.items():
            p = self.root / "skills" / "sepia" / "references" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def run_check(self, body):
        f = self.root / "persona.md"
        f.write_text(body, encoding="utf-8")
        findings = check_persona.check_file(f, self.root)
        errors = [x for x in findings if ": ERROR: " in x]
        warns = [x for x in findings if ": WARN: " in x]
        return errors, warns

    # --- positive ---------------------------------------------------------

    def test_valid_persona_passes_with_apostrophes_and_curly_fixed_lines(self):
        errors, warns = self.run_check(persona())
        self.assertEqual(errors, [])
        self.assertEqual(warns, [])

    def test_single_quoted_long_span_is_not_a_quotation(self):
        body = persona(extra={"Negatives": "She never writes 'a very long single-quoted span of more than twenty characters' in narration."})
        errors, _ = self.run_check(body)
        self.assertEqual(errors, [])

    def test_table_row_with_odd_straight_quotes_passes(self):
        body = persona(extra={"Moves by frequency": '| a | a 12" print run | b |\n| c | another cell with one " mark | d |'})
        errors, _ = self.run_check(body)
        self.assertEqual(errors, [])

    def test_nine_override_rows_warn_but_pass(self):
        rows = [(f"`discourse-pass.md §{n}`", "x", "y") for n in (1, 2, 4, 5)]
        rows += [(f"`narrative-pass.md §{n}`", "x", "y") for n in (1, 2, 4, 5, 6)]
        errors, warns = self.run_check(persona(overrides=rows))
        self.assertEqual(errors, [])
        self.assertEqual(len(warns), 1)
        self.assertIn("9 override rows", warns[0])

    def test_domain_rule_within_range_passes(self):
        errors, _ = self.run_check(persona(overrides=[("`domains/journalism.md rule 8`", "x", "y")]))
        self.assertEqual(errors, [])

    # --- quotes ---------------------------------------------------------

    def test_long_corner_quote_fails(self):
        body = persona(extra={"Negatives": "「這是一段超過二十個字的引文範例，用來測試驗證器會不會擋」"})
        errors, _ = self.run_check(body)
        self.assertTrue(any("longer than 20" in e for e in errors), errors)

    def test_long_double_quote_on_one_line_fails(self):
        body = persona(extra={"Negatives": 'She wrote "a quoted example that runs well past the twenty character limit" once.'})
        errors, _ = self.run_check(body)
        self.assertTrue(any("longer than 20" in e for e in errors), errors)

    # --- structure ------------------------------------------------------

    def test_missing_section_fails(self):
        errors, _ = self.run_check(persona(drop="Boundary"))
        self.assertTrue(any("missing section '## Boundary'" in e for e in errors), errors)

    def test_wrong_order_fails(self):
        order = list(SECTIONS)
        order[1], order[2] = order[2], order[1]
        errors, _ = self.run_check(persona(order=order))
        self.assertTrue(any("not in template order" in e for e in errors), errors)

    def test_missing_consent_fails(self):
        status = {"Name": "s", "Routes": "any", "Opt-in phrase": "apply persona s", "Provenance": "p", "Tested": "untested"}
        errors, _ = self.run_check(persona(status=status))
        self.assertTrue(any("'Consent:'" in e for e in errors), errors)

    def test_unknown_route_fails(self):
        status = {"Name": "s", "Routes": "newsletter", "Opt-in phrase": "apply persona s", "Provenance": "p", "Consent": "own style", "Tested": "untested"}
        errors, _ = self.run_check(persona(status=status))
        self.assertTrue(any("Routes must be one of" in e for e in errors), errors)

    def test_missing_fixed_prohibition_fails(self):
        errors, _ = self.run_check(persona(prohibitions=["Never invent facts, gestures, adverbs, or emotions; a missing fact is a TODO."]))
        self.assertTrue(any("missing the fixed line" in e and "Do not reuse" in e for e in errors), errors)

    # --- override table -------------------------------------------------

    def test_non_yielding_tokens_fail(self):
        for tok in (
            "`style-pass.md §5`",
            "`professional-pass.md check 9`",
            "`professional-pass.md check 5`",
            "`languages/zh.md §2 flat-sentence-length`",
            "`discourse-pass.md §3`",
            "`domains/journalism.md rule 1`",
            "`domains/tech-articles.md rule 1`",
            "`domains/postmortems.md rule 2`",
            "`domains/journalism.md rule 3`",
        ):
            with self.subTest(tok=tok):
                errors, _ = self.run_check(persona(overrides=[(tok, "x", "y")]))
                self.assertTrue(any("never yields" in e for e in errors), (tok, errors))

    def test_free_text_rule_cells_fail(self):
        for tok in ("professional-pass.md #9", "professional-pass.md Sameness of rhythm", "SKILL.md Hard guardrails", "domains/journalism.md tells row 3"):
            with self.subTest(tok=tok):
                errors, _ = self.run_check(persona(overrides=[(tok, "x", "y")]))
                self.assertTrue(any("not a recognised rule token" in e for e in errors), (tok, errors))

    def test_unknown_domain_file_fails(self):
        errors, _ = self.run_check(persona(overrides=[("`domains/newsletters.md rule 1`", "x", "y")]))
        self.assertTrue(any("not found under references/" in e for e in errors), errors)

    def test_domain_rule_out_of_range_fails(self):
        errors, _ = self.run_check(persona(overrides=[("`domains/tickets.md rule 6`", "x", "y")]))
        self.assertTrue(any("no rule 6" in e for e in errors), errors)

    def test_section_out_of_range_fails(self):
        errors, _ = self.run_check(persona(overrides=[("`style-pass.md §8`", "x", "y")]))
        self.assertTrue(any("has no §8" in e for e in errors), errors)

    def test_zh_row_only_on_section_2(self):
        errors, _ = self.run_check(persona(overrides=[("`languages/zh.md §3 manner-adverb`", "x", "y")]))
        self.assertTrue(any("only on languages/zh.md §2" in e for e in errors), errors)

    def test_empty_cost_cell_fails(self):
        errors, _ = self.run_check(persona(overrides=[("`style-pass.md §3`", "x", "")]))
        self.assertTrue(any("three non-empty cells" in e for e in errors), errors)

    # --- step 3 interface gaps -------------------------------------------

    def test_private_study_consent_is_accepted(self):
        base = {"Name": "sample", "Routes": "any", "Opt-in phrase": "apply persona sample", "Provenance": "p", "Tested": "untested"}
        errors, _ = self.run_check(persona(status={**base, "Consent": "private study, not for distribution"}))
        self.assertEqual(errors, [])
        errors, _ = self.run_check(persona(status={**base, "Consent": "private study"}))
        self.assertTrue(any("Consent must be one of" in e for e in errors), errors)

    def test_optin_name_match_ignores_case(self):
        base = {"Name": "Nyaneko", "Routes": "professional", "Provenance": "p", "Consent": "brand persona", "Tested": "untested"}
        for phrase in ("apply persona Nyaneko", "apply persona nyaneko"):
            with self.subTest(phrase=phrase):
                errors, _ = self.run_check(persona(status={**base, "Opt-in phrase": phrase}))
                self.assertEqual(errors, [], phrase)
        errors, _ = self.run_check(persona(status={**base, "Opt-in phrase": "apply persona someone-else"}))
        self.assertTrue(any("but Name is" in e for e in errors), errors)

    def test_bilingual_optin_halves_match_ignoring_case(self):
        base = {"Name": "Nyaneko", "Routes": "professional", "Provenance": "p", "Consent": "brand persona", "Tested": "untested"}
        for phrase in ("apply persona Nyaneko / 「套用 persona Nyaneko」",
                       "apply persona nyaneko / 「套用 persona Nyaneko」",
                       "apply persona Nyaneko / 「套用 persona nyaneko」"):
            with self.subTest(phrase=phrase):
                errors, _ = self.run_check(persona(status={**base, "Opt-in phrase": phrase}))
                self.assertEqual(errors, [], phrase)
        errors, _ = self.run_check(persona(status={**base, "Opt-in phrase": "apply persona Nyaneko / 「套用 persona someone-else」"}))
        self.assertTrue(any("in the Chinese form" in e for e in errors), errors)

    def test_optin_name_match_is_caseless_not_just_lowercased(self):
        # casefold(), unlike lower(), folds ß to ss, so these three are one name.
        base = {"Routes": "any", "Provenance": "p", "Consent": "own style", "Tested": "untested"}
        for name, phrase in (("Straße", "apply persona STRASSE"),
                             ("STRASSE", "apply persona Straße"),
                             ("Straße", "apply persona Straße / 「套用 persona STRASSE」")):
            with self.subTest(name=name, phrase=phrase):
                errors, _ = self.run_check(persona(status={**base, "Name": name, "Opt-in phrase": phrase}))
                self.assertEqual(errors, [], (name, phrase))

    def test_consent_error_names_every_accepted_value(self):
        base = {"Name": "sample", "Routes": "any", "Opt-in phrase": "apply persona sample", "Provenance": "p", "Tested": "untested"}
        errors, _ = self.run_check(persona(status={**base, "Consent": "no idea"}))
        msg = next(e for e in errors if "Consent must be one of" in e)
        for value in ("own style", "public-domain author", "fictional persona", "brand persona",
                      "private study, not for distribution", "consent from the person"):
            self.assertIn(value, msg)

    # --- follow-up after the final report --------------------------------

    def test_bare_zh_section_2_fails_but_other_sections_pass(self):
        errors, _ = self.run_check(persona(overrides=[("`languages/zh.md §2`", "x", "y")]))
        self.assertTrue(any("§2 must name a row" in e for e in errors), errors)
        errors, _ = self.run_check(persona(overrides=[("`languages/zh.md §4`", "x", "y")]))
        self.assertEqual(errors, [])

    def test_tilde_line_inside_a_backtick_fence_does_not_close_it(self):
        body = persona()
        pro = "- Do not reuse this file\u2019s example phrases verbatim; they are shapes, not a word list.\n- Never invent facts, gestures, adverbs, or emotions; a missing fact is a TODO."
        # the fixed lines sit inside a ``` block that quotes a ~~~ line: the
        # block must stay open, so the lines are sample text and not list items
        errors, _ = self.run_check(body.replace(pro, "```\n~~~\n" + pro + "\n```"))
        self.assertTrue(any("missing the fixed line" in e for e in errors), errors)

    def test_fenced_code_does_not_count_as_structure(self):
        body = persona()
        table = "| Rule | How the persona departs | Expected cost |\n|---|---|---|\n| `style-pass.md §3` | idioms in narration | §3 idiom hits reported as Persona cost |\n| `professional-pass.md check 4` | a verdict sentence ends each section | check 4 findings as Persona cost |"
        self.assertIn(table, body)
        errors, _ = self.run_check(body.replace(table, "```\n" + table + "\n```"))
        self.assertTrue(any("override table has no rows" in e for e in errors), errors)
        moves = every_piece([("`style-pass.md §3`", "", ""), ("`professional-pass.md check 4`", "", "")])
        errors, _ = self.run_check(body.replace(moves, "```\n" + moves + "\n```"))
        self.assertTrue(any("found 0" in e for e in errors), errors)
        pro = "- Do not reuse this file\u2019s example phrases verbatim; they are shapes, not a word list.\n- Never invent facts, gestures, adverbs, or emotions; a missing fact is a TODO."
        errors, _ = self.run_check(body.replace(pro, "```\n" + pro + "\n```"))
        self.assertTrue(any("missing the fixed line" in e for e in errors), errors)

    # --- round-5 (final-report) cases ------------------------------------

    def test_unbolded_domain_rule_within_range_passes(self):
        errors, _ = self.run_check(persona(overrides=[("`domains/release-notes.md rule 3`", "x", "y")]))
        self.assertEqual(errors, [])
        errors, _ = self.run_check(persona(overrides=[("`domains/release-notes.md rule 4`", "x", "y")]))
        self.assertTrue(any("no rule 4" in e for e in errors), errors)

    def test_tested_value_is_case_sensitive(self):
        body = persona().replace("Tested: untested", "Tested: UnTested")
        errors, _ = self.run_check(body)
        self.assertTrue(any("Tested must be" in e for e in errors), errors)

    def test_doubled_edge_pipes_fail(self):
        body = persona().replace("| Rule | How the persona departs | Expected cost |", "|| Rule | How the persona departs | Expected cost ||")
        errors, _ = self.run_check(body)
        self.assertTrue(any("header must be exactly" in e for e in errors), errors)

    # --- round-4 review cases -------------------------------------------

    def test_multi_word_name_passes(self):
        status = {"Name": "Virginia Woolf", "Routes": "fiction", "Opt-in phrase": "apply persona Virginia Woolf / 「套用 persona Virginia Woolf」", "Provenance": "p", "Consent": "public-domain author", "Tested": "untested"}
        errors, _ = self.run_check(persona(status=status))
        self.assertEqual(errors, [])
        status["Opt-in phrase"] = "apply persona Virginia Woolf / 「套用 persona Virginia」"
        errors, _ = self.run_check(persona(status=status))
        self.assertTrue(any("Opt-in phrase" in e for e in errors), errors)

    # --- round-3 review cases -------------------------------------------

    def test_narrative_endings_section_is_overridable(self):
        errors, _ = self.run_check(persona(overrides=[("`narrative-pass.md §3`", "ends on the narrator's verdict", "endings findings as Persona cost")]))
        self.assertEqual(errors, [])

    def test_empty_move_text_fails(self):
        body = persona().replace("3. Open on a number (overrides: none)", "3. (overrides: none)")
        errors, _ = self.run_check(body)
        self.assertTrue(any("needs move text" in e for e in errors), errors)

    def test_consent_date_must_be_a_calendar_date(self):
        base = {"Name": "sample", "Routes": "any", "Opt-in phrase": "apply persona sample", "Provenance": "p", "Tested": "untested"}
        errors, _ = self.run_check(persona(status={**base, "Consent": "consent from the person, 2025-99-99"}))
        self.assertTrue(any("not a calendar date" in e for e in errors), errors)

    def test_unknown_status_line_fails(self):
        body = persona().replace("Tested: untested", "Tested: untested\nReviewer: someone")
        errors, _ = self.run_check(body)
        self.assertTrue(any("only the six 'Key: value' lines" in e for e in errors), errors)

    def test_tested_with_placeholder_record_fails(self):
        status = {"Name": "sample", "Routes": "any", "Opt-in phrase": "apply persona sample", "Provenance": "p", "Consent": "own style", "Tested": "tested"}
        for rec in ("TODO", "not run", "one reader picked the persona passage", "2026-09-16", "2026-09-16 — judge: — compared: x — outcome: y"):
            with self.subTest(rec=rec):
                errors, _ = self.run_check(persona(status=status).replace("none yet", rec))
                self.assertTrue(any("Blind-test record" in e for e in errors), (rec, errors))
        rec = "2026-09-16 — judge: one reader — compared: a vs b — outcome: TODO"
        errors, _ = self.run_check(persona(status=status).replace("none yet", rec))
        self.assertTrue(any("field is a placeholder" in e for e in errors), errors)
        rec = "2026-09-16 — judge: one reader — compared: a vs b — outcome: none preferred"
        errors, _ = self.run_check(persona(status=status).replace("none yet", rec))
        self.assertEqual(errors, [])
        rec = "2026-09-16 — judge: one reader — compared: a vs b — outcome: a\nfree text line"
        errors, _ = self.run_check(persona(status=status).replace("none yet", rec))
        self.assertTrue(any("is not of the form" in e for e in errors), errors)

    # --- round-2 review cases -------------------------------------------

    def test_duplicate_status_key_fails(self):
        body = persona().replace("Routes: professional", "Routes: professional\nRoutes: fiction")
        errors, _ = self.run_check(body)
        self.assertTrue(any("2 'Routes:' lines" in e for e in errors), errors)

    def test_negated_or_padded_optin_phrase_fails(self):
        base = {"Name": "sample", "Routes": "any", "Provenance": "p", "Consent": "own style", "Tested": "untested"}
        for phrase in ("do not apply persona sample", "apply persona sample please", "套用 persona sample"):
            with self.subTest(phrase=phrase):
                errors, _ = self.run_check(persona(status={**base, "Opt-in phrase": phrase}))
                self.assertTrue(any("Opt-in phrase" in e for e in errors), (phrase, errors))
        errors, _ = self.run_check(persona(status={**base, "Opt-in phrase": "apply persona sample / 「套用 persona sample」"}))
        self.assertEqual(errors, [])

    def test_consent_with_trailing_text_fails(self):
        base = {"Name": "sample", "Routes": "any", "Opt-in phrase": "apply persona sample", "Provenance": "p", "Tested": "untested"}
        for c in ("own style, no permission", "consent from the person, 2025-01-15 (not recorded)"):
            with self.subTest(c=c):
                errors, _ = self.run_check(persona(status={**base, "Consent": c}))
                self.assertTrue(any("Consent must be one of" in e for e in errors), (c, errors))

    def test_every_piece_count_and_annotations(self):
        body = persona().replace(every_piece([("`style-pass.md §3`", "", ""), ("`professional-pass.md check 4`", "", "")]), "1. Only one move (overrides: none)")
        errors, _ = self.run_check(body)
        self.assertTrue(any("must list 3–8 numbered moves, found 1" in e for e in errors), errors)
        body = persona().replace("3. Open on a number (overrides: none)", "3. Open on a number")
        errors, _ = self.run_check(body)
        self.assertTrue(any("needs move text and a trailing" in e for e in errors), errors)
        body = persona().replace("3. Open on a number (overrides: none)", "3. Open on a number (overrides: discourse-pass.md §1)")
        errors, _ = self.run_check(body)
        self.assertTrue(any("not in the override table" in e for e in errors), errors)

    def test_duplicate_heading_fails(self):
        body = persona() + "\n## Boundary\n\nagain\n"
        errors, _ = self.run_check(body)
        self.assertTrue(any("duplicate section '## Boundary'" in e for e in errors), errors)

    def test_four_column_separator_fails(self):
        body = persona().replace("|---|---|---|", "|---|---|---|---|")
        errors, _ = self.run_check(body)
        self.assertTrue(any("three-column separator" in e for e in errors), errors)

    def test_prohibition_as_paragraph_fails(self):
        body = persona().replace("- Do not reuse this file\u2019s example phrases verbatim; they are shapes, not a word list.", "Do not reuse this file\u2019s example phrases verbatim; they are shapes, not a word list.")
        errors, _ = self.run_check(body)
        self.assertTrue(any("missing the fixed line" in e and "Do not reuse" in e for e in errors), errors)

    # --- round-1 review cases -------------------------------------------

    def test_malformed_table_header_fails_and_hides_nothing(self):
        body = persona(overrides=[("`style-pass.md §5`", "x", "y")])
        body = body.replace("| Rule | How the persona departs | Expected cost |\n|---|---|---|\n", "")
        errors, _ = self.run_check(body)
        self.assertTrue(any("header must be exactly" in e for e in errors), errors)

    def test_extra_heading_fails(self):
        body = persona() + "\n## Notes\n\nextra\n"
        errors, _ = self.run_check(body)
        self.assertTrue(any("unexpected section '## Notes'" in e for e in errors), errors)

    def test_optin_name_must_match_name(self):
        status = {"Name": "alice", "Routes": "any", "Opt-in phrase": "apply persona bob / 「套用 persona bob」", "Provenance": "p", "Consent": "own style", "Tested": "untested"}
        errors, _ = self.run_check(persona(status=status))
        self.assertTrue(any("but Name is 'alice'" in e for e in errors), errors)

    def test_bad_consent_fails_and_dated_consent_passes(self):
        base = {"Name": "s", "Routes": "any", "Opt-in phrase": "apply persona s", "Provenance": "p", "Tested": "untested"}
        errors, _ = self.run_check(persona(status={**base, "Consent": "I have no permission"}))
        self.assertTrue(any("Consent must be one of" in e for e in errors), errors)
        errors, _ = self.run_check(persona(status={**base, "Consent": "consent from the person, 2025-01-15"}))
        self.assertEqual(errors, [])
        errors, _ = self.run_check(persona(status={**base, "Consent": "consent from the person, last year"}))
        self.assertTrue(any("Consent must be one of" in e for e in errors), errors)

    def test_tested_requires_a_record(self):
        status = {"Name": "sample", "Routes": "any", "Opt-in phrase": "apply persona sample", "Provenance": "p", "Consent": "own style", "Tested": "tested"}
        errors, _ = self.run_check(persona(status=status))
        self.assertTrue(any("Blind-test record" in e for e in errors), errors)
        body = persona(status=status).replace("none yet", "2026-09-16 — judge: one reader — compared: persona passage vs house style — outcome: persona picked")
        errors, _ = self.run_check(body)
        self.assertEqual(errors, [])

    def test_prohibition_embedded_in_a_longer_line_fails(self):
        errors, _ = self.run_check(persona(prohibitions=[
            "Note: Do not reuse this file's example phrases verbatim; they are shapes, not a word list.",
            "Never invent facts, gestures, adverbs, or emotions; a missing fact is a TODO.",
        ]))
        self.assertTrue(any("missing the fixed line" in e for e in errors), errors)

    def test_long_quote_in_provenance_is_metadata_and_passes(self):
        status = {"Name": "sample", "Routes": "any", "Opt-in phrase": "apply persona sample", "Provenance": 'read "A Very Long Source Title That Exceeds Twenty Characters" in full', "Consent": "own style", "Tested": "untested"}
        errors, _ = self.run_check(persona(status=status))
        self.assertEqual(errors, [])

    def test_main_exit_codes(self):
        good = self.root / "good.md"
        good.write_text(persona(), encoding="utf-8")
        bad = self.root / "bad.md"
        bad.write_text(persona(drop="Boundary"), encoding="utf-8")
        self.assertEqual(check_persona.main(["--root", str(self.root), str(good)]), 0)
        self.assertEqual(check_persona.main(["--root", str(self.root), str(bad)]), 1)


if __name__ == "__main__":
    unittest.main()
