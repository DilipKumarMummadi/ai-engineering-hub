import os
import subprocess
import unittest
from pathlib import Path

from .helpers import make_repo

LAUNCHER = Path(__file__).resolve().parent.parent / "project-context"


class TestLauncher(unittest.TestCase):
    def run_launcher(self, *args, cwd=None):
        return subprocess.run([str(LAUNCHER), *args], capture_output=True, text=True, cwd=cwd)

    def test_launcher_is_executable_and_prints_version(self):
        self.assertTrue(os.access(LAUNCHER, os.X_OK))
        r = self.run_launcher("--version")
        self.assertEqual(r.returncode, 0)
        self.assertIn("project-context", r.stdout)

    def test_generate_from_current_directory_and_update(self):
        root = make_repo({"package.json": '{"name":"x","scripts":{"test":"jest"}}', "README.md": "A tiny demo project for the launcher test.\n"})
        r = self.run_launcher("generate", cwd=root)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((root / "PROJECT-CONTEXT.md").is_file())
        r = self.run_launcher("update", cwd=root)
        self.assertEqual(r.returncode, 0)
        self.assertIn("No material project context changes detected.", r.stdout)

    def test_usage_errors_use_exit_code_2(self):
        self.assertEqual(self.run_launcher("generate", "--repo", "/definitely/not/here").returncode, 2)
        self.assertEqual(self.run_launcher("frobnicate").returncode, 2)

    def test_dry_run_writes_nothing(self):
        root = make_repo({"go.mod": "module x\ngo 1.22\n"})
        r = self.run_launcher("generate", "--repo", str(root), "--dry-run")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((root / "PROJECT-CONTEXT.md").exists())
        self.assertFalse(list(root.rglob("*.tmp")))
