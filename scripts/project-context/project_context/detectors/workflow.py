"""Development workflow files and coding-convention configuration."""
from __future__ import annotations

from ..model import confirmed

_WORKFLOW = (
    ("Contribution guide", ("CONTRIBUTING.md", "CONTRIBUTING", "CONTRIBUTING.rst")),
    ("Pull request template", ("pull_request_template.md",)),
    ("Code ownership file", ("CODEOWNERS",)),
    ("Changelog", ("CHANGELOG.md", "CHANGELOG")),
    ("Commit message tooling", ("commitlint.config.js", "commitlint.config.cjs", ".commitlintrc", ".commitlintrc.json", "lefthook.yml")),
    ("Pre-commit hooks configuration", (".pre-commit-config.yaml",)),
    ("Release automation configuration", ("release-please-config.json", ".releaserc", ".releaserc.json")),
)
_CONVENTIONS = (
    ("EditorConfig", (".editorconfig",)),
    ("ESLint configuration", (".eslintrc", ".eslintrc.json", ".eslintrc.js", ".eslintrc.cjs", "eslint.config.js", "eslint.config.mjs")),
    ("Prettier configuration", (".prettierrc", ".prettierrc.json", "prettier.config.js")),
    ("Python linting configuration", (".flake8", "ruff.toml", ".pylintrc", ".pre-commit-config.yaml")),
    ("Checkstyle configuration", ("checkstyle.xml",)),
    ("golangci-lint configuration", (".golangci.yml", ".golangci.yaml")),
    ("StyleCop configuration", ("stylecop.json", ".globalconfig")),
)


def detect(repo):
    items = []
    for label, names in _WORKFLOW:
        hits = repo.named(*names)
        if hits:
            items.append(confirmed("Development Workflow", f"{label}: {', '.join(hits[:3])}", *hits[:3]))
    if ".github/ISSUE_TEMPLATE" in repo.dirs:
        items.append(confirmed("Development Workflow", "Issue templates: .github/ISSUE_TEMPLATE", ".github/ISSUE_TEMPLATE"))
    if ".husky" in repo.dirs:
        items.append(confirmed("Development Workflow", "Git hooks directory: .husky", ".husky"))
    for label, names in _CONVENTIONS:
        hits = repo.named(*names)
        if hits:
            items.append(confirmed("Coding Conventions", f"{label}: {', '.join(hits[:3])}", *hits[:3]))
    return items
