#!/usr/bin/env bash
set -euo pipefail

session="${1:-example}"
repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
manifest="$repo_root/sessions/$session/session.manifest.yml"
outdir="$repo_root/out"
mkdir -p "$outdir"
src="$repo_root/sessions/$session/source.md"
template="$repo_root/templates/word/template.docx"
out="$outdir/${session}-output.docx"
resource_path="$repo_root/sessions/$session/images:docs:docs/images"

echo "Rendering $src -> $out using template $template"

pandoc "$src" -o "$out" --reference-doc="$template" --resource-path="$resource_path"

if [ $? -eq 0 ]; then
  echo "Pandoc succeeded, updating manifest: $manifest"
  python3 "$repo_root/.github/scripts/update_manifest.py" "$manifest" "$out"
  echo "Render complete: $out"
else
  echo "Render failed" >&2
  exit 1
fi
