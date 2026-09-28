from dataclasses import replace
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from taskcognition.artifacts import child_path, read_json, write_new
from taskcognition.cli import main
from taskcognition.contracts import (FeatureRecord, IntegrityError, SOURCE_SHA256, StudyManifest,
                                    canonical, digest, evidence_split, file_hash, stream_id)
from taskcognition.fixtures import PACKAGE_HASHES, build_rows, run_fixture, verify_fixture
from taskcognition.stages import guard_final_collection, read_training_rows, require_p00
from taskcognition.targets import aggregate


class TargetTests(unittest.TestCase):
    def agg(self, ds, rs):
        row, draws, _ = build_rows(ds=ds, rs=rs)
        return aggregate(row, draws, len(ds), PACKAGE_HASHES)

    def test_analytical_k4(self):
        a = self.agg([1, 1, 1, 0], [1, 1, 0, 0])
        self.assertEqual((a.mean_score_D, a.mean_score_R, a.benefit, a.joint_spoilage,
                          a.direct_redraw, a.decline_010, a.decline_025, a.winner),
                         (.75, .5, -.25, .375, .25, .375, .375, 0))

    def test_partial_credit_not_exact_match(self):
        a = self.agg([1, .5], [.75, .75])
        self.assertEqual((a.benefit, a.joint_spoilage, a.perfect_rate_R, a.winner), (0, .5, 0, 0))
        self.assertEqual(a.decline_025, .5)

    def test_all_perfect_and_exact_ties_direct(self):
        a = self.agg([1]*4, [1]*4)
        self.assertEqual((a.benefit, a.joint_spoilage, a.direct_redraw, a.winner), (0, 0, 0, 0))

    def test_equal_distributions_can_have_spoilage(self):
        a = self.agg([1, 0], [1, 0])
        self.assertEqual((a.benefit, a.joint_spoilage, a.direct_redraw), (0, .25, .5))

    def test_near_one_is_not_perfect(self):
        a = self.agg([1-1e-12]*2, [1]*2)
        self.assertEqual(a.perfect_rate_D, 0)
        self.assertGreater(a.benefit, 0)

    def test_k_one_rejected(self):
        with self.assertRaises(IntegrityError):
            self.agg([1], [0])

    def test_missing_draw_not_zero_imputed(self):
        row, draws, _ = build_rows()
        with self.assertRaises(IntegrityError):
            aggregate(row, draws[:-1], 4, PACKAGE_HASHES)

    def test_duplicate_draw_id_rejected(self):
        row, draws, _ = build_rows()
        draws[-1] = draws[-2]
        with self.assertRaisesRegex(IntegrityError, "duplicate draw"):
            aggregate(row, draws, 4, PACKAGE_HASHES)

    def test_cross_mode_rng_reuse_rejected(self):
        row, draws, _ = build_rows()
        draws[-1] = replace(draws[-1], stream_id=draws[0].stream_id)
        with self.assertRaisesRegex(IntegrityError, "sampling stream"):
            aggregate(row, draws, 4, PACKAGE_HASHES)

    def test_mixed_evidence_or_split_rejected(self):
        row, draws, _ = build_rows()
        for change in ({"evidence_kind": "development_observation"}, {"split": "TEST"}):
            mixed = draws[:-1] + [replace(draws[-1], **change)]
            with self.assertRaises(IntegrityError):
                aggregate(row, mixed, 4, PACKAGE_HASHES)

    def test_wrong_package_rejected(self):
        row, draws, _ = build_rows()
        with self.assertRaises(IntegrityError):
            aggregate(row, draws, 4, {"D": digest("unexpected"), "R": PACKAGE_HASHES["R"]})

    def test_invalid_score_cost_correctness(self):
        _, draws, _ = build_rows()
        for field, values in {"native_score": [-.1, 1.1, float("nan"), float("inf"), True],
                              "scalar_cost": [-1, float("inf")], "perfect_correct": [False, 1]}.items():
            for value in values:
                with self.subTest(field=field, value=value), self.assertRaises(IntegrityError):
                    replace(draws[0], **{field: value})

    def test_mixed_cost_units_rejected(self):
        row, draws, _ = build_rows()
        draws[0] = replace(draws[0], cost_unit="seconds")
        with self.assertRaises(IntegrityError):
            aggregate(row, draws, 4, PACKAGE_HASHES)

    def test_admitted_failure_retained(self):
        row, draws, _ = build_rows()
        draws[3] = replace(draws[3], status="admitted_failure")
        a = aggregate(row, draws, 4, PACKAGE_HASHES)
        self.assertEqual(a.status_counts["admitted_failure"], 1)
        self.assertEqual(a.mean_score_D, .75)


class GuardTests(unittest.TestCase):
    def test_no_final_collection_without_freeze(self):
        for split in ("TRAIN", "TUNE", "AUDIT", "TEST"):
            with self.subTest(split=split), self.assertRaisesRegex(IntegrityError, "freeze"):
                guard_final_collection(split, None, None)

    def test_hash_or_fake_freeze_cannot_enable_p00(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"fake.json"
            write_new(path, {"status": "SEALED"})
            with self.assertRaisesRegex(IntegrityError, "mismatch"):
                guard_final_collection("TRAIN", path, "0"*64)
            with self.assertRaisesRegex(IntegrityError, "P00 forbids"):
                guard_final_collection("TRAIN", path, file_hash(path))

    def test_train_reader_rejects_all_nontrain_splits(self):
        train = build_rows(split="TRAIN")[0]
        self.assertEqual(read_training_rows([train], "fixture"), [train])
        for split in ("DEVELOPMENT", "TUNE", "AUDIT", "TEST"):
            with self.subTest(split=split), self.assertRaises(IntegrityError):
                read_training_rows([train, build_rows(split=split)[0]], "fixture")
        with self.assertRaises(IntegrityError):
            read_training_rows([train], "development_observation")

    def test_final_label_kinds_match_exact_split(self):
        for kind, correct_split in (("final_train_labels", "TRAIN"), ("final_tune_labels", "TUNE")):
            for split in ("DEVELOPMENT", "TRAIN", "TUNE", "AUDIT", "TEST"):
                with self.subTest(kind=kind, split=split):
                    if split == correct_split:
                        evidence_split(kind, split)
                        row = replace(build_rows(split=split)[0], evidence_kind=kind)
                        self.assertEqual(row.split, split)
                    else:
                        with self.assertRaises(IntegrityError):
                            evidence_split(kind, split)

    def test_final_label_kinds_do_not_authorize_collection(self):
        for kind, split in (("final_train_labels", "TRAIN"), ("final_tune_labels", "TUNE")):
            evidence_split(kind, split)
            with self.assertRaisesRegex(IntegrityError, "freeze"):
                guard_final_collection(split, None, None)
        train = replace(build_rows(split="TRAIN")[0], evidence_kind="final_train_labels")
        tune = replace(build_rows(split="TUNE")[0], evidence_kind="final_tune_labels")
        self.assertEqual(read_training_rows([train], "final_train_labels"), [train])
        with self.assertRaises(IntegrityError):
            read_training_rows([tune], "final_tune_labels")

    def test_feature_allowlist_rejects_leaks(self):
        good = {"evidence_kind": "fixture", "input_id": "key-only", "text": "123", "character_count": 3}
        FeatureRecord.from_dict(good)
        for field in ("family", "dataset_id", "gold", "answer", "trace", "native_score", "generator_config", "latent_id", "verifier_feedback", "draft", "metadata"):
            with self.subTest(field=field), self.assertRaises(IntegrityError):
                FeatureRecord.from_dict({**good, field: "leak"})
        with self.assertRaises(IntegrityError):
            FeatureRecord.from_dict({**good, "character_count": 999})

    def test_stage_guard_rejects_unauthorized_phase(self):
        for state in ({}, {"active_phase": "P01", "status": "IN_PROGRESS"}, {"active_phase": "P00", "status": "SEALED"}):
            with self.assertRaises(IntegrityError):
                require_p00(state)

    def test_manifest_scope_and_freeze(self):
        kwargs = dict(study_id="fixture", evidence_kind="fixture", source_sha256=SOURCE_SHA256,
                      model_id="Qwen/Qwen3-8B", model_revision=None, package_hashes=PACKAGE_HASHES,
                      design={"K": None, "alpha": None})
        StudyManifest(**kwargs)
        for change in ({"model_id": "another/checkpoint"}, {"source_sha256": "0"*64}, {"status": "SEALED"}):
            with self.assertRaises(IntegrityError):
                StudyManifest(**{**kwargs, **change})


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.output = self.root/"artifacts/fixtures/test"

    def test_complete_roundtrip_and_resume_are_immutable(self):
        first = run_fixture(self.root, self.output)
        before = {p: file_hash(p) for p in self.output.rglob("*") if p.is_file()}
        self.assertEqual(run_fixture(self.root, self.output, resume=True), first)
        self.assertEqual(before, {p: file_hash(p) for p in before})
        with self.assertRaises(IntegrityError):
            run_fixture(self.root, self.output)

    def test_deterministic_artifacts_across_directories(self):
        a = run_fixture(self.root, self.output)
        b = run_fixture(self.root, self.output.parent/"second")
        self.assertEqual(a["manifest_sha256"], b["manifest_sha256"])

    def test_dry_run_writes_nothing(self):
        run_fixture(self.root, self.output, dry_run=True)
        self.assertFalse(self.output.exists())

    def test_final_development_and_traversal_output_rejected(self):
        for path in ("artifacts/final/a", "artifacts/development/a", "artifacts/fixtures/../../final/a"):
            with self.subTest(path=path), self.assertRaises(IntegrityError):
                run_fixture(self.root, self.root/path)

    def test_missing_corrupted_unexpected_evidence_rejected(self):
        for change in ("missing", "corrupt", "extra"):
            out = self.output.parent/change
            run_fixture(self.root, out)
            raw = next((out/"raw").glob("*.json"))
            if change == "missing":
                raw.unlink()
            elif change == "corrupt":
                raw.write_text("{}")
            else:
                (out/"extra.json").write_text("{}")
            with self.subTest(change=change), self.assertRaises(IntegrityError):
                verify_fixture(out)

    def test_rehashed_wrong_report_still_fails_recomputation(self):
        run_fixture(self.root, self.output)
        report = read_json(self.output/"report.json")
        report["balanced_mean_benefit"] = 1
        (self.output/"report.json").write_bytes(canonical(report))
        manifest = read_json(self.output/"manifest.json")
        manifest["files"]["report.json"] = file_hash(self.output/"report.json")
        (self.output/"manifest.json").write_bytes(canonical(manifest))
        with self.assertRaisesRegex(IntegrityError, "recompute"):
            verify_fixture(self.output)

    def test_interrupted_write_is_retained_not_regenerated(self):
        self.output.mkdir(parents=True)
        write_new(self.output/"intent.json", {"evidence_kind": "fixture"})
        with self.assertRaises(FileNotFoundError):
            run_fixture(self.root, self.output, resume=True)
        self.assertEqual(list(self.output.iterdir()), [self.output/"intent.json"])

    def test_immutable_write(self):
        path = self.root/"a.json"
        write_new(path, {"x": 1})
        with self.assertRaises(FileExistsError):
            write_new(path, {"x": 2})
        self.assertEqual(read_json(path), {"x": 1})

    def test_json_duplicate_keys_nonfinite_and_path_escape(self):
        path = self.root/"a.json"
        for text in ('{"x":1,"x":2}', '{"x":NaN}'):
            path.write_text(text)
            with self.assertRaises(IntegrityError):
                read_json(path)
        with self.assertRaises(IntegrityError):
            child_path(self.root, "../outside.json")

    def test_canonical_hash_and_disjoint_streams(self):
        self.assertEqual(digest({"a": 1, "b": 2}), digest({"b": 2, "a": 1}))
        streams = {stream_id("s", 0, split, "i", PACKAGE_HASHES[mode], index)
                   for split in ("TRAIN", "TUNE", "AUDIT", "TEST") for mode in ("D", "R") for index in range(4)}
        self.assertEqual(len(streams), 32)
        with self.assertRaises(ValueError):
            canonical({"x": float("nan")})

    def test_cli_collect_is_guard_only(self):
        with patch("builtins.print"):
            self.assertEqual(main(["--root", str(self.root), "collect", "--split", "TRAIN"]), 2)

    def test_doctor_does_not_load_models(self):
        from taskcognition.doctor import inventory
        with patch("taskcognition.doctor.command", return_value={"exit": None}), patch("taskcognition.doctor.cache_inventory", return_value={}):
            result = inventory(self.root)
        self.assertEqual(result["actual_model_calls"], 0)
        self.assertFalse(result["gpu_runtime_verified"])
        self.assertFalse(result["source_matches"])


if __name__ == "__main__":
    unittest.main()
