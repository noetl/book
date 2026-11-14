# `loop`: One Step, Many Items

<span class="status status-real">REAL</span>

NoETL has **two** ways to repeat work, and both are real:

1. **`loop:`** on a step runs that step once per item of a collection
   (this section).
2. **Back-edges**: an arc that goes back to an earlier step, guarded by
   `when` ([6.4](ch06-04-back-edges.md)).

```yaml
{{#include ../examples/ch06/loop-parallel/playbook.yaml}}
```

## The keys

| Key | Meaning |
|---|---|
| `loop.in` | A template that evaluates to a list. Required for `sequential` and `parallel`. |
| `loop.iterator` | The name each item gets. Must not be empty. |
| `loop.spec.mode` | `sequential` (the default), `parallel`, or `cursor` |
| `loop.spec.max_in_flight` | Parsed, and **ignored** (see below) |

Inside the loop body each item is available as `{{ iter.<iterator> }}`
and also as plain `{{ <iterator> }}`, together with `{{ iter._index }}`
and `{{ iter._total }}`, which are also available plain as `_index` and
`_total`. The same values are injected into the tool's `args`
(`build_iteration_command`, `orchestrate-core/src/commands.rs`,
v3.161.2). There is no `loop.index`.

## Sequential and parallel

These were checked in `orchestrator.rs` at v3.161.2:

- **`sequential`** dispatches item 0. Each time an item completes and
  nothing else of the loop is in flight, it dispatches the next. One
  slot at a time.
- **`parallel`** dispatches **every item at once**:
  `dispatch_count = if is_parallel { total } else { 1 }`. A 500-item
  parallel loop puts 500 commands on the bus in one pass. They run as
  fast as there are free worker slots, so a large loop can occupy a
  whole pool.

```admonish myth
"`max_in_flight` limits how many items of a parallel loop run at once."
It does not. At server v3.161.2, `loop.spec.max_in_flight` is parsed
into the grammar and **nothing reads it**: not the orchestrator, not
the server, not the worker. The server's resource model says the same:
"max_in_flight is parsed but has no reader, so it does not throttle
anything". To bound concurrency today, use `sequential` mode, split
the collection across steps, or size the worker pool
([Chapter 10](ch10-04-slots-and-keda.md)).
```

## The loop's result

When the last item completes, the step completes. Its result is a
**list** of each iteration's result, in the order the iterations
**completed**. In parallel mode that need not be the order of `in:`;
the code says so itself: "may not match dispatch index in parallel
mode" (`state.rs`). If order matters, have each iteration return its
own index or key.

An empty collection completes the step at once, with the result `[]`
and no commands dispatched.

## `cursor` mode

`mode: cursor` is for draining a work queue rather than a fixed list.
Instead of `in:`, the loop has a `cursor.claim` query (a `postgres`
tool by default) that atomically leases a batch of rows, for example
with `FOR UPDATE SKIP LOCKED`. The body runs once per claimed row,
`loop.spec.frame.row_concurrency` rows at a time (default 1). When the
batch is done, the next one is claimed. A claim that returns no rows
ends the loop. `frame.max_rows` caps each claim. The lease and
heartbeat fields are documented as advisory. Cursor mode is used only
when a playbook asks for it.

## On the local runtime

```admonish warning title="The local runtime ignores `loop:`"
At CLI v6.4.0 the local runtime parses `loop:` but has no code that
reads it. A loop step runs **once**, as if `loop:` were not there, and
the run ends `ok`. CI checks this (`examples/ch08/loop-runs-once`).
Locally, iterate with a back-edge ([6.4](ch06-04-back-edges.md)) or
inside one step: a set-based DuckDB query, or a Rhai script.
[Chapter 8](ch08-03-local-iteration.md) covers local iteration.
```

The examples on this page are distributed. CI validates them against
the schema but does not run them.

## Check your understanding

{{#quiz ../quizzes/ch06-03.toml}}
