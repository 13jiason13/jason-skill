# Reproduction fixtures

`results/native-controls.json` preserves de-identified driver samples, versions, and timing boundaries. `ControlFixture.swift` contains the original native fixture. The historical documentation describes its scope.

For cross-platform acceptance, use `parity/README.md`. Open `browser-fixture.html` in a task-specific browser session, enter `Jason parity`, check Enable test, submit, and verify `Jason parity | enabled`.

Compare three alternating rounds on the same task, keeping driver timing and end-to-end timing separate. Record success, retries, screenshots, focus changes, and actual saved output. Model token and quota measurements need a real source; unknown values remain unknown.

Installer test results are recorded in `TEST-REPORT.json`.

After installation, prefer `skills/jason-skill/acceptance/` and `scripts/accept.py --all`.
