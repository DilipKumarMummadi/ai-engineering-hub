# Scenario

The command is run inside the Hub repository.

# Input

/context generate

# Context

The current directory is the AI Engineering Hub checkout.

# Expected Behavior

The command recognizes the Hub (`plugin.json` naming it and the generator sources), does not generate, explains that the command targets the repository being worked on, and offers to continue only if the user explicitly wants the Hub's own context.

# Important Checks

- No `PROJECT-CONTEXT.md` appears in the Hub.
- The user is given a clear choice.

# Failure Conditions

- Generating the Hub's context silently.
- Storing another repository's context in the Hub.

# Notes

Real-run behavior observed. Guards the ownership rule.
