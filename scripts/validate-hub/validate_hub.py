#!/usr/bin/env python3
"""Structural validation of the AI Engineering Hub as one system. Standard library only, read-only.

Checks that the layers are wired together as the specifications say: commands route to one existing
agent, agents and workflows reference things that exist, project context is consumed through the
central standard and never copied into skills or commands, platform copies agree, and the
end-to-end scenarios and matrix describe routing the Hub can actually perform.

This proves structure. It does not prove how an assistant behaves. See docs/end-to-end-validation.md.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "project-context"))
from project_context.secrets import find_secrets  # noqa: E402

PLATFORMS = {
    "claude": {"agents": ".claude/agents", "commands": ".claude/commands", "cmd_suffix": ".md", "workflows": ".claude/workflows", "skills": ".claude/skills"},
    "github": {"agents": ".github/agents", "commands": ".github/prompts", "cmd_suffix": ".prompt.md", "workflows": ".github/workflows", "skills": ".github/skills"},
}
AGENT_SECTIONS = ["Purpose", "When to Use", "When NOT to Use", "Inputs", "Project Context", "Skills Used", "Process", "Decision Rules",
                  "Tool Usage", "Safety", "Output", "Handoff", "Examples", "Related Agents"]
WORKFLOW_SECTIONS = ["Purpose", "When to Use", "When NOT to Use", "Inputs", "Project Context", "Stages", "Commands", "Agents", "Skills",
                     "Decision Points", "Validation", "Safety", "Output", "Handoff", "Examples", "Related Workflows"]
CONSUMPTION = "project-context-consumption.md"
SCENARIO_SECTIONS = ["Scenario", "Input", "Expected Flow", "Actual Flow", "Skills Selected", "Context Used", "Evidence Used",
                     "Validation", "Safety Checks", "Result", "Findings", "Follow-up"]

errors: list = []
checked = {"commands": 0, "agents": 0, "workflows": 0, "skills": 0, "scenarios": 0, "links": 0}


def fail(where, msg):
    errors.append(f"{where}: {msg}")


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def headings(text, level="##"):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.findall(rf"(?m)^{level} (.+?)\s*$", text)


def section(text, title):
    m = re.search(rf"(?ms)^## {re.escape(title)}\s*$(.*?)(?=^## |\Z)", text)
    return m.group(1) if m else ""


def skills_of(agent_text):
    return re.findall(r"skills/([a-z-]+)/SKILL\.md", section(agent_text, "Skills Used"))


def check_skills():
    names = {p.name for p in (ROOT / ".claude/skills").iterdir() if p.is_dir()}
    if names != {p.name for p in (ROOT / ".github/skills").iterdir() if p.is_dir()}:
        fail("skills", "platform skill sets differ")
    for n in sorted(names):
        checked["skills"] += 1
        for plat in PLATFORMS.values():
            f = ROOT / plat["skills"] / n / "SKILL.md"
            if not f.is_file():
                fail(f"{plat['skills']}/{n}", "SKILL.md missing")
            elif re.search(r"(?i)project-context\.md|project context", f.read_text(encoding="utf-8")):
                fail(f"{plat['skills']}/{n}", "skills must stay generic and must not reference project context")
    return names


def check_agents(skills):
    agents = {}
    for p in sorted((ROOT / ".claude/agents").glob("*.md")):
        name = p.stem
        texts = {k: read(f"{v['agents']}/{name}.md") for k, v in PLATFORMS.items() if (ROOT / v["agents"] / f"{name}.md").is_file()}
        if len(texts) != 2:
            fail(f"agents/{name}", "missing on one platform")
            continue
        checked["agents"] += 1
        if texts["claude"] != texts["github"]:
            fail(f"agents/{name}", "platform copies differ")
        t = texts["claude"]
        if headings(t) != AGENT_SECTIONS:
            fail(f"agents/{name}", f"sections {headings(t)} != required order")
        pc = section(t, "Project Context")
        if CONSUMPTION not in pc:
            fail(f"agents/{name}", "Project Context section does not reference the consumption standard")
        if "Relevant sections:" not in pc:
            fail(f"agents/{name}", "Project Context section has no relevance list")
        if len(pc.splitlines()) > 20:
            fail(f"agents/{name}", "Project Context section is not lightweight (>20 lines)")
        if re.search(r"(?i)postgres|oracle|rabbit|kubernetes|react|\.net|asp\.net", pc):
            fail(f"agents/{name}", "Project Context section contains project-specific technology")
        sk = skills_of(t)
        for s in sk:
            if s not in skills:
                fail(f"agents/{name}", f"unknown skill {s}")
        if not sk:
            fail(f"agents/{name}", "no skills declared")
        agents[name] = sk
    return agents


ENTRY_VARIANTS = {"review-pr": "pr-intelligence"}  # a command that shares its base command's agent
TOOL_COMMANDS = {"context"}  # run a Hub tool instead of routing to an agent
TOOL_OPERATIONS = ("generate", "inspect", "drift")


def check_tool_command(plat, p, t):
    where = f"{plat['commands']}/{p.name}"
    if re.search(r"`[a-z-]+-agent`", t):
        fail(where, "a tool command must not route to an agent")
    if "scripts/project-context/project-context" not in t:
        fail(where, "must invoke the existing Project Context Generator launcher")
    for op in TOOL_OPERATIONS:
        if f"| `{op}` |" not in t:
            fail(where, f"missing operation {op}")
    for needle in ("git rev-parse --show-toplevel", "AI Engineering Hub itself", "does not authorize commits", "--repo <target root>", "Never reproduce a secret"):
        if needle not in t:
            fail(where, f"missing required rule: {needle}")
    if re.search(r"(?i)\bgenerator\b.*\b(reimplement|rewrite the generator)", t):
        fail(where, "must not reimplement the generator")


def check_commands(agents):
    routes = {}
    tool_headings = {}
    for key, plat in PLATFORMS.items():
        for p in sorted((ROOT / plat["commands"]).glob("*" + plat["cmd_suffix"])):
            checked["commands"] += 1
            t = p.read_text(encoding="utf-8")
            name = p.name[: -len(plat["cmd_suffix"])]
            if name in TOOL_COMMANDS:
                check_tool_command(plat, p, t)
                tool_headings.setdefault(name, {})[key] = re.findall(r"(?m)^#{1,3} .*$", t)
                continue
            named = sorted(set(re.findall(r"`([a-z-]+-agent)`", t)))
            if len(named) != 1 or named[0] not in agents:
                fail(f"{plat['commands']}/{p.name}", f"must route to exactly one existing agent, found {named}")
                continue
            if re.search(r"(?i)project[- ]context", t):
                fail(f"{plat['commands']}/{p.name}", "commands must not contain project context logic")
            if re.search(r"(?i)skills/|\bselect(s)? skills?\b.*:", t):
                fail(f"{plat['commands']}/{p.name}", "commands must not select skills")
            routes.setdefault(key, {})[p.name.replace(plat["cmd_suffix"], "")] = named[0]
    for name, by_plat in tool_headings.items():
        if len(by_plat) != 2 or by_plat["claude"] != by_plat["github"]:
            fail(f"commands/{name}", "tool command missing on a platform or structure differs between platforms")
    if routes.get("claude") != routes.get("github"):
        fail("commands", "platform routing differs")
    claude_routes = routes.get("claude", {})
    for variant, base in ENTRY_VARIANTS.items():
        if variant in claude_routes and claude_routes[variant] != claude_routes.get(base):
            fail(f"commands/{variant}", f"must route to the same agent as /{base}")
    independent = {n: a for n, a in claude_routes.items() if n not in ENTRY_VARIANTS}
    if len(set(independent.values())) != len(independent):
        fail("commands", "two commands route to the same agent")
    return routes.get("claude", {})


def check_workflows(agents, commands, skills):
    for p in sorted((ROOT / ".claude/workflows").glob("*.md")):
        name = p.stem
        texts = {k: read(f"{v['workflows']}/{name}.md") for k, v in PLATFORMS.items() if (ROOT / v["workflows"] / f"{name}.md").is_file()}
        if len(texts) != 2:
            fail(f"workflows/{name}", "missing on one platform")
            continue
        checked["workflows"] += 1
        norm = lambda s: re.sub(r"\]\(\.\./(prompts|commands)/[^)]*\)", "](cmd)", s)
        if norm(texts["claude"]) != norm(texts["github"]):
            fail(f"workflows/{name}", "platform copies differ beyond command links")
        t = texts["claude"]
        if headings(t) != WORKFLOW_SECTIONS:
            fail(f"workflows/{name}", f"sections {headings(t)} != required order")
        pc = section(t, "Project Context")
        if CONSUMPTION not in pc or "adds no" not in pc and "no context-loading stage" not in pc:
            fail(f"workflows/{name}", "Project Context section must reference the standard and add no stage")
        stages = section(t, "Stages")
        rows = re.findall(r"(?m)^\| (\d+) \| ([^|]+) \|", stages)
        nums = {int(n) for n, _ in rows}
        if re.search(r"(?i)project context", " ".join(s for _, s in rows)):
            fail(f"workflows/{name}", "a stage named for project context was added")
        for n in re.findall(r"[Ss]tages? (\d+)(?:(?:,| and|-| \d)[ \d,and-]*)?", pc):
            pass
        for grp in re.findall(r"[Ss]tages? ((?:\d+(?:-\d+)?(?:, | and |, and )?)+)", pc):
            for n in re.findall(r"\d+", grp):
                if int(n) not in nums:
                    fail(f"workflows/{name}", f"Project Context section cites stage {n}, which does not exist")
        for a in set(re.findall(r"`([a-z-]+-agent)`", t)):
            if a not in agents:
                fail(f"workflows/{name}", f"unknown agent {a}")
        for c in set(re.findall(r"`/([a-z-]+)`", t)):
            if c not in commands:
                fail(f"workflows/{name}", f"unknown command /{c}")
        for s in set(re.findall(r"skills/([a-z-]+)/SKILL\.md", t)):
            if s not in skills:
                fail(f"workflows/{name}", f"unknown skill {s}")


def check_links_and_secrets():
    files = [p for d in ("docs", "evals", ".claude", ".github", "templates") for p in (ROOT / d).rglob("*.md")] + [ROOT / "CHANGELOG.md", ROOT / "README.md"]
    for f in files:
        if "fixtures" in f.parts:
            continue
        text = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        for m in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", text):
            link = m.group(1)
            if link.startswith(("http", "mailto")):
                continue
            checked["links"] += 1
            if not (f.parent / link).resolve().exists():
                fail(str(f.relative_to(ROOT)), f"broken link {link}")
    for d in (".claude", ".github"):
        for f in (ROOT / d).rglob("*.md"):
            if find_secrets(f.read_text(encoding="utf-8")):
                fail(str(f.relative_to(ROOT)), "secret-like content in a Hub definition")


def check_scenarios(agents, commands, skills):
    base = ROOT / "evals/end-to-end"
    files = sorted((base / "scenarios").glob("[0-9][0-9]-*.md")) if (base / "scenarios").is_dir() else []
    matrix = (ROOT / "docs/end-to-end-validation-matrix.md")
    mtext = matrix.read_text(encoding="utf-8") if matrix.is_file() else ""
    if not files:
        fail("evals/end-to-end", "no scenarios")
    for f in files:
        checked["scenarios"] += 1
        t = f.read_text(encoding="utf-8")
        rel = str(f.relative_to(ROOT))
        h = headings(t, "##")
        if headings(t, "#")[:1] != ["Scenario"] or h != SCENARIO_SECTIONS[1:]:
            fail(rel, f"headings {h} do not match the result format")
        res = section(t, "Result")
        if not re.search(r"\b(Pass|Needs Improvement|Fail|Not yet run)\b", res):
            fail(rel, "Result has no outcome")
        if re.search(r"\b\d+\s*/\s*\d+\b|score", res, re.I):
            fail(rel, "numeric scoring")
        m = re.search(r"Entry: (/[a-z-]+|[a-z-]+ workflow)", t)
        agent = re.search(r"Agent: `([a-z-]+-agent)`", t)
        if not m:
            fail(rel, "no 'Entry:' line")
        elif m.group(1).startswith("/") and m.group(1)[1:] not in commands:
            fail(rel, f"unknown command {m.group(1)}")
        if agent:
            if agent.group(1) not in agents:
                fail(rel, f"unknown agent {agent.group(1)}")
            elif m and m.group(1).startswith("/") and commands.get(m.group(1)[1:]) != agent.group(1):
                fail(rel, f"{m.group(1)} does not route to {agent.group(1)}")
        for role, name in re.findall(r"(?m)^\| `([a-z-]+)` \| (Primary|Supporting|Conditional|Unnecessary) \|", t) and []:
            pass
        for name, role in re.findall(r"(?m)^\| `([a-z-]+)` \| (Primary|Supporting|Conditional|Unnecessary) \|", t):
            if name not in skills:
                fail(rel, f"unknown skill {name}")
            elif agent and agent.group(1) in agents and role != "Unnecessary" and name not in agents[agent.group(1)]:
                fail(rel, f"skill {name} is {role} but is not in {agent.group(1)}'s skill set")
        if f.stem not in mtext:
            fail(rel, "missing from the end-to-end matrix")


def main():
    skills = check_skills()
    agents = check_agents(skills)
    commands = check_commands(agents)
    check_workflows(agents, commands, skills)
    check_links_and_secrets()
    check_scenarios(agents, commands, skills)
    print("checked: " + ", ".join(f"{v} {k}" for k, v in checked.items()))
    if errors:
        print(f"{len(errors)} problem(s):")
        for e in errors:
            print("  - " + e)
        return 1
    print("structure OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
