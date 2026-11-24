# Tool routes

agent-desktop and agent-browser are required tools. Installation is incomplete until both are installed on macOS or Windows. Cua Driver remains optional. Official required tools are not available on Linux.

## Cua Driver

Confirm that the current host exposes callable Cua tools. Read `get_guide({topic:"overview"})` and the platform/permission guidance; check permissions before GUI operations. This distribution pins optional downloads to 0.55.0.

Use `list_windows` for the exact process/window, a narrow `get_window_state` for fresh references, and `run_steps` with one final observation for known compatible actions. Prefer background delivery when supported. Refresh tokens after a state change. Use `type_text` when an attribute assignment fails to update the application model.

For browser page content, use supported typed browser tools. An existing-profile connection requires the recipient's authorization and a supported startup grant. If that connection is unavailable, inspect permitted accessibility routes and verify each result before switching tools.

Generate MCP paths on the recipient's machine. Official downloads and the local compatibility build are distinct; each needs its own acceptance test.

Source: https://github.com/trycua/cua

## agent-desktop

Before first use, run `agent-desktop status`, `agent-desktop skills get desktop`, and `agent-desktop skills get platform`. Use the installed binary or the path returned by the setup helper.

Prefer `find` or a narrow snapshot. Act only on current qualified references and the intended window. Inspect uncertain delivery before retrying. Headed input follows the user's explicit permission for foreground interaction.

Source: https://github.com/vercel-labs/agent-desktop

## Browser

Reuse the host's connected isolated browser when suitable. agent-browser offers a task-specific isolated session; load `agent-browser skills get core` before using it. Check the submitted page state rather than only an input value.

Existing-profile access uses the host's supported browser connection. Keep unrelated tabs, cookies, passwords, and state exports out of public logs. A successful local form test does not establish compatibility with every website.

Source: https://github.com/vercel-labs/agent-browser

## Host Computer Use

Check the host's currently callable tools and permissions. Use an exact observed target and verify the action. The host's built-in capabilities are provided by that host; availability and model access depend on the recipient's environment.

## Remote consoles

Identify whether the terminal is at login, password entry, or a shell prompt. Test a short harmless input before sending long commands. If text is corrupted, stop batch input and read back the current screen. A connected viewer proves only the viewer connection. Prefer SSH for authorized server diagnostics once available.
