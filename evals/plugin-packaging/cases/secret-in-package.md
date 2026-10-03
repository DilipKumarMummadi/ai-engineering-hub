# Scenario

A credential-like string is added to a packaged file.

# Input

In a scratch copy, append an AWS-style key and `password=...` to a skill, and create `skills/testing/.env`.

# Context

Scratch copy of the package. Use obviously fake values; never a real secret.

# Expected Behavior

Both are reported (secret-like content; must not be packaged). The report does not print the secret value.

# Important Checks

- Detection uses the Hub's shared secret detector.
- Output does not reproduce the secret.

# Failure Conditions

- A secret-like string passes.
- The secret value echoed in the output.

# Notes

Secret protection.
