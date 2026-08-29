# PF3-EVAL-V1 run metadata

This file records the execution contract for the two arms. The grader fields
were populated after both immutable arm artifacts existed.

## Provenance

| Field | Value |
|---|---|
| suite | PF3-EVAL-V1 |
| parent_commit | b5a70677e8cd2ef6eaff828d12ad5ade9eaedc68 |
| plugin_version | 0.2.0 |
| generation_date | 2026-08-30 Asia/Taipei |
| utc_timestamp | 2026-08-29T16:29:57Z |
| grader_role | executor |
| grader_model | gpt-5.6-luna |
| grader_reasoning | configured reasoning max |

## Arm execution

| Field | Value |
|---|---|
| baseline_role | executor |
| baseline_model | gpt-5.6-luna |
| baseline_reasoning | configured reasoning max |
| sepia_role | executor |
| sepia_model | gpt-5.6-luna |
| sepia_reasoning | configured reasoning max |
| agent_isolation | independent fresh agents |
| baseline_forbidden_inputs | `skills/sepia`; `evals/runs/2026-08-30/sepia.md` |
| sepia_forbidden_inputs | `evals/runs/2026-08-30/baseline.md` |
| temperature | not exposed |
| token_cap | not exposed |

## Runner and spend

| Field | Value |
|---|---|
| native_command | `claude plugin eval init --bare` |
| native_runner | claude 2.1.251 early_access_exit_1 |
| external_spend | NONE |

The local native command returned early-access exit 1 on Claude 2.1.251, so
this run uses the checked Markdown arm artifacts rather than a native runner.

## Claim boundary

| Field | Value |
|---|---|
| human_preference | NOT_RUN |
| statistical_efficacy | NOT_CLAIMED |
| detector_accuracy | NOT_CLAIMED |
| generalization | NOT_CLAIMED |

The result is descriptive for this run and does not measure human preference,
human-likeness, statistical efficacy, detector accuracy, causality, or
generalization.
