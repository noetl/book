# What Is Not Yet Measured

<span class="status status-real">REAL</span>

The resource model lists the questions that are real and have **no
number** (`not_yet_measured`, `as_of` 2026-11-11). Verbatim, all
seven:

1. per-step latency of http, duckdb, postgres and mcp steps on prod
2. latency of a hosted LLM call inside a real playbook step
3. sustained executions per second on prod
4. worker slot occupancy over time
5. user-pool KEDA ramp time on the EHDB trigger, and scale-down time on prod
6. catalog URI fetch latency
7. unsaturated prod command-bus latency after 2026-07-30

## Why this list matters

The model's rule for this label is "a real question with no number; do
not invent one". It is a defence against a common failure: a plan that
needs a number, finds none, and borrows the nearest one. Three
borrowings this list rules out:

| Tempting borrowing | Why it is wrong |
|---|---|
| "The bus adds ~140 ms": the p50 138.5 ms `issued → claimed` figure | it is from 2026-07-30; item 7 says nothing unsaturated has been measured since |
| "The local run took 40 ms, so the HTTP step costs 40 ms" | a local figure does not transfer to prod (`read_first`), and item 1 is open |
| "Ramp time is about a minute", from the ~60-90 s Autopilot node figure | that is node provisioning only; item 5, the pool's ramp on the EHDB trigger, is open |

## Closing one

A gap closes when someone measures it and the model gains a MEASURED
entry with environment, date, n and a public source, in a server
release. [21.5](ch21-05-estimating.md#check-the-estimate) shows where
the numbers come from for one execution. Until a release carries the
figure, this book treats the question as open.

## Check your understanding

{{#quiz ../quizzes/ch21-06.toml}}
