"""Secret protection. Nothing in this module ever returns or stores a secret value.

`find_secrets` reports (pattern name, line number) only. `scrub` replaces matches with a fixed
marker. All terminal output and all generated text pass through these functions.
"""
from __future__ import annotations

import math
import re
from pathlib import PurePosixPath

REDACTED = "[REDACTED]"

_PATTERNS = [
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS-style access key id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("payment provider key", re.compile(r"\b[sr]k_(?:live|test)_[A-Za-z0-9]{8,}\b|\bpk_(?:live|test)_[A-Za-z0-9_]{8,}\b")),
    ("JSON web token", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]*")),
    ("URL with embedded credentials", re.compile(r"[A-Za-z][A-Za-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@")),
    (
        "credential in connection string",
        re.compile(r"(?i)\b(?:password|pwd|accountkey|sharedaccesskey|sharedaccesssignature)\s*=\s*[^;\s'\"]{3,}"),
    ),
    (
        "credential assignment",
        re.compile(
            r"(?i)\b[\w.-]*(?:password|passwd|secret|token|api[_-]?key|private[_-]?key|signing[_-]?key|access[_-]?key)"
            r"[\w.-]*\s*[:=]\s*['\"]?(?!\s*(?:\[REDACTED\]|<|\$\{|\{\{|%|null\b|none\b|true\b|false\b))[^\s'\";,)]{6,}"
        ),
    ),
]

_TOKEN = re.compile(r"[A-Za-z0-9+/=_-]{32,}")

# Key names whose values must never be read into memory beyond a placeholder test.
SENSITIVE_KEY = re.compile(
    r"(?i)(password|passwd|pwd|secret|token|api[_-]?key|private[_-]?key|signing[_-]?key|credential|"
    r"connection[_-]?string|access[_-]?key|account[_-]?key|shared[_-]?access|cookie|\bsas\b)"
)

_PLACEHOLDER_WORDS = {
    "", "changeme", "change-me", "change_me", "password", "secret", "xxx", "xxxx", "todo", "tbd",
    "example", "your-key", "your_key", "null", "none", "placeholder", "***", "...",
}


def _entropy(s: str) -> float:
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    return -sum(c / n * math.log2(c / n) for c in counts.values())


def _high_entropy_tokens(line: str):
    for m in _TOKEN.finditer(line):
        tok = m.group(0)
        if "/" in tok and not tok.endswith("="):
            continue  # looks like a path
        if not (any(c.isdigit() for c in tok) and any(c.isalpha() for c in tok)):
            continue
        if _entropy(tok) >= 4.3:
            yield m


def find_secrets(text: str):
    """Return [(pattern name, line number)] for secret-like content. Never returns the matched text."""
    found = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, pat in _PATTERNS:
            if pat.search(line):
                found.append((name, lineno))
        if any(True for _ in _high_entropy_tokens(line)):
            found.append(("high-entropy token", lineno))
    return found


def scrub(text: str) -> str:
    """Replace secret-like content with a fixed marker."""
    out = text
    for _, pat in _PATTERNS:
        out = pat.sub(REDACTED, out)
    out = _TOKEN.sub(lambda m: REDACTED if _is_entropy_token(m.group(0)) else m.group(0), out)
    return out


def _is_entropy_token(tok: str) -> bool:
    if "/" in tok and not tok.endswith("="):
        return False
    return any(c.isdigit() for c in tok) and any(c.isalpha() for c in tok) and _entropy(tok) >= 4.3


def is_sensitive_key(name: str) -> bool:
    return bool(SENSITIVE_KEY.search(name))


def looks_placeholder(value: str) -> bool:
    """True if a config value is empty, an interpolation, or an obvious placeholder. Value is not retained."""
    v = value.strip().strip("'\"").strip()
    if v.lower() in _PLACEHOLDER_WORDS:
        return True
    if v.startswith(("<", "${", "{{", "%", "$(", "env(", "@")):
        return True
    low = v.lower()
    if "your_" in low or "your-" in low or "placeholder" in low or low.startswith("example"):
        return True
    return False


_EXAMPLE_SUFFIXES = (".example", ".sample", ".template", ".dist", ".tmpl")
_SENSITIVE_EXTS = {".pem", ".key", ".pfx", ".p12", ".jks", ".keystore", ".tfstate", ".kdbx", ".ppk"}
_SENSITIVE_NAMES = {
    "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", ".npmrc", ".pypirc", ".netrc", ".htpasswd", "kubeconfig",
    "credentials", "credentials.json", "secrets.json", "secret.json", "secrets.yaml", "secrets.yml",
    ".git-credentials", "terraform.tfvars",
}


def is_example_name(name: str) -> bool:
    return name.lower().endswith(_EXAMPLE_SUFFIXES)


def is_sensitive_path(rel: str) -> bool:
    """Files whose content is never read. Existence may be recorded."""
    p = PurePosixPath(rel)
    name = p.name.lower()
    if is_example_name(name):
        return False
    if name == ".env" or name.startswith(".env."):
        return True
    if name in _SENSITIVE_NAMES:
        return True
    if p.suffix.lower() in _SENSITIVE_EXTS:
        return True
    if name.endswith((".tfvars", ".tfvars.json")):
        return True
    if name.startswith("service-account") and name.endswith(".json"):
        return True
    if "secret" in name and p.suffix.lower() in {".json", ".yaml", ".yml", ".env", ".properties", ".ini"}:
        return True
    return False
