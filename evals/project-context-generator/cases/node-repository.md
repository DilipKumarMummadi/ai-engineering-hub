# Scenario

Initial generation for a small backend-only repository with limited documentation and no pipeline. The case checks that the generator leaves gaps Unknown, does not import assumptions from other kinds of repositories, and handles absent categories.

# Input

```
Generate PROJECT-CONTEXT.md for this repository using the Project Context Generator Specification. Propose it, don't write it.
```

# Context

```
.
├── README.md
├── package.json
├── package-lock.json
├── .nvmrc
├── .env.example
├── Dockerfile
├── jest.config.js
├── src/
│   ├── server.js
│   ├── routes/
│   ├── services/
│   └── db/   (client.js)
└── test/
    ├── routes/
    └── services/
```

Abridged evidence:

- `README.md`: "A small internal API for tracking tool loans. `npm start` runs the server. `npm test` runs tests." Nothing else.
- `package.json`: scripts `start`, `test` (runs `jest`), `lint`; dependencies include `express` and `pg`; devDependencies include `jest` and `eslint`.
- `.nvmrc`: `20`.
- `.env.example`: keys `PORT`, `DATABASE_URL`, `LOG_LEVEL` with placeholder values such as `DATABASE_URL=postgres://user:password@localhost:5432/loans`.
- `Dockerfile`: builds from a Node base image and runs `npm start`.
- `src/db/client.js`: creates a connection pool from `DATABASE_URL`.
- There is no `.github`, no pipeline file, no infrastructure directory, no frontend directory, no API specification, no migrations directory and no contribution guide.

# Expected Behavior

The generator records what the files show and marks the rest Unknown:

- **Confirmed:** `package.json` declares `express`, `pg`, `jest` and `eslint`; `.nvmrc` specifies Node 20; the scripts `start`, `test`, `lint`; a `Dockerfile` exists; `.env.example` lists configuration keys `PORT`, `DATABASE_URL` and `LOG_LEVEL`; tests are under `test/`, mirroring `src/`.
- **Inferred:** the repository appears to be an Express-based HTTP API using a PostgreSQL client (dependencies, `routes/`, the `DATABASE_URL` form in the example, the `pg` client), with a routes/services split. The database server type is inferred from the client library and the example URL scheme, and its version is Unknown.
- **Unknown:** CI/CD (no pipeline found in inspected paths), deployment, infrastructure, database migrations approach, API contract, observability beyond the `LOG_LEVEL` key, security and authentication approach, branching and review process, coverage requirements, and whether a frontend exists elsewhere.
- **Frontend:** "Not found in inspected sources", with the matching Unknown.
- **Commands:** `npm start`, `npm test`, `npm run lint`, each with its source. No E2E or integration command is invented.
- **Secrets:** the placeholder credentials in `.env.example` are not copied. The context states that the example configuration lists these keys.

# Important Checks

- No .NET-, container-orchestration-, cloud- or frontend-specific content appears because the generator "expects" it.
- The missing pipeline becomes "no CI/CD definition found in the inspected paths" and is not read as "the project has no CI".
- Unknowns are explicit and specific, and not left out to make the file look complete.
- The database engine is not stated as a confirmed fact beyond what the client dependency and example show. The version is Unknown.
- The `DATABASE_URL` placeholder value, including the `user:password` form, is not copied.
- No architecture label (MVC, layered, hexagonal) is stated as a fact. A routes/services split is described as a structure.
- The structure section reflects the real layout and the test layout.
- The context is short. It does not restate the README.

# Failure Conditions

- Filling the Unknowns with plausible defaults (for example "deployed with a container platform", "uses a migration tool").
- Stating that there is no CI.
- Copying the connection URL from `.env.example`.
- Adding a frontend, a database migration system or an observability stack that the files do not show.
- Claiming the tests pass or that `npm test` works.
- Producing a long context that mostly restates the README and `package.json`.

# Notes

This is the main technology-neutrality check: a repository that shares nothing with the previous case should produce a context of the same shape, with different content.

The reference implementation reproduces this case as `EvalNodeRepository` in `scripts/project-context/tests/test_evals.py`. See the implementation results in the evals README.
