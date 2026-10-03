# Scenario

A developer adds a cancellation rule to a booking feature in a React and TypeScript app. The PR description says: "Allow free cancellation up to and including 24 hours before the start time. Already cancelled bookings cannot be cancelled again."

# Input

Please review this pull request. The description, the implementation and the tests are below.

# Context

`booking/canCancel.ts`:

```ts
export type Booking = { startsAt: Date; status: "confirmed" | "cancelled" };

export function canCancel(booking: Booking, now: Date): boolean {
  if (booking.status === "cancelled") return false;
  const hoursUntilStart =
    (booking.startsAt.getTime() - now.getTime()) / 3_600_000;
  return hoursUntilStart >= 24;
}
```

`booking/canCancel.test.ts`:

```ts
const now = new Date("2025-03-10T12:00:00Z");

test("allows cancellation 48 hours before start", () => {
  const booking = {
    startsAt: new Date("2025-03-12T12:00:00Z"),
    status: "confirmed" as const,
  };
  expect(canCancel(booking, now)).toBe(true);
});

test("rejects cancellation 2 hours before start", () => {
  const booking = {
    startsAt: new Date("2025-03-10T14:00:00Z"),
    status: "confirmed" as const,
  };
  expect(canCancel(booking, now)).toBe(false);
});
```

# Expected Behavior

The review recognizes that the implementation matches the stated rule and does not report a defect in it. It identifies that the tests leave important behavior unverified: the boundary at exactly 24 hours (which the description says is allowed), and the already-cancelled case. It may also note a start time in the past. It recommends specific tests with concrete inputs and expected results, and rates the gap as medium or low, not high.

# Important Checks

- The response does not claim the implementation is wrong.
- The exact-24-hour boundary is identified as untested, and tied to the "up to and including" wording.
- The already-cancelled rule is identified as untested.
- Recommended tests have concrete inputs and expected outcomes.
- Severity matches a coverage gap in correct code (medium or low).
- The two existing tests are described accurately.

# Failure Conditions

- The response says the tests are adequate.
- The response reports a bug in `canCancel` that is not there (for example that `>=` should be `>`).
- The recommendation is only "add more tests" with no specific cases.
- The response rates the gap as critical, or dismisses it as unimportant.
- The response asks for E2E or browser tests for a pure function.
- The response rewrites the function or switches the test framework.

# Notes

Mentioning time zones or daylight-saving changes is acceptable as an optional extra if it is framed as a question, since the code works with absolute timestamps. It should not be reported as a defect.
