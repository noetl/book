# Back-Edges: Loops Made of Arcs

<span class="status status-real">REAL</span>

A **back-edge** is an arc to a step that has already run. Guarded by
`when`, it turns part of the workflow into a loop: fetch a page, check
whether there is another, go back and fetch again. This is how NoETL
expresses loops whose length is not known in advance, such as
pagination, polling and retries of a whole step.

```yaml
{{#include ../examples/ch06/back-edge/playbook.yaml}}
```

The loop variable travels in `set:`. Each completion of `fetch_page`
persists `page` as a `ctx.updated` event, so the next pass, and the
re-dispatched step, sees the new value
([4.2](ch04-02-workload-and-templating.md)).

## How the server recognises one

Every completion event triggers a pass that re-evaluates the arcs of
every completed step, so the orchestrator must tell a real loop from a
stale arc. An arc from `src` to `target` is treated as a back-edge, and
re-dispatches `target`, only when all three of these hold
(`orchestrator.rs`, v3.161.2):

1. `target` has already finished;
2. `target` can reach `src` through the workflow, so there is a cycle;
3. `src` finished **after** `target`, or the arc is a self-loop.

Re-dispatching does not reset anything. A step's state and its result
are kept **by step name**, so each new completion overwrites the
previous result. If you need every page's result, collect them
yourself, in `set:` or in a data store. Back-edges are also left out
of fan-in barriers, so a step that waits for several branches does not
wait for a loop's earlier iterations.

## Nothing bounds it but your guard

```admonish myth
"The server stops a runaway loop after some number of iterations." It
does not. At v3.161.2 there is **no cap** on how many times a
back-edge can re-run a step, and none on how many items a `loop:` can
have. A search of the server, worker and tools for iteration or
re-entry limits finds only the tool-list cap, which counts sub-tasks
*inside one step* ([5.2](ch05-02-ordered-tool-list.md)). The `when`
on the back-edge is the only thing that ends the loop.
```

A related setting is easy to mistake for a cap.
`NOETL_RECONCILE_MAX_NOOPS` (default 225, about 30 minutes at the 8 s
reconcile tick) stops the server **re-driving an execution that is
making no progress**. A loop that is making progress resets it, so it
is not a bound on a loop.

So before shipping a back-edge, answer the question in this section's
quiz: *will this loop terminate?* The guard must reach false on every
path, for example a counter compared to a limit, or a "has more" flag
that the source eventually clears.

## On the local runtime

Back-edges work locally (CLI v6.4.0), with the local variable rules:
the counter travels in step `vars:`, not `set:`. This version runs in
CI:

```yaml
{{#include ../examples/ch06/back-edge-local/playbook.yaml}}
```

```json
{{#include ../examples/ch06/back-edge-local/expected.json}}
```

`count` ran three times, but `executed_steps` lists it once, because
the local result lists each step the first time it runs. The local
runtime has no cap either. An unguarded back-edge was observed still
running, with no output, when it was stopped after 60 seconds.

## Check your understanding

{{#quiz ../quizzes/ch06-04.toml}}
