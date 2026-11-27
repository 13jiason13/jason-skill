import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
import install_bundle as installer
import build_bundle


class DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle=build_bundle.build()

    def alter(self, folder, transform):
        text=self.bundle.read_text(encoding='utf-8')
        match=re.search(r'(?m)^```json jason-skill-bundle\n([\s\S]*?)^```',text)
        payload=json.loads(match.group(1));transform(payload)
        text=text[:match.start(1)]+json.dumps(payload,ensure_ascii=False)+'\n'+text[match.end(1):]
        path=Path(folder)/'changed.txt';path.write_text(text,encoding='utf-8')
        return path

    def test_single_file_contains_exactly_the_expected_files(self):
        self.assertEqual(set(installer.load_bundle(self.bundle)['files']),installer.ALLOWED)

    def test_install_and_repeat_install_in_temporary_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'skills';result=installer.install(self.bundle,root,with_required_tools=False)
            self.assertTrue(result['skill_files_installed'])
            self.assertIn(result['status'], {'installed', 'skill-installed-required-tools-incomplete'})
            self.assertEqual(result['install_complete'], result['required_tools_complete'])
            again=installer.install(self.bundle,root,with_required_tools=False)
            self.assertIn(again['status'], {'already-installed', 'already-installed-required-tools-incomplete'})
            self.assertEqual(again['status']=='already-installed', again['install_complete'])
            for name,item in installer.load_bundle(self.bundle)['files'].items():
                self.assertEqual((root/installer.NAME/name).read_bytes(),item['text'].encode('utf-8'))

    def test_existing_skill_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'skills';target=root/installer.NAME;target.mkdir(parents=True)
            (target/'SKILL.md').write_text('original')
            with self.assertRaises(FileExistsError):installer.install(self.bundle,root)
            self.assertEqual((target/'SKILL.md').read_text(),'original')

    def test_replace_keeps_backup_outside_skill_scan_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'skills';target=root/installer.NAME;target.mkdir(parents=True)
            (target/'SKILL.md').write_text('original')
            result=installer.install(self.bundle,root,replace=True,with_required_tools=False)
            backup=Path(result['backup'])
            self.assertEqual((backup/'SKILL.md').read_text(),'original')
            self.assertNotEqual(backup.parent,root)
            self.assertTrue((target/'scripts/doctor.py').exists())

    def test_failed_commit_restores_original_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'skills';target=root/installer.NAME;target.mkdir(parents=True)
            (target/'SKILL.md').write_text('original')
            rename=installer.os.rename
            def fail_staging(source,destination):
                if Path(source).name.startswith('.desktop-control-stage-'):raise OSError('test failure')
                return rename(source,destination)
            with patch.object(installer.os,'rename',side_effect=fail_staging):
                with self.assertRaises(OSError):installer.install(self.bundle,root,replace=True)
            self.assertEqual((target/'SKILL.md').read_text(),'original')

    def test_corrupted_content_is_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            def corrupt(p):p['files']['SKILL.md']['text']+='altered'
            bundle=self.alter(folder,corrupt);root=Path(folder)/'skills'
            with self.assertRaisesRegex(ValueError,'Checksum'):installer.install(bundle,root)
            self.assertFalse(root.exists())

    def test_extra_or_traversal_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            def extra(p):p['files']['../outside.txt']={'text':'bad','sha256':hashlib.sha256(b'bad').hexdigest()}
            with self.assertRaises(ValueError):installer.install(self.alter(folder,extra),Path(folder)/'skills')
            self.assertFalse((Path(folder)/'outside.txt').exists())

    def test_symlink_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'skills';root.mkdir();other=Path(folder)/'other';other.mkdir()
            try:(root/installer.NAME).symlink_to(other,target_is_directory=True)
            except (OSError,NotImplementedError):self.skipTest('symlinks unavailable')
            with self.assertRaisesRegex(ValueError,'symlink'):installer.install(self.bundle,root,True)
            self.assertEqual(list(other.iterdir()),[])

    def test_crlf_forwarded_file_is_readable(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'forwarded.txt'
            path.write_bytes(b'\xef\xbb\xbf'+self.bundle.read_bytes().replace(b'\n',b'\r\n'))
            self.assertEqual(installer.load_bundle(path)['name'],installer.NAME)

    def test_embedded_installer_really_installs_offline(self):
        text=self.bundle.read_text(encoding='utf-8')
        code=re.search(r'(?m)^```python\n([\s\S]*?)^```',text).group(1)
        self.assertEqual(code,(ROOT/'tools/install_bundle.py').read_text())
        with tempfile.TemporaryDirectory() as folder:
            script=Path(folder)/'installer.py';script.write_text(code,encoding='utf-8')
            root=Path(folder)/'skills'
            result=subprocess.run([sys.executable,str(script),str(self.bundle),'--skills-root',str(root),'--skill-files-only'],capture_output=True,text=True,timeout=10)
            self.assertIn(result.returncode, (0, 2), result.stderr)
            self.assertTrue((root/installer.NAME/'SKILL.md').exists())
            payload=json.loads(result.stdout)
            self.assertTrue(payload['skill_files_installed'])
            self.assertEqual(result.returncode==0, payload['install_complete'])

    def test_doctor_is_read_only_and_has_structured_output(self):
        script=ROOT/'skills/jason-skill/scripts/doctor.py'
        result=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout)
        self.assertEqual(set(data['commands']),{'python3','agent-desktop','agent-browser','cua-driver'})
        self.assertIn('installed', data['states'])
        self.assertEqual(data['states']['connected'], 'host-must-confirm')
        self.assertIn('permissions_granted', data['states'])
        self.assertFalse(data['states']['acceptance_passed'])
        self.assertIn('required_tools_complete', data)
        self.assertIn('agent-desktop', data['required_tools'])
        self.assertIn('agent-browser', data['required_tools'])
        self.assertFalse(data['optional_cua']['required'])
        self.assertIn('next_command', data)

    def test_installer_header_requires_tools_and_acceptance(self):
        text=self.bundle.read_text(encoding='utf-8')
        self.assertIn('Attaching or registering the skill files only is incomplete', text)
        self.assertIn('run acceptance', text.lower())
        self.assertIn('--with-required-tools', text)
        self.assertIn('--skill-files-only', text)
        self.assertIn('SHA-256', text)
        self.assertIn('does not run this installer', text)


if __name__=='__main__':unittest.main()
