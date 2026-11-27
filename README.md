# Jason Skill

Verified file, browser, and desktop workflows for Codex on macOS and Windows.

The checksum-verified public release remains **0.2.2**. The reviewed required-tools update in this repository is **0.3.0-draft**. Installation of that draft is three steps: install the skill, install the required tools, then run acceptance. **agent-desktop** and **agent-browser** are mandatory. `install_bundle.py` installs them by default. Attaching or registering skill files only is incomplete. `--skill-files-only` is the offline opt-out; without the required tools the installer stays at `skill-installed-required-tools-incomplete` and exits 2. Cua stays optional (`--include-cua`). macOS and Windows are separate flows. Official required tools are unavailable on Linux. Downloading or cloning this repository does not run the installer. Pinned binaries are fetched at install time and checked with SHA-256: agent-browser 0.43.0, agent-desktop 1.3.1, and optional Cua 0.55.0. The acceptance pack uses synthetic data only. This package does not include accounts, cookies, private files, or real-operation recordings.

`Jason-Skill-0.3.0-source.zip` is an unverified snapshot already in the repository. It is labeled in [Jason-Skill-0.3.0-source.NOT-APPROVED.txt](Jason-Skill-0.3.0-source.NOT-APPROVED.txt) and is omitted from [SHA256SUMS.txt](SHA256SUMS.txt).

## Downloads

Verify a download against [SHA256SUMS.txt](SHA256SUMS.txt) before use.

### Verified release 0.2.2

[Installer](Jason-Skill-0.2.2-install.txt) · [Complete MIT source](Jason-Skill-0.2.2-source.zip) · [Release notes](RELEASE-NOTES.md) · [Security and privacy](SECURITY.md) · [MIT License](LICENSE)

### Reviewed draft 0.3.0-draft

[Installer](Jason-Skill-0.3.0-draft-install.txt) · [Complete MIT source](Jason-Skill-0.3.0-draft-source.zip) · [Source tree](jason-skill-0.3.0-draft/) · [Release notes](jason-skill-0.3.0-draft/RELEASE-NOTES.md) · [Security and privacy](SECURITY.md)

Copyright (c) 2026 jason-skill contributors. The [MIT License](LICENSE) is unchanged.

## Install the reviewed draft

Python 3.8 or later is required. On Windows, use `py -3`. Downloading or cloning this repository does not install the skill or the tools. Verify the installer checksum in [SHA256SUMS.txt](SHA256SUMS.txt) before use, attach `Jason-Skill-0.3.0-draft-install.txt` to a Codex environment with local file and terminal access, and ask:

> Install Jason Skill, install the required desktop and browser tools (agent-desktop and agent-browser), and run acceptance. Attaching or registering the skill files only is incomplete.

From the source tree:

```sh
cd jason-skill-0.3.0-draft
python3 tools/build_bundle.py
python3 tools/install_bundle.py dist/Jason-Skill-0.3.0-draft-install.txt --with-required-tools
python3 ~/.agents/skills/jason-skill/scripts/doctor.py
python3 ~/.agents/skills/jason-skill/scripts/accept.py --all
```

`install_bundle.py` installs the skill files, then fetches the pinned official agent-desktop and agent-browser binaries (SHA-256 checked). That is the default. `--with-required-tools` is the same request written out explicitly. Add `--include-cua` only when optional Cua is requested. `--skill-files-only` is the offline skill-files-only opt-out and does not fetch those tools. Without agent-desktop and agent-browser, the status stays `skill-installed-required-tools-incomplete` and the process exits 2. If `doctor.py` reports the required tools missing, run the `next_command` it prints instead of continuing with only host automation or host Chrome.

Report these states separately: **installed**, **connected**, **permissions granted**, and **acceptance passed**.

### macOS

The installer selects official native assets: Apple Silicon uses arm64, Intel uses x86_64. A Rosetta-capable arm64 host is treated as arm64. After the binaries are installed, grant **Accessibility** and **Screen Recording** in System Settings > Privacy & Security. Scripts do not edit TCC. Desktop acceptance uses `acceptance/macos/MacForm.swift` and Xcode Command Line Tools.

### Windows

Required-tool install and desktop acceptance must run from the signed-in interactive desktop. Windows x64 uses official native agent-desktop and agent-browser. Windows 11 ARM uses official native ARM64 agent-desktop and official x64 agent-browser through OS emulation, with a separate runtime and page test. Windows 10 ARM has official native ARM64 agent-desktop only; this installer has no pinned official agent-browser asset for that system. Desktop acceptance uses `acceptance/windows/WindowsForm.ps1`.

### Linux

Official agent-desktop and agent-browser assets are unavailable. Skill files and the file-organization check can still run. A complete required-tool install cannot be finished on Linux.

The full bilingual guide is [jason-skill-0.3.0-draft/README.md](jason-skill-0.3.0-draft/README.md). Acceptance steps are in [jason-skill-0.3.0-draft/skills/jason-skill/acceptance/README.md](jason-skill-0.3.0-draft/skills/jason-skill/acceptance/README.md).

## 中文说明

已核验的公开发布仍是 0.2.2。本页加入的是审阅过的 **0.3.0-draft**：先安装 skill，再安装必装工具，然后在自己的电脑上验收。下载或克隆仓库不会自动安装。只把 skill 文件挂上或注册到宿主，不算安装完成。agent-desktop 和 agent-browser 是必装项，`install_bundle.py` 默认就会安装它们。`--with-required-tools` 是把这个默认写明。`--skill-files-only` 才是离线、只装 skill 文件的退出选项；没装完必装工具时，状态仍是 `skill-installed-required-tools-incomplete`，退出码为 2。Cua 只用 `--include-cua` 才安装。macOS 与 Windows 是分开的流程。Linux 上没有官方必装工具。安装前请对照 `SHA256SUMS.txt` 核验校验和。仓库里的 `Jason-Skill-0.3.0-source.zip` 是未核验快照，不在 `SHA256SUMS.txt` 里。完整中文说明见 [源码 README](jason-skill-0.3.0-draft/README.md)。
