# Subscriptions: NATS, Pub/Sub, Kafka

<span class="status status-real">REAL</span>

A subscription is its own YAML document, `kind: Subscription`. It names
a **source**, and a **dispatch** target: the playbook to run per
message. This one uses the `timer` source, so it needs nothing else
running:

```yaml
{{#include ../examples/ch09/timer/subscription.yaml}}
```

```yaml
{{#include ../examples/ch09/timer/playbook.yaml}}
```

```console
$ noetl subscribe examples/ch09/timer/subscription.yaml --events ./trail.jsonl --max-messages 2
…
✓ subscription stopped — received=2 dispatched=2 spooled=0 replayed=0 failed=0 pending_spooled=0
  event-sourced trail: ./trail.jsonl
```

That is the real summary line from a run on CLI v6.4.0. The book's CI
does not run daemons, so this example is checked against the schema
only.

## Sources

The source implementations live in the shared tool library
(`src/tools/source/`, tools v4.6.0), the same code a worker's
subscription runtime uses:

| `source:` | Messages come from |
|---|---|
| `nats` | a NATS JetStream pull consumer (`url`, `stream`, `consumer`, credentials) |
| `pubsub` | a Google Pub/Sub subscription |
| `kafka` | a Kafka topic |
| `timer` | a clock: one message every `every` (at least 100 ms), with `payload` merged into each |

`kafka` and `pubsub` are optional build features of the tool library
(`#[cfg(feature = …)]`). This book ran only the `timer` source, so
whether a given CLI build includes Kafka or Pub/Sub support is
something to check on your binary.

Source credentials come from explicit fields or from `auth: <alias>`
plus `--credential <file>`. In local mode an alias is resolved from
that file and never from a server.

## One run per message

For each message, the daemon builds an envelope and runs the target
playbook **in-process** with the envelope as its **workload**. The
fields chosen by `dispatch.payload_from` are merged to the top level,
so a message field `order_id` is read as `{{ workload.order_id }}`
(`src/subscribe/dispatch.rs`). The loop dispatches a message before it
polls for the next one, so runs do not overlap.

The `timer` source's rules (tools v4.6.0 `source/timer.rs`):

- one tick per poll, so a run that overruns the period produces one
  catch-up tick, never a burst;
- the next tick is due `every` after the previous one **fired**;
- ticks are not acknowledged or redelivered: a failed tick is not
  retried, and the next tick is the retry;
- each message carries `payload` plus `tick` (counting from 1),
  `scheduled_at` and `fired_at`.

Useful flags: `--once` (drain once and exit), `--max-messages N`,
`--playbook-dir`, `--events`, `--spool-dir`, `-v`.

## Check your understanding

{{#quiz ../quizzes/ch09-01.toml}}
