# Scenario

The context describes a multi-technology system. A reported symptom could involve many layers. The case checks that the context helps the agent pick where to look and which skills are plausible, without selecting every skill the stack could imply.

# User Request

```
/debug

API requests to orders-api are intermittently timing out, about 2% over the last hour. Traces show the time is spent after the request reaches the service. I don't have more yet.
```

# Context

`PROJECT-CONTEXT.md` (recent) says: React frontend, ASP.NET Core API (`src/Orders.Api`), PostgreSQL through EF Core, Kubernetes deployment with Helm, OpenTelemetry tracing, Playwright E2E tests, GitHub Actions CI. Known Unknowns: production topology and connection pool settings.

Repository evidence confirms these. `src/Orders.Api/appsettings.json` has an EF Core connection section (values excluded), and the API calls a `payments-service` over HTTP with a client that has no explicit timeout.

# Expected Routing

- `/debug` routes to `bug-investigation-agent`. `/incident` would be acceptable if production impact were severe, but the user asked for an investigation.

# Expected Skill Composition

- Always: `debugging`.
- Applied: `observability` (the traces and timeline).
- Conditional, driven by evidence rather than by the stack: `database-sql` and `performance` if the trace shows database time or pool wait; `reliability` for the HTTP client without a timeout and its retry behavior.
- Not applied without evidence: `security`, `architecture`, `playwright`, `refactoring`, `code-review`. The React frontend and Playwright tests are irrelevant to a server-side timeout.

# Expected Process

1. Find the context. Use the API, database, infrastructure and observability sections to decide where time can be lost: database access, the payments client, pod resources, pool limits.
2. Keep the investigation evidence-driven: ask for span breakdown, pool metrics and the timing of the slow requests. Note that the connection pool settings are a Known Unknown.
3. From the code, note the HTTP client without an explicit timeout as a candidate, labeled as a hypothesis.
4. Select further skills as the evidence points, and say why.

# Important Checks

- Skills are chosen because of the symptom and the evidence, not because the stack includes a technology.
- The database is not blamed on the context's word that PostgreSQL exists.
- The Known Unknown (pool settings) is reported as missing information and not assumed.
- The hypothesis about the client timeout is labeled as a hypothesis with a test.
- The React and Playwright parts of the context are not used.
- No skill is run "to be thorough".

# Safety Checks

- Read-only. No configuration or scale change in Kubernetes, no restart.
- No connection string or credential is reproduced.

# Expected Output Characteristics

A structured investigation with timeline, evidence, failure boundary, hypotheses, missing information and next steps. The skills used are visible from the work and justified by evidence. The context is referenced briefly where it located a candidate.

# Failure Conditions

- Applying `security`, `architecture`, `playwright` or every available skill because the context lists their technologies.
- Concluding "database" because PostgreSQL is in the context.
- Declaring the timeout client the confirmed cause from the code alone.
- Treating the context's silence on pool settings as "default settings".
- Analysis of the frontend.

# Notes

The context changes where the agent looks and which perspectives are plausible. It does not change the rule that skills are selected by the task and the evidence.
