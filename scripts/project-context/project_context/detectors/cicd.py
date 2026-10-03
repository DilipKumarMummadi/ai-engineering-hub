"""CI/CD definitions. GitHub Actions is parsed in detail; other systems are recorded by existence."""
from __future__ import annotations

import re

from ..catalog import CI_DIRS, CI_FILES, DEPLOY_HINTS
from ..model import confirmed, inferred, unknown
from ..secrets import find_secrets, scrub
from .common import add_command

_MAX_CMDS = 25


def _parse_workflow(text: str):
    name = (re.search(r"(?m)^name:[ \t]*(.+?)[ \t]*$", text) or [None, ""])[1].strip("'\"")
    triggers = []
    m = re.search(r"(?m)^on:[ \t]*(.*)$", text)
    if m:
        inline = m.group(1).strip()
        if inline:
            triggers = re.findall(r"[a-z_]+", inline.strip("[]{}"))
        else:
            for line in text[m.end():].splitlines()[1:]:
                if line and not line.startswith(" "):
                    break
                k = re.match(r"^ {2}([a-z_]+):", line)
                if k:
                    triggers.append(k.group(1))
    jobs = []
    jm = re.search(r"(?m)^jobs:\s*$", text)
    if jm:
        for line in text[jm.end():].splitlines()[1:]:
            if line and not line.startswith(" "):
                break
            k = re.match(r"^ {2}([\w\-]+):\s*$", line)
            if k:
                jobs.append(k.group(1))
    runs = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)-?\s*run:\s*(.*)$", line)
        if not m:
            continue
        rest = m.group(2).strip()
        if rest in ("|", ">", "|-", ">-", "|+"):
            base = len(m.group(1))
            for nxt in lines[i + 1:]:
                if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= base:
                    break
                c = nxt.strip()
                if c and not c.startswith("#"):
                    runs.append(c)
        elif rest:
            runs.append(rest.strip("'\""))
    uses = sorted(set(re.sub(r"@.*$", "", u) for u in re.findall(r"(?m)^\s*-?\s*uses:\s*(\S+)", text)))
    envs = sorted(set(re.findall(r"(?m)^\s*environment:\s*([\w\-]+)\s*$", text)) | set(re.findall(r"(?m)^\s{6,}name:\s*(production|staging|prod|dev|test|qa|uat)\s*$", text)))
    return name, triggers, jobs, runs, uses, envs, bool(re.search(r"secrets\.\w+", text))


def detect(repo):
    items = []
    wfs = sorted(p for p in repo.files if re.match(r"^\.github/workflows/[^/]+\.ya?ml$", p))
    have_ci, deploy_seen, n_cmds = False, False, 0
    if wfs:
        have_ci = True
        items.append(confirmed("CI/CD", f"GitHub Actions workflows: {', '.join(w.rsplit('/', 1)[-1] for w in wfs[:10])}", *wfs[:10]))
        for wf in wfs[:10]:
            text = repo.read(wf)
            if text is None:
                continue
            name, triggers, jobs, runs, uses, envs, secrets = _parse_workflow(text)
            fname = wf.rsplit("/", 1)[-1]
            detail = []
            if triggers:
                detail.append("triggers " + ", ".join(sorted(set(triggers))))
            if jobs:
                detail.append("jobs " + ", ".join(jobs[:8]))
            items.append(confirmed("CI/CD", f"Workflow {fname}: " + ("; ".join(detail) or "defined"), wf))
            blob = "\n".join(runs + uses).lower()
            if "docker build" in blob or "docker/build-push-action" in blob:
                items.append(confirmed("CI/CD", f"Workflow {fname}: builds a container image", wf))
            hits = sorted({h.strip() for h in DEPLOY_HINTS if h in blob})
            if hits:
                deploy_seen = True
                items.append(inferred("CI/CD", f"Workflow {fname}: appears to include deployment or publish steps (matched: {', '.join(hits)})", wf))
            if envs:
                items.append(confirmed("CI/CD", f"Workflow {fname}: environments referenced: {', '.join(envs)}", wf))
            if secrets:
                items.append(confirmed("CI/CD", f"Workflow {fname}: references repository secrets (names not recorded)", wf))
            if any(u.startswith("github/codeql-action") for u in uses):
                items.append(confirmed("Security", f"Workflow {fname}: runs CodeQL analysis", wf))
            for c in runs:
                if n_cmds >= _MAX_CMDS:
                    break
                if find_secrets(c) or "${{" in c and "secrets" in c:
                    continue
                add_command(repo, f"CI step in {fname} runs `{scrub(c)[:100]}`", "", wf)
                n_cmds += 1
    for name, label in CI_FILES.items():
        for p in repo.named(name):
            have_ci = True
            items.append(confirmed("CI/CD", f"{label} pipeline definition present ({p}); contents not analysed", p))
    for d, label in CI_DIRS.items():
        if d in repo.dirs:
            have_ci = True
            items.append(confirmed("CI/CD", f"{label} configuration directory present ({d}); contents not analysed", d))
    if have_ci and not deploy_seen:
        items.append(unknown("CI/CD", "deployment mechanism not found in analysed pipeline definitions"))
    if not have_ci:
        items.append(unknown("CI/CD", "no CI/CD definition found in inspected paths"))
    for p in repo.named("dependabot.yml", "dependabot.yaml", "renovate.json", ".renovaterc", ".renovaterc.json"):
        items.append(confirmed("Development Workflow", f"Dependency update automation configured ({p})", p))
    return items
