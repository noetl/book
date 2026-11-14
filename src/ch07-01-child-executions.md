# `kind: playbook` and Child Executions

<span class="status status-real">REAL</span>

```yaml
{{#include ../examples/ch07/await-child/playbook.yaml}}
```

(A distributed example: CI validates it against the schema but does not
run it.)

## What the call creates

On a cluster, a `kind: playbook` step does not run the child inside the
parent. The worker calls the server's `POST /api/execute` and starts a
**separate execution** of the child, which has its own event log
([Chapter 3](ch03-02-event-sourcing.md)) and runs on whatever worker pool
its own steps target. The worker sends the parent's id with the
request, so the child carries a **`parent_execution_id`**
(`src/tools/playbook.rs`, tools v4.6.0). A step can override it with
`parent_execution_id:`.

The step's fields include:

| Field | Meaning |
|---|---|
| `path` | the child's catalog path (and optionally `version`, `digest`) |
| `args` | the child's inputs, sent as the `payload` of its execute request (`payload:` is accepted too) |
| `return_result` | `true`: wait for the child and use **its result** as this step's result |
| `result_step` | with `return_result`: which child step's result to return. Unset: the latest `call.done` result |
| `return_step` | legacy: wait, and return the child's **status** payload instead of its data |
| `timeout` | seconds: the start request (default **30**), and also the wait (default **180** with `return_result`, **300** with `return_step`) |
| `poll_interval` | seconds between status polls while waiting (default **2**, minimum 1) |

All the defaults are DEFAULT values in tools v4.6.0.

## Fire-and-forget or await

| | Default (async) | `return_result: true` (or `return_step`) |
|---|---|---|
| The step returns | as soon as the child **starts**, with `{status, execution_id}` | when the child **finishes**, with its result |
| The parent's slot is held | only for the start request | for the **whole wait**, polling every 2 s |
| On timeout | — | `return_result`: the step **fails**. It does not return an empty result |

The default is async: a parent that does not ask to wait only starts
the child. `return_result` is opt-in because, as the source puts it,
the 100+ existing callers keep their async semantics. An operator
kill-switch, `NOETL_PLAYBOOK_AWAIT_CHILD_RESULT` (default `true`), can
turn `return_result` back into the legacy status payload.

```admonish warning title="An awaiting parent and its child can deadlock a small pool"
While a parent awaits, it holds a slot **and** its child needs one. If
both run on the same small pool, enough concurrent awaiting parents can
occupy every slot, and no child can start. The resource model's
guidance is to budget **two slots per awaiting parent** and to avoid
sending both to a small pool (`step_kinds` `deadlock_note`, GUIDANCE).
```

## Calling another NoETL instance

`path` can also name a playbook on **another NoETL instance**
(`noetl://<instance>/<path>` or `peer/<instance>/<path>`), with
`remote: import | delegate`. That is gated on the server and covered in
[Chapter 17](ch17-00-cross-instance.md).

## Locally

The local runtime runs `kind: playbook` **in the same process**, with
`path` relative to the parent file. `input:` becomes the child's
workload. As on a cluster, the step has no result unless it sets
`return_result: true` (`examples/ch08/sub-playbook`, CI). See
[8.2](ch08-02-local-kinds.md). The two runtimes use different field
names for the child's inputs: `args` on a worker, `input` locally.

## Check your understanding

{{#quiz ../quizzes/ch07-01.toml}}
