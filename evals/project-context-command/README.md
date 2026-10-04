# Project Context Command Evaluations

Evaluations for the `/context generate | inspect | drift` command, defined in [Commands](../../docs/commands.md#context-generate-inspect-drift) and the [Command Registry](../../docs/command-registry.md). The command runs the existing Project Context Generator ([`scripts/project-context/`](../../scripts/project-context/README.md)) on the repository being worked on; the Hub stores no consuming repository's context. The generator's own behavior is evaluated in [project-context-generator](../project-context-generator/README.md) and [project-context-drift](../project-context-drift/README.md); these cases judge the command around it.

## What Is Being Evaluated

Whether the command analyzes the right repository, reuses the generator, stays read-only where it should, reports honestly, and never leaks a secret.

## Dimensions

| Dimension | Question |
| --- | --- |
| Target repository | Is the context created for the current repository (its root, even from a subdirectory), and never for the Hub or an unrecognizable directory? |
| Generator reuse | Is the existing generator run with `--repo`, with no second generator and no hand-written context? |
| Fidelity | Does the context match repository evidence, with Confirmed, Inferred and Unknown kept apart and nothing invented? |
| Preservation | Are manual and developer-provided contents preserved on update? |
| Secrets | Is no secret value written or shown, with only location and kind reported? |
| Read-only operations | Do `inspect` and `drift` leave every file unchanged? |
| Scope of change | Is only `PROJECT-CONTEXT.md` modified, and never application source? |
| Reporting | Are discoveries, unknowns, conflicts and secret status reported clearly? |

## Evaluation Process

1. Recreate the case's repository in a scratch directory (never a real repository).
2. Run the command from the stated directory with the Hub available.
3. Compare the result to Expected Behavior, Important Checks and Failure Conditions.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores.

Deterministic parts are also covered by `scripts/project-context/tests/test_context_command.py`.

## Validation Performed

A scratch .NET-style backend repository was used with Claude Code and the Hub loaded as a plugin. Observed: dry run writes nothing; generate creates the file at the repository root even when started in a subdirectory, with the decoy password absent; inspect and drift leave the file byte-identical; drift reported a new Dockerfile; an empty non-repository directory and the Hub itself both stopped with a question. The Copilot prompt follows the same rules but was not run.

## Cases

| Case | Tests |
| --- | --- |
| [dotnet-backend](cases/dotnet-backend.md) | Generate context in a .NET backend. |
| [react-frontend](cases/react-frontend.md) | Generate context in a React frontend. |
| [python-project](cases/python-project.md) | Generate context in a Python project. |
| [monorepo](cases/monorepo.md) | Generate context in a monorepo. |
| [existing-context](cases/existing-context.md) | PROJECT-CONTEXT.md already exists with manually maintained content. |
| [missing-context](cases/missing-context.md) | `/context inspect` and `/context drift` with no PROJECT-CONTEXT.md. |
| [incomplete-documentation](cases/incomplete-documentation.md) | Documentation is sparse or missing. |
| [secret-like-values](cases/secret-like-values.md) | Secret-like values exist in the repository. |
| [context-drift](cases/context-drift.md) | `/context drift` after the repository changed. |
| [wrong-directory](cases/wrong-directory.md) | The command is run from a directory that is not a repository. |
| [hub-as-target](cases/hub-as-target.md) | The command is run inside the Hub repository. |
| [minimal-repository](cases/minimal-repository.md) | Empty or minimal repository. |
| [conflicting-documentation](cases/conflicting-documentation.md) | Documentation conflicts with source evidence. |
