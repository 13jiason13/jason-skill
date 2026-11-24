"""Optional pinned Windows Cua Driver setup. No PATH, elevation, or autostart edits."""
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import tempfile
import zipfile

from setup_tools import download_checked

VERSION = "0.55.0"
BASE = "https://github.com/trycua/cua/releases/download/cua-driver-rs-v" + VERSION + "/"
CHECKSUMS = {
    "arm64": "ab1515f8893fb8b1acda5a4ffe1d2e97d19a938460d0f5ac7b6e9ed88f37f020",
    "x86_64": "357b93254183c0e24a501eb9ad3a6e0f3738a67bfed55c0c292959b540d9b4a7",
}
EXE = "cua-driver.exe"


def plan(arch, target, pinned=False):
    managed = target / EXE
    for existing in (managed, Path(shutil.which("cua-driver") or EXE)):
        if existing.is_absolute() and existing.is_file() and not existing.is_symlink():
            if existing == managed or not pinned:
                return {"status": "existing-needs-runtime-test", "command": str(existing)}
    checksum = CHECKSUMS.get(arch)
    if checksum is None:
        return {"status": "use-host-or-upstream", "reason": "No pinned native Windows Cua asset"}
    filename = f"cua-driver-rs-{VERSION}-windows-{arch}-binary.zip"
    return {"status": "planned", "command": str(managed), "url": BASE + filename, "sha256": checksum,
            "version": VERSION}


def extract_executable(archive, target):
    with zipfile.ZipFile(archive) as package:
        matches = []
        for item in package.infolist():
            path = PurePosixPath(item.filename)
            if (path.is_absolute() or ".." in path.parts or ":" in item.filename or "\\" in item.filename
                    or stat.S_ISLNK(item.external_attr >> 16)):
                raise ValueError("Unsafe Windows Cua archive entry")
            if not item.is_dir() and path.name.lower() == EXE:
                matches.append(item)
        if len(matches) != 1 or not 0 < matches[0].file_size <= 160 * 1024 * 1024:
            raise ValueError("Expected one bounded cua-driver.exe")
        with package.open(matches[0]) as source, target.open("xb") as output:
            shutil.copyfileobj(source, output)


def install(item):
    executable = Path(item["command"])
    target = executable.parent
    if target.exists() or target.is_symlink():
        raise FileExistsError("Windows Cua directory already exists; inspect before reusing")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".jason-cua-", dir=target.parent) as directory:
        staging = Path(directory)
        archive = staging / "release.zip"
        binary = staging / EXE
        download_checked(item["url"], item["sha256"], archive, max_bytes=64 * 1024 * 1024)
        extract_executable(archive, binary)
        probe = subprocess.run([str(binary), "--version"], capture_output=True, text=True,
                               check=True, timeout=20)
        if VERSION not in probe.stdout.split():
            raise ValueError("Unexpected Windows Cua Driver version")
        target.mkdir()
        try:
            binary.rename(executable)
        except OSError:
            target.rmdir()
            raise
    return {**item, "status": "installed-binary-version-verified",
            "mcp_fragment": {"mcpServers": {"cua-driver": {
                "command": str(executable), "args": ["mcp"],
                "env": {"DO_NOT_TRACK": "1", "CUA_TELEMETRY": "0"}}}},
            "next": "Use the logged-in interactive Windows session, run cua-driver doctor, and verify the test form."}
