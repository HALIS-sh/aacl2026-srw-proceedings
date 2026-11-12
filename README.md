# AACL-IJCNLP 2026 — Student Research Workshop Proceedings

aclpub2 sources and build output for the SRW volume of AACL-IJCNLP 2026
(Hengqin, Zhuhai, China, November 6, 2026).

- Volume: Proceedings of the 15th International Joint Conference on Natural Language
  Processing and the 5th Conference of the Asia-Pacific Chapter of the Association for
  Computational Linguistics (Volume 4: Student Research Workshop)
- `volume_name`: srw, `anthology_venue_id`: AACL, ISBN 979-8-89176-442-2
- Papers: 41 accepted (37 direct + 4 ARR commitments), 38 archival in this volume.
  Two papers opted for non-archival status; one further paper is excluded because no
  camera-ready version was provided. All papers were submitted under the CC BY 4.0 license.

## Layout

- `srw/` — aclpub2 input: `conference_details.yml`, `papers.yml` + `papers/*.pdf`,
  `prefaces*`, `organizing_committee.yml`, `program_committee.yml`, `attachments/`
- `output_srw/` — build output: `proceedings.pdf`, `watermarked_pdfs/` (0.pdf = front matter),
  `attachments/`, `inputs/`
- `scripts/build.sh` — re-runs `aclpub2 bin/generate srw --proceedings` (requires the
  aclpub2 checkout under `tools/aclpub2`, not committed)
- `archival_list.txt` — whitelist of papers included in the volume

Built with [aclpub2](https://github.com/rycolab/aclpub2) on 2026-11-12.

SRW chairs: Shibo Hong, Yuhang Zhou, Wenhe Sun. Faculty advisor: Yixin Cao.
Contact: whsun25@m.fudan.edu.cn
