"""Fingerprint recovered task-repository sources without changing or importing them."""
from datetime import datetime, timezone
from pathlib import Path
from taskcognition.artifacts import write_new
from taskcognition.contracts import SOURCE_SHA256, file_hash

root = Path(__file__).resolve().parents[1]
archive = root / "docs/iclr2027"
originals = {p.relative_to(root).as_posix(): file_hash(p) for p in sorted(archive.rglob("*")) if p.is_file()}
active = [root/"AGENTS.md", root/"README.md", root/"docs/prompts/P00_bootstrap.md"]
active += sorted((root/"docs").glob("*.md"))
active += sorted((root/"docs/templates").glob("*.md"))
pdf = root/"reference/TaskCognition_Revised_Verified.pdf"
assert file_hash(pdf) == SOURCE_SHA256
assert file_hash(archive/"TaskCognition_ICLR_2027_Critique_Revised_Verified.pdf") == SOURCE_SHA256
write_new(root/"reports/source_inventory.json", {
    "evidence_kind": "development_observation", "artifact_role": "source_inventory_no_generation",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(), "source_sha256": SOURCE_SHA256,
    "reference_pdf_pages": 12, "all_pages_text_read": True, "visually_checked_equation_pages": [2, 5],
    "original_tex_present": True, "original_bib_present": True, "original_protocol_present": True,
    "original_manuscript_rebuilt": False, "originals_remain_ignored": True,
    "active_contracts": {p.relative_to(root).as_posix(): file_hash(p) for p in active},
    "preserved_original_files": originals,
    "conflicts": {"handoff_sources_absent": "superseded by local discovery", "prelabel_candidate_hashes": "C01 resolved by user",
                  "failed_resample_wording": "C02 resolved by user", "train_tune_evidence_kinds": "C03 resolved by user"},
})
print("Source hashes verified; source_inventory.json created; originals not modified.")
