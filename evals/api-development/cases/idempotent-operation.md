# Scenario

A mobile app calls a .NET payments endpoint. On poor networks the app times out and retries, and a few customers have been charged twice. The team asks for a fix.

# Input

Some customers are charged twice when the mobile app retries after a timeout. Please recommend how to change the payment endpoint so this can't happen.

# Context

Current endpoint:

```csharp
[HttpPost("payments")]
public async Task<IActionResult> Create(PaymentRequest req)
{
    var charge = await _gateway.ChargeAsync(req.CustomerId, req.Amount, req.Currency);
    var payment = new Payment { CustomerId = req.CustomerId, Amount = req.Amount, GatewayRef = charge.Id };
    _db.Payments.Add(payment);
    await _db.SaveChangesAsync();
    return Created($"/payments/{payment.Id}", payment.ToDto());
}
```

Facts:

- The mobile app sends the same request again when it does not receive a response within 10 seconds. It can send the retry while the first request is still being processed.
- The payment gateway accepts an optional idempotency key on charge requests, and treats repeated charges with the same key as the same charge.
- The request has no client-supplied unique identifier today. The team can change the mobile app in its next release, but older app versions will remain in use for months.
- The database is PostgreSQL, accessed through EF Core.
- Gateway calls usually take 1 to 3 seconds and occasionally take longer than 10 seconds.

# Expected Behavior

The response explains why the duplicates occur: the client retries a non-idempotent POST, and the server has no way to recognize that the retry is the same operation. The retry may also overlap the first request, so a simple "check whether it exists, then charge" is not enough without an atomic guard. It recommends an idempotency key supplied by the client and defines the server behavior: the key is stored with the request outcome under a unique constraint, a repeated request with the same key returns the stored result, a request with the same key and a different payload is rejected with a clear error, and a request that arrives while the first is still in progress is handled (wait, or return a conflict or an in-progress response) rather than starting a second charge. It passes the key to the gateway as well, and explains the crash window between charging and saving the result, which the gateway key protects. It addresses older app versions that do not send a key, for example by accepting requests without a key at a documented risk, or deriving a key, and plans the rollout. It addresses key retention and the status codes, and recommends tests including concurrent duplicate requests. It does not claim the fix was tested.

# Important Checks

- The cause of the duplicate charge (retry of a non-idempotent operation, overlap with the in-flight request) is explained.
- A key-based approach is proposed, with the unique constraint enforcing it atomically.
- The behavior for same key with same payload, same key with a different payload, and concurrent in-flight duplicates is defined.
- The gateway idempotency key is used and the window between the gateway call and the database save is discussed.
- Backward compatibility with older app versions is addressed.
- Key retention and the API contract (header or field, status codes) are considered.
- Tests include simultaneous duplicate requests.
- The response doesn't suggest just lengthening the client timeout or disabling retries as the solution.

# Failure Conditions

- Suggesting only a "check if payment exists" query before charging, without atomicity.
- Suggesting only a longer client timeout or removing the retry.
- Switching the endpoint to PUT or GET without a sound explanation.
- Ignoring the overlapping requests.
- Not using the gateway's idempotency support.
- Ignoring older app versions.
- Returning a new charge for the same key with a different payload.
- Claiming the problem is fixed without tests.

# Notes

Where the key is sent (header or body) is a design choice. The important part is the semantics and the handling of concurrent duplicates. Mentioning that retries should only be enabled for operations that are safe to repeat is a good addition.
