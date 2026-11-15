# The Command Bus and Worker Pools

<span class="status status-real">REAL</span>

A command is a request to run one step. The server writes it down, the
**command bus** holds it until a worker takes it, and exactly one
worker runs it. This section covers how that hand-off works at server
**v3.161.2** and worker **v6.15.0**.

## The bus is EHDB, and it is a worker binary

```admonish myth
"Commands travel over NATS." Not any more. NATS is refused outright:
`NOETL_COMMAND_BUS` is required, has no default, and only the EHDB bus
is accepted (server `src/command_bus.rs:47-90`, worker
`src/command_bus.rs:85-115`). Names such as `nats_filter_subject` in
the worker's config are leftovers.
```

The bus runs as the **`cmdbus-writer`**, a StatefulSet that runs the
**worker binary in host mode** (`NOETL_COMMAND_BUS_HOST=true`, worker
`src/worker.rs:159-204`). It is not a separate product. It hosts:

- an **ingest** face, where the server publishes command notifications;
- a **claim coordinator**, where workers compete for them;
- a **metrics** face, which the autoscaler reads ([10.4](ch10-04-slots-and-keda.md)).

(`src/command_bus.rs:129-200`; each face has its own
`NOETL_COMMAND_BUS_*_BIND`.) The same process can also host the
**event** bus (`NOETL_EVENT_BUS_HOST`), which serves the gateway's live
feed and its key-value store ([10.1](ch10-01-gateway.md)).

## Subjects

The writer files each command under a subject derived from the
notification, `commands.<pool>.shard.<n>` (worker
`src/command_bus.rs:364-368`). A worker claims everything for its pool
with the filter **`commands.<pool>.>`** (`src/worker.rs:233-244`).

A worker learns its pool from `NOETL_FEED_FILTER_SUBJECT` (for example
`noetl.commands.shared.>`), and **refuses to start** without one:
"Refusing to default … because a worker on the wrong pool stalls
executions silently" (`worker.rs:236-242`).

## Which pool runs a step

The pool is chosen **once per execution**, when the server publishes
the first command (`src/handlers/execute.rs:1976-1983`):

1. the request's pool override (`execution_pool`, or the
   `x-noetl-pool` header), if given;
2. otherwise from the playbook's catalog path: `system/…` → `system`,
   `subscription/…` → `subscription`;
3. otherwise **`shared`**.

```admonish myth
"Each step can choose its pool." There is no step-level pool field in
the playbook model at v3.161.2. Every step of an execution goes to the
same pool, and the drive passes between steps go to `system`
([10.2](ch10-02-server.md#where-the-drive-runs)).
```

## Claiming: two locks

1. **The bus** hands a command to one worker and waits for an ack.
   An unacked command is redelivered after
   `NOETL_COMMAND_BUS_ACK_WAIT_SECS` (default **30 s**, worker
   `src/command_bus.rs:191`).
2. **The server** is the real gate. The worker calls
   `POST /api/commands/{id}/claim`, which takes a Postgres advisory lock
   on the command id and checks for an existing claim
   (`claim_command`, server `src/handlers/events.rs:929-1134`). This
   writes `command.claimed`. A second claimant is told the command is
   already claimed and skips it.

Only after the server claim succeeds does the worker ack the bus and
start the tool (worker `src/worker.rs:821-833`).

## When a worker dies mid-command

```admonish myth
"If a worker crashes, its step is retried on another worker." At
default flags it is not. The bus was acked when the claim succeeded,
so it will not redeliver. The command stays claimed by a worker that no
longer exists, no `command.completed` arrives, and the execution stays
**RUNNING**. The server's reconciler re-drives it every 8 s and finds
nothing new to issue (server `src/config/app.rs:600-608`), until
`NOETL_RECONCILE_MAX_NOOPS` (default 225, about 30 minutes) stops the
re-driving ([6.4](ch06-04-back-edges.md#nothing-bounds-it-but-your-guard)).
After that it is simply RUNNING, forever.
```

Two server sweeps end such an execution, and both are **off by
default**:

| Sweep | Flag (default) | What it does |
|---|---|---|
| orphan sweep | `NOETL_ORPHAN_SWEEP_ENABLED` (`false`) | finds a claim held by a worker with no heartbeat (TTL 90 s) after a grace of 180 s, and writes **`playbook.failed`** (`app.rs:608-660`) |
| non-convergence sweep | `NOETL_NONCONVERGENCE_SWEEP_ENABLED` (`false`) | writes **`playbook.failed`** for an execution whose newest event has not moved for a grace period while no live worker holds a command: the shapes the orphan sweep cannot see, such as a command never claimed or a router whose arcs were all false (`src/main.rs:1361-1378`, `app.rs:680-700`) |

Neither re-runs the step: the orphan sweep "never re-executes a
side-effecting step". A playbook cannot catch the crash either. Its
retry rules react to a `command.failed` ([6.5](ch06-05-errors-timeouts-retries.md)),
and none arrives. A crash mid-step ends, at best, in a failed
execution that you re-submit, so a step that might be re-run that way
should be safe to run twice.

## Check your understanding

{{#quiz ../quizzes/ch10-03.toml}}
