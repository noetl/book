# Errors, Timeouts and Retries

<span class="status status-partial">PARTIAL</span>

This page is **PARTIAL** because most of the error-handling keys in the
grammar are parsed and then ignored. The grammar describes more than
the engine does. The table below separates the two, checked at
**server v3.161.2**, **worker v6.15.0** and **tools v4.6.0** by
searching for every reader of each key.

| Key | In the grammar | Applied? |
|---|---|---|
| `spec.on_error` (`fail` / `continue` / `retry`) | yes (`StepSpec`) | **no**: no reader in server, worker or tools |
| `spec.timeout` (`"30s"`, `"5m"`) | yes (`StepSpec`) | **no**: no reader; step commands carry no timeout |
| `tool.eval` (`continue` / `retry` / `break` / `jump` / `fail`, with `attempts`, `backoff`, `delay`) | yes; the validator checks the action names | **no**: copied into the command, and no worker or tool reads it |
| the tool library's `retry` setting | — | **no**: "parsed but no executor applies it" (resource model `retry_config_inert`) |
| `spec.policy.rules` on a sub-task of a **tool list** | yes | **yes**: inside `task_sequence` only |
| a tool's own `timeout_seconds` | per kind | **yes**, for the kinds that read it |

```admonish myth
"Set `spec.on_error: retry` (or `retry:`) and NoETL will retry a failed
step." Nothing does that at these versions. `on_error`, `spec.timeout`
and `tool.eval` are accepted, validated in part, and then never
consulted. A failed step fails.
```

## What does retry: policy rules in a tool list

Inside an ordered tool list ([5.2](ch05-02-ordered-tool-list.md)), each
sub-task may carry `spec.policy.rules`. After the sub-task runs, the
first rule whose `when` matches decides what happens
(`task_sequence.rs`, tools v4.6.0):

```yaml
tool:
  - name: call_api
    kind: http
    method: GET
    url: https://api.example.com/v1/report
    spec:
      policy:
        rules:
          - when: "{{ output.status == 'error' and _attempt < 3 }}"
            then: { do: retry, delay: 2, backoff: exponential }
          - when: "{{ output.status == 'error' }}"
            then: { do: fail }
          - else:
              then: { do: continue }
```

- `do` is `continue`, `retry`, `jump` (with `to: <label>`), `break` or
  `fail`. An unknown or missing `do` means `continue`.
- `retry` defaults to 3 `attempts`, `backoff: none` and a `delay` of
  1.0 s. `backoff` may also be `linear` or `exponential`.
- A rule's `when` sees `output` (`status`, `data`, `error`) and the
  attempt number `_attempt`.
- When no rule matches, an error means `fail` and success means
  `continue`.

To retry a single tool this way, make it a one-item tool list. To
retry a whole step, use a back-edge with a counter
([6.4](ch06-04-back-edges.md)).

## Timeouts

The worker sets **no** wall-clock limit on a command (resource model
`no_global_timeout`, DEFAULT). Each tool kind brings its own default,
from the resource model at v3.161.2:

| Kind | Default timeout |
|---|---|
| `http` | 30 s; per-request `timeout_seconds` overrides it |
| `mcp` | 60 s (`NOETL_MCP_REQUEST_TIMEOUT_SECONDS`) |
| `script` | 600 s, also the Job's deadline |
| `agent` | 300 s per model request |
| `python`, `shell` | **none** unless the step sets `timeout_seconds` |
| `postgres`, `duckdb`, `rhai`, `transfer` | **none** |

All are DEFAULT. [Appendix B](appendix-02-tool-kinds.md) lists every
kind. A step with no timeout that hangs holds its worker slot
indefinitely.

## What a failure does

When a step's command fails (`command.failed`), the server
(`orchestrator.rs`, v3.161.2):

- **does not follow the failed step's `next` arcs**: there is no
  "on failure, go to …" arc;
- if other steps are still running, **waits**. The comment in the code
  says each in-flight branch gets to record its own outcome;
- once nothing is running, ends the execution **FAILED**, with
  `Failed steps: <names>`.

```admonish partial
Sibling branches keep running after a failure, and their completions
are handled by the normal path, which can dispatch their successors. A
failed step also counts as "done" for a fan-in barrier, so a step that
joins branches can still run after one branch failed. How the final
status is decided when the last sibling finishes *successfully* is in
code this book has read but not run. Treat that case as unverified.
```

On the local runtime (CLI v6.4.0), the first failing step stops the
whole run with an error, and nothing after it runs. CI checks this
(`examples/ch06/failure-local`).

## Check your understanding

{{#quiz ../quizzes/ch06-05.toml}}
