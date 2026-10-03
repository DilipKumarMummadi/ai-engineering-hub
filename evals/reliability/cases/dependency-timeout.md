# Scenario

A .NET checkout service calls a third-party shipping-rate API. Last week the shipping API slowed down and the whole shop stopped responding. The team asks for a reliability analysis and a fix.

# Input

When the shipping-rate API got slow last week, our whole site stopped responding. Please analyze what went wrong and recommend a design so this doesn't happen again.

# Context

Code and configuration (relevant parts):

```csharp
// Program.cs
builder.Services.AddHttpClient<ShippingClient>(c => c.BaseAddress = new Uri("https://rates.example-carrier.com"));

// ShippingClient.cs
public async Task<Rate> GetRateAsync(Cart cart)
{
    for (var attempt = 0; attempt < 4; attempt++)
    {
        try { return await _http.GetFromJsonAsync<Rate>($"/rates?zip={cart.Zip}&kg={cart.WeightKg}"); }
        catch (HttpRequestException) { }
    }
    throw new ShippingUnavailableException();
}
```

Facts:

- The HTTP client timeout is the library default of 100 seconds. No other timeout, cancellation token or circuit breaker is configured.
- During the incident, the shipping API took 30 to 60 seconds to respond to most requests. The site's web server ran out of available worker threads and stopped serving all pages, including ones that do not use shipping.
- Under normal conditions, the shipping API responds in about 150 ms at the median and 400 ms at p99.
- The rate lookup is a read-only `GET`. Rates for the same zip and weight change rarely, at most a few times per day.
- The business has said that if a live rate is unavailable, checkout should still work with a flat rate of a fixed, agreed amount, and the customer should be told it is an estimate. Blocking checkout entirely is not acceptable.
- Checkout has a page-level latency budget of about 2 seconds.
- Retries happen immediately with no delay. When the API returns errors, each checkout makes up to four calls.

# Expected Behavior

The response identifies the failure chain: a slow dependency, a 100-second timeout, so each request holds a worker for a very long time, and then the worker pool is exhausted and unrelated pages fail. The retry loop makes it worse by multiplying calls to a struggling service, immediately and without a bound on the total time. It recommends a timeout derived from the normal latency (p99 about 400 ms) and the 2 second budget, so a few hundred milliseconds to about a second, not the default, with an overall deadline that includes retries. Since the operation is a safe read, retries are acceptable, but they should be few, with exponential backoff and jitter, and limited by the deadline; it also notes retries at other layers can multiply. It recommends a circuit breaker so that calls stop while the dependency is unhealthy, isolating the dependency so its slowness cannot consume all workers (bulkhead or concurrency limit), and graceful degradation that follows the business rule: a flat rate marked as an estimate, and optionally a short cache of recent rates given that they change rarely. It recommends making the behavior visible (metrics for timeouts, breaker state and fallback use) and testing it by injecting latency and errors in a test environment. It does not run or claim results of those tests.

# Important Checks

- The cascade is explained from the facts (long timeout, worker exhaustion, unrelated pages failing).
- The timeout is derived from the measured latency and the budget, not a guess.
- Retries are judged safe because the call is a read, and are made bounded, with backoff and jitter, and under an overall deadline.
- The retry amplification (four immediate attempts) is identified.
- A breaker and isolation of the dependency are included.
- The fallback follows the stated business rule, and is marked as visible to users as an estimate.
- Failure injection testing is part of the plan.
- Monitoring of the mechanisms is mentioned.
- The response does not invent facts or results.

# Failure Conditions

- Recommending only more retries, or more workers or servers.
- Keeping the 100-second timeout, or picking an arbitrary one with no reasoning.
- Immediate or unbounded retries.
- Blocking checkout when the API is down, against the business rule.
- Silent fallback that the user does not know about.
- Ignoring that unrelated pages failed.
- Claiming tests were run.
- Over-engineering, such as recommending multi-region deployment, for this problem.

# Notes

Several values for the timeout and retry counts are acceptable if they follow from the latency and the budget. Caching rates is optional and should come with a note on staleness.
