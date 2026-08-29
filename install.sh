#!/usr/bin/env bash
# Install or uninstall Sepia at user scope for Claude Code, Codex, Grok Build,
# and Antigravity. See README.md for the SHA-pinned bootstrap command.
set -euo pipefail
umask 077

REPO_URL="${SEPIA_REPO:-https://github.com/Nanako0129/sepia.git}"
CLONE_DIR="${SEPIA_HOME:-${HOME:-}/.sepia}"
REF="${SEPIA_REF:-}"
ACTION="${SEPIA_ACTION:-install}"
OWNER="sepia-installer-v1"
STATE_NAME=".sepia-install-state"
MANIFEST_NAME=".sepia-install-manifest"
SCRIPT_SRC="${BASH_SOURCE[0]:-}"

export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null

die() {
  printf 'sepia installer: %s\n' "$*" >&2
  exit 1
}

collision() {
  printf 'sepia installer: refusing to change %s: %s\n' "$1" "$2" >&2
  printf 'Move the path aside, or restore its Sepia ownership metadata and installed content, then rerun. No destination was changed.\n' >&2
  exit 1
}

git_safe() {
  git -c core.hooksPath=/dev/null -c core.fsmonitor=false "$@"
}

sha256_file() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    sha256sum "$1" | awk '{print $1}'
  fi
}

validate_inputs() {
  [ -n "${HOME:-}" ] || die 'HOME is empty'
  case "$HOME" in /*) ;; *) die 'HOME must be an absolute path' ;; esac
  [ "$HOME" != / ] || die 'HOME cannot be /'
  [ -d "$HOME" ] && [ ! -L "$HOME" ] || die 'HOME must be a real directory, not a symlink'

  case "$CLONE_DIR" in /*) ;; *) die 'SEPIA_HOME must be an absolute path' ;; esac
  [ "$CLONE_DIR" != / ] && [ "$CLONE_DIR" != "$HOME" ] || die 'SEPIA_HOME is too broad'
  case "$CLONE_DIR" in *$'\n'*) die 'SEPIA_HOME cannot contain a newline' ;; esac
  case "$CLONE_DIR/" in *//*|*/./*|*/../*) die 'SEPIA_HOME must be a normalized path without //, ., or .. segments' ;; esac

  [ -n "$REPO_URL" ] || die 'SEPIA_REPO is empty'
  case "$REPO_URL" in -*|*$'\n'*) die 'SEPIA_REPO is invalid' ;; esac
  case "$REPO_URL" in
    https://*|ssh://*|git@*:*|file://*|/*) ;;
    *) die 'SEPIA_REPO must use HTTPS, SSH, or an explicit local/file path' ;;
  esac
  [[ "$REF" =~ ^[0-9A-Fa-f]{40}$ ]] || die 'SEPIA_REF must be one full 40-hex commit SHA; branches and tags are not accepted'
  REF="$(printf '%s' "$REF" | tr 'A-F' 'a-f')"
  case "$ACTION" in install|uninstall) ;; *) die 'SEPIA_ACTION must be install or uninstall' ;; esac

  command -v git >/dev/null 2>&1 || die 'git is required'
  command -v awk >/dev/null 2>&1 || die 'awk is required'
  command -v cmp >/dev/null 2>&1 || die 'cmp is required'
  command -v find >/dev/null 2>&1 || die 'find is required'
  command -v sort >/dev/null 2>&1 || die 'sort is required'
  if ! command -v shasum >/dev/null 2>&1 && ! command -v sha256sum >/dev/null 2>&1; then
    die 'shasum or sha256sum is required'
  fi
}

verify_installer_entry() {
  local root="$1" revision="$2" entry mode type oid path
  entry="$(git_safe -C "$root" ls-tree "$revision" -- install.sh)"
  read -r mode type oid path <<<"$entry"
  [ "$mode" = 100755 ] && [ "$type" = blob ] && [ "$path" = install.sh ] ||
    die "revision $revision does not contain install.sh as an executable regular file"
  printf '%s\n' "$oid"
}

verify_running_installer() {
  local root="$1" revision="$2" oid
  oid="$(verify_installer_entry "$root" "$revision")"
  [ "$(git_safe -C "$root" hash-object --no-filters -- "$SCRIPT_SRC")" = "$oid" ]
}

verify_origin() {
  local root="$1" origins
  origins="$(git_safe -C "$root" config --local --get-all remote.origin.url || true)"
  [ "$origins" = "$REPO_URL" ] || die "$root has a foreign or ambiguous origin; expected exactly $REPO_URL"
}

verify_payload() {
  local root="$1" revision="$2" record metadata mode type oid path relative entry flag actual_oid
  local expected_count=0 actual_count=0 found_installer=0 found_skill=0 found_workflow=0

  while IFS= read -r -d '' record; do
    flag="${record%% *}"
    case "$flag" in
      [a-z]|S) die "$root payload index contains assume-unchanged or skip-worktree flags" ;;
    esac
  done < <(git_safe -C "$root" ls-files -z -v -- install.sh skills/sepia .agents/workflows/sepia.md)

  while IFS= read -r -d '' record; do
    metadata="${record%%$'\t'*}"
    path="${record#*$'\t'}"
    read -r mode type oid <<<"$metadata"
    [ "$type" = blob ] || die "revision $revision payload contains a non-file entry: $path"
    case "$path" in
      install.sh)
        [ "$mode" = 100755 ] || die "revision $revision does not contain install.sh as an executable regular file"
        found_installer=1
        ;;
      skills/sepia/*)
        case "$mode" in 100644|100755) ;; *) die "revision $revision payload has an unsupported mode at $path" ;; esac
        [ "$path" = skills/sepia/SKILL.md ] && found_skill=1
        ;;
      .agents/workflows/sepia.md)
        case "$mode" in 100644|100755) ;; *) die "revision $revision payload has an unsupported mode at $path" ;; esac
        found_workflow=1
        ;;
      *) die "revision $revision payload has an unexpected path: $path" ;;
    esac
    expected_count=$((expected_count + 1))
  done < <(git_safe -C "$root" ls-tree -r -z --full-tree "$revision" -- install.sh skills/sepia .agents/workflows/sepia.md)

  [ "$found_installer" = 1 ] || die "revision $revision is missing install.sh"
  [ "$found_skill" = 1 ] || die "revision $revision is missing skills/sepia/SKILL.md"
  [ "$found_workflow" = 1 ] || die "revision $revision is missing .agents/workflows/sepia.md"
  [ -d "$root/skills/sepia" ] && [ ! -L "$root/skills/sepia" ] || die "$root/skills/sepia must be a real directory"
  [ -e "$root/install.sh" ] || [ -L "$root/install.sh" ] || die "$root/install.sh is missing"
  [ -e "$root/.agents/workflows/sepia.md" ] || [ -L "$root/.agents/workflows/sepia.md" ] ||
    die "$root/.agents/workflows/sepia.md is missing"

  while IFS= read -r -d '' path; do
    relative="${path#"$root"/}"
    entry="$(git_safe -C "$root" ls-tree "$revision" -- ":(literal)$relative")"
    [ -n "$entry" ] || die "$root payload has an unexpected path: $relative"
    read -r mode type oid _ <<<"$entry"
    [ "$type" = blob ] && [ -f "$path" ] && [ ! -L "$path" ] ||
      die "$root payload path has an unexpected type: $relative"
    case "$mode" in
      100755) [ -x "$path" ] || die "$root payload path must be executable: $relative" ;;
      100644) [ ! -x "$path" ] || die "$root payload path must not be executable: $relative" ;;
      *) die "revision $revision payload has an unsupported mode at $relative" ;;
    esac
    actual_oid="$(git_safe -C "$root" hash-object --no-filters -- "$relative")"
    [ "$actual_oid" = "$oid" ] || die "$root payload does not match revision $revision: $relative"
    actual_count=$((actual_count + 1))
  done < <(find "$root/install.sh" "$root/skills/sepia" "$root/.agents/workflows/sepia.md" -mindepth 0 ! -type d -print0)

  [ "$actual_count" = "$expected_count" ] || die "$root payload paths do not match revision $revision"
}

verify_clean_checkout() {
  local root="$1" expected="$2" head
  if [ -L "$root/.git" ] || { [ ! -d "$root/.git" ] && [ ! -f "$root/.git" ]; }; then
    die "$root/.git has an unexpected type"
  fi
  git_safe -C "$root" rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "$root is not a Git checkout"
  verify_origin "$root"
  [ -z "$(git_safe -C "$root" status --porcelain=v1 --untracked-files=all)" ] ||
    die "$root is dirty or contains untracked files; refusing to execute or replace its installer"
  head="$(git_safe -C "$root" rev-parse 'HEAD^{commit}')"
  [ "$head" = "$expected" ] || die "$root HEAD $head does not match SEPIA_REF $expected"
  verify_payload "$root" "$expected"
}

snapshot_dir() {
  local dir="$1" output="$2" list path hash status
  list="$(mktemp "${TMPDIR:-/tmp}/sepia-list.XXXXXX")"
  : >"$output"
  (
    cd "$dir"
    find . -mindepth 1 ! -path "./$STATE_NAME" ! -path "./$MANIFEST_NAME" -print | LC_ALL=C sort >"$list"
    while IFS= read -r path; do
      if [ -L "$path" ]; then
        return 1
      elif [ -d "$path" ]; then
        printf 'd  %s\n' "$path" >>"$output"
      elif [ -f "$path" ]; then
        hash="$(sha256_file "$path")"
        printf 'f %s %s\n' "$hash" "$path" >>"$output"
      else
        return 1
      fi
    done <"$list"
  )
  status=$?
  rm -f "$list"
  return "$status"
}

valid_state() {
  local state="$1" owner revision lines
  [ -f "$state" ] && [ ! -L "$state" ] || return 1
  owner="$(sed -n '1p' "$state")"
  revision="$(sed -n '2p' "$state")"
  lines="$(wc -l <"$state" | tr -d ' ')"
  [ "$owner" = "owner=$OWNER" ] && [[ "$revision" =~ ^revision=[0-9a-f]{40}$ ]] && [ "$lines" = 2 ]
}

preflight_parent() {
  local path="$1" parent
  case "$path" in "$HOME"/*) ;; *) die "destination escapes HOME: $path" ;; esac
  parent="$(dirname "$path")"
  while [ "$parent" != "$HOME" ]; do
    if [ -L "$parent" ]; then
      collision "$path" "parent $parent is a symlink"
    elif [ -e "$parent" ] && [ ! -d "$parent" ]; then
      collision "$path" "parent $parent is not a directory"
    fi
    parent="$(dirname "$parent")"
  done
}

resolved_link() {
  local link="$1" target
  target="$(readlink "$link")" || return 1
  (cd "$(dirname "$link")" && cd "$target" 2>/dev/null && pwd -P)
}

preflight_link() {
  local target="$1" destination="$2" resolved expected
  preflight_parent "$destination"
  if [ -L "$destination" ]; then
    resolved="$(resolved_link "$destination")" || collision "$destination" 'symlink target is missing or not a directory'
    expected="$(cd "$target" && pwd -P)"
    [ "$resolved" = "$expected" ] || collision "$destination" "symlink does not resolve to $expected"
  elif [ -e "$destination" ]; then
    collision "$destination" 'only an absent path or the expected Sepia symlink is managed'
  fi
}

preflight_skill_copy() {
  local destination="$1" manifest
  preflight_parent "$destination"
  if [ ! -e "$destination" ] && [ ! -L "$destination" ]; then
    return
  fi
  [ -d "$destination" ] && [ ! -L "$destination" ] || collision "$destination" 'managed Antigravity skill must be a real directory'
  valid_state "$destination/$STATE_NAME" || collision "$destination" 'ownership state is missing or invalid'
  [ -f "$destination/$MANIFEST_NAME" ] && [ ! -L "$destination/$MANIFEST_NAME" ] ||
    collision "$destination" 'content manifest is missing or invalid'
  manifest="$(mktemp "${TMPDIR:-/tmp}/sepia-manifest.XXXXXX")"
  if ! snapshot_dir "$destination" "$manifest" || ! cmp -s "$manifest" "$destination/$MANIFEST_NAME"; then
    rm -f "$manifest"
    collision "$destination" 'managed copy was modified'
  fi
  rm -f "$manifest"
}

preflight_workflow() {
  local workflow="$1" state="$2" expected_hash actual_hash revision lines
  preflight_parent "$workflow"
  preflight_parent "$state"
  if [ ! -e "$workflow" ] && [ ! -L "$workflow" ]; then
    [ ! -e "$state" ] && [ ! -L "$state" ] || collision "$state" 'orphaned workflow ownership state'
    return
  fi
  [ -f "$workflow" ] && [ ! -L "$workflow" ] || collision "$workflow" 'managed workflow must be a regular file, not a symlink'
  [ -f "$state" ] && [ ! -L "$state" ] || collision "$workflow" 'workflow ownership state is missing or invalid'
  [ "$(sed -n '1p' "$state")" = "owner=$OWNER" ] || collision "$workflow" 'workflow owner is invalid'
  revision="$(sed -n '2p' "$state")"
  expected_hash="$(sed -n '3p' "$state")"
  lines="$(wc -l <"$state" | tr -d ' ')"
  [[ "$revision" =~ ^revision=[0-9a-f]{40}$ ]] && [[ "$expected_hash" =~ ^sha256=[0-9a-f]{64}$ ]] && [ "$lines" = 3 ] ||
    collision "$workflow" 'workflow ownership state is invalid'
  actual_hash="$(sha256_file "$workflow")"
  [ "sha256=$actual_hash" = "$expected_hash" ] || collision "$workflow" 'managed workflow was modified'
}

validate_clone_location() {
  local destination
  for destination in "$CLAUDE" "$CODEX" "$GROK" "$AG" "$WF" "$WF_STATE"; do
    case "$CLONE_DIR/" in "$destination/"*) die "SEPIA_HOME cannot be inside destination $destination" ;; esac
    case "$destination/" in "$CLONE_DIR/"*) die "destination $destination cannot be inside SEPIA_HOME" ;; esac
  done
}

preflight_all() {
  local skill="$1"
  preflight_link "$skill" "$CLAUDE"
  preflight_link "$skill" "$CODEX"
  preflight_link "$skill" "$GROK"
  preflight_skill_copy "$AG"
  preflight_workflow "$WF" "$WF_STATE"
}

prepare_checkout() {
  local destination="$1" temp fetched
  mkdir -p "$(dirname "$destination")"
  temp="$(mktemp -d "${destination}.tmp.XXXXXX")"
  git_safe init -q "$temp"
  git_safe -C "$temp" remote add origin "$REPO_URL"
  if ! git_safe -C "$temp" fetch -q --depth 1 origin "$REF"; then
    rm -rf -- "$temp"
    die "cannot fetch commit $REF from $REPO_URL"
  fi
  fetched="$(git_safe -C "$temp" rev-parse 'FETCH_HEAD^{commit}')"
  [ "$fetched" = "$REF" ] || { rm -rf -- "$temp"; die "fetched commit $fetched does not match SEPIA_REF $REF"; }
  if ! verify_running_installer "$temp" "$REF"; then
    rm -rf -- "$temp"
    die 'running installer bytes do not match install.sh at SEPIA_REF'
  fi
  git_safe -C "$temp" checkout -q --detach "$REF"
  verify_clean_checkout "$temp" "$REF"
  printf '%s\n' "$temp"
}

bootstrap() {
  local expected_skill="$CLONE_DIR/skills/sepia" temp backup failed current
  if [ -e "$CLONE_DIR" ] || [ -L "$CLONE_DIR" ]; then
    [ -d "$CLONE_DIR" ] && [ ! -L "$CLONE_DIR" ] || die "$CLONE_DIR exists but is not a real directory"
    [ -d "$CLONE_DIR/.git" ] && [ ! -L "$CLONE_DIR/.git" ] || die "$CLONE_DIR/.git must be a real directory"
    verify_origin "$CLONE_DIR"
    [ -f "$CLONE_DIR/install.sh" ] && [ ! -L "$CLONE_DIR/install.sh" ] || die "$CLONE_DIR/install.sh has an unexpected type"
    [ -z "$(git_safe -C "$CLONE_DIR" status --porcelain=v1 --untracked-files=all)" ] ||
      die "$CLONE_DIR is dirty or contains untracked files; refusing to execute or replace its installer"
    current="$(git_safe -C "$CLONE_DIR" rev-parse 'HEAD^{commit}')"
    verify_payload "$CLONE_DIR" "$current"
  elif [ "$ACTION" = uninstall ]; then
    die "$CLONE_DIR does not exist; there is no verified installer to run"
  fi

  preflight_all "$expected_skill"

  if [ "$ACTION" = uninstall ]; then
    verify_clean_checkout "$CLONE_DIR" "$REF"
    verify_running_installer "$CLONE_DIR" "$REF" || die 'running installer bytes do not match install.sh at SEPIA_REF'
    exec env SEPIA_REF="$REF" SEPIA_REPO="$REPO_URL" SEPIA_HOME="$CLONE_DIR" SEPIA_ACTION=uninstall bash "$CLONE_DIR/install.sh"
  fi

  temp="$(prepare_checkout "$CLONE_DIR")"
  if [ -e "$CLONE_DIR" ]; then
    backup="$CLONE_DIR.sepia-backup.$$"
    failed="$CLONE_DIR.sepia-failed.$$"
    [ ! -e "$backup" ] && [ ! -L "$backup" ] && [ ! -e "$failed" ] && [ ! -L "$failed" ] || {
      rm -rf -- "$temp"
      die 'temporary checkout path collision'
    }
    mv "$CLONE_DIR" "$backup"
    mv "$temp" "$CLONE_DIR"
    if env SEPIA_REF="$REF" SEPIA_REPO="$REPO_URL" SEPIA_HOME="$CLONE_DIR" bash "$CLONE_DIR/install.sh"; then
      rm -rf -- "$backup"
      exit 0
    fi
    mv "$CLONE_DIR" "$failed"
    mv "$backup" "$CLONE_DIR"
    rm -rf -- "$failed"
    die 'installation failed; the previous checkout was restored'
  fi

  failed="$CLONE_DIR.sepia-failed.$$"
  [ ! -e "$failed" ] && [ ! -L "$failed" ] || {
    rm -rf -- "$temp"
    die 'temporary checkout path collision'
  }
  mv "$temp" "$CLONE_DIR"
  if env SEPIA_REF="$REF" SEPIA_REPO="$REPO_URL" SEPIA_HOME="$CLONE_DIR" bash "$CLONE_DIR/install.sh"; then
    exit 0
  fi
  mv "$CLONE_DIR" "$failed"
  rm -rf -- "$failed"
  die 'installation failed; the new checkout and destinations were removed'
}

TX_CREATED_DIRS=()
TX_CREATED_LINKS=()
TX_AG_TEMP=""
TX_WF_TEMP=""
TX_WF_STATE_TEMP=""
TX_AG_BACKUP=""
TX_WF_BACKUP=""
TX_WF_STATE_BACKUP=""
TX_AG_BACKED_UP=0
TX_WF_BACKED_UP=0
TX_WF_STATE_BACKED_UP=0
TX_AG_PUBLISHED=0
TX_WF_PUBLISHED=0
TX_WF_STATE_PUBLISHED=0

ensure_parent() {
  local parent current i
  local -a missing=()
  parent="$(dirname "$1")"
  current="$parent"
  while [ "$current" != "$HOME" ] && [ ! -e "$current" ] && [ ! -L "$current" ]; do
    missing[${#missing[@]}]="$current"
    current="$(dirname "$current")"
  done
  for ((i=${#missing[@]} - 1; i >= 0; i--)); do
    TX_CREATED_DIRS[${#TX_CREATED_DIRS[@]}]="${missing[$i]}"
  done
  mkdir -p "$parent"
}

rollback_install() {
  local failed=0 i path
  set +e
  if [ "$TX_WF_STATE_PUBLISHED" = 1 ]; then rm -rf -- "$WF_STATE" || failed=1; fi
  if [ "$TX_WF_STATE_BACKED_UP" = 1 ]; then mv "$TX_WF_STATE_BACKUP" "$WF_STATE" || failed=1; fi
  if [ "$TX_WF_PUBLISHED" = 1 ]; then rm -rf -- "$WF" || failed=1; fi
  if [ "$TX_WF_BACKED_UP" = 1 ]; then mv "$TX_WF_BACKUP" "$WF" || failed=1; fi
  if [ "$TX_AG_PUBLISHED" = 1 ]; then rm -rf -- "$AG" || failed=1; fi
  if [ "$TX_AG_BACKED_UP" = 1 ]; then mv "$TX_AG_BACKUP" "$AG" || failed=1; fi
  for ((i=${#TX_CREATED_LINKS[@]} - 1; i >= 0; i--)); do
    rm -f -- "${TX_CREATED_LINKS[$i]}" || failed=1
  done
  for path in "$TX_AG_TEMP" "$TX_WF_TEMP" "$TX_WF_STATE_TEMP"; do
    if [ -n "$path" ]; then rm -rf -- "$path" || failed=1; fi
  done
  for ((i=${#TX_CREATED_DIRS[@]} - 1; i >= 0; i--)); do
    if [ -d "${TX_CREATED_DIRS[$i]}" ] && [ ! -L "${TX_CREATED_DIRS[$i]}" ]; then
      rmdir "${TX_CREATED_DIRS[$i]}" || failed=1
    fi
  done
  if [ "$failed" != 0 ]; then
    printf 'sepia installer: destination rollback was incomplete; inspect paths reported above\n' >&2
  else
    printf 'sepia installer: restored all destinations to their pre-install state\n' >&2
  fi
}

rollback_on_exit() {
  local status=$?
  trap - EXIT
  rollback_install
  exit "$status"
}

check_transaction_paths() {
  local path
  TX_AG_BACKUP="$AG.sepia-backup.$$"
  TX_WF_BACKUP="$WF.sepia-backup.$$"
  TX_WF_STATE_BACKUP="$WF_STATE.sepia-backup.$$"
  for path in "$TX_AG_BACKUP" "$TX_WF_BACKUP" "$TX_WF_STATE_BACKUP"; do
    [ ! -e "$path" ] && [ ! -L "$path" ] || die "temporary path exists: $path"
  done
}

stage_install() {
  local hash
  ensure_parent "$CLAUDE"
  ensure_parent "$CODEX"
  ensure_parent "$GROK"
  ensure_parent "$AG"
  ensure_parent "$WF"

  TX_AG_TEMP="$(mktemp -d "${AG}.tmp.XXXXXX")"
  cp -R "$SKILL"/. "$TX_AG_TEMP"/
  snapshot_dir "$TX_AG_TEMP" "$TX_AG_TEMP/$MANIFEST_NAME" || die 'canonical skill contains an unsupported file type or symlink'
  printf 'owner=%s\nrevision=%s\n' "$OWNER" "$REF" >"$TX_AG_TEMP/$STATE_NAME"

  TX_WF_TEMP="$(mktemp "${WF}.tmp.XXXXXX")"
  TX_WF_STATE_TEMP="$(mktemp "${WF_STATE}.tmp.XXXXXX")"
  cp "$ROOT/.agents/workflows/sepia.md" "$TX_WF_TEMP"
  hash="$(sha256_file "$TX_WF_TEMP")"
  printf 'owner=%s\nrevision=%s\nsha256=%s\n' "$OWNER" "$REF" "$hash" >"$TX_WF_STATE_TEMP"
}

publish_link() {
  local target="$1" destination="$2"
  if [ ! -L "$destination" ]; then
    ln -s "$target" "$destination"
    TX_CREATED_LINKS[${#TX_CREATED_LINKS[@]}]="$destination"
  fi
  printf 'linked  %s\n' "$destination"
}

publish_skill_copy() {
  if [ -e "$AG" ]; then
    mv "$AG" "$TX_AG_BACKUP"
    TX_AG_BACKED_UP=1
  fi
  mv "$TX_AG_TEMP" "$AG"
  TX_AG_PUBLISHED=1
  printf 'copied  %s\n' "$AG"
}

publish_workflow() {
  if [ -e "$WF" ]; then
    mv "$WF" "$TX_WF_BACKUP"
    TX_WF_BACKED_UP=1
    mv "$WF_STATE" "$TX_WF_STATE_BACKUP"
    TX_WF_STATE_BACKED_UP=1
  fi
  mv "$TX_WF_TEMP" "$WF"
  TX_WF_PUBLISHED=1
  mv "$TX_WF_STATE_TEMP" "$WF_STATE"
  TX_WF_STATE_PUBLISHED=1
  printf 'copied  %s\n' "$WF"
}

finish_install() {
  local failed=0 path
  trap - EXIT
  for path in "$TX_AG_BACKUP" "$TX_WF_BACKUP" "$TX_WF_STATE_BACKUP"; do
    if [ -e "$path" ] || [ -L "$path" ]; then rm -rf -- "$path" || failed=1; fi
  done
  if [ "$failed" != 0 ]; then
    printf 'sepia installer: warning: installation succeeded but a private backup could not be removed\n' >&2
  fi
}

install_all() {
  check_transaction_paths
  trap rollback_on_exit EXIT
  stage_install
  publish_link "$SKILL" "$CLAUDE"
  publish_link "$SKILL" "$CODEX"
  publish_link "$SKILL" "$GROK"
  publish_skill_copy
  publish_workflow
  printf '\nInstalled revision %s at user scope.\n' "$REF"
  printf 'Keep %s: the Claude, Codex, and Grok links use its canonical skill.\n' "$ROOT"
  finish_install
}

uninstall_all() {
  local path
  preflight_all "$SKILL"
  verify_clean_checkout "$ROOT" "$REF"
  for path in "$CLAUDE" "$CODEX" "$GROK"; do
    if [ -L "$path" ]; then
      rm "$path"
      printf 'removed %s\n' "$path"
    fi
  done
  if [ -d "$AG" ]; then
    rm -rf -- "$AG"
    printf 'removed %s\n' "$AG"
  fi
  if [ -f "$WF" ]; then
    rm "$WF" "$WF_STATE"
    printf 'removed %s\n' "$WF"
  fi
  printf 'Kept checkout: %s\n' "$ROOT"
}

validate_inputs
CLAUDE="$HOME/.claude/skills/sepia"
CODEX="$HOME/.agents/skills/sepia"
GROK="$HOME/.grok/skills/sepia"
AG="$HOME/.gemini/config/skills/sepia"
WF="$HOME/.gemini/antigravity/global_workflows/sepia.md"
WF_STATE="$WF$STATE_NAME"
validate_clone_location

SCRIPT_DIR=""
SCRIPT_PATH=""
if [ -n "$SCRIPT_SRC" ] && [ -f "$SCRIPT_SRC" ] && [ ! -L "$SCRIPT_SRC" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_SRC")" && pwd -P)"
  SCRIPT_PATH="$SCRIPT_DIR/$(basename "$SCRIPT_SRC")"
fi
if [ -z "$SCRIPT_DIR" ] || [ "$SCRIPT_PATH" != "$SCRIPT_DIR/install.sh" ] || [ ! -f "$SCRIPT_DIR/skills/sepia/SKILL.md" ]; then
  bootstrap
fi

ROOT="$(git_safe -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null)" || die 'installer is not in a Git checkout'
[ "$(cd "$ROOT" && pwd -P)" = "$SCRIPT_DIR" ] || die 'install.sh must be run from the checkout root'
verify_clean_checkout "$ROOT" "$REF"
SKILL="$ROOT/skills/sepia"

if [ "$ACTION" = uninstall ]; then
  uninstall_all
  exit 0
fi

preflight_all "$SKILL"
verify_clean_checkout "$ROOT" "$REF"
install_all
