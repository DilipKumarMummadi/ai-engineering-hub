"""Test directories, test files and test configuration. Frameworks come from the manifest detectors."""
from __future__ import annotations

import re

from ..model import confirmed, inferred

_TEST_DIRS = ("test", "tests", "__tests__", "spec", "specs", "e2e")
_CONFIGS = (
    "jest.config.*", "vitest.config.*", "playwright.config.*", "cypress.config.*", "karma.conf.*", ".mocharc*",
    "pytest.ini", "tox.ini", "conftest.py", "codecov.yml", ".coveragerc", "coverlet.runsettings", "*.runsettings",
)
_FILE_PATTERNS = (
    r".+\.(test|spec)\.[jt]sx?$", r".+_test\.go$", r"test_.+\.py$", r".+_test\.py$", r".+Tests?\.cs$", r".+Tests?\.java$",
)


def detect(repo):
    items = []
    dirs = [d for d in repo.dirs_named(*_TEST_DIRS) if repo.in_dir(d)]
    if dirs:
        # A name is only a name: this records the directories, not what their contents are.
        items.append(confirmed("Testing", f"Directories with test-style names (test, tests, spec, e2e): {', '.join(dirs[:10])}", *dirs[:10]))
    cfgs = sorted({p for g in _CONFIGS for p in repo.find(f"**/{g}") + repo.find(g)})
    if cfgs:
        items.append(confirmed("Testing", f"Test configuration files: {', '.join(cfgs[:8])}", *cfgs[:8]))
    rx = [re.compile(p) for p in _FILE_PATTERNS]
    test_files = [p for p in repo.files if any(r.match(p.rsplit("/", 1)[-1]) for r in rx)]
    if test_files:
        top = sorted({(p.rsplit("/", 1)[0] if "/" in p else ".") for p in test_files})
        items.append(confirmed("Testing", f"Test files found in: {', '.join(top[:8])}", *test_files[:5]))
    e2e_cfg = [c for c in cfgs if "playwright.config" in c or "cypress.config" in c]
    if e2e_cfg:
        items.append(inferred("Testing", "Browser end-to-end tests appear to be set up (E2E tool configuration present)", *e2e_cfg[:3]))
    return items
