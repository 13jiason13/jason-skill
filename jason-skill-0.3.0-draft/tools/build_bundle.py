"""Build a readable, self-contained file for forwarding and Codex installation."""
import hashlib
import json
from pathlib import Path
from install_bundle import ALLOWED, VERSION

ROOT = Path(__file__).resolve().parent.parent


def build():
    skill = ROOT / "skills/jason-skill"
    files = {}
    for name in sorted(ALLOWED):
        path = ROOT / "LICENSE" if name == "LICENSE" else skill / name
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != ROOT):
            raise ValueError("Refusing symlink in release input: " + name)
        content = path.read_text(encoding="utf-8")
        files[name] = {"text": content, "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest()}
    installer = (ROOT / "tools/install_bundle.py").read_text(encoding="utf-8")
    payload = {"format": 1, "name": "jason-skill", "version": VERSION, "files": files}
    header = """# Jason Skill 0.3.0-draft — single-file installer

THIS FILE IS A DRAFT FOR REVIEW. It is not a published release.

Attach this file to Codex with local file and terminal tools, then ask: Install Jason Skill, install the required desktop and browser tools, and run acceptance.

Python 3.8+ is required. On Windows, use py -3 instead of python3 when appropriate.

Installation has three steps and is incomplete until required tools are installed:
1. Install the skill files.
2. Install required tools: agent-desktop and agent-browser. Cua is optional.
3. Run acceptance on this computer.

For the receiving agent:
1. Inspect the installer and JSON manifest.
2. Save the Python code block as a temporary install_bundle.py, then run python3 install_bundle.py <this-file> --with-required-tools. Default location: ~/.agents/skills/jason-skill. Inspect existing installations in the host's skill directories and use --skills-root if needed. Updating with --replace preserves a backup outside the scanned skill directory.
3. Do not report installation as complete until required tools (agent-desktop and agent-browser) are installed. Cua is optional; add --include-cua only when requested. Use --pinned to install the distribution's pinned versions in their dedicated directories.
4. macOS and Windows are separate install paths. Do not collapse them.
   - macOS: the installer selects official native arm64 or x86_64 assets. After tool install, the recipient grants Accessibility and Screen Recording in System Settings > Privacy & Security. Scripts do not edit TCC.
   - Windows: use py -3 where needed. Windows x64 uses native official assets. Windows 11 ARM uses native ARM64 agent-desktop and official x64 agent-browser through OS emulation, subject to a runtime and page test. Windows 10 ARM has no pinned official agent-browser asset. Desktop operations need a signed-in interactive session; do not use a locked or disconnected session.
   - Linux and other systems: official agent-desktop and agent-browser assets are unavailable. File-route acceptance can still run. A complete install cannot be finished on this OS.
5. Read the installed SKILL.md, run scripts/doctor.py, and report these states separately: installed, connected, permissions granted, acceptance passed.
6. Run scripts/accept.py --all. Use the local file check, acceptance/browser-fixture.html, and the OS-specific form in acceptance/macos/ or acceptance/windows/. System grants and account access belong to the recipient.

Validate this entire file against the checksum from a trusted review or release. Embedded hashes detect corruption but do not authenticate a publisher.

## Readable installer

"""
    text = header + "```python\n" + installer + "```\n\n## Complete skill payload (UTF-8)\n\n"
    text += "```json jason-skill-bundle\n" + json.dumps(payload, ensure_ascii=False, indent=2) + "\n```\n"
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    path = out / "Jason-Skill-0.3.0-draft-install.txt"
    path.write_bytes(text.encode("utf-8"))
    (out / "SHA256SUMS.txt").write_text(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.name + "\n")
    return path


if __name__ == "__main__":
    print(build())
