#!/usr/bin/env bash
set -euo pipefail

CACHE_ROOT="${HARNESS_EXPLORE_CACHE:-${CODEX_HOME:-$HOME/.codex}/harness-explore}"
CLI_ROOT="$CACHE_ROOT/codex-cli"
CLI_BIN="$CLI_ROOT/node_modules/.bin/codex"
SOURCE_DIR="$CACHE_ROOT/openai-codex"
MANUAL_PATH="$CACHE_ROOT/codex-manual.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_MANIFEST="$SCRIPT_DIR/../references/codex-source-files.txt"

mkdir -p "$CACHE_ROOT"

working_codex=""
if command -v codex >/dev/null 2>&1 && codex --version >/dev/null 2>&1; then
  working_codex="$(command -v codex)"
elif [[ -x "$CLI_BIN" ]] && "$CLI_BIN" --version >/dev/null 2>&1; then
  working_codex="$CLI_BIN"
else
  if ! command -v npm >/dev/null 2>&1; then
    echo "npm is required to download Codex CLI into $CLI_ROOT" >&2
    exit 1
  fi
  echo "Downloading the latest official Codex CLI into $CLI_ROOT ..."
  npm install --prefix "$CLI_ROOT" --no-audit --no-fund @openai/codex@latest
  working_codex="$CLI_BIN"
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required to download the official Codex source snapshot." >&2
  exit 1
fi
[[ -f "$SOURCE_MANIFEST" ]] || { echo "Missing source manifest: $SOURCE_MANIFEST" >&2; exit 1; }

if ! command -v git >/dev/null 2>&1; then
  echo "git is required to download the selected Codex source." >&2
  exit 1
fi

if [[ ! -d "$SOURCE_DIR/.git" ]]; then
  echo "Downloading selected official Codex source ..."
  temp_dir="$(mktemp -d "$CACHE_ROOT/source.XXXXXX")"
  trap 'rm -rf "$temp_dir"' EXIT
  extracted_dir="$temp_dir/openai-codex"
  git -c http.version=HTTP/1.1 clone --depth=1 --filter=blob:none --no-checkout \
    https://github.com/openai/codex.git "$extracted_dir"
  git -C "$extracted_dir" sparse-checkout init --no-cone
  git -C "$extracted_dir" sparse-checkout set --stdin < "$SOURCE_MANIFEST"
  git -C "$extracted_dir" checkout --detach
  rm -rf "$SOURCE_DIR"
  mv "$extracted_dir" "$SOURCE_DIR"
  rm -rf "$temp_dir"
  trap - EXIT
else
  git -c http.version=HTTP/1.1 -C "$SOURCE_DIR" fetch --depth=1 origin main
  git -C "$SOURCE_DIR" checkout --detach FETCH_HEAD
  git -C "$SOURCE_DIR" sparse-checkout set --stdin < "$SOURCE_MANIFEST"
fi

source_commit="$(git -C "$SOURCE_DIR" rev-parse HEAD)"
while IFS= read -r source_path; do
  [[ -z "$source_path" || "$source_path" == \#* ]] && continue
  if [[ ! -f "$SOURCE_DIR/$source_path" ]]; then
    echo "Selected Codex source is missing at $source_commit: $source_path" >&2
    exit 1
  fi
done < "$SOURCE_MANIFEST"

manual_temp="$(mktemp "$CACHE_ROOT/manual.XXXXXX")"
if curl --http1.1 --max-time 20 -fsSL \
  https://developers.openai.com/codex/codex-manual.md \
  -o "$manual_temp"; then
  mv "$manual_temp" "$MANUAL_PATH"
else
  rm "$manual_temp"
  echo "Codex web manual is unavailable; using versioned repository docs." >&2
fi

echo "codex_bin=$working_codex"
echo "codex_version=$($working_codex --version)"
echo "source_dir=$SOURCE_DIR"
echo "source_commit=$source_commit"
echo "official_docs_dir=$SOURCE_DIR/docs"
if [[ -f "$MANUAL_PATH" ]]; then
  echo "manual_path=$MANUAL_PATH"
else
  echo "manual_path=unavailable"
fi
echo "progress_path=$CACHE_ROOT/progress.md"
