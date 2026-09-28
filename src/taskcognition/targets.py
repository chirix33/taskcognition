"""Per-input finite-K estimators only; no audit/test inference in P00."""
from collections import Counter
from statistics import fmean
from .contracts import AggregateRecord, IntegrityError, InputRecord, DrawRecord, integer


def aggregate(input_row: InputRecord, draws: list[DrawRecord], k: int, package_hashes: dict[str, str]) -> AggregateRecord:
    integer(k, 2)
    if len(draws) != 2 * k:
        raise IntegrityError("incomplete input cluster")
    if len({d.draw_id for d in draws}) != len(draws):
        raise IntegrityError("duplicate draw ID")
    if len({d.stream_id for d in draws}) != len(draws):
        raise IntegrityError("reused sampling stream")
    for d in draws:
        if (d.input_id, d.split, d.evidence_kind) != (input_row.input_id, input_row.split, input_row.evidence_kind):
            raise IntegrityError("mixed cluster/split/evidence kind")
        if d.package_hash != package_hashes[d.mode]:
            raise IntegrityError("unexpected package hash")
    if len({d.cost_unit for d in draws}) != 1:
        raise IntegrityError("mixed scalar cost units")
    groups = {mode: [d for d in draws if d.mode == mode] for mode in ("D", "R")}
    if any(len(g) != k or {d.draw_index for d in g} != set(range(k)) for g in groups.values()):
        raise IntegrityError("missing/duplicate draw index")
    ds, rs = ([d.native_score for d in groups[m]] for m in ("D", "R"))
    pd, pr = (fmean(d.perfect_correct for d in groups[m]) for m in ("D", "R"))
    md, mr = fmean(ds), fmean(rs)
    return AggregateRecord(
        input_row.evidence_kind, input_row.input_id, input_row.split, input_row.family, k,
        md, mr, pd, pr, mr-md, pd*(1-pr), k/(k-1)*pd*(1-pd),
        sum(d-r >= 0.10 for d in ds for r in rs)/(k*k),
        sum(d-r >= 0.25 for d in ds for r in rs)/(k*k), int(mr > md),
        fmean(d.scalar_cost for d in groups["D"]), fmean(d.scalar_cost for d in groups["R"]),
        dict(Counter(d.status for d in draws)),
    )
