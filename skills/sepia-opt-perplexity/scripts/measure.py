#!/usr/bin/env python3
"""Perplexity-proxy diagnostic for the optional sepia-opt-perplexity skill.

Standard library only. Estimates lexical "surprise" with stylometric proxies
(true perplexity needs an LLM):
  - type-token ratio (TTR)
  - rare-word ratio vs. a small common-English list
  - character-bigram self-entropy (bits)
Directional only; do not treat as an exact perplexity score. English prose only.
"""
import sys
import re
import json
import math
from collections import Counter

COMMON = set(
    """the be to of and a in that have i it for not on with he as you do at this but
    his by from they we say her she or an will my one all would there their what so
    up out if about who get which go me when make can like time no just him know take
    people into year your good some could them see other than then now look only come
    its over think also back after use two how our work first well way even new want
    because any these give day most us""".split()
)


def read_text(path):
    """Read input text from a file path, or fall back to stdin when no path is given."""
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def words(text):
    """Tokenize text into lowercased word tokens, stripping punctuation."""
    return [w.lower() for w in re.findall(r"[a-z']+", text.lower())]


def analyze(text):
    """Estimate lexical surprise via TTR, rare-word ratio, and char-bigram entropy; return a descriptive assessment."""
    toks = words(text)
    n = len(toks)
    if n == 0:
        return {"error": "empty text", "language_scope": "english-prose-only"}
    types = set(toks)
    ttr = len(types) / n
    rare = [w for w in toks if w not in COMMON]
    rare_ratio = len(rare) / n
    chars = re.sub(r"\s+", "", text.lower())
    bigrams = [chars[i : i + 2] for i in range(len(chars) - 1)]
    if bigrams:
        cnt = Counter(bigrams)
        total = len(bigrams)
        H = -sum((c / total) * math.log2(c / total) for c in cnt.values())
    else:
        H = 0.0
    min_tokens = 5
    if n < min_tokens:
        band = "insufficient sample (need >=%d tokens) - metrics only" % min_tokens
    elif ttr < 0.35 or rare_ratio < 0.45:
        band = "low lexical variety - may read as over-smooth"
    elif ttr > 0.8:
        band = "high lexical variety - watch readability"
    else:
        band = "moderate lexical variety"
    return {
        "tokens": n,
        "ttr": round(ttr, 3),
        "rare_word_ratio": round(rare_ratio, 3),
        "char_bigram_entropy_bits": round(H, 3),
        "band": band,
        "language_scope": "english-prose-only",
        "note": "Proxy only; true perplexity requires an LM (TTR + rare-word ratio + self-entropy).",
    }


def main():
    """CLI entry point: read from a file argument or stdin and print the JSON analysis."""
    text = read_text(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps(analyze(text), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
