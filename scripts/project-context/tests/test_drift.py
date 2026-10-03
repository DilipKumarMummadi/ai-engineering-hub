"""Drift detection: fixture repositories are generated, changed, and compared. Nothing scans the Hub."""
import hashlib
import json
import shutil
import subprocess
import unittest

from .eval_fixtures import conflict_repo, dotnet_react, node_only, stale_repo, unknown_architecture, CONFLICT_CONTEXT, STALE_CONTEXT
from .helpers import DATE, make_repo, run

WORKFLOW = "name: CI\non:\n  pull_request:\njobs:\n  test:\n    steps:\n      - run: npm test\n"
TOKEN = "sk_live_" + "Zq81LmXv03TdWpRc92HnKa5B"   # planted; must never appear in any output


def tree_hash(root):
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(root)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


class DriftCase(unittest.TestCase):
    def repo(self, files):
        self.root = make_repo(files)
        code, out, err = run("generate", "--repo", str(self.root), "--date", DATE)
        self.assertEqual(code, 0, out + err)
        return self.root

    def drift(self, *extra, code=0):
        c, out, err = run("drift", "--repo", str(self.root), "--date", DATE, *extra)
        self.assertEqual(c, code, out + err)
        self.out = out
        return out

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def section(self, out, title):
        """Text of one '## title' section."""
        parts = out.split(f"## {title}\n")
        return parts[1].split("\n## ")[0] if len(parts) > 1 else ""

    def assertStatus(self, out, status):
        self.assertIn(f"Status: {status}", out)


class TestNoFalsePositives(DriftCase):
    def test_no_drift(self):
        self.repo(dotnet_react())
        out = self.drift()
        self.assertStatus(out, "NO DRIFT")
        self.assertNotIn("## Material Changes", out)
        self.assertIn("No action needed", out)

    def test_source_only_changes_are_not_drift(self):
        self.repo(dotnet_react())
        self.write("src/Shop.Api/Controllers/OrdersController.cs", "class Changed { void NewMethod() {} }")
        self.write("src/Shop.Api/Controllers/NewController.cs", "class N {}")
        self.write("src/shop-web/src/App.tsx", "export const App = () => null")
        (self.root / "src/Shop.Domain/Shop.Domain.csproj").touch()
        self.assertStatus(self.drift(), "NO DRIFT")
        self.drift("--ci")

    def test_tests_and_comments_only(self):
        self.repo(node_only())
        self.write("test/routes/b.test.js", "test('new', () => {})")
        self.write("src/server.js", "// a different comment\n")
        self.assertStatus(self.drift(), "NO DRIFT")

    def test_documentation_only_changes(self):
        self.repo(node_only())
        self.write("README.md", "Reworded. A completely different description of the loans API.\n")
        self.write("docs/guide.md", "# Guide\nUses Kubernetes and Terraform in prose only.\n")
        out = self.drift()
        self.assertStatus(out, "NO DRIFT")
        self.assertNotIn("Kubernetes", self.section(out, "Material Changes"))

    def test_build_output_changes_are_ignored(self):
        self.repo(node_only())
        self.write("dist/package.json", json.dumps({"dependencies": {"vue": "3"}}))
        self.write("node_modules/x/Dockerfile", "FROM scratch")
        self.assertStatus(self.drift(), "NO DRIFT")

    def test_empty_minimal_repository(self):
        self.root = make_repo({})
        self.assertEqual(run("generate", "--repo", str(self.root), "--date", DATE)[0], 0)
        self.assertStatus(self.drift(), "NO DRIFT")

    def test_unchanged_technology_is_not_drift(self):
        self.repo(dotnet_react())
        self.write("src/shop-web/package.json", json.dumps({"name": "shop-web", "dependencies": {"react": "^18.3.1", "react-router-dom": "^6"},
            "devDependencies": {"vite": "^5", "typescript": "^5", "vitest": "^1", "@playwright/test": "^1.40"},
            "scripts": {"dev": "vite", "build": "vite build", "test": "vitest", "test:e2e": "playwright test", "lint": "eslint ."}}))
        self.assertStatus(self.drift(), "NO DRIFT")


class TestTechnologyAndArchitecture(DriftCase):
    def pkg(self, **deps):
        base = {"name": "loans", "scripts": {"start": "node src/server.js", "test": "jest", "lint": "eslint ."},
                "dependencies": {"express": "^4.18.0", "pg": "^8.11.0"}, "devDependencies": {"jest": "^29", "eslint": "^8"}}
        base["dependencies"].update(deps)
        return json.dumps(base)

    def test_new_technology(self):
        self.repo(node_only())
        self.write("package.json", self.pkg(fastify="^4"))
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")
        self.assertIn("New repository evidence detected: Fastify", self.section(out, "Material Changes"))
        self.assertIn("package.json", out)

    def test_removed_technology(self):
        self.repo(node_only())
        self.write("package.json", json.dumps({"name": "loans", "scripts": {"start": "node src/server.js"}, "dependencies": {"pg": "^8"}, "devDependencies": {"jest": "^29"}}))
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")
        self.assertIn("Express is documented in the context but is no longer detected", out)
        self.assertIn("Stale Context", out)

    def test_runtime_version_change(self):
        self.repo(node_only())
        self.write(".nvmrc", "22\n")
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")
        self.assertIn("Node.js version changed: the context records 20; the repository declares 22", out)

    def test_new_service_project(self):
        self.repo(dotnet_react())
        self.write("src/Payment/Payment.csproj", '<Project Sdk="Microsoft.NET.Sdk.Worker"></Project>')
        out = self.drift()
        self.assertStatus(out, "REVIEW RECOMMENDED")
        self.assertIn("src/Payment", self.section(out, "Potentially Material"))
        self.assertIn("src/Payment/Payment.csproj", out)
        self.drift("--ci")   # potentially material does not fail CI

    def test_removed_service_project(self):
        self.repo(dotnet_react())
        shutil.rmtree(self.root / "src/shop-web")
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")
        self.assertIn("src/shop-web is documented but no longer detected", self.section(out, "Material Changes"))

    def test_major_restructuring(self):
        self.repo(unknown_architecture())
        for d in ("alpha", "beta", "gamma"):
            self.write(f"{d}/main.go", "package x")
        out = self.drift()
        self.assertIn("Major repository restructuring", out)
        self.assertStatus(out, "DRIFT DETECTED")

    def test_new_database_configuration(self):
        self.repo(unknown_architecture())
        self.write("db/migrations/001_init.sql", "create table t(id int);")
        out = self.drift()
        self.assertIn("migration infrastructure introduced", out)


class TestCiInfrastructure(DriftCase):
    def test_new_ci_workflow(self):
        self.repo(stale_repo())
        self.write(".github/workflows/deploy.yml", WORKFLOW)
        out = self.drift()
        self.assertIn("New workflow detected: deploy.yml", self.section(out, "Potentially Material"))
        self.assertStatus(out, "REVIEW RECOMMENDED")

    def test_removed_ci_workflow_among_several(self):
        files = stale_repo()
        files[".github/workflows/deploy.yml"] = WORKFLOW
        self.repo(files)
        (self.root / ".github/workflows/deploy.yml").unlink()
        out = self.drift()
        self.assertIn("Workflow deploy.yml is documented but no longer detected", out)
        self.assertStatus(out, "REVIEW RECOMMENDED")

    def test_removed_only_ci_is_material(self):
        self.repo(dotnet_react())
        shutil.rmtree(self.root / ".github")
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")
        self.assertIn("GitHub Actions is documented in the context but is no longer detected", self.section(out, "Material Changes"))
        self.drift("--ci", code=1)

    def test_new_ci_platform(self):
        self.repo(node_only())
        self.write(".github/workflows/ci.yml", WORKFLOW)
        self.assertIn("New repository evidence detected: GitHub Actions", self.section(self.drift(), "Material Changes"))

    def test_new_docker_configuration(self):
        self.repo(unknown_architecture())
        self.write("Dockerfile", "FROM golang:1.22\n")
        out = self.drift()
        self.assertIn("New repository evidence detected: Docker", self.section(out, "Material Changes"))
        self.assertIn("Infrastructure", out)

    def test_removed_docker_configuration(self):
        self.repo(node_only())
        (self.root / "Dockerfile").unlink()
        out = self.drift()
        self.assertIn("Docker is documented in the context but is no longer detected", self.section(out, "Material Changes"))

    def test_new_terraform_configuration(self):
        self.repo(node_only())
        self.write("terraform/main.tf", 'provider "aws" {}\nterraform { backend "s3" {} }\n')
        out = self.drift()
        self.assertIn("New repository evidence detected: Terraform", self.section(out, "Material Changes"))
        self.assertIn("terraform/main.tf", out)

    def test_container_base_image_is_not_a_project_technology(self):
        self.repo(unknown_architecture())
        self.write("Dockerfile", "FROM python:3.12\nFROM node:22\n")
        out = self.drift()
        self.assertIn("Docker", self.section(out, "Material Changes"))
        self.assertNotIn("Python", out)
        self.assertNotIn("Node.js", out)

    def test_directory_named_like_a_tool_is_not_evidence(self):
        self.repo(node_only())
        (self.root / "kubernetes").mkdir()
        self.write("kubernetes/notes.txt", "x")
        self.assertNotIn("Kubernetes", self.section(self.drift(), "Material Changes"))


class TestStaleAndConflict(DriftCase):
    def test_stale_context_statement(self):
        self.root = make_repo(node_only())
        (self.root / "PROJECT-CONTEXT.md").write_text(
            "# Project Context\n\n## Infrastructure\n\n- Repository contains Kubernetes deployment manifests.\n", encoding="utf-8")
        before = tree_hash(self.root)
        out = self.drift()
        stale = self.section(out, "Stale Context")
        self.assertIn("Repository contains Kubernetes deployment manifests.", stale)
        self.assertIn("Nothing was deleted", stale)
        self.assertEqual(before, tree_hash(self.root))

    def test_hand_written_stale_and_conflicting_context(self):
        self.root = make_repo(stale_repo())
        (self.root / "PROJECT-CONTEXT.md").write_text(STALE_CONTEXT, encoding="utf-8")
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")
        conflicts = self.section(out, "Conflicts")
        self.assertIn("Jenkins", conflicts)
        self.assertIn("GitHub Actions", conflicts)
        self.assertIn("Jest", conflicts)
        self.assertIn("Node.js version changed", out)
        self.assertNotIn("Express is documented", out)      # unchanged entries are not reported

    def test_frontend_conflict(self):
        self.root = make_repo(dotnet_react())
        (self.root / "PROJECT-CONTEXT.md").write_text("# Project Context\n\n## Frontend\n\n- Angular — Confirmed — developer-provided\n", encoding="utf-8")
        out = self.drift()
        conflicts = self.section(out, "Conflicts")
        self.assertIn("names Angular", conflicts)
        self.assertIn("shows React", conflicts)
        self.assertIn("developer-provided", conflicts)
        self.assertIn("potentially stale", conflicts)

    def test_database_conflict_from_generated_context(self):
        self.repo(node_only())
        self.write("package.json", json.dumps({"name": "loans", "dependencies": {"express": "4", "oracledb": "6"}, "devDependencies": {"jest": "29"}}))
        (self.root / ".env.example").unlink()
        (self.root / "Dockerfile").unlink()
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")

    def test_developer_provided_entries_are_not_called_material_when_unverifiable(self):
        self.root = make_repo(conflict_repo())
        (self.root / "PROJECT-CONTEXT.md").write_text(CONFLICT_CONTEXT, encoding="utf-8")
        out = self.drift()
        self.assertIn("developer-provided", out)


class TestModes(DriftCase):
    def test_multiple_simultaneous_categories(self):
        self.repo(dotnet_react())
        shutil.rmtree(self.root / ".github")
        (self.root / "Dockerfile").unlink()
        self.write("terraform/main.tf", 'provider "aws" {}')
        self.write("src/Payment/Payment.csproj", '<Project Sdk="Microsoft.NET.Sdk.Worker"></Project>')
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")
        material = self.section(out, "Material Changes")
        for heading in ("### Infrastructure", "### CI/CD"):
            self.assertIn(heading, material)
        self.assertIn("Potentially Material", out)
        self.assertIn("src/Payment", out)

    def test_ci_mode_is_concise_and_fails_only_on_material_drift(self):
        self.repo(node_only())
        self.drift("--ci")
        self.write("terraform/main.tf", 'provider "aws" {}')
        out = self.drift("--ci", code=1)
        self.assertNotIn("# Project Context Drift Report", out)
        self.assertLess(len(out.splitlines()), 12)
        self.assertIn("DRIFT DETECTED (", out)
        self.assertIn("Terraform", out)

    def test_ci_mode_does_not_modify_the_repository(self):
        self.repo(node_only())
        self.write("terraform/main.tf", 'provider "aws" {}')
        before = tree_hash(self.root)
        self.drift("--ci", code=1)
        self.drift()
        self.assertEqual(before, tree_hash(self.root))

    def test_ci_flag_only_for_drift(self):
        self.repo(node_only())
        c, out, err = run("generate", "--repo", str(self.root), "--ci")
        self.assertEqual(c, 2)
        self.assertIn("--ci", err)

    def test_check_is_an_alias(self):
        self.repo(node_only())
        c, out, _ = run("check", "--repo", str(self.root), "--date", DATE)
        self.assertEqual(c, 0)
        self.assertIn("Status: NO DRIFT", out)

    def test_missing_context(self):
        self.root = make_repo(node_only())
        c, out, err = run("drift", "--repo", str(self.root))
        self.assertEqual(c, 2)
        self.assertIn("no existing context", err)
        self.assertFalse((self.root / "PROJECT-CONTEXT.md").exists())

    def test_non_git_repository(self):
        self.repo(node_only())
        out = self.drift()
        self.assertNotIn("Files changed since", out)
        self.assertStatus(out, "NO DRIFT")

    @unittest.skipUnless(shutil.which("git"), "git not available")
    def test_git_is_supporting_evidence_only(self):
        self.repo(node_only())
        git = lambda *a: subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *a],
                                        check=True, capture_output=True)
        git("init", "-q")
        git("add", "-A")
        git("commit", "-q", "-m", "init")
        self.write("src/routes/b.js", "// new source file\n")
        git("add", "-A")
        git("commit", "-q", "-m", "more source")
        out = self.drift()
        self.assertStatus(out, "NO DRIFT")
        self.assertIn("Files changed since 2026-01-15", self.section(out, "Informational"))
        self.assertIn("not treated as drift", out)

    def test_secret_containing_configuration(self):
        files = node_only()
        files[".env"] = f"API_KEY={TOKEN}\nDATABASE_URL=postgres://admin:hunter2hunter2@db.internal:5432/loans\n"
        files["config/settings.json"] = json.dumps({"stripeKey": TOKEN, "password": "P@ssw0rd-Correct-Horse"})
        self.repo(files)
        (self.root / "PROJECT-CONTEXT.md").write_text(
            (self.root / "PROJECT-CONTEXT.md").read_text() + f"\n## Infrastructure\n\n- Kubernetes deployment uses token {TOKEN}\n", encoding="utf-8")
        self.write("terraform/terraform.tfvars", f"db_password = \"{TOKEN}\"\n")
        self.write("terraform/main.tf", 'provider "aws" {}')
        for extra in ((), ("--ci",)):
            out = self.drift(*extra, code=1 if extra else 0)
            for secret in (TOKEN, "hunter2hunter2", "P@ssw0rd-Correct-Horse", "Zq81LmXv03"):
                self.assertNotIn(secret, out)
        self.assertIn("Terraform", out)
        self.assertNotIn(".env", out)          # a sensitive file is not evidence of anything
        self.assertNotIn("tfvars", out)


if __name__ == "__main__":
    unittest.main()
