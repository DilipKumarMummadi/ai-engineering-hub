# Skills

This document describes the skill architecture and lists the skills that exist today.

## Existing Skills

Fourteen skills exist. Each lives in its own directory with a `SKILL.md`:

| Skill | Purpose |
| --- | --- |
| `api-development` | Design, implement, review and improve APIs |
| `architecture` | Analyze, design and evolve software architecture |
| `change-intelligence` | Identify the engineering impact of a change |
| `code-review` | Review software changes and produce severity-ranked findings |
| `database-sql` | Relational database, SQL, schema and migration work |
| `debugging` | Evidence-driven investigation of failures |
| `observability` | Logs, metrics, traces, alerts and telemetry analysis |
| `performance` | Measured performance investigation and improvement |
| `playwright` | Plan, generate, review and debug Playwright/E2E tests |
| `refactoring` | Improve code structure while preserving behavior |
| `reliability` | Failure modes, resilience and recovery |
| `requirement-intelligence` | Analyze and interactively refine a requirement and assess its readiness |
| `security` | Defensive security review and hardening |
| `testing` | Test planning, generation and review |

## Structure

Each skill lives in its own lowercase kebab-case directory and follows the standardized `SKILL.md` structure defined in [skill-specification.md](skill-specification.md), for example:

```
<skills-dir>/
└── code-review/
    └── SKILL.md
```

The same skills are present in the portable plugin directory `skills/`, in the platform-native directories `.claude/skills/` and `.github/skills/`, and in the tool-neutral `.agents/skills/`.

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
