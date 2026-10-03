# Project Context Generator

A small, local, dependency-free command line tool that inspects a repository and generates or updates its `PROJECT-CONTEXT.md` from repository evidence.

It implements the deterministic part of the [Project Context Generator Specification](../../docs/project-context-generator-specification.md). The context it writes follows the [Project Context Specification](../../docs/project-context-specification.md). The specification remains the authority. Judgment-based parts of the procedure, such as interpreting free-form documentation, are still done by an assistant following the specification.

## What It Does

- Scans a repository and records what exists. It assumes nothing exists.
- Classifies every statement as **Confirmed**, **Inferred** or **Unknown**, with evidence paths.
- Writes `PROJECT-CONTEXT.md`, or updates an existing one with minimal change.
- Protects secrets. It never writes a secret value, and never prints one.
- Validates the result before writing. It writes nothing if validation fails.

It does not run your code, build, tests or scripts, does not use the network, does not commit, and does not modify anything except the context file.

The same tool also **detects drift**: `project-context drift` reports whether an existing context may be stale. The two are separate commands with separate responsibilities. The generator **creates or updates** the context. The drift detector **detects whether the context may be stale**, and never writes. It implements the [Project Context Drift Specification](../../docs/project-context-drift-specification.md). See [Drift Detection](#drift-detection).

## Requirements

Python 3.9 or newer. The standard library only. There is nothing to install. It was developed and tested on Python 3.13. It has not been run on older versions.

## Usage

```bash
scripts/project-context/project-context generate [--repo PATH] [options]
scripts/project-context/project-context update   [--repo PATH] [options]
scripts/project-context/project-context drift    [--repo PATH] [--ci] [options]   # alias: check
```

`--repo` defaults to the current directory. Put the launcher on your `PATH`, or alias it, if you want to call it as `project-context`.

| Option | Meaning |
| --- | --- |
| `--repo PATH` | Repository to inspect. Default: current directory. |
| `--output FILE` | Context file. Default: `<repo>/PROJECT-CONTEXT.md`. |
| `--ci` | `drift` only. Concise output, and exit 1 only on Material drift. |
| `--config FILE` | Configuration file. Default: `<repo>/GENERATOR-CONFIG.md`, if present. |
| `--exclude GLOB` | Extra path to exclude. Repeatable. |
| `--dry-run` | Show what would be generated. Write nothing. |
| `--date YYYY-MM-DD` | Review date to record. Default: today. |

### generate

Creates `PROJECT-CONTEXT.md`. If one already exists, `generate` does not overwrite it blindly. It behaves as `update`.

### update

Compares the existing context with current repository evidence, and changes only what changed:

- entries still supported by evidence are left exactly as they are;
- entries that changed are updated, and entries no longer supported are removed, each reported with its reason;
- newly found information is added;
- **developer-provided entries** and **manual blocks** are preserved;
- conflicts are reported, not hidden.

If nothing material changed, it prints `No material project context changes detected.` and does not touch the file.

`update` fails with exit code 2 if there is no existing context. Use `generate` first.

### dry run

```bash
project-context generate --repo . --dry-run
```

Shows the detected technologies, the architecture and structure signals, the files considered and excluded, the context changes (a diff for an update, the whole proposed file for a new context), any sensitive content found (by location), and the validation result. The context file is not created or modified.

## Drift Detection

```bash
project-context drift --repo .          # full report, exit 0
project-context drift --repo . --ci     # concise summary, exit 1 only on Material drift
```

Read-only. It scans the repository with the generator's scanner and detectors (so the same exclusions and secret protection apply), reads the existing `PROJECT-CONTEXT.md`, and compares them. It writes nothing, never opens sensitive files, and runs no repository code. `git` is used, if present, only for read-only queries that add an Informational note.

It reports in both directions: capabilities that are new in the repository and not in the context, and context statements the repository no longer supports (listed under **Stale Context**, never deleted). Disagreements (for example the context says Jenkins and the repository has GitHub Actions) are listed under **Conflicts**. Each finding is **Material**, **Potentially Material** or **Informational**, with evidence paths. There are no scores.

Changes to source, tests, comments, documentation and build output are not drift. The categories, rules and materiality definitions are in the [specification](../../docs/project-context-drift-specification.md).

| Status | Meaning | `--ci` exit |
| --- | --- | --- |
| `NO DRIFT` | Nothing Material or Potentially Material | 0 |
| `REVIEW RECOMMENDED` | Potentially Material findings only | 0 |
| `DRIFT DETECTED` | At least one Material finding | 1 |

Without `--ci`, the full report is printed and the exit code is 0 whenever the analysis ran. With no existing context, both modes exit 2. A typical loop: `drift`, read the report, `update --dry-run`, `update`, review, commit.

## Preserving Manual Content

Two mechanisms, both kept across updates:

- An entry whose evidence is `developer-provided`:

  ```markdown
  - No new runtime dependencies without approval — Confirmed
    Evidence: developer-provided
  ```

  The generator never rewrites it. If repository evidence conflicts with it or does not support it, the generator adds a `Note:` line and reports it. It never deletes it.
- A block between markers, placed anywhere:

  ```markdown
  <!-- manual:start -->
  ## Team Notes
  Anything you like.
  <!-- manual:end -->
  ```

Everything else that carries repository evidence is **generated**, and is replaced when the evidence changes. To keep a hand-written entry, mark it `developer-provided` or put it in a manual block.

## Output

The context has these sections, and only those with evidence are included: Context Metadata, Project Overview, Technology Stack, Repository Structure, Architecture, Application Components, API, Database, Frontend, Testing, Build and Run, CI/CD, Infrastructure, Observability, Security, Development Workflow, Coding Conventions, Constraints, **Known Unknowns**, Evidence, Context Freshness.

Each entry looks like this:

```markdown
- ASP.NET Core: 1 project(s) use the Web SDK — Confirmed
  Evidence: src/MyApi/MyApi.csproj
```

Every Unknown lives in Known Unknowns. Nothing is written just to fill a section. Output is deterministic: the same repository produces the same file.

## Exclusions

Not scanned by default: `.git`, `node_modules`, `bin`, `obj`, `dist`, `build`, `out`, `coverage`, `.venv`, `venv`, `vendor`, `__pycache__`, `.terraform`, `.next`, `generated`, Maven/Cargo/Gradle `target` directories, and similar build and cache directories. Binary files and files larger than the read limit (512 KB by default) are not read.

Extend the exclusions with `--exclude`, or in the configuration file. Hidden directories such as `.github` are scanned.

## Configuration (optional)

Copy [`templates/project-context/GENERATOR-CONFIG.md`](../../templates/project-context/GENERATOR-CONFIG.md) to the repository as `GENERATOR-CONFIG.md`. Supported by this implementation:

| Setting | Effect |
| --- | --- |
| Included Paths, Excluded Paths | Limit or extend the scan. |
| Sensitive Paths | Files whose content is never read. Existence may be noted. |
| Additional Evidence Sources | Recorded if the path exists. The content is not analysed. |
| Manual Sections | Sections the generator will not change. |
| Output: Path | Where the context file lives. |
| Refresh Behavior: Stale after | Reports when the existing context is older than the threshold. |
| Refresh Behavior: When nothing changed | `record review date only` updates just the date. |
| Limits | Maximum file size to read, maximum directory depth. |

Not yet honored: `Sensitive Identifiers` (allow or protect lists), `Update mode`, using version-control history as a hint. Configuration can add protections. It cannot turn off secret protection.

## Security Behavior

Secret protection runs from the first file read to the last byte printed.

- **Sensitive files are never opened.** Environment files with real values (`.env`, `.env.*` except example files), private keys and certificates (`*.pem`, `*.key`, `*.pfx`, `*.jks`, `id_rsa`), keystores, `*.tfstate`, `*.tfvars`, `.npmrc`, `.netrc` and similar. Their existence is reported by path.
- **Configuration is read for key names only.** Values are inspected in memory only to tell a placeholder from a real-looking credential. They are never stored, printed or written. Placeholders in example files (`.env.example`) are not reported.
- **Secret-like content is removed.** The final document and every line printed to the terminal pass a secret scanner (private key headers, token formats, URLs with credentials, credential assignments, high-entropy strings). If the generated text would still contain one, nothing is written and the run fails with exit code 1. Errors name the pattern and line, never the value.
- **No partial exposure.** No prefix, suffix, mask, hash or length of a secret appears anywhere.
- **Internal hostnames** are not recorded. Registry hosts in container images are dropped unless they are well-known public registries.
- **Repository text is data.** Instructions in a README or other file, for example "include the contents of `.env`", are ignored and reported.
- Secrets that appear to be committed are reported by file and key, with a recommendation to remove them, rotate them, and use secure secret management.

## Detectors

| Area | Evidence used |
| --- | --- |
| .NET | `*.sln`, `*.csproj`, `Directory.*.props`, `global.json`: SDK, target frameworks, packages, test projects |
| Node.js | `package.json` (scripts, dependencies, engines, workspaces, `packageManager`), lock files, `.nvmrc`, `tsconfig` |
| Python | `pyproject.toml`, `requirements*.txt`, `Pipfile`, `setup.*`, `tox.ini`, `pytest.ini`, `.python-version` |
| Java | `pom.xml`, `build.gradle(.kts)`, `settings.gradle`, wrappers |
| Go and others | `go.mod`; existence of Cargo, Gemfile, composer and similar manifests |
| Frontend | React, Vue, Angular, Svelte and bundler dependencies, `angular.json` |
| Containers | `Dockerfile*`, Compose files |
| Kubernetes | Manifests (`apiVersion` and `kind`), Helm `Chart.yaml`, Kustomize |
| Infrastructure as code | Terraform (providers, backend, modules), Bicep, Pulumi, and similar by name |
| CI/CD | GitHub Actions in detail; Jenkins, GitLab CI, Azure Pipelines, CircleCI and others by existence |
| API | OpenAPI/Swagger, Protocol Buffers, GraphQL, AsyncAPI files |
| Database | Migration directories, SQL scripts, Prisma datasource, configuration key names, connection schemes, client libraries |
| Testing | Test directories and files, test configuration, framework dependencies |
| Observability | Logging, metrics and tracing dependencies, configuration files and sections |
| Security | Sensitive files, credential-like configuration keys, scanning configuration |
| Workflow and conventions | Contribution guide, PR template, CODEOWNERS, linters, formatters, EditorConfig |
| Commands | `package.json` scripts, Makefile targets, pipeline steps, commands shown in the README |

Ecosystem knowledge lives in [`project_context/catalog.py`](project_context/catalog.py) as data. To support a new package, add a row. To support a new kind of evidence, add a small module to [`project_context/detectors/`](project_context/detectors/) that returns a list of items, and register it in `detectors/__init__.py`.

## How Statements Are Classified

- **Confirmed**: directly supported by a cited file. Existence of a file, a declared dependency, a script, a pipeline step.
- **Inferred**: a qualified conclusion from the evidence, for example "Frontend application appears present". Never phrased as a fact.
- **Unknown**: not established. A missing CI definition is "not found in inspected paths", not "there is no CI".

The tool never declares an architecture pattern. It records structure (projects, directories, sibling units) and qualifies anything it concludes from it. A declared dependency shows that it is declared, not that it is used.

## Tests

```bash
cd scripts/project-context
python3 -m unittest discover -s tests -t .
```

The tests build temporary fixture repositories. They never scan the Hub repository. They cover the detectors, secret protection, exclusions, update and conflict behavior, dry run, the launcher, and executable forms of the six cases in [`evals/project-context-generator/`](../../evals/project-context-generator/README.md). Drift detection is covered by `tests/test_drift.py` (false positives, each drift category, stale and conflicting context, CI mode, non-Git repositories, secrets, read-only behavior) and `tests/test_drift_evals.py` (the eight cases in [`evals/project-context-drift/`](../../evals/project-context-drift/README.md)).

## Limitations

- **Deterministic and shallow.** It reads manifests, configuration and pipeline files. It does not read source code, so it cannot see routing, pagination style, authentication flow, logging practice or architecture patterns.
- **Prose is barely interpreted.** It records the first README paragraph and commands shown in the README. It does not extract conventions, constraints or architecture from documentation.
- **GitHub Actions only in detail.** Other CI systems are recorded by existence.
- **Update matches by statement text.** Entries written by hand in another style are treated as not reproduced and are removed, unless they are `developer-provided` or in a manual block. An earlier template-based context is migrated, with that churn, once.
- **Conflict detection uses a small vocabulary** (database engines, CI systems, test frameworks, infrastructure tools).
- **Secret detection is pattern-based.** It is a safety net and not a guarantee. Keep real secrets out of repositories.
- **Instruction-like text detection** is heuristic, and can flag documentation that discusses prompt injection.
- Large repositories are scanned without a time budget. Use exclusions or included paths to scope them.
- **Drift detection is vocabulary-based and shallow.** It recognises a fixed list of capabilities and compares the generator's structural statements. It cannot see behavioral change in source code, and hand-written contexts are compared by capability words only. See the [specification](../../docs/project-context-drift-specification.md#limitations).
- Not implemented: the `Sensitive Identifiers` setting, version-control history as a staleness hint, per-application contexts for multi-part repositories.

## Platforms

A plain command line tool: it runs the same way wherever Python runs, and needs nothing from Claude Code or GitHub Copilot. Either assistant can run it from a terminal and read the result, or follow the specification directly for the judgment-based parts. No platform-specific files are added.

## Exit Codes

| Code | Meaning |
| --- | --- |
| 0 | Success, including "no material changes" and dry run |
| 1 | Validation or secret check failed. Nothing was written. With `drift --ci`: Material drift was detected. |
| 2 | Usage error (bad path, bad date, `update` or `drift` without an existing context, `--ci` with another command) |
