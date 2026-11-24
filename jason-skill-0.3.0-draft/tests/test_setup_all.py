from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills/jason-skill/scripts"))
import setup_all


class SetupAllTests(unittest.TestCase):
    def test_preview_with_all_options_does_not_install_anything(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            args = SimpleNamespace(apply=False, tool_root=base/"tools", pinned=True,
                                   include_cua=True, cua_target=base/"CuaDriver.app",
                                   browser_runtime=True)
            with patch.object(setup_all.setup_tools, "platform_key", return_value=("Darwin", "x86_64")), \
                    patch.object(setup_all.setup_tools, "download_checked") as download, \
                    patch.object(setup_all.subprocess, "run") as run:
                result = setup_all.run_setup(args)
            download.assert_not_called()
            run.assert_not_called()
            self.assertEqual(result["browser_runtime"]["status"], "planned")
            self.assertEqual(result["cua"]["status"], "planned")
            self.assertFalse(result["gui_verified"])
            self.assertEqual(list(base.iterdir()), [])

    def test_unavailable_browser_reported_without_running_install(self):
        args = SimpleNamespace(apply=True, tool_root=Path("unused"), pinned=True,
                               include_cua=True, cua_target=Path("unused.app"),
                               browser_runtime=True)
        with patch.object(setup_all.setup_tools, "platform_key", return_value=("Windows", "arm64")), \
                patch.object(setup_all.setup_tools, "resolve_tools", return_value=[
                    {"tool":"agent-browser", "status":"use-host-tool-or-upstream-guide"},
                    {"tool":"agent-desktop", "status":"found-not-GUI-verified"}]), \
                patch.object(setup_all.subprocess, "run") as run, \
                patch.object(setup_all.setup_windows, "install", side_effect=OSError("mock download failure")) as cua_install:
            result = setup_all.run_setup(args)
        run.assert_not_called()
        cua_install.assert_called_once()
        self.assertEqual(result["browser_runtime"]["status"], "failed")
        self.assertEqual(result["cua"]["status"], "failed")
