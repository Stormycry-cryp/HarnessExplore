#!/usr/bin/env bash
# Compatible with the macOS system Bash (3.2).
set -euo pipefail

CACHE_ROOT="${HARNESS_EXPLORE_CACHE:-${CODEX_HOME:-$HOME/.codex}/harness-explore}"
CLI_ROOT="$CACHE_ROOT/codex-cli"
CLI_BIN="$CLI_ROOT/node_modules/.bin/codex"
SOURCE_DIR="$CACHE_ROOT/openai-codex"
MANUAL_PATH="$CACHE_ROOT/codex-manual.md"
EVIDENCE_PATH="$CACHE_ROOT/bootstrap-evidence.txt"
SOURCE_REF="${HARNESS_EXPLORE_SOURCE_REF:-main}"
OFFICIAL_ORIGIN="https://github.com/openai/codex.git"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_MANIFEST="$SCRIPT_DIR/../references/codex-source-files.txt"
offline=false
skip_cli=false
for arg in "$@"; do
  case "$arg" in
    --offline) offline=true ;;
    --skip-cli) skip_cli=true ;;
    --help|-h)
      echo "Usage: bootstrap_codex.sh [--offline] [--skip-cli]"
      echo "HARNESS_EXPLORE_CACHE selects the isolated cache."
      echo "HARNESS_EXPLORE_SOURCE_REF selects an official branch, tag, or commit (default: main)."
      exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 1 ;;
  esac
done
# Partial-clone verification must not silently fetch missing objects offline.
if [[ "$offline" == true ]]; then export GIT_NO_LAZY_FETCH=1; fi
fail() { echo "$*" >&2; exit 1; }
previous() {
  if [[ -f "$EVIDENCE_PATH" ]]; then
    awk -v key="$1" 'index($0, key "=") == 1 {print substr($0, length(key) + 2); exit}' "$EVIDENCE_PATH"
  fi
}
now() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
command -v git >/dev/null 2>&1 || fail "git is required to verify the official source cache."
[[ -f "$SOURCE_MANIFEST" ]] || fail "Missing source manifest: $SOURCE_MANIFEST"
case "$SOURCE_REF" in ''|-*) fail "Invalid source ref: $SOURCE_REF" ;; esac
git check-ref-format --allow-onelevel "$SOURCE_REF" >/dev/null 2>&1 || fail "Invalid source ref: $SOURCE_REF"
validate_existing_source() {
[[ ! -L "$SOURCE_DIR" ]] || fail "Refusing source symlink: $SOURCE_DIR"
if [[ -e "$SOURCE_DIR" ]]; then
  [[ -d "$SOURCE_DIR/.git" && ! -L "$SOURCE_DIR/.git" ]] || fail "Refusing source cache without an independent Git checkout: $SOURCE_DIR"
  origin="$(git -C "$SOURCE_DIR" remote get-url origin)" || fail "Cannot verify source cache origin: $SOURCE_DIR"
  case "$origin" in
    https://github.com/openai/codex.git|https://github.com/openai/codex|git@github.com:openai/codex.git|ssh://git@github.com/openai/codex.git) ;;
    *) fail "Refusing non-official source cache origin: $origin" ;;
  esac
  source_status="$(git -C "$SOURCE_DIR" status --porcelain --untracked-files=all --ignored)" || fail "Cannot verify source cache status: $SOURCE_DIR"
  [[ -z "$source_status" ]] || fail "Refusing dirty source checkout; preserve your edits before retrying: $SOURCE_DIR"
fi
}
validate_existing_source
mkdir -p "$CACHE_ROOT"
checked_at="$(now)"
temp_dir="$(mktemp -d "$CACHE_ROOT/bootstrap.XXXXXX")"
trap 'rm -rf "$temp_dir"' EXIT
verify_manifest() {
  local checkout="$1" commit="$2" missing=false source_path
  while IFS= read -r source_path || [[ -n "$source_path" ]]; do
    [[ -z "$source_path" || "$source_path" == \#* ]] && continue
    case "$source_path" in
      /*|../*|*/../*|*/..|..) fail "Unsafe source manifest path: $source_path" ;;
    esac
    if [[ ! -f "$checkout/$source_path" || -L "$checkout/$source_path" ]]; then
      echo "Selected Codex source is missing at $commit: $source_path" >&2
      missing=true
    fi
  done < "$SOURCE_MANIFEST"
  if [[ "$missing" == true ]]; then
    echo "Find replacement paths in the selected tree:" >&2
    echo "  git -C '$checkout' ls-tree -r --name-only '$commit' (temporary checkout is removed on exit)" >&2
    echo "  gh api 'repos/openai/codex/git/trees/$commit?recursive=1' --jq '.tree[].path'" >&2
    echo "Update references/codex-source-files.txt after checking the matching official file." >&2
    return 1
  fi
}
source_acquired_at=unknown
if [[ "$offline" == true ]]; then
  [[ -d "$SOURCE_DIR/.git" ]] || fail "Offline mode requires an existing official source cache: $SOURCE_DIR"
  source_commit="$(git -C "$SOURCE_DIR" rev-parse HEAD)"
  if [[ -n "${HARNESS_EXPLORE_SOURCE_REF+x}" ]]; then
    local_ref_commit="$(git -C "$SOURCE_DIR" rev-parse --verify "$SOURCE_REF^{commit}" 2>/dev/null || true)"
    if [[ "$local_ref_commit" != "$source_commit" && !( "$(previous source_ref)" == "$SOURCE_REF" && "$(previous source_commit)" == "$source_commit" ) ]]; then
      fail "Offline snapshot $source_commit does not verify requested ref $SOURCE_REF; refresh online first."
    fi
  else
    SOURCE_REF="$(previous source_ref)"
    SOURCE_REF="${SOURCE_REF:-unknown}"
  fi
  verify_manifest "$SOURCE_DIR" "$source_commit"
  if [[ "$(previous source_commit)" == "$source_commit" ]]; then
    source_acquired_at="$(previous source_acquired_at_utc)"
    source_acquired_at="${source_acquired_at:-unknown}"
  fi
  source_state=cached_verified
else
  echo "Downloading selected official Codex source at $SOURCE_REF ..."
  candidate="$temp_dir/openai-codex"
  git -c http.version=HTTP/1.1 clone --depth=1 --filter=blob:none --no-checkout "$OFFICIAL_ORIGIN" "$candidate"
  git -c http.version=HTTP/1.1 -C "$candidate" fetch --depth=1 origin "$SOURCE_REF"
  git -C "$candidate" sparse-checkout init --no-cone
  git -C "$candidate" sparse-checkout set --stdin < "$SOURCE_MANIFEST"
  git -C "$candidate" checkout --detach FETCH_HEAD
  source_commit="$(git -C "$candidate" rev-parse HEAD)"
  verify_manifest "$candidate" "$source_commit"
  source_acquired_at="$(now)"
  source_state=fetched_verified
fi

working_codex=unavailable
codex_version=unavailable
if [[ "$skip_cli" == true ]]; then
  cli_status=skipped
elif command -v codex >/dev/null 2>&1 && codex --version >/dev/null 2>&1; then
  working_codex="$(command -v codex)"
  cli_status=existing
elif [[ -x "$CLI_BIN" ]] && "$CLI_BIN" --version >/dev/null 2>&1; then
  working_codex="$CLI_BIN"
  cli_status=isolated_cached
else
  [[ "$offline" == false ]] || fail "Offline mode found no working Codex CLI; use --skip-cli to study cached source."
  command -v npm >/dev/null 2>&1 || fail "npm is required to download Codex CLI into $CLI_ROOT; use --skip-cli for source only."
  echo "Downloading the latest official Codex CLI into $CLI_ROOT ..."
  npm install --prefix "$CLI_ROOT" --no-audit --no-fund @openai/codex@latest
  working_codex="$CLI_BIN"
  cli_status=isolated_installed
fi
if [[ "$skip_cli" == false ]]; then
  codex_version="$("$working_codex" --version)"
fi

manual_status=unavailable
manual_attempted_at=not_attempted
manual_acquired_at=unknown
manual_hash=unavailable
if [[ -f "$MANUAL_PATH" && ! -L "$MANUAL_PATH" ]]; then
  manual_status=cached_stale
  manual_hash="$(git hash-object --no-filters "$MANUAL_PATH")"
  if [[ "$(previous manual_hash)" == "$manual_hash" ]]; then
    manual_acquired_at="$(previous manual_acquired_at_utc)"
    manual_acquired_at="${manual_acquired_at:-unknown}"
  fi
fi
if [[ "$offline" == false ]]; then
  manual_attempted_at="$(now)"
  if command -v curl >/dev/null 2>&1 && curl --http1.1 --max-time 20 -fsSL \
    https://developers.openai.com/codex/codex-manual.md -o "$temp_dir/manual.md" && [[ -s "$temp_dir/manual.md" ]]; then
    manual_status=downloaded
    manual_acquired_at="$(now)"
    manual_hash="$(git hash-object --no-filters "$temp_dir/manual.md")"
  else
    echo "Codex web manual download failed; manual_status=$manual_status. Repository docs are available." >&2
  fi
fi
if [[ "$offline" == false ]]; then
  # Recheck in case the user edited the cache while the download was running.
  validate_existing_source
  # The old clean snapshot survives every failure before this point.
  if [[ -d "$SOURCE_DIR" ]]; then mv "$SOURCE_DIR" "$temp_dir/previous-source"; fi
  if ! mv "$candidate" "$SOURCE_DIR"; then
    [[ ! -d "$temp_dir/previous-source" ]] || mv "$temp_dir/previous-source" "$SOURCE_DIR"
    fail "Unable to publish source snapshot."
  fi
fi
if [[ "$manual_status" == downloaded ]]; then mv "$temp_dir/manual.md" "$MANUAL_PATH"; fi
{
  echo "format_version=1"
  echo "mode=$([[ "$offline" == true ]] && echo offline || echo online)"
  echo "checked_at_utc=$checked_at"
  echo "source_state=$source_state"
  echo "source_acquired_at_utc=$source_acquired_at"
  echo "source_ref=$SOURCE_REF"
  echo "source_commit=$source_commit"
  echo "source_dir=$SOURCE_DIR"
  echo "cli_status=$cli_status"
  echo "codex_bin=$working_codex"
  echo "codex_version=$codex_version"
  echo "official_docs_dir=$SOURCE_DIR/docs"
  echo "manual_status=$manual_status"
  echo "manual_path=$([[ "$manual_status" != unavailable ]] && echo "$MANUAL_PATH" || echo unavailable)"
  echo "manual_attempted_at_utc=$manual_attempted_at"
  echo "manual_acquired_at_utc=$manual_acquired_at"
  echo "manual_hash=$manual_hash"
  echo "progress_path=$CACHE_ROOT/progress.md"
} > "$temp_dir/evidence.txt"
mv "$temp_dir/evidence.txt" "$EVIDENCE_PATH"
cat "$EVIDENCE_PATH"
echo "evidence_path=$EVIDENCE_PATH"
