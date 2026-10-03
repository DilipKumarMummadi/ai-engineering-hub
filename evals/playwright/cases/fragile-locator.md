# Scenario

A React and TypeScript storefront upgraded its component library. After the upgrade, several Playwright tests fail with "element not found", although the application works. The team asks how to fix the test and avoid repeats.

# Input

After our UI library upgrade this test fails with a timeout waiting for the button. The app works fine when I click through it manually. How should I fix the test, and how do we stop this happening again?

# Context

Failing test:

```ts
test('places an order', async ({ page }) => {
  await page.goto('/cart');
  await page.locator('.css-1x2y3z > div:nth-child(2) > button.btn-primary').click();
  await expect(page).toHaveURL(/\/order-confirmation/);
});
```

Rendered HTML of the cart page footer after the upgrade:

```html
<div class="css-9k2m4q">
  <div class="css-7a1b0c">
    <p>Total: $42.00</p>
  </div>
  <div class="css-5d8e3f">
    <button type="button" class="css-2p6r1t">Place order</button>
    <button type="button" class="css-2p6r1t">Continue shopping</button>
  </div>
</div>
```

The team does not add `data-testid` attributes to this page, and the buttons have their visible text as their accessible name.

# Expected Behavior

The response explains that the selector depends on generated class names and on the position of elements, both of which changed with the upgrade, so the test broke without any change in behavior. It recommends a locator based on what a user sees and the accessibility tree: the button with the name "Place order". It explains that this survives styling and layout changes, and that it also ties the test to the user-visible label, which is a reasonable dependency. It notes that the order of the two buttons also makes position-based selection risky. For prevention it recommends preferring role and name based locators as a team convention, with a test ID only when no stable user-facing option exists. Keeping the URL assertion is fine.

# Important Checks

- The cause of the failure is explained from the HTML given (generated classes, structure).
- The recommended locator identifies the button by its role and visible name.
- The response explains why the new locator is more stable.
- It mentions or handles the risk of two similar buttons by using the distinguishing name.
- The prevention advice is practical and fits the team's constraints (no test IDs on this page).
- It does not suggest copying the new generated class names into the selector.
- It does not claim the test was run.

# Failure Conditions

- Updating the selector to the new generated class names or position.
- Recommending a longer timeout or retries.
- Recommending XPath or `nth` selection.
- Requiring `data-testid` attributes even though the context says the team does not add them and a better option exists.
- Blaming the library upgrade as a defect in the application.
- Suggesting a rewrite of the test suite into a new framework or page object layer for a single locator.

# Notes

Mentioning that a user-facing label can change with copy edits, and that this is an acceptable trade-off because such a change is a real behavior change, is a good addition.
