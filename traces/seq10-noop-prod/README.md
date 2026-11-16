# Trace: `bench/seq10_noop` on prod (2026-11-16)

One captured execution, for T-05 ([#7](https://github.com/noetl/book/issues/7)) and Ch. 10.5.
`events.json` is a JSON array of `noetl_orchestrate_core::event::Event`, in event order
(the input `tools/trace-fold` expects).

## Where, when, which releases

| | |
|---|---|
| Stack | NoETL prod (GKE), through the gateway, `--runtime distributed` |
| Playbook | `bench/seq10_noop` v1: 12 sequential `noop` steps (`start`, `s01`–`s10`, `end`), no inputs, no credentials, no user data |
| Execution | `380575470791434240`, status `COMPLETED` |
| Run | 2026-11-16T04:31:02.995Z → 04:31:07.266Z (4.27 s), 74 events |
| Server | `noetl/server` **v3.163.1** (the only replica serving) |
| Worker (claimed every command) | `noetl/worker` **6.18.0** |
| Event/command bus writer | `noetl/worker` **6.11.9** |
| Gateway | `noetl/gateway` **v3.21.0** |

Image digests were mapped to these tags in the release registry on the day of the run.

## How it was captured

`GET /noetl/executions/{id}` on the gateway (= server `GET /api/executions/{id}`). Each event
row was mapped onto `Event` without changing any value: `created_at` → `timestamp` (the
field's own serde alias), plus `execution_id` and `catalog_id` from the same response's
header (the API puts them there once, not on each row).

## Scrub

One kind of internal identifier occurs: the worker pod name in the `result.context.worker_id`
of the 12 `command.claimed` events. It is replaced by `worker-1`. Nothing else matched
(hostnames, IPs, cluster DNS, emails, tokens, credentials). Event, execution, catalog and
command ids are engine values that enter the folded state, so they are kept.

Folding the unscrubbed and scrubbed logs with `tools/trace-fold` (orchestrate-core at
`tools/SERVER_SCHEMA_PIN`, v3.161.2) gives identical `canonical_state_digest`s at all 74
positions. The final state is `completed`, with all 12 steps completed.
Final digest: `bc150cfda0a18c3de085839d83aa483b9ff3cbf3c4bdc562473f271dbdafcb56`.

## ⚠ Known gap: `context`, `meta`, `attempt`

The execution API's event shape (`ExecutionEvent` in server v3.163.1) has no `context`,
`meta` or `attempt` columns, and `WorkflowState::apply_event` reads all three. This log
carries `result` in full but not those three fields, so its fold is the reducer's fold of
**this projection**. It is not proven identical to the drive's fold of the database rows.

For this playbook the difference is expected to be nil: no loops, no retries, and an empty
workload. That is an expectation, not a check. Capturing the full rows needs a read of the
event table or a server API that returns those columns. Until then this trace does not meet
T-05 AC1, and should not be cited as if it did.
