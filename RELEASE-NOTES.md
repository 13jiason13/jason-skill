# Jason Skill v0.3.0-draft

**This is a review draft, not a published release.** The checksum-verified public release remains v0.2.2.

This draft changes installation so other people can reproduce the skill's file, browser, and desktop workflow. It does not promise that every computer will match one author's results.

## Changes since 0.2.2

- Installation is a required three-step path: install the skill, install required tools, run acceptance.
- agent-desktop and agent-browser are required. The installer reports `skill-installed-required-tools-incomplete` and exits 2 until those tools are installed. `install_bundle.py --with-required-tools` continues from skill files into required-tool setup in one command.
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

`Jason-Skill-0.3.0-source.zip` remains in the repository unchanged. It is an unverified snapshot, has no `SHA256SUMS.txt` entry, and is not this draft. See [Jason-Skill-0.3.0-source.NOT-APPROVED.txt](Jason-Skill-0.3.0-source.NOT-APPROVED.txt).

The same notes are in [jason-skill-0.3.0-draft/RELEASE-NOTES.md](jason-skill-0.3.0-draft/RELEASE-NOTES.md).

# Jason Skill v0.2.2

A cross-platform preview for verified Codex file, browser, and native-desktop workflows.

- One readable skill installer and one dependency setup entry point for macOS and Windows.
- Official pinned agent-browser, agent-desktop, and optional Cua assets with SHA-256 validation.
- Native Windows x64 and ARM64 desktop routes. Windows 11 ARM can try the x64 browser through OS emulation.
- Equivalent macOS and Windows native test forms, local browser fixture, and saved-file verifier.
- English instructions, MIT source, explicit packaging allowlist, and privacy documentation.

The local automated run passed 27 tests. Historical Intel Mac samples and local compatibility-build acceptance are documented. Windows GUI acceptance, Windows ARM browser emulation, particular applications, and cross-machine speed remain to be verified. This release is marked as a preview.
