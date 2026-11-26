# Querying: openCypher, Query API v2 and Bolt

<span class="status status-partial">PARTIAL</span>

ehgraph speaks a practical subset of **openCypher**, the query language
of Neo4j, Memgraph and others. This section says what the subset
covers, where it stops, and how well it matches the language's own test
suite. Everything here is ehgraph at git **`f200516`** (2026-11-10), the
commit server v3.161.2 embeds. The page is PARTIAL for two reasons:
ehgraph has no release tag yet, and the server embeds it behind
`NOETL_EHGRAPH_EMBEDDED`, off by default ([15.1](ch15-01-three-stores.md)).

## Four ways in, one store

| Interface | Where | Notes |
|---|---|---|
| MCP tool `graph.cypher` | `POST /mcp`, `tools/call` | what a `kind: mcp` playbook step uses |
| HTTP | `POST /v1/cypher` | the same body and result envelope |
| Neo4j Query API v2 shape | `POST /db/{namespace}/query/v2`, transactions under `…/query/v2/tx` | the plain-JSON shape Neo4j's own HTTP API uses |
| Bolt 5.0, falling back to 4.4 | `[bolt] listen = "…"` in the standalone server's config | official Neo4j drivers over `bolt://`; **off unless configured** (`crates/ehgraph-server/src/lib.rs:20-22`) |

(`docs/wiki/Cypher.md`.) The older fixed tools (`graph.upsert`,
`graph.query`, `graph.neighbors`, `graph.path`, …) remain the stable
contract. Cypher is an extra interface over the same store.

```admonish warning title="Bolt is not on the embedded graph"
The server's embedded instance serves the HTTP and MCP routes under
`/ehgraph/noetl-cluster` (server `src/ehgraph_embedded.rs:90`) and
does **not** open a Bolt listener: there is no Bolt code in the server
at v3.161.2. Bolt exists in the standalone `ehgraph` server, and the
listener has no TLS yet (TARGET), so the docs advise loopback or a TLS
proxy in front.
```

## What the subset covers

Reads and writes, both:

- **Matching**: `MATCH`, `OPTIONAL MATCH`, `WHERE`, multiple patterns,
  relationship direction and type alternatives, named paths,
  `shortestPath` and `allShortestPaths`.
- **Variable-length paths**: `*`, `*m..n` and the other forms, with
  trail semantics and an upper bound capped at **16 hops**
  (`max_hops: 16`, `crates/ehgraph-cypher/src/exec.rs:41`).
- **Shaping**: `WITH`, `UNWIND`, `RETURN` with `DISTINCT`, `ORDER BY`,
  `SKIP`, `LIMIT`; aggregation; `UNION`; `CASE`; list comprehensions;
  pattern predicates and comprehensions; `EXISTS { pattern }`.
- **Writes**: `CREATE`, `MERGE` (with `ON CREATE SET` and `ON MATCH SET`),
  `SET`, `REMOVE n.k`, `DELETE`, `DETACH DELETE`.
- **Transactions**: several statements committed atomically as one
  graph version, serializable and optimistic (first committer wins),
  with conditional commits (section 15.4).

A typical topology question:

```cypher
MATCH p = shortestPath((a:AccessPoint)-[*..8]->(:Internet))
RETURN a.name, [n IN nodes(p) | n.name] AS via
```

## Where it differs from Neo4j

These are not bugs to work around. They follow from ehgraph's model.

- **One label per node.** A node's label *is* its type, and it has
  exactly one (`exec.rs:1639`). Multiple labels, label expressions
  (`:A&B`) and `REMOVE n:Label` are refused. So is a node with **no**
  label (`CREATE ()`).
- **`DELETE` deactivates.** Deleted elements are soft-deactivated, and
  their history and versions are kept (`exec.rs:80-81`). `MATCH` sees
  active elements unless the request asks for inactive ones.
- **`id` is the element id, not a property.** `id(n)` returns
  ehgraph's string id, not Neo4j's integer.
- **Idempotent writes report idempotently.** `MERGE … SET` with
  unchanged values writes nothing and creates no new version, and
  `properties_set` counts only real changes.

Not supported at `f200516`: `CALL` procedures and subqueries,
`COUNT { }`, `FOREACH`, `LOAD CSV`, regular expressions (`=~`),
temporal and spatial types, `reduce()`, schema DDL (`CREATE INDEX`), and
`neo4j://` routing. GQL-only syntax is on the roadmap, not in the
subset.

## How well it matches the standard

ehgraph runs the openCypher **TCK** (the language's conformance suite),
release **2024.3**, on 2026-11-10. The scenario-level results are in
`docs/wiki/tck-results.json`. The book recounted them from that file:

| Scenarios | Pass | Fail | Out of model | Pass rate, all | Pass rate, in-model |
|---:|---:|---:|---:|---:|---:|
| 3,896 | **2,292** | 434 | 1,170 | 58.8% | **84.1%** |

"Out of model" scenarios use features ehgraph does not have by design.
By the recorded reasons, 1,069 of the 1,170 involve temporal or spatial
types, 52 `CALL` procedures and 44 multiple labels per node.
"In-model" is pass ÷ (pass + fail).

**The largest single gap is unlabeled nodes.** Of the 434 failures,
**391** come from scenarios that create a node with no label in their
setup or query. The book counted the failure reasons in the JSON to
check that figure. Without them the in-model rate would be 98.2%.
ehgraph deliberately counts them as failures: an unlabeled node is a
gap in the model, not a reason to drop the test. Whether unlabeled nodes
get a mapping is an open roadmap item.

```admonish tip title="Reading a conformance number"
"84% of the TCK" without its denominator overstates this result.
Quote the release (2024.3), the date, both rates, and that most of the
remaining failures share one cause. Re-run it (`scripts/tck.sh`) before
quoting a newer number.
```

## Check your understanding

{{#quiz ../quizzes/ch15-03.toml}}
