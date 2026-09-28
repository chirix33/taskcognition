"""Small immutable fixture bundles with complete, checked child hashes."""
import json
import os
from pathlib import Path
from .contracts import IntegrityError, canonical, file_hash, require_hash


def read_json(path: Path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise IntegrityError("duplicate JSON key")
            result[key] = value
        return result
    def invalid(value):
        raise IntegrityError("nonfinite JSON constant")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=invalid)


def write_new(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(canonical(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def child_path(root: Path, relative: str) -> Path:
    path = root / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(root.resolve()) or path.resolve() == root.resolve():
        raise IntegrityError("artifact path escapes bundle")
    return path


def fixture_output(root: Path, output: Path) -> Path:
    fixtures = (root / "artifacts/fixtures").resolve()
    resolved = output.resolve()
    if not resolved.is_relative_to(fixtures) or resolved == fixtures:
        raise IntegrityError("fixture output must be a run directory beneath artifacts/fixtures")
    return resolved


def verify_bundle(root: Path) -> dict:
    manifest = read_json(root / "manifest.json")
    if manifest.get("evidence_kind") != "fixture" or manifest.get("schema") != "p00-fixture-v1":
        raise IntegrityError("not a P00 fixture bundle")
    files = manifest.get("files")
    if not isinstance(files, dict) or not {"inputs.json", "draws.json", "aggregates.json", "report.json", "packages.json"}.issubset(files):
        raise IntegrityError("missing required fixture artifacts")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()} - {"manifest.json"}
    if set(files) != actual:
        raise IntegrityError("missing or unexpected bundle files")
    for relative, expected in files.items():
        require_hash(expected)
        path = child_path(root, relative)
        if not path.is_file() or file_hash(path) != expected:
            raise IntegrityError("artifact missing or hash mismatch: " + relative)
        obj = read_json(path)
        objects = obj if isinstance(obj, list) else [obj]
        if not objects or any(o.get("evidence_kind") != "fixture" for o in objects):
            raise IntegrityError("fixture evidence isolation violated")
    return manifest
