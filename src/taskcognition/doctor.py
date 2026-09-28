"""Read-only, no-generation inventory. Never imports torch or contacts a model hub."""
import ctypes
import importlib.metadata
import os
import platform
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from .contracts import SOURCE_SHA256, file_hash


def command(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=20)
        return {"exit": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"exit": None, "error": type(exc).__name__}


def memory():
    if os.name == "nt":
        class Status(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [
                (name, ctypes.c_ulonglong) for name in ("total_physical", "available_physical", "total_page", "available_page", "total_virtual", "available_virtual", "extended")]
        status = Status()
        status.length = ctypes.sizeof(status)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return {"total_bytes": status.total_physical, "available_bytes": status.available_physical}
    return {"status": "unavailable"}


def cache_inventory(root):
    # Only known model cache locations and task-local model directories, never home enumeration.
    locations = {"default_hf_hub": Path.home()/".cache/huggingface/hub",
                 "project_models": root/"models", "project_cache": root/".cache"}
    for var in ("HF_HOME", "HF_HUB_CACHE", "HUGGINGFACE_HUB_CACHE", "TRANSFORMERS_CACHE"):
        if os.environ.get(var):
            locations[var] = Path(os.environ[var]) / "hub" if var == "HF_HOME" else Path(os.environ[var])
    result = []
    for label, path in locations.items():
        try:
            matches = [p for p in path.glob("*Qwen*") if p.is_dir()] if path.is_dir() else []
            result.append({"location_label": label, "exists": path.is_dir(), "qwen_directories": len(matches),
                           "qwen_file_bytes": sum(f.stat().st_size for p in matches for f in p.rglob("*") if f.is_file())})
        except OSError:
            result.append({"location_label": label, "status": "unreadable"})
    return {"bounded_search_only": True, "locations": result}


def inventory(root: Path):
    versions = {}
    for name in ("taskcognition", "pip", "setuptools", "wheel", "torch", "transformers", "accelerate", "huggingface-hub"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    pdf = root/"reference/TaskCognition_Revised_Verified.pdf"
    disk = shutil.disk_usage(root)
    os_info = {"system": platform.system(), "release": platform.release(), "version": platform.version(), "machine": platform.machine()}
    if os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                os_info["processor"] = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        except OSError:
            os_info["processor"] = "unavailable"
    return {"evidence_kind": "development_observation", "artifact_role": "environment_inventory_no_generation",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(), "actual_model_calls": 0,
            "os": os_info, "logical_cpu_count": os.cpu_count(), "memory": memory(),
            "disk": {"total_bytes": disk.total, "free_bytes": disk.free},
            "python": {"version": sys.version, "project_local": sys.prefix != sys.base_prefix, "packages": versions},
            "tools_on_path": {name: shutil.which(name) is not None for name in ("python", "py", "uv", "git", "nvidia-smi", "nvcc", "pdftoppm")},
            "shell": command(["pwsh", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]),
            "gpu": command(["nvidia-smi", "--query-gpu=name,memory.total,memory.free,driver_version,compute_cap", "--format=csv,noheader"]),
            "gpu_runtime_verified": False, "qwen_cache": cache_inventory(root),
            "source_sha256": file_hash(pdf) if pdf.is_file() else None,
            "source_matches": pdf.is_file() and file_hash(pdf) == SOURCE_SHA256,
            "git": {"branch": command(["git", "-C", str(root), "branch", "--show-current"]),
                    "head": command(["git", "-C", str(root), "rev-parse", "HEAD"])}}
