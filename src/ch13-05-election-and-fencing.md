# Writer Election and Fencing

<span class="status status-partial">PARTIAL</span>

An EHDB shard must have **one writer**. If two processes both believe
they own the log, they can write conflicting histories. Two mechanisms
prevent it: an **election** decides who the writer is, and a **fence**
refuses writes from one that no longer is.

## The election

The writer holds a Kubernetes `Lease` named `ehdb-shard-<shard>`
(`ehdb-shard-00000000` for shard 0; ehdb v0.15.1
`crates/ehdb-reference/src/election.rs:169`).

| Setting | Default | Variable |
|---|---|---|
| enabled | off | `NOETL_EHDB_ELECTION` |
| lease duration | 15 s | `NOETL_EHDB_ELECTION_LEASE_SECS` |
| renew interval | 5 s ("three missed renewals lose the lease") | `NOETL_EHDB_ELECTION_RENEW_SECS` |

(ehdb `election.rs:53-55`; the switch is read by worker v6.15.0
`src/ehdb/lease_store.rs:162-166`.) The holder identity is the pod's hostname plus a
random id, so a restarted pod is a new candidate and waits out the old
lease: failover takes about **lease + renew + 1 = 21 s** (worker
v6.15.0 `src/ehdb/election.rs:38-51`). The **epoch** is the lease's
transition count.

On prod, the record for 2026-10-10 says "C2+C3 (election + fencing)
remain HELD" (ai-meta wiki Home). By 2026-11-04 the election was
running: the lease was held at **epoch 29** (Home, "Verified state",
from the writer's `/metrics`), and a writer restart on 2026-11-06 moved
it to 30 (Sessions-Log, 2026-11-06).

## The fence

`EpochFence` (ehdb v0.15.1 `crates/ehdb-core/src/fence.rs`) has three
modes: `off`, `shadow` (count what it would refuse) and `enforce`
(refuse a durable mutation whose epoch is lower than the highest one
accepted). The switch is `NOETL_EHDB_FENCING`, **default off**, and
without a running election the fence is inert.

```admonish partial title="What is not known publicly: the fence's prod mode"
No dated public record states which mode the fence runs in on prod.
What the code records, in worker v6.15.0 `src/worker.rs:133-147`: the
election once acquired its lease **+332 s** after the writer started,
behind two engine opens. Under `enforce` that would have refused every
durable write for about 5.5 minutes per restart, on the one process
hosting both buses, "and it is why enforce was not armed". The
election's start was moved ahead of the bus hosts to fix that. This
book does not claim a mode until a dated record does.
```

## Why the order of start-up mattered

The incident is a general lesson about fences: a fence makes a
**late** election into an **outage**. The failover window you publish
(21 s here) holds only if the election runs first; anything that
delays it widens the window for every restart.

## Check your understanding

{{#quiz ../quizzes/ch13-05.toml}}
