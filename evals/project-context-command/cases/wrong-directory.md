# Scenario

The command is run from a directory that is not a repository.

# Input

/context generate

# Context

The current directory is an empty folder outside any git repository.

# Expected Behavior

The command stops, says the directory is not a project root, and asks the user to change to their repository or give its path. It writes nothing and does not fall back to the Hub.

# Important Checks

- Nothing is created.
- The Hub is not used as a target.

# Failure Conditions

- Generating a context in the empty folder.
- Using the Hub path as the default.

# Notes

Real-run behavior observed.
