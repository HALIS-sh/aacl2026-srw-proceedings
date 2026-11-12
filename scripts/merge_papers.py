#!/usr/bin/env python3
"""Merge export/direct and export/arr (from export_openreview.sh) into srw/papers.yml + srw/papers/.

- ARR-committed papers are renumbered id+100 so they cannot collide with direct-submission numbers.
- paper_type: 'Thesis Proposal:' titles -> thesis_proposal (9 content pages); others keep the exported
  value (ARR venue has Long/Short) or 'long' when unknown; fix by hand if the CFP distinguishes short papers.
- archival: taken from the OpenReview camera-ready field "archival" ("archival" / "non-archival") that
  the patched or2papers.py exports; archival_list.txt (lines 'direct 12' / 'arr 3') overrides it if present.
"""
import pathlib, re, shutil, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRW = ROOT / "srw"
(SRW / "papers").mkdir(exist_ok=True); (SRW / "attachments").mkdir(exist_ok=True)

archival = None
lst = ROOT / "archival_list.txt"
if lst.exists():
    archival = set()
    for line in lst.read_text().splitlines():
        line = line.split("#")[0].strip()
        if line:
            src, num = line.split(); archival.add((src, int(num)))
else:
    print("archival_list.txt not found -> using the 'archival' field exported from OpenReview (camera-ready form)")

merged = []
for src, offset in (("direct", 0), ("arr", 100)):
    d = ROOT / "export" / src
    if not (d / "papers.yml").exists():
        print(f"skip {src}: no export"); continue
    papers = yaml.safe_load((d / "papers.yml").read_text()) or []
    for p in papers:
        orig = int(p["id"]); new = orig + offset
        pdf_src = d / "papers" / f"{orig}.pdf"
        if pdf_src.exists():
            shutil.copy2(pdf_src, SRW / "papers" / f"{new}.pdf")
        else:
            print(f"WARNING: missing PDF for {src} #{orig}")
        for att in p.get("attachments", []) or []:
            a = d / "attachments" / att["file"]
            if a.exists():
                newname = re.sub(rf"^{orig}(?=[._])", str(new), att["file"])
                shutil.copy2(a, SRW / "attachments" / newname); att["file"] = newname
        p["id"] = new; p["file"] = f"{new}.pdf"
        attrs = p.setdefault("attributes", {})
        if re.match(r"\s*thesis\s*proposal\s*:", p["title"], re.I):
            attrs["submission_track"] = "thesis_proposal"; attrs["paper_type"] = "long"
        else:
            attrs["submission_track"] = "research_paper"
            if str(attrs.get("paper_type", "N/A")).lower() not in ("long", "short"):
                attrs["paper_type"] = "long"
        attrs["source_venue"] = src; attrs["openreview_number"] = orig
        if archival is not None:
            p["archival"] = (src, orig) in archival
        else:
            flag = str(attrs.get("archival", "")).strip().lower()
            if not flag:
                print(f"WARNING: {src} #{orig} has no archival field -> defaulting to archival: true")
                p["archival"] = True
            else:
                p["archival"] = not flag.startswith("non")
        for k in ("pdf_file", "decision"):
            p.pop(k, None)
        merged.append(p)

merged.sort(key=lambda p: p["id"])
(SRW / "papers.yml").write_text(yaml.safe_dump(merged, allow_unicode=True, sort_keys=False, width=100))
n_arch = sum(p["archival"] for p in merged)
print(f"wrote {SRW/'papers.yml'}: {len(merged)} papers, {n_arch} archival, {len(merged)-n_arch} non-archival")
for p in merged:
    print(f"  {'A' if p['archival'] else '-'} {p['id']:>4}  [{p['attributes']['source_venue']}#{p['attributes']['openreview_number']}] {p['title'][:70]}")
