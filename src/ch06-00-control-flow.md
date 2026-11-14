# Control Flow

<span class="status status-real">REAL</span>

A playbook's steps say *what* to do. Their `next`, `when` and `loop`
keys say *in what order*, *whether* and *how many times*. This chapter
covers all three, plus what happens when a step fails
([6.5](ch06-05-errors-timeouts-retries.md)).

Control flow is where most wrong beliefs about NoETL live, so every
rule here is tied to the code that implements it. Server rules are from
the orchestrator in `orchestrate-core` at **server v3.161.2** (commit
`983e36e`). It is the same engine whether the server drives an
execution itself or runs it as WASM on a worker. Local behaviour is
from **CLI v6.4.0**, and every local claim is a CI example.

## How an execution moves

The server does not run a playbook as a script from top to bottom.
It reacts to events:

1. The execution starts by dispatching the step named `start`.
2. When a step finishes, the worker reports it with a completion
   event. That event triggers an **orchestration pass**.
3. In each pass the orchestrator evaluates the `next` arcs of the
   completed steps, applies their `when` guards, and dispatches the
   targets that are taken. A target that is not taken is recorded with
   a `step.skipped` event.
4. Steps dispatched in the same pass run **at the same time**, each in
   its own worker slot.

The whole history, including every dispatch, completion and skip, is
the execution's event log ([Chapter 3](ch03-00-what-noetl-is.md)).

## When an execution is finished

An execution **completes** when nothing is still running and either a
step named `end` has completed, or some step with **no `next`** has
completed (`check_completion`, `orchestrate-core/src/orchestrator.rs`).
It **fails** when a step fails and nothing else is still running
([6.5](ch06-05-errors-timeouts-retries.md)).

There is a third outcome, and it surprises people.

```admonish warning title="A branch whose arcs all fail stalls the execution"
If a step **has** `next` arcs and none of them is taken (every `when`
is false), nothing is dispatched. That step is not a step "with no
`next`", so it does not count as an ending either. If nothing else is
running, the execution is **neither completed nor failed**: it has no
terminal event and stays in progress.

The server's own sweep for this shape ("all branches evaluated false,
no successor issued", `src/handlers/nonconvergence_sweep.rs`) is off
by default (`nonconvergence_sweep_enabled: false`). When it is turned
on, it fails such an execution after a 24-hour grace period.

**Always give a router a final arc with no `when`**, a default branch,
unless a stall is what you want.
```

`end` is a convention, not a keyword. The engine treats a target named
`end` specially. The validator, though, requires every `next` target
to be a step in the playbook. So to route to `end`, define a step
called `end`.

## Sections

- [6.1 `next`](ch06-01-next-and-routers.md): the four forms and the two modes
- [6.2 `when`](ch06-02-when-guards.md): guards on arcs and on steps
- [6.3 `loop`](ch06-03-loop.md): one step, many items
- [6.4 Back-edges](ch06-04-back-edges.md): loops made of arcs
- [6.5 Errors, timeouts, retries](ch06-05-errors-timeouts-retries.md): what is applied and what is only parsed

## Check your understanding

{{#quiz ../quizzes/ch06-00.toml}}
