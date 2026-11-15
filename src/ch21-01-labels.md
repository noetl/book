# Labels: MEASURED, DEPLOYED, DEFAULT, GUIDANCE, TARGET

<span class="status status-real">REAL</span>

Every figure in the resource model carries a **label**, and the label
decides what you may do with the number. The server's tests refuse a
number without one (`orchestrate-core/src/resource_model.rs`, server
v3.161.2). The definitions are the file's own (`labels`, `as_of`
2026-11-11):

| Label | Means | Before you reuse it |
|---|---|---|
| **MEASURED** | observed on a cluster or harness | read its environment, date and source; it describes that build under that load |
| **DEPLOYED** | read off the production cluster on `as_of` | it is configuration, not code: it changes without a release |
| **DEFAULT** | a code default (env var + value) | a deployment may override it; check the environment |
| **GUIDANCE** | a planning rule derived from the figures | it is arithmetic, not a measurement |
| **TARGET** | a goal or budget | nobody has achieved it yet |
| **NOT_YET_MEASURED** | a real question with no number | do not invent one ([21.6](ch21-06-not-yet-measured.md)) |

## Three numbers about the same thing

The user pool's slots show how labels differ:

| Figure | Label | What it tells you |
|---|---|---|
| `WORKER_MAX_CONCURRENT` = 4 slots per worker | DEFAULT | what a worker does if nobody sets the variable |
| user pool: 2 replicas, KEDA 2–20, 8 slots at min, 80 at max | DEPLOYED (2026-11-11) | what one cluster ran on one day |
| `command.issued` → `command.claimed` p50 2123 ms with 90 commands against 8 slots | MEASURED (prod, 2026-07-30) | what queueing cost once, under that burst |

None of them is wrong, and none answers the others' question. A plan
needs to say which one it used.

```admonish warning title="A label is not a freshness guarantee"
A MEASURED figure is true of the build it was taken on. The model's own
caveat on orchestration cost: "several of these figures predate later
dispatch fixes" (`orchestration_overhead.caveat`). A label tells you
what kind of number it is, not that it is current.
```

## Check your understanding

{{#quiz ../quizzes/ch21-01.toml}}
