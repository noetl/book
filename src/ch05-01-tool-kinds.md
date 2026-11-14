# The Tool Kinds

<span class="status status-real">REAL</span>

The server publishes the list of kinds it accepts in its DSL manifest,
`orchestrate-core/schema/dsl-manifest.json`. At **server v3.161.2**
(commit `983e36e`) the manifest lists **27 kinds**. **25** are accepted
with no flag set, and **2** are gated, off unless the server sets a
flag:

| Gated kind | Server flag | Also needs |
|---|---|---|
| `agent` | `NOETL_TOOL_KIND_AGENT` | a worker started with `NOETL_WORKER_AGENT_TOOL=true` |
| `mcp` | `NOETL_TOOL_KIND_MCP` | — |

With its flag off, the server refuses a gated kind like any unknown
kind. [Chapter 18](ch18-00-mcp-and-agents.md) covers both.

The 25 kinds accepted by default, grouped by what they do:

| Group | Kinds |
|---|---|
| Run code | `python`, `shell`, `rhai`, `wasm`, `noop` |
| Query and move data | `postgres`, `duckdb`, `ducklake`, `snowflake`, `snowflake_transfer`, `transfer`, `gcs`, `artifact` |
| Call out | `http`, `gateway` |
| Run on Kubernetes | `script` (a Job the worker polls), `container` (a Job that calls back) |
| Compose | `playbook`, `playbooks`, `iterator`, `workbook`, `task_sequence` |
| Messaging and secrets | `nats`, `subscription`, `secrets` |

**Accepted** means the server's parser takes the kind. Whether a given
worker can run it is a separate question. The manifest says so
itself: "Which kinds a live worker can execute is reported by workers
… and is not known to this process."

[Appendix B](appendix-02-tool-kinds.md) is generated from the manifest
and the resource model. For every kind it gives how a worker executes
it, how long it holds a slot, its default timeout, and any measured
figures.

## How some common kinds run

From the resource model's `step_kinds`, all DEFAULT values at
v3.161.2, citing tools v4.6.0:

| Kind | Runs as | Holds the slot | Default timeout |
|---|---|---|---|
| `python` | a subprocess on the worker | for the whole run | **none** unless the step sets one |
| `shell` | a subprocess | for the whole run | **none** unless set |
| `http` | in-process (reqwest) | for the whole request | 30 s |
| `postgres` | in-process, one pool per connection string | for the whole query | **none** |
| `duckdb` | in-process | for the whole query | **none**; a large query uses the worker pod's memory |
| `rhai` | in-process | for the whole script | **none**, and no operation limits |
| `playbook` | a separate child execution ([Chapter 7](ch07-00-sub-playbooks.md)) | only for the start request, unless the parent waits for the result | 30 s for the start request |
| `container` | a Kubernetes Job | **no**: the slot is freed once the Job is created | none by default |
| `noop` | in-process | briefly, but it still pays the per-step orchestration cost | — |

## `python` is a worker kind, not a retired one

```admonish myth
"NoETL dropped Python." What was retired is the **Python platform**:
the old Python server, worker and tools, removed from `noetl/noetl` in
2026-08 (523 files, `25bef859`). Each is now its own Rust repository.
`kind: python` is still a supported tool. On a worker it runs your
code in a `python3` subprocess (tools v4.6.0 `src/tools/python.rs`).
What has no Python is the **local runtime**: CLI v6.4.0 refuses
`kind: python` before any step runs.
```

A `python` step gets its tool `args` as a dict named `args`. It
reports a value by setting a global `result`, or by a top-level
`return`, which the tool wraps in a function for you:

```yaml
{{#include ../examples/ch05/python-step/playbook.yaml}}
```

This example needs a worker, so the book's CI validates it against
the schema but does not run it.

## Local kinds, and fields that differ

The local runtime (CLI v6.4.0) accepts its own set of kinds:
`agent`, `auth`, `duckdb`, `http`, `mcp`, `noop`, `playbook`,
`provider`, `rhai`, `shell` and `sink`. Any other kind is refused
before the first step runs, with the list
([Chapter 8](ch08-00-local-runtime.md)). Three of those, `auth`,
`provider` and `sink`, are local-only: the server's parser does not
accept them.

Even a kind both runtimes accept can take **different fields**. The
sharpest case is `shell`:

| | Worker (tools v4.6.0) | Local (CLI v6.4.0) |
|---|---|---|
| Field | `command:` (one string) | `cmds:` (a string or a list) |
| Written with the other runtime's field | `cmds:` alone fails: `command` is a required field of `ShellConfig` | `command:` is **ignored**: the step runs nothing |

```yaml
{{#include ../examples/ch05/shell-command-local/playbook.yaml}}
```

Locally, this step runs nothing, is not even recorded as executed, and
the run still ends `ok` (checked in CI):

```json
{{#include ../examples/ch05/shell-command-local/expected.json}}
```

So there is no `shell` step that runs on both runtimes. For examples
that must run in both places, this book uses `rhai`, whose `code:`
field is the same on both sides.

## Check your understanding

{{#quiz ../quizzes/ch05-01.toml}}
