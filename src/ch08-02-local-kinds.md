# Local Tool Kinds and Their Limits

<span class="status status-real">REAL</span>

At CLI v6.4.1 the local runtime accepts **eleven** kinds: `shell`,
`http`, `playbook`, `duckdb`, `auth`, `sink`, `rhai`, `provider`,
`agent`, `mcp` and `noop`. That is the list in its refusal message
(`LOCAL_KINDS_FOR_MESSAGE`). The check itself asks the CLI's `Tool`
type, so the message cannot drift from it. Three of them (`auth`,
`provider`, `sink`) do not exist on a server
([Appendix B](appendix-02-tool-kinds.md)).

## Everything else is refused, before anything runs

Any other kind fails the whole run **before the first step**, with every
offending step listed. This is the real output for a `python` step
(`examples/ch08/python-refused`, checked in CI):

```text
Error: Playbook 'py_local' uses tool kinds the local runtime cannot run:
  step `start`: kind `python`
Local tool kinds: shell, http, playbook, duckdb, auth, sink, rhai, provider, agent, mcp, noop.
Run it on a cluster instead: noetl run … --runtime distributed
```

```admonish myth
"The local runtime runs Python and Postgres steps." It runs neither.
`python`, `postgres`, `workbook` and every other non-local kind are
refused up front. CI checks `python`, `postgres` and `workbook`
(`examples/ch08/python-refused`, `postgres-refused`, `workbook-refused`).
```

The check used to skip such steps with a note and still end the run
`ok`. It became a hard refusal so that one run lists everything a
playbook would need to move to a cluster (comment on
`reject_unsupported_kinds`, citing noetl/ai-meta#539).

## Notes on the local kinds

| Kind | Locally |
|---|---|
| `rhai` | Runs the script in-process. The result is the last expression. `code:` is the same field as on a worker, so `rhai` is the most portable kind. |
| `shell` | Runs `cmds:` (a string or a list). **`command:` is ignored**, and the step then runs nothing ([5.1](ch05-01-tool-kinds.md)). |
| `http` | `method`, `url`, `headers`, `params`, `body`. The result is `{status, body}`. `credential: <alias>` reads the local credential store (`noetl credential set`). |
| `duckdb` | `db:` (default `.noetl/state.duckdb` **next to the playbook**; relative paths resolve against the playbook's directory), `query:`, `params:` (bound `?` values). The result is the rows as JSON. |
| `playbook` | Runs the child **in the same process**, resolving `path` relative to the parent. `input:` is passed to the child as workload. The step has **no result unless `return_result: true`**, the same opt-in as on a cluster. A path on another NoETL instance (`noetl://…`, `peer/<instance>/…`) is refused. |
| `mcp` | Calls an MCP server at a URL. A `server: mcp/<path>` catalog reference is refused unless `NOETL_MCP_<SLUG>_ENDPOINT` or `NOETL_MCP_URL` supplies an endpoint. |
| `agent` | Runs a model call loop. Credentials come from the local store. |
| `sink` | Writes the result of the most recently completed step to a file, a DuckDB table or GCS (`format:` `json`, the default, `yaml` or `csv`). See below. |
| `auth`, `provider` | Local-only. `auth` obtains a provider access token (`provider`, `scopes`); `provider` runs cloud-provider operations through the same tool a worker would use. |
| `noop` | Does nothing, and the step is **not recorded** in `executed_steps`. |

The sub-playbook case, run in CI (`examples/ch08/sub-playbook`):

```yaml
{{#include ../examples/ch08/sub-playbook/playbook.yaml}}
```

```json
{{#include ../examples/ch08/sub-playbook/expected.json}}
```

```admonish note title="Fixed in v6.4.1: `sink` writes the most recent result"
Up to CLI v6.4.0 the local `sink` tool wrote
`context.step_results.values().last()`. `step_results` is a hash map,
which has no defined order, so once two or more steps had results the
sink wrote an arbitrary one, and which one changed from run to run.
From **v6.4.1** (noetl/cli#111) the runner records which step finished
most recently, a back-edge re-run included, and the sink writes that
step's result.
```

This example has eight steps that each produce a result before the
sink, then reads the file back. On v6.4.0 it printed a different word
on different runs; on v6.4.1 it always prints `eight`
(`examples/ch08/sink-last-result`, run in CI). `sink` is local-only, so
the server's playbook schema refuses this playbook; CI checks that too:

```yaml
{{#include ../examples/ch08/sink-last-result/playbook.yaml}}
```

```text
{{#include ../examples/ch08/sink-last-result/expected.txt}}
```

## Check your understanding

{{#quiz ../quizzes/ch08-02.toml}}
