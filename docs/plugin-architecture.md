# Plugin Architecture

How the AI Engineering Hub is packaged as an [Agent Plugins](https://agent-plugins.org) 1.0.0 plugin. Packaging is additive: the Hub works directly from the repository without installing the plugin.

## Layers

```
AI Engineering Hub Repository   (source of truth)
        |
        v
Plugin Package                  (plugin.json + skills/ + com.github.copilot/ + README.md)
        |
        v
Portable Skills                 (skills/<name>/SKILL.md, technology-neutral)
        |
        v
Client-Specific Extensions      (com.github.copilot/, and the native .claude/ and .github/ trees)
        |
        v
AI Client                       (Claude Code, GitHub Copilot, other Agent Plugins clients)
```

## Plugin Is Not MCP

| | Plugin | MCP |
| --- | --- | --- |
| Role | Packaging and distribution layer | Tool and integration layer |
| Delivers | Skills (instructions), client extensions, metadata | Callable tools, resources and servers |
| Status | This step | Future step. No `mcp.json`, server, tools or transport exist in this package. |

The plugin stays valid without MCP. MCP, when added, will be a separate, additive file.

## Package Contents

| Path | Kind | Role |
| --- | --- | --- |
| `plugin.json` | Portable | Manifest. Core fields only; no `extensions` entry. |
| `README.md` | Portable | Package documentation. |
| `skills/<name>/SKILL.md` | Portable | 13 generic engineering skills, discovered by the client from `skills/`. |
| `com.github.copilot/` | Client-specific | Copilot namespace. Documents the Copilot resources; holds no copied logic. |
| `docs/` | Documentation | Specifications and this file. Skills link only to sibling skills and never to `docs/`. |

## What Stays Out of the Package

| Area | Classification | Why |
| --- | --- | --- |
| `evals/` | Evaluation infrastructure | Tests the Hub itself; not a runtime capability |
| `scripts/` | Development tooling | Validators, the Project Context generator and their tests |
| `.claude/agents`, `.claude/commands`, `.claude/workflows` | Client-specific (Claude Code) | Native to Claude Code; not part of the portable core |
| `.github/agents`, `.github/prompts`, `.github/workflows` | Client-specific (Copilot) | Native to Copilot; see below |
| `templates/project-context/` | Template | Blank template only |
| Any `PROJECT-CONTEXT.md` | Repository-specific | See below |

## Skills: Source and Package Copy

Agent Plugins discovers skills only in a root `skills/` directory. The Hub's canonical skills live in `.claude/skills/` (with a byte-identical copy in `.github/skills/`, already enforced by `scripts/validate-hub`). `skills/` is therefore a third, generated copy that packaging requires, kept honest by the plugin validator:

- `.claude/skills/` is the source. Edit skills there.
- `python3 scripts/validate-plugin/validate_plugin.py --sync` refreshes `skills/` from the source.
- The validator fails when `skills/` differs from `.claude/skills/`.

Symlinks were rejected because they are unreliable on Windows checkouts and in archives.

## Agents, Commands and Workflows

The core specification is portable around skills only, so none of these are core plugin content.

- **Agents** (9 per client) link to skills and to `docs/` with relative paths (`../skills/...`, `../../docs/...`) that are valid only in `.claude/agents/` and `.github/agents/`. Placing copies under `com.github.copilot/agents/` would break those links or force a rewritten duplicate of the agent logic, so they are **not** repackaged in this step. They remain intact in place. Packaging them later needs a path strategy that does not fork the definitions.
- **Commands** (Claude `.claude/commands/`, Copilot `.github/prompts/`) are thin entry points that read the agent definition by repository path. They are unchanged and are not plugin components.
- **Workflows** are Hub orchestration documents for the same reason. Unchanged.

## Project Context

The plugin may carry the *capability*: the Project Context specification and generator live in `docs/` and `scripts/project-context/`, and the blank template in `templates/project-context/`. There is no Project Context skill, so none is packaged.

A `PROJECT-CONTEXT.md` describes one repository. It is generated in, and stays in, the repository that uses the Hub. It is never part of the package, and the validator rejects one anywhere in the packaged directories.

## Validation

`python3 scripts/validate-plugin/validate_plugin.py` checks the manifest (canonical schema URL, permitted fields, name, version), the `skills/` layout and its agreement with the source, link containment, required docs, forbidden content (evals, scripts, fixtures, secrets, `PROJECT-CONTEXT.md`, `mcp.json`). Tests: `python3 scripts/validate-plugin/test_validate_plugin.py`. Evaluation cases: [`evals/plugin-packaging/`](../evals/plugin-packaging/README.md).
