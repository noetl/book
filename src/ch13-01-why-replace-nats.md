# Why NATS Was Replaced

<span class="status status-real">REAL</span>

Until July 2026 NoETL's commands and events travelled over **NATS
JetStream**. Today NATS is gone from the platform: the server and the
workers refuse to start with any command bus but EHDB
(`NOETL_COMMAND_BUS`, required, worker v6.15.0
`src/command_bus.rs:85-115`).

## The dates

| Date | What happened | Record |
|---|---|---|
| 2026-07-15 | The decision: "EHDB takes over from NATS" | ai-meta `docs/rfc/ehdb-nats-takeover-plan.md` |
| 2026-07-26, 07-27 | Two earlier attempts did not complete: held at canary (07-26), then a full flip that failed (07-27) | Sessions-Log, 2026-07-28 |
| **2026-07-27** | **The third flip succeeded**: EHDB is the production command bus (server v3.58.1, worker v5.81.1) | Sessions-Log, "2026-07-28 — EHDB is the production command bus" |
| **2026-08-01** | **NATS deleted**: its namespaces removed (server v3.60.1, worker v5.88.0) | Sessions-Log, "2026-08-01 — NATS IS DELETED" |

## The reasons given

- **One fewer system to run.** The coupling RFC's goal was no external
  infrastructure dependency except Kubernetes.
- **Delivery in one hop.** The takeover plan's design has a stateful
  writer per shard that owns both the durable log and delivery;
  workers subscribe to it directly and the server is out of the
  delivery path (`ehdb-nats-takeover-plan.md`, decision 3).
- **A plaintext credential retired** (ai-meta#188).

```admonish note title="The analysis recommended the opposite"
The transport analysis written the same day,
`docs/rfc/nats-vs-ehdb-transport-boundary.md` (2026-07-15),
recommended **partial replacement: keep NATS** as the command bus, and
warned about push latency, redelivery and the autoscaler's lag signal.
The takeover plan decided to replace it anyway. The concerns it raised
are the ones the rest of this chapter covers: [13.2](ch13-02-append-log.md)
for latency, [10.3](ch10-03-bus-and-pools.md#when-a-worker-dies-mid-command)
for redelivery, and [10.4](ch10-04-slots-and-keda.md) for the lag signal.
```

Names in the worker's configuration such as `nats_filter_subject` and
the `NATS_FILTER_SUBJECT` fallback are leftovers from that period
(worker `src/config.rs:40-46`).

## Check your understanding

{{#quiz ../quizzes/ch13-01.toml}}
