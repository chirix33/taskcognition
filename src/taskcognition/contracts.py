"""Strict P00 records. Fixture identities are not frozen model packages."""
from dataclasses import asdict, dataclass
from enum import StrEnum
import hashlib
import json
import math
from pathlib import Path

SOURCE_SHA256 = "9eed0fe74f46c3acbc200183cf11693f1bec66a1180568087aeb775c97d8f6c8"
FAMILIES = ("number_sorting", "number_format", "letter_counting", "graph_color", "shortest_path", "knights_knaves")


class IntegrityError(ValueError):
    """Evidence cannot be interpreted; never impute an answer score."""


class EvidenceKind(StrEnum):
    FIXTURE = "fixture"
    DEVELOPMENT = "development_observation"
    SIMULATION = "development_simulation"
    TRAIN_LABELS = "final_train_labels"
    TUNE_LABELS = "final_tune_labels"
    AUDIT = "confirmatory_audit"
    TEST = "confirmatory_test"
    SECONDARY = "secondary_descriptive"


class Split(StrEnum):
    DEVELOPMENT = "DEVELOPMENT"
    TRAIN = "TRAIN"
    TUNE = "TUNE"
    AUDIT = "AUDIT"
    TEST = "TEST"


def canonical(value) -> bytes:
    # No salted hash, nonfinite JSON values, or self-hash fields.
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require_hash(value: str):
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise IntegrityError("expected lowercase SHA-256")


def number(value, low=0.0, high=math.inf):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise IntegrityError("nonfinite, out-of-range, or nonnumeric value")


def integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise IntegrityError("invalid integer")


def evidence_split(kind: str, split: str):
    EvidenceKind(kind)
    Split(split)
    allowed = {
        "fixture": set(Split), "development_observation": {Split.DEVELOPMENT},
        "development_simulation": set(Split), "confirmatory_audit": {Split.AUDIT},
        "final_train_labels": {Split.TRAIN}, "final_tune_labels": {Split.TUNE},
        "confirmatory_test": {Split.TEST}, "secondary_descriptive": {Split.TEST},
    }
    if split not in allowed[kind]:
        raise IntegrityError("evidence kind/split mismatch")


def stream_id(study_id: str, root_seed: int, split: str, input_id: str, package_hash: str, draw_index: int) -> str:
    integer(root_seed)
    integer(draw_index)
    return digest(["answer-sampling-v1", study_id, root_seed, split, input_id, package_hash, draw_index])


@dataclass(frozen=True)
class StudyManifest:
    """Unfrozen bootstrap schema; not a production freeze validator."""
    study_id: str
    evidence_kind: str
    source_sha256: str
    model_id: str
    model_revision: str | None
    package_hashes: dict[str, str]
    design: dict
    status: str = "UNFROZEN"

    def __post_init__(self):
        EvidenceKind(self.evidence_kind)
        if self.source_sha256 != SOURCE_SHA256 or self.model_id != "Qwen/Qwen3-8B":
            raise IntegrityError("source/checkpoint scope mismatch")
        if self.status != "UNFROZEN":
            raise IntegrityError("P00 cannot create a frozen study")
        if set(self.package_hashes) != {"D", "R"}:
            raise IntegrityError("exactly D and R required")
        for value in self.package_hashes.values():
            require_hash(value)


@dataclass(frozen=True)
class InputRecord:
    evidence_kind: str
    input_id: str
    split: str
    family: str
    latent_sha256: str
    prompt: str
    input_token_length: int | None
    generation_seed: int
    generator_config_hash: str
    scorer_reference: str
    gold_reference: str

    def __post_init__(self):
        evidence_split(self.evidence_kind, self.split)
        if self.family not in FAMILIES or not self.input_id or not self.prompt:
            raise IntegrityError("invalid input identity/family/prompt")
        require_hash(self.latent_sha256)
        require_hash(self.generator_config_hash)
        integer(self.generation_seed)
        if self.input_token_length is not None:
            integer(self.input_token_length)


@dataclass(frozen=True)
class FeatureRecord:
    evidence_kind: str
    input_id: str
    text: str
    character_count: int

    def __post_init__(self):
        EvidenceKind(self.evidence_kind)
        integer(self.character_count)
        if not isinstance(self.text, str) or self.character_count != len(self.text):
            raise IntegrityError("feature must be derived from input text")

    @classmethod
    def from_dict(cls, value: dict):
        # Exact allowlist at the boundary, including no nested arbitrary metadata.
        if set(value) != {"evidence_kind", "input_id", "text", "character_count"}:
            raise IntegrityError("prohibited or unknown feature field")
        return cls(**value)


@dataclass(frozen=True)
class DrawRecord:
    evidence_kind: str
    draw_id: str
    input_id: str
    split: str
    mode: str
    package_hash: str
    draw_index: int
    stream_id: str
    raw_path: str
    raw_sha256: str
    native_score: float
    perfect_correct: bool
    scalar_cost: float
    cost_unit: str
    status: str

    def __post_init__(self):
        evidence_split(self.evidence_kind, self.split)
        if self.mode not in ("D", "R"):
            raise IntegrityError("unknown package mode")
        integer(self.draw_index)
        for value in (self.package_hash, self.stream_id, self.raw_sha256):
            require_hash(value)
        number(self.native_score, 0, 1)
        number(self.scalar_cost)
        if type(self.perfect_correct) is not bool or self.perfect_correct != (self.native_score == 1):
            raise IntegrityError("perfect correctness must be exact score equality")
        if self.status not in ("perfect", "partial", "wrong", "admitted_failure"):
            raise IntegrityError("unknown P00 status")
        expected = "perfect" if self.native_score == 1 else "partial" if self.native_score > 0 else "wrong"
        if self.status != expected and not (self.status == "admitted_failure" and self.native_score == 0):
            raise IntegrityError("score/status mismatch")
        if self.draw_id != digest([self.input_id, self.package_hash, self.draw_index]):
            raise IntegrityError("draw ID mismatch")


@dataclass(frozen=True)
class AggregateRecord:
    evidence_kind: str
    input_id: str
    split: str
    family: str
    k: int
    mean_score_D: float
    mean_score_R: float
    perfect_rate_D: float
    perfect_rate_R: float
    benefit: float
    joint_spoilage: float
    direct_redraw: float
    decline_010: float
    decline_025: float
    winner: int
    mean_cost_D: float
    mean_cost_R: float
    status_counts: dict[str, int]


def record_dict(record) -> dict:
    return asdict(record)
