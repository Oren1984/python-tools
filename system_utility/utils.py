# Utility functions for system_utility
# Provides common helpers reused across the tool

import os
import sys
import time
import json
import math
import shutil
import platform
import subprocess
from datetime import datetime
from typing import Optional, Tuple

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover
    psutil = None  # graceful degradation

def human_bytes(num: int) -> str:
    if num < 0:
        return f"-{human_bytes(abs(num))}"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    if num == 0:
        return "0 B"
    i = int(math.floor(math.log(num, 1024))) if num > 0 else 0
    i = min(i, len(units) - 1)
    p = math.pow(1024, i)
    s = round(num / p, 2)
    return f"{s} {units[i]}"

def system_info() -> dict:
    info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "hostname": platform.node(),
    }
    # uptime
    if psutil and hasattr(psutil, "boot_time"):
        boot_ts = psutil.boot_time()
        info["boot_time"] = datetime.fromtimestamp(boot_ts).isoformat(timespec="seconds")
        info["uptime_seconds"] = int(time.time() - boot_ts)
    else:
        # Attempt shell uptime (Linux/macOS)
        try:
            if platform.system() != "Windows":
                out = subprocess.check_output(["uptime", "-p"], text=True).strip()
                info["uptime_pretty"] = out
        except Exception:
            pass
    return info

def list_processes(top_n: int = 15) -> list:
    """Return a list of dictionaries with process info."""
    procs = []
    if psutil:
        try:
            for p in psutil.process_iter(attrs=["pid", "name", "username", "cpu_percent", "memory_info"]):
                mem = getattr(p.info.get("memory_info"), "rss", 0) if p.info.get("memory_info") else 0
                procs.append({
                    "pid": p.info.get("pid"),
                    "name": p.info.get("name"),
                    "user": p.info.get("username"),
                    "cpu": p.info.get("cpu_percent"),
                    "rss": mem,
                })
            # sort by rss desc
            procs.sort(key=lambda x: x["rss"] or 0, reverse=True)
            return procs[:top_n]
        except Exception:
            # fallback to shell below
            pass

    # Fallback using shell
    try:
        if platform.system() == "Windows":
            cmd = ["tasklist"]
            out = subprocess.check_output(cmd, text=True, errors="ignore")
            lines = out.strip().splitlines()[3:]
            for line in lines[:top_n]:
                procs.append({"pid": None, "name": line.strip(), "user": None, "cpu": None, "rss": None})
        else:
            cmd = ["ps", "aux"]
            out = subprocess.check_output(cmd, text=True, errors="ignore")
            lines = out.strip().splitlines()[1: top_n+1]
            for line in lines:
                procs.append({"pid": None, "name": line.strip(), "user": None, "cpu": None, "rss": None})
    except Exception as e:
        procs.append({"error": f"Failed to list processes: {e}"})
    return procs

def check_permissions(path: str) -> dict:
    path = os.path.expanduser(os.path.expandvars(path))
    result = {
        "exists": os.path.exists(path),
        "is_file": os.path.isfile(path),
        "is_dir": os.path.isdir(path),
        "readable": os.access(path, os.R_OK),
        "writable": os.access(path, os.W_OK),
        "executable": os.access(path, os.X_OK),
        "mode_unix": None,
    }
    try:
        st = os.stat(path)
        result["mode_unix"] = oct(st.st_mode & 0o777)
    except Exception:
        pass
    return result

def folder_size(path: str) -> Tuple[int, int, int]:
    """Return total_size_bytes, files_count, dirs_count"""
    path = os.path.expanduser(os.path.expandvars(path))
    total = 0
    files = 0
    dirs = 0
    for root, dirnames, filenames in os.walk(path, onerror=None, followlinks=False):
        dirs += len(dirnames)
        for fname in filenames:
            fp = os.path.join(root, fname)
            try:
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)
                    files += 1
            except Exception:
                continue
    return total, files, dirs

def env_list() -> dict:
    return dict(os.environ)

def env_get(key: str) -> Optional[str]:
    return os.environ.get(key)

def env_set(key: str, value: str) -> None:
    os.environ[key] = value  # current process only

def env_del(key: str) -> bool:
    if key in os.environ:
        del os.environ[key]
        return True
    return False

def count_files_dirs(path: str) -> Tuple[int, int]:
    path = os.path.expanduser(os.path.expandvars(path))
    files = 0
    dirs = 0
    for root, dirnames, filenames in os.walk(path, followlinks=False):
        dirs += len(dirnames)
        files += len(filenames)
    return files, dirs

def ping_host(host: str, timeout: int = 2) -> Tuple[bool, Optional[str]]:
    system = platform.system()
    if system == "Windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), host]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, errors="ignore")
        return True, out
    except subprocess.CalledProcessError as e:
        return False, e.output
    except FileNotFoundError:
        return False, "ping command not found. Ensure it's available on PATH."

def monitor_cpu_ram(seconds: int = 10, interval: float = 1.0) -> list:
    """Return a list of (timestamp, cpu_percent, mem_percent)."""
    if not psutil:
        return []
    data = []
    # initial call for cpu_percent to set baseline
    psutil.cpu_percent(interval=None)
    for _ in range(int(seconds/interval)):
        cpu = psutil.cpu_percent(interval=interval)
        mem = psutil.virtual_memory().percent
        data.append({
            "ts": datetime.now().isoformat(timespec="seconds"),
            "cpu_percent": cpu,
            "mem_percent": mem
        })
    return data
