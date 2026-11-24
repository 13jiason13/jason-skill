# Jason Skill

Verified file, browser, and desktop workflows for Codex on macOS and Windows.

The checksum-verified public release remains **0.2.2**. The reviewed required-tools update in this repository is **0.3.0-draft**. Installation of that draft is three steps: install the skill, install the required tools, then run acceptance. **agent-desktop** and **agent-browser** are mandatory. The installer exits 2 until they are installed. Cua stays optional (`--include-cua`). macOS and Windows are separate flows. Official required tools are unavailable on Linux. Pinned binaries are fetched at install time and checked with SHA-256: agent-browser 0.43.0, agent-desktop 1.3.1, and optional Cua 0.55.0. The acceptance pack uses synthetic data only. This package does not include accounts, cookies, private files, or real-operation recordings.

`Jason-Skill-0.3.0-source.zip` is an unverified snapshot already in the repository. It is labeled in [Jason-Skill-0.3.0-source.NOT-APPROVED.txt](Jason-Skill-0.3.0-source.NOT-APPROVED.txt) and is omitted from [SHA256SUMS.txt](SHA256SUMS.txt).

## Downloads

Verify a download against [SHA256SUMS.txt](SHA256SUMS.txt) before use.

### Verified release 0.2.2

[Installer](Jason-Skill-0.2.2-install.txt) · [Complete MIT source](Jason-Skill-0.2.2-source.zip) · [Release notes](RELEASE-NOTES.md) · [Security and privacy](SECURITY.md) · [MIT License](LICENSE)

### Reviewed draft 0.3.0-draft

[Installer](Jason-Skill-0.3.0-draft-install.txt) · [Complete MIT source](Jason-Skill-0.3.0-draft-source.zip) · [Source tree](jason-skill-0.3.0-draft/) · [Release notes](jason-skill-0.3.0-draft/RELEASE-NOTES.md) · [Security and privacy](SECURITY.md)

Copyright (c) 2026 jason-skill contributors. The [MIT License](LICENSE) is unchanged.

## Install the reviewed draft

Python 3.8 or later is required. On Windows, use `py -3`. Verify the installer checksum, attach `Jason-Skill-0.3.0-draft-install.txt` to a Codex environment with local file and terminal access, and ask:

> Install Jason Skill, install the required desktop and browser tools, and run acceptance.

From the source tree:

```sh
cd jason-skill-0.3.0-draft
python3 tools/build_bundle.py
python3 tools/install_bundle.py dist/Jason-Skill-0.3.0-draft-install.txt --with-required-tools
```

`--with-required-tools` installs the skill files, then fetches the pinned official agent-desktop and agent-browser binaries. Add `--include-cua` only when optional Cua is requested. Without `--with-required-tools`, skill files can still be installed offline, the status is `skill-installed-required-tools-incomplete`, and the process exits 2.

Report these states separately: **installed**, **connected**, **permissions granted**, and **acceptance passed**.

### macOS

The installer selects official native assets: Apple Silicon uses arm64, Intel uses x86_64. A Rosetta-capable arm64 host is treated as arm64. After the binaries are installed, grant **Accessibility** and **Screen Recording** in System Settings > Privacy & Security. Scripts do not edit TCC. Desktop acceptance uses `acceptance/macos/MacForm.swift` and Xcode Command Line Tools.

### Windows

Required-tool install and desktop acceptance must run from the signed-in interactive desktop. Windows x64 uses official native agent-desktop and agent-browser. Windows 11 ARM uses official native ARM64 agent-desktop and official x64 agent-browser through OS emulation, with a separate runtime and page test. Windows 10 ARM has official native ARM64 agent-desktop only; this installer has no pinned official agent-browser asset for that system. Desktop acceptance uses `acceptance/windows/WindowsForm.ps1`.

### Linux

Official agent-desktop and agent-browser assets are unavailable. Skill files and the file-organization check can still run. A complete required-tool install cannot be finished on Linux.

The full bilingual guide is [jason-skill-0.3.0-draft/README.md](jason-skill-0.3.0-draft/README.md). Acceptance steps are in [jason-skill-0.3.0-draft/skills/jason-skill/acceptance/README.md](jason-skill-0.3.0-draft/skills/jason-skill/acceptance/README.md).

## 中文说明

已核验的公开发布仍是 0.2.2。本页加入的是审阅过的 **0.3.0-draft**：先安装 skill，再安装必装工具，然后在自己的电脑上验收。agent-desktop 和 agent-browser 是必装项，没装完时安装器以状态 `skill-installed-required-tools-incomplete` 退出，退出码为 2。Cua 只用 `--include-cua` 才安装。macOS 与 Windows 是分开的流程。Linux 上没有官方必装工具。仓库里的 `Jason-Skill-0.3.0-source.zip` 是未核验快照，不在 `SHA256SUMS.txt` 里。完整中文说明见 [源码 README](jason-skill-0.3.0-draft/README.md)。
