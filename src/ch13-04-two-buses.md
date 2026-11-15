# Two Buses: Commands and Events

<span class="status status-real">REAL</span>

The `cmdbus-writer` ([10.3](ch10-03-bus-and-pools.md)) can host two
EHDB buses in one process, each with its **own engine**, directory and
`fsync` stream (worker v6.15.0 `src/event_bus.rs:1-33`).

| | Command bus | Event bus |
|---|---|---|
| Carries | commands, per pool and shard: `commands.<pool>.shard.<n>` | every `noetl.event` |
| Written by | the server, at each `command.issued` | the server, as it ingests events |
| Read by | workers, which compete for claims | three durable materializer groups (`noetl_materializer`, `noetl_result_materializer`, `noetl_state_materializer`) and the gateway's SSE feed |
| Switch | `NOETL_COMMAND_BUS_HOST` | `NOETL_EVENT_BUS_HOST` |
| Also hosts | the lag metric KEDA reads | the gateway's key-value store and the WAL fan-out the off-server state builder replays |

## Why two engines

Events run about **an order of magnitude hotter** than commands (the
worker's own note, `event_bus.rs`). The binding cost in an EHDB engine
is `fsync` under the engine lock (ai-meta#205), so sharing one engine
would put event volume in front of command dispatch. Separate engines
keep a burst of events from slowing the next claim.

## The event bus carries the source of truth

When the server publishes events instead of inserting them
(`NOETL_EVENT_INGEST_PUBLISH_ONLY=true`), the first materializer group
is the **only writer** of the durable `noetl.event` log
(`event_bus.rs`). The worker's documentation says the server runs that
way; with the code default (`false`) the server inserts directly
([10.1](ch10-01-gateway.md#how-results-get-back)).

## Check your understanding

{{#quiz ../quizzes/ch13-04.toml}}
