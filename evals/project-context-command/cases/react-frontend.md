# Scenario

Generate context in a React frontend.

# Input

/context generate

# Context

A git repository with `package.json` (React, Vitest, `@playwright/test`), `src/App.tsx` and a `vite build` script. No README description.

# Expected Behavior

The context records React, Vitest, Playwright and the build and test scripts as Confirmed with evidence, notes that the README has no description, and lists API, database and deployment as Unknown. Scripts are recorded, not run.

# Important Checks

- Technologies match the manifest.
- No backend is invented.
- Commands are recorded from files and not claimed to work.

# Failure Conditions

- Inventing an API or backend.
- Running the scripts.
- Claiming a design system without evidence.

# Notes

Frontend-only repository.
