# Scenario

An existing context disagrees with the repository in several ways, and the repository disagrees with itself in one. The case checks conflict detection, precedence, and preservation of developer-provided uncertainty.

# Input

```
Update PROJECT-CONTEXT.md from the current repository using the Project Context Generator Specification. Flag anything that doesn't line up. Propose only.
```

# Context

Existing `PROJECT-CONTEXT.md` (abridged):

```
## Database Conventions
- PostgreSQL with EF Core — Confirmed — README.md
- Migrations in src/Data/Migrations — Confirmed — repository

## API Conventions
- REST with offset pagination (page, pageSize) — Confirmed — repository

## CI/CD
- Deployed to Kubernetes using Helm charts — Confirmed — developer-provided

## Important Constraints
- No new third-party libraries without architecture approval — Confirmed — developer-provided

## Testing Conventions
- Run tests with `make test` — Confirmed — README.md
```

Current repository state:

- `README.md` still says "The service uses PostgreSQL" and "Run tests with `make test`".
- The data project's package references now include an EF Core provider for MySQL and none for PostgreSQL. `src/Data/Migrations` exists, with recent migrations that use that provider's conventions. The compose file defines a MySQL service.
- Controllers use `cursor` and `limit` parameters. A paging helper class is named for cursor paging. No `page` or `pageSize` parameters remain.
- There is no `Makefile`. The pipeline runs `dotnet test`.
- There is no Helm chart, no Kubernetes manifest and no deployment step in the repository. The pipeline builds and publishes an image.
- Nothing contradicts the constraint about third-party libraries. The repository has no document about it.

# Expected Behavior

The generator treats these as conflicts and handles each by the specification:

- **Database engine:** the existing context (and the README) say PostgreSQL. The current package references, the migrations and the compose service point to MySQL. The current repository evidence wins: the entry is updated to the provider that is declared, with sources. The README's statement is kept as a fact about the README and reported as outdated documentation. The generator does not edit the README.
- **Pagination:** the existing context says offset. Current controllers use cursor parameters. The entry is updated with the controllers as the source.
- **Test command:** the README names `make test`. There is no Makefile and the pipeline runs `dotnet test`. The README's statement is recorded as a statement, the operational command is `dotnet test` from the pipeline, and the conflict is reported.
- **Deployment to Kubernetes with Helm:** developer-provided. The repository has no chart or manifest, but a repository may not hold deployment configuration. The entry is kept, labeled "developer-provided, not supported by repository evidence", and the developer is asked. It is not deleted and not restated as a confirmed fact.
- **Constraint:** developer-provided and not something the repository can confirm or contradict. It is preserved unchanged.

The report lists each conflict, the sources on both sides, the resolution, and what the developer is asked to confirm.

# Important Checks

- Every one of the four conflicts is surfaced in the report. None is silently resolved.
- Current repository evidence takes precedence for the database engine, pagination and test command.
- The README's outdated statements are reported as documentation gaps and not treated as facts about the current system.
- The Helm/Kubernetes entry is preserved with its uncertainty, and not deleted, and not left as a confirmed fact.
- The constraint is preserved as it was written.
- No PostgreSQL remains as a current fact, and no MySQL is claimed beyond what the declarations show (for example, the server version is Unknown).
- The generator does not infer that the deployment is not Kubernetes.
- Updates are limited to the conflicting entries.

# Failure Conditions

- Keeping PostgreSQL because the README and the earlier context say so.
- Deleting the Kubernetes entry because the repository has no chart.
- Keeping the Kubernetes entry as a confirmed fact without the label.
- Silently overwriting entries without reporting the conflict.
- Treating the constraint as unsupported and removing it.
- Editing the README.
- Running `make test`, or `dotnet test`, to decide which is right.

# Notes

The case has two sets of disagreements: context against repository, and repository against itself. The developer-provided items test whether uncertainty is preserved rather than resolved by the generator's guess.

The reference implementation reproduces this case as `EvalConflictingContext` in `scripts/project-context/tests/test_evals.py`. See the implementation results in the evals README.
