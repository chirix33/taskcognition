"""Fail-closed workflow controls, not a security boundary."""
from pathlib import Path
from .contracts import IntegrityError, Split, file_hash


def require_p00(state: dict):
    if state.get("active_phase") != "P00" or state.get("status") not in ("IN_PROGRESS", "READY_FOR_REVIEW"):
        raise IntegrityError("P00 fixture execution is not active")


def guard_final_collection(split: str, manifest: Path | None, accepted_hash: str | None):
    Split(split)
    if split == Split.DEVELOPMENT:
        raise IntegrityError("real development collection is not implemented in P00")
    if manifest is None or not manifest.is_file() or accepted_hash is None:
        raise IntegrityError("final collection requires an accepted immutable base freeze")
    if file_hash(manifest) != accepted_hash:
        raise IntegrityError("base freeze hash mismatch")
    # A hash alone is not evidence of acceptance/completeness. No escape via fake seal.
    raise IntegrityError("P00 forbids real collection; full freeze validation belongs to P04")


def read_training_rows(rows, expected_kind: str):
    result = list(rows)
    if any(row.split != Split.TRAIN for row in result):
        raise IntegrityError("fitting readers accept TRAIN only")
    if any(row.evidence_kind != expected_kind for row in result):
        raise IntegrityError("training evidence kind mismatch")
    return result
