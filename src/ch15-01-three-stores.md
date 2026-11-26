# Three Stores, Three Jobs

<span class="status status-real">REAL</span>

A NoETL deployment has three stores of its own: Postgres, EHDB and
ehgraph. They are easy to confuse, because the same words get used
for each (log, snapshot, version). They hold different things, and
only one of them is the record. This section says which store does
which job, at server **v3.161.2**, which embeds ehgraph at git
**`f200516`**. Business data (your data) lives in none of them
([3.4](ch03-04-two-catalogs.md)).

## Who is authoritative for what

| Store | Holds | Authoritative? |
|---|---|---|
| **Postgres** | the event log (`noetl.event`), the catalog (`noetl.catalog`), credentials, commands | **yes: it is the system of record.** Every event is written with `INSERT INTO noetl.event` (`src/db/queries/event.rs:40`), and the catalog reads and writes Postgres by default ([3.4](ch03-04-two-catalogs.md)) |
| **EHDB** | the command bus and the event bus ([13.4](ch13-04-two-buses.md)); a mirror of the event log; the chain store | **not yet for state.** It carries every command and event in flight. The event log reaches it as a mirror of the Postgres row (`src/handlers/ehdb_eventlog_mirror.rs`), appended asynchronously on production per the dated record of 2026-11-22. Making it the authoritative state store is a design ([Chapter 14](ch14-00-ehdb-state-substrate.md), TARGET) |
| **ehgraph** | topology graphs: which instances exist, which pools they are in, which playbooks they can run, who knows whom | **never.** It is a *read model*: a picture projected from the instance registry. The design calls it "never authoritative" (ai-meta RFC `interstate-runtime-bus.md` §5) |

So the answer to "where is the truth about this execution?" is
Postgres today. The answer to "what is connected to what?" is meant to
be ehgraph. Neither EHDB nor ehgraph replaces Postgres at these
releases.

## ehgraph is not part of EHDB

The names suggest a family, and the designs share ideas: an
append-only change log of frames, sealed immutable parts, an age-based
seal. But ehgraph only borrows the *design*. Its README states that the
repository does not depend on EHDB and "never stores graph data in an
EHDB dataset" (`noetl/ehgraph` `f200516`, `README.md`), and its crates
do not link it. The server's own pin comment says the same: ehgraph
"does not link EHDB" (server v3.161.2 `Cargo.toml:248`).

The practical consequence is the one that matters in an incident. The
two stores fail, back up and restore independently. An EHDB problem
does not touch the graph, and a graph that refuses to open does not
stop the buses.

## Why a graph store at all

Topology questions are path questions. "Which instances can run this
playbook, and through which pool?" or "what did this instance hand work
to, and when?" are joins of unknown depth in a table, and one
`MATCH` in a graph. ehgraph keeps such graphs as a labeled property
graph, with history: deactivating a node keeps it, so "who knew whom,
and when" can still be answered after an instance is gone (server
`src/instances/graph.rs:19-22`).

It is deliberately small:

- **one writer per graph**, a single primary with no replicas yet;
- graphs assumed to fit in one node's memory, up to about 10⁶ elements;
- scale-out by adding instances per topology domain, not by splitting
  one graph (`docs/wiki/Roadmap.md`).

## Off by default, and idle where it is on

```admonish warning title="Built, embedded, and not yet used"
In server v3.161.2 the embedded graph is off unless
`NOETL_EHGRAPH_EMBEDDED=true`, and the topology writer needs
`NOETL_EHGRAPH_TOPOLOGY_WRITER=true` plus a token file with a write
grant (`src/ehgraph_embedded.rs:77`, `src/instances/graph.rs:28-33`).
Nothing in the server reads the graph. No server code calls
`graph.query`, `graph.neighbors`, `graph.path` or `graph.cypher`.

On production, the dated record of 2026-11-22 reads the graph as
**embedded, writer switched on, and idle**:
`noetl_instance_total{outcome="graph_written"}` was 0 since the server
pod started on 2026-11-19, and the backup loop had shipped no new
objects (ai-meta wiki Sessions-Log, 2026-11-22). A counter is a reading
over a window, here about three days. It says nothing was written in
that window, not that the writer cannot write.
```

Sections 15.2–15.6 cover what ehgraph supports today. 15.7 covers what
it is planned to become: the read model for runtime topology.

## Check your understanding

{{#quiz ../quizzes/ch15-01.toml}}
