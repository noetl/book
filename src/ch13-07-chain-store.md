# The Chain Store

<span class="status status-partial">PARTIAL</span>

Reading one execution's history from a log ordered by time means
scanning everything around it. The **chain store** links each
execution's events by `(execution_id, prev_event_id)`, so its history
can be read by following links (ehdb v0.15.1
`crates/ehdb-l0/src/chain.rs:1-40`).

## Three gates

The server reads from the chain only when **all three** are set
(server v3.161.2 `src/db/queries/event_chain.rs:218-262`):

| Gate | Off when |
|---|---|
| `NOETL_CHAIN_POPULATE` | unset (an allow-list: `1`, `true`, `yes`, `on`) |
| `NOETL_CHAIN_ADVANCE` | unset (same) |
| `NOETL_CHAIN_SOURCE=chain` | any other value, or unset |

All three are **off by default**, so the chain store serves nothing
unless a deployment arms them. Without the populator, the source
resolves to off.

## On prod: serving, after three attempts

| Date | Event | Record |
|---|---|---|
| 2026-09-28 | the populator proven; a problem found: after a restart, a running execution's next event got `prev = NULL`, and the store could not tell that pseudo-root from a genuine first event | Sessions-Log, 2026-09-28 |
| 2026-09-29 | both halves of the root problem fixed (a coverage record plus head hydration) | Sessions-Log, "the chain-store root problem, both halves" |
| 2026-09-30 | ramp **rolled back**: a third mechanism, events chained in the wrong order (ai-meta#362, fixed by ordering the chain by links in ehdb v0.4.5) | Sessions-Log, "the chain store ramp is ROLLED BACK" |
| 2026-10-06 | gates disarmed at 18:36Z and **re-armed** at 19:23Z on evidence | Sessions-Log, 2026-10-06 (evening) |
| 2026-10-09 | "all three chain gates still armed" | Sessions-Log, 2026-10-09 (deploy) |

That is the latest dated statement this book found.

```admonish partial title="What is still open"
The comparator that checks the chain against the log reports **false**
divergence when its log snapshot is behind the store: staleness read as
conflict (ai-meta#360, open). The chain store serves; the instrument
that would show it agrees with the log is not yet trustworthy.
```

## The general lesson

The root problem is worth remembering beyond EHDB: a store that marks
"the first event" by an absent link cannot tell a real beginning from
a gap. A restart creates exactly that gap. Whatever marks a beginning
must be written, not inferred from something missing.

## Check your understanding

{{#quiz ../quizzes/ch13-07.toml}}
