# Two Catalogs: Internal Objects vs Business Data

<span class="status status-partial">PARTIAL</span>

NoETL deals with two kinds of stored information, and it keeps them
strictly apart.

| | The **internal** catalog | **Business** data |
|---|---|---|
| What | NoETL's own objects: playbooks, and other catalog kinds such as subscriptions | Your domain data: customers, orders, bookings, documents |
| Who reads it | the NoETL server, through `/api/catalog/*` | **playbook steps only**, through tools such as `postgres`, `http`, `mcp` |
| Where it lives | the server's store (see below) | wherever it belongs: your databases, APIs, buckets |

A playbook in the internal catalog is the program that reads the
business data. The two never mix: business data is not put into the
internal catalog or into NoETL's event store, and NoETL's own objects
are not read by steps from business stores. This is a project rule,
and the reason why data access happens inside steps
([3.3](ch03-03-blueprints-and-workers.md)). It is stated as owner
direction in the RFC
[`postgres-to-ehdb-internal-data.md`](https://github.com/noetl/ai-meta/blob/main/docs/rfc/postgres-to-ehdb-internal-data.md)
(2026-08-29, design only): NoETL's internal orchestration data belongs
in EHDB, and "only user/business result data should stay in Postgres".

## Where the internal catalog is stored today

This section is **PARTIAL** because the storage is in transition.
At **server v3.161.2** (checked in the code):

- `/api/catalog/*` reads and writes the Postgres table `noetl.catalog`
  (`src/db/queries/catalog.rs`). Every catalog read resolves from it
  by default.
- An EHDB **catalog log** exists, but only as a **shadow** dual-write:
  `NOETL_CATALOG_LOG=shadow` also records each registration in an EHDB
  store, and nothing reads it (`src/handlers/catalog_log.rs`).
- Serving catalog reads from EHDB is **staged**:
  `NOETL_CATALOG_READ_SOURCE` can be `postgres` (the default),
  `verify` (compare both, serve Postgres) or `tier` (serve EHDB). The
  code calls the cutover "a flag flip, and … an owner decision"
  (`src/handlers/catalog_read.rs`).

```admonish not-yet
The design target is an internal catalog stored in **EHDB only**
([Chapter 16](ch16-00-distributed-catalog.md),
[Part IV](ch13-00-ehdb.md)). At v3.161.2 that is built as a shadow and
a staged read path, not the default.
```

## Check your understanding

{{#quiz ../quizzes/ch03-04.toml}}
