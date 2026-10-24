"""PreToolUse hook: editing a file that holds the locked visual style asks the user first.

Locked: style-lock.md and its hash manifest, the page-frame templates and style/deck specs,
the approved samples, rules.md, page-patterns.md, quick-card.md, style_guard.py.
The user sees the reason and approves or rejects each such edit (references/style-lock.md).
"""
import json
import re
import sys

LOCKED = re.compile(
    r"Sam-PPT-Bain[\\/]+(references[\\/]+(style-lock\.(md|sha256\.json)|approved[\\/]|rules\.md|page-patterns\.md|quick-card\.md)"
    r"|template[\\/]+templates[\\/]|scripts[\\/]+style_guard\.py)", re.I)

event = json.load(sys.stdin)
inp = event.get("tool_input", {})
target = inp.get("file_path") or inp.get("notebook_path") or ""
if event.get("tool_name") in ("Bash", "PowerShell"):
    target = inp.get("command", "") if re.search(r"(sed\s+-i|>\s*\S|Set-Content|Out-File|mv |cp |rm )", inp.get("command", "")) else ""
if target and LOCKED.search(target):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "This edits the locked visual style of Sam-PPT-Bain (references/style-lock.md). "
                                    "Allow only if the user explicitly approved changing this item.",
    }}))
sys.exit(0)
