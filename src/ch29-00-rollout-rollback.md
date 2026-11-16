# Rollout and Rollback Discipline

<span class="status status-real">REAL</span>

[Chapter 27](ch27-03-deploy-by-digest.md) covered how one workload's
image is changed. This chapter covers the order: what to check, in what
sequence, and when to undo. Every rule here was written after something
went wrong. Each is stated with the dated record that taught it.

Sources: ai-meta `playbooks/516-ehdb-426-rollout/` and
`playbooks/517-floor-exact/` at **`0e835fd`** (procedures, and the
records of their execution), and the public issues and wiki
Sessions-Log entries cited. This book has run none of it.

## Smoke before and after every roll

A **smoke** is a short, fixed set of real executions that must pass.
The one production uses is "agreed with the owner 2026-11-04"
(516 README) and has three parts:

- seven credential-free fixture playbooks from the `noetl/e2e` suite
  (`scripts/prod_regression_validate.py --set smoke`: hello world,
  Python, arguments, variables, a loop, output selection, a large
  result), gate "7/7 COMPLETED";
- one turn of a real product playbook through the server API;
- one turn of another through the **live gateway as a guest**, so
  sign-in, the proxy and the result stream are exercised too.

The rule, in the script's own words: "Run before AND after every roll;
any FAIL => roll back" (`smoke.py`). *Before* matters as much as
*after*: a smoke that already fails cannot tell you the roll broke it.

```admonish tip title="Prove the smoke reached the right cluster"
`smoke.py` refuses to run unless it can read `noetl_server_build_info`,
and prints it. A port-forward that silently points at another cluster
would otherwise give a confident pass for the wrong system.
```

## One pool at a time

```admonish warning title="Rolling a system pool stalls every drive"
Measured on production on 2026-11-03: a fresh system-pool pod fails
every drive pass ("WAL chain incomplete") for about **7–10 minutes**
while it replays the event feed. It reports ready after about 8 s, so
readiness says nothing about it. The first roll that day restarted
both system pools together, stopped all executions, and was read as a
regression and rolled back. The fix was to roll them **one at a time**:
with one pool warm, smoke turns slowed to about 110–127 s instead of
stalling (ai-meta#504, closed 2026-11-03).
```

The order the 516 playbook records: server → smoke → user pool → smoke
→ system pool A → wait out the catch-up → smoke → system pool B →
smoke. "Never both system pools together." A smoke failure inside a
catch-up window counts against the window, not the release.

Workers drain on shutdown since **worker v6.11.3** (worker#390,
2026-11-03). On SIGTERM a worker stops claiming, lets in-flight
commands finish within `NOETL_WORKER_DRAIN_TIMEOUT_SECS` (default
150 s), then deregisters; the pool manifests' grace period went from 30
to 180 s to match. Before that, a roll dropped claimed commands and the
execution failed minutes later (ai-meta#511).

## Rollback is a recorded digest

Before each step, the playbooks record the digest each workload runs.
After it, a table: workload, new digest, rollback digest, smoke before
→ after. Rollback is the same image-only patch with the recorded
digest. Real cases from the public record:

| Date | What | Why |
|---|---|---|
| 2026-07-26 | bus cutover held at canary, rolled back | flipping would have stranded about half the shared commands (ai-meta#202) |
| 2026-07-27 | full bus flip rolled back; a third round succeeded the same day | ~10% of commands were never claimed (ai-meta#203) |
| 2026-09-30 | chain-store gates disarmed (an environment change, ~16 s) | the parity check read 772/0, then 13/839 an hour later (wiki Sessions-Log) |
| 2026-11-03 | system pools back to the previous worker | every drive stalled; the cause was rolling both at once (ai-meta#504) |

The lesson of 2026-09-30 is worth keeping: a check that passes on a lot
of traffic over a short time has not passed. Size a soak by duration,
not volume.

## Readers before writers

When a release changes a format that one component writes and others
read, order matters. Bloom scheme 2 (ehdb v0.15.0, ai-meta#517) went
out as two releases:

1. **Release A, 2026-11-06:** every reader learns the format; nothing
   writes it. Server, then each worker deployment, one at a time, then a
   soak of at least 24 h. Until B, rolling back below v0.15.0 is safe.
2. **Release B, 2026-11-07:** writers set `EHDB_BLOOM_SCHEME=2`, one
   store at a time. Rollback is to unset it.

```admonish warning title="The rollback floor moves"
After B, no reader may run below v0.15.0 while scheme-2 data exists. An
old reader does not refuse: on kind it fell back silently and rewrote
the manifest (517 README). So B waited for a reader that refuses
loudly (ehdb v0.15.1), and the rollback pins moved up with it. After a
format change, the old digest is no longer a safe rollback.
```

## Restart costs to plan for

| Restart | Cost | Source |
|---|---|---|
| `cmdbus-writer` | ~21 s failover (15 s lease), the cost of the election | 516 README, 2026-11-04 |
| `cmdbus-writer`, side effect | one gateway execution-owner record is lost; that turn completes but cannot be polled, so a smoke may fail once and pass on retry | ai-meta#523, open |
| system pool | ~7–10 min of no-op drives | ai-meta#504 |

## Check your understanding

{{#quiz ../quizzes/ch29-00.toml}}
