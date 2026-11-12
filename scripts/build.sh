#!/usr/bin/env bash
# Build proceedings with aclpub2.
# Usage: scripts/build.sh [input_dir]   (default: srw)  -> output copied to output_<input_dir>/
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IN="${1:-srw}"
export PATH="/opt/homebrew/opt/openjdk/bin:/Library/TeX/texbin:$PATH"
cd "$ROOT/tools/aclpub2"
rm -rf build output
export PYTHONPATH=.:${PYTHONPATH:-}
"$ROOT/.venv/bin/python" bin/generate "$ROOT/$IN" --proceedings < /dev/null
OUT="$ROOT/output_$IN"
rm -rf "$OUT"; cp -R output "$OUT"
echo; echo "Built -> $OUT"; ls "$OUT"
if [ -f "$OUT/watermarked_pdfs/0.pdf" ]; then echo "OK: watermarked_pdfs/0.pdf present (required by the Anthology)"; else echo "MISSING: watermarked_pdfs/0.pdf"; exit 1; fi
