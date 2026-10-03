# GitHub Copilot Extension Namespace

Client-specific content for GitHub Copilot lives under this reverse-domain namespace directory, kept apart from the portable core (`skills/`, `plugin.json`).

The Hub's Copilot resources are currently native to the repository and are **not copied here**:

| Resource | Location |
| --- | --- |
| Agents | `.github/agents/` |
| Prompts (commands) | `.github/prompts/` |
| Workflows | `.github/workflows/` |
| Skills | `.github/skills/` (also packaged portably as `skills/`) |

Agent definitions use relative links that only resolve from `.github/agents/`, so copying them here would fork their logic. See [Plugin Architecture](../docs/plugin-architecture.md) for the reasoning and the deferred follow-up.
