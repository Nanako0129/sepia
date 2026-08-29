#!/usr/bin/env bash
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
RUN_DIR="$ROOT/runs/2026-08-30"
CASES="$ROOT/cases.md"
META="$RUN_DIR/metadata.md"
BASELINE="$RUN_DIR/baseline.md"
SEPIA="$RUN_DIR/sepia.md"
GRADES="$RUN_DIR/grades.md"

IDS="PF3-F-WRITE PF3-F-REVIEW PF3-F-REFACTOR PF3-F-RECREATE PF3-P-WRITE PF3-P-REVIEW PF3-P-REFACTOR PF3-P-RECREATE"

fail() {
  printf 'CHECK FAILED: %s\n' "$1" >&2
  return 1
}

incomplete() {
  printf 'INCOMPLETE: %s\n' "$1" >&2
  return 1
}

required_literal() {
  file=$1
  literal=$2
  if ! grep -F -q "$literal" "$file"; then
    fail "$file is missing required literal: $literal"
  fi
}

count_occurrences() {
  needle=$1
  file=$2
  awk -v needle="$needle" '
    {
      rest = $0
      while ((pos = index(rest, needle)) > 0) {
        count++
        rest = substr(rest, pos + length(needle))
      }
    }
    END { print count + 0 }
  ' "$file"
}

heading_count() {
  id=$1
  file=$2
  level=${3:-'##[#]?'}
  awk -v id="$id" -v level="$level" '$0 ~ ("^" level "[[:space:]]+" id "([[:space:]]|$)") { count++ } END { print count + 0 }' "$file"
}

section_has_body() {
  id=$1
  file=$2
  level=${3:-'##[#]?'}
  awk -v id="$id" -v level="$level" '
    BEGIN { found = 0; body = 0 }
    $0 ~ ("^" level "[[:space:]]+" id "([[:space:]]|$)") { found = 1; next }
    found && $0 ~ ("^" level "[[:space:]]") { exit }
    found && $0 !~ "^[[:space:]]*$" { body = 1 }
    END { exit !(found && body) }
  ' "$file"
}

section_has_literal() {
  id=$1
  literal=$2
  file=$3
  awk -v id="$id" -v literal="$literal" '
    $0 == "### " id { found = 1; next }
    found && $0 ~ "^###[[:space:]]" { exit }
    found && $0 == literal { matched = 1 }
    END { exit !matched }
  ' "$file"
}

check_inventory() {
  expected=$(printf '%s\n' \
    README.md \
    cases.md \
    check.sh \
    runs/2026-08-30/metadata.md \
    runs/2026-08-30/baseline.md \
    runs/2026-08-30/sepia.md \
    runs/2026-08-30/grades.md | sort)
  actual=$(cd "$ROOT" && find . -type f -print | sed 's#^./##' | sort)
  if [ "$actual" != "$expected" ]; then
    incomplete "expected exactly seven authoritative files; missing arm or grade artifacts may not exist yet (expected: $expected; actual: $actual)"
  fi
}

check_cases() {
  [ -f "$CASES" ] || incomplete "missing cases.md"
  for id in $IDS; do
    case "$id" in
      PF3-F-WRITE) route='| Route | Fiction; `write` |' ;;
      PF3-F-REVIEW) route='| Route | Fiction; `review` |' ;;
      PF3-F-REFACTOR) route='| Route | Fiction; `refactor` |' ;;
      PF3-F-RECREATE) route='| Route | Fiction; `recreate` |' ;;
      PF3-P-WRITE) route='| Route | Professional prose; release notes; `write` |' ;;
      PF3-P-REVIEW) route='| Route | Professional prose; PR reply; `review` |' ;;
      PF3-P-REFACTOR) route='| Route | Professional prose; postmortem; `refactor` |' ;;
      PF3-P-RECREATE) route='| Route | Professional prose; technical article; `recreate` |' ;;
    esac
    [ "$(count_occurrences "$id" "$CASES")" -eq 1 ] || fail "cases.md must contain $id exactly once"
    [ "$(heading_count "$id" "$CASES" '###')" -eq 1 ] || fail "cases.md must contain one H3 section for $id"
    section_has_body "$id" "$CASES" '###' || fail "cases.md section $id is empty"
    section_has_literal "$id" "$route" "$CASES" || fail "cases.md section $id has the wrong route"
  done
  [ "$(grep -F -c '| Original input |' "$CASES")" -eq 8 ] || fail "cases.md must provide eight original inputs"
  [ "$(grep -F -c '| Exact request |' "$CASES")" -eq 8 ] || fail "cases.md must provide eight exact requests"
  [ "$(grep -F -c '| Protected facts / voice |' "$CASES")" -eq 8 ] || fail "cases.md must provide eight protected-facts/voice fields"
  [ "$(grep -F -c '| Human-only questions |' "$CASES")" -eq 8 ] || fail "cases.md must provide eight human-only question fields"
  [ "$(grep -F -c '| Route |' "$CASES")" -eq 8 ] || fail "cases.md must provide eight route fields"
  for invariant in I1 I2 I3 I4; do
    [ "$(grep -F -c "| $invariant |" "$CASES")" -eq 8 ] || fail "cases.md must provide $invariant for all eight cases"
  done
  grep -F -i -q 'no copyrighted passages' "$CASES" || fail "cases.md must state that inputs contain no copyrighted passages"
}

check_arm() {
  arm=$1
  label=$2
  [ -f "$arm" ] || incomplete "missing $label arm artifact"
  [ "$(grep -E -c '^##[[:space:]]+' "$arm")" -eq 8 ] || fail "$label arm must contain exactly eight H2 sections"
  for id in $IDS; do
    [ "$(count_occurrences "$id" "$arm")" -eq 1 ] || fail "$label arm must contain $id exactly once"
    [ "$(heading_count "$id" "$arm" '##')" -eq 1 ] || fail "$label arm must contain one H2 section for $id"
    section_has_body "$id" "$arm" '##' || fail "$label arm section $id is empty"
  done
}

check_grades() {
  [ -f "$GRADES" ] || incomplete "missing grades.md"
  grade_rows=$(awk '
    /^\| ID \|/ { in_table = 1; next }
    in_table && /^\|---/ { next }
    in_table && /^\|/ { count++; next }
    in_table { exit }
    END { print count + 0 }
  ' "$GRADES")
  [ "$grade_rows" -eq 8 ] || fail "grades.md must contain exactly eight grade rows"
  for id in $IDS; do
    [ "$(count_occurrences "$id" "$GRADES")" -eq 1 ] || fail "grades.md must contain $id exactly once"
    row=$(grep -F "$id" "$GRADES")
    printf '%s\n' "$row" | awk -F'|' -v id="$id" '
      {
        if (NF != 18) exit 1
        cell = $2
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", cell)
        if (cell != id) exit 1
        for (i = 3; i < NF; i++) {
          cell = $i
          gsub(/^[[:space:]]+|[[:space:]]+$/, "", cell)
          if (cell !~ /^(PASS|FAIL|NOT_RUN)$/) exit 1
        }
        human = $(NF - 1)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", human)
        if (human != "NOT_RUN") exit 1
      }
    ' || fail "grades.md row for $id must have only PASS|FAIL|NOT_RUN statuses and human-only NOT_RUN"
  done
}

check_metadata() {
  [ -f "$META" ] || incomplete "missing metadata.md"
  required_literal "$META" '| suite | PF3-EVAL-V1 |'
  required_literal "$META" '| parent_commit | b5a70677e8cd2ef6eaff828d12ad5ade9eaedc68 |'
  required_literal "$META" '| plugin_version | 0.2.0 |'
  required_literal "$META" '| generation_date | 2026-08-30 Asia/Taipei |'
  if ! grep -E -q '^\| utc_timestamp \| [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z \|$' "$META"; then
    fail "$META must contain an ISO 8601 UTC timestamp"
  fi
  required_literal "$META" '| baseline_role | executor |'
  required_literal "$META" '| baseline_model | gpt-5.6-luna |'
  required_literal "$META" '| baseline_reasoning | configured reasoning max |'
  required_literal "$META" '| sepia_role | executor |'
  required_literal "$META" '| sepia_model | gpt-5.6-luna |'
  required_literal "$META" '| sepia_reasoning | configured reasoning max |'
  required_literal "$META" '| baseline_forbidden_inputs | direct reads of `skills/sepia`; `.agents/skills/sepia`; `evals/runs/2026-08-30/sepia.md` |'
  required_literal "$META" '| sepia_forbidden_inputs | `evals/runs/2026-08-30/baseline.md` |'
  required_literal "$META" '| temperature | not exposed |'
  required_literal "$META" '| token_cap | not exposed |'
  required_literal "$META" '| agent_isolation | independent fresh agents; cross-arm reads prohibited |'
  required_literal "$META" '| skill_capability_isolation | NOT_PROVEN: host exposed `.agents/skills/sepia` alias |'
  required_literal "$META" '| grader_role | executor |'
  required_literal "$META" '| grader_model | gpt-5.6-luna |'
  required_literal "$META" '| grader_reasoning | configured reasoning max |'
  required_literal "$META" '| native_runner | claude 2.1.251 early_access_exit_1 |'
  required_literal "$META" '| human_preference | NOT_RUN |'
  required_literal "$META" '| statistical_efficacy | NOT_CLAIMED |'
  required_literal "$META" '| detector_accuracy | NOT_CLAIMED |'
  required_literal "$META" '| skill_effect | NOT_CLAIMED |'
  required_literal "$META" '| external_spend | NONE |'
}

check_claim_boundary() {
  for file in "$BASELINE" "$SEPIA" "$GRADES"; do
    if grep -E -i -q 'statistical[[:space:]_-]+efficacy|detector[[:space:]_-]+accuracy|human[-[:space:]]likeness|human[[:space:]_-]+preference|generaliz(e|ation|able)|causal(ity|[[:space:]_-]+claim)' "$file"; then
      fail "$file contains an unsupported efficacy, detector, human-preference, causality, or generalization claim"
    fi
  done
}

run_checks() {
  check_inventory
  check_cases
  check_arm "$BASELINE" baseline
  check_arm "$SEPIA" Sepia
  check_grades
  check_metadata
  check_claim_boundary
  printf 'PF3-EVAL-V1 check: PASS\n'
}

expect_failure() {
  label=$1
  shift
  if "$@" >/dev/null 2>&1; then
    fail "self-test expected $label to fail"
  fi
  printf 'self-test: %s FAIL confirmed\n' "$label"
}

replace_with_sed() {
  file=$1
  expression=$2
  temporary="$file.self-test"
  sed -e "$expression" "$file" > "$temporary"
  mv "$temporary" "$file"
}

self_test() {
  if ! bash "$0" >/dev/null 2>&1; then
    incomplete 'self-test requires the complete seven-file pack; create baseline.md, sepia.md, and grades.md first'
  fi

  temporary_root=$(mktemp -d "${TMPDIR:-/tmp}/pf3-eval-self-test.XXXXXX")
  trap 'rm -rf "$temporary_root"' EXIT HUP INT TERM
  copy_root="$temporary_root/evals"
  cp -R "$ROOT" "$copy_root"
  copy_check="$copy_root/check.sh"
  copy_baseline="$copy_root/runs/2026-08-30/baseline.md"
  copy_cases="$copy_root/cases.md"
  copy_meta="$copy_root/runs/2026-08-30/metadata.md"
  copy_grades="$copy_root/runs/2026-08-30/grades.md"
  backup="$temporary_root/backup"

  cp "$copy_baseline" "$backup"
  rm "$copy_baseline"
  expect_failure 'missing arm' bash "$copy_check"
  cp "$backup" "$copy_baseline"

  cp "$copy_cases" "$backup"
  replace_with_sed "$copy_cases" '/^##[#]* PF3-F-WRITE$/d'
  expect_failure 'missing ID' bash "$copy_check"
  cp "$backup" "$copy_cases"

  cp "$copy_cases" "$backup"
  replace_with_sed "$copy_cases" 's/^### PF3-F-WRITE$/## PF3-F-WRITE/'
  expect_failure 'wrong case heading level' bash "$copy_check"
  cp "$backup" "$copy_cases"

  cp "$copy_cases" "$backup"
  replace_with_sed "$copy_cases" '/^| Route |/d'
  expect_failure 'missing routes' bash "$copy_check"
  cp "$backup" "$copy_cases"

  cp "$copy_cases" "$backup"
  replace_with_sed "$copy_cases" 's/| Route | Fiction; `write` |/| Route | Professional prose; PR reply; `review` |/'
  expect_failure 'wrong route value' bash "$copy_check"
  cp "$backup" "$copy_cases"

  cp "$copy_meta" "$backup"
  replace_with_sed "$copy_meta" 's/| plugin_version | 0.2.0 |/| plugin_version | |/'
  expect_failure 'missing metadata' bash "$copy_check"
  expect_failure 'invalid source self-test' bash "$copy_check" --self-test
  cp "$backup" "$copy_meta"

  cp "$copy_grades" "$backup"
  replace_with_sed "$copy_grades" '/PF3-F-WRITE/s/| NOT_RUN |$/| PASS |/'
  expect_failure 'human-only status' bash "$copy_check"
  cp "$backup" "$copy_grades"

  cp "$copy_grades" "$backup"
  replace_with_sed "$copy_grades" '/PF3-F-WRITE/s/| [A-Z_][A-Z_]* |/| MAYBE |/'
  expect_failure 'invalid status' bash "$copy_check"
  cp "$backup" "$copy_grades"

  cp "$copy_grades" "$backup"
  replace_with_sed "$copy_grades" '/^| PF3-P-RECREATE |/a\
| PF3-EXTRA | MAYBE |'
  expect_failure 'extra grade row' bash "$copy_check"
  cp "$backup" "$copy_grades"

  cp "$copy_baseline" "$backup"
  printf '\n## PF3-EXTRA\n\nUnexpected extra arm section.\n' >> "$copy_baseline"
  expect_failure 'extra arm section' bash "$copy_check"
  cp "$backup" "$copy_baseline"

  printf 'PF3-EVAL-V1 self-test: PASS\n'
}

case "${1:-}" in
  '') run_checks ;;
  --self-test) self_test ;;
  *)
    printf 'usage: %s [--self-test]\n' "$0" >&2
    exit 2
    ;;
esac
