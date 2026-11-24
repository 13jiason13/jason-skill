import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "skills/jason-skill/scripts"))
import doctor
import setup_all
import install_bundle as installer


class RequiredInstallTests(unittest.TestCase):
    def test_linux_doctor_does_not_use_macos_permission_steps(self):
        with patch.object(doctor.platform, "system", return_value="Linux"), \
                patch.object(doctor.platform, "machine", return_value="x86_64"), \
                patch.object(doctor.platform, "release", return_value="6.1"):
            report = doctor.inspect()
        self.assertFalse(report["official_tools_supported"])
        self.assertFalse(report["install_complete"])
        joined = " ".join(report["next_steps"])
        self.assertNotIn("System Settings", joined)
        self.assertNotIn("Accessibility", joined)
        self.assertIn("not available", joined.lower())

    def test_macos_and_windows_guidance_stay_separate(self):
        mac_perm, mac_steps, mac_note = doctor.platform_guidance("Darwin", "arm64")
        win_perm, win_steps, win_note = doctor.platform_guidance("Windows", "x86_64")
        win11_perm, win11_steps, win11_note = doctor.platform_guidance("Windows", "arm64", 22631)
        win10_perm, win10_steps, win10_note = doctor.platform_guidance("Windows", "arm64", 19045)
        self.assertEqual(mac_perm["macos"], ["Accessibility", "Screen Recording"])
        self.assertNotIn("macos", win_perm)
        self.assertIn("Interactive signed-in desktop session", win_perm["windows"])
        self.assertIn("arm64", mac_note.lower())
        self.assertIn("native", win_note.lower())
        self.assertIn("emulation", win11_note.lower())
        self.assertIn("no pinned official agent-browser", win10_note.lower())
        self.assertTrue(any("Accessibility" in step for step in mac_steps))
        self.assertTrue(any("interactive desktop" in step.lower() for step in win_steps))

    def test_setup_all_linux_apply_is_incomplete_without_downloads(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as directory:
            args = SimpleNamespace(
                apply=True, tool_root=Path(directory) / "tools", pinned=True,
                include_cua=False, cua_target=Path(directory) / "unused.app",
                browser_runtime=False)
            with patch.object(setup_all.setup_tools, "platform_key", return_value=("Linux", "x86_64")), \
                    patch.object(setup_all.setup_tools, "download_checked") as download, \
                    patch.object(setup_all.subprocess, "run") as run:
                result = setup_all.run_setup(args)
            download.assert_not_called()
            run.assert_not_called()
            self.assertEqual(result["official_tools"], "unavailable")
            self.assertFalse(result["install_complete"])
            self.assertFalse(result["required_tools_complete"])
            self.assertEqual(result["required_tools"], ["agent-desktop", "agent-browser"])
            self.assertEqual(result["cua"]["status"], "optional-not-requested")

    def test_install_bundle_does_not_fetch_tools_without_flag(self):
        bundle = __import__("build_bundle").build()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "skills"
            with patch.object(installer, "configure_required_tools") as configure:
                result = installer.install(bundle, root)
            configure.assert_not_called()
            self.assertTrue(result["skill_files_installed"])
            self.assertIsNone(result["tool_setup"])
            self.assertTrue((root / installer.NAME / "scripts" / "accept.py").exists())
            self.assertTrue((root / installer.NAME / "acceptance" / "macos" / "MacForm.swift").exists())
            self.assertTrue((root / installer.NAME / "acceptance" / "windows" / "WindowsForm.ps1").exists())

    def test_with_required_tools_invokes_setup_and_keeps_cua_optional(self):
        bundle = __import__("build_bundle").build()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "skills"
            fake = {"returncode": 2, "setup": {"install_complete": False}, "stderr": None}
            with patch.object(installer, "configure_required_tools", return_value=fake) as configure:
                result = installer.install(bundle, root, with_required_tools=True)
            configure.assert_called_once_with(root / installer.NAME, include_cua=False)
            self.assertEqual(result["tool_setup"], fake)
            self.assertEqual(result["optional_cua"], "not-requested")
            self.assertFalse(result["install_complete"])


class AcceptTests(unittest.TestCase):
    def test_file_check_passes_on_linux(self):
        sys.path.insert(0, str(ROOT / "skills/jason-skill/scripts"))
        import accept
        result = accept.run_files()
        self.assertTrue(result["passed"])
        self.assertTrue(result["cleaned"])

    def test_all_report_does_not_claim_full_acceptance_on_linux(self):
        import accept
        import subprocess
        completed = subprocess.run(
            [sys.executable, str(ROOT / "skills/jason-skill/scripts/accept.py"), "--all"],
            capture_output=True, text=True, timeout=10)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertFalse(report["acceptance_passed"])
        checks = {item["check"]: item for item in report["checks"]}
        self.assertTrue(checks["files"]["passed"])
        self.assertEqual(checks["browser"]["status"], "official-tools-unavailable")
        self.assertEqual(checks["desktop"]["status"], "official-tools-unavailable")

    def test_desktop_result_verifier(self):
        import accept
        with tempfile.TemporaryDirectory() as folder:
            good = Path(folder) / "good.json"
            bad = Path(folder) / "bad.json"
            good.write_text('{"name": "Jason parity", "enabled": true, "count": 1}', encoding="utf-8")
            bad.write_text('{"name": "nope", "enabled": true, "count": 1}', encoding="utf-8")
            self.assertTrue(accept.verify_desktop_result(good)["passed"])
            self.assertFalse(accept.verify_desktop_result(bad)["passed"])


if __name__ == "__main__":
    unittest.main()
