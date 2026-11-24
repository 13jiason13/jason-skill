"""One entry to preview or configure Jason Skill's required and optional tools."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import zipfile

import doctor
import setup_macos
import setup_tools
import setup_windows


CLI_READY = {"found-not-GUI-verified", "installed-binary-version-verified"}
REQUIRED_TOOLS = ("agent-desktop", "agent-browser")


def required_tools_complete(cli, system):
    if system not in ("Darwin", "Windows"):
        return False
    by_tool = {item["tool"]: item for item in cli}
    return all(by_tool.get(name, {}).get("status") in CLI_READY for name in REQUIRED_TOOLS)


def run_setup(args):
    system, arch = key = setup_tools.platform_key()
    cli = setup_tools.resolve_tools(
        args.tool_root.expanduser().absolute(), key,
        list(setup_tools.VERSIONS), args.pinned, args.apply)
    win_build = doctor.windows_build() if system == "Windows" else None
    permissions, next_steps, arch_note = doctor.platform_guidance(
        system, arch, win_build, required_tools_complete(cli, system))
    result = {
        "mode": "applied" if args.apply else "preview",
        "platform": system,
        "architecture": arch,
        "architecture_note": arch_note,
        "required_tools": list(REQUIRED_TOOLS),
        "optional_tools": ["cua"],
        "toolchain": cli,
        "browser_runtime": {"status": "reuse-or-configure-if-needed"},
        "cua": {"status": "optional-not-requested"},
        "gui_verified": False,
        "official_tools_supported": doctor.official_tools_supported(system),
        "states": {
            "installed": required_tools_complete(cli, system),
            "connected": "host-must-confirm",
            "permissions_granted": permissions,
            "acceptance_passed": False,
        },
        "next_steps": next_steps,
    }
    if system not in ("Darwin", "Windows"):
        result["official_tools"] = "unavailable"
        result["note"] = (
            "Official agent-desktop and agent-browser assets are not available on this OS. "
            "Required-tool installation cannot be completed here. Cua is also not installed by this helper."
        )
    browser = next(item for item in cli if item["tool"] == "agent-browser")
    if args.browser_runtime:
        if not args.apply:
            result["browser_runtime"] = {"status": "planned", "source": "agent-browser install"}
        elif browser["status"] in CLI_READY:
            try:
                subprocess.run([browser["command"], "install"], capture_output=True,
                               timeout=420, check=True)
                result["browser_runtime"] = {"status": "installed-needs-browser-test"}
            except (OSError, subprocess.SubprocessError) as error:
                result["browser_runtime"] = {"status": "failed", "error": str(error)}
        else:
            result["browser_runtime"] = {"status": "failed", "error": "agent-browser unavailable"}
    if args.include_cua:
        try:
            result["cua"] = configure_cua(args, system, arch)
        except (OSError, ValueError, subprocess.SubprocessError, tarfile.TarError, zipfile.BadZipFile) as error:
            result["cua"] = {"status": "failed", "error": str(error)}
    result["required_tools_complete"] = required_tools_complete(cli, system)
    result["install_complete"] = result["required_tools_complete"]
    result["states"]["installed"] = result["required_tools_complete"]
    if not result["install_complete"]:
        result["incomplete_reason"] = (
            "Installation is incomplete until required tools are installed: agent-desktop and agent-browser."
        )
    return result


def configure_cua(args, system, arch):
    if system == "Windows":
        target = args.cua_target or args.tool_root / "cua-driver" / setup_windows.VERSION
        item = setup_windows.plan(arch, target.expanduser().absolute(), args.pinned)
        if args.apply and item["status"] == "planned":
            return setup_windows.install(item)
        return item
    if system != "Darwin":
        return {"status": "use-host-or-upstream", "reason": "This helper supports macOS and Windows"}
    target = (args.cua_target or Path.home() / "Applications/CuaDriver.app").expanduser().absolute()
    if target.is_symlink():
        return {"status": "inspect-existing", "target": str(target)}
    if target.is_dir():
        return {"status": "existing-needs-runtime-test", "target": str(target)}
    if not args.apply:
        return {"status": "planned", "version": setup_macos.VERSION, "target": str(target)}
    return setup_macos.install(arch, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--browser-runtime", action="store_true", help="Run upstream Chrome for Testing setup")
    parser.add_argument("--include-cua", action="store_true", help="Optionally set up official Cua on macOS or Windows")
    parser.add_argument("--pinned", action="store_true")
    parser.add_argument("--tool-root", type=Path, default=setup_tools.ROOT)
    parser.add_argument("--cua-target", type=Path)
    args = parser.parse_args()
    result = run_setup(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    statuses = [*result["toolchain"], result["browser_runtime"], result["cua"]]
    if any(item.get("status") == "failed" for item in statuses):
        return 1
    if args.apply and not result.get("install_complete"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
