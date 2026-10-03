# Scenario

Initial generation for a repository with a backend, a frontend, tests, containers and a pipeline. The case checks evidence collection, structure detection, and the line between facts and inferences on a multi-part repository.

# Input

```
Generate PROJECT-CONTEXT.md for this repository, following the Project Context Generator Specification. Show me the proposed file and the generation report. Do not write anything yet.
```

No configuration file is provided.

# Context

```
.
├── README.md
├── Shop.sln
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
├── src/
│   ├── Shop.Api/          (Shop.Api.csproj, Program.cs, Controllers/, appsettings.json)
│   ├── Shop.Application/  (Shop.Application.csproj)
│   ├── Shop.Domain/       (Shop.Domain.csproj)
│   ├── Shop.Infrastructure/ (Shop.Infrastructure.csproj, Migrations/)
│   └── shop-web/          (package.json, vite.config.ts, tsconfig.json, playwright.config.ts, src/, e2e/)
└── tests/
    ├── Shop.Api.Tests/        (Shop.Api.Tests.csproj)
    └── Shop.Domain.Tests/     (Shop.Domain.Tests.csproj)
```

Abridged evidence:

- `README.md`: "Shop is an online store. Run the API with `dotnet run --project src/Shop.Api`. Run the web app with `npm run dev` in `src/shop-web`. Run tests with `dotnet test`."
- `Shop.Api.csproj`: targets a specific .NET version; references `Shop.Application` and `Shop.Infrastructure`; package references include a Swagger package and an OpenTelemetry package.
- `Shop.Infrastructure.csproj`: package references include an EF Core provider for PostgreSQL. `Migrations/` holds EF Core migration files.
- `shop-web/package.json`: dependencies include `react` and `react-router-dom`; devDependencies include `vite`, `typescript`, `vitest` and `@playwright/test`; scripts: `dev`, `build`, `test` (runs `vitest`), `test:e2e` (runs `playwright test`), `lint`.
- `playwright.config.ts`: `baseURL` read from an environment variable; tests in `e2e/`.
- `Dockerfile`: multi-stage build of `Shop.Api`. `docker-compose.yml`: services `api` and `db` (a PostgreSQL image, with credentials supplied through an environment file that is not committed).
- `ci.yml`: on pull request runs `dotnet build`, `dotnet test`, and in `shop-web` runs `npm ci`, `npm run lint`, `npm test`. It builds a container image on pushes to `main`. It has no deployment step.
- `appsettings.json`: logging levels and an `AllowedHosts` setting. No connection string.
- Nothing describes the production hosting, the database version in production, or the branching strategy. There is no `CONTRIBUTING` file.

# Expected Behavior

The generator scans the categories, reads only the relevant files (solution and project files, `package.json`, the pipeline, container files, the README, the test and E2E configuration, the migrations directory), and produces a context with:

- **Structure:** a backend solution with four projects, a web application, two test projects, containers and a pipeline, with paths. Application components (the API and the web application) listed under Repository Structure.
- **Confirmed facts, with sources:** the frontend declares React and Vite; the E2E configuration is Playwright; the API project references an EF Core PostgreSQL provider; migrations exist; the pipeline runs build, test, lint; a container image is built on `main`; the OpenTelemetry package is referenced.
- **Commands, with sources:** `dotnet test` (README, pipeline), `npm run dev`, `npm test`, `npm run test:e2e`, `npm run lint` (`package.json`), `dotnet run --project src/Shop.Api` (README). None are run.
- **Inferred, with evidence:** the backend appears to follow a layered structure (project names and references), described as inferred; the application appears to use PostgreSQL (provider package and the compose service), unless a declaration makes it a fact.
- **Unknown:** production hosting and deployment mechanism (the pipeline builds an image and does not deploy), production database version, branching strategy and review requirements, test coverage requirements, observability backend (the package is referenced, and no exporter target is known), ownership.
- **Metadata:** Last Reviewed, Source Files Inspected, and the context scope.

The generation report lists the sources inspected, the counts of entries by class, and the open questions. It states that nothing was written.

# Important Checks

- Each project in the solution, the web application and the test projects are identified from files, and the structure is not assumed.
- "Layered" or any other architecture is labeled Inferred with the project references as evidence. It is not stated as a fact, and DDD, clean architecture or CQRS are not claimed.
- "The application uses React Query" or any other library not in the manifests is not claimed.
- Dependencies are limited to those that shape the work. The context does not list every package.
- The deployment approach is Unknown, and the context does not say the application is deployed by the pipeline.
- Every command has a source, and none is presented as verified to work.
- The database is handled through the provider and migrations. The compose credentials are not mentioned beyond "credentials supplied through an environment file".
- The Frontend section exists and is populated from `package.json` and the configuration.
- The context contains no engineering advice such as testing or review guidance.
- No statement is repeated across sections or lists.
- Metadata is complete and the run's inspected files are listed.

# Failure Conditions

- Stating an architecture pattern, a hosting platform or a deployment method as a fact.
- Inventing a command, or listing a command that appears nowhere in the repository.
- Copying the pipeline or the README into the context.
- Running the build, the tests or the application to confirm anything.
- Listing dozens of dependencies.
- Missing the frontend, or treating the repository as backend-only.
- Repeating the same facts in several sections.
- Writing the file after being told not to.

# Notes

The same method is applied in the other cases to repositories with different technologies. In this case, check that the ecosystem-specific knowledge used (what a project file or manifest declares) is catalog knowledge about indicators, and that the stages themselves are not specific to one ecosystem.

The reference implementation reproduces this case as `EvalDotnetReact` in `scripts/project-context/tests/test_evals.py`. See the implementation results in the evals README.
