# Productionization

This document defines the production-ready lifecycle of the AI Engineering Hub: the path a change takes from development to release, adoption, maintenance and deprecation. It names the gate at each step, says what already enforces it, and says plainly what is not enforced yet.

The Hub is a set of files: skills, agents, commands, workflows, templates, documentation and evaluations, packaged as a plugin. It has no backend, database or service of its own, and productionizing it does not add one. The lifecycle reuses the mechanisms the repository already has.

## 1. Lifecycle

```text
Development
    ↓
Local Validation
    ↓
Evaluation
    ↓
Integration Validation
    ↓
Security Validation
    ↓
Compatibility Validation
    ↓
Plugin Validation
    ↓
Release Candidate
    ↓
Release
    ↓
Adoption
    ↓
Maintenance
    ↓
Deprecation
```

A change moves forward only when the gate for its stage passes. A failed gate sends the change back to development. A gate that is not automated is still a gate: it is a documented check a reviewer performs and records.

## 2. Stages, Gates and Current Enforcement

| Stage | Question it answers | What runs today | Not yet enforced |
| --- | --- | --- | --- |
| Development | Is the change focused and conventional? | [Contributing](../CONTRIBUTING.md) guidelines: one concern per change, kebab-case names, document every capability, add evaluations | No automated check of the guidelines |
| Local Validation | Is the repository structurally consistent? | `python3 scripts/validate-hub/validate_hub.py` checks commands, agents, workflows and skills, their wiring, platform parity and links. `python3 -m unittest discover -s tests` from `scripts/project-context` runs the Project Context tests | Nothing runs it automatically on commit or push; there is no CI configuration in the repository |
| Evaluation | Does behavior match the specification? | Qualitative cases under `evals/`, judged Pass, Needs Improvement or Fail, per the [evaluation overview](../evals/README.md) | Cases are judged by hand against a live model; there is no runner and no recorded result history |
| Integration Validation | Do layers and external tools work together? | Cross-layer cases in `evals/integration/`, MCP cases in `evals/mcp-integration/`, and read-only pilots against a real repository | Pilots are manual and were not recorded in the repository |
| Security Validation | Does the package contain secrets or unsafe configuration? | The plugin validator rejects credentials, `env`, `headers` and secret-like values in `mcp.json`, and forbidden content in the package | No dependency or pinned-version review process; no review of MCP server versions beyond the pin |
| Compatibility Validation | Does it still work on Claude Code and GitHub Copilot, and for existing users? | `validate_hub.py` enforces Claude and Copilot parity. The client pages in [`mcp-clients/`](mcp-clients/README.md) record what was tested per client | No defined compatibility promise and no check that a change is backward compatible |
| Plugin Validation | Is the package valid and clean? | `python3 scripts/validate-plugin/validate_plugin.py` and its tests (`python3 -m unittest discover -s scripts/validate-plugin`): manifest, `skills/` layout, link containment, `mcp.json`, forbidden content | None beyond those above |
| Release Candidate | Is this build a candidate for release? | None | No candidate definition, no freeze, no sign-off |
| Release | Is it versioned, recorded and distributable? | A `version` in `plugin.json` and `.claude-plugin/plugin.json` (both `1.0.0`), validated by the plugin validator, and an `Unreleased` section in the [Changelog](../CHANGELOG.md) | No tags, no version-bump rule, no release notes procedure, and no distribution channel beyond the repository |
| Adoption | Can an engineer or team start using it? | README, the [setup guide](mcp-setup-guide.md) and [plugin architecture](plugin-architecture.md) | No onboarding path by role and no adoption checklist |
| Maintenance | Does it stay correct as things change? | Changelog entries and re-running the validators | No ownership, review cadence, or process for upstream MCP changes |
| Deprecation | How is something retired safely? | None | No deprecation policy or notice period |

The right-hand column is the work this phase exists to do. Each gap is to be closed by the smallest mechanism that works, not by new infrastructure.

## 3. Principles

| Principle | Meaning |
| --- | --- |
| Reuse what exists | The validators, the evaluation format and the registries are the gates. Extend them before adding anything. |
| Documented gates over tooling | Where automation does not exist, write the check down and make it reviewable. Do not build a system to avoid writing a checklist. |
| No platform | The Hub gains no backend, database, service, telemetry or custom MCP server. |
| Honest status | A gate that is manual is labelled manual. A result that was not produced is reported as not produced. |
| Backward compatibility is a decision | Breaking changes are deliberate, named in the changelog and tied to a version change, never incidental. |
| Both clients | Nothing is released for one client only unless that limit is stated. |
| No credentials | Nothing in the repository, the package or a release artifact holds a secret. |

## 4. What Counts as a Change to the Hub

Different kinds of change carry different risk and need different gates.

| Change | Example | Minimum gates |
| --- | --- | --- |
| Documentation only | Clarifying a specification | Local Validation (links) |
| Content of a skill, agent, workflow or command | Rewording a step, adding a stage | Local, Evaluation, Compatibility |
| Behavior contract | A new output section, a changed safety rule or checkpoint | All validation stages, changelog entry, version consideration |
| Packaging | `plugin.json`, `mcp.json`, directory layout | Plugin Validation, Security Validation, Compatibility |
| New or changed MCP server definition | Bumping a pinned server | Security, Integration, Plugin, documentation of client configuration |
| Removal or rename | Deleting a command or renaming a capability | All stages, deprecation notice, version change |

## 5. Relationship to Other Documents

- [Architecture](architecture.md) and [Plugin Architecture](plugin-architecture.md) describe what is being released.
- [Contributing](../CONTRIBUTING.md) governs how changes are made before they enter this lifecycle.
- The [evaluation overview](../evals/README.md) defines how behavior is judged.
- [MCP Runtime Configuration](mcp-runtime-configuration.md) and the [MCP clients](mcp-clients/README.md) define what stays outside the package.
- The [Changelog](../CHANGELOG.md) is the record of what each release contains.

## 6. Out of Scope for This Document

This document defines the lifecycle and its gates. It does not yet define the versioning scheme, the release procedure, the compatibility promise, the automation of the gates, the adoption guidance or the deprecation policy. Those are specified separately and must follow the principles above.
