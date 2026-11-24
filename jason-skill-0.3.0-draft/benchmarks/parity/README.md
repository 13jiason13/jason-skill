# Shared macOS and Windows acceptance

The skill-shipped pack lives in `skills/jason-skill/acceptance/`. Use that copy after installation. This directory keeps the same fixtures for source-tree review.


Use synthetic data and an owned test window. Record OS, architecture, and tool versions. Installation and delivery acknowledgments do not replace result checks.

| Test | Input and expected result |
| --- | --- |
| Files | In an empty directory, create `parity.txt` containing `Jason parity`, move it to a new `done` folder, and verify the source is gone and the destination content matches. |
| Browser | Open `../browser-fixture.html` in an isolated session. Enter `Jason parity`, check Enable test, click Save locally, and verify `Jason parity \| enabled`. |
| Native form | Use the fixture below. Enter `Jason parity`, click Add one once, check Enable test, and click Save test. Read back the application, then validate the JSON with `check_result.py`. |
| Timing | Record cold startup separately. Repeat each route at least three times with the same checks. Record failures, retries, screenshots, foreground changes, and actual completion. |

Windows PowerShell, from this directory, in the signed-in interactive desktop:

```powershell
$result = Join-Path $env:TEMP ("jason-parity-" + [guid]::NewGuid().ToString("N") + ".json")
Write-Output $result
powershell -NoProfile -STA -File .\WindowsForm.ps1 -ResultFile $result
py -3 .\check_result.py $result
```

macOS, with Xcode Command Line Tools:

```sh
probe_dir="$(mktemp -d)"
xcrun swiftc -parse-as-library MacForm.swift -o "$probe_dir/JasonParityTest"
"$probe_dir/JasonParityTest" "$probe_dir/result.json"
python3 check_result.py "$probe_dir/result.json"
```

Choose a fresh, writable result path. Both native forms write the same fields. Background-input support depends on the application, window state, and system permissions. Record any failed route and select an authorized alternative.
