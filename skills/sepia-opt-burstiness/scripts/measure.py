#!/usr/bin/env python3
"""Burstiness diagnostic for the optional sepia-opt-burstiness skill.

Standard library only. Reports sentence-length statistics as an editorial
rhythm signal:
  - CV (coefficient of variation) of sentence word-counts
  - an alternation index (mean adjacent length difference / mean)
Human prose typically varies more than uniform machine text; the reported
bands are descriptive, not validated thresholds. English prose only.
"""
import sys
import re
import json
import statistics


def read_text(path):
    """Read input text from a file path, or fall back to stdin when no path is given."""
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


ABBREVIATIONS = {
    "dr", "mr", "mrs", "ms", "prof", "sr", "jr", "st", "vs", "etc",
    "inc", "ltd", "co", "e.g", "i.e", "a.m", "p.m", "u.s.a",
}

# Title abbreviations always attach to the next word, regardless of how long the
# current segment is. Other abbreviations/acronyms use the short-segment cutoff
# in _is_short_abbrev_segment so a longer segment ending in one (e.g.
# "I live in the U.S.A.") still keeps its own sentence boundary.
TITLE_ABBREVIATIONS = {"dr", "mr", "mrs", "ms", "prof"}


def _is_short_abbrev_segment(segment):
    """Return True when a segment ending in an abbreviation should merge with the next.

    A title abbreviation ("Dr.", "Mr.", "Mrs.", "Ms.", "Prof.") always attaches to
    the next word, regardless of segment length. Other abbreviations and acronyms
    (e.g. "U.S.A.", "U.K.", "Inc.") only merge when the segment is short (<=3 words),
    so a longer segment ending in one (e.g. "I live in the U.S.A.") keeps its own
    sentence boundary and a following sentence is counted separately.
    """
    words = segment.rstrip().split()
    if not words:
        return False
    last = words[-1]
    if not last.endswith("."):
        return False
    core = last[:-1].lower()
    is_title = core in TITLE_ABBREVIATIONS
    if core in ABBREVIATIONS:
        is_abbrev = True
    else:
        # Single capital letter ("U.") or all-caps acronym with periods ("U.K.",
        # "U.S.A."). Match against the original `last` (uppercase preserved), not the
        # lowercased `core`, so "U.K." is recognized.
        is_abbrev = bool(re.fullmatch(r"([A-Z]\.)+", last))
    if not is_abbrev:
        return False
    return is_title or len(words) <= 3


def sentences(text):
    """Split text into sentences, keeping abbreviation periods (e.g. 'Dr.') inside one sentence."""
    parts = re.split(r"(?<=[.!?])\s+|(?<=[.!?])(?=\")", text.strip())
    parts = [p for p in parts if p.strip()]
    merged = []
    for seg in parts:
        if merged and _is_short_abbrev_segment(merged[-1]):
            merged[-1] = merged[-1] + " " + seg
        else:
            merged.append(seg)
    return merged


def words_of(s):
    """Return the list of alphanumeric word tokens found in a single sentence string."""
    return re.findall(r"[A-Za-z0-9']+", s)


def analyze(text):
    """Compute burstiness metrics (CV, alternation) and a descriptive variation assessment."""
    sents = sentences(text)
    lengths = [len(words_of(s)) for s in sents if words_of(s)]
    n = len(lengths)
    if n < 2:
        return {
            "sentences": n,
            "error": "need >=2 sentences to measure burstiness",
            "language_scope": "english-prose-only",
        }
    mean = statistics.mean(lengths)
    sd = statistics.pstdev(lengths)
    cv = sd / mean if mean else 0.0
    diffs = [abs(lengths[i] - lengths[i - 1]) for i in range(1, n)]
    alt = statistics.mean(diffs) / mean if mean else 0.0
    if n <= 2:
        band = "limited sample (<=2 sentences) - variation needs >=3 sentences"
    elif cv < 0.45:
        band = "uniform - low sentence-length variation"
    elif cv > 1.1:
        band = "highly variable - watch readability"
    else:
        band = "moderate variation"
    return {
        "sentences": n,
        "mean_len": round(mean, 2),
        "std_len": round(sd, 2),
        "cv": round(cv, 3),
        "alternation": round(alt, 3),
        "min": min(lengths),
        "max": max(lengths),
        "band": band,
        "language_scope": "english-prose-only",
    }


def main():
    """CLI entry point: read from a file argument or stdin and print the JSON analysis."""
    text = read_text(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps(analyze(text), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
