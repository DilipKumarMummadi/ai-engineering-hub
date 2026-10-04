# Scenario

Documentation conflicts with source evidence.

# Input

/context generate

# Context

The README says the service uses Django and MySQL. The manifests show ASP.NET Core and an Npgsql provider.

# Expected Behavior

The context records what the source shows as Confirmed or Inferred, does not adopt the README claim as a fact, and reports the conflict in the generator's conflicts output so the developer can resolve it.

# Important Checks

- Source evidence wins.
- The conflict is visible in the report.
- Django is not listed as a dependency.

# Failure Conditions

- Recording Django or MySQL as facts.
- Hiding the conflict.

# Notes

Covered by a fixture test.
