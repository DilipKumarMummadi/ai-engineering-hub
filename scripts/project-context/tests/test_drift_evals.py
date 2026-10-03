"""Executable forms of evals/project-context-drift/cases/*.md. Fixtures are built here, never from the Hub."""
import json
import shutil

from .eval_fixtures import dotnet_react, node_only
from .helpers import DATE, make_repo, run
from .test_drift import DriftCase, tree_hash

TOKEN = "Zq81LmXv03TdWpRc92HnKa5B"


class EvalNoDrift(DriftCase):
    def test_patch_bump_and_readme_rewording(self):
        self.repo(node_only())
        pkg = json.loads((self.root / "package.json").read_text())
        pkg["dependencies"]["express"] = "^4.19.2"
        self.write("package.json", json.dumps(pkg))
        self.write("README.md", "Reworded.\n")
        out = self.drift()
        self.assertStatus(out, "NO DRIFT")
        self.assertNotIn("Express", out)
        self.drift("--ci")


class EvalTechnologyDrift(DriftCase):
    def test_new_removed_and_runtime(self):
        self.repo(node_only())
        self.write(".nvmrc", "22\n")
        self.write("package.json", json.dumps({"name": "loans", "scripts": {"start": "x", "test": "jest"},
                   "dependencies": {"fastify": "^4", "pg": "^8"}, "devDependencies": {"jest": "^29", "eslint": "^8"}}))
        self.write("src/routes/a.js", "// edited")
        out = self.drift()
        mat = self.section(out, "Material Changes")
        self.assertIn("New repository evidence detected: Fastify", mat)
        self.assertIn("Express is documented", mat)
        self.assertIn("Node.js version changed: the context records 20; the repository declares 22", mat)
        self.assertNotIn("Jest", out)
        self.assertNotIn("PostgreSQL", mat)
        self.assertNotIn("a.js", out)
        self.assertIn("Stale Context", out)
        self.drift("--ci", code=1)


class EvalArchitectureDrift(DriftCase):
    def test_new_project_removed_application_and_source_edits(self):
        self.repo(dotnet_react())
        self.write("src/Payment/Payment.csproj", '<Project Sdk="Microsoft.NET.Sdk.Worker"></Project>')
        shutil.rmtree(self.root / "src/shop-web")
        self.write("src/Shop.Api/Controllers/OrdersController.cs", "class Edited {}")
        self.write("src/Shop.Domain/Order.cs", "class Order {}")
        out = self.drift()
        self.assertStatus(out, "DRIFT DETECTED")
        self.assertIn("src/Payment", self.section(out, "Potentially Material"))
        self.assertIn("src/shop-web is documented but no longer detected", self.section(out, "Material Changes"))
        self.assertIn("React is documented", out)
        self.assertNotIn("OrdersController", out)
        self.assertNotIn("Order.cs", out)
        for style in ("microservice", "hexagonal", "layered"):
            self.assertNotIn(style, out.lower())


class EvalStaleContext(DriftCase):
    def test_stale_statements_are_quoted_not_deleted(self):
        files = {"package.json": '{"name":"x","scripts":{"start":"node a.js"}}', ".nvmrc": "20\n", "src/a.js": "// a",
                 "README.md": "We plan on deploying to Kubernetes one day.\n"}
        self.root = make_repo(files)
        ctx = ("# Project Context\n\n## Infrastructure\n\n- Repository contains Kubernetes deployment manifests.\n- Deployed with Helm charts.\n\n"
               "## Technology Stack\n\n- Node.js 20 — Confirmed — .nvmrc\n\n<!-- manual:start -->\n## Team Notes\n"
               "We used to run on Jenkins; that is history now.\n<!-- manual:end -->\n")
        (self.root / "PROJECT-CONTEXT.md").write_text(ctx, encoding="utf-8")
        out = self.drift()
        stale = self.section(out, "Stale Context")
        self.assertIn("Repository contains Kubernetes deployment manifests.", stale)
        self.assertIn("Deployed with Helm charts.", stale)
        self.assertIn("Kubernetes is documented", out)
        self.assertNotIn("Node.js", out)
        self.assertNotIn("Jenkins", out)
        self.assertEqual((self.root / "PROJECT-CONTEXT.md").read_text(encoding="utf-8"), ctx)


class EvalConflictingContext(DriftCase):
    def test_three_conflicts_surfaced(self):
        files = {"src/web/package.json": '{"name":"web","dependencies":{"react":"18","react-dom":"18"}}',
                 "src/Data/Data.csproj": '<Project Sdk="Microsoft.NET.Sdk"><ItemGroup><PackageReference Include="Pomelo.EntityFrameworkCore.MySql" Version="8"/></ItemGroup></Project>',
                 "docker-compose.yml": "services:\n  db:\n    image: mysql:8\n", ".github/workflows/ci.yml": "name: CI\non: push\njobs:\n  b:\n    steps:\n      - run: echo\n"}
        self.root = make_repo(files)
        ctx = ("# Project Context\n\n## Frontend\n\n- Frontend: Angular — Confirmed — developer-provided\n\n"
               "## Database\n\n- PostgreSQL with EF Core — Confirmed — src/Data/Data.csproj\n\n"
               "## CI/CD\n\n- CI runs on Jenkins — Confirmed — Jenkinsfile\n")
        (self.root / "PROJECT-CONTEXT.md").write_text(ctx, encoding="utf-8")
        out = self.drift()
        conflicts = self.section(out, "Conflicts")
        for pair in (("Angular", "React"), ("PostgreSQL", "MySQL"), ("Jenkins", "GitHub Actions")):
            self.assertIn(f"names {pair[0]}", conflicts)
            self.assertIn(f"shows {pair[1]}", conflicts)
        self.assertStatus(out, "DRIFT DETECTED")
        self.assertEqual((self.root / "PROJECT-CONTEXT.md").read_text(encoding="utf-8"), ctx)


class EvalInfrastructureDrift(DriftCase):
    def test_terraform_in_docker_out_no_kubernetes_no_secret(self):
        files = node_only()
        self.repo(files)
        (self.root / "Dockerfile").unlink()
        self.write("terraform/main.tf", 'provider "aws" {}\nterraform { backend "s3" {} }\n')
        self.write("terraform/terraform.tfvars", f'db_password = "{TOKEN}"\n')
        self.write("docs/kubernetes/notes.md", "notes")
        for extra, code in ((( ), 0), (("--ci",), 1)):
            out = self.drift(*extra, code=code)
            self.assertNotIn(TOKEN, out)
            self.assertNotIn(TOKEN[:8], out)
            self.assertNotIn("tfvars", out)
            self.assertNotIn("Kubernetes", out)
        full = self.drift()
        mat = self.section(full, "Material Changes")
        self.assertIn("New repository evidence detected: Terraform", mat)
        self.assertIn("Docker is documented", mat)
        self.assertIn("terraform/main.tf", mat)


class EvalCicdDrift(DriftCase):
    def test_new_workflow_exit_0_and_only_ci_removed_exit_1(self):
        wf = "name: CI\non: push\njobs:\n  b:\n    steps:\n      - run: echo\n"
        a = dotnet_react()
        self.repo(a)
        self.write(".github/workflows/deploy.yml", wf)
        self.write("src/Shop.Api/Program.cs", "// changed")
        before = tree_hash(self.root)
        out = self.drift("--ci")
        self.assertIn("REVIEW RECOMMENDED", out)
        self.assertEqual(before, tree_hash(self.root))
        self.repo(dotnet_react())
        shutil.rmtree(self.root / ".github")
        self.write("src/Shop.Api/Program.cs", "// changed")
        out = self.drift("--ci", code=1)
        self.assertIn("DRIFT DETECTED", out)
        self.assertLess(len(out.splitlines()), 10)


class EvalSourceOnlyChange(DriftCase):
    def test_busy_week_is_not_drift(self):
        self.repo(dotnet_react())
        for rel in ("src/Shop.Api/Controllers/OrdersController.cs", "src/Shop.Api/Controllers/NewController.cs",
                    "src/shop-web/src/App.tsx", "src/shop-web/src/components/Cart.tsx", "tests/Shop.Api.Tests/CartTests.cs",
                    "README.md", "docs/decisions.md", "dist/bundle.js", "node_modules/x/index.js"):
            self.write(rel, "// changed " + rel)
        before = tree_hash(self.root)
        out = self.drift()
        self.assertStatus(out, "NO DRIFT")
        self.assertNotIn("## Material Changes", out)
        self.assertNotIn("## Potentially Material", out)
        self.assertNotIn("OrdersController", out)
        self.drift("--ci")
        self.assertEqual(before, tree_hash(self.root))
