# Skills

This document describes the future skill architecture. No skills exist yet.

## Structure

Each skill will live in its own lowercase kebab-case directory and follow a standardized `SKILL.md` structure, for example:

```
<skills-dir>/
└── code-review/
    └── SKILL.md
```

The exact `SKILL.md` format (metadata, instructions, supporting files) will be defined when the first skill is introduced. Skills will be placed in the directory native to each platform (`.claude/skills/`, `.github/skills/`) or in the tool-neutral `.agents/skills/`.

## Design Qualities

Skills should be:

- **Reusable**: useful across projects and contexts
- **Focused**: one capability per skill
- **Composable**: usable on their own or combined by agents and workflows
- **Technology-aware where necessary**: specific to a stack only when the task requires it
- **Tool-independent where possible**: avoid coupling to one AI tool
- **Versionable**: changes are tracked and reviewable
- **Testable**: covered by evals in `evals/`

## Naming

Use lowercase kebab-case, named for the capability: `code-review`, `playwright-debugging`, `unit-test-generation`, `software-architecture`.
