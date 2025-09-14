from typing import Optional
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

def header(title: str) -> None:
    print(Fore.CYAN + "=" * 64)
    print(Fore.CYAN + f"{title}".center(64))
    print(Fore.CYAN + "=" * 64 + Style.RESET_ALL)

def prompt(msg: str) -> str:
    try:
        return input(Fore.YELLOW + msg + Style.RESET_ALL)
    except (EOFError, KeyboardInterrupt):
        print()
        return ""

def main_menu() -> None:
    print(Fore.GREEN + "\n[1] System info")
    print("[2] List processes")
    print("[3] Check file permissions")
    print("[4] Folder size")
    print("[5] Environment variables")
    print("[6] Count files & directories")
    print("[7] Ping host")
    print("[8] Monitor CPU/RAM (bonus)")
    print("[0] Exit" + Style.RESET_ALL)

def env_menu() -> None:
    print(Fore.MAGENTA + "\nEnv Vars:")
    print("[1] List all")
    print("[2] Get a variable")
    print("[3] Set a variable")
    print("[4] Delete a variable")
    print("[0] Back" + Style.RESET_ALL)
