import json

from .helpers import RepoTestCase

CSPROJ_WEB = """<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><Nullable>enable</Nullable></PropertyGroup>
  <ItemGroup><PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.0.0" />
  <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" /></ItemGroup></Project>"""
CSPROJ_TEST = """<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup>
<ItemGroup><PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.0.0" /><PackageReference Include="xunit" Version="2.6.0" /></ItemGroup></Project>"""


class TestDotnet(RepoTestCase):
    def test_dotnet_repository_detection(self):
        t = self.generate({
            "App.sln": "", "src/MyApi/MyApi.csproj": CSPROJ_WEB, "src/MyApi/Controllers/HomeController.cs": "class X {}",
            "tests/MyApi.Tests/MyApi.Tests.csproj": CSPROJ_TEST,
        })
        self.assertEntry(t, "ASP.NET Core: 1 project(s) use the Web SDK", "Confirmed")
        self.assertEntry(t, ".NET target frameworks: net8.0", "Confirmed")
        self.assertEntry(t, "Npgsql (PostgreSQL provider)", "Confirmed")
        self.assertEntry(t, "xUnit", "Confirmed")
        self.assertEntry(t, "Application likely exposes HTTP APIs", "Inferred")
        self.assertEntry(t, "Database engine appears to be PostgreSQL", "Inferred")
        self.assertIn("Evidence: src/MyApi/MyApi.csproj", t)
        self.assertEntry(t, "src/MyApi: ASP.NET Core project", "Confirmed")

    def test_layer_names_are_inferred_not_confirmed(self):
        files = {f"src/Shop.{n}/Shop.{n}.csproj": '<Project Sdk="Microsoft.NET.Sdk"></Project>' for n in ("Api", "Application", "Domain", "Infrastructure")}
        t = self.generate(files)
        self.assertEntry(t, "layered organisation", "Inferred")
        self.assertNotIn("Clean Architecture", t)


class TestNodeFrontend(RepoTestCase):
    PKG = {"name": "shop-web", "scripts": {"dev": "vite", "test": "vitest", "build": "vite build"},
           "dependencies": {"react": "^18", "react-dom": "^18"}, "devDependencies": {"vite": "^5", "vitest": "^1", "@playwright/test": "^1"},
           "engines": {"node": ">=20"}}

    def test_node_repository_detection(self):
        t = self.generate({"package.json": json.dumps({"name": "svc", "scripts": {"start": "node s.js", "test": "jest"},
                           "dependencies": {"express": "4", "pg": "8"}, "devDependencies": {"jest": "29"}}),
                           "package-lock.json": "{}", ".nvmrc": "20\n"})
        self.assertEntry(t, "Express: declared", "Confirmed")
        self.assertEntry(t, "Jest: declared", "Confirmed")
        self.assertEntry(t, "Node.js version file (.nvmrc): 20", "Confirmed")
        self.assertEntry(t, "Package manager appears to be npm", "Inferred")
        self.assertEntry(t, "Script `test` (package.json)", "Confirmed")
        self.assertEntry(t, "PostgreSQL client (pg)", "Confirmed")

    def test_frontend_detection(self):
        t = self.generate({"web/package.json": json.dumps(self.PKG), "web/angular.json": "{}"})
        self.assertEntry(t, "React: declared", "Confirmed")
        self.assertEntry(t, "Frontend application appears present in web", "Inferred")
        self.assertEntry(t, "Angular workspace configuration", "Confirmed")
        self.assertEntry(t, "Playwright: declared", "Confirmed")
        self.assertEntry(t, "Node.js version requirement (web/package.json): >=20", "Confirmed")


class TestPython(RepoTestCase):
    def test_python_repository_detection(self):
        t = self.generate({
            "pyproject.toml": '[project]\nname = "svc"\nrequires-python = ">=3.10"\ndependencies = ["fastapi>=0.100", "psycopg2-binary"]\n'
                              '[project.scripts]\nserve = "svc.main:run"\n[tool.ruff]\nline-length = 100\n',
            "requirements-dev.txt": "pytest==8.0\n# comment\n",
            "tests/test_a.py": "def test_x(): pass",
        })
        self.assertEntry(t, "FastAPI: declared", "Confirmed")
        self.assertEntry(t, "pytest: declared", "Confirmed")
        self.assertEntry(t, "Python version requirement (pyproject.toml): >=3.10", "Confirmed")
        self.assertEntry(t, "Application likely serves HTTP", "Inferred")
        self.assertEntry(t, "Ruff configured", "Confirmed")
        self.assertEntry(t, "Entry point `serve`", "Confirmed")
        self.assertEntry(t, "Test files found in: tests", "Confirmed")


class TestInfrastructure(RepoTestCase):
    def test_docker_detection_and_private_registry_host_excluded(self):
        t = self.generate({
            "Dockerfile": "FROM registry.internal.example/team/base:1.2 AS build\nFROM mcr.microsoft.com/dotnet/aspnet:8.0\nEXPOSE 8080\n",
            "docker-compose.yml": "services:\n  api:\n    build: .\n  db:\n    image: postgres:16\n",
        })
        self.assertEntry(t, "Dockerfiles: Dockerfile", "Confirmed")
        self.assertEntry(t, "mcr.microsoft.com/dotnet/aspnet:8.0", "Confirmed")
        self.assertEntry(t, "Compose services (docker-compose.yml): api (build), db (postgres:16)", "Confirmed")
        self.assertEntry(t, "Database engine appears to be PostgreSQL", "Inferred")
        self.assertNotIn("registry.internal.example", t)
        self.assertIn("private registry; host excluded", t)

    def test_kubernetes_detection(self):
        t = self.generate({
            "k8s/deploy.yaml": "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: a\n---\napiVersion: v1\nkind: Service\n",
            "charts/app/Chart.yaml": "name: app\nversion: 0.1.0\n",
            "charts/app/templates/d.yaml": "apiVersion: apps/v1\nkind: Deployment\n",
        })
        self.assertEntry(t, "Kubernetes manifests: 1 file(s) declaring kinds Deployment, Service", "Confirmed")
        self.assertEntry(t, "Helm charts: charts/app/Chart.yaml (app)", "Confirmed")

    def test_terraform_detection(self):
        t = self.generate({"infra/main.tf": 'terraform {\n  required_version = ">= 1.5"\n  backend "s3" {}\n}\nprovider "aws" {}\n'})
        self.assertEntry(t, "Terraform providers declared: aws", "Confirmed")
        self.assertEntry(t, "Target cloud appears to be AWS", "Inferred")


class TestCiCd(RepoTestCase):
    WF = ("name: CI\non:\n  pull_request:\n  push:\n    branches: [main]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    environment: production\n"
          "    steps:\n      - uses: actions/checkout@v4\n      - run: dotnet test\n      - run: |\n          docker build -t app .\n          kubectl apply -f k8s/\n"
          "      - run: echo ${{ secrets.TOKEN }}\n")

    def test_github_actions_detection(self):
        t = self.generate({".github/workflows/ci.yml": self.WF, ".github/workflows/notes.md": "# not a workflow"})
        self.assertEntry(t, "GitHub Actions workflows: ci.yml", "Confirmed")
        self.assertEntry(t, "Workflow ci.yml: triggers pull_request, push; jobs build", "Confirmed")
        self.assertEntry(t, "builds a container image", "Confirmed")
        self.assertEntry(t, "appears to include deployment or publish steps (matched: kubectl", "Inferred")
        self.assertEntry(t, "references repository secrets (names not recorded)", "Confirmed")
        self.assertEntry(t, "CI step in ci.yml runs `dotnet test`", "Confirmed")
        self.assertNotIn("notes.md", t.split("GitHub Actions workflows")[1].split("\n")[0])
        self.assertNotIn("secrets.TOKEN", t)

    def test_no_ci_is_unknown_not_absent(self):
        t = self.generate({"README.md": "A small example service for testing.\n"})
        self.assertEntry(t, "CI/CD: no CI/CD definition found in inspected paths", "Unknown")

    def test_ci_without_deploy_step_leaves_deployment_unknown(self):
        t = self.generate({".github/workflows/ci.yml": "name: CI\non: [push]\njobs:\n  b:\n    steps:\n      - run: npm test\n"})
        self.assertEntry(t, "CI/CD: deployment mechanism not found", "Unknown")
        self.assertEntry(t, "Deployment: production environment", "Unknown")
