#!/usr/bin/env bash
# Export accepted papers (metadata + PDFs) from both SRW OpenReview venues with aclpub2's or2papers.py.
# Credentials are read from the environment so they never appear in a chat log or shell history:
#   export OPENREVIEW_USERNAME='you@example.org'
#   read -s OPENREVIEW_PASSWORD && export OPENREVIEW_PASSWORD
#   scripts/export_openreview.sh
# Output: export/direct/{papers.yml,papers/,attachments/}  and  export/arr/{...}
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# Credentials: environment variables, or (fallback) a two-line file ~/.config/openreview/credentials
# (line 1 = username, line 2 = password, mode 600). Delete the file when the proceedings are done.
CRED="$HOME/.config/openreview/credentials"
if [ -z "${OPENREVIEW_USERNAME:-}" ] && [ -r "$CRED" ]; then
  OPENREVIEW_USERNAME="$(sed -n 1p "$CRED")"; OPENREVIEW_PASSWORD="$(sed -n 2p "$CRED")"
fi
: "${OPENREVIEW_USERNAME:?set OPENREVIEW_USERNAME or create $CRED}"; : "${OPENREVIEW_PASSWORD:?set OPENREVIEW_PASSWORD or create $CRED}"
PY="$ROOT/.venv/bin/python"
OR="$ROOT/tools/aclpub2/openreview"

export_venue() {   # $1 = short name, $2 = OpenReview venue id
  local out="$ROOT/export/$1"
  rm -rf "$out"; mkdir -p "$out"; cd "$out"
  echo "=== exporting $2 -> $out"
  PYTHONPATH="$OR" "$PY" "$OR/or2papers.py" "$OPENREVIEW_USERNAME" "$OPENREVIEW_PASSWORD" "$2" --all --pdfs
  echo "    papers: $(ls papers/*.pdf 2>/dev/null | wc -l | tr -d ' ')  log: $out/papers.log"
}

export_venue direct "aclweb.org/AACL-IJCNLP/2026/SRW_Direct_Submission"
export_venue arr    "aclweb.org/AACL-IJCNLP/2026/Workshop/SRW_ARR_Commitment"
echo; echo "Next: $PY $ROOT/scripts/merge_papers.py"
