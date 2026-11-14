# Spooling and the Event Trail

<span class="status status-real">REAL</span>

## The event trail

The daemon writes every event to a **JSONL file**: one JSON object per
line, `--events <path>` (default `./<name>-events.jsonl`). It emits the
same event envelope as the in-cluster runtime, so the file is a
replayable, event-sourced log of the daemon's life. These are the event
types from the two-tick run in [9.1](ch09-01-subscriptions.md), in
order:

```text
subscription.lifecycle         REGISTERED
subscription.lifecycle         ACTIVE
subscription.message.received  RECEIVED
playbook.started               STARTED
playbook.completed             COMPLETED
subscription.message.received  RECEIVED
playbook.started               STARTED
playbook.completed             COMPLETED
subscription.lifecycle         DRAINING
subscription.lifecycle         DEACTIVATED
```

Each playbook run has its own execution id. The subscription's
lifecycle events carry the subscription's id.

## The spool: store and forward

A subscription can declare a **spool**. When the downstream (the
target of dispatch) is unreachable, messages are written to disk and
replayed when it comes back. In local mode the only spool backend is
**`local_disk`** (`src/subscribe/spool.rs`, CLI v6.4.0). The engine
(circuit breaker, ordering, idempotency, dead-letter, retention) is
shared with the worker's spool runtime, from the tool library.

The loss-safety contract, as the source states it:

- the source's batch is already acknowledged when it is fetched, so a
  message in hand is no longer on the source;
- each message is therefore **written durably to the spool before
  anything else**;
- the spool drains only after an active probe confirms that the
  downstream is reachable again.

The circuit breaker's state is a JSON file next to the spool, so a
restart in the middle of an outage resumes in the right phase.
Spool and circuit events go into the same JSONL trail. The summary
line counts them: `spooled`, `replayed`, `pending_spooled`.

## Check your understanding

{{#quiz ../quizzes/ch09-02.toml}}
