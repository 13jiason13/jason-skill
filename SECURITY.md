# Security and privacy

## Package contents

The release contains Jason Skill source, readable installer code, synthetic test fixtures, de-identified historical measurements, and the MIT license. An explicit allowlist defines release contents. Publisher accounts, cookies, private keys, remote-server configuration, personal files, real-operation recordings, and system grants are excluded.

Validate the whole downloaded installer against the checksum obtained from a trusted release before executing it. The per-file bundle hashes detect corruption; they are not a publisher identity signature.

## Installation behavior

Basic skill installation can run offline. Dependency preview is read-only. Explicit `--apply` installation fetches pinned official assets, verifies their fixed SHA-256 values, and checks executable versions. Optional macOS Cua setup also validates Apple code signing, the expected developer team, and Gatekeeper assessment. Windows setup respects Defender and organizational policy.

The optional `--browser-runtime` action runs agent-browser's own runtime installer. System permissions are granted by the recipient through native system interfaces. Scripts do not edit TCC databases, global MCP configuration, global PATH, proxies, or network settings.

## Runtime data

Desktop snapshots, browser output, clipboard content, and recordings can contain private information. Use task-specific sessions, exact targets, and synthetic data for tests. Keep raw private artifacts out of public issues and logs.

Third-party tools and the host use their own privacy mechanisms. Generated Cua MCP configuration requests telemetry opt-out for its child process. Verify effective settings separately if using a standalone daemon.

## Reporting

Use a private reporting channel with a minimal, de-identified reproduction. If a credential has leaked, revoke it promptly and then follow GitHub's history-removal guidance. Avoid posting the original secret in an issue.

References: [GitHub push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection), [GitHub acceptable use](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies), and the [upstream Cua project](https://github.com/trycua/cua).
