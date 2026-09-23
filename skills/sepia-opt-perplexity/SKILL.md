---
name: sepia-opt-perplexity
description: OPTIONAL sepia add-on. Estimates a perplexity proxy (lexical surprise via type-token ratio, rare-word ratio, self-entropy) as an editorial lexical-variety diagnostic. Use when the user explicitly asks to assess lexical variety or reduce over-smooth wording. This skill is OPTIONAL — never auto-load; ask the user before applying.
metadata:
  optional: true
  ask-before-load: true
---

**STOP — THIS SKILL IS DISABLED BY DEFAULT.** Do not perform any operation here unless the user has *explicitly* enabled it in this conversation. If you are unsure whether it was enabled, do nothing and say so instead of guessing.

> ⚠️ **OPTIONAL SKILL — ASK BEFORE USING.**
> This skill is **not** part of core sepia and is **not** loaded by default.
> Before you apply any of its operations, you **MUST** ask the user:
> *"Enable optional lexical-variety assessment for this document? It estimates a perplexity proxy and can suggest more varied wording; sepia core deliberately does not use this axis."*
> Only proceed if the user says yes. If they decline, do nothing.

# sepia-opt-perplexity (optional)

Prose that is over-smooth and predictable tends to read as machine-written. Human
writing usually shows more lexical surprise. This optional skill estimates a
**perplexity proxy** with no external model and reports it as an editorial
lexical-variety signal.

> **Note:** a true perplexity score needs an LLM API. This skill uses lightweight
> stylometric proxies — type-token ratio, rare-word ratio against a common-word
> list, and character-bigram self-entropy. Treat the numbers as *directional*,
> not exact.

## What it does
- **Diagnose** — run `scripts/measure.py` for TTR, rare-word ratio, self-entropy,
  and a variation assessment.
- **Calibrate** — raise lexical variety without breaking clarity: replace vague
  common words with precise/concrete ones, vary syntax, add specifics.

## How to run the diagnostic
```bash
<PY> skills/sepia-opt-perplexity/scripts/measure.py "<file-or-stdin>.txt"
```
- `<PY>` = a Python 3.10+ interpreter (standard library only; no install needed).

## Calibration moves (apply only after the user opts in)
1. Swap generic verbs/nouns for specific ones (e.g., "utilize" → "wield",
   "thing" → a named entity).
2. Vary sentence openers and clause order.
3. Add concrete detail where the text is abstract — but never invent facts.

## Limitations
- Proxy only; real perplexity requires an LM.
- The reported bands are descriptive, not validated thresholds. The TTR and
  rare-word cutoffs are illustrative editorial references, **not** figures
  derived from this project's corpus.
- More "surprise" is not always better — over-rare words hurt readability.
- **English prose only.** Tokenization accepts only `[a-z']+`; non-English text
  is out of scope for this version.
- Does **not** guarantee any change in how automated tools score the text.
