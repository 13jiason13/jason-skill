import importlib.util
import io
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'skills/jason-skill/scripts'))
import doctor
import setup_macos

class PortableSetupTests(unittest.TestCase):
 def test_native_and_rosetta_architecture(self):
  self.assertEqual(doctor.mac_arch('x86_64',False),'x86_64')
  self.assertEqual(doctor.mac_arch('arm64',True),'arm64')
  self.assertEqual(doctor.mac_arch('x86_64',True),'arm64')
 def test_only_supported_architectures_have_downloads(self):
  self.assertIn('darwin-arm64',setup_macos.asset_for('arm64'))
  self.assertIn('darwin-x86_64',setup_macos.asset_for('x86_64'))
  with self.assertRaises(ValueError):setup_macos.asset_for('unknown')
 def test_archive_traversal_rejected_without_outside_write(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);archive=p/'bad.tar.gz'
   with tarfile.open(archive,'w:gz') as t:
    info=tarfile.TarInfo('../outside');info.size=3;t.addfile(info,io.BytesIO(b'bad'))
   with self.assertRaises(ValueError):setup_macos.extract_checked(archive,p/'target')
   self.assertFalse((p/'outside').exists())
 def test_archive_symlinks_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);archive=p/'bad.tar.gz'
   with tarfile.open(archive,'w:gz') as t:
    info=tarfile.TarInfo('link');info.type=tarfile.SYMTYPE;info.linkname='/tmp';t.addfile(info)
   with self.assertRaises(ValueError):setup_macos.extract_checked(archive,p/'target')
 def test_existing_application_is_not_overwritten(self):
  with tempfile.TemporaryDirectory() as d:
   target=Path(d)/'CuaDriver.app';target.mkdir();(target/'keep').write_text('original')
   with self.assertRaises(FileExistsError):setup_macos.install('x86_64',target)
   self.assertEqual((target/'keep').read_text(),'original')

if __name__=='__main__':unittest.main()
