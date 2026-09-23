---
name: sepia-opt-burstiness
description: OPTIONAL sepia add-on. Assesses sentence-length variation (burstiness: variance and alternation pattern) as an editorial rhythm diagnostic. Use when the user explicitly asks to assess sentence rhythm or vary sentence length for readability. This skill is OPTIONAL — never auto-load; ask the user before applying.
metadata:
  optional: true
  ask-before-load: true
---

**STOP — THIS SKILL IS DISABLED BY DEFAULT.** Do not perform any operation here unless the user has *explicitly* enabled it in this conversation. If you are unsure whether it was enabled, do nothing and say so instead of guessing.

> ⚠️ **OPTIONAL SKILL — ASK BEFORE USING.**
> This skill is **not** part of core sepia and is **not** loaded by default.
> Before you apply any of its operations, you **MUST** ask the user:
> *"Enable optional burstiness assessment for this document? It measures sentence-length variation and can adjust it for a more varied rhythm; sepia core deliberately does not use this axis."*
> Only proceed if the user says yes. If they decline, do nothing.

# sepia-opt-burstiness (optional)

A standalone, opt-in editorial diagnostic. Human prose varies in sentence length;
mechanically uniform text reads as machine-written. This optional skill measures
that variation — called **burstiness** — as a plain readability signal.

Core sepia intentionally excludes mean sentence length / paragraph length as
signals (the underlying research gives contradictory directions). This optional
skill covers that axis **as a standalone editorial rhythm adjustment** for
readability.

## What it does
- **Diagnose** — run `scripts/measure.py` to report sentence count, mean length,
  coefficient of variation (CV), alternation index, and a variation assessment.
- **Calibrate** — rewrite toward greater sentence-length variation: merge
  consecutive short sentences, split over-long ones, and deliberately alternate
  short/long rhythm instead of a steady beat.

## How to run the diagnostic
```bash
<PY> skills/sepia-opt-burstiness/scripts/measure.py "<file-or-stdin>.txt"
```
- `<PY>` = a Python 3.10+ interpreter (standard library only; no install needed).
- Reads a file path argument, or falls back to stdin.

## Calibration moves (apply only after the user opts in)
1. **Break monotony** — if CV is low (sentences similar in length), merge two
   shorts into one, or split one long into two.
2. **Alternate** — follow a long sentence with a short one; avoid 3+ sentences of
   the same length in a row.
3. **Keep meaning** — calibration must not alter facts, claims, or the user's
   voice beyond rhythm.

## Limitations
- Pure heuristic; the reported bands are descriptive, not validated thresholds.
  The CV reference range (≈0.45–1.1) is an illustrative editorial reference,
  **not** a figure derived from this project's corpus. Treat it as a hint, not a
  target.
- Does **not** guarantee any change in how automated tools score the text.
- **English prose only.** Tokenization is ASCII-oriented and assumes whitespace
  after sentence-ending punctuation (`.`, `!`, `?`); non-English text is out of
  scope for this version.
- Not a substitute for sepia's structural passes; use alongside, not instead of.
