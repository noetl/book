# The Daemon: `noetl subscribe` and `noetl serve`

<span class="status status-real">REAL</span>

The local runtime runs one playbook and exits. The **daemon** keeps the
CLI running and starts playbooks when something happens:

- **`noetl subscribe <spec>`** holds a message source open (NATS,
  Pub/Sub, Kafka or a timer) and runs a playbook **once per message**.
- **`noetl serve`** publishes playbooks over HTTP, as an **MCP server**
  (`POST /mcp`) and as **agents** (`/api/agents/*`), and runs one per
  call. `noetl subscribe --serve <addr>` does both in one process.

Both run playbooks on the **local runtime** ([Chapter 8](ch08-00-local-runtime.md)),
with all of its rules and limits. Neither needs Kubernetes, a NoETL
server or a database (`noetl instance --help`: "Run a kind:Subscription
listener standalone in local mode (no k8s, no server)", CLI v6.4.0).

```admonish note title="What the daemon is not"
It is not a general-purpose service manager or scheduler. It runs one
subscription spec (plus, optionally, an HTTP surface) per process. The
`timer` source gives it a schedule, but there is no job table and no
cluster. For durable, multi-worker execution, dispatch to a server
([9.3](ch09-03-dispatch-to-server.md)) or use the distributed runtime
([Chapter 10](ch10-00-distributed-runtime.md)).
```

## Sections

- [9.1 Subscriptions](ch09-01-subscriptions.md): the spec, the sources,
  one run per message
- [9.2 Spooling and the event trail](ch09-02-spool-and-trail.md)
- [9.3 Dispatching to a server](ch09-03-dispatch-to-server.md), and
  `noetl serve`

## Check your understanding

{{#quiz ../quizzes/ch09-00.toml}}
