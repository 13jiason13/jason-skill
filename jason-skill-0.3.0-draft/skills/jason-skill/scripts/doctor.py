"""Portable, read-only environment report. No credentials or application data."""
import ctypes
import json
import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_TOOLS = ("agent-desktop", "agent-browser")


def required_tool_install_command():
    """Ready-to-run command that installs agent-desktop and agent-browser."""
    setup = Path(__file__).resolve().parent / "setup_all.py"
    parts = [sys.executable, str(setup), "--apply", "--browser-runtime"]
    if platform.system() == "Windows":
        return subprocess.list2cmdline(parts)
    return shlex.join(parts)


def mac_arch(machine=None, arm_capable=None):
    machine = machine or platform.machine()
    if arm_capable is None and platform.system() == "Darwin":
        try:
            arm_capable = subprocess.check_output(
                ["/usr/sbin/sysctl", "-n", "hw.optional.arm64"],
                stderr=subprocess.DEVNULL, timeout=3).decode().strip() == "1"
        except (OSError, subprocess.SubprocessError):
            arm_capable = machine == "arm64"
    return "arm64" if machine == "arm64" or arm_capable else "x86_64"


def windows_arch():
    # Use the native machine even if Python itself is running under Windows emulation.
    try:
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        from ctypes import wintypes
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        kernel.IsWow64Process2.argtypes = [
            wintypes.HANDLE, ctypes.POINTER(ctypes.c_ushort), ctypes.POINTER(ctypes.c_ushort)
        ]
        kernel.IsWow64Process2.restype = wintypes.BOOL
        process = ctypes.c_ushort()
        native = ctypes.c_ushort()
        if kernel.IsWow64Process2(kernel.GetCurrentProcess(), ctypes.byref(process), ctypes.byref(native)):
            return {0xAA64: "arm64", 0x8664: "x86_64", 0x014C: "x86"}.get(
                native.value, platform.machine().lower())
    except (AttributeError, OSError):
        pass
    machine = platform.machine().lower()
    return {"amd64": "x86_64", "aarch64": "arm64"}.get(machine, machine)


def windows_build():
    try:
        info = sys.getwindowsversion()
        return getattr(info, "platform_version", (0, 0, info.build))[2]
    except (AttributeError, IndexError):
        return 0


def official_tools_supported(system=None):
    return (system or platform.system()) in ("Darwin", "Windows")


def managed_tool_path(name, system=None):
    system = system or platform.system()
    suffix = ".exe" if system == "Windows" else ""
    root = Path.home() / ".local/share/jason-skill/tools" / name
    matches = [
        path for path in root.glob("*/" + name + suffix)
        if path.is_file() and not path.is_symlink()
    ]
    return str(matches[0]) if matches else None


def tool_command(name, system=None):
    system = system or platform.system()
    managed = managed_tool_path(name, system)
    if managed:
        return managed
    found = shutil.which(name)
    if found:
        return found
    if system == "Windows":
        return shutil.which(name + ".exe")
    return None


def platform_guidance(system, architecture, win_build=None, required_tools_complete=False):
    if system == "Darwin":
        permissions = {
            "status": "recipient-must-grant",
            "macos": ["Accessibility", "Screen Recording"],
            "how": "Grant these in System Settings > Privacy & Security. Scripts do not edit TCC databases.",
        }
        arch_note = (
            "This Mac uses the official native arm64 assets."
            if architecture == "arm64"
            else "This Mac uses the official native x86_64 assets."
        )
        if required_tools_complete:
            next_steps = [
                "Grant Accessibility and Screen Recording in System Settings > Privacy & Security.",
                "Connect agent-desktop and agent-browser through the host-supported configuration path, then reload if required.",
                "Run scripts/accept.py --all with the macOS form in acceptance/macos/MacForm.swift and the local browser fixture.",
                "Optional: add --include-cua only if you want the official Cua Driver.",
            ]
        else:
            next_steps = [
                "Installation is incomplete until the required tools are installed: agent-desktop and agent-browser. Attaching or registering skill files only is incomplete.",
                "Run this command to install the required tools: " + required_tool_install_command(),
                arch_note,
                "Then grant Accessibility and Screen Recording, connect the tools, and run scripts/accept.py --all. Cua remains optional (--include-cua).",
            ]
        return permissions, next_steps, arch_note
    if system == "Windows":
        permissions = {
            "status": "recipient-must-grant",
            "windows": ["Interactive signed-in desktop session"],
            "how": (
                "Use the signed-in interactive desktop. Do not run desktop acceptance from a locked "
                "or disconnected session. Follow Microsoft Defender and organizational policy. "
                "Scripts do not change execution policy, elevation, PATH, or MCP configuration."
            ),
        }
        if architecture == "arm64" and (win_build or 0) >= 22000:
            arch_note = (
                "Windows 11 ARM: agent-desktop uses the official native ARM64 asset; "
                "agent-browser uses the pinned official Windows x64 asset through OS emulation "
                "and needs a separate runtime and page test."
            )
        elif architecture == "arm64":
            arch_note = (
                "Windows 10 ARM: a native official agent-desktop asset is available; "
                "there is no pinned official agent-browser asset. The required browser tool "
                "cannot be completed from this installer."
            )
        elif architecture == "x86_64":
            arch_note = "Windows x64 uses official native agent-desktop and agent-browser assets."
        else:
            arch_note = "This Windows architecture has no pinned official required-tool assets."
        if required_tools_complete:
            next_steps = [
                "Continue from the signed-in interactive desktop. Use py -3 where needed.",
                "Connect agent-desktop and agent-browser through the host-supported configuration path, then reload if required.",
                "Run scripts/accept.py --all with the Windows form in acceptance/windows/WindowsForm.ps1 and the local browser fixture.",
                "Optional: add --include-cua only if you want the official Cua Driver.",
            ]
        else:
            next_steps = [
                "Installation is incomplete until the required tools are installed: agent-desktop and agent-browser. Attaching or registering skill files only is incomplete.",
                "Run this command to install the required tools: " + required_tool_install_command(),
                arch_note,
                "Then continue from the signed-in interactive desktop, connect the tools, and run scripts/accept.py --all. Cua remains optional (--include-cua).",
            ]
        return permissions, next_steps, arch_note
    permissions = {
        "status": "official-tools-unavailable",
        "linux_or_other": "Official agent-desktop and agent-browser releases are not provided for this OS.",
        "how": "File-route acceptance can still run. Browser and desktop routes require macOS or Windows.",
    }
    arch_note = "Official required tools are unavailable on Linux and other non-macOS, non-Windows systems."
    next_steps = [
        "Official agent-desktop and agent-browser assets are not available on this OS, so a complete Jason Skill install cannot be finished here.",
        "You can still run scripts/accept.py --files for the local file-organization check.",
        "To install the required browser and desktop tools, use a Mac or a Windows PC.",
    ]
    return permissions, next_steps, arch_note


def inspect():
    system = platform.system()
    version = platform.mac_ver()[0] if system == "Darwin" else platform.release()
    architecture = {
        "Darwin": mac_arch, "Windows": windows_arch
    }.get(system, platform.machine)()
    win_build = windows_build() if system == "Windows" else None
    warnings = []
    if system == "Darwin" and version.startswith("14."):
        warnings.append(
            "Cua Driver 0.55.0 background-input crash was observed on one Intel Sonoma host. "
            "Prefer callable official Computer Use for writes until this host passes a synthetic "
            "write/save test. Reinstall alone is not proof of repair."
        )
    if system == "Windows" and architecture == "arm64" and (win_build or 0) < 22000:
        warnings.append(
            "Windows 10 ARM has no pinned official agent-browser asset, so the required browser "
            "tool cannot be completed from this installer."
        )
    if not official_tools_supported(system):
        warnings.append(
            "Official agent-desktop and agent-browser releases are unavailable on this OS. "
            "Installation of the required tools cannot be completed here."
        )
    paths = (Path("/Applications/CuaDriver.app"), Path.home() / "Applications/CuaDriver.app")
    required = {}
    for name in REQUIRED_TOOLS:
        command = tool_command(name, system)
        required[name] = {
            "installed": bool(command),
            "command": command,
            "managed": bool(managed_tool_path(name, system)),
            "required": True,
        }
    required_tools_complete = official_tools_supported(system) and all(
        item["installed"] for item in required.values()
    )
    permissions, next_steps, arch_note = platform_guidance(
        system, architecture, win_build, required_tools_complete
    )
    next_command = None
    if official_tools_supported(system) and not required_tools_complete:
        next_command = required_tool_install_command()
    cua_command = tool_command("cua-driver", system)
    return {
        "platform": system,
        "os_version": version,
        "architecture": architecture,
        "windows_build": win_build,
        "python_supported": sys.version_info >= (3, 8),
        "official_tools_supported": official_tools_supported(system),
        "architecture_note": arch_note,
        "commands": {name: bool(shutil.which(name)) for name in ("python3", "agent-desktop", "agent-browser", "cua-driver")},
        "managed_tools": {
            name: bool(managed_tool_path(name, system)) for name in ("agent-desktop", "agent-browser")
        },
        "required_tools": required,
        "optional_cua": {
            "required": False,
            "installed": bool(cua_command) or any(path.is_dir() for path in paths),
            "command": cua_command,
            "cua_app_installed": any(path.is_dir() for path in paths),
        },
        "cua_app_installed": any(path.is_dir() for path in paths),
        "builtin_computer_use": "Host must check currently callable tools and run an owned-window test; no separate API key is implied.",
        "states": {
            "installed": required_tools_complete,
            "connected": "host-must-confirm",
            "permissions_granted": permissions,
            "acceptance_passed": False,
        },
        "required_tools_complete": required_tools_complete,
        "install_complete": required_tools_complete,
        "gui_verified": False,
        "warnings": warnings,
        "next_command": next_command,
        "next_steps": next_steps,
        "note": (
            "No username, home path, account, file listing, browser state, network state or telemetry is collected. "
            "Presence is not runtime success. Installation, connection, permission, and acceptance are reported separately. "
            "Installation is incomplete until required tools (agent-desktop and agent-browser) are installed on macOS or Windows."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(inspect(), ensure_ascii=False, indent=2))
