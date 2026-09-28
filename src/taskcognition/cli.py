import argparse
import json
from pathlib import Path
from .artifacts import read_json, write_new
from .contracts import IntegrityError
from .doctor import inventory
from .fixtures import run_fixture, verify_fixture
from .stages import guard_final_collection, require_p00


def main(argv=None):
    parser = argparse.ArgumentParser(description="P00 offline tools; no generation/training backend")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor", help="read-only local inventory, no generation or network")
    doctor.add_argument("--output", type=Path)
    fixture = sub.add_parser("fixture-run")
    fixture.add_argument("--output", type=Path, required=True)
    fixture.add_argument("--resume", action="store_true", help="verify completed bundle; never regenerate partial evidence")
    fixture.add_argument("--dry-run", action="store_true")
    verify = sub.add_parser("verify-artifacts")
    verify.add_argument("--run", type=Path, required=True)
    collect = sub.add_parser("collect", help="guard-only stub; always rejects real collection in P00")
    collect.add_argument("--split", choices=["TRAIN", "TUNE", "AUDIT", "TEST"], required=True)
    collect.add_argument("--manifest", type=Path)
    collect.add_argument("--accepted-hash")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "doctor":
            result = inventory(root)
            if args.output:
                write_new(root / args.output, result)
            if not result["source_matches"]:
                raise IntegrityError("governing PDF hash mismatch/missing")
        elif args.command == "fixture-run":
            require_p00(read_json(root / "configs/phase_state.json"))
            result = run_fixture(root, root / args.output, args.resume, args.dry_run)
        elif args.command == "verify-artifacts":
            result = verify_fixture(root / args.run)
        else:
            guard_final_collection(args.split, root / args.manifest if args.manifest else None, args.accepted_hash)
    except (IntegrityError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "REJECTED", "error": str(exc)}))
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0
