"""Local Git lifecycle replay. No network, CI command, or production mutation."""
import subprocess
import tempfile
import unittest
from pathlib import Path


class ReleaseAncestryTests(unittest.TestCase):
    def test_merge_is_not_release_and_patch_equivalence_is_not_ancestry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
            git('init', '-b', 'main')
            git('config', 'commit.gpgsign', 'false')
            git('config', 'tag.gpgsign', 'false')
            git('config', 'user.name', 'Synthetic experiment')
            git('config', 'user.email', 'synthetic@example.invalid')
            (root/'base').write_text('base\n')
            git('add', 'base'); git('commit', '-m', 'Synthetic baseline')
            git('tag', 'v0.0.1-demo')
            git('switch', '-c', 'feature')
            (root/'feature').write_text('synthetic feature\n')
            git('add', 'feature'); git('commit', '-m', 'Synthetic feature')
            feature = git('rev-parse', 'HEAD')
            git('switch', 'main'); git('merge', '--no-ff', 'feature', '-m', 'Synthetic merge')
            merged = git('rev-parse', 'HEAD')
            def contained(commit, ref):
                return subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',commit,ref],capture_output=True).returncode == 0
            self.assertFalse(contained(merged, 'v0.0.1-demo'))
            git('tag', 'v0.0.2-demo')
            self.assertTrue(contained(merged, 'v0.0.2-demo'))
            git('switch', '-c', 'backport', 'v0.0.1-demo')
            git('cherry-pick', feature)
            git('tag', 'v0.0.1-patch-demo')
            self.assertTrue((root/'feature').exists())
            self.assertFalse(contained(merged, 'v0.0.1-patch-demo'))
