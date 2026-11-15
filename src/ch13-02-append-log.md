# The Append Log: Parts, Segments, Manifest

<span class="status status-real">REAL</span>

EHDB stores records in an **append-only log**. Nothing is updated in
place: a record is written once, and the only deletion is retention
dropping whole old files. All facts here are ehdb **v0.15.1**,
`crates/ehdb-l0`.

## Parts

Appends go to the **active part**, a local file. When it is full it is
**sealed**: closed, made immutable as an `.eslog` part, and uploaded
asynchronously to the storage substrate (`src/lib.rs:36-41`,
`src/part.rs:1-19`). A part seals when any of these is reached
(`part.rs:530-536`):

| Trigger | Default |
|---|---|
| size | 8 MiB (`DEFAULT_SEAL_MAX_BYTES`, `src/engine.rs:67`) |
| record count | 1024 (`DEFAULT_SEAL_MAX_RECORDS`, `engine.rs:65`) |
| age | off unless configured (`NOETL_EHDB_SEAL_MAX_AGE_SECS` on the server, `NOETL_EHDB_SEAL_MAX_AGE_MS` on the worker) |

The records in the active part are the **unsealed tail**. They live on
the local disk only until the part seals
([13.6](ch13-06-durability.md)).

"Segments" is the older name: the L0 part frame is byte-identical to
the earlier durable-segment format (`lib.rs:52-55`).

## The manifest

The **manifest** is a versioned list of the sealed parts (`PartMeta`
rows) plus `reclaimed_through`, the point below which retention has
dropped data (`src/catalog.rs:251-267`). The engine keeps the 32 most
recent manifest versions (`engine.rs:80`).

## When a write is durable

`FlushPolicy` (`part.rs:33-50`) has three postures:

| Posture | What it does | Used for |
|---|---|---|
| `EveryAppend` | `fsync` after every append; durable before the append returns | the default for the source-of-truth event log |
| group commit | appends do not `fsync` alone; the caller syncs a batch, and must do so before acknowledging any record in it | the bus writers: N records that arrive together share one `fsync` (ai-meta#205) |
| `Buffered` | `fsync` every N records | derived or metrics tiers only |

Group commit does not widen the crash window: a record is still
durable before its writer confirms it. It changes the cost.

## Reads

A read merges the active part (held in memory, so a writer can read
its own writes), the local sealed parts and any replica parts, and uses
the manifest to skip parts that cannot hold what was asked for
(`lib.rs:40`). Skipping by key is what the bloom filters are for
([13.3](ch13-03-bloom-and-floor.md)).

## Check your understanding

{{#quiz ../quizzes/ch13-02.toml}}
