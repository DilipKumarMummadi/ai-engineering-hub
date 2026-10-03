# Scenario

A skill links outside `skills/`, or a stray file sits in `skills/`.

# Input

In a scratch copy, append a link whose target is `../../plugin.json` to a skill, and create `skills/notes.md`.

# Context

Scratch copy of the package.

# Expected Behavior

The escaping link is reported as needing to resolve inside `skills/`; the stray file is reported. Links to sibling skills remain valid.

# Important Checks

- No skill depends on files outside the skills tree.
- Sibling-skill links are not flagged.

# Failure Conditions

- A link that escapes the skills tree accepted.
- Valid sibling links flagged.

# Notes

Path safety.
