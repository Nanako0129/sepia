"""Unit tests for scripts/check_versions.py.

Each test builds a small repository in a temp directory and runs the whole
check against it, asserting on the exit code and the report text. The cases
mirror the ways the real repository could drift, including the two found in
review: a required version field disappearing, and a version edited into a
non-string value, both of which must fail rather than count as "not declared".

Standard library only, like the script:  python3 -m unittest discover -s tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_versions


def skill_md(frontmatter_lines):
    return "---\n" + "\n".join(frontmatter_lines) + "\n---\n\n# sepia\n"


BASELINE = {
    ".claude-plugin/plugin.json": {"name": "sepia", "version": "0.4.0"},
    ".codex-plugin/plugin.json": {"name": "sepia", "version": "0.4.0"},
    ".claude-plugin/marketplace.json": {"name": "sepia", "plugins": [{"name": "sepia"}]},
    "plugin.json": {"name": "sepia"},
    "skills/sepia/SKILL.md": skill_md(
        ["name: sepia", "license: MIT", "metadata:", '  version: "0.4.0"']
    ),
}


class CheckVersionsCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def write(self, files):
        for rel, content in files.items():
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, dict):
                content = json.dumps(content, indent=2) + "\n"
            path.write_text(content, encoding="utf-8")

    def run_check(self, overrides=None):
        files = dict(BASELINE)
        files.update(overrides or {})
        self.write(files)
        return check_versions.run(self.root)

    # --- the healthy repository ---------------------------------------------

    def test_agreeing_declarations_pass(self):
        code, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertIn("3 declarations, all 0.4.0", report)

    def test_undeclared_files_are_listed_not_failed(self):
        code, report = self.run_check()
        self.assertEqual(code, 0)
        self.assertIn("plugin.json", report)
        self.assertIn("(no version declared)", report)

    # --- disagreement -------------------------------------------------------

    def test_one_manifest_behind_fails_naming_both_versions(self):
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia", "version": "0.3.0"}}
        )
        self.assertEqual(code, 1)
        self.assertIn("0.3.0", report)
        self.assertIn("0.4.0", report)

    # --- the two review findings -------------------------------------------

    def test_removing_a_required_version_field_fails(self):
        # Review case: delete .codex-plugin/plugin.json's version. The two
        # remaining declarations still agree, so without the required set this
        # would pass, which is exactly the silent failure being guarded.
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia"}}
        )
        self.assertEqual(code, 1)
        self.assertIn("required to declare a version", report)
        self.assertIn(".codex-plugin/plugin.json", report)

    def test_a_non_string_version_fails_rather_than_counting_as_absent(self):
        # Review case: "version": 0.5. Present-but-wrong is an error.
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia", "version": 0.5}}
        )
        self.assertEqual(code, 1)
        self.assertIn("not a non-empty string", report)

    def test_an_empty_string_version_fails(self):
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia", "version": ""}}
        )
        self.assertEqual(code, 1)
        self.assertIn("not a non-empty string", report)

    # --- frontmatter scoping ------------------------------------------------

    def test_version_under_another_key_is_not_the_skill_version(self):
        # Review case: compatibility.version must not shadow metadata.version.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    [
                        "name: sepia",
                        "compatibility:",
                        '  version: "9.9.9"',
                        "metadata:",
                        '  version: "0.4.0"',
                    ]
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertNotIn("9.9.9", report)

    def test_only_a_foreign_version_means_the_skill_declares_none(self):
        # With no metadata.version at all, the skill declares nothing, and
        # since it is a required file that is a failure.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "compatibility:", '  version: "9.9.9"']
                )
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("skills/sepia/SKILL.md: required", report)

    def test_a_top_level_frontmatter_version_does_not_count(self):
        # The Agent Skills shape puts the version under metadata; a top-level
        # version key belongs to nothing and must not be picked up.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ['version: "9.9.9"', "name: sepia", "metadata:", '  version: "0.4.0"']
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertNotIn("9.9.9", report)

    def test_a_nested_version_inside_metadata_is_not_the_skill_version(self):
        # Review case, round two: metadata.compatibility.version must not
        # shadow metadata's own direct child. Only the direct child counts.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    [
                        "name: sepia",
                        "metadata:",
                        "  compatibility:",
                        '    version: "9.9.9"',
                        '  version: "0.4.0"',
                    ]
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertNotIn("9.9.9", report)

    def test_only_a_nested_version_means_the_skill_declares_none(self):
        # With nothing but metadata.compatibility.version, the skill declares
        # no version of its own, and since it is required that fails.
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", "  compatibility:", '    version: "9.9.9"']
                )
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("skills/sepia/SKILL.md: required", report)

    def test_a_utf8_bom_before_the_frontmatter_is_tolerated(self):
        # Editors on Windows add a BOM; real frontmatter loaders tolerate it.
        # Exact-line delimiter matching must not turn an invisible byte into
        # a red required check.
        content = "\ufeff" + skill_md(["name: sepia", "metadata:", '  version: "0.4.0"'])
        code, report = self.run_check({"skills/sepia/SKILL.md": content})
        self.assertEqual(code, 0)
        self.assertIn("3 declarations, all 0.4.0", report)

    def test_a_corrupted_opening_delimiter_means_no_frontmatter(self):
        # Review round 7: ---oops is not a frontmatter opener, but prefix
        # matching accepted it, so the guard stayed green after the
        # declaration was broken. A real YAML loader sees no frontmatter
        # here; so must the scanner, and the required core then goes red.
        content = "---oops\nname: sepia\nmetadata:\n  version: \"0.4.0\"\n---\n\n# sepia\n"
        code, report = self.run_check({"skills/sepia/SKILL.md": content})
        self.assertEqual(code, 1)
        self.assertIn("skills/sepia/SKILL.md: required", report)

    def test_a_corrupted_closing_delimiter_means_no_frontmatter(self):
        # ---- is not a closing delimiter; without an exact --- line the
        # block is unterminated and declares nothing.
        content = "---\nname: sepia\nmetadata:\n  version: \"0.4.0\"\n----\n\n# sepia\n"
        code, report = self.run_check({"skills/sepia/SKILL.md": content})
        self.assertEqual(code, 1)
        self.assertIn("skills/sepia/SKILL.md: required", report)

    def test_a_blank_line_inside_metadata_does_not_close_the_block(self):
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", "", '  version: "0.4.0"']
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertIn("3 declarations, all 0.4.0", report)

    # --- review round four: whitespace, comments, unquoted scalars ----------

    def test_surrounding_whitespace_in_a_json_version_is_invalid_not_normalized(self):
        # " 0.4.0 " is not the same advertised version as "0.4.0"; stripping
        # it away would hide a manifest that differs from its siblings.
        code, report = self.run_check(
            {".codex-plugin/plugin.json": {"name": "sepia", "version": " 0.4.0 "}}
        )
        self.assertEqual(code, 1)
        self.assertIn("surrounding whitespace", report)

    def test_an_unindented_comment_does_not_close_the_metadata_block(self):
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", "# version used for packaging", '  version: "0.4.0"']
                )
            }
        )
        self.assertEqual(code, 0)
        self.assertIn("3 declarations, all 0.4.0", report)

    def test_an_indented_comment_does_not_fix_the_child_indentation(self):
        # If the comment were treated as the first child, its indentation
        # would become the required level and the real version would be
        # skipped as "wrong depth".
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", "    # a deeper comment", '  version: "0.4.0"']
                )
            }
        )
        self.assertEqual(code, 0)

    def test_any_unquoted_version_is_rejected_with_quote_instructions(self):
        # Inverted per review round five: enumerating what YAML reads as
        # non-strings had no natural end (1.0, true, null, 0b10, ...), so an
        # unquoted value is invalid, full stop. This includes 0.4.0, which
        # YAML would read as a string: quoting is the requirement, not a
        # workaround for particular scalar forms.
        for value in ("1.0", "true", "null", "~", "off", "0b10", "0.4.0"):
            code, report = self.run_check(
                {
                    "skills/sepia/SKILL.md": skill_md(
                        ["name: sepia", "metadata:", f"  version: {value}"]
                    )
                }
            )
            self.assertEqual(code, 1, f"version: {value} should be rejected")
            self.assertIn("quote it", report)

    def test_quoted_whitespace_in_frontmatter_is_held_to_the_json_rule(self):
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", '  version: " 0.4.0 "']
                )
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("surrounding whitespace", report)

    def test_manifests_inside_skipped_directories_are_not_scanned(self):
        # A vendored manifest deep in node_modules must not fail the check;
        # the walk prunes these directories instead of reading and then
        # discarding them.
        code, report = self.run_check(
            {"node_modules/dep/.claude-plugin/plugin.json": {"name": "dep", "version": "9.9.9"}}
        )
        self.assertEqual(code, 0)
        self.assertNotIn("9.9.9", report)

    def test_a_repository_under_a_skipped_ancestor_name_still_scans(self):
        # Review round five: SKIP_DIRS applied to absolute path parts made a
        # checkout at .../venv/<repo> skip every file and report all required
        # manifests missing. Only directories below root may match.
        nested = self.root / "venv" / "repo"
        for rel, content in BASELINE.items():
            path = nested / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, dict):
                content = json.dumps(content, indent=2) + "\n"
            path.write_text(content, encoding="utf-8")
        code, report = check_versions.run(nested)
        self.assertEqual(code, 0)
        self.assertIn("3 declarations, all 0.4.0", report)

    # --- inline metadata is refused, not parsed (round 6) -------------------

    def test_inline_metadata_is_refused_with_block_style_instructions(self):
        # The flow parser produced two review findings of its own (nested
        # braces, then version-like text inside a quoted value). Deleted per
        # review: any inline metadata value is refused with a message naming
        # the fix. The last case is the round-six finding itself: without the
        # deletion, text inside a quoted scalar was mistaken for a version key.
        for inline in (
            '{version: "0.4.0"}',
            '{compatibility: {version: "9.9.9"}, version: "0.4.0"}',
            '{version: 1.0}',
            'oops',
            '{description: "current, version: 9.9.9"}',
        ):
            code, report = self.run_check(
                {"skills/sepia/SKILL.md": skill_md(["name: sepia", f"metadata: {inline}"])}
            )
            self.assertEqual(code, 1, f"metadata: {inline} should be refused")
            self.assertIn("use block style", report)

    def test_an_empty_metadata_version_fails(self):
        code, report = self.run_check(
            {
                "skills/sepia/SKILL.md": skill_md(
                    ["name: sepia", "metadata:", "  version:"]
                )
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("present but empty", report)

    # --- discovery of manifests that grow a version later -------------------

    def test_root_plugin_json_growing_a_matching_version_is_counted(self):
        code, report = self.run_check(
            {"plugin.json": {"name": "sepia", "version": "0.4.0"}}
        )
        self.assertEqual(code, 0)
        self.assertIn("4 declarations", report)

    def test_root_plugin_json_growing_a_different_version_fails(self):
        code, report = self.run_check(
            {"plugin.json": {"name": "sepia", "version": "0.5.0"}}
        )
        self.assertEqual(code, 1)
        self.assertIn("0.5.0", report)

    def test_a_marketplace_plugins_entry_version_is_checked_by_label(self):
        code, report = self.run_check(
            {
                ".claude-plugin/marketplace.json": {
                    "name": "sepia",
                    "plugins": [{"name": "sepia", "version": "0.9.9"}],
                }
            }
        )
        self.assertEqual(code, 1)
        self.assertIn("plugins[0]", report)
        self.assertIn("0.9.9", report)

    # --- the guard guarding itself ------------------------------------------

    def test_an_empty_tree_fails_rather_than_passing_vacuously(self):
        self.write({})  # nothing at all
        code, report = check_versions.run(self.root)
        self.assertEqual(code, 1)

    def test_unreadable_json_fails(self):
        code, report = self.run_check({".codex-plugin/plugin.json": "{not json"})
        self.assertEqual(code, 1)
        self.assertIn("unreadable", report)


if __name__ == "__main__":
    unittest.main()
