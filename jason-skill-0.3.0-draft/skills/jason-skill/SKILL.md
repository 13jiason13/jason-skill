---
name: jason-skill
description: Operate local files, websites, and desktop apps through an appropriate CLI, service interface, isolated browser, accessibility driver, or host Computer Use tool, with efficient observation and actual-result verification.
---

# Jason Skill

Choose the fastest currently verified route that fits the requested task. Check which tools the current host actually exposes. Reuse an available host interface or installed tool before adding dependencies.

## Routing

| Task | Preferred route | Result to verify |
| --- | --- | --- |
| Files, configuration, services, SSH | Authorized CLI or service API | File contents, service status, or actual response |
| Supported structured websites | Connected isolated browser | Rendered state and application result |
| Native accessibility controls | A suitable, verified agent-desktop route, or optional Cua Driver | Model readback and saved output |
| Canvas or remote console with weak semantics | Available host Computer Use or screenshot route | Fresh visual evidence and actual postcondition |

An observed advantage on one window applies to that tested scenario. Use a different route when the target toolkit or current machine behaves differently.

## Observe, act, verify

1. Identify the exact target application and window, then read fresh state. Narrow observation after locating the relevant region.
2. Act on qualified, current references. Prefer background delivery where the target supports it. Foreground input follows the user's authorization.
3. Batch known compatible actions. Keep actions sequential when the next step depends on an earlier result.
4. Verify the application's actual state, saved file, or response. An attribute echo or delivery acknowledgment alone does not establish completion.
5. If delivery is uncertain, inspect the current state before repeating a click, input, or submission.

Refresh references when the window, menu, or list changes. Use screenshots for canvases, missing accessibility content, and visual checks. Reuse loaded guidance within the same task.

## Tool setup

Read [tool routes](references/tools.md) when first using a driver. Load its version-matched guidance and check permissions.

A complete install has three steps: install the skill files, install the required tools, then run acceptance. Installation is incomplete until **agent-desktop** and **agent-browser** are installed. Cua remains optional. macOS and Windows are separate install paths; official required tools are not available on Linux.

For new machines or missing required tools, read [portable setup](references/portable-install.md), run `scripts/doctor.py`, and preview `scripts/setup_all.py`. A user request to install Jason Skill, or to configure the tools it needs, supplies installation intent for `install_bundle.py --with-required-tools` or `scripts/setup_all.py --apply --browser-runtime`. Use `--include-cua` only for optional Cua setup.

Do not report the install as complete when only the skill files are present. Report these states separately and do not collapse them into one success message:

- installed (required tools are present)
- connected (the host can actually call the tools)
- permissions granted (macOS Accessibility and Screen Recording, or a Windows signed-in interactive desktop)
- acceptance passed (the local file, browser, and owned-window checks verified actual results)

After an uncertain write or disconnection, check whether the operation occurred before reconnecting. One clean reconnect followed by a targeted check is appropriate; if it fails, use an independently available route.

## Privacy and continuity

Preserve current working sessions, unsaved work, and the active usable network. Network changes, service restarts, and SSH modifications remain within the user's task scope.

Use task-specific browser sessions and synthetic acceptance data. Keep credentials, private keys, and browser state out of skill files, reports, and public artifacts. Use the user's private sign-in interface when authentication is needed.

## Performance

Measure actual completion, retries, screenshots, and focus effects. Keep driver timing and model end-to-end timing distinct. Include observation, reasoning, retries, and verification when comparing models. Historical scope and unmeasured items are documented in [benchmarks](references/benchmark.md).
