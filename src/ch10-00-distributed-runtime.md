# The Distributed Runtime

<span class="status status-real">REAL</span>

The local runtime ([Chapter 8](ch08-00-local-runtime.md)) runs a whole
playbook in one process. The **distributed runtime** splits the same
work across services that each do one job. Its parts are a gateway, a
server, a command bus and pools of workers. This chapter follows a
request through them.

Every claim here was checked against **server v3.161.2**, **worker
v6.15.0** and **gateway v3.22.1**. Deployment numbers come from the
public resource model
([`noetl.ai/dsl/resource-model.json`](https://noetl.ai/dsl/resource-model.json)),
whose DEPLOYED entries were read off the production cluster on its
`as_of` date, **2026-11-11**.

## The path of one request

```text
 client
   │  HTTPS, session token
   ▼
 gateway ─────────────── authenticates, authorizes, proxies,
   │                     streams results back (SSE)
   │  POST /api/execute
   ▼
 server ──────────────── writes playbook_started, builds the first
   │                     commands, owns the event log and the catalog
   │  publish command notification
   ▼
 cmdbus-writer ───────── the EHDB command bus: a durable log per pool
   │                     and shard, plus a claim coordinator
   │  claim commands.<pool>.>
   ▼
 worker pools ────────── shared (user steps), system (the drive),
                         subscription; each worker has N slots
   │
   └─ events back to the server: POST /api/events
        └─ command.completed triggers the next drive pass,
           which runs as a command on the system pool
```

The loop at the bottom is the heart of it. A worker finishes a step and
reports `command.completed`. That event starts a **drive pass**: the
orchestrator reads the playbook and the events so far and decides the
next commands. By default that pass is itself a command, run as WASM on
a worker in the **system** pool ([10.2](ch10-02-server.md)).

## What each part owns

| Part | Runs | Owns | Never does |
|---|---|---|---|
| Gateway | `noetl-gateway` | sessions, request ids, the client's SSE stream | run tools or touch your data |
| Server | `noetl-server` | the event log, the catalog, command records, the first commands | run tools (it has no tool runtime) |
| Command bus | the worker binary in **host mode** (`cmdbus-writer`) | the durable command log and who claimed what | decide what runs |
| Workers | `noetl-worker`, one Deployment per pool | nothing between commands | read or write `noetl.*` directly; they call the server's API |

## Sections

- [10.1 Gateway](ch10-01-gateway.md): the gatekeeper, and the state it
  does keep.
- [10.2 Server](ch10-02-server.md): what happens on `POST
  /api/execute`, and where the drive runs.
- [10.3 The command bus and worker pools](ch10-03-bus-and-pools.md):
  subjects, claims, pools, and what happens when a worker dies.
- [10.4 Slots, pools and KEDA](ch10-04-slots-and-keda.md): capacity
  and autoscaling, with the deployed numbers.
- [10.5 Following one execution](ch10-05-one-execution.md): the
  event log of one run, step by step.

```admonish not-yet title="10.5 is not written yet"
Section 10.5 steps through the event log of one real execution with the
book's trace viewer ([T-05](https://github.com/noetl/book/issues/7)).
That needs an execution captured from a stack running tagged releases,
which the book does not have yet. The event sequence it will show is
already listed in [10.2](ch10-02-server.md#the-events-of-a-one-step-execution).
```

## Check your understanding

{{#quiz ../quizzes/ch10-00.toml}}
