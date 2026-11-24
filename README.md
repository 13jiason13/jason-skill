# Jason Skill

Verified file, browser, and desktop workflows for Codex on macOS and Windows.

[Download installer](Jason-Skill-0.2.2-install.txt) · [Download complete MIT source](Jason-Skill-0.2.2-source.zip) · [SHA-256 checksums](SHA256SUMS.txt) · [Security and privacy](SECURITY.md)

## Install

Verify the download checksum, attach the installer TXT to Codex with local file and terminal access, and ask:

> Install Jason Skill and configure the desktop and browser tools I need.

Python 3.8+ is required. Windows can use `py -3`. Invoke `$jason-skill` after installation. The recipient completes system permissions and third-party sign-ins on their own computer.

## Capabilities

| Task | Tools | Acceptance |
| --- | --- | --- |
| File editing, organization, and batch work | Host file tools and terminal | Saved paths and content |
| Browser reading, forms, and submissions | Isolated browser or agent-browser | Actual page state |
| Native windows, controls, text, and save | Computer Use, agent-desktop, or optional Cua | Application readback and saved files |

The complete source ZIP includes the skill, a readable bundle installer, dependency setup, macOS and Windows test forms, benchmark scope, optional Sonoma source patch, and MIT license.

## Compatibility

The local automated run passed 27 tests. One Intel Mac has verified desktop samples. Windows dependency selection is simulated; Windows GUI, Windows 11 ARM browser emulation, particular applications, and cross-machine speed need acceptance on the recipient's machine. See the included shared test procedure.

Third-party dependencies are fetched from official sources with pinned SHA-256 checks. This package excludes publisher credentials, browser profiles, remote-server configuration, and system grants.

## Release

Version 0.2.2 is a cross-platform preview. Read [release notes](RELEASE-NOTES.md), the [MIT License](LICENSE), and [security documentation](SECURITY.md).
