# Jason Skill v0.3.0-draft

**This is a review draft, not a published release.** The current checksum-verified public release remains v0.2.2.

This draft changes installation so other people can reproduce the skill's file, browser, and desktop workflow. It does not promise that every computer will match one author's results.

## Changes since 0.2.2

- Installation is a required three-step path: install the skill, install required tools, run acceptance.
- agent-desktop and agent-browser are required. `install_bundle.py` installs them by default. `--with-required-tools` is that same default written explicitly. `--skill-files-only` is the offline skill-files-only opt-out. Without those tools the installer reports `skill-installed-required-tools-incomplete` and exits 2. Attaching or registering skill files only is incomplete. When required tools are missing, `doctor.py` prints a ready-to-run `next_command` (`setup_all.py --apply --browser-runtime`).
- Cua Driver remains optional and is installed only with `--include-cua`.
- macOS and Windows are documented and reported as separate install paths, including architecture-specific official assets and permission models.
- Linux and other systems are documented as official required tools unavailable. File-route acceptance can still run.
- `doctor.py` and `setup_all.py` report installed, connected, permissions granted, and acceptance passed separately, with OS-specific next steps.
- A synthetic acceptance pack ships inside the skill: local file organization, `acceptance/browser-fixture.html`, `acceptance/macos/MacForm.swift`, and `acceptance/windows/WindowsForm.ps1`.
- Pinned official versions are unchanged: agent-browser 0.43.0, agent-desktop 1.3.1, optional Cua 0.55.0. Binaries are still fetched from official sources with SHA-256 checks and are not committed to git.

## Platform notes

- macOS: official native arm64 or x86_64 assets; recipient grants Accessibility and Screen Recording in System Settings.
- Windows x64: official native required-tool assets; signed-in interactive desktop required for desktop operations.
- Windows 11 ARM: native ARM64 agent-desktop; official x64 agent-browser through OS emulation, subject to a runtime and page test.
- Windows 10 ARM: native ARM64 agent-desktop only; required browser install cannot be completed from this installer.
- Linux: official required tools unavailable.

## Validation

Automated tests in this draft are intended to run on Linux without downloading third-party binaries. macOS and Windows GUI acceptance, Windows ARM browser emulation, particular applications, and cross-machine speed still require recipient-side verification. This draft is marked as a preview.

The unverified `Jason-Skill-0.3.0-source.zip` already present in the public GitHub repository is not this draft, has no `SHA256SUMS.txt` entry, and is not an approved release.
