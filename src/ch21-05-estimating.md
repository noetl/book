# Estimating a Playbook Before You Run It

<span class="status status-real">REAL</span>

The model's first heuristic is the estimating rule (`heuristics`,
GUIDANCE, `as_of` 2026-11-11):

> wall clock ≈ steps × per-step overhead + Σ(step work) + hops × hop overhead

where **steps** counts every step *run* (a step that a back-edge
re-runs counts each time) and **hops** counts awaited `kind: playbook`
children. The model's figures for prod: **~4.5 s per step** and
**~9-15 s per hop** (`orchestration_overhead.measured`, MEASURED, prod,
2026-08). "Re-measure: the overhead, not the work, decides the total."

## A worked estimate

Take the playbook from [Chapter 2](ch02-00-project-first-playbook.md),
moved to a cluster. Its loop body (`pick`, `fetch`, `load`, `advance`)
runs twice, so the step runs are:

| Step | Runs |
|---|---|
| `start` | 1 |
| `pick`, `fetch`, `load`, `advance` | 2 each = 8 |
| `report`, `check` | 1 each = 2 |
| **total** | **11** |

There are no sub-playbooks, so **hops = 0**.

| Term | Value | Label |
|---|---|---|
| orchestration: 11 × ~4.5 s | **~50 s** | GUIDANCE from a MEASURED figure (prod, 2026-08) |
| work: 2 small HTTP fetches, 5 small DuckDB queries, 2 rhai one-liners | not known | NOT_YET_MEASURED on prod for `http` and `duckdb` |
| hops | 0 | |
| **estimate** | **~50 s + the work** | GUIDANCE |

The work here is tiny, so the estimate is about **50 s, nearly all of
it orchestration**. For scale: the local runtime runs the whole
playbook, the two HTTP fetches included, in **1.7-2.0 s** (MEASURED:
CLI v6.4.1 on the author's laptop, 2026-11-15, n = 3;
[Chapter 8](ch08-00-local-runtime.md)). The difference is the cost of
distribution, paid per step. It buys a durable event log, the full set
of tool kinds, and scale; whether that is worth 50 s is the question
[Chapter 11](ch11-00-choosing-a-runtime.md) helps you answer.

```admonish warning title="The 4.5 s figure is older than the code you will run"
The model's caveat: "several of these figures predate later dispatch
fixes". A later measurement put orchestration at **~0.95 s per step**
(MEASURED, prod, 2026-11-02, n = 4), in an RFC that is still under
review (noetl/ai-meta PR #556). With that figure the estimate is
**~10 s + the work**. Which one is right for your cluster is exactly
what you have to measure; [Chapter 22](ch22-00-orchestration-overhead.md)
covers where the time goes.
```

### What changes the estimate most

- **Adding a hop.** Make `fetch` an awaited sub-playbook, and each of
  its 2 runs adds a child execution: +2 × 9-15 s = **+18-30 s**, more
  than the whole loop's orchestration at the newer figure. The model's
  advice: inline a child that only wraps one call (GUIDANCE).
- **Adding steps, not work.** Splitting `report` into three steps adds
  two step runs, ~9 s at the older figure, for no extra work.
- **Peak slots.** This playbook needs one slot at a time. A parallel
  `loop:` over 30 items would need 30 at once ([21.4](ch21-04-slot-model.md)).

## Check the estimate

The model lists where a real run's cost is recorded (`metrics`):

- `GET /api/executions/{id}` returns `started_at`, `completed_at` and
  up to the 2000 most recent events, each with `created_at`. There is
  no duration field: subtract.
- Each step's `call.done` carries `result.context.duration_ms`, the
  tool's own time.
- `command.started` → `command.completed` timestamps give the step's
  wall clock including any slot wait after claim.

Orchestration per step is then roughly *(execution wall clock − Σ
`duration_ms`) ÷ step runs*. With n = 1 that is one observation, not a
figure: label it MEASURED with the date, environment and n, as the
model does.

## Check your understanding

{{#quiz ../quizzes/ch21-05.toml}}
