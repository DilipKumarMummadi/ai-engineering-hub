# Scenario

A Playwright checkout test passes on developers' machines but fails in CI, which runs headless. A teammate suggests running CI in headed mode under a virtual display.

# Input

This test passes locally but fails in CI, which runs headless. We're thinking of switching CI to headed mode with a virtual display. Can you work out what's going on and tell me the right fix?

# Context

CI failure output:

```
Error: locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for getByRole('button', { name: 'Checkout' })
  -   locator resolved to <button class="css-2p6r1t">Checkout</button>
  -   element is visible, enabled and stable
  -   <div class="cookie-banner" role="dialog"> intercepts pointer events
  -   retrying click action
```

Playwright configuration and setup:

- Local runs use `launchPersistentContext` with a developer profile folder on disk. The profile was used before, and developers accepted the site's cookie banner once.
- CI uses the default fresh context for each test, with no stored cookies.
- The viewport is the default in both cases for this test and the button is in view.
- The application shows the cookie banner on the first visit when no consent cookie is present. It is part of the application.

# Expected Behavior

The response reads the call log: the button is found, visible and enabled, but the cookie banner intercepts the click. It then connects this to the setup difference. Local runs reuse a profile where consent is already stored, so no banner appears. CI starts clean, so the banner covers the button. The cause is a difference in browser state, not headless mode, so switching to headed mode would not fix it. The response recommends handling consent deterministically: either start tests with a consent state applied (for example through pre-set storage or cookie state) or dismiss the banner through its user-facing control, in a way that is consistent for every environment. It also suggests making local and CI contexts behave the same way. It does not recommend forcing the click or removing the banner from the application.

# Important Checks

- The call log is used as evidence, and the interception is identified as the immediate cause.
- The local and CI difference (persistent profile with stored consent vs fresh context) is identified as the underlying cause.
- Headless mode is correctly ruled out as the cause, and headed mode is not recommended as the fix.
- The fix makes consent state explicit and repeatable.
- The response does not advise forced clicks, longer timeouts or retries as the fix.
- The response does not advise disabling the banner in the application for all users.
- The response distinguishes a test environment problem from an application defect.
- Nothing is fabricated about the environment.

# Failure Conditions

- Agreeing that headed mode or a virtual display is the fix.
- Attributing the failure to headless rendering, timing or CI slowness without using the call log.
- Recommending `force` on the click, or a longer timeout.
- Recommending adding retries.
- Missing the persistent profile versus fresh context difference.
- Suggesting permanently removing the consent banner from the application.
- Asking for information that is already in the context.

# Notes

A response may propose testing the consent banner itself in one dedicated test, while other tests start with consent already given. That is a good practice and should be viewed favorably.
