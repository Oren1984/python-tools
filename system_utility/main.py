# Entry point for the system_utility tool
# Provides CLI interface to run different utilities

import json
import sys
from colorama import Fore, Style
from .menu import header, prompt, main_menu, env_menu
from .utils import (
    system_info, list_processes, check_permissions, folder_size,
    env_list, env_get, env_set, env_del, count_files_dirs,
    ping_host, monitor_cpu_ram, human_bytes
)

def pretty(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

def run_env_menu():
    while True:
        env_menu()
        choice = prompt("Select (env): ").strip()
        if choice == "1":
            print(Fore.CYAN + "All environment variables:" + Style.RESET_ALL)
            pretty(env_list())
        elif choice == "2":
            key = prompt("Key to get: ").strip()
            val = env_get(key)
            print(Fore.CYAN + f"{key}=" + Style.RESET_ALL + f"{val}")
        elif choice == "3":
            key = prompt("Key to set: ").strip()
            value = prompt("Value: ").strip()
            env_set(key, value)
            print(Fore.GREEN + f"Set {key}." + Style.RESET_ALL)
        elif choice == "4":
            key = prompt("Key to delete: ").strip()
            ok = env_del(key)
            msg = "deleted" if ok else "not found"
            print(Fore.GREEN + f"{key} {msg}." + Style.RESET_ALL)
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)

def main():
    header("Python System Utility")
    while True:
        main_menu()
        choice = prompt("Select: ").strip()
        if choice == "1":
            header("System info")
            pretty(system_info())
        elif choice == "2":
            header("Top processes")
            procs = list_processes()
            pretty([
                {
                    "pid": p.get("pid"),
                    "name": p.get("name"),
                    "user": p.get("user"),
                    "cpu%": p.get("cpu"),
                    "rss": human_bytes(p.get("rss") or 0) if p.get("rss") is not None else None
                } for p in procs
            ])
        elif choice == "3":
            path = prompt("Enter file/folder path: ").strip()
            header("Permissions")
            pretty(check_permissions(path))
        elif choice == "4":
            path = prompt("Enter folder path: ").strip()
            header("Folder size")
            total, files, dirs = folder_size(path)
            pretty({"path": path, "size_bytes": total, "size_human": human_bytes(total), "files": files, "dirs": dirs})
        elif choice == "5":
            header("Environment Variables")
            print(Fore.YELLOW + "Note: Changes affect current process only." + Style.RESET_ALL)
            run_env_menu()
        elif choice == "6":
            path = prompt("Enter folder path: ").strip()
            header("Count files & directories")
            files, dirs = count_files_dirs(path)
            pretty({"path": path, "files": files, "dirs": dirs})
        elif choice == "7":
            host = prompt("Enter host to ping (e.g., 8.8.8.8 or example.com): ").strip()
            header(f"Ping {host}")
            ok, out = ping_host(host)
            print(Fore.GREEN + "SUCCESS" if ok else Fore.RED + "FAILED", Style.RESET_ALL)
            print(out)
        elif choice == "8":
            header("Monitor CPU/RAM (10s)")
            data = monitor_cpu_ram(seconds=10, interval=1.0)
            if not data:
                print(Fore.RED + "psutil is not installed. Install it to use this feature." + Style.RESET_ALL)
            else:
                pretty(data)
        elif choice == "0":
            print(Fore.CYAN + "Goodbye!" + Style.RESET_ALL)
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
