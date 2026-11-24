# Jason Skill

**Draft 0.3.0-draft — for review, not a published release.**

A Codex skill for verified file, browser, and desktop workflows. It selects an appropriate interface for the task, batches compatible actions, and checks the actual result.

This draft keeps the skill small and readable, then adds a required-tool installer and a synthetic acceptance pack. Installation is incomplete until **agent-desktop** and **agent-browser** are installed. Cua remains optional. macOS and Windows are separate install paths. Official required tools are not available on Linux.

The current public checksum-verified release remains [v0.2.2](https://github.com/13jiason13/jason-skill/releases). Do not treat this draft, or the unverified `Jason-Skill-0.3.0-source.zip` already present on GitHub, as a published 0.3.0 release.

## Install in three steps

1. Install the skill files.
2. Install the required tools: agent-desktop and agent-browser. Cua is optional.
3. Run acceptance on this computer.

Report these states separately and do not collapse them into one success message: **installed**, **connected**, **permissions granted**, and **acceptance passed**. Recipients grant system permissions and complete third-party sign-ins on their own computer. This package does not include accounts, cookies, private files, or real-operation recordings.

Python 3.8 or later is required. Download the draft installer only after review, verify its SHA-256, attach the TXT file to a Codex environment with local file and terminal access, and ask:

> Install Jason Skill, install the required desktop and browser tools, and run acceptance.

That request is installation intent for the required tools. Invoke `$jason-skill` after a complete install. Open a new conversation if the host has not refreshed its skill list.

From this source tree:

```sh
python3 tools/build_bundle.py
python3 tools/install_bundle.py dist/Jason-Skill-0.3.0-draft-install.txt --with-required-tools
```

`--with-required-tools` installs the skill files, then installs required official tools (SHA-256 checked). Without it, skill-file installation can finish offline, but the status is incomplete. Add `--include-cua` only for optional official Cua. Use `--skills-root` for an existing host skill directory, and `--replace` only after inspecting a different installed copy.

### macOS

Use `python3` as shown above. The installer selects official native assets for this Mac:

| Mac | Required official assets |
| --- | --- |
| Apple Silicon (arm64) | agent-browser Darwin arm64; agent-desktop aarch64-apple-darwin |
| Intel (x86_64) | agent-browser Darwin x64; agent-desktop x86_64-apple-darwin |

A Rosetta-capable host that is arm64-capable is treated as arm64.

After the binaries are installed, grant **Accessibility** and **Screen Recording** in System Settings > Privacy & Security. Scripts do not edit TCC and cannot click those dialogs for you. Connect the returned command paths through the host-supported configuration path, then reload if required. Run:

```sh
python3 ~/.agents/skills/jason-skill/scripts/doctor.py
python3 ~/.agents/skills/jason-skill/scripts/accept.py --all
```

Desktop acceptance uses `acceptance/macos/MacForm.swift` and needs Xcode Command Line Tools. Optional Cua setup is `scripts/setup_all.py --apply --include-cua`; the helper verifies SHA-256, Apple code signing, the expected developer team, and Gatekeeper assessment.

### Windows

Use `py -3` where examples use `python3`. Required-tool installation and desktop acceptance must run from the **signed-in interactive desktop**. Do not use a locked or disconnected session. Follow Microsoft Defender and organizational policy.

```bat
py -3 tools/build_bundle.py
py -3 tools/install_bundle.py dist/Jason-Skill-0.3.0-draft-install.txt --with-required-tools
py -3 %USERPROFILE%\.agents\skills\jason-skill\scripts\doctor.py
py -3 %USERPROFILE%\.agents\skills\jason-skill\scripts\accept.py --all
```

| Windows PC | Required official assets |
| --- | --- |
| Windows x64 | Native agent-desktop and agent-browser |
| Windows 11 ARM | Native ARM64 agent-desktop; official x64 agent-browser through OS emulation, subject to a runtime and page test |
| Windows 10 ARM | Native ARM64 agent-desktop; no pinned official agent-browser asset, so the required browser tool cannot be completed from this installer |

Desktop acceptance uses `acceptance/windows/WindowsForm.ps1`. Optional Cua setup is `scripts/setup_all.py --apply --include-cua` and needs its own form verification from the interactive session.

### Linux and other systems

Official agent-desktop and agent-browser releases are not available. You can install the skill files and run the file-organization check, but a complete install of the required browser and desktop tools cannot be finished here. Use a Mac or a Windows PC for those routes.

## Capabilities

| Task | Route | Verification |
| --- | --- | --- |
| Find, edit, organize, and archive files | Host file tools, terminal, or application APIs | Read the saved file and check its destination |
| Read pages, fill forms, and submit information | Isolated browser or agent-browser | Check the page state and submission result |
| Read windows, click, type, check controls, and save | Host Computer Use, required agent-desktop, or optional Cua Driver | Read the application model and persisted output |
| Operate canvases or authorized remote consoles | Available visual desktop tools; SSH when suitable | Confirm the target and actual response |
| Configure a new machine and diagnose missing tools | Bundled environment and setup scripts | Report installation, connection, permission, and acceptance separately |

Pinned official versions in this draft, unchanged from 0.2.2: [agent-browser](https://github.com/vercel-labs/agent-browser) 0.43.0, [agent-desktop](https://github.com/vercel-labs/agent-desktop) 1.3.1, and optional [Cua Driver](https://github.com/trycua/cua/releases/tag/cua-driver-rs-v0.55.0) 0.55.0. Binaries are fetched at install time from those official releases, or may later be attached as per-OS GitHub Release assets. They are not committed to git.

## Scripts

| Script | Purpose |
| --- | --- |
| `tools/build_bundle.py` | Build the readable single-file installer and integrity manifest from an explicit file list |
| `tools/install_bundle.py` | Validate and install the skill; with `--with-required-tools`, also install required official tools |
| `scripts/doctor.py` | Read-only platform, architecture, Python, and dependency detection, with OS-specific next steps |
| `scripts/setup_all.py` | One setup entry point; required tools by default, optional Cua with `--include-cua` |
| `scripts/setup_tools.py` | Fetch pinned official CLI assets, verify SHA-256, and check executable versions |
| `scripts/setup_macos.py` | Optional signed macOS Cua installation and machine-specific MCP configuration |
| `scripts/setup_windows.py` | Optional native Windows Cua installation and machine-specific MCP configuration |
| `scripts/accept.py` | Synthetic file check, plus macOS- and Windows-specific browser and desktop acceptance procedures |
| `acceptance/` | Local file procedure, browser fixture, macOS form, Windows form, and saved-result verifier |

See the [portable installation guide](skills/jason-skill/references/portable-install.md) and the [acceptance pack](skills/jason-skill/acceptance/README.md).

## Verification and compatibility

Run `python3 -m unittest discover -s tests -v`. This draft adds tests around incomplete installs, Linux unavailability, OS-specific doctor guidance, and the file acceptance check. Use the [shared acceptance procedure](skills/jason-skill/acceptance/README.md) on each Mac or Windows machine.

On one Intel Mac running macOS 14.8.9, the earlier 0.2.2 local Cua 0.55.0 compatibility build passed background read, click, text entry, checkbox, save, and persisted-file verification. The public installer uses official binaries. The optional source patch and its provenance are included under `patches/`.

Windows GUI acceptance, Windows ARM browser emulation, other target applications, and cross-machine performance remain unverified in this draft. Historical driver timings are documented in the [benchmark scope](skills/jason-skill/references/benchmark.md).

## License and privacy

Jason Skill source is distributed under the [MIT License](LICENSE). Third-party tools are downloaded from their upstream projects and retain their own licenses. The package excludes publisher accounts, browser profiles, credentials, remote-server configuration, and system grants. See [SECURITY.md](SECURITY.md).

---

## 中文说明

这是 **0.3.0-draft** 审阅稿，还不是已发布版本。当前已核验的公开发布仍是 0.2.2。

别人要复刻的是这套功能和工作流，不是你的电脑环境。安装分三步，而且 **必须先装完必装工具，才算安装完成**：

1. 安装 skill 文件。
2. 安装必装工具：agent-desktop 和 agent-browser。Cua 仍是可选项。
3. 在自己的电脑上跑验收。

安装结果要分开报告这四件事，不要混成一句“成功了”：**已安装**、**已连接**、**已授权**、**验收通过**。macOS 的辅助功能/屏幕录制权限，以及 Windows 上的登录交互桌面，必须由对方自己确认。第三方账号登录也一样。这些都不会、也不该打进安装包。

### macOS

用 `python3 tools/install_bundle.py … --with-required-tools`。安装器会按这台 Mac 选择官方原生资源：Apple Silicon 用 arm64，Intel 用 x86_64。装完二进制后，到“系统设置 > 隐私与安全性”里打开**辅助功能**和**屏幕录制**。脚本不会改 TCC，也不能替对方点同意。然后连接工具、运行 `scripts/accept.py --all`。桌面验收用 `acceptance/macos/MacForm.swift`。

### Windows

需要时用 `py -3`。必装工具和桌面验收必须在**已登录的交互桌面**上运行，不要在锁屏或断开会话里做。Windows x64 使用官方原生资源；Windows 11 ARM 的 agent-desktop 用官方 ARM64 资源，agent-browser 走官方 x64 资源的系统模拟，并需要单独做运行时和页面测试；Windows 10 ARM 没有 pinned 的官方 agent-browser 资源，必装浏览器工具在这个安装器里无法完成。桌面验收用 `acceptance/windows/WindowsForm.ps1`。

### Linux 及其他系统

官方的 agent-desktop 和 agent-browser 不可用。可以安装 skill 文件，也可以跑本地文件整理验收，但浏览器和桌面这两条链路要在 Mac 或 Windows 上才能装完必装工具。
