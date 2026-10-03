# Project Context Generator Configuration

<!--
Optional configuration for the Project Context Generator. See docs/project-context-generator-specification.md.

Configuration is NOT required. Every setting has a default, and the generator works with no configuration file at all.
Copy this file into the repository (for example next to PROJECT-CONTEXT.md as GENERATOR-CONFIG.md), keep only the settings you need,
and delete the rest, including these comments.

This file is technology-neutral. The examples below are illustrations. Use paths and patterns that exist in your repository.

Honored by the reference implementation (scripts/project-context): Included Paths, Excluded Paths, Sensitive Paths, Manual Sections,
Additional Evidence Sources (presence only), Output path, Stale after, When nothing changed, and the Limits. Not yet honored: Sensitive Identifiers,
Update mode, and the version-control hint. An assistant following the specification should honor all of them.

Hard limits (cannot be changed by configuration):
- Secret protection cannot be turned off. You can add sensitive paths, not remove the built-in protections.
- The generator never executes repository code, build, tests, scripts or deployment commands.
- The generator writes only the context file, and only when explicitly asked in the current run.
- This file must not contain secrets, credentials or personal data.
-->

## Scope

### Included Paths

<!-- Paths the generator should inspect. Default: the whole repository, except the default exclusions.
Use this to limit a large or multi-part repository to the parts the context should cover.
- apps/
- services/billing/
-->

### Excluded Paths

<!-- Paths the generator should skip, in addition to the defaults (generated output, vendored and dependency directories, build output, binaries).
- legacy/
- third-party/
- **/generated/
-->

## Additional Evidence Sources

<!-- Extra files or documents that are good evidence in this repository but are not in the default source catalog.
Say what each one evidences, so the generator knows what it may conclude from it.
- docs/runbooks/   → operational and deployment procedures
- ops/environments.yaml   → environment names and deployment targets
-->

## Sensitive Paths

<!-- Paths that must not be read for content, in addition to the built-in protections. Their existence may still be noted.
- config/local/
- **/*.keystore
- data/fixtures/customers/
-->

### Sensitive Identifiers

<!-- Default: internal hostnames, IP addresses and account, tenant or subscription identifiers are treated as sensitive and not recorded.
You may list non-sensitive ones that are safe and useful to record, or add more categories to protect.
- allow: public documentation site hostname
- protect: internal project codenames
-->

## Manual Sections

<!-- Sections of PROJECT-CONTEXT.md maintained by hand. The generator will not edit them. It may report when repository evidence contradicts them.
Use the section names from the template.
- Important Constraints
- Development Workflow
-->

## Refresh Behavior

<!-- All optional.
- Stale after: <duration, for example "6 months">   (default: no fixed threshold; a context with no review date is treated as potentially stale)
- Update mode: <propose | propose-and-write-when-asked>   (default: propose. Writing always needs an explicit request.)
- When nothing changed: <leave file untouched | record review date only>   (default: leave file untouched)
- Use version-control history as a staleness hint: <yes | no>   (default: yes if available)
-->

## Output

<!-- Where the context file lives. Default: PROJECT-CONTEXT.md at the repository root.
- Path: PROJECT-CONTEXT.md
-->

## Limits

<!-- Optional guards for large repositories.
- Maximum file size to read in full: <size>   (larger files are read in targeted sections)
- Maximum directory depth for structure detection: <number>
-->

## Notes

<!-- Anything else the generator should know about scope, that is not a secret. For example:
- This repository contains two independently owned applications; produce one context section per application.
-->
