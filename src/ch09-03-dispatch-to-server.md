# Dispatching to a Server

<span class="status status-real">REAL</span>

## `--dispatch server`

By default each message runs a playbook **locally**
(`--dispatch local`). With `--dispatch server`, the daemon instead
sends each message to a NoETL server as `POST /api/execute`
(`--server-url`, or the resolved base URL). The daemon becomes an
**ingress**: it listens at the edge and the cluster does the work.
That is how you run playbooks with `python`, `postgres` or `loop:`
from a subscription the cluster cannot reach directly. Combined with
the spool, messages survive a server outage.

## `noetl serve`: MCP and agents, locally

```console
$ noetl serve --playbooks ./playbooks
```

`noetl serve` scans a directory, recursively and on every request, for
playbooks that opt in with `metadata.expose`
([4.1](ch04-01-header.md)). It publishes them as:

- an **MCP server**: `POST /mcp`, one MCP tool per playbook with
  `expose.mcp`;
- **agents**: `/api/agents/*`, for playbooks with `expose.agent`, with
  callbacks to origins allowed by `--callback-origin`.

Defaults and limits (CLI v6.4.0 `noetl serve --help`):

| Option | Default |
|---|---|
| `--listen` | `127.0.0.1:8765`. Any non-loopback address needs `--token-file` |
| `--max-concurrent` | 4 playbooks at once; more are refused with 503 |
| `--task-db` | none: agent tasks are **in memory** and lost on restart |

`--task-db <file>` keeps agent tasks in **SQLite**, so they survive a
restart: finished tasks stay readable, working ones are rerun, and
owed callbacks are delivered. It was added in **CLI v6.3.0**
(2026-11-11, CHANGELOG "serve: durable agent tasks with --task-db").

`noetl subscribe --serve <addr>` serves the same surface for as long
as the daemon runs. [Chapter 18](ch18-00-mcp-and-agents.md) covers MCP
and agents in depth, including the server-side equivalents, which are
gated.

## Check your understanding

{{#quiz ../quizzes/ch09-03.toml}}
