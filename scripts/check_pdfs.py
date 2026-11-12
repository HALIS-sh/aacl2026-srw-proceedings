#!/usr/bin/env python3
"""Run ACL pubcheck on every paper in srw/papers.yml using each paper's own paper_type.
Writes reports/<id>.txt and reports/SUMMARY.md. Name-check (external API) is disabled for speed."""
import pathlib, re, subprocess, sys, yaml
R = pathlib.Path(__file__).resolve().parents[1]
PY = R / ".venv/bin/python"
papers = yaml.safe_load((R / "srw/papers.yml").read_text())
rep = R / "reports"; rep.mkdir(exist_ok=True)
rows = []
for p in papers:
    pdf = R / "srw/papers" / p["file"]
    ptype = str(p["attributes"].get("paper_type", "long")).lower()
    if ptype not in ("long", "short"): ptype = "long"
    out = subprocess.run([str(PY), "-m", "aclpubcheck.formatchecker", "--paper_type", ptype, "--disable_name_check", str(pdf)],
                         cwd=R / "tools/aclpubcheck", capture_output=True, text=True)
    txt = out.stdout + out.stderr
    (rep / f"{p['id']}.txt").write_text(txt)
    m = re.search(r"We detected (\d+) errors? and (\d+) warnings?", txt)
    if m:
        errs, warns = int(m.group(1)), int(m.group(2))
    elif "All Clear!" in txt:
        errs, warns = 0, 0
    else:
        errs = len(re.findall(r"^Error \(", txt, re.M)); warns = len(re.findall(r"^Warning \(", txt, re.M))
    kinds = sorted(set(re.findall(r"^(?:Error|Warning) \(([^)]+)\)", txt, re.M)))
    rows.append((p["id"], ptype, p["archival"], errs, warns, kinds, p["title"][:60]))
    print(f"{p['id']:>4} {ptype:5s} {'A' if p['archival'] else '-'} errors={errs:>2} warnings={warns:>2} {kinds}", flush=True)
lines = ["| id | type | archival | errors | warnings | kinds | title |", "|---|---|---|---|---|---|---|"]
for r in rows: lines.append(f"| {r[0]} | {r[1]} | {'yes' if r[2] else 'no'} | {r[3]} | {r[4]} | {', '.join(r[5])} | {r[6]} |")
(rep / "SUMMARY.md").write_text("\n".join(lines) + "\n")
bad = [r for r in rows if r[3] != 0 and r[2]]
print(f"\nArchival papers with errors: {len(bad)} / {sum(1 for r in rows if r[2])}  -> reports/SUMMARY.md")
