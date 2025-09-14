# Python System Utility (Cross-Platform CLI)

A small, cross‑platform **menu‑based** system utility written in Python.  
Designed to run on **Windows** and **Linux/macOS**, showcasing fundamentals like:
- System information
- Listing running processes
- File permission check
- Folder size calculation
- Environment variables (view / set / delete)
- Count files & directories
- Ping a host
- (Bonus) Uptime & CPU/RAM monitor

> Built as a clean, revisited version of an old "final lab" assignment.

---

##  Requirements
- Python 3.8+
- Packages: `psutil`, `colorama`  
  Install with:
  ```bash
  pip install -r requirements.txt
  ```

##  Run
```bash
python -m system_utility
```
or
```bash
python system_utility/main.py
```

##  Menu Features
1. **System Info** – OS, Python version, CPU cores, architecture, (uptime if available).
2. **List Processes** – Top processes (CPU/Memory). Uses `psutil` when available, falls back to native commands.
3. **Check File Permissions** – Read/Write/Execute and UNIX-style flags.
4. **Folder Size** – Recursively computes directory size (skips broken links).
5. **Environment Variables** – Sub‑menu: list, get, set, delete (affects current process only).
6. **Count Files & Directories** – Recursively counts files and folders under a path.
7. **Ping Host** – Cross‑platform ping (`ping -c 1` on Linux/macOS, `ping -n 1` on Windows).
8. **Monitor CPU/RAM (Bonus)** – Live monitor for a few seconds (requires `psutil`).

##  Notes
- Environment variable changes apply **only to the current process**.
- Some features degrade gracefully if `psutil` is not installed.
- Ping requires the `ping` executable to be available in your system `PATH`.

##  Project Layout
```
python-system-utility/
├─ system_utility/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ menu.py
│  └─ utils.py
├─ tests/
├─ requirements.txt
├─ .gitignore
└─ README.md
```

##  Example Session
```
[1] System info
[2] List processes
[3] Check file permissions
[4] Folder size
[5] Environment variables
[6] Count files & directories
[7] Ping host
[8] Monitor CPU/RAM (bonus)
[0] Exit
Select: 1
...
```
