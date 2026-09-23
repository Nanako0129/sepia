"""Deterministic tests for the optional sepia-opt-* measure.py diagnostics.

Covers empty input, one sentence, Unicode punctuation, abbreviations, no final
punctuation, short texts, and each classification boundary. Also verifies the
scripts emit valid JSON and do not crash on valid UTF-8 input.

Standard library only:  python3 -m unittest discover -s tests
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BURST = ROOT / "skills" / "sepia-opt-burstiness" / "scripts" / "measure.py"
PERP = ROOT / "skills" / "sepia-opt-perplexity" / "scripts" / "measure.py"


def _load(path, name):
    """Load a measure.py script as a module under a distinct name to avoid import clashes."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


burst_measure = _load(str(BURST), "burst_measure")
perp_measure = _load(str(PERP), "perp_measure")


class BurstinessTests(unittest.TestCase):
    def test_empty_input(self):
        """Empty text should return an error payload with the language scope."""
        out = burst_measure.analyze("")
        self.assertIn("error", out)
        self.assertEqual(out["language_scope"], "english-prose-only")

    def test_one_sentence_is_too_few(self):
        """A single sentence cannot support a burstiness measurement."""
        out = burst_measure.analyze("One short sentence.")
        self.assertIn("error", out)
        self.assertIn(">=2 sentences", out["error"])

    def test_uniform_text_flagged(self):
        """Three equal-length sentences should read as uniform (low variation)."""
        out = burst_measure.analyze("Word word. Word word. Word word.")
        self.assertEqual(out["band"], "uniform - low sentence-length variation")

    def test_highly_variable_text(self):
        """Mixed very short and very long sentences should read as highly variable."""
        text = (
            "Go. Go. Go. Go. Go. "
            "The quick brown fox jumps over the lazy dog near the riverbank "
            "while the children played happily outside."
        )
        out = burst_measure.analyze(text)
        self.assertIn("highly variable", out["band"])

    def test_mixed_text_limited_sample(self):
        """Two sentences cannot support a reliable variation band; expect the limited-sample note."""
        out = burst_measure.analyze(
            "I went. The quick brown fox jumps over the lazy dog and then runs away fast."
        )
        self.assertEqual(
            out["band"],
            "limited sample (<=2 sentences) - variation needs >=3 sentences",
        )
        self.assertEqual(out["language_scope"], "english-prose-only")

    def test_unicode_punctuation_no_crash(self):
        """Unicode punctuation and em dashes should not crash the analyzer."""
        out = burst_measure.analyze("Café! “Quotes?” — em dash. Résumé.")
        self.assertIn("sentences", out)

    def test_abbreviation_no_crash(self):
        """Abbreviations like Dr. and U.S.A. should not crash the analyzer."""
        out = burst_measure.analyze("Dr. Smith went to the U.S.A. He was happy.")
        self.assertIn("sentences", out)

    def test_abbreviation_counts_as_one_sentence(self):
        """'Dr. Smith wrote.' is one sentence; the period after Dr. must not create a boundary."""
        out = burst_measure.analyze("Dr. Smith wrote.")
        self.assertEqual(out["sentences"], 1)
        self.assertIn("error", out)
        self.assertIn(">=2 sentences", out["error"])

    def test_abbreviation_at_sentence_end_preserves_boundary(self):
        """A real sentence ending in an abbreviation (e.g. 'U.S.A.') must not swallow the next sentence."""
        out = burst_measure.analyze("I live in the U.S.A. Today I leave.")
        self.assertEqual(out["sentences"], 2)

    def test_mid_sentence_abbreviation_merges(self):
        """A short segment ending in an abbreviation continues the same sentence (e.g. 'He met Mr. Smith.')."""
        out = burst_measure.analyze("He met Mr. Smith. They left.")
        self.assertEqual(out["sentences"], 2)

    def test_uk_acronym_recognized_two_sentences(self):
        """'The U.K. is vast. Go.' is two sentences; U.K. is an acronym not present as lowercased in
        ABBREVIATIONS, so it must be matched case-sensitively against the original token to keep
        the boundary after it."""
        out = burst_measure.analyze("The U.K. is vast. Go.")
        self.assertEqual(out["sentences"], 2)

    def test_title_abbreviation_merge_exempt_from_word_limit(self):
        """A title abbreviation (Prof.) at the end of a short segment merges with the next word even
        though it is the only abbreviation; 'Prof. Smith wrote.' is one sentence."""
        out = burst_measure.analyze("Prof. Smith wrote.")
        self.assertEqual(out["sentences"], 1)
        self.assertIn("error", out)
        self.assertIn(">=2 sentences", out["error"])

    def test_two_sentence_extreme_not_highly_variable(self):
        """A two-sentence extreme ratio cannot be called 'highly variable'; the band is withheld."""
        out = burst_measure.analyze(
            "Go. The quick brown fox jumps over the lazy dog and then runs away fast."
        )
        self.assertNotIn("highly variable", out["band"])

    def test_no_final_punctuation(self):
        """Text without terminal punctuation should fall back to the too-few error."""
        out = burst_measure.analyze("this is a sentence without ending")
        self.assertIn("error", out)


class PerplexityTests(unittest.TestCase):
    def test_empty_input(self):
        """Empty text should return an error payload with the language scope."""
        out = perp_measure.analyze("")
        self.assertIn("error", out)
        self.assertEqual(out["language_scope"], "english-prose-only")

    def test_single_token(self):
        """A single token is an insufficient sample; metrics are kept but no variety band is given."""
        out = perp_measure.analyze("Word.")
        self.assertEqual(out["tokens"], 1)
        self.assertIn("insufficient sample", out["band"])

    def test_low_variety_flagged(self):
        """Heavy repetition should read as low lexical variety."""
        out = perp_measure.analyze("the the the the the the the the the the")
        self.assertIn("low lexical variety", out["band"])

    def test_high_variety_flagged(self):
        """Many rare, distinct words should read as high lexical variety."""
        text = (
            "quartz zirconium xylophonist juxtaposition brackish wombat "
            "kleptomania zephyr quokka"
        )
        out = perp_measure.analyze(text)
        self.assertIn("high lexical variety", out["band"])

    def test_moderate_variety(self):
        """Repeated content words with some variety should read as moderate."""
        out = perp_measure.analyze("The wizard cast a spell. The wizard found a spell book.")
        self.assertEqual(out["band"], "moderate lexical variety")
        self.assertEqual(out["language_scope"], "english-prose-only")

    def test_unicode_no_crash(self):
        """Unicode words should not crash the analyzer."""
        out = perp_measure.analyze("Café résumé naïve über.")
        self.assertIn("tokens", out)

    def test_abbreviation_no_crash(self):
        """Abbreviations should not crash the analyzer."""
        out = perp_measure.analyze("Dr. Smith went to the U.S.A. happily.")
        self.assertIn("tokens", out)


class CliJsonTests(unittest.TestCase):
    def _run(self, script, text):
        """Run a measure.py script against a temp UTF-8 file and return the completed process."""
        with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(text)
            path = f.name
        try:
            return subprocess.run(
                [sys.executable, str(script), path],
                capture_output=True,
                text=True,
            )
        finally:
            Path(path).unlink(missing_ok=True)

    def test_burstiness_cli_emits_json(self):
        """The burstiness CLI should emit valid JSON containing a cv metric."""
        res = self._run(
            BURST,
            "I went. The quick brown fox jumps over the lazy dog and then runs away fast.",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        data = json.loads(res.stdout)
        self.assertIn("cv", data)

    def test_perplexity_cli_emits_json_on_utf8(self):
        """The perplexity CLI should emit valid JSON containing a ttr metric on UTF-8 input."""
        res = self._run(PERP, "Café résumé naïve über. The quark zoomed past.")
        self.assertEqual(res.returncode, 0, res.stderr)
        data = json.loads(res.stdout)
        self.assertIn("ttr", data)

    def test_cli_handles_empty_file(self):
        """The burstiness CLI should emit a valid JSON error for an empty file."""
        res = self._run(BURST, "")
        self.assertEqual(res.returncode, 0, res.stderr)
        data = json.loads(res.stdout)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
