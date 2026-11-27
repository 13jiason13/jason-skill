# Portable setup

Installation has three steps and is incomplete until the required tools are installed:

1. Install the skill files.
2. Install required tools: **agent-desktop** and **agent-browser**. Cua is optional.
3. Run the acceptance pack.

macOS and Windows are separate paths. Official required tools are not available on Linux. Report installed, connected, permissions granted, and acceptance passed as four separate states.

## 1. Install the skill and the required tools

Downloading or cloning the repository does not run the installer. Verify the installer SHA-256 against `SHA256SUMS.txt` before use. Inspect an existing same-name installation before updating it. Preserve the backup and use the host's established skill directory. Python 3.8 or later is required.

Attaching or registering skill files only is incomplete. The default command installs the skill files and the required tools (agent-desktop and agent-browser, SHA-256 checked), then you run acceptance:

```sh
python3 tools/install_bundle.py dist/Jason-Skill-0.3.0-draft-install.txt --with-required-tools
python3 ~/.agents/skills/jason-skill/scripts/doctor.py
python3 ~/.agents/skills/jason-skill/scripts/accept.py --all
```

On Windows, use `py -3` instead of `python3` when needed. The default skill directory is `~/.agents/skills/jason-skill`; an existing installation can use `--skills-root`. `--with-required-tools` is the default written out explicitly: omitting the flag also installs agent-desktop and agent-browser. `--skill-files-only` is the offline skill-files-only opt-out. It does not fetch those tools. Without them, the status stays `skill-installed-required-tools-incomplete` and the process exits 2.

If `doctor.py` reports required tools missing, run the `next_command` it prints (`scripts/setup_all.py --apply --browser-runtime`). Do not continue with only host Windows automation or host Chrome.

Add `--include-cua` only when the recipient wants the optional official Cua Driver.

## 2. Install required tools

Reuse a connected host tool when it is already present. Otherwise preview, then apply, the required official assets. Downloads use pinned official URLs and SHA-256 checks.

```sh
python3 ~/.agents/skills/jason-skill/scripts/doctor.py
python3 ~/.agents/skills/jason-skill/scripts/setup_all.py
python3 ~/.agents/skills/jason-skill/scripts/setup_all.py --apply --browser-runtime
```

`--browser-runtime` runs agent-browser's own official Chrome for Testing installer so the browser route can be accepted. `--pinned` installs the distribution's pinned versions in dedicated user directories while preserving existing programs. The report returns full executable paths. Scripts do not edit TCC databases, global MCP configuration, global PATH, proxies, or network settings.

### macOS

The installer selects official native assets for this Mac:

- Apple Silicon (arm64): official `agent-browser` Darwin arm64 and `agent-desktop` aarch64-apple-darwin assets
- Intel (x86_64): official `agent-browser` Darwin x64 and `agent-desktop` x86_64-apple-darwin assets
- A Rosetta-capable Intel-reported host that is arm64-capable is treated as arm64

After the binaries are installed, the recipient grants **Accessibility** and **Screen Recording** in System Settings > Privacy & Security. Scripts cannot click those dialogs and do not edit TCC. Connect the returned command paths through the host's supported configuration path, then reload if required.

Optional Cua uses `setup_macos.py`. It verifies the official archive, SHA-256, Apple signature, the expected developer team, and Gatekeeper assessment, then installs the signed app. A present Cua app is not an accepted Cua route until a synthetic write/save test passes. On some Intel macOS 14 hosts, official Cua 0.55.0 background input has a known issue; see the skill warnings.

### Windows

Use `py -3` where needed. Required-tool install and desktop acceptance must run from the **signed-in interactive desktop**. Do not use a locked or disconnected session. Follow Microsoft Defender and organizational policy.

The installer selects assets by native machine architecture, even if Python is running under emulation:

- Windows x64: official native `agent-desktop` and `agent-browser` assets
- Windows 11 ARM (build 22000 or later): official native ARM64 `agent-desktop`; official Windows x64 `agent-browser` through OS emulation, subject to a separate runtime and page test
- Windows 10 ARM: official native ARM64 `agent-desktop` is available; there is no pinned official `agent-browser` asset, so the required browser tool cannot be completed from this installer
- Other Windows architectures: no pinned official required-tool assets

Optional Cua uses `setup_windows.py` and installs a pinned official `cua-driver.exe`. Run `cua-driver doctor` from the interactive session and verify the Windows test form before treating Cua as accepted.

### Linux and other systems

Official agent-desktop and agent-browser releases are not available. Skill files and the file-organization check can still be installed and run. Browser and desktop routes, and a complete required-tool install, need a Mac or a Windows PC.

## 3. Run acceptance

Use synthetic data and owned test windows only:

```sh
python3 ~/.agents/skills/jason-skill/scripts/accept.py --all
```

- Files: create `parity.txt` containing `Jason parity`, move it to `done/`, and verify the source is gone and the destination matches.
- Browser: open `acceptance/browser-fixture.html` in an isolated session, enter `Jason parity`, check Enable test, save, and verify `Jason parity | enabled`.
- Desktop: use the macOS form in `acceptance/macos/MacForm.swift` or the Windows form in `acceptance/windows/WindowsForm.ps1`. Enter `Jason parity`, click Add one once, check Enable test, save, read back the application, and validate the JSON with `acceptance/check_result.py`.

See [acceptance/README.md](../acceptance/README.md). Historical measurements remain in the [benchmark scope](benchmark.md).

When a driver disconnects after a write, inspect the application and saved result first. Reconnect once when justified, verify the state, and use an independently available route if the failure persists.

## Privacy

Skill-file installation can run offline. Required-tool installation contacts official release sources and, if requested, the upstream browser-runtime installer. The generated Cua MCP child environment opts out of Cua telemetry. A separately running daemon may have its own environment; verify its effective settings through upstream documentation.

Project source is MIT licensed. Third-party binaries retain their own upstream licenses. Recipients keep their own accounts, credentials, browser profiles, SSH keys, and system grants.
