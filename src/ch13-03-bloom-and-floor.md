# Bloom Filters and the Prune Floor

<span class="status status-real">REAL</span>

## Blooms: skipping parts

Each sealed part carries **bloom filters** over `execution_id`, per
part and per granule inside it (ehdb v0.15.1 `crates/ehdb-l0/src/bloom.rs:1-13`).
A read for one execution asks each part's bloom first: "definitely
not here" skips the part, "maybe here" reads it. A bloom can say
*maybe* for an execution that is not there (a **false positive**), but
never *no* for one that is.

## The prune floor

Retention deletes old parts, but it must not delete events an
execution still needs. The **floor** is the lowest sequence that must
be kept: the minimum over every execution not yet safe to prune, such
as one still running or not yet archived (server v3.161.2
`src/services/event_archive.rs:246, 863-875`). Everything below the
floor can go.

The floor is found with the blooms: a part whose bloom says *maybe*
for a live execution is treated as holding it. So a **false positive
on an old part pins the floor** there, and nothing above it can be
pruned, though no live data is in it.

Two fixes, both recorded in the public log:

| Fix | Switch | Default | On prod |
|---|---|---|---|
| **floor-exact**: confirm the floor holder with an exact read before trusting a bloom | `NOETL_EHDB_FLOOR_EXACT` (server) | off (`event_archive.rs:2059, 2428-2440`) | armed 2026-11-04 (Sessions-Log, "2026-11-04 (evening) — #517 floor-exact armed on prod") |
| **bloom scheme 2**: the legacy probes `(h1 + i·h2) mod m` could collapse onto few bits; scheme 2 derives each probe independently with SplitMix64 | `EHDB_BLOOM_SCHEME` (`1` or unset = legacy, `2` = new; any other value reads as legacy) | legacy (`bloom.rs:19-58`) | readers first (ehdb v0.15.0, 2026-11-06), then armed on the server and the `cmdbus-writer` 2026-11-07 (Sessions-Log, "Release B") |

```admonish warning title="Readers before writers"
Scheme 2 filters cannot be read by an older reader. That is why the
rollout put the reader (v0.15.0) everywhere first and armed the writer
a day later, and why an unrecognised value of `EHDB_BLOOM_SCHEME`
falls back to legacy: "a typo must never write a filter an older
reader cannot open" (`bloom.rs:54-58`).
```

## Check your understanding

{{#quiz ../quizzes/ch13-03.toml}}
