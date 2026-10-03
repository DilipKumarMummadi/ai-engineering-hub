# Scenario

A backend developer changes an endpoint's response shape. The repository also contains a web client.

# Input

/change-impact I changed `GET /api/users/{id}` to return `fullName` instead of `firstName` and `lastName`. What breaks?

# Context

- `server/UsersController.ts` was modified.
- `client/src/pages/Profile.tsx` reads `user.firstName` and `user.lastName` from the response.
- `client/src/pages/Profile.test.tsx` mocks a response with `firstName`.
- `e2e/profile.spec.ts` asserts the heading shows the first name.
- The `client/src/api/generated/` directory holds a generated client that was not regenerated.
- No other consumers are documented.

# Expected Behavior

The report classifies the change as API and Backend, and identifies the client as affected. It confirms, with paths, that the page reads the removed fields, that the component test and the end-to-end test depend on the old shape, and that the generated client was not regenerated. It labels the runtime failure of the page as Inferred, because the repository shows the read and not the execution. It states that other consumers are Unknown. It recommends updating or regenerating the client, component and end-to-end tests, and contract validation. It recommends `api-development` and `testing`, and `playwright` only because a browser test is affected.

# Important Checks

- Generated code is treated as a dependent, not ignored.
- The runtime effect is Inferred and not stated as observed.
- Other consumers are Unknown.
- Only the affected tests are named.

# Failure Conditions

- Stating that the page crashes as a confirmed fact.
- Missing the generated client or the end-to-end test.
- Reviewing the controller for defects.

# Notes

Checks that frontend impact is reached through dependency tracing.
