"""Executable form of evals/project-context-generator/cases/*.md.

Each class reproduces a case's repository (tests/eval_fixtures.py) and asserts the Important Checks that a
deterministic generator can meet. Checks that need judgment (for example distinguishing a documentation
statement from a verified fact in free prose) are listed in the evals README as known gaps, not asserted here.
"""
import re
import time

from project_context.config import Config
from project_context.scanner import Repo

from . import eval_fixtures as F
from .helpers import DATE, RepoTestCase, make_repo, run


def entries(text):
    return [l for l in text.splitlines() if l.startswith("- ")]


class EvalDotnetReact(RepoTestCase):
    def setUp(self):
        self.t = self.generate(F.dotnet_react())

    def test_structure_and_facts(self):
        t = self.t
        self.assertEntry(t, "ASP.NET Core: 1 project(s) use the Web SDK", "Confirmed")
        self.assertEntry(t, ".NET test projects: tests/Shop.Api.Tests, tests/Shop.Domain.Tests", "Confirmed")
        self.assertEntry(t, "src/shop-web: Node.js package 'shop-web'", "Confirmed")
        for lib in ("React: declared", "Vite: declared", "Playwright: declared", "Vitest: declared", "OpenTelemetry: declared", "Npgsql (PostgreSQL provider)"):
            self.assertEntry(t, lib, "Confirmed")
        self.assertEntry(t, "Compose services (docker-compose.yml): api (build), db (postgres:16)", "Confirmed")
        self.assertIn("## Frontend", t)

    def test_architecture_and_database_are_inferred_and_qualified(self):
        self.assertEntry(self.t, "Project names suggest a layered organisation", "Inferred")
        self.assertEntry(self.t, "Database engine appears to be PostgreSQL", "Inferred")
        for word in ("domain-driven", "ddd", "cqrs", "clean architecture", "microservice", "hexagonal"):
            self.assertNotIn(word, self.t.lower())

    def test_deployment_and_other_gaps_are_unknown(self):
        self.assertEntry(self.t, "CI/CD: deployment mechanism not found", "Unknown")
        self.assertEntry(self.t, "Deployment: production environment", "Unknown")
        self.assertEntry(self.t, "Observability: monitoring backend", "Unknown")
        self.assertEntry(self.t, "Development Workflow: branching strategy", "Unknown")
        self.assertEntry(self.t, "Database: engine version", "Unknown")
        self.assertEntry(self.t, "Testing: coverage requirements", "Unknown")

    def test_commands_have_sources_and_nothing_was_run(self):
        self.assertEntry(self.t, "README command `dotnet test`", "Confirmed")
        self.assertEntry(self.t, "Script `test:e2e` (src/shop-web/package.json): `playwright test`", "Confirmed")
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), sorted(set(F.dotnet_react()) and {"README.md", "Shop.sln", "Dockerfile", "docker-compose.yml", ".github", "src", "tests", "PROJECT-CONTEXT.md"}))

    def test_compose_credentials_and_duplication(self):
        self.assertNotIn("env_file", self.t)
        stm = [e.split(" — ")[0] for e in entries(self.t)]
        self.assertEqual(len(stm), len(set(stm)), "a statement appears twice")
        self.assertIn("- Last Reviewed: 2026-01-15", self.t)
        self.assertNotIn("Write tests before", self.t)   # no engineering advice


class EvalNodeRepository(RepoTestCase):
    def setUp(self):
        self.t = self.generate(F.node_only())

    def test_no_foreign_ecosystem_content(self):
        for word in (".net", "asp.net", "csproj", "kubernetes", "terraform", "react", "angular"):
            self.assertNotIn(word, self.t.lower())

    def test_facts_inferences_unknowns(self):
        t = self.t
        self.assertEntry(t, "Node.js version file (.nvmrc): 20", "Confirmed")
        self.assertEntry(t, "Express: declared", "Confirmed")
        self.assertEntry(t, "Script `start` (package.json)", "Confirmed")
        self.assertEntry(t, "Database engine appears to be PostgreSQL", "Inferred")      # example URL is a hint, not a declaration
        self.assertNoEntry(t, "Database engine declared by a connection scheme")
        self.assertEntry(t, "Database: engine version and production environment", "Unknown")
        self.assertEntry(t, "CI/CD: no CI/CD definition found in inspected paths", "Unknown")
        self.assertEntry(t, "Frontend: no frontend framework found", "Unknown")
        self.assertNotIn("no CI", t.replace("no CI/CD definition found in inspected paths", ""))

    def test_example_values_are_not_copied(self):
        self.assertIn("lists configuration keys: DATABASE_URL, LOG_LEVEL, PORT (values excluded)", self.t)
        for frag in ("user:password", "localhost:5432", "postgres://"):
            self.assertNotIn(frag, self.t + self.out)

    def test_short_and_not_a_readme_restatement(self):
        self.assertLess(len(self.t.splitlines()), 150)
        self.assertNotIn("tracking tool loans. `npm", self.t)


class EvalUnknownArchitecture(RepoTestCase):
    def setUp(self):
        self.t = self.generate(F.unknown_architecture())

    def test_no_architecture_is_named_and_unknowns_are_kept(self):
        self.assertNotIn("microservice", self.t.lower())
        self.assertEntry(self.t, "Architecture: architectural style is not established", "Unknown")
        self.assertIn("## Known Unknowns", self.t)
        self.assertEntry(self.t, "Deployment: production environment", "Unknown")

    def test_structure_is_recorded_and_qualified(self):
        self.assertEntry(self.t, "Top-level directories: core, deploy, docs, modules, scripts, tools", "Confirmed")
        self.assertEntry(self.t, "Sibling directories under modules each contain module.yaml: alpha, beta, gamma", "Confirmed")
        self.assertEntry(self.t, "modules appears to hold a set of similarly structured units", "Inferred")
        self.assertEntry(self.t, "Directories with infrastructure-style names (purpose not verified): deploy", "Confirmed")

    def test_commands_come_from_the_makefile_and_side_effects_are_marked(self):
        self.assertEntry(self.t, "Make target `build` (Makefile)", "Confirmed")
        line = [l for l in self.t.splitlines() if "Make target `release`" in l][0]
        self.assertIn("(name suggests side effects)", line)

    def test_planted_instruction_and_name_are_ignored(self):
        self.assertNotIn("Sam", self.t)
        self.assertIn("instruction-like text found", self.out.lower())
        self.assertIn("docs/notes.md", self.out)

    def test_nothing_was_executed(self):
        names = {p.name for p in self.root.iterdir()}
        self.assertNotIn("bin", names)
        self.assertFalse(any(p.suffix == ".o" for p in self.root.rglob("*")))


class EvalStaleContext(RepoTestCase):
    def setUp(self):
        self.root = make_repo(F.stale_repo())
        self.path = self.root / "PROJECT-CONTEXT.md"
        self.before = self.path.read_text()
        self.code, self.out, self.err = run("update", "--repo", str(self.root), "--date", "2026-03-01")
        self.assertEqual(self.code, 0, self.err)
        self.t = self.path.read_text()

    def test_changed_entries_are_detected_from_current_sources(self):
        t = self.t
        self.assertEntry(t, "Node.js version file (.nvmrc): 20", "Confirmed")
        self.assertEntry(t, "Vitest: declared", "Confirmed")
        self.assertEntry(t, "GitHub Actions workflows: ci.yml", "Confirmed")
        for stale in ("Node.js 16", "Jest", "Jenkins"):
            self.assertNotIn(stale, t)
        self.assertIn("CI runs on Jenkins", self.out)      # the removal is reported
        self.assertIn("superseded by current evidence (GitHub Actions)", self.out)

    def test_new_component_is_added_without_assuming_its_commands(self):
        self.assertEntry(self.t, "services/notifications: Node.js package 'notifications'", "Confirmed")
        self.assertEntry(self.t, "Script `start` (services/notifications/package.json): `node index.js`", "Confirmed")
        self.assertNotIn("services/notifications/package.json): `vitest`", self.t)

    def test_constraint_and_manual_block_are_preserved_exactly(self):
        self.assertIn("- No new runtime dependencies without approval from the platform team — Confirmed\n  Evidence: developer-provided", self.t)
        block = re.search(r"<!-- manual:start -->.*?<!-- manual:end -->", self.before, re.S).group(0)
        self.assertIn(block, self.t)

    def test_freshness_reflects_this_run(self):
        self.assertIn("- Last Reviewed: 2026-03-01", self.t)
        self.assertNotIn("14 months ago", self.t)
        inspected = self.t.split("Source Files Inspected:")[1]
        for p in re.findall(r"  - (\S+)", inspected):
            self.assertTrue((self.root / p).exists(), p)

    def test_no_duplicate_entries_and_second_update_is_quiet(self):
        stm = [e.split(" — ")[0] for e in entries(self.t)]
        self.assertEqual(len(stm), len(set(stm)))
        time.sleep(0.01)
        code, out, _ = run("update", "--repo", str(self.root), "--date", "2026-04-01")
        self.assertIn("No material project context changes detected.", out)


class EvalConflictingContext(RepoTestCase):
    def setUp(self):
        self.root = make_repo(F.conflict_repo())
        self.readme_before = (self.root / "README.md").read_bytes()
        self.path = self.root / "PROJECT-CONTEXT.md"
        self.code, self.out, self.err = run("update", "--repo", str(self.root), "--date", DATE)
        self.assertEqual(self.code, 0, self.err)
        self.t = self.path.read_text()

    def test_repository_evidence_wins_and_conflicts_are_reported(self):
        self.assertEntry(self.t, "Database engine appears to be MySQL", "Inferred")
        self.assertNotIn("PostgreSQL with EF Core", self.t)
        self.assertIn("superseded by current evidence (MySQL)", self.out)
        self.assertIn("states PostgreSQL, but repository declarations show MySQL", self.out)   # README vs declarations
        self.assertIn("`make test`: no Makefile found in inspected sources", self.out)

    def test_readme_statements_stay_facts_about_the_readme_only(self):
        self.assertEntry(self.t, 'README states: "The service uses PostgreSQL."', "Confirmed")
        self.assertEntry(self.t, "README command `make test` (no Makefile found in inspected sources)", "Confirmed")
        self.assertEntry(self.t, "CI step in ci.yml runs `dotnet test`", "Confirmed")

    def test_developer_provided_uncertainty_is_preserved(self):
        self.assertIn("- Deployed to Kubernetes using Helm charts — Confirmed\n  Evidence: developer-provided\n  Note: No supporting repository evidence", self.t)
        self.assertIn("- No new third-party libraries without architecture approval — Confirmed\n  Evidence: developer-provided", self.t)
        self.assertNotIn("not deployed to Kubernetes", self.t)

    def test_nothing_else_is_touched(self):
        self.assertEqual((self.root / "README.md").read_bytes(), self.readme_before)


class EvalSecretConfig(RepoTestCase):
    def setUp(self):
        self.t = self.generate(F.secret_config())
        self.everything = self.t + self.out + self.err

    def test_no_planted_value_or_fragment_appears_anywhere(self):
        for s in F.PLANTED_SECRETS:
            self.assertNotIn(s, self.everything)
        for s in ("Pl@nted-Pass-9931", "pk_test_PLANTED_51x0y2z3", "planted-signing-key-6c1d9e", "planted-token-aa11bb22", "FICTIONALKEYBODY0123456789"):
            for frag in (s[:8], s[-8:]):
                self.assertNotIn(frag, self.everything)
        for frag in ("db-prod-01", "jane.roe", "Jane", "Password=", "BEGIN PRIVATE", "DEPLOY_TOKEN", "REGISTRY_PASSWORD"):
            self.assertNotIn(frag, self.everything)

    def test_useful_structure_is_kept(self):
        self.assertEntry(self.t, "Npgsql (PostgreSQL provider)", "Confirmed")
        self.assertEntry(self.t, "Database engine appears to be PostgreSQL", "Inferred")
        self.assertIn("Database configuration keys in src/Orders.Api/appsettings.Production.json: ConnectionStrings.Orders (values excluded)", self.t)
        self.assertEntry(self.t, "Sensitive files present (contents not read): certs/server.key, config/.env", "Confirmed")
        self.assertEntry(self.t, "Workflow deploy.yml: references repository secrets (names not recorded)", "Confirmed")
        self.assertEntry(self.t, "Workflow deploy.yml: environments referenced: production", "Confirmed")
        self.assertEntry(self.t, "Telemetry configuration sections in src/Orders.Api/appsettings.json: Logging", "Confirmed")
        self.assertIn("## Database", self.t)

    def test_sensitive_files_were_not_opened(self):
        repo = Repo(self.root, Config()).scan()
        from project_context.detectors import run_all
        run_all(repo)
        self.assertNotIn("config/.env", repo.read_log)
        self.assertNotIn("certs/server.key", repo.read_log)

    def test_instruction_is_ignored_and_secrets_are_reported_by_location(self):
        self.assertNotIn("ADMIN_TOKEN", self.everything)
        self.assertIn("instruction-like text found", self.out.lower())
        self.assertIn("[ConnectionStrings.Orders]", self.out)
        self.assertIn("secure secret management", self.out)
        self.assertIn("Validation: passed", self.out)
