# Durability: Tail Replication and the Unsealed Tail

<span class="status status-partial">PARTIAL</span>

How much can EHDB lose? The answer depends on which records you ask
about: sealed ones or the unsealed tail ([13.2](ch13-02-append-log.md)).

## Sealed parts

A sealed part is immutable, so copying it needs no consensus: EHDB
writes it once to each of N places (ehdb v0.15.1
`crates/ehdb-l0/src/lib.rs:80-94`). For the **server's** event-log
store, an off-box object-storage replica was armed on prod on
2026-10-10 (Sessions-Log, "the off-box replica was armed").

## The unsealed tail

The active part exists only on the local disk until it seals. A lost
disk loses it. **Tail replication** ("B3") copies the tail off the node
on a timer, so a loss is bounded by the tick rather than by the part
size (`crates/ehdb-l0/src/engine.rs:110-128`):

| Setting | Default | Variable |
|---|---|---|
| tail replication | off | `NOETL_EHDB_TAIL_REPLICATION` |
| tick | 15 s | |
| clean up replicated tail objects (`false` keeps them all) | on | `NOETL_EHDB_TAIL_CLEANUP` |

The project's own framing of what the server store's replicas buy is
a "bounded-loss consistent prefix of sealed history, not 'no data
loss'" (ai-meta wiki Home, the #460 block).

Tail replication is in the **server's** embedded store only (server v3.161.2
`src/handlers/ehdb_embedded.rs:1015-1033`), and was live on prod with a
60 s tick from 2026-10-10 (Sessions-Log, "B3+D2 live on prod"). It
bounds the loss; it does not make writes synchronously durable.

## The bus stores

```admonish partial title="The buses are single-copy"
The command and event buses on the `cmdbus-writer` use the local
filesystem substrate only (worker v6.15.0 `src/command_bus.rs:286`);
the worker has no object-storage substrate. Their sealed parts **and**
their tail sit on one volume. Treat the bus as durable against a
process restart, not against losing its disk.
```

## Check your understanding

{{#quiz ../quizzes/ch13-06.toml}}
