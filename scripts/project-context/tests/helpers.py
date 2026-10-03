"""Fixture helpers: build throwaway repositories and run the CLI in-process."""
from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from project_context.cli import main

DATE = "2026-01-15"


def make_repo(files: dict) -> Path:
    root = Path(tempfile.mkdtemp(prefix="pcg-test-")) / "fixture-repo"
    root.mkdir()
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content, encoding="utf-8")
    return root


def run(*argv):
    """Run the CLI. Returns (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class RepoTestCase(unittest.TestCase):
    def generate(self, files: dict, *extra):
        self.root = make_repo(files)
        code, out, err = run("generate", "--repo", str(self.root), "--date", DATE, *extra)
        self.assertEqual(code, 0, msg=out + err)
        self.out, self.err = out, err
        return (self.root / "PROJECT-CONTEXT.md").read_text(encoding="utf-8")

    def assertEntry(self, text, fragment, cls):
        for line in text.splitlines():
            if fragment in line and line.startswith("- "):
                self.assertTrue(line.endswith(f"\u2014 {cls}"), msg=f"'{fragment}' is not {cls}: {line}")
                return
        self.fail(f"no entry containing '{fragment}'")

    def assertNoEntry(self, text, fragment):
        for line in text.splitlines():
            if fragment in line and line.startswith("- "):
                self.fail(f"unexpected entry: {line}")
