# Acceptance pack

Use synthetic data only. Do not use accounts, cookies, private files, or real-operation recordings.

Run from the installed skill directory:

```sh
python3 scripts/accept.py --all
```

On Windows, use `py -3` instead of `python3` when needed. The file check can run on any OS. Browser and desktop checks pass only after the actual page or saved form is verified.

## Files

`scripts/accept.py --files` creates `parity.txt` containing `Jason parity`, moves it into a `done` folder, and checks that the source is gone and the destination content matches.

## Browser

Open `browser-fixture.html` in an isolated agent-browser session or the host isolated browser. Enter `Jason parity`, check Enable test, click Save locally, and verify `Jason parity | enabled`.

Official agent-browser assets are for macOS and Windows only.

## Desktop: macOS

Grant Accessibility and Screen Recording in System Settings > Privacy & Security first. Scripts do not edit TCC.

```sh
probe_dir="$(mktemp -d)"
xcrun swiftc -parse-as-library macos/MacForm.swift -o "$probe_dir/JasonParityTest"
"$probe_dir/JasonParityTest" "$probe_dir/result.json"
python3 check_result.py "$probe_dir/result.json"
```

Enter `Jason parity`, click Add one once, check Enable test, and click Save test. Then read back the application and validate the saved JSON. Xcode Command Line Tools are required.

## Desktop: Windows

Run this from the signed-in interactive desktop. Do not use a locked or disconnected session.

```powershell
$result = Join-Path $env:TEMP ("jason-parity-" + [guid]::NewGuid().ToString("N") + ".json")
Write-Output $result
powershell -NoProfile -STA -File .\windows\WindowsForm.ps1 -ResultFile $result
py -3 .\check_result.py $result
```

Enter `Jason parity`, click Add one once, check Enable test, and click Save test. Then read back the application and validate the saved JSON.

## Linux

Official agent-desktop and agent-browser releases are not available. You can still run the file check. Browser and desktop acceptance require macOS or Windows.
