# EHDB: The Event Horizon Database

<span class="status status-real">REAL</span>

**EHDB** is NoETL's own storage engine: an append-only log built for
the event log and the command bus. It replaced NATS as the transport
between the server and the workers, and it is the substrate the
platform is moving its state onto ([Chapter 14](ch14-00-ehdb-state-substrate.md)).

This chapter describes **ehdb v0.15.1**, the version server v3.161.2
and worker v6.15.0 both pin (their `Cargo.lock` files name the tag).
Code facts are from that tag. Facts about production come only from
the dated public record in the
[ai-meta wiki](https://github.com/noetl/ai-meta/wiki) (the Sessions-Log
and Home pages) and its issues, and each carries its date.

## Where EHDB sits

| Store | Runs in | Holds |
|---|---|---|
| command bus | the `cmdbus-writer` (worker binary, host mode) | every command, per pool and shard ([10.3](ch10-03-bus-and-pools.md)) |
| event bus | the same process, its own engine | every `noetl.event` on its way to the materializers and the gateway |
| embedded event-log tier | the server | the server's own EHDB store, with retention and archive |
| chain store | the server | each execution's events linked by `prev_event_id` ([13.7](ch13-07-chain-store.md)) |

## Sections

- [13.1 Why NATS was replaced](ch13-01-why-replace-nats.md)
- [13.2 The append log](ch13-02-append-log.md): parts, sealing, the manifest
- [13.3 Bloom filters and the prune floor](ch13-03-bloom-and-floor.md)
- [13.4 Two buses](ch13-04-two-buses.md)
- [13.5 Writer election and fencing](ch13-05-election-and-fencing.md)
- [13.6 Durability](ch13-06-durability.md) <span class="status status-partial">PARTIAL</span>
- [13.7 The chain store](ch13-07-chain-store.md) <span class="status status-partial">PARTIAL</span>

```admonish note title="The docs and the code disagree in places"
Some of ehdb's own documents at v0.15.1 describe an older state than
its code. For example, `docs/spec/durability-window.md` says there is
no age-based seal trigger, but `crates/ehdb-l0/src/part.rs:530-536`
seals on age. This chapter follows the code and says where it does.
```

```admonish note title="EHDB's sibling store"
ehgraph, the graph database for topology, shares EHDB's change-log design but none of its code or
data. [15.1](ch15-01-three-stores.md) sets out which of Postgres, EHDB and ehgraph is authoritative
for what.
```

## Check your understanding

{{#quiz ../quizzes/ch13-00.toml}}
