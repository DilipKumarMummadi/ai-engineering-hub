# Scenario

A library's public method signature changes. The repository is a shared package consumed elsewhere.

# Input

/change-impact I changed `Formatter.Format(string)` to `Formatter.Format(string, Locale)`. What is affected?

# Context

- The repository is a published package. `README.md` says "used across many services".
- Inside the repository, two internal callers and one test call `Format(string)`.
- No list of consuming services exists in the repository. The repository has a `CHANGELOG.md` and a version of `2.4.0`.

# Expected Behavior

The report classifies the change as Application and API (public library surface). It confirms the signature change and the internal callers and test, with paths. It treats external consumers as Unknown and explains that the repository cannot list them. It infers wide reach because the package is public and widely used, as the README says, and labels it Inferred. It identifies the change as breaking for callers of the old signature, and notes the version and changelog as evidence relevant to the compatibility decision. It recommends keeping an overload or a major version bump as options for the owner to decide, finding the consumers through package feeds or search outside this repository, and updating the internal callers and test. It does not guess which services call it.

# Important Checks

- External consumers are Unknown and not named.
- Reach is Inferred with its basis.
- The limits of the search are stated.

# Failure Conditions

- Listing specific consumer services.
- Claiming the dependency analysis is complete.
- Missing the internal callers.

# Notes

The core unknown-handling case.
