# Choosing a Runtime

<span class="status status-real">REAL</span>

The same playbook grammar runs in three places. They are not
interchangeable. This page puts them side by side, with each cell tied
to the chapter or source it comes from. Versions: **CLI v6.4.0**,
**server v3.161.2** (resource model `as_of` 2026-11-11), worker
v6.15.0.

## At a glance

| | Local (`noetl run -r local`) | Daemon (`noetl subscribe` / `serve`) | Distributed (server + workers) |
|---|---|---|---|
| **Runs where** | in the CLI process | in a long-running CLI process | on a NoETL server's worker pools |
| **Started by** | you, once | each message, timer tick or HTTP call | `POST /api/execute`, the gateway, another playbook |
| **Tool kinds** | 11 local kinds; **no** `python`, `postgres`, `workbook`, …: refused up front ([8.2](ch08-02-local-kinds.md)) | the same as local, unless `--dispatch server` ([9.3](ch09-03-dispatch-to-server.md)) | 25 kinds accepted by default, plus `agent` and `mcp` behind flags ([5.1](ch05-01-tool-kinds.md)) |
| **`loop:`** | runs once ([8.3](ch08-03-local-iteration.md)) | runs once (local runtime) | sequential, parallel, cursor ([6.3](ch06-03-loop.md)) |
| **Tool lists** | parse error ([5.2](ch05-02-ordered-tool-list.md)) | parse error | one `task_sequence` command ([5.2](ch05-02-ordered-tool-list.md)) |
| **Passing values** | step `vars:` | step `vars:` | step `set:` ([4.2](ch04-02-workload-and-templating.md)) |
| **Concurrency** | none: targets run one after another ([8.1](ch08-01-in-process-interpreter.md)) | one message at a time; `serve` runs up to 4 playbooks at once (`--max-concurrent`, DEFAULT) ([9.3](ch09-03-dispatch-to-server.md)) | replicas × slots. The user pool is 8 slots at minimum and 80 at maximum, the system pool 4 (DEPLOYED, resource model `concurrency.pools`, as of 2026-11-11) |
| **Durability** | none. The optional event buffer is a record, not a resume point ([8.4](ch08-04-event-buffer.md)) | the local_disk spool survives outages; `--task-db` keeps agent tasks ([9.2](ch09-02-spool-and-trail.md), [9.3](ch09-03-dispatch-to-server.md)) | an append-only event log; state is folded from it ([3.2](ch03-02-event-sourcing.md)) |
| **Credentials** | the local store, `noetl credential` ([4.4](ch04-04-keychain.md)) | a `--credential` file for the source; the local store for steps | the keychain, resolved on the worker ([4.4](ch04-04-keychain.md)) |
| **Fixed cost per step** | small: in-process, no bus | the same as local per run | ~4.5 s per step on prod in 2026-08 (MEASURED, resource model); hops ~9–15 s ([7.2](ch07-02-what-a-hop-costs.md)) |
| **Needs** | the CLI | the CLI (and a message source, unless `timer`) | a server, a bus and worker pools ([Chapter 10](ch10-00-distributed-runtime.md)) |
| **Refuses or ignores** | non-local kinds (refused); `loop:`, bare-name `next`, `set:` (ignored) ([8.1](ch08-01-in-process-interpreter.md)) | the same as local | `case:` blocks; gated kinds and features unless their flags are on ([4.1](ch04-01-header.md)) |

```admonish warning title="Mind the per-step cost figure"
"~4.5 s per step" is a 2026-08 measurement of one playbook on prod.
The resource model warns that several of its figures "predate later
dispatch fixes". The latency plan (ai-meta PR #556, open) reports
~0.95 s per step on prod on 2026-11-02 (n = 4). Treat both as dated
measurements and measure your own cluster
([Chapter 22](ch22-00-orchestration-overhead.md)).
```

## How to choose

1. **Does it need `python`, `postgres` or another cluster-only kind, or
   real `loop:` fan-out?** Then distributed, or the daemon with
   `--dispatch server`.
2. **Is it triggered by messages, a schedule or HTTP calls, on one
   machine?** The daemon.
3. **Is it a one-off, a CI check or a fast edit-and-run loop, using
   local kinds?** Local.
4. **Must it run on both?** Write it for the server's rules, then
   check it against the local differences table
   ([8.1](ch08-01-in-process-interpreter.md)) before trusting a local
   run.

## Check your understanding

{{#quiz ../quizzes/ch11-00.toml}}
