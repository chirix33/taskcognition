"""Synthetic score records, not real tasks, scorers, or model requests."""
from pathlib import Path
import platform
from .artifacts import child_path, fixture_output, read_json, verify_bundle, write_new
from .contracts import (DrawRecord, InputRecord, IntegrityError, FAMILIES, SOURCE_SHA256,
                        digest, file_hash, record_dict, stream_id)
from .targets import aggregate

STUDY_ID = "p00-analytical-fixture-v1"
ROOT_SEED = 0
PACKAGES = {m: {"evidence_kind": "fixture", "mode": m, "synthetic": True,
                "enable_thinking": m == "R", "backend": "none"} for m in ("D", "R")}
PACKAGE_HASHES = {m: digest(p) for m, p in PACKAGES.items()}


def producer():
    return {"python": platform.python_version(), "package_version": "0.0.1",
            "source_files": {p.name: file_hash(p) for p in sorted(Path(__file__).parent.glob("*.py"))},
            "rng_scheme": "SHA256 canonical JSON [answer-sampling-v1, study, root_seed, split, input, package_hash, draw_index]",
            "root_seed": ROOT_SEED, "sampling_performed": False}


def build_rows(family=FAMILIES[0], ds=(1, 1, 1, 0), rs=(1, 1, 0, 0), split="DEVELOPMENT"):
    input_id = digest([STUDY_ID, family, split])
    row = InputRecord("fixture", input_id, split, family, digest(["synthetic-latent", family]),
                      "Synthetic analytical scores only; no task generation.", None, 0,
                      digest({"synthetic": True}), "fixture-scores-v1; not a native scorer", "fixture://no-gold")
    draws, raws = [], {}
    for mode, scores in (("D", ds), ("R", rs)):
        for i, score in enumerate(scores):
            draw_id = digest([input_id, PACKAGE_HASHES[mode], i])
            raw_path = "raw/" + draw_id + ".json"
            raw = {"evidence_kind": "fixture", "synthetic": True, "native_score": score,
                   "token_ids": [], "text": "synthetic score, not model output", "final_payload": None,
                   "finish_reason": "fixture", "attempts": [], "actual_model_calls": 0}
            # write_new appends a newline; file hashes refer to exact persisted bytes.
            from hashlib import sha256
            from .contracts import canonical
            raw_hash = sha256(canonical(raw) + b"\n").hexdigest()
            draws.append(DrawRecord("fixture", draw_id, input_id, split, mode, PACKAGE_HASHES[mode], i,
                                    stream_id(STUDY_ID, ROOT_SEED, split, input_id, PACKAGE_HASHES[mode], i),
                                    raw_path, raw_hash, score, score == 1, 1 if mode == "D" else 2,
                                    "synthetic_units", "perfect" if score == 1 else "partial" if score > 0 else "wrong"))
            raws[raw_path] = raw
    return row, draws, raws


def summarize(rows):
    from statistics import fmean
    if len(rows) != 6 or {r.family for r in rows} != set(FAMILIES):
        raise IntegrityError("fixture requires one complete cluster per family")
    return {"evidence_kind": "fixture", "study_id": STUDY_ID, "source_sha256": SOURCE_SHA256,
            "input_clusters": 6, "draws_per_package_per_input": 4, "synthetic_draw_records": 48,
            "cross_pairs_per_input": 16, "inferential_unit": "input_cluster", "inference_performed": False,
            "actual_model_calls": 0, "actual_model_tokens": 0, "gate_training_runs": 0,
            "family_weight": "1/6", "cost_unit": "synthetic_units; not measured research expense",
            "balanced_mean_benefit": fmean(r.benefit for r in rows),
            "balanced_mean_joint_spoilage": fmean(r.joint_spoilage for r in rows),
            "balanced_mean_direct_redraw": fmean(r.direct_redraw for r in rows),
            "balanced_mean_decline_010": fmean(r.decline_010 for r in rows),
            "balanced_mean_decline_025": fmean(r.decline_025 for r in rows),
            "scope": "analytical fixture; no native renderer/scorer or manuscript empirical result"}


def verify_fixture(output: Path):
    manifest = verify_bundle(output)
    if manifest.get("study_id") != STUDY_ID or manifest.get("source_sha256") != SOURCE_SHA256:
        raise IntegrityError("fixture provenance mismatch")
    if read_json(output / "packages.json") != {"evidence_kind": "fixture", "packages": PACKAGES}:
        raise IntegrityError("fixture package mismatch")
    inputs = [InputRecord(**r) for r in read_json(output / "inputs.json")]
    draws = [DrawRecord(**r) for r in read_json(output / "draws.json")]
    if len({r.input_id for r in inputs}) != len(inputs) or len({r.draw_id for r in draws}) != len(draws):
        raise IntegrityError("duplicate input/draw ID")
    if len(draws) != 48 or {d.input_id for d in draws} != {r.input_id for r in inputs}:
        raise IntegrityError("draw plan incompleteness")
    for d in draws:
        raw = child_path(output, d.raw_path)
        if manifest["files"].get(d.raw_path) != d.raw_sha256 or file_hash(raw) != d.raw_sha256:
            raise IntegrityError("raw artifact linkage mismatch")
        if read_json(raw)["native_score"] != d.native_score:
            raise IntegrityError("raw score mismatch")
        if d.stream_id != stream_id(STUDY_ID, ROOT_SEED, d.split, d.input_id, d.package_hash, d.draw_index):
            raise IntegrityError("sampling stream mismatch")
    rows = [aggregate(r, [d for d in draws if d.input_id == r.input_id], 4, PACKAGE_HASHES) for r in inputs]
    if read_json(output / "aggregates.json") != [record_dict(r) for r in rows]:
        raise IntegrityError("saved aggregates do not recompute")
    if read_json(output / "report.json") != summarize(rows):
        raise IntegrityError("saved report does not recompute")
    return {"evidence_kind": "fixture", "status": "VERIFIED", "files": len(manifest["files"]),
            "manifest_sha256": file_hash(output / "manifest.json")}


def run_fixture(root: Path, output: Path, resume=False, dry_run=False):
    output = fixture_output(root, output)
    if dry_run:
        return {"evidence_kind": "fixture", "status": "PLAN", "input_clusters": 6,
                "synthetic_draw_records": 48, "actual_model_calls": 0, "output": output.relative_to(root.resolve()).as_posix()}
    if output.exists():
        if not resume:
            raise IntegrityError("run exists; no overwrite (use --resume to verify only)")
        return verify_fixture(output)
    output.mkdir(parents=True)
    # Persist intent first. An interrupted partial bundle is retained and fails resume.
    write_new(output / "intent.json", {"evidence_kind": "fixture", "study_id": STUDY_ID, "actual_model_calls": 0})
    inputs, draws, aggregates = [], [], []
    for family in FAMILIES:
        row, batch, raws = build_rows(family)
        inputs.append(record_dict(row))
        draws.extend(record_dict(d) for d in batch)
        aggregates.append(aggregate(row, batch, 4, PACKAGE_HASHES))
        for relative, raw in raws.items():
            write_new(output / relative, raw)
    for name, obj in {"inputs.json": inputs, "draws.json": draws,
                      "aggregates.json": [record_dict(r) for r in aggregates],
                      "packages.json": {"evidence_kind": "fixture", "packages": PACKAGES},
                      "report.json": summarize(aggregates)}.items():
        write_new(output / name, obj)
    files = {p.relative_to(output).as_posix(): file_hash(p) for p in output.rglob("*") if p.is_file()}
    write_new(output / "manifest.json", {"evidence_kind": "fixture", "schema": "p00-fixture-v1",
              "study_id": STUDY_ID, "source_sha256": SOURCE_SHA256, "producer": producer(), "files": files})
    return verify_fixture(output)
