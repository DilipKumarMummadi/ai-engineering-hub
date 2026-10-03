# Scenario

A team's Playwright suite tests a React report page with an "Export" button. The export test passes locally but fails in about one of every eight CI runs. A developer proposes raising the fixed delay from 2 to 5 seconds.

# Input

Our export test is flaky in CI. I'm thinking of increasing the wait from 2 seconds to 5 seconds. Can you review the test and recommend a fix?

# Context

```ts
test('exports the monthly report', async ({ page }) => {
  await page.goto('/reports/monthly');
  await page.getByRole('button', { name: 'Export' }).click();
  await page.waitForTimeout(2000);
  const done = await page.getByText('Export complete').isVisible();
  expect(done).toBe(true);
});
```

Known facts:

- The page shows "Export complete" when the export API call returns.
- In recent CI runs the export API response took between 0.4 and 3.6 seconds.
- Failures show `expected true, received false` at the final assertion.
- Locally the API responds in under a second.

# Expected Behavior

The response explains that a fixed delay checks the page after a set time and not when the export is finished, so the result depends on how long the API takes. Since the API took up to 3.6 seconds in CI, a 2-second delay sometimes checks too early, which matches the intermittent failures. The final check reads the state once, so it cannot wait or retry either. Raising the delay to 5 seconds would only make failures rarer and would slow every run. The response recommends removing the delay and asserting on the expected outcome in a way that waits for it (so the test proceeds as soon as the export completes and fails only if it never does). If the default wait is too short for the export, it may suggest a specific, justified timeout for that assertion. It does not recommend retries as the fix.

# Important Checks

- The response links the intermittent failures to the fixed delay and the measured response times.
- It identifies the one-time visibility check as a second problem.
- It rejects "increase the delay" as a solution and explains why.
- The recommended test waits on the application state (the completion message), not on time.
- Any timeout increase is specific and justified by the measured 3.6 seconds, not arbitrary.
- Retries are not recommended as the fix.
- The response does not claim the new test was run.

# Failure Conditions

- Approving a longer fixed delay.
- Recommending more test retries as the fix.
- Replacing one fixed delay with another.
- Keeping the single-read visibility check.
- Blaming CI infrastructure without analyzing the test.
- Adding unrelated changes such as new abstractions or mocking the export API, without a reason.
- Claiming the fix was verified when nothing was executed.

# Notes

Mocking the export API is not needed here. The point of the test is the real export flow. A response that offers mocking as an option should explain the trade-off.
