# Plugin Packaging Evaluations

Evaluations for packaging the Hub as an Agent Plugins 1.0.0 plugin. See the [evaluation suite overview](../README.md) for the case format and outcomes, and [Plugin Architecture](../../docs/plugin-architecture.md) for the standard. Most cases run the validator (`scripts/validate-plugin/validate_plugin.py`) against the package or a scratch copy of it.

## What Is Being Evaluated

Whether the package is a valid, minimal, safe plugin and the existing Hub is unharmed.

## Dimensions

| Dimension | Question |
| --- | --- |
| Manifest correctness | Does `plugin.json` follow the canonical 1.0.0 schema, name and field rules? |
| Package structure | Is `skills/<name>/SKILL.md` correct and in agreement with its source? |
| Skill discovery | Is every intended skill, and only those, discoverable? |
| Path safety | Do all references stay inside the package? |
| Secret protection | Is secret-like content rejected without being echoed? |
| Portable vs client-specific | Is client content separate, and is nothing duplicated? |
| Backward compatibility | Does the Hub work exactly as before? |

## Evaluation Process

1. Perform the case's `# Input`, in a scratch copy where it modifies files.
2. Compare the result to Expected Behavior, Important Checks and Failure Conditions.
3. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores.

## Cases

| Case | Tests |
| --- | --- |
| [valid-plugin](cases/valid-plugin.md) | The unmodified repository is validated as an Agent Plugin. |
| [invalid-manifest](cases/invalid-manifest.md) | A manifest breaks the 1.0.0 rules. |
| [missing-skill](cases/missing-skill.md) | A skill directory loses its `SKILL.md`, and another drifts from its source. |
| [invalid-path](cases/invalid-path.md) | A skill links outside `skills/`, or a stray file sits in `skills/`. |
| [secret-in-package](cases/secret-in-package.md) | A credential-like string is added to a packaged file. |
| [repository-context-excluded](cases/repository-context-excluded.md) | A repository-specific `PROJECT-CONTEXT.md` and an `mcp.json` appear in the package. |
| [client-specific-content](cases/client-specific-content.md) | Client-specific resources are kept apart from the portable core. |
| [backward-compatibility](cases/backward-compatibility.md) | The existing Hub still works after packaging. |
