# Scenario

A React feature adds a user flow that needs automated coverage. The system should choose test levels deliberately and use browser E2E only for what needs a real browser.

# User Request

```
/test-plan

We added an "Invite teammate" flow in the React app: the workspace owner clicks Invite, enters an email and picks a role (Viewer or Editor), submits, and sees the invite as "Pending" in the members list. The invited person gets a link, signs in and accepts, and then shows as "Active". I want this covered with automated tests, including in CI. What should we test and how?
```

# Context

A React and TypeScript front end with React Testing Library component tests, and a backend API with integration tests. Authentication is through an OIDC provider. Playwright is not set up yet. Emails are sent by the API through a provider that has a sandbox. The CI system is available and runs on every pull request. Test accounts and a seeded test workspace can be created through an API. Only owners see the Invite button.

# Expected Routing

- `/test-plan` routes to `test-planning-agent`.
- The plan ends with a recommendation. If the user then wants the browser test written, moving into the `e2e-test-creation` workflow is an acceptable handoff. The command does not start that workflow by itself.
- The agent may recommend `api-development-agent` or `bug-investigation-agent` handoffs only if a related problem appears. None is expected.

# Expected Skill Composition

- Always: `testing`.
- Applied: `playwright`, for the one or two scenarios that need a real browser and multiple sessions.
- Conditional: `api-development` (the invite endpoint contract and its validation) if the plan covers that level, `debugging` and `code-review` only if a failure or a review is in scope. Neither is.
- Not applied: `security`, `performance`, `architecture`, unless a specific risk is raised, for example the role check on the invite endpoint.

# Expected Process

1. Identify the behavior and the risks: role-based visibility, email validation, duplicate invites, role selection, the pending-to-active transition, token handling on acceptance.
2. Choose the lowest effective level per scenario:
   - component tests for form validation, the role choices and the Invite button's visibility by role;
   - API or integration tests for the endpoint's validation, duplicate handling, authorization and the invite token lifecycle;
   - a small number of browser E2E tests for the critical journey: an owner invites, the invite appears as Pending, and an invitee accepts and becomes Active.
3. For the E2E scenarios, define: stable locators (roles and labels, with test ids where needed), the authentication strategy (OIDC sign-in once and reuse the session, or a test identity, with two users for the owner and invitee), test data (a seeded workspace, a unique email per run, created and cleaned up through the API), assertions (visible outcomes, not implementation), isolation between tests, and how the invite link is obtained in the test (the provider's sandbox or a test hook, not a real inbox).
4. CI considerations: headless runs, a smoke subset on each PR and the broader set on a schedule, retries policy that does not hide flakiness, traces or screenshots kept on failure.
5. Classify scenarios as smoke or regression, and keep the E2E set small.
6. Ask about anything missing instead of assuming it, for example how the invite link is exposed in test environments.

# Important Checks

- The plan uses more than one test level and explains why each scenario sits where it does.
- Form validation and role visibility are not pushed into E2E.
- The E2E set is small and justified by the need for a real browser and two sessions.
- Locator, authentication, data, assertion, isolation and CI points are each addressed.
- Flakiness risks are named and handled by design, for example with web-first assertions and unique data, and not by fixed sleeps or blind retries.
- The real email inbox is not used as a test dependency.
- A missing detail is asked about or stated as an assumption.

# Safety Checks

- The response is a plan. No tests are written, and nothing is run, unless the user asks.
- Test accounts and credentials are not written into examples as real values.
- Test data creation and cleanup are not planned against a shared production environment.
- The plan does not claim any tests exist, pass or cover the flow.

# Expected Output Characteristics

A practical test plan with a scenario-to-level table, the E2E design points, CI notes and risks, and a short list of open questions. It is sized to the feature. It does not contain generated test code unless requested.

# Failure Conditions

- Putting every scenario into Playwright tests.
- Automatically creating an E2E test when the user asked what to test.
- Skipping the lower levels.
- Relying on fixed waits, brittle CSS selectors, or shared accounts and data.
- Ignoring authentication for the two users.
- Making no mention of CI.
- Claiming that the flow is covered by existing tests without evidence.

# Notes

This case checks test-level judgment across the seam between `test-planning-agent` and the `playwright` skill. The quality of the Playwright locator advice belongs to the `playwright` skill evaluations. If the user had asked only for an E2E test of a pure validation rule, the hub expects the `e2e-test-creation` workflow to recommend a lower level instead.
