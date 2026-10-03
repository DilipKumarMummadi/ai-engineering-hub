# Scenario

A React and TypeScript storefront is adding a coupon step to checkout. The team wants to make sure the flow works for users and asks the Test Planning Agent for a plan. One developer proposes testing every rule in the browser.

# Input

We're adding coupon support to checkout. A developer wants to cover every coupon rule with Playwright tests. Please create a test plan and tell us what should be browser tests and what shouldn't.

# Context

Requirement:

On the checkout page the user can enter a coupon code and press "Apply". The page shows the discounted total or an error message. The user can then pay and sees an order confirmation page.

Coupon rules (all enforced by the server, which the page calls through `POST /api/coupons/validate`):

- `SAVE10`: 10% off orders of at least 50.00.
- `FREESHIP`: removes the shipping charge.
- Expired, unknown and below-minimum coupons are rejected with a specific message each.
- Only one coupon can be applied at a time.

Front-end facts:

- The displayed total is calculated by a pure TypeScript function `applyCoupon(cart, coupon)` using the coupon data returned by the server.
- The page uses a `CouponForm` component with loading, success and error states.
- Payment uses an external payment provider's hosted fields, with a sandbox available for testing.
- The team has Playwright configured for CI and a seeded test environment with a test user and products. The authentication state can be reused.
- E2E tests currently take about 40 seconds each, and the CI budget for the browser suite is tight.

# Expected Behavior

The agent uses `testing` for the strategy and `playwright` for the scenarios that need a real browser, and `api-development` for the validation endpoint contract, if relevant. It separates the rules from the journey. The coupon rules, discount calculation, minimum amount and the one-coupon-at-a-time rule are logic, so they belong in unit tests of `applyCoupon` and in API tests of the validation endpoint, which are fast and precise. The `CouponForm` states (loading, success, error messages, disabled button while loading) belong in component tests with the server response faked. A small number of browser tests covers what only a real browser can verify: a critical journey (add to cart, apply a valid coupon, see the discounted total, pay in the sandbox, reach the confirmation), and one or two negative paths through the real integration, such as an invalid coupon showing the message and letting the user continue. It explains why each browser test earns its cost and why the per-rule browser tests would be slow and redundant, and it classifies the browser tests as smoke or regression. It describes stable locator and assertion expectations at a high level (user-facing locators, waiting on application state), without writing the tests. It plans test data: a seeded user and products, coupons set up through the API or seed data, and payment sandbox cards, with each test independent and cleaned up, and notes dependencies on the sandbox. It flags risks such as third-party payment flakiness and lists open questions. It does not claim any test was run.

# Important Checks

- The rules are moved to unit and API tests, with reasons.
- Component tests are planned for the form states.
- A small set of browser tests is kept for the journey and selected negative path, each with a reason.
- The per-rule browser tests are explicitly declined, and the trade-off is explained with the CI budget.
- Smoke vs regression classification is given for browser tests.
- Test data and coupon setup are planned, independent per test.
- Dependencies and risks (payment sandbox) are identified.
- The agent does not produce the Playwright code, or claim execution.
- Open questions are listed.

# Failure Conditions

- Agreeing to test every coupon rule in the browser.
- Dropping browser tests entirely for a checkout journey.
- Missing component-level tests for the form states.
- Not justifying the browser scenarios.
- Ignoring the CI budget and test duration.
- Ignoring test data or the payment sandbox dependency.
- Writing the tests or claiming they pass.
- Inventing coupon rules not in the requirement.
- Recommending testing the payment provider's own behavior.

# Notes

A good plan is not opposed to browser tests. It uses a few for what only a browser can show, and gives everything else to cheaper tests.
