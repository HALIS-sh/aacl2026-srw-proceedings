#!/usr/bin/env bash
# Run ACL pubcheck on every PDF in srw/papers/. Usage: scripts/check_pdfs.sh [long|short]
# Writes one report per paper to reports/ and a summary to reports/SUMMARY.txt
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TYPE="${1:-long}"
mkdir -p "$ROOT/reports"
: > "$ROOT/reports/SUMMARY.txt"
for f in "$ROOT"/srw/papers/*.pdf; do
  [ -e "$f" ] || { echo "no PDFs in srw/papers/"; exit 1; }
  b="$(basename "$f" .pdf)"
  "$ROOT/.venv/bin/python" -m aclpubcheck.formatchecker --paper_type "$TYPE" "$f" > "$ROOT/reports/$b.txt" 2>&1
  if grep -qiE "error|warning" "$ROOT/reports/$b.txt"; then
    n=$(grep -ciE "error|warning" "$ROOT/reports/$b.txt")
    echo "$b.pdf  ->  $n issue line(s), see reports/$b.txt" | tee -a "$ROOT/reports/SUMMARY.txt"
  else
    echo "$b.pdf  ->  clean" | tee -a "$ROOT/reports/SUMMARY.txt"
  fi
done
