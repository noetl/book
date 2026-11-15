# Limits: WASM Fuel, Agent Caps, Context Sizes

<span class="status status-real">REAL</span>

A limit is a number that **stops** something. The model lists the ones
a worker or server enforces, each with the variable that changes it
(`limits`, `as_of` 2026-11-11). All are **DEFAULT**: code values a
deployment may override. The ones checked for this page against worker
v6.15.0 are marked ✓.

## Plug-ins (`kind: wasm`)

| Limit | Default | Variable |
|---|---|---|
| fuel per invocation | 10,000,000,000 ✓ | `NOETL_WASM_FUEL` (`0`, `off`, `none` or `unlimited` removes it) |
| wall clock per invocation | 30 s ✓ (10 ms granularity) | `NOETL_WASM_TIMEOUT_MS` |
| linear memory | 1024 MiB ✓ | `NOETL_WASM_MAX_MEMORY_MB` |

(worker `src/plugin.rs:41-47`.) A trip increments
`noetl_worker_plugin_limit_trips_total{limit}`. No metric reports the
fuel a run actually spent; the model says to read it from the worker's
debug log.

## Agent steps (`kind: agent`)

| Limit | Default | Variable |
|---|---|---|
| tool calls per agent step | 32 ✓ | `NOETL_AGENT_MAX_TOOL_CALLS` |
| time per playbook-bound child | 180 s ✓ | `NOETL_AGENT_TOOL_TIMEOUT_SECS` |
| turns | 8 | step `max_turns` |
| tokens per model call | 4096 | step `max_tokens` |

(worker `src/executor/agent_host.rs:50-51`; tools v4.6.0
`src/tools/agent.rs`.) The model cannot raise the tool-call budget;
exceeding it ends the step with `agent.final` refused:
`tool_call_budget`. Worst case for one step: 32 × 180 s = **96 minutes
of one held slot** (GUIDANCE).

## Sizes

| Limit | Default | What happens past it |
|---|---|---|
| step result in an event (`NOETL_EVENT_RESULT_CONTEXT_MAX_BYTES`) | 100 KiB | spilled to the result store; a downstream read becomes a fetch ([5.3](ch05-03-results-and-references.md)) |
| command context (`NOETL_COMMAND_CONTEXT_MAX_BYTES`) | 512 KiB | offloaded as a `__context_ref__` |
| request body on `/api/execute` and `/api/events` | 2 MiB | refused (the axum default; no explicit layer) |
| events returned by `GET /api/executions/{id}` | the 2000 most recent | older ones are not in the response |

## Waiting and draining

| Limit | Default | Variable |
|---|---|---|
| extra retry window for event emits while the server is down (the slot stays held) | 120 s | `NOETL_EVENT_EMIT_OUTAGE_BUDGET_SECS` |
| finishing in-flight commands on SIGTERM | 150 s | `NOETL_WORKER_DRAIN_TIMEOUT_SECS` |
| slots per worker | 4 ✓ | `WORKER_MAX_CONCURRENT` ([21.4](ch21-04-slot-model.md)) |

```admonish note title="What is not a limit"
There is **no** per-command wall-clock timeout, **no** cap on back-edge
re-runs, and **no** cap on `loop:` items
([6.4](ch06-04-back-edges.md)). A step is bounded by its own tool's
timeout and nothing else ([21.2](ch21-02-step-kind-costs.md)).
```

## Check your understanding

{{#quiz ../quizzes/ch21-03.toml}}
