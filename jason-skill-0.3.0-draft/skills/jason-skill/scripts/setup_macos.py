"""Install the pinned, signed official Cua app. Preview by default; no TCC/MCP edits."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import subprocess
import tarfile
import tempfile
from doctor import mac_arch
from setup_tools import download_checked

VERSION = '0.55.0'
TEAM = 'YCK386LBJ7'
BASE = 'https://github.com/trycua/cua/releases/download/cua-driver-rs-v' + VERSION + '/'
CHECKSUMS = {
    'arm64': '2749dfbc95d5735fd848926725bb8dae137a3526c239e1ef2cd7ae0767956878',
    'x86_64': '163cea6a71b369e7366e765e0c9b9c97ad3d07ebf9dec3f10590e9840cddbd38',
}


def asset_for(arch):
    if arch not in ('arm64', 'x86_64'):
        raise ValueError('Unsupported architecture')
    return 'cua-driver-rs-' + VERSION + '-darwin-' + arch + '.tar.gz'


def extract_checked(archive, destination):
    with tarfile.open(archive, 'r:gz') as handle:
        members = handle.getmembers()
        if sum(m.size for m in members) > 700 * 1024 * 1024:
            raise ValueError('Archive exceeds expected size')
        for member in members:
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or '..' in relative.parts or '\\' in member.name or not (member.isdir() or member.isfile()):
                raise ValueError('Unsafe archive member')
        handle.extractall(destination, members=members)


def verify_app(app):
    subprocess.run(['/usr/bin/codesign', '--verify', '--deep', '--strict', str(app)], check=True, capture_output=True, timeout=30)
    details = subprocess.run(['/usr/bin/codesign', '-dv', '--verbose=2', str(app)], check=True, capture_output=True, text=True, timeout=10)
    if 'TeamIdentifier=' + TEAM not in details.stderr:
        raise ValueError('Unexpected signing team')
    subprocess.run(['/usr/sbin/spctl', '--assess', '--type', 'execute', str(app)], check=True, capture_output=True, timeout=60)


def install(arch, target):
    if target.exists() or target.is_symlink():
        raise FileExistsError('App already exists; inspect it and reuse it or make a deliberate backup before replacing. Nothing was overwritten.')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='jason-signed-cua-') as temp:
        temp = Path(temp)
        asset = asset_for(arch)
        archive = temp / asset
        download_checked(BASE + asset, CHECKSUMS[arch], archive, max_bytes=100 * 1024 * 1024)
        extract_checked(archive, temp/'expanded')
        source = temp/'expanded'/('cua-driver-rs-' + VERSION + '-darwin-' + arch)/'CuaDriver.app'
        verify_app(source)
        # Stage on the destination filesystem, then commit without overwriting.
        staging = Path(tempfile.mkdtemp(prefix='.jason-cua-stage-', dir=str(target.parent)))
        try:
            shutil.copytree(source, staging/'CuaDriver.app')
            verify_app(staging/'CuaDriver.app')
            if target.exists() or target.is_symlink():
                raise FileExistsError('Target appeared during setup')
            os.rename(str(staging/'CuaDriver.app'), str(target))
        finally:
            shutil.rmtree(str(staging), ignore_errors=True)
    command = str(target/'Contents/MacOS/cua-driver')
    return {'status': 'app-installed-not-yet-GUI-verified', 'version': VERSION,
            'permission_command': [command, 'permissions', 'grant'],
            'mcp_fragment': {'mcpServers': {'cua-driver': {'command': command, 'args': ['mcp'], 'env': {'DO_NOT_TRACK': '1', 'CUA_TELEMETRY': '0'}}}},
            'changed_privacy_permissions': False, 'changed_mcp_config': False,
            'next': 'Grant permissions through the signed app. Add the returned MCP fragment through the host-supported configuration path, reload the connection, and verify synthetic read/click/input/save. Do not use --direct as the default standalone installation.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--target', type=Path)
    args = parser.parse_args()
    if platform.system() != 'Darwin':
        raise SystemExit('This dependency helper is for macOS. The Skill itself can use other host-supported routes.')
    arch = mac_arch()
    target = (args.target or Path.home()/'Applications/CuaDriver.app').expanduser()
    if args.apply:
        print(json.dumps(install(arch, target), ensure_ascii=False, indent=2))
    else:
        print(json.dumps({'mode': 'preview', 'version': VERSION, 'architecture': arch,
                          'download': BASE + asset_for(arch), 'target': str(target),
                          'verification': 'SHA256, Apple codesign, pinned Developer ID team and Gatekeeper assessment',
                          'changes': 'One signed app only. No shell profiles, PATH, permissions, network or MCP settings are changed.',
                          'apply': 'Run again with --apply after reviewing; user-requested dependency setup supplies installation intent.'}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
