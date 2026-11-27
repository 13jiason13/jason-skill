# Security and privacy

## Package contents

The release contains Jason Skill source, readable installer code, a required-tool installer, synthetic acceptance fixtures, de-identified historical measurements, and the MIT license. An explicit allowlist defines skill-bundle contents. Publisher accounts, cookies, private keys, remote-server configuration, personal files, real-operation recordings, and system grants are excluded.

Validate the whole downloaded installer against the checksum obtained from a trusted review or release before executing it. The per-file bundle hashes detect corruption; they are not a publisher identity signature.

Third-party agent-desktop, agent-browser, optional Cua, and browser-runtime binaries are not stored in git. They are fetched at install time from pinned official GitHub releases and checked against fixed SHA-256 values. A later published release may also attach those official binaries as per-OS GitHub Release assets. Recipients should still verify checksums from a trusted source.

## Installation behavior

Skill-file installation can run offline with `--skill-files-only`. That step alone is not a complete install. Attaching or registering skill files only is incomplete. Installation is incomplete until the required tools (agent-desktop and agent-browser) are installed on macOS or Windows. `install_bundle.py` installs those required tools by default. Cua remains optional.

Required-tool preview is read-only. The default install, `--with-required-tools`, or `setup_all.py --apply` fetches pinned official assets, verifies their fixed SHA-256 values, and checks executable versions. `--browser-runtime` runs agent-browser's own official runtime installer. Optional macOS Cua setup also validates Apple code signing, the expected developer team, and Gatekeeper assessment. Windows setup respects Defender and organizational policy. Verify the installer checksum before executing it. Downloading or cloning the repository does not run the installer.

macOS recipients grant Accessibility and Screen Recording themselves in System Settings. Windows recipients must use a signed-in interactive desktop; do not treat a locked or disconnected session as a valid desktop environment. Scripts do not edit TCC databases, global MCP configuration, global PATH, proxies, network settings, Windows execution policy, or elevation state.

Official required tools are unavailable on Linux and other non-macOS, non-Windows systems. Doctor and installer reports must say so clearly.

## Runtime data

Desktop snapshots, browser output, clipboard content, and recordings can contain private information. Use task-specific sessions, exact targets, and synthetic data for tests. Keep raw private artifacts out of public issues and logs.

Third-party tools and the host use their own privacy mechanisms. Generated Cua MCP configuration requests telemetry opt-out for its child process. Verify effective settings separately if using a standalone daemon.

## Reporting

Use a private reporting channel with a minimal, de-identified reproduction. If a credential has leaked, revoke it promptly and then follow GitHub's history-removal guidance. Avoid posting the original secret in an issue.

References: [GitHub push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection), [GitHub acceptable use](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies), and the [upstream Cua project](https://github.com/trycua/cua).
