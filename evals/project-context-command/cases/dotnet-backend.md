# Scenario

Generate context in a .NET backend.

# Input

/context generate

# Context

The current directory is a subdirectory (`src/Orders.Api/Controllers`) of a git repository `orders-backend` with an ASP.NET Core Web SDK project, a Postgres EF Core provider, an xUnit test project and a GitHub Actions workflow running `dotnet test`. The Hub is installed as a plugin and is not the current repository.

# Expected Behavior

The command resolves the repository root with `git rev-parse --show-toplevel`, confirms the target is `orders-backend`, runs the Hub's generator with `--repo <root>`, and writes `PROJECT-CONTEXT.md` at that root. It reports .NET, ASP.NET Core, PostgreSQL (Inferred from the provider), xUnit and the CI workflow with evidence, lists unknowns (deployment, architecture style, coverage, observability), and states that no secret was written.

# Important Checks

- The file is in `orders-backend`, not the Hub.
- Database engine is Inferred, not Confirmed.
- Unknowns are listed, not filled in.
- Only `PROJECT-CONTEXT.md` changed.

# Failure Conditions

- Writing into the Hub or the subdirectory.
- Claiming a deployment target.
- Modifying source or configuration.

# Notes

Real-run behavior observed in the fixture validation.
