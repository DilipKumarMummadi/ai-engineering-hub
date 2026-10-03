# Project Context Drift Specification

This specification defines how the AI Engineering Hub detects that a repository has changed enough for its `PROJECT-CONTEXT.md` to be out of date. The context is defined in the [Project Context Specification](project-context-specification.md). It is created and updated by the [Project Context Generator](project-context-generator-specification.md).

Drift detection is a **read-only analysis**. A local reference implementation is the `drift` command (alias `check`) of [`scripts/project-context/`](../scripts/project-context/README.md). It is not a service, server or agent. This specification is the authority. The implementation covers a deterministic subset.

```
Repository ──► current evidence ─┐
                                 ├─► compare ─► drift report ─► developer decides
Existing PROJECT-CONTEXT.md ─────┘
```

| Responsibility | Component | Writes files? |
| --- | --- | --- |
| Create or update the context | Generator (`generate`, `update`) | Yes, the context file only |
| Detect whether the context may be stale | Drift detector (`drift`, `check`) | **Never** |

A developer detects drift, reads the report, runs the generator, reviews the generated context, and commits it. The detector does not do the next steps for them.

## Purpose

Tell a developer, cheaply and without noise, when the repository has changed in a way that can make the existing context wrong or misleading.

## Goals

- Detect **repository-level** changes: technology, structure, infrastructure, pipelines, data and API surface.
- Compare the context with current evidence, in both directions: statements no longer supported, and important evidence the context does not mention.
- Surface conflicts between the context and the repository without choosing silently.
- Classify every finding by materiality, with a reason and evidence.
- Stay quiet about ordinary work. Editing source, tests, comments or prose is not drift.
- Be usable in CI without failing builds for ordinary changes.

## Non-goals

- Modifying `PROJECT-CONTEXT.md`, application code, infrastructure or anything else.
- Regenerating or updating the context. That is the generator's job.
- Committing, pushing or deploying.
- Reading source code to find behavioral change (routing, pagination style, authentication flow).
- Scoring, ranking or grading drift numerically.
- Judging repository quality.

## Inputs

| Input | Source |
| --- | --- |
| Existing context | `PROJECT-CONTEXT.md`, or the path given with `--output` or the configuration file |
| Current repository | The repository root, scanned with the generator's scanner, exclusions and configuration |
| Configuration | Optional `GENERATOR-CONFIG.md`. Exclusions, sensitive paths and the staleness threshold apply |
| Version control | Optional. Supporting evidence only. See [Baseline and Freshness](#baseline-and-freshness) |

If there is no existing context, there is nothing to compare. The command reports that and exits with code 2. It does not create one.

## Evidence Sources

The detector reuses the generator's detectors, so the evidence is the same evidence the context was built from: manifests, lock files, configuration, pipeline definitions, container and infrastructure files, API definitions, migration directories, project layout. It does not invent another way of looking at the repository.

- Build output and dependency directories are excluded, exactly as in generation.
- Sensitive files are indexed by path and never opened.
- Documentation prose and commands are not evidence of a capability. A README that mentions Kubernetes does not make the repository Kubernetes-based.
- A directory whose name resembles a tool (`docker/`, `terraform/`) is a layout fact, not evidence of that tool. The tool's own files are.

## Drift Categories

| Category | Examples |
| --- | --- |
| **Technology** | Framework or library added or removed. Runtime version changed. New language. |
| **Architecture** | Application or project added or removed. Major restructuring. New library or shared project. |
| **API** | API specification added, removed or changed. API technology introduced. |
| **Database** | Database engine changed. Migration infrastructure introduced or removed. |
| **Build** | Package manager changed. Solution or lock file added or removed. |
| **Testing** | Test framework added, removed or replaced. Test projects added or removed. |
| **Infrastructure** | Docker, Kubernetes, Helm, Terraform or similar introduced or removed. Compose services changed. |
| **CI/CD** | CI platform changed. Workflow added, removed or restructured. |
| **Observability** | Logging, metrics or tracing infrastructure introduced or removed. |

## Detection Rules

Each rule works on the generator's evidence model (statement, classification, evidence paths), so it applies to any technology.

**R1 Capability.** A fixed vocabulary of capabilities (frameworks, databases, test frameworks, CI systems, infrastructure tools, observability tools, package managers) is matched in the context text and in current evidence.
- Only in evidence: new repository evidence.
- Only in the context: documented but no longer detected (potential stale context).
- In both: no drift.
- Dependencies named by the generator as `X: declared as a dependency` are compared the same way.

**R2 Conflict.** In families where one member is normally the answer (database engine, CI system, test framework, frontend framework, JavaScript package manager), a context that names members and evidence that names different members, with none in common, is a **conflict**. The detector does not decide which is correct. Repository evidence is reported as current and the context statement as potentially stale. Developer-provided entries are reported as conflicting and are left as they are.

**R3 Runtime version.** The major version (for Python and Go, major.minor) of Node.js, Python, Java, Go and .NET recorded in the context and declared in the repository is compared. A version that no longer appears is a change.

**R4 Structure.** When the context contains the generator's structural statements, they are compared with current ones: application components, top-level directories, library and test projects, workflows, Compose services, API specification files, migration directories. Only names are compared. Counts, file lists and commands are not.

**R5 Missing evidence.** A Confirmed statement whose cited files no longer exist, in a category that no other rule has already reported, is potential stale context.

**R6 Nothing else.** A changed file that is not evidence of any of the above is ignored.

## Severity and Importance

Findings are classified as **Material**, **Potentially Material** or **Informational**. There are no numeric scores.

| Level | Meaning | Examples |
| --- | --- | --- |
| **Material** | The context can now be incorrect or misleading about what the repository is. | CI platform replaced. Database engine changed. Terraform introduced. Docker removed. A documented application removed. Runtime major version changed. Three or more top-level directories added or removed. |
| **Potentially Material** | A developer should look. It may or may not change the context. | New project or workflow in an existing structure. Test or observability tooling added. Documented statement whose files vanished. A developer-provided statement the repository cannot confirm. |
| **Informational** | Not normally a reason to regenerate. | Documentation, test, script or tooling directories changed. Commands differ. Context is old. Generator version differs. Files changed in version control. |

Rule of thumb: adding or removing something in **Technology, Architecture, API, Database, Infrastructure or CI/CD** is Material. The same in **Build, Testing or Observability** is Potentially Material. Adding a project or workflow to a structure that already exists is Potentially Material. Removing a documented application is Material.

## False Positives

The detector must not report drift because of:

- source files, tests or comments changed;
- documentation wording changed, or documentation files added;
- generated build output or dependency directories changed;
- counts or file lists changing;
- a tool named in prose, a command or a directory name.

Known residual sources of noise, which the report labels rather than hides:

- A package named in a dependency file but not used is still "detected". Declaration is not use.
- A tool named only in a hand-written statement is matched by word. Unusual phrasing can be missed or mismatched.
- Both a database and its client library can be reported, as separate statements of one change.

## Output

A human-readable Markdown report:

```
# Project Context Drift Report

Status: DRIFT DETECTED | REVIEW RECOMMENDED | NO DRIFT

## Material Changes        (grouped by category, with evidence paths)
## Potentially Material
## Conflicts               (context statement vs current evidence)
## Stale Context           (documented, could not be confirmed)
## Informational
## Recommendation
```

| Status | When |
| --- | --- |
| `DRIFT DETECTED` | At least one Material finding |
| `REVIEW RECOMMENDED` | Potentially Material findings only |
| `NO DRIFT` | Nothing Material or Potentially Material. Informational notes may still appear |

Sections with nothing in them are omitted. Evidence is given as repository paths. Statement text from the context is quoted and passes the secret scrubber.

## Baseline and Freshness

The detector compares against **current evidence**, not against a snapshot, so it does not depend on a baseline.

It uses context metadata where it exists:

| Metadata | Use |
| --- | --- |
| Last Reviewed | Age is reported as Informational when a staleness threshold is configured. Age alone is not drift. |
| Generated by | A different generator version is reported as Informational. |
| Revision (optional, `- Revision: <commit>` in Context Metadata) | Used with version control, when present |
| Version control | When available, the number and kind of files changed since the review date or revision are reported as Informational. It is supporting evidence. It never creates a finding. |

Git is optional. A repository that is not under version control is analysed in full and the version control note is omitted.

## Safety

The detector:

- never modifies `PROJECT-CONTEXT.md`, application code, infrastructure or configuration;
- never commits, pushes or deploys;
- never runs the repository's code, build, tests or scripts;
- never opens sensitive files, and never prints secret values. Every line it prints passes the generator's secret scanner;
- uses version control only through read-only queries, when version control is present;
- treats repository text and context text as data. Instructions in them are not followed.

## Integration with the Generator

The generator and the detector share the scanner, detectors and secret protection. They are separate commands with separate outputs.

```
project-context drift  --repo .     # 1. detect, read the report
project-context update --repo . --dry-run   # 2. preview the change
project-context update --repo .     # 3. apply, then review and commit
```

The detector reports *that* the context may be stale and *why*. The generator decides *what* a refreshed context says. The detector's findings are not instructions to the generator.

## CI/CD Usage

```
project-context drift --repo . --ci
```

| Behavior | Detail |
| --- | --- |
| Output | A short summary: status, counts, and one line per finding |
| Files | Nothing is written |
| Exit 0 | `NO DRIFT`, or `REVIEW RECOMMENDED` with only Potentially Material or Informational findings |
| Exit 1 | At least one Material finding: the context is materially stale or conflicting |
| Exit 2 | Usage error, or no context to compare |

Ordinary source changes never produce a non-zero exit. Without `--ci` the command prints the full report and exits 0 whenever it could analyse the repository, because the report is the product and the developer decides. Teams that want a gate use `--ci`.

A repository that has adopted the context will usually want the CI job to run on pull requests that change manifests, pipeline definitions or infrastructure files. It is also safe to run on every pull request.

## Limitations

- **Deterministic and shallow.** It reads what the generator reads. It cannot see behavioral change in source code.
- **Vocabulary-based.** Capabilities and conflicts are recognised from a fixed vocabulary. Anything outside it is seen only through the generator's structural statements, if the context has them.
- **Hand-written contexts** are compared by capability words only. Structural comparison needs the generator's statement format.
- **Changes within a component** (a new framework used only inside one project) appear as technology changes of the repository, without naming the component.
- **Declared is not used.** A dependency that is declared but unused is detected like one in use.
- **Removal of a developer-provided statement** is never Material. The repository may simply not show it.
- **Git is supporting evidence only.** It covers committed changes, not the working tree.
- **It does not judge which side is right.** A conflict needs a developer.
