"""Synthetic local acceptance for file, browser, and desktop routes.

No accounts, cookies, private files, or real-operation recordings are used.
File checks run here. Browser and desktop checks report the OS-specific procedure
and only pass when the recipient verifies the actual result.
"""
import argparse
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import doctor

ACCEPTANCE = Path(__file__).resolve().parent.parent / "acceptance"
EXPECTED_TEXT = "Jason parity"
EXPECTED_PAGE = "Jason parity | enabled"


def run_files(workspace=None):
    cleanup = workspace is None
    root = Path(workspace) if workspace else Path(tempfile.mkdtemp(prefix="jason-accept-files-"))
    root.mkdir(parents=True, exist_ok=True)
    try:
        source = root / "parity.txt"
        done = root / "done"
        source.write_text(EXPECTED_TEXT + "\n", encoding="utf-8")
        done.mkdir()
        destination = done / "parity.txt"
        shutil.move(str(source), str(destination))
        passed = (
            not source.exists()
            and destination.is_file()
            and destination.read_text(encoding="utf-8") == EXPECTED_TEXT + "\n"
        )
        return {
            "check": "files",
            "passed": passed,
            "expected": "Create parity.txt containing 'Jason parity', move it to done/, verify the source is gone and the destination content matches.",
            "workspace": str(root),
            "cleaned": cleanup,
        }
    finally:
        if cleanup:
            shutil.rmtree(root, ignore_errors=True)


def browser_check(system):
    fixture = ACCEPTANCE / "browser-fixture.html"
    steps = [
        "Open acceptance/browser-fixture.html in an isolated agent-browser session, or the host isolated browser.",
        "Enter 'Jason parity', check Enable test, and click Save locally.",
        "Verify the rendered page shows 'Jason parity | enabled'.",
    ]
    if system not in ("Darwin", "Windows"):
        return {
            "check": "browser",
            "passed": False,
            "status": "official-tools-unavailable",
            "fixture": str(fixture),
            "expected_result": EXPECTED_PAGE,
            "steps": steps,
            "note": "Official agent-browser assets are for macOS and Windows only. This check is not claimed as passed.",
        }
    return {
        "check": "browser",
        "passed": False,
        "status": "recipient-must-verify-rendered-page",
        "fixture": str(fixture),
        "expected_result": EXPECTED_PAGE,
        "steps": steps,
        "note": "A delivery acknowledgment is not enough. Record a pass only after the page shows the expected text.",
    }


def desktop_check(system):
    verifier = ACCEPTANCE / "check_result.py"
    if system == "Darwin":
        form = ACCEPTANCE / "macos/MacForm.swift"
        return {
            "check": "desktop",
            "passed": False,
            "status": "recipient-must-verify-saved-form",
            "platform": "macOS",
            "permissions": ["Accessibility", "Screen Recording"],
            "form": str(form),
            "steps": [
                "Grant Accessibility and Screen Recording in System Settings if not already granted.",
                "Compile and open the owned macOS test form, then enter 'Jason parity', click Add one once, check Enable test, and click Save test.",
                "Read back the application state and validate the JSON with check_result.py.",
            ],
            "commands": [
                'probe_dir="$(mktemp -d)"',
                'xcrun swiftc -parse-as-library "' + str(form) + '" -o "$probe_dir/JasonParityTest"',
                '"$probe_dir/JasonParityTest" "$probe_dir/result.json"',
                'python3 "' + str(verifier) + '" "$probe_dir/result.json"',
            ],
            "note": "Requires Xcode Command Line Tools. Record a pass only after check_result.py reports PASS.",
        }
    if system == "Windows":
        form = ACCEPTANCE / "windows/WindowsForm.ps1"
        return {
            "check": "desktop",
            "passed": False,
            "status": "recipient-must-verify-saved-form",
            "platform": "Windows",
            "permissions": ["Interactive signed-in desktop session"],
            "form": str(form),
            "steps": [
                "Run the following from the signed-in interactive desktop, not a locked or disconnected session.",
                "Enter 'Jason parity', click Add one once, check Enable test, and click Save test.",
                "Read back the application state and validate the JSON with check_result.py.",
            ],
            "commands": [
                '$result = Join-Path $env:TEMP ("jason-parity-" + [guid]::NewGuid().ToString("N") + ".json")',
                "Write-Output $result",
                'powershell -NoProfile -STA -File "' + str(form) + '" -ResultFile $result',
                'py -3 "' + str(verifier) + '" $result',
            ],
            "note": "Record a pass only after check_result.py reports PASS.",
        }
    return {
        "check": "desktop",
        "passed": False,
        "status": "official-tools-unavailable",
        "platform": system,
        "note": "Official agent-desktop assets and the shipped native test forms target macOS and Windows only.",
    }


def verify_desktop_result(path):
    verifier = ACCEPTANCE / "check_result.py"
    completed = subprocess.run(
        [sys.executable, str(verifier), str(path)],
        capture_output=True, text=True, timeout=10)
    return {
        "check": "desktop-result",
        "passed": completed.returncode == 0,
        "result_file": str(path),
        "output": (completed.stdout or completed.stderr).strip(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files", action="store_true", help="Run the synthetic file-organization check")
    parser.add_argument("--browser", action="store_true", help="Print the local browser-fixture procedure")
    parser.add_argument("--desktop", action="store_true", help="Print the OS-specific native form procedure")
    parser.add_argument("--all", action="store_true", help="Run files and report browser plus desktop procedures")
    parser.add_argument("--workspace", type=Path, help="Optional workspace for the file check; kept on disk")
    parser.add_argument("--verify-desktop-result", type=Path, help="Validate a saved native-form JSON")
    args = parser.parse_args()
    system = platform.system()
    selected = []
    if args.all or args.files or not (args.browser or args.desktop or args.verify_desktop_result or args.all or args.files):
        # Default to --all when no check is named, so a bare run shows the full pack.
        if not (args.files or args.browser or args.desktop or args.verify_desktop_result):
            args.all = True
    if args.all or args.files:
        selected.append(run_files(args.workspace))
    if args.all or args.browser:
        selected.append(browser_check(system))
    if args.all or args.desktop:
        selected.append(desktop_check(system))
    if args.verify_desktop_result:
        selected.append(verify_desktop_result(args.verify_desktop_result))
    report = {
        "platform": system,
        "official_tools_supported": doctor.official_tools_supported(system),
        "checks": selected,
        "acceptance_passed": all(item.get("passed") for item in selected) if selected else False,
        "states": {
            "installed": "see doctor.py / setup_all.py",
            "connected": "host-must-confirm",
            "permissions_granted": "recipient-must-grant",
            "acceptance_passed": all(item.get("passed") for item in selected) if selected else False,
        },
        "note": (
            "File checks can pass on this machine. Browser and desktop routes pass only after the "
            "rendered page or saved form is actually verified. Official browser and desktop tools "
            "are for macOS and Windows."
        ),
    }
    # Bare --all should not claim overall acceptance just because the file check passed
    # while browser/desktop still require a recipient-verified GUI result.
    if any(item.get("status") in {"recipient-must-verify-rendered-page", "recipient-must-verify-saved-form", "official-tools-unavailable"} for item in selected):
        report["acceptance_passed"] = False
        report["states"]["acceptance_passed"] = False
        report["incomplete_reason"] = "Browser and/or desktop acceptance still needs a verified actual result on a supported OS."
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not selected:
        return 1
    runnable = [item for item in selected if item["check"] in {"files", "desktop-result"}]
    if runnable and not all(item.get("passed") for item in runnable):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
