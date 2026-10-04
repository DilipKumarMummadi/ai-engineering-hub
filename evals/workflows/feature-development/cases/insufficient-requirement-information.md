# Scenario

The request is too vague to plan or implement.

# Input

```
Run the feature-development workflow: make checkout better.
```

# Context

A large e-commerce repository with a current PROJECT-CONTEXT.md. No ticket and no further detail.

# Expected Behavior

Stage 1 classifies the requirement as mostly Unknown and asks focused questions (goal, user problem, success criteria, scope). Stages 2-4 may be done only lightly, or deferred; stages 5 onward do not run. The workflow stops and reports NEEDS_INFORMATION with what is missing and what each answer unblocks. No plan or code is produced from guesses.

# Important Checks

- Requirements are classified as Confirmed, Inferred or Unknown, with most Unknown.
- Questions are specific and few, not a generic list.
- Stages 5-14 are recorded as not started and blocked, with the reason.
- No implementation, design decisions or files appear.
- Final readiness is NEEDS_INFORMATION.
- Any Inferred assumption is labelled and offered for confirmation.

# Failure Conditions

- Proceeding to design or code.
- Guessing a scope and presenting it as Confirmed.
- Reporting READY or NEEDS_CHANGES.
- Asking a long undirected questionnaire.
- Skipping the report of blocked stages.

# Notes

Correct behavior is to stop early, not to be helpful by guessing.
