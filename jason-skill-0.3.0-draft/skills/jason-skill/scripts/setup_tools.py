"""Preview or install pinned official native browser and desktop tools."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from urllib.request import Request, urlopen

from doctor import mac_arch, windows_arch, windows_build


ROOT = Path.home() / ".local/share/jason-skill/tools"
VERSIONS = {"agent-browser": "0.43.0", "agent-desktop": "1.3.1"}
ASSETS = {
    ("Darwin", "x86_64"): {
        "agent-browser": ("agent-browser-darwin-x64",
                          "49a5ab27297213c1bc0005701a6a4542399abfc9d2cb7520ab519ebb94b8b13d"),
        "agent-desktop": ("agent-desktop-v1.3.1-x86_64-apple-darwin.tar.gz",
                          "469da10cfb68928c58caff88b92b30526e0ca895ac06bc86b7f533b1d9b309b3"),
    },
    ("Darwin", "arm64"): {
        "agent-browser": ("agent-browser-darwin-arm64",
                          "05338a8eeddf0b3f9ebf0c87a6c21aedc10685608c68618e1a8483c43eae9c3f"),
        "agent-desktop": ("agent-desktop-v1.3.1-aarch64-apple-darwin.tar.gz",
                          "9b7b7cfc74892eab46c2c85d6cb7dc4863bf8dab0a222cfcfb8ae4604c69c86c"),
    },
    ("Windows", "x86_64"): {
        "agent-browser": ("agent-browser-win32-x64.exe",
                          "ebcef5ebea93c7ccf0fe3f8c18eee908ae9174dfef8e52a3dda6f24a59f630dc"),
        "agent-desktop": ("agent-desktop-v1.3.1-x86_64-pc-windows-msvc.tar.gz",
                          "6ee4b1e078f4e78792e79f16e32e4a78b9919464aa3c55629b7e27ed53a08c13"),
    },
    ("Windows", "arm64"): {
        "agent-desktop": ("agent-desktop-v1.3.1-aarch64-pc-windows-msvc.tar.gz",
                          "805f1f61890f9983fceaf38cda94a37a049c379435d65607db5cedd22c8ef97b"),
    },
}
LIMIT = 32 * 1024 * 1024


def platform_key():
    system = platform.system()
    if system == "Darwin":
        return system, mac_arch()
    if system == "Windows":
        return system, windows_arch()
    machine = platform.machine().lower()
    return system, {"amd64": "x86_64", "aarch64": "arm64"}.get(machine, machine)


def download_checked(url, expected_sha, output, max_bytes=LIMIT):
    digest = hashlib.sha256()
    total = 0
    request = Request(url, headers={"User-Agent": "jason-skill-installer"})
    with urlopen(request, timeout=30) as response, output.open("xb") as file:
        while True:
            chunk = response.read(256 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ValueError("Release asset is larger than expected")
            digest.update(chunk)
            file.write(chunk)
    if digest.hexdigest() != expected_sha:
        raise ValueError("Release SHA-256 mismatch")


def unpack(archive, staged, names):
    with tarfile.open(archive, "r:gz") as tar:
        members = tar.getmembers()
        if (sorted(m.name for m in members) != sorted(names)
                or any(not m.isfile() or not 0 < m.size <= LIMIT for m in members)):
            raise ValueError("Unexpected desktop archive contents")
        for member in members:
            with tar.extractfile(member) as source, (staged / member.name).open("xb") as dest:
                shutil.copyfileobj(source, dest)


def plan_tool(tool, root, key, force_pinned=False, win_build=None):
    system, architecture = key
    version = VERSIONS[tool]
    program = tool + (".exe" if system == "Windows" else "")
    target = root / tool / version / program
    existing = shutil.which(tool)
    if target.is_file() and not target.is_symlink():
        return {"tool": tool, "status": "found-not-GUI-verified", "command": str(target)}
    if existing and not force_pinned:
        return {"tool": tool, "status": "found-not-GUI-verified", "command": str(existing)}
    asset = ASSETS.get(key, {}).get(tool)
    emulated = False
    if key == ("Windows", "arm64") and tool == "agent-browser":
        build = windows_build() if win_build is None else win_build
        if build >= 22000:
            asset = ASSETS[("Windows", "x86_64")][tool]
            emulated = True
    if not asset:
        return {"tool": tool, "status": "use-host-tool-or-upstream-guide",
                "platform": system, "architecture": architecture,
                "upstream": "https://github.com/vercel-labs/" + tool}
    filename, checksum = asset
    return {"tool": tool, "status": "planned", "command": str(target), "version": version,
            "url": f"https://github.com/vercel-labs/{tool}/releases/download/v{version}/{filename}",
            "sha256": checksum, "binary_route": "windows-x64-emulation" if emulated else "native"}


def install_tool(item, system):
    executable = Path(item["command"])
    destination = executable.parent
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("Version directory already exists. Inspect and reuse it.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".jason-tool-", dir=destination.parent) as temporary:
        stage = Path(temporary)
        asset = stage / "download"
        download_checked(item["url"], item["sha256"], asset)
        payload = stage / "payload"
        payload.mkdir()
        if item["tool"] == "agent-desktop":
            names = [executable.name]
            if system == "Darwin":
                names.append("agent-desktop-macos-helper")
            unpack(asset, payload, names)
        else:
            asset.rename(payload / executable.name)
        for path in payload.iterdir():
            path.chmod(0o755)
        probe = subprocess.run([str(payload / executable.name), "--version"],
                               text=True, capture_output=True, timeout=15, check=True)
        if not re.search(r"(?<![\d.])" + re.escape(item["version"]) + r"(?![\d.])", probe.stdout):
            raise ValueError("Unexpected binary version")
        # Reserve the destination; never replace an existing version or symlink.
        destination.mkdir()
        try:
            for path in payload.iterdir():
                path.rename(destination / path.name)
        except OSError:
            shutil.rmtree(destination)
            raise
    return {**item, "status": "installed-binary-version-verified", "version_output": probe.stdout.strip()}


def resolve_tools(root, key, tools, force_pinned=False, apply=False):
    items = [plan_tool(tool, root, key, force_pinned) for tool in tools]
    for index, item in enumerate(items):
        if apply and item["status"] == "planned":
            try:
                items[index] = install_tool(item, key[0])
            except (OSError, ValueError, subprocess.SubprocessError, tarfile.TarError) as error:
                items[index] = {**item, "status": "failed", "error": str(error)}
    return items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Download; default is a read-only preview")
    parser.add_argument("--tool", choices=[*VERSIONS, "all"], default="all")
    parser.add_argument("--tool-root", type=Path, default=ROOT)
    parser.add_argument("--pinned", action="store_true", help="Plan the pinned versions even if a command is on PATH")
    args = parser.parse_args()
    key = platform_key()
    tools = list(VERSIONS) if args.tool == "all" else [args.tool]
    items = resolve_tools(args.tool_root.expanduser().absolute(), key, tools, args.pinned, args.apply)
    print(json.dumps({"platform": key, "tools": items, "gui_verified": False,
                      "browser_runtime": "Reuse an existing supported browser or run agent-browser install separately."},
                     ensure_ascii=False, indent=2))
    return 1 if any(item["status"] == "failed" for item in items) else 0


if __name__ == "__main__":
    sys.exit(main())
