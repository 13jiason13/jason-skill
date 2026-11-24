import hashlib
import io
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills/jason-skill/scripts"))
import setup_tools


class SetupToolsTests(unittest.TestCase):
    def test_arm64_windows_only_offers_the_available_native_tool(self):
        root = Path("isolated")
        platform = ("Windows", "arm64")
        desktop = setup_tools.plan_tool("agent-desktop", root, platform, True)
        browser = setup_tools.plan_tool("agent-browser", root, platform, True, win_build=19045)
        self.assertIn("aarch64-pc-windows-msvc.tar.gz", desktop["url"])
        self.assertEqual(Path(desktop["command"]).name, "agent-desktop.exe")
        self.assertEqual(browser["status"], "use-host-tool-or-upstream-guide")

    def test_windows_11_arm_browser_uses_pinned_x64_under_emulation(self):
        root = Path("isolated")
        arm = setup_tools.plan_tool("agent-browser", root, ("Windows", "arm64"), True, win_build=22631)
        x64 = setup_tools.plan_tool("agent-browser", root, ("Windows", "x86_64"), True)
        self.assertEqual(arm["status"], "planned")
        self.assertEqual(arm["binary_route"], "windows-x64-emulation")
        self.assertEqual(arm["sha256"], x64["sha256"])
        self.assertEqual(arm["url"], x64["url"])

    def test_uses_existing_tool_without_installing(self):
        with patch.object(setup_tools.shutil, "which", return_value="existing/agent-browser"):
            plan = setup_tools.plan_tool("agent-browser", Path("isolated"), ("Darwin", "arm64"))
        self.assertEqual(plan["command"], "existing/agent-browser")
        self.assertEqual(plan["status"], "found-not-GUI-verified")

    def test_uses_installed_pinned_version_even_with_pinned_option(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "agent-browser/0.43.0/agent-browser"
            target.parent.mkdir(parents=True)
            target.touch()
            result = setup_tools.plan_tool("agent-browser", root, ("Darwin", "arm64"), True)
            self.assertEqual(result["command"], str(target))
            self.assertEqual(result["status"], "found-not-GUI-verified")

    def test_download_verifies_exact_bytes_and_rejects_bad_hash(self):
        sample = b"sample asset"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "asset"
            with patch.object(setup_tools, "urlopen", return_value=io.BytesIO(sample)):
                setup_tools.download_checked("https://example.invalid", hashlib.sha256(sample).hexdigest(), output)
            self.assertEqual(output.read_bytes(), sample)
            with patch.object(setup_tools, "urlopen", return_value=io.BytesIO(sample)):
                with self.assertRaisesRegex(ValueError, "SHA-256"):
                    setup_tools.download_checked("https://example.invalid", "0" * 64, output.with_name("bad"))

    def test_unpacks_only_the_cli_and_macos_helper(self):
        names = ["agent-desktop", "agent-desktop-macos-helper"]
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            archive = base / "desktop.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                for name in names:
                    entry = tarfile.TarInfo(name)
                    entry.size = len(name)
                    tar.addfile(entry, io.BytesIO(name.encode()))
            output = base / "out"
            output.mkdir()
            with self.assertRaisesRegex(ValueError, "Unexpected"):
                setup_tools.unpack(archive, output, names[:1])
            self.assertEqual(list(output.iterdir()), [])
            setup_tools.unpack(archive, output, names)
            self.assertEqual({p.name: p.read_text() for p in output.iterdir()}, {n:n for n in names})
