# Scenario

A skill directory loses its `SKILL.md`, and another drifts from its source.

# Input

In a scratch copy, delete `skills/testing/SKILL.md`; separately, edit `skills/debugging/SKILL.md` without changing `.claude/skills/debugging/SKILL.md`.

# Context

Scratch copy of the package.

# Expected Behavior

The first is reported as `SKILL.md missing`; the second as differing from `.claude/skills` with the `--sync` hint. `--sync` then restores agreement.

# Important Checks

- A skill is never silently dropped.
- Nothing deeper than one directory level is treated as a skill.

# Failure Conditions

- A missing or drifted skill passes.
- `--sync` changes `.claude/skills/`.

# Notes

Package structure and skill discovery.
