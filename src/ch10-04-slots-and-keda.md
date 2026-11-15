# Slots, Pools and KEDA Autoscaling

<span class="status status-real">REAL</span>

How many steps can run at once, and what happens to the rest? The
answer is the slot model plus the autoscaler. Code facts are worker
**v6.15.0**. Numbers labelled **DEPLOYED** are from the public resource
model ([`noetl.ai/dsl/resource-model.json`](https://noetl.ai/dsl/resource-model.json)),
which read them off the production cluster on **2026-11-11**; they
describe that cluster on that day, not a default and not a
recommendation.

## A slot is a semaphore permit

Each worker process has **`WORKER_MAX_CONCURRENT`** slots, default
**4** (`src/config.rs:115-118`), held in a semaphore
(`src/worker.rs:313`). The claim loop takes a slot **before** it pulls
a command (`worker.rs:748-754`), so a full worker claims nothing. The
slot is released:

- when the command's tool returns and its events are sent
  (`worker.rs:848-850`);
- at once, if the claim turns out to be already taken, deferred or
  failed (`worker.rs:926-999`), or the pull returns nothing;
- early, when a step **parks on an external callback**: the worker
  skips its own `call.done` and frees the slot while the external
  system works (`src/executor/command.rs:1326-1333`).

So **a pool's capacity is replicas × slots**. Commands beyond it wait
on the command bus, not in the worker.

## The deployed pools

| Pool | Replicas | Slots each | Capacity | CPU / memory (request / limit) | Label |
|---|---|---|---|---|---|
| `worker-rust-pool`, the user pool (`shared`) | 2, KEDA 2-20 | 4 | 8 at min, 80 at max | 250m / 2; 256Mi / 768Mi | DEPLOYED |
| `worker-system-pool` (two Deployments) | 1 + 1, **fixed** | 2 | 4 | 750m / 2; 3Gi / 3Gi | DEPLOYED |

The system pool runs every drive pass ([10.2](ch10-02-server.md#where-the-drive-runs)),
and every `system/` playbook. On that cluster at most **4** of those
run at a time, whatever the user pool's size.

## Autoscaling on bus lag

```admonish myth
"KEDA scales the workers on NATS consumer lag." NATS is gone. The
trigger is **`ehdb_feed_subject_lag`**, the number of commands waiting
on a subject. The `cmdbus-writer` serves it on its metrics face,
sampled every 2 s, one series per `commands.<pool>.shard.<n>` subject
(worker `src/command_bus.rs:505-518`). The server does not produce it.
```

The deployed ScaledObject (DEPLOYED, 2026-11-11):

| Setting | Value |
|---|---|
| target | `noetl-worker-rust` (the user pool) |
| trigger | `metrics-api`: `ehdb_feed_subject_lag{subject="commands.shared.shard.0"}` from the command-bus writer |
| target value | 2 |
| min / max replicas | 2 / 20 |
| polling interval / cooldown | 10 s / 30 s |

With a target of 2, KEDA aims for about **one replica per two waiting
commands**: `replicas ≈ ceil(lag / 2)`, between 2 and 20 (the rule the
resource model records with the ScaledObject; it describes the
setting, not a measured response).

```admonish myth
"The system pool autoscales too." The `noetl/ops` repository declares
a system-pool ScaledObject (3-10 replicas). The resource model records
that it is **not on the cluster**, so the system pool does not scale.
A manifest in a repository is a statement of intent; only a read of
the cluster says what runs.
```

## What has been measured

| What | Value | Label |
|---|---|---|
| user pool under 200 real executions (200/200 completed) | replicas 2 → 4 → 8 → 16 → 20 → 2 | MEASURED, prod, 2026-07-31 |
| a new GKE Autopilot node when a scale-up needs one | ~60-90 s | MEASURED, prod |
| `command.issued` → `command.claimed`, pool not saturated | p50 138.5 / p95 156.4 / p99 181.0 ms (n = 60) | MEASURED, prod, 2026-07-30 |
| the same, 90 commands offered in 1.2 s against 8 slots | p50 2123 / p99 3735 ms | MEASURED, prod, 2026-07-30 |
| time for the user pool to ramp under load on the EHDB trigger | no number | NOT_YET_MEASURED |
| sustained executions per second | no number | NOT_YET_MEASURED |

(All from the resource model's `concurrency` section, which names each
source.) The fourth row is the slot model at work: 90 commands, 8
slots, so most of them waited on the bus. The 2 s median is queueing,
not the bus being slow.

## Check your understanding

{{#quiz ../quizzes/ch10-04.toml}}
