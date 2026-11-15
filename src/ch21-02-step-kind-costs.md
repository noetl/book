# Per-Step-Kind Costs

<span class="status status-real">REAL</span>

The model profiles the tool kinds whose execution was read in the
worker and tools code (`step_kinds.kinds`, `as_of` 2026-11-11). For
each it says how the kind runs, **how long it holds a worker slot**,
and what timeout applies by default. The rest of the parser's kinds
(`artifact`, `gateway`, `gcs`, `iterator`, `nats`, `playbooks`,
`secrets`, `snowflake_transfer`, `workbook`) are listed as not
profiled; nothing is measured for them.

| Kind | Runs | Holds the slot | Default timeout |
|---|---|---|---|
| `python` | subprocess | whole run | none unless the step sets `timeout_seconds` |
| `shell` | subprocess | whole run | none unless the step sets `timeout_seconds` |
| `http` | in process | whole request | 30 s client default; `timeout_seconds` overrides. The body is read in full, no cap |
| `postgres` | in process, a pool per connection string | whole query | **none** set by the tool |
| `duckdb` | in process | whole query, in the worker's memory | **none** |
| `rhai` | in process | whole script | **none**, and no operation limits |
| `wasm` | in process, **one module at a time per worker** | invocation **plus any wait for the wasm lock** | 30 s ([21.3](ch21-03-limits.md)) |
| `mcp` | remote JSON-RPC | whole call | `NOETL_MCP_REQUEST_TIMEOUT_SECONDS`, clamped to 180 s |
| `agent` | in-process loop of remote model calls | **the whole loop** | bounded by tool-call and child limits |
| `playbook` | a separate child execution | only for the start request; with `return_result` / `return_step` the **whole child**, polling every 2 s | 30 s to start; the await is the step's timeout, else 180 s / 300 s |
| `script` | Kubernetes Job, polled every 2 s | until the Job finishes | 600 s |
| `container` | Kubernetes Job | **no**: freed once the Job is created; a callback ends the step | none by default |
| `snowflake` | remote REST | whole statement | 60 s statement timeout |
| `task_sequence` | in process, sub-tasks in order | all sub-tasks | per sub-task |
| `noop` | in process | briefly | it still pays the per-step orchestration cost |

(Each row cites tools v4.6.0 or worker `d1c9584`, which is in v6.15.0;
the citations are in [Appendix D](appendix-04-resource-model.md#step-kinds).)

## Two rules that hold for every kind

- **No global timeout.** "The worker sets no wall-clock timeout per
  command" (`step_kinds.no_global_timeout`, tools v4.6.0
  `src/registry.rs:241-259`). A kind with no default timeout can hold a
  slot indefinitely unless the step sets one.
- **The tool retry config is inert.** `ToolConfig.retry` is parsed but
  no executor applies it (`step_kinds.retry_config_inert`). Do not
  budget for automatic retries ([6.5](ch06-05-errors-timeouts-retries.md)).

## What has been measured

Only a few kinds have numbers, and most of them are about
**orchestration around** the kind, not the kind itself:

| Kind | Figure | Label |
|---|---|---|
| `python` | 0.66 s warm / 1.20 s cold for a simple playbook end to end | MEASURED, idle kind, 2026-05 |
| `python` | 9.3 s → 3.0 s when a provider call moved from a `kind: playbook` child to inline python | MEASURED, prod, 2026-08-24 |
| `playbook` | ~9 s of orchestration per hop, regardless of the work inside | MEASURED, prod, 2026-08-24 |
| `playbook` | median 34.7 s → 19.4 s (−44%) when provider children were inlined | MEASURED, prod, 2026-06-29 (paired A/B) |
| `wasm` | ~1.5 s once, first dispatch of a ~1.6 MB module on a fresh pod | MEASURED, kind, 2026-06 |
| `agent` | a hosted LLM call inside a real step | NOT_YET_MEASURED |

The per-step latency of `http`, `duckdb`, `postgres` and `mcp` steps on
prod is **not measured** ([21.6](ch21-06-not-yet-measured.md)).

## Check your understanding

{{#quiz ../quizzes/ch21-02.toml}}
