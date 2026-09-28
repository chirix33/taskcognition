"""Capture bounded offline validation commands and real exit codes, without a model."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--environment-output", default="reports/environment_p00.json")
    args = parser.parse_args()
    if not args.run_id.replace("-", "").replace("_", "").isalnum():
        parser.error("run ID must be a simple directory name")
    if args.output.exists():
        parser.error("validation evidence already exists; choose a new output")
    root = Path(__file__).resolve().parents[1]
    cli = [sys.executable, "-m", "taskcognition"]
    run = "artifacts/fixtures/" + args.run_id
    commands = [
        ([sys.executable, "-m", "pip", "check"], 0),
        ([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], 0),
        (cli + ["doctor", "--output", args.environment_output], 0),
        (cli + ["fixture-run", "--output", run, "--dry-run"], 0),
        (cli + ["fixture-run", "--output", run], 0),
        (cli + ["verify-artifacts", "--run", run], 0),
        (cli + ["fixture-run", "--output", run, "--resume"], 0),
        (cli + ["collect", "--split", "TRAIN"], 2),
    ]
    started = time.perf_counter()
    report = {"evidence_kind": "development_observation", "artifact_role": "offline_software_validation",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(), "actual_model_calls": 0,
              "commands": []}
    for command, expected in commands:
        begin = time.perf_counter()
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=120)
        entry = {"argv": [".venv/python" if a == sys.executable else a for a in command],
                 "exit": result.returncode, "expected_exit": expected, "seconds": time.perf_counter()-begin,
                 "stdout": result.stdout.replace(str(root), "<repository>").replace(str(Path.home()), "<home>"),
                 "stderr": result.stderr.replace(str(root), "<repository>").replace(str(Path.home()), "<home>")}
        report["commands"].append(entry)
        print(json.dumps({"command": entry["argv"], "exit": result.returncode, "expected_exit": expected}))
        if result.returncode != expected:
            break
    report["elapsed_seconds"] = time.perf_counter()-started
    report["passed"] = len(report["commands"]) == len(commands) and all(c["exit"] == c["expected_exit"] for c in report["commands"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
