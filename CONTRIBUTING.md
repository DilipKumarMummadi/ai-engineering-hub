# Contributing

Thanks for helping build the AI Engineering Hub. Please follow these guidelines.

- **Keep capabilities reusable.** Design for use across projects, not a single codebase.
- **Prefer skills over duplicated prompts.** If instructions repeat, extract them into a skill.
- **Avoid technology-specific logic unless required.** Be stack-specific only when the task demands it.
- **Follow consistent naming.** Use lowercase kebab-case for skill, agent, and workflow directories (for example `code-review`, `unit-test-generation`).
- **Document every capability.** Each addition needs clear documentation of what it does and when to use it.
- **Add evaluations for important capabilities.** Place them in `evals/`.
- **Avoid duplicating Claude/Copilot logic unnecessarily.** Share logic through skills and templates where practical.
- **Keep platform-specific configuration inside the appropriate native directories.** Claude Code in `.claude/`, GitHub Copilot in `.github/`.
- **Keep changes focused and reviewable.** One capability or concern per pull request.
