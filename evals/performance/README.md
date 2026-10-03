# Performance Evaluations

Evaluations for the [`performance`](../../.claude/skills/performance/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the skill reasons from measurements to a bottleneck, picks changes that address it, and never claims an improvement it has not measured.

## Evaluation Principles

- Evidence comes before any recommendation.
- Observed issues, suspected bottlenecks and confirmed bottlenecks are kept apart.
- The dominant cost is found by breaking the total into parts.
- Recommendations target that cost. Reflex fixes (caching, indexes, scaling) are avoided unless the evidence supports them.
- Expected impact is a hypothesis with a way to measure it.
- Side effects, such as staleness or a new bottleneck, are considered.
- Numbers are only those in the context.

## Expected Behavior

A good response defines the problem and target, reads the evidence given, identifies where the time or resource goes, proposes a change to the dominant cost with reasoning, and describes how to measure before and after. It states what it cannot conclude from a single sample.

## Common Failure Modes

- Suggesting caching, an index or more instances without connecting it to the evidence.
- Treating a suspicion as confirmed.
- Promising a specific speedup.
- Optimizing a part that is a small share of the total.
- Ignoring workload or percentiles.
- Wrapping everything in memoization or caching.
- Fixing a bottleneck in a way that moves it elsewhere.

## Qualitative Evaluation

Outcomes are Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [slow-api](cases/slow-api.md) | Finds the dominant cost in a trace and does not reach for caching. |
| [n-plus-one](cases/n-plus-one.md) | Recognizes an N+1 pattern from query evidence and fixes it with care. |
| [react-rendering](cases/react-rendering.md) | Uses profiler evidence to find why a list re-renders, without blanket memoization. |
