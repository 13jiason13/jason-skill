import io
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills/jason-skill/scripts"))
import setup_windows


class WindowsCuaTests(unittest.TestCase):
    def test_preview_selects_native_asset_and_never_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for arch in ("arm64", "x86_64"):
                item = setup_windows.plan(arch, root/"new", pinned=True)
                self.assertIn(f"windows-{arch}-binary.zip", item["url"])
                self.assertEqual(Path(item["command"]).name, "cua-driver.exe")
            self.assertEqual(list(root.iterdir()), [])

    def test_extracts_only_the_expected_binary(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            archive = base / "release.zip"
            with zipfile.ZipFile(archive, "w") as package:
                package.writestr("release/cua-driver.exe", b"test-binary")
                package.writestr("release/LICENSE", b"test-license")
            binary = base / "cua-driver.exe"
            setup_windows.extract_executable(archive, binary)
            self.assertEqual(binary.read_bytes(), b"test-binary")
            self.assertFalse((base/"LICENSE").exists())

    def test_rejects_escape_duplicate_and_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            for mode in ["escape", "duplicate", "symlink"]:
                archive = base / f"{mode}.zip"
                with zipfile.ZipFile(archive, "w") as package:
                    package.writestr("release/cua-driver.exe", b"test-binary")
                    if mode == "symlink":
                        item = zipfile.ZipInfo("symlink")
                        item.create_system = 3
                        item.external_attr = (stat.S_IFLNK | 0o777) << 16
                        package.writestr(item, "release/cua-driver.exe")
                    else:
                        package.writestr("../evil.exe" if mode == "escape" else "copy/CUA-DRIVER.EXE", b"bad")
                with self.assertRaises(ValueError):
                    setup_windows.extract_executable(archive, base/"output.exe")
                self.assertFalse((base/"output.exe").exists())
