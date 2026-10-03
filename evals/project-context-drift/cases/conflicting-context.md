# Scenario

The context and the repository disagree about a technology. The case checks that the conflict is surfaced, that neither side is chosen silently, and that a developer-provided entry is handled honestly.

# Input

```
Compare PROJECT-CONTEXT.md with the repository using the Project Context Drift Specification. If they disagree, tell me, and don't decide for me.
```

# Context

Existing `PROJECT-CONTEXT.md`:

```
## Frontend
- Frontend: Angular — Confirmed — developer-provided

## Database
- PostgreSQL with EF Core — Confirmed — src/Data/Data.csproj

## CI/CD
- CI runs on Jenkins — Confirmed — Jenkinsfile
```

Current repository: `src/web/package.json` declares `react` and `react-dom`, with no Angular packages; `src/Data/Data.csproj` references `Pomelo.EntityFrameworkCore.MySql` and `docker-compose.yml` uses a `mysql:8` image; the `Jenkinsfile` is gone and `.github/workflows/ci.yml` exists.

# Expected Behavior

Three conflicts, each reported under **Conflicts** and in Material Changes:

- Frontend: the context names Angular; the repository shows React. The entry is developer-provided and is left as it is.
- Database: the context names PostgreSQL; the repository shows MySQL.
- CI/CD: the context names Jenkins; the repository shows GitHub Actions.

Each states that repository evidence is current and the context statement is potentially stale, and asks a developer to decide. Status is DRIFT DETECTED.

# Important Checks

- All three conflicts are reported, including the one from a developer-provided entry.
- The report says "conflict". It does not say the context is wrong, or silently adopt the repository's answer.
- Evidence paths are given for the repository side.
- No file is changed.

# Failure Conditions

- Hiding the Angular conflict because the entry is developer-provided.
- Reporting a conflict where the context and the repository agree.
- Resolving the conflict in the report by rewording the context.
- Missing the database conflict because EF Core appears in both.

# Notes

The conflict vocabulary is small (database engine, CI system, test framework, frontend framework, package manager). Conflicts outside it appear as a new capability plus a stale statement.

The reference implementation reproduces this case as `EvalConflictingContext` in `scripts/project-context/tests/test_drift_evals.py`. Related checks are in `test_drift.py`.
