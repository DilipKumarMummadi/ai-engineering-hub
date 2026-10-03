"""Structural reading of configuration files: key names only, never values.

Values are inspected in memory only to tell a placeholder from a real-looking credential. The
result holds key paths and a status, so a secret cannot leak through this module's output.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

from .secrets import is_sensitive_key, looks_placeholder


@dataclass(frozen=True)
class Key:
    path: str          # dotted key path
    sensitive: bool    # the key name indicates a credential
    has_value: bool    # a non-placeholder value is present (value itself is not kept)


def _walk_json(obj, prefix, out, is_example):
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, (dict, list)):
                _walk_json(v, path, out, is_example)
            else:
                sens = is_sensitive_key(path)
                out.append(Key(path, sens, sens and not is_example and _real(v)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:20]):
            _walk_json(v, f"{prefix}[{i}]", out, is_example)


def _real(v) -> bool:
    return isinstance(v, str) and not looks_placeholder(v) or isinstance(v, (int, float)) and not isinstance(v, bool)


_LINE = re.compile(r"^(\s*)(?:export\s+)?([A-Za-z_][\w.\-]*)\s*[:=]\s*(.*?)\s*$")


def _walk_lines(text, is_example):
    """Keys from .env / .properties / .ini / simple YAML, with indentation-based nesting for YAML."""
    out, stack = [], []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith(("#", ";", "//", "- ", "[")):
            continue
        m = _LINE.match(raw)
        if not m:
            continue
        indent, name, value = len(m.group(1)), m.group(2), m.group(3)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        path = ".".join([s[1] for s in stack] + [name])
        if value == "" or value in ("|", ">"):
            stack.append((indent, name))
            if value == "":
                continue
        sens = is_sensitive_key(path)
        out.append(Key(path, sens, sens and not is_example and not looks_placeholder(value)))
    return out


def extract_keys(text: str, rel: str, is_example: bool = False):
    """Return [Key] for a config file. JSON is parsed; other formats are read line by line."""
    if rel.lower().endswith(".json"):
        try:
            data = json.loads(re.sub(r"^﻿", "", text))
        except ValueError:
            data = None
        if data is not None:
            out = []
            _walk_json(data, "", out, is_example)
            return out
    return _walk_lines(text, is_example)
