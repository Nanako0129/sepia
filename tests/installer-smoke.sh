#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
TEST_TMPDIR="${TMPDIR:-/tmp}"
TMP="$(mktemp -d "${TEST_TMPDIR%/}/sepia-installer-test.XXXXXX")"
trap 'rm -rf -- "$TMP"' EXIT
export GIT_ALLOW_PROTOCOL=file

pass=0
fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

ok() {
  pass=$((pass + 1))
  printf 'ok %02d - %s\n' "$pass" "$1"
}

make_home() {
  CASE_HOME="$TMP/homes/$1"
  CASE_CLONE="$TMP/clones/$1"
  mkdir -p "$CASE_HOME" "$(dirname "$CASE_CLONE")"
}

snapshot_tree() {
  local root="$1" output="$2" list="$TMP/tree-list" path relative hash
  find "$root" -mindepth 1 -print | LC_ALL=C sort >"$list"
  : >"$output"
  while IFS= read -r path; do
    relative="${path#"$root"/}"
    if [ -L "$path" ]; then
      printf 'l %s %s\n' "$(readlink "$path")" "$relative" >>"$output"
    elif [ -d "$path" ]; then
      printf 'd %s\n' "$relative" >>"$output"
    elif [ -f "$path" ]; then
      hash="$(shasum -a 256 "$path" | awk '{print $1}')"
      printf 'f %s %s\n' "$hash" "$relative" >>"$output"
    else
      fail "unsupported test path type: $path"
    fi
  done <"$list"
}

install_from_bootstrap() {
  HOME="$1" SEPIA_HOME="$2" SEPIA_REPO="$3" SEPIA_REF="$4" bash "$BOOTSTRAP"
}

assert_reject_bootstrap() {
  local name="$1" home="$2" clone="$3" repo="$4" ref="$5" before="$TMP/before-$1" after="$TMP/after-$1"
  snapshot_tree "$home" "$before"
  if install_from_bootstrap "$home" "$clone" "$repo" "$ref" >"$TMP/$name.out" 2>&1; then
    fail "$name unexpectedly succeeded"
  fi
  snapshot_tree "$home" "$after"
  cmp -s "$before" "$after" || fail "$name changed a destination"
  ok "$name rejects before destination writes"
}

assert_reject_uninstall() {
  local name="$1" home="$2" clone="$3" repo="$4" ref="$5" before="$TMP/before-$1" after="$TMP/after-$1"
  snapshot_tree "$home" "$before"
  if HOME="$home" SEPIA_HOME="$clone" SEPIA_REPO="$repo" SEPIA_REF="$ref" SEPIA_ACTION=uninstall \
    bash "$BOOTSTRAP" >"$TMP/$name.out" 2>&1; then
    fail "$name uninstall unexpectedly succeeded"
  fi
  snapshot_tree "$home" "$after"
  cmp -s "$before" "$after" || fail "$name uninstall changed a destination"
  ok "$name uninstall preserves every destination"
}

make_clone() {
  git clone -q "$ORIGIN" "$1"
  git -C "$1" checkout -q --detach "$2"
}

SOURCE="$TMP/source"
mkdir -p "$SOURCE/skills" "$SOURCE/.agents/workflows"
cp "$ROOT/install.sh" "$SOURCE/install.sh"
chmod 755 "$SOURCE/install.sh"
cp -R "$ROOT/skills/sepia" "$SOURCE/skills/sepia"
cp "$ROOT/.agents/workflows/sepia.md" "$SOURCE/.agents/workflows/sepia.md"
git -C "$SOURCE" init -q
git -C "$SOURCE" config user.name 'Sepia Installer Test'
git -C "$SOURCE" config user.email 'installer-test@example.invalid'
git -C "$SOURCE" add .
git -C "$SOURCE" commit -qm 'fixture v1'
REF1="$(git -C "$SOURCE" rev-parse HEAD)"

ORIGIN="$TMP/origin.git"
git clone -q --bare "$SOURCE" "$ORIGIN"
git -C "$SOURCE" remote add origin "$ORIGIN"
printf '\nfixture revision two\n' >>"$SOURCE/skills/sepia/SKILL.md"
git -C "$SOURCE" add skills/sepia/SKILL.md
git -C "$SOURCE" commit -qm 'fixture v2'
REF2="$(git -C "$SOURCE" rev-parse HEAD)"
git -C "$SOURCE" push -q origin HEAD

BOOTSTRAP="$TMP/install.sh"
cp "$ROOT/install.sh" "$BOOTSTRAP"
chmod 755 "$BOOTSTRAP"

make_home clean
install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF1" >/dev/null
for path in .claude/skills/sepia .agents/skills/sepia .grok/skills/sepia; do
  [ -L "$CASE_HOME/$path" ] || fail "clean install did not create $path symlink"
  [ "$(cd "$CASE_HOME/$path" && pwd -P)" = "$(cd "$CASE_CLONE/skills/sepia" && pwd -P)" ] ||
    fail "$path does not use the canonical skill"
done
[ -f "$CASE_HOME/.gemini/config/skills/sepia/.sepia-install-state" ] || fail 'Antigravity skill is unmarked'
[ -f "$CASE_HOME/.gemini/config/skills/sepia/.sepia-install-manifest" ] || fail 'Antigravity skill lacks a manifest'
[ -f "$CASE_HOME/.gemini/antigravity/global_workflows/sepia.md.sepia-install-state" ] || fail 'workflow is unmarked'
ok 'clean local-file bootstrap install'

install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2" >/dev/null
[ "$(git -C "$CASE_CLONE" rev-parse HEAD)" = "$REF2" ] || fail 'managed update did not select REF2'
grep -q 'fixture revision two' "$CASE_HOME/.gemini/config/skills/sepia/SKILL.md" || fail 'managed copy did not update'
grep -q "revision=$REF2" "$CASE_HOME/.gemini/config/skills/sepia/.sepia-install-state" || fail 'managed state did not update'
ok 'repeat managed update'

make_home regular_file
mkdir -p "$CASE_HOME/.claude/skills"
printf 'sentinel\n' >"$CASE_HOME/.claude/skills/sepia"
assert_reject_bootstrap regular_file "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home nonempty_dir
mkdir -p "$CASE_HOME/.agents/skills/sepia"
printf 'sentinel\n' >"$CASE_HOME/.agents/skills/sepia/keep"
assert_reject_bootstrap nonempty_dir "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home wrong_symlink
mkdir -p "$CASE_HOME/.grok/skills" "$CASE_HOME/target"
printf 'sentinel\n' >"$CASE_HOME/target/keep"
ln -s "$CASE_HOME/target" "$CASE_HOME/.grok/skills/sepia"
assert_reject_bootstrap wrong_symlink "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home workflow_symlink
mkdir -p "$CASE_HOME/.gemini/antigravity/global_workflows"
printf 'sentinel\n' >"$CASE_HOME/workflow-target"
ln -s "$CASE_HOME/workflow-target" "$CASE_HOME/.gemini/antigravity/global_workflows/sepia.md"
assert_reject_bootstrap workflow_symlink "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home legacy_skill
mkdir -p "$CASE_HOME/.gemini/config/skills"
cp -R "$SOURCE/skills/sepia" "$CASE_HOME/.gemini/config/skills/sepia"
assert_reject_bootstrap legacy_unmarked_skill "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home legacy_workflow
mkdir -p "$CASE_HOME/.gemini/antigravity/global_workflows"
cp "$SOURCE/.agents/workflows/sepia.md" "$CASE_HOME/.gemini/antigravity/global_workflows/sepia.md"
assert_reject_bootstrap legacy_unmarked_workflow "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home modified_skill
install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2" >/dev/null
printf 'local edit\n' >>"$CASE_HOME/.gemini/config/skills/sepia/SKILL.md"
assert_reject_bootstrap modified_managed_skill "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home modified_workflow
install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2" >/dev/null
printf 'local edit\n' >>"$CASE_HOME/.gemini/antigravity/global_workflows/sepia.md"
assert_reject_bootstrap modified_managed_workflow "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home foreign_origin
make_clone "$CASE_CLONE" "$REF2"
git -C "$CASE_CLONE" remote set-url origin "$TMP/foreign.git"
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap foreign_origin "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home dirty_checkout
make_clone "$CASE_CLONE" "$REF2"
printf 'dirty\n' >>"$CASE_CLONE/skills/sepia/SKILL.md"
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap dirty_checkout "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home untracked_checkout
make_clone "$CASE_CLONE" "$REF2"
printf 'untracked\n' >"$CASE_CLONE/untracked"
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap untracked_checkout "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home symlinked_installer
make_clone "$CASE_CLONE" "$REF2"
rm "$CASE_CLONE/install.sh"
ln -s skills/sepia/SKILL.md "$CASE_CLONE/install.sh"
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap symlinked_installer "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home invalid_revision
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap invalid_revision "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" main

make_home nonfull_revision
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap nonfull_revision "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "${REF2%?}"

make_home unsafe_repo_transport
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap unsafe_repo_transport "$CASE_HOME" "$CASE_CLONE" 'ext::sh -c id' "$REF2"

make_home overlapping_home
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap overlapping_home "$CASE_HOME" "$CASE_HOME/.claude/skills/sepia/checkout" "$ORIGIN" "$REF2"

make_home head_mismatch
make_clone "$CASE_CLONE" "$REF1"
printf 'sentinel\n' >"$CASE_HOME/keep"
before="$TMP/before-head-mismatch"
after="$TMP/after-head-mismatch"
snapshot_tree "$CASE_HOME" "$before"
if HOME="$CASE_HOME" SEPIA_HOME="$CASE_CLONE" SEPIA_REPO="$ORIGIN" SEPIA_REF="$REF2" \
  bash "$CASE_CLONE/install.sh" >"$TMP/head_mismatch.out" 2>&1; then
  fail 'HEAD mismatch unexpectedly succeeded'
fi
snapshot_tree "$CASE_HOME" "$after"
cmp -s "$before" "$after" || fail 'HEAD mismatch changed a destination'
ok 'HEAD/revision mismatch rejects before destination writes'

BAD_SOURCE="$TMP/bad-source"
mkdir -p "$BAD_SOURCE/skills/sepia" "$BAD_SOURCE/.agents/workflows"
cp "$ROOT/skills/sepia/SKILL.md" "$BAD_SOURCE/skills/sepia/SKILL.md"
cp "$ROOT/.agents/workflows/sepia.md" "$BAD_SOURCE/.agents/workflows/sepia.md"
ln -s skills/sepia/SKILL.md "$BAD_SOURCE/install.sh"
git -C "$BAD_SOURCE" init -q
git -C "$BAD_SOURCE" config user.name 'Sepia Installer Test'
git -C "$BAD_SOURCE" config user.email 'installer-test@example.invalid'
git -C "$BAD_SOURCE" add .
git -C "$BAD_SOURCE" commit -qm 'bad installer type'
BAD_REF="$(git -C "$BAD_SOURCE" rev-parse HEAD)"
BAD_ORIGIN="$TMP/bad-origin.git"
git clone -q --bare "$BAD_SOURCE" "$BAD_ORIGIN"
make_home bad_installer_type
printf 'sentinel\n' >"$CASE_HOME/keep"
assert_reject_bootstrap unexpected_installer_type "$CASE_HOME" "$CASE_CLONE" "$BAD_ORIGIN" "$BAD_REF"

make_home downloaded_mismatch
printf 'sentinel\n' >"$CASE_HOME/keep"
MISMATCH_BOOTSTRAP="$TMP/mismatched-install.sh"
cp "$BOOTSTRAP" "$MISMATCH_BOOTSTRAP"
printf '\n# changed after publication\n' >>"$MISMATCH_BOOTSTRAP"
before="$TMP/before-downloaded-mismatch"
after="$TMP/after-downloaded-mismatch"
snapshot_tree "$CASE_HOME" "$before"
if HOME="$CASE_HOME" SEPIA_HOME="$CASE_CLONE" SEPIA_REPO="$ORIGIN" SEPIA_REF="$REF2" \
  bash "$MISMATCH_BOOTSTRAP" >"$TMP/downloaded_mismatch.out" 2>&1; then
  fail 'downloaded installer mismatch unexpectedly succeeded'
fi
snapshot_tree "$CASE_HOME" "$after"
cmp -s "$before" "$after" || fail 'downloaded installer mismatch changed a destination'
ok 'downloaded installer bytes must match the selected revision'

make_home clean_uninstall
install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2" >/dev/null
target_hash="$(git -C "$CASE_CLONE" hash-object skills/sepia/SKILL.md)"
HOME="$CASE_HOME" SEPIA_HOME="$CASE_CLONE" SEPIA_REPO="$ORIGIN" SEPIA_REF="$REF2" SEPIA_ACTION=uninstall \
  bash "$BOOTSTRAP" >/dev/null
for path in .claude/skills/sepia .agents/skills/sepia .grok/skills/sepia .gemini/config/skills/sepia \
  .gemini/antigravity/global_workflows/sepia.md .gemini/antigravity/global_workflows/sepia.md.sepia-install-state; do
  [ ! -e "$CASE_HOME/$path" ] && [ ! -L "$CASE_HOME/$path" ] || fail "clean uninstall left $path"
done
[ "$(git -C "$CASE_CLONE" hash-object skills/sepia/SKILL.md)" = "$target_hash" ] || fail 'uninstall changed the symlink target checkout'
ok 'safe uninstall removes only clean managed artifacts'

make_home uninstall_modified
install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2" >/dev/null
printf 'local edit\n' >>"$CASE_HOME/.gemini/config/skills/sepia/SKILL.md"
assert_reject_uninstall uninstall_modified "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home uninstall_replacement
install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2" >/dev/null
rm "$CASE_HOME/.claude/skills/sepia"
printf 'replacement\n' >"$CASE_HOME/.claude/skills/sepia"
assert_reject_uninstall uninstall_unmanaged_replacement "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home uninstall_wrong_link
install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2" >/dev/null
rm "$CASE_HOME/.grok/skills/sepia"
mkdir -p "$CASE_HOME/wrong-target"
printf 'target sentinel\n' >"$CASE_HOME/wrong-target/keep"
ln -s "$CASE_HOME/wrong-target" "$CASE_HOME/.grok/skills/sepia"
assert_reject_uninstall uninstall_wrong_final_symlink "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

make_home uninstall_legacy
install_from_bootstrap "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2" >/dev/null
rm "$CASE_HOME/.gemini/antigravity/global_workflows/sepia.md.sepia-install-state"
assert_reject_uninstall uninstall_legacy_unmarked "$CASE_HOME" "$CASE_CLONE" "$ORIGIN" "$REF2"

printf 'PASS: %d installer safety checks\n' "$pass"
