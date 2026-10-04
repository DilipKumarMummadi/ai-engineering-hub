import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_plugin as vp  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


def make_copy() -> Path:
    tmp = Path(tempfile.mkdtemp())
    for rel in ("plugin.json", "README.md", "mcp.json", ".claude-plugin", "skills", ".claude/skills", "docs/plugin-architecture.md", "com.github.copilot"):
        s, d = REPO / rel, tmp / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(s, d) if s.is_dir() else shutil.copy2(s, d)
    return tmp


class PluginTests(unittest.TestCase):
    def setUp(self):
        self.root = make_copy()
        self.addCleanup(shutil.rmtree, self.root)

    def manifest(self, **changes):
        p = self.root / "plugin.json"
        d = json.loads(p.read_text())
        d.update(changes)
        p.write_text(json.dumps(d))

    def has(self, text):
        return any(text in e for e in vp.validate(self.root))

    def test_valid(self):
        self.assertEqual(vp.validate(self.root), [])

    def test_real_repo(self):
        self.assertEqual(vp.validate(REPO), [])

    def test_bad_schema(self):
        self.manifest(**{"$schema": "https://example.com/old.json"})
        self.assertTrue(self.has("$schema"))

    def test_bad_names(self):
        for bad in ("AI Engineering Hub", "ai_engineering_hub", "-x", "a--b", ""):
            self.manifest(name=bad)
            self.assertTrue(self.has("invalid name"), bad)

    def test_unknown_field(self):
        self.manifest(mcpServers={})
        self.assertTrue(self.has("not a permitted core field"))

    def test_missing_marketplace(self):
        (self.root / ".claude-plugin/marketplace.json").unlink()
        self.assertTrue(self.has("marketplace.json"))

    def test_bad_version(self):
        self.manifest(version="one")
        self.assertTrue(self.has("version"))

    def test_missing_skill_file(self):
        (self.root / "skills/testing/SKILL.md").unlink()
        self.assertTrue(self.has("SKILL.md missing"))

    def test_skill_drift(self):
        (self.root / "skills/testing/SKILL.md").write_text("---\nname: testing\ndescription: x\n---\nchanged")
        self.assertTrue(self.has("differs from"))

    def test_escaping_link(self):
        f = self.root / "skills/testing/SKILL.md"
        f.write_text(f.read_text() + "\n[x](../../plugin.json)\n")
        self.assertTrue(self.has("must resolve inside skills/"))

    def test_secret(self):
        f = self.root / "skills/testing/SKILL.md"
        f.write_text(f.read_text() + "\nAKIAIOSFODNN7EXAMPLE password=hunter2hunter2\n")
        self.assertTrue(self.has("secret-like"))

    def test_repo_context_packaged(self):
        (self.root / "skills/testing/PROJECT-CONTEXT.md").write_text("x")
        self.assertTrue(self.has("must not be packaged"))

    def mcp(self, mutate):
        p = self.root / "mcp.json"
        d = json.loads(p.read_text())
        mutate(d["mcpServers"])
        p.write_text(json.dumps(d))

    def test_mcp_headers_rejected(self):
        self.mcp(lambda s: s["github"].update(headers={"Authorization": "Bearer ${GITHUB_TOKEN}"}))
        self.assertTrue(self.has("field 'headers' is not allowed"))

    def test_mcp_env_rejected(self):
        self.mcp(lambda s: s["postgres"].update(env={"DATABASE_URI": "postgresql://u:pw@h/db"}))
        self.assertTrue(self.has("field 'env' is not allowed"))

    def test_mcp_connection_string_in_args_rejected(self):
        self.mcp(lambda s: s["postgres"].update(args=["postgres-mcp", "postgresql://user:hunter2pass@db.example.com:5432/app"]))
        self.assertTrue(self.has("secret-like value"))

    def test_portable_manifest_has_no_user_config(self):
        self.manifest(userConfig={"github_token": {}})
        self.assertTrue(self.has("'userConfig' is not a permitted core field"))

    def test_mcp_url_credentials_rejected(self):
        self.mcp(lambda s: s["figma"].update(url="https://user:pw@mcp.example.com/mcp"))
        self.assertTrue(self.has("no embedded credentials"))

    def test_mcp_bad_type_and_command(self):
        self.mcp(lambda s: s["figma"].update(type="http"))
        self.mcp(lambda s: s["postgres"].update(command="uvx postgres-mcp"))
        self.assertTrue(self.has("needs a type"))
        self.assertTrue(self.has("single executable token"))

    def test_mcp_inline_in_plugin_json_rejected(self):
        self.manifest(mcpServers={})
        self.assertTrue(self.has("not a permitted core field"))

    def test_mcp_needs_claude_bridge(self):
        (self.root / ".claude-plugin/plugin.json").unlink()
        self.assertTrue(self.has("Claude Code would not load"))

    def claude(self, mutate):
        p = self.root / ".claude-plugin/plugin.json"
        d = json.loads(p.read_text())
        mutate(d)
        p.write_text(json.dumps(d))

    def test_claude_override_literal_token_rejected(self):
        self.claude(lambda d: d["mcpServers"][1]["github"]["headers"].update(Authorization="Bearer abc123"))
        self.assertTrue(self.has("user_config.KEY"))

    def test_claude_override_needs_sensitive_option(self):
        self.claude(lambda d: d["userConfig"]["github_token"].update(sensitive=False))
        self.assertTrue(self.has("sensitive userConfig option"))

    def test_claude_override_must_match_server(self):
        self.claude(lambda d: d["mcpServers"][1]["github"].update(url="https://evil.example.com/mcp"))
        self.assertTrue(self.has("must match a server in mcp.json"))

    def test_mcp_nested_config_rejected(self):
        (self.root / "skills/testing/.mcp.json").write_text("{}")
        self.assertTrue(self.has("belongs only in the root mcp.json"))

    def test_mcp_optional(self):
        (self.root / "mcp.json").unlink()
        self.claude(lambda d: (d.pop("mcpServers"), d.pop("userConfig")))
        self.assertEqual(vp.validate(self.root), [])

    def test_eval_not_packaged(self):
        (self.root / "com.github.copilot/evals").mkdir()
        (self.root / "com.github.copilot/evals/a.md").write_text("x")
        self.assertTrue(self.has("must not be packaged"))


if __name__ == "__main__":
    unittest.main()
