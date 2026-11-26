# ehgraph: A Graph Database for Topology

<span class="status status-partial">PARTIAL</span> <span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md) (Part IV).

ehgraph is the NoETL ecosystem's labeled-property graph database, for topology: what is connected to what. It runs standalone or embedded in the server, which embeds it at git `f200516` behind a default-off switch. It stores nothing in EHDB, and on production it is embedded and idle (dated record, 2026-11-22).

Planned sections:

- **15.1 Three Stores, Three Jobs** — [written](ch15-01-three-stores.md).
- **15.2 The Model: a Labeled Property Graph with History** (PARTIAL) — one label per node, typed properties, soft deactivation, graph versions; the per-namespace change log, sealed parts, snapshots and session graphs; one primary per topology domain.
- **15.3 Querying: openCypher, Query API v2 and Bolt** — [written](ch15-03-query.md).
- **15.4 Transactions** (PARTIAL) — multi-statement transactions (`graph.tx.*`, Bolt BEGIN/COMMIT, Query API `/tx`): snapshot reads with read-your-writes, one atomic serializable commit, conditional commits with `expect`.
- **15.5 ehgraph Inside the Server** (PARTIAL) — the embedded `noetl-cluster` graph under `/ehgraph/noetl-cluster` and its switches (all off by default); the single-writer declaration; the instance graph the registry writes; rollback safety across format versions; and that nothing reads it yet.
- **15.6 Operations: Backup, Compaction and Budgets** (PARTIAL) — backup to a filesystem prefix or GCS (put-if-absent, head last), crash-safe change-log compaction (off by default), memory budgets for embedded instances, and the metrics that show each.
- **15.7 Where It Is Heading: a Read Model for Runtime Topology** (TARGET) — the designs that fold ehgraph in as a read model, never authoritative: runtime topology for the interstate bus (RFC #586), cell topology (the Firecracker cells RFC), peer catalog nodes (the distributed catalog RFC); read replicas (Stage 1, not built).
