# Skill Specification

This is the canonical standard for every AI Engineering Hub skill. It defines structure and authoring rules only. No skills exist yet.

## 1. Purpose of the Standard

A standardized format keeps skills consistent, so engineers and tools know what to expect. Every skill must be:

- **Reusable**: useful across projects, not tied to one codebase
- **Focused**: one responsibility
- **Composable**: usable alone or combined by agents and workflows
- **Discoverable**: a clear name and description make it findable and triggerable
- **Maintainable**: easy to read, review and update
- **Versionable**: changes are tracked and communicated
- **Testable**: behavior can be checked with evals
- **Portable**: usable across supported AI coding assistants where possible

## 2. Skill Identity

Every skill requires two metadata fields, in YAML front matter:

| Field | Requirement |
| --- | --- |
| `name` | Lowercase kebab-case. Must match the skill's directory name. |
| `description` | One or two sentences stating what the skill does and when to use it. Assistants use this to decide whether to invoke the skill, so make it specific. |

**Naming conventions**
- Lowercase kebab-case: letters, digits and hyphens only.
- Name the capability, not the tool brand, unless the tool is the point.
- Prefer `noun-verb` or `domain-task` forms that read clearly in a list.

Examples: `code-review`, `playwright-debugging`, `unit-test-generation`, `sql-optimization`.

## 3. Sections

Every skill must contain the following sections, in this order.

### Purpose
State the capability the skill provides, in a few sentences.

### When to Use
List the situations and trigger conditions in which the skill should be invoked.

### When NOT to Use
List situations where another skill or approach is more appropriate, and point to that skill when one exists.

### Inputs
Define what information the skill expects. Mark each input as required or optional. Examples: source code, requirements, error messages, logs, configuration, test results, architecture documentation. If a required input is missing, the skill should say to ask for it rather than guess.

### Process
A clear, numbered, step-by-step description of how the AI performs the task. Steps should be concrete and ordered, and include verification steps where relevant.

### Rules
Explicit constraints and engineering principles. Rules must be deterministic and actionable ("Do not change public API signatures without flagging it"), not vague ("Write good code").

### Output
A predictable output structure (headings, fields, or format) that is useful to engineers and easy for other skills and workflows to consume.

### Examples
Include examples where they materially improve understanding, such as a sample input and expected output. Omit them when they add nothing.

### Related Skills
Reference other skills where composition is useful. Link to them instead of duplicating their responsibility.

## 4. Tool Usage

Describe tool needs as capabilities, not products. Say "search the codebase" or "run the test suite", not a specific assistant's tool name. Name a specific tool only when the skill cannot work without it, and document that requirement explicitly. Note any optional tools and how the skill behaves without them.

## 5. Safety and Destructive Operations

Every skill must:

- Avoid destructive operations unless explicitly authorized.
- Ask for confirmation before deleting or overwriting data or code where appropriate.
- Never expose secrets (keys, tokens, passwords, credentials) in output, logs or examples.
- Never fabricate results. Do not claim tests passed, files exist, or commands ran unless verified.
- Clearly distinguish assumptions from verified information.

## 6. Scope

Each skill has one focused responsibility. If a skill covers unrelated problems, split it. Larger processes belong in agents or workflows that compose skills, not in a single giant skill.

## 7. Quality Checklist

A new skill is approved only if it has:

- [ ] A clear purpose
- [ ] Clear trigger conditions (When to Use / When NOT to Use)
- [ ] Clear inputs
- [ ] A clear process
- [ ] A clear output
- [ ] No unnecessary duplication of other skills
- [ ] Technology assumptions documented
- [ ] Security considerations documented
- [ ] Examples where useful
- [ ] Evaluatable behavior, with evals in `evals/` for important skills
- [ ] A kebab-case name matching its directory

## 8. Versioning

- Skills evolve through normal, reviewed changes recorded in git and [CHANGELOG.md](../CHANGELOG.md).
- Prefer backward-compatible changes. Avoid changing a skill's name, inputs or output structure without need, since other skills and workflows may depend on them.
- Treat changes to the Output structure or renaming as breaking changes and call them out in the changelog.
- Skills may optionally carry a `version` field in front matter (semantic versioning) once versioning needs justify it.
- Retire a skill by documenting the replacement before removal.

## 9. Claude Code and GitHub Copilot Compatibility

The canonical skill should stay platform-neutral where possible. The same skill concept may be exposed through:

- `.claude/skills/` for Claude Code
- `.github/skills/` for GitHub Copilot
- `.agents/skills/` or other supported locations

Rules:
- Do not duplicate skill logic unnecessarily. Keep the behavior in one canonical place and expose it to each client.
- Canonical behavior must remain consistent across clients.
- Platform-specific wiring or metadata belongs in that platform's native directory, not in the skill body.

The mechanism for sharing one skill across locations (for example, generation or linking) will be decided when the first skill is added.

## 10. Recommended SKILL.md Template

```markdown
---
name: <skill-name>
description: <short description>
---

# <Skill Name>

## Purpose

## When to Use

## When NOT to Use

## Inputs

## Process

## Rules

## Output

## Examples

## Related Skills
```
