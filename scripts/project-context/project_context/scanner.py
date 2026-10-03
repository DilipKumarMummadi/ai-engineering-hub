"""Repository Scanner: indexes which files exist and which may be read.

The scanner never reads file content while indexing. It records excluded directories and skipped
files so a dry run can show what was and was not considered. Sensitive files are indexed (their
existence may be reported) but `Repo.read` refuses to return their content.
"""
from __future__ import annotations

import os
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .config import DEFAULT_EXCLUDED_DIRS, Config, glob_to_regex
from .secrets import is_sensitive_path

BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".svgz", ".pdf", ".zip", ".gz", ".tar", ".tgz",
    ".7z", ".rar", ".jar", ".war", ".dll", ".exe", ".so", ".dylib", ".class", ".o", ".a", ".pyc", ".woff",
    ".woff2", ".ttf", ".eot", ".mp3", ".mp4", ".mov", ".avi", ".bin", ".dat", ".db", ".sqlite", ".nupkg",
    ".map", ".lockb",
}
# Build-output directories that are only excluded next to the manifest that produces them.
_TARGET_PARENT_MARKERS = {"pom.xml", "Cargo.toml", "build.gradle", "build.gradle.kts"}


@dataclass
class FileEntry:
    rel: str
    size: int
    sensitive: bool
    binary: bool
    too_large: bool


class Repo:
    def __init__(self, root: Path, config: Config):
        self.root = root
        self.config = config
        self.files: dict[str, FileEntry] = {}
        self.dirs: set[str] = set()
        self.excluded_dirs: Counter = Counter()
        self.skipped_binary = 0
        self.skipped_large = 0
        self.read_log: set[str] = set()
        self.facts: dict = {}  # shared between detectors
        self.findings: list = []  # list[Finding]
        self._by_name: dict[str, list] = {}
        self._excl_res = [glob_to_regex(p) for p in config.excluded]
        self._incl_res = [glob_to_regex(p) for p in config.included]
        self._sens_res = [glob_to_regex(p) for p in config.sensitive]

    # ---- indexing -------------------------------------------------------------------------
    def scan(self) -> "Repo":
        for dirpath, dirnames, filenames in os.walk(self.root, followlinks=False):
            rel_dir = Path(dirpath).relative_to(self.root).as_posix()
            rel_dir = "" if rel_dir == "." else rel_dir
            depth = 0 if not rel_dir else rel_dir.count("/") + 1
            keep = []
            for d in sorted(dirnames):
                rel = f"{rel_dir}/{d}" if rel_dir else d
                if self._dir_excluded(d, rel, filenames):
                    self.excluded_dirs[d] += 1
                    continue
                if self.config.max_depth and depth >= self.config.max_depth:
                    continue
                if os.path.islink(os.path.join(dirpath, d)):
                    continue
                keep.append(d)
                self.dirs.add(rel)
            dirnames[:] = keep
            for f in sorted(filenames):
                rel = f"{rel_dir}/{f}" if rel_dir else f
                full = os.path.join(dirpath, f)
                if os.path.islink(full):
                    continue
                if self._excluded_by_config(rel) or not self._included(rel):
                    continue
                try:
                    size = os.path.getsize(full)
                except OSError:
                    continue
                binary = PurePosixPath(f).suffix.lower() in BINARY_EXTS
                sensitive = is_sensitive_path(rel) or any(r.match(rel) for r in self._sens_res)
                too_large = size > self.config.max_read_bytes
                if binary:
                    self.skipped_binary += 1
                if too_large and not binary:
                    self.skipped_large += 1
                self.files[rel] = FileEntry(rel, size, sensitive, binary, too_large)
                self._by_name.setdefault(f.lower(), []).append(rel)
        return self

    def _dir_excluded(self, name: str, rel: str, siblings) -> bool:
        if name in DEFAULT_EXCLUDED_DIRS:
            return True
        if name == "target" and any(m in siblings for m in _TARGET_PARENT_MARKERS):
            return True
        return self._excluded_by_config(rel) or self._excluded_by_config(rel + "/x")

    def _excluded_by_config(self, rel: str) -> bool:
        return any(r.match(rel) for r in self._excl_res)

    def _included(self, rel: str) -> bool:
        return not self._incl_res or any(r.match(rel) for r in self._incl_res)

    # ---- queries --------------------------------------------------------------------------
    def exists(self, rel: str) -> bool:
        return rel in self.files or rel in self.dirs

    def named(self, *names: str) -> list:
        out = []
        for n in names:
            out += self._by_name.get(n.lower(), [])
        return sorted(set(out))

    def find(self, pattern: str) -> list:
        rx = glob_to_regex(pattern)
        return sorted(r for r in self.files if rx.match(r))

    def with_suffix(self, *suffixes: str) -> list:
        sfx = tuple(s.lower() for s in suffixes)
        return sorted(r for r in self.files if r.lower().endswith(sfx))

    def dirs_named(self, *names: str) -> list:
        lower = {n.lower() for n in names}
        return sorted(d for d in self.dirs if d.rsplit("/", 1)[-1].lower() in lower)

    def in_dir(self, directory: str):
        prefix = directory.rstrip("/") + "/" if directory else ""
        return sorted(r for r in self.files if r.startswith(prefix))

    # ---- reading --------------------------------------------------------------------------
    def read(self, rel: str, limit: int | None = None) -> str | None:
        """Read a non-sensitive text file. Returns None for sensitive, binary, missing or oversized files."""
        e = self.files.get(rel)
        if e is None or e.sensitive or e.binary or e.too_large:
            return None
        try:
            with open(self.root / rel, "rb") as fh:
                data = fh.read(limit or self.config.max_read_bytes)
        except OSError:
            return None
        if b"\x00" in data[:4096]:
            return None
        self.read_log.add(rel)
        return data.decode("utf-8", errors="replace")
