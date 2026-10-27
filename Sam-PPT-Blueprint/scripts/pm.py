"""Locate the installed ppt-master plugin (read-only; never modified).

Set PPT_MASTER_DIR to override; otherwise the newest plugin-cache copy is used.
Run as a script to print the path: python pm.py
"""
import glob
import os
import sys
from pathlib import Path


def ppt_master_dir() -> Path:
    env = os.environ.get("PPT_MASTER_DIR")
    if env:
        return Path(env)
    pattern = str(Path.home() / ".claude/plugins/cache/ppt-master/ppt-master/*/ppt-master/SKILL.md")
    found = sorted(glob.glob(pattern), key=os.path.getmtime)
    if not found:
        sys.exit("ppt-master not found; install the ppt-master plugin or set PPT_MASTER_DIR")
    return Path(found[-1]).parent


if __name__ == "__main__":
    print(ppt_master_dir())
