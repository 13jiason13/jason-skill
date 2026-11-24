"""Install the text bundle using Python's standard library only."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

NAME = "jason-skill"
VERSION = "0.3.0-draft"
ALLOWED = {
    "SKILL.md", "LICENSE", "agents/openai.yaml",
    "scripts/doctor.py", "scripts/setup_macos.py", "scripts/setup_tools.py",
    "scripts/setup_all.py", "scripts/setup_windows.py", "scripts/accept.py",
    "references/tools.md", "references/benchmark.md", "references/portable-install.md",
    "acceptance/browser-fixture.html", "acceptance/check_result.py",
    "acceptance/macos/MacForm.swift", "acceptance/windows/WindowsForm.ps1",
    "acceptance/README.md",
}


def load_bundle(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    blocks = re.findall(r"(?m)^```json jason-skill-bundle\r?\n([\s\S]*?)^```[ \t]*\r?$", text)
    if len(blocks) != 1:
        raise ValueError("Expected exactly one bundle payload")
    bundle = json.loads(blocks[0])
    if bundle.get("name") != NAME or bundle.get("format") != 1:
        raise ValueError("Unsupported bundle")
    files = bundle.get("files")
    if not isinstance(files, dict) or set(files) != ALLOWED:
        raise ValueError("Unexpected or missing file")
    for name, item in files.items():
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or "\\" in name:
            raise ValueError("Unsafe path")
        content = item["text"]
        if not isinstance(content, str) or len(content.encode("utf-8")) > 200000:
            raise ValueError("Invalid file content")
        if hashlib.sha256(content.encode("utf-8")).hexdigest() != item["sha256"]:
            raise ValueError("Checksum mismatch: " + name)
    if not files["SKILL.md"]["text"].startswith("---\nname: " + NAME + "\n"):
        raise ValueError("Skill identity mismatch")
    return bundle


def is_bytecode(path, root):
    return path.suffix == ".pyc" or "__pycache__" in path.relative_to(root).parts


def matches(target, files):
    if any(p.is_symlink() and not is_bytecode(p, target) for p in target.rglob("*")):
        return False
    actual = {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file() and not is_bytecode(p, target)}
    if actual != set(files):
        return False
    return all(not (target / n).is_symlink() and
               (target / n).read_bytes() == item["text"].encode("utf-8")
               for n, item in files.items())


def load_installed_doctor(skill_dir):
    path = skill_dir / "scripts" / "doctor.py"
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location("jason_skill_doctor", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.dont_write_bytecode = previous


def assess_required_tools(skill_dir):
    doctor = load_installed_doctor(skill_dir)
    report = doctor.inspect()
    return {
        "platform": report["platform"],
        "architecture": report["architecture"],
        "architecture_note": report["architecture_note"],
        "official_tools_supported": report["official_tools_supported"],
        "required_tools": report["required_tools"],
        "required_tools_complete": report["required_tools_complete"],
        "states": report["states"],
        "next_steps": report["next_steps"],
        "warnings": report["warnings"],
    }


def configure_required_tools(skill_dir, include_cua=False):
    script = skill_dir / "scripts" / "setup_all.py"
    command = [sys.executable, str(script), "--apply", "--browser-runtime"]
    if include_cua:
        command.append("--include-cua")
    completed = subprocess.run(command, capture_output=True, text=True, timeout=900)
    payload = None
    text = completed.stdout.strip()
    if text:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {"raw_stdout": text}
    return {
        "returncode": completed.returncode,
        "setup": payload,
        "stderr": completed.stderr.strip() or None,
    }


def skill_status(files_matched, tools_complete, replaced=False, backup=None):
    if files_matched and tools_complete:
        status = "already-installed" if not replaced else "installed"
    elif files_matched:
        status = "already-installed-required-tools-incomplete" if not replaced else "skill-installed-required-tools-incomplete"
    else:
        status = "installed" if tools_complete else "skill-installed-required-tools-incomplete"
    return status


def install(bundle_path, root=None, replace=False, with_required_tools=False, include_cua=False):
    bundle = load_bundle(bundle_path)
    # Current documented Codex user skill directory. No global config edits.
    root = Path(root).expanduser() if root is not None else Path.home() / ".agents/skills"
    root = root.resolve()
    target = root / NAME
    root.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        raise ValueError("Target is a symlink; inspect it manually")
    files_already_matched = False
    backup = None
    if target.exists():
        if not target.is_dir():
            raise ValueError("Target is not a directory")
        if matches(target, bundle["files"]):
            files_already_matched = True
        elif not replace:
            raise FileExistsError("Existing skill differs; review it before --replace")
    if not files_already_matched:
        staging = Path(tempfile.mkdtemp(prefix=".desktop-control-stage-", dir=root.parent))
        try:
            for name, item in bundle["files"].items():
                path = staging / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(item["text"].encode("utf-8"))
                path.chmod(0o644)
            if target.exists():
                backup_root = root.parent / "skill-backups"
                backup_root.mkdir(parents=True, exist_ok=True)
                stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                backup = backup_root / (NAME + "-" + stamp)
                os.rename(target, backup)
            try:
                os.rename(staging, target)
            except BaseException:
                if backup is not None:
                    os.rename(backup, target)
                raise
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    tool_setup = None
    if with_required_tools:
        tool_setup = configure_required_tools(target, include_cua=include_cua)
    assessment = assess_required_tools(target)
    complete = assessment["required_tools_complete"]
    status = skill_status(files_already_matched, complete, replaced=bool(backup), backup=backup)
    result = {
        "status": status,
        "path": str(target),
        "backup": str(backup) if backup else None,
        "version": bundle.get("version", VERSION),
        "skill_files_installed": True,
        "required_tools_complete": complete,
        "install_complete": complete,
        "drivers_installed": complete,
        "global_config_changed": False,
        "required_tools": assessment["required_tools"],
        "states": assessment["states"],
        "next_steps": assessment["next_steps"],
        "architecture_note": assessment["architecture_note"],
        "official_tools_supported": assessment["official_tools_supported"],
        "tool_setup": tool_setup,
        "optional_cua": "not-requested" if not include_cua else "requested",
    }
    if not complete:
        result["incomplete_reason"] = (
            "Skill files are installed, but installation is incomplete until required tools "
            "(agent-desktop and agent-browser) are installed on macOS or Windows. "
            "Cua remains optional. Re-run with --with-required-tools, or run scripts/setup_all.py --apply --browser-runtime."
        )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--skills-root", type=Path)
    parser.add_argument("--replace", action="store_true")
    parser.add_argument(
        "--with-required-tools", action="store_true",
        help="After installing skill files, install required agent-desktop and agent-browser tools")
    parser.add_argument(
        "--include-cua", action="store_true",
        help="Also configure optional official Cua; only used with --with-required-tools")
    args = parser.parse_args()
    result = install(
        args.bundle, args.skills_root, args.replace,
        with_required_tools=args.with_required_tools, include_cua=args.include_cua)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("install_complete") else 2


if __name__ == "__main__":
    sys.exit(main())
