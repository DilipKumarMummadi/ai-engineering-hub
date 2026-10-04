"""Consuming-repository fixtures for the /context command: the generator targets the repository it is pointed
at, never the Hub, and its output is safe. Also checks the command files for Claude/Copilot alignment."""
from __future__ import annotations

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from .helpers import make_repo, run

HUB = Path(__file__).resolve().parents[3]
LAUNCHER = HUB / "scripts" / "project-context" / "project-context"
CLAUDE_CMD = HUB / ".claude/commands/context.md"
COPILOT_CMD = HUB / ".github/prompts/context.prompt.md"
SECRET = "Sup3rS3cretValue99"

DOTNET = {
    "README.md": "# Orders Service\nBackend API that manages customer orders.\n",
    "src/Orders.Api/Orders.Api.csproj": '<Project Sdk="Microsoft.NET.Sdk.Web"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup>'
                                        '<ItemGroup><PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.0.0" /></ItemGroup></Project>',
    "src/Orders.Api/appsettings.json": '{"ConnectionStrings":{"Default":"Host=db;Database=orders;Username=app;Password=%s"}}' % SECRET,
    "tests/Orders.Tests/Orders.Tests.csproj": '<Project Sdk="Microsoft.NET.Sdk"><ItemGroup><PackageReference Include="xunit" Version="2.6.0" /></ItemGroup></Project>',
    ".github/workflows/ci.yml": "name: ci\non: [push]\njobs:\n  b:\n    runs-on: ubuntu-latest\n    steps:\n      - run: dotnet test\n",
}


def context_of(root: Path) -> str:
    return (root / "PROJECT-CONTEXT.md").read_text(encoding="utf-8")


class ConsumingRepositoryTests(unittest.TestCase):
    def generate(self, files):
        root = make_repo(files)
        code, out, err = run("generate", "--repo", str(root), "--date", "2026-01-15")
        self.assertEqual(code, 0, out + err)
        return root

    def test_dotnet_backend_is_analyzed_and_secret_free(self):
        root = self.generate(DOTNET)
        text = context_of(root)
        for expected in ("ASP.NET Core", ".NET target frameworks: net8.0", "xUnit"):
            self.assertIn(expected, text)
        self.assertNotIn(SECRET, text)

    def test_react_frontend(self):
        root = self.generate({"package.json": '{"name":"shop-ui","dependencies":{"react":"18"},"devDependencies":{"vitest":"1"},"scripts":{"test":"vitest"}}', "src/App.tsx": "x"})
        text = context_of(root)
        self.assertIn("React: declared as a dependency", text)
        self.assertIn("Vitest", text)

    def test_python_project(self):
        root = self.generate({"pyproject.toml": '[project]\nname="etl"\ndependencies=["fastapi","pytest"]\n', "app/main.py": "x"})
        text = context_of(root)
        self.assertIn("FastAPI", text)
        self.assertIn("Inferred", text)

    def test_monorepo_records_each_project(self):
        root = self.generate({"package.json": '{"name":"m","workspaces":["apps/*"]}', "apps/web/package.json": '{"name":"web","dependencies":{"react":"18"}}',
                              "apps/api/Orders.Api.csproj": '<Project Sdk="Microsoft.NET.Sdk.Web"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>'})
        text = context_of(root)
        self.assertIn("apps/api: ASP.NET Core", text)
        self.assertIn("apps/web: Node.js package", text)

    def test_minimal_repository_is_all_unknowns_not_invented(self):
        root = self.generate({})
        text = context_of(root)
        self.assertNotRegex(text, r"(?m)^- .* — Confirmed$.*React")
        self.assertIn("## Known Unknowns", text)
        self.assertNotIn("ASP.NET", text)

    def test_existing_context_preserves_manual_block(self):
        root = self.generate(DOTNET)
        path = root / "PROJECT-CONTEXT.md"
        path.write_text(path.read_text() + "\n<!-- manual:start -->\n## Team Notes\n\nDeployments happen on Thursdays.\n<!-- manual:end -->\n")
        code, out, err = run("update", "--repo", str(root), "--date", "2026-01-16")
        self.assertEqual(code, 0, out + err)
        self.assertIn("Deployments happen on Thursdays.", context_of(root))

    def test_drift_reports_and_never_writes(self):
        root = self.generate(DOTNET)
        before = context_of(root)
        (root / "Dockerfile").write_text("FROM mcr.microsoft.com/dotnet/aspnet:8.0\n")
        code, out, err = run("drift", "--repo", str(root))
        self.assertEqual(code, 0)
        self.assertRegex(out, r"(?i)docker|drift")
        self.assertEqual(context_of(root), before)

    def test_missing_context_drift_is_an_error_not_a_guess(self):
        root = make_repo(DOTNET)
        code, out, err = run("drift", "--repo", str(root))
        self.assertEqual(code, 2)
        self.assertFalse((root / "PROJECT-CONTEXT.md").exists())

    def test_conflicting_documentation_is_reported_not_adopted(self):
        files = dict(DOTNET)
        files["README.md"] = "# Orders\nThis service is built with Django and MySQL.\n"
        root = make_repo(files)
        code, out, err = run("generate", "--repo", str(root), "--dry-run", "--date", "2026-01-15")
        self.assertEqual(code, 0, out + err)
        self.assertNotIn("Django: declared as a dependency", out)
        self.assertRegex(out, r"(?i)conflict|README states")

    def test_hub_is_never_the_implicit_target(self):
        """Running the launcher from the Hub with --repo pointing elsewhere must leave the Hub untouched."""
        root = make_repo(DOTNET)
        r = subprocess.run([str(LAUNCHER), "generate", "--repo", str(root)], capture_output=True, text=True, cwd=HUB)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((root / "PROJECT-CONTEXT.md").is_file())
        self.assertFalse((HUB / "PROJECT-CONTEXT.md").exists())

    def test_application_source_is_not_modified(self):
        root = make_repo(DOTNET)
        before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
        run("generate", "--repo", str(root), "--date", "2026-01-15")
        for p, data in before.items():
            self.assertEqual(p.read_bytes(), data, f"{p} was modified")


class CommandContractTests(unittest.TestCase):
    def setUp(self):
        self.claude, self.copilot = CLAUDE_CMD.read_text(), COPILOT_CMD.read_text()

    def test_both_platforms_exist_and_share_structure(self):
        heads = lambda t: re.findall(r"(?m)^#{1,3} .*$", t)
        self.assertEqual(heads(self.claude), heads(self.copilot))

    def test_both_use_the_existing_generator_and_operations(self):
        for t in (self.claude, self.copilot):
            self.assertIn("scripts/project-context/project-context", t)
            for op in ("generate", "inspect", "drift"):
                self.assertIn(f"| `{op}` |", t)
            self.assertIn("--repo <target root>", t)

    def test_target_is_current_repository_and_hub_is_guarded(self):
        for t in (self.claude, self.copilot):
            self.assertIn("git rev-parse --show-toplevel", t)
            self.assertIn("AI Engineering Hub itself", t)

    def test_safety_rules_present_on_both(self):
        for t in (self.claude, self.copilot):
            self.assertIn("Never reproduce a secret", t)
            self.assertIn("does not authorize commits", t)
            self.assertIn("Never edit application source", t)
            self.assertIn("Do not write, rewrite or hand-edit `PROJECT-CONTEXT.md` yourself", t)

    def test_no_agent_routing_and_no_second_generator(self):
        for t in (self.claude, self.copilot):
            self.assertNotRegex(t, r"`[a-z-]+-agent`")
            self.assertIn("do not create a second generator", t.lower())


if __name__ == "__main__":
    unittest.main()
