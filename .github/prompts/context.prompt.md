---
description: Generate, inspect or check the Project Context (PROJECT-CONTEXT.md) of the current repository
agent: agent
---

# /context

Generate, inspect or check the Project Context (`PROJECT-CONTEXT.md`) of the **repository you are working in**. Project Context belongs to that consuming repository. The AI Engineering Hub only provides the capability and never stores a repository's context.

This is a tool command. It does not route to an agent. It runs the Hub's existing Project Context Generator, which is the only thing that writes the context. Do not write, rewrite or hand-edit `PROJECT-CONTEXT.md` yourself, and do not create a second generator.

## Operations

| Request | What to do |
| --- | --- |
| `generate` | Create or update the target repository's `PROJECT-CONTEXT.md` with the generator. Add `--dry-run` to show what would change and write nothing. |
| `inspect` | Read the existing `PROJECT-CONTEXT.md` and summarize it. Do not regenerate. |
| `drift` | Run the generator's read-only drift check and report it. Do not modify the context. |

If the request is empty or names none of these, show this table and stop. Do nothing else.

## 1. Identify the target repository

The target is the repository of the current working directory, never the Hub.

1. Run `git rev-parse --show-toplevel` from the current working directory. Use its output as the target root. If the current directory is not in a git repository, use the current directory only if it clearly is a project root (it holds a project manifest, source directories or a README). Otherwise stop and ask the user to change to their repository.
2. Confirm the target to the user in one line (its name and path) before any operation that writes.
3. Stop if the target is the AI Engineering Hub itself (it contains `plugin.json` naming `ai-engineering-hub` and `scripts/project-context/project_context/`). Say the command targets the repository you are working in, and continue only if the user explicitly asks for the Hub's own context.

## 2. Locate the generator

The generator is the launcher `scripts/project-context/project-context` inside the Hub. Resolve it in this order and use the first that exists:

1. `$AI_HUB_HOME/scripts/project-context/project-context`, when the `AI_HUB_HOME` environment variable names a Hub checkout.
2. A Hub checkout path the user gives you.
3. Otherwise ask the user where the Hub is installed. Do not search the filesystem and do not copy the generator into the target repository.

It needs Python 3.9 or newer and nothing else. Always pass `--repo <target root>`. Never run it with the Hub as the implicit target.

## 3. Run the operation

- **generate:** `<generator> generate --repo <target root>` (add `--dry-run` if asked). With an existing context the generator updates it minimally: supported entries are kept, developer-provided entries and manual blocks are preserved, changes and removals are reported, and conflicts are shown. A first generation only creates the new file, so run it directly unless the user asked for `--dry-run`.
- **inspect:** read `<target root>/PROJECT-CONTEXT.md` (or the path the repository's `GENERATOR-CONFIG.md` names). If it does not exist, say so and suggest `/context generate`. Summarize these areas where the context has them: project overview, technology stack, architecture, repository structure, API, database, testing, CI/CD, infrastructure, observability, security, conventions, constraints, unknowns and freshness (last reviewed, known stale sections). Keep Confirmed, Inferred and Unknown apart. Say when an area is absent instead of filling it in.
- **drift:** `<generator> drift --repo <target root>`. Report the status and findings as the tool gives them. If drift is Material or Potentially Material, recommend `/context generate` to the user. Do not run it.

## 4. Report

For generate, say what was written or that nothing changed, then give:

- the target repository and the file written
- what was discovered (technologies and structure) and the Confirmed, Inferred and Unknown counts
- the important unknowns the developer should fill in or confirm
- whether sensitive files or secret-like content were detected, where (path and kind only), and that no value was written
- validation result, and conflicts between documentation and source, if any

Remind the user to review the file before committing it. It is safe to commit because it holds no secrets, but it is their repository and their decision.

## Rules

- Repository evidence is the source of truth. Never invent, infer beyond the tool's output, or claim that something exists because it is typical.
- Never reproduce a secret, in a summary or anywhere else. Report location and kind only.
- Modify only `PROJECT-CONTEXT.md`, and only through the generator. Never edit application source, configuration or `GENERATOR-CONFIG.md`.
- This command does not authorize commits, pushes, deployments or changes to any other file.
- If the generator cannot run, report why and stop. Do not substitute a hand-written context.

The request is everything the user wrote after this prompt.
