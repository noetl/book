# What a Hop Costs

<span class="status status-real">REAL</span>

A **hop** is one `kind: playbook` call. It is never free: the child is
a whole execution, with its own dispatch, claims, events and
completion, on top of whatever work it does. The cost is real and was
measured. The improvements planned since then are not built, so they
appear below as TARGET.

## Measured

From the resource model (`step_kinds`, `kind: playbook`, server
v3.161.2), all **MEASURED** on prod:

| Figure | What | When | Source |
|---|---|---|---|
| **~9 s** | orchestration cost of one hop, regardless of the work inside it | 2026-08-24 | noetl/travel wiki, itinerary planner (#286) |
| **~10–15 s per hop** | the same work as a child vs inline: a 369 ms Firestore read took 11.4 s as a child; 663 ms of Places work took 1.5 s inline | 2026-08 | noetl/travel wiki, itinerary planner, latency |
| **34.7 s → 19.4 s** median (−44 %) | a paired A/B test: provider children inlined into the planner as `python` steps | 2026-06-29 | noetl/ai-meta Sessions-Log |

Read each one with its date. The resource model's own caveat: several
of these figures predate later dispatch fixes, so "measure on the
target cluster at the target load before committing to a budget".

## Not yet measured

The latency-reduction build plan (ai-meta PR
[#556](https://github.com/noetl/ai-meta/pull/556),
`docs/rfc/latency-reduction-plan.md`, **open, design only**) gives an
awaited hop at about **~3–5 s** today. It labels that figure
*predicted*, next to the 9–15 s MEASURED in 2026-08. In this book's
labels that is **NOT_YET_MEASURED**: a real question without a
measured answer. 

```admonish not-yet
The plan's later stages aim to remove the 0–2 s poll per awaited hop
and to return the awaiting parent's slot, and finally to turn a pure
child hop into a function call inside one compiled WASM run. All of
that is design only (PR #556, open), with each stage's flags off by
default.
```

## The heuristic

The resource model's GUIDANCE:

> Prefer an inline python step to a kind: playbook child when the
> child only wraps one call: each hop measured ~9-15 s of orchestration
> on prod, and inlining cut a planner turn by 44%.

So use a sub-playbook when you get something real for the cost: reuse
across many parents, a separate pool or credentials, independent
failure, or a child that is itself a large workflow. Don't use one to
wrap a single call.

To estimate a playbook's wall clock, the resource model's rule is
`steps × per-step overhead + Σ step work + hops × hop overhead`
(GUIDANCE). [Chapter 21](ch21-00-resource-model.md) and
[Chapter 22](ch22-00-orchestration-overhead.md) take it further.

## Check your understanding

{{#quiz ../quizzes/ch07-02.toml}}
