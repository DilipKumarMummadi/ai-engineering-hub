# GitHub Copilot Extension Namespace

Client-specific content for GitHub Copilot lives under this reverse-domain namespace directory, kept apart from the portable core (`skills/`, `plugin.json`).

| Resource | Location | In the plugin |
| --- | --- | --- |
| Agents | `.github/agents/` (source) | Yes: generated copy in `agents/<name>.agent.md` |
| Prompts (commands) | `.github/prompts/` | No |
| Workflows | `.github/workflows/` | No |
| Skills | `.github/skills/` (also packaged portably as `skills/`) | Yes, as `skills/` |

`agents/` is **generated**. Do not edit it. Edit `.github/agents/` and run `python3 scripts/validate-plugin/validate_plugin.py --sync`. The copy differs from the source only in two path rewrites (`../skills/` to `../../skills/`, and sibling agent links gain `.agent.md`), and the plugin validator fails if it drifts. See [Plugin Architecture](../docs/plugin-architecture.md).
