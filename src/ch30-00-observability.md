# Observability and Alerting

<span class="status status-real">REAL</span>

When a playbook misbehaves on the distributed runtime, three questions
come up in turn. What happened to *this* run? Is the platform healthy?
And would anyone have been told if it were not? This chapter answers
each with what NoETL ships.

Code facts are server **v3.161.2**, worker **v6.15.0**, gateway
**v3.22.1** and CLI **v6.4.1**. Alerting facts are the `noetl/ops`
repository at commit **`3f63656`** (2026-11-02) plus the dated public
record, each with its date.

## One run: the execution id is the trace key

Every execution gets an `execution_id` from a snowflake generator in
the server, before any I/O (`src/handlers/execute.rs:366-371`). Its
events, its commands and its child executions are all keyed by it.
So the trace of one run is its **event log**, read by that id:

| Read | What you get |
|---|---|
| `noetl status <execution_id>` (add `--json` for everything) | the status summary; falls back to the event log if the server has no cached state (CLI `src/lib.rs:5726-5910`) |
| `GET /api/executions/{execution_id}` | the execution with its events: type, step (`node_name`), status, time, result, error (server `src/services/execution.rs:28-50`) |
| `GET /api/executions/{execution_id}/status` | status only |

Status is worked out from the events (`determine_status`), not read
from a stored column. [Chapter 10](ch10-00-distributed-runtime.md)
lists the events a one-step run writes.

```admonish myth
"NoETL exports distributed traces." Not at these releases. Server,
worker and gateway use `tracing` for logs and have **no OpenTelemetry
dependency** (their `Cargo.toml` files), so no spans leave the
process. What exists is a join point: a caller may pass a W3C `trace`
object (`traceparent`, `tracestate`, `baggage`) to `POST /api/execute`.
The server stores it on `playbook_started` and passes it to the
execution's commands and to child executions that do not bring their
own (`src/handlers/execute.rs:50-56`, `476-483`). The code calls
`execution_id` "the primary NoETL trace key" and the W3C object "the
external join".
```

Inheritance is best effort. If the parent's state is no longer hot,
the child starts a fresh trace segment rather than scan the event log
(`execute.rs:1036-1056`).

## The platform: three metric surfaces

Each service serves Prometheus text at `/metrics`:

| Service | Where | Unauthenticated? | Off switch |
|---|---|---|---|
| server | its HTTP port, `/metrics` | yes, with the health routes (`src/main.rs:90-104`) | `NOETL_DISABLE_METRICS` (default `false`; the server reads `NOETL_`-prefixed variables, `src/config/app.rs:1086-1088`) |
| worker | `WORKER_METRICS_BIND`, default `0.0.0.0:9090` (`src/config.rs:124-134`), next to `/healthz` and `/readyz` | yes (`src/metrics_server.rs:59-62`) | none |
| gateway | `/metrics` (`src/main.rs:435-437`) | yes, merged outside the auth layer (`src/main.rs:508-520`) | none |

The `cmdbus-writer` runs the worker binary, so it serves the worker
surface too, plus the bus-lag face the autoscaler reads
([10.4](ch10-04-slots-and-keda.md#autoscaling-on-bus-lag)).

```admonish warning title="execution_id is never a metric label"
A label value per run would grow the metric registry without bound.
So metrics answer "how many, how slow, how far behind", and the event
log answers "which run". To go from a bad number to a run, find the
time window in the metric, then list executions in that window.
```

A few series the alerts below read, each found in code at these
releases:

| Series | Served by | Tells you |
|---|---|---|
| `noetl_ehdb_command_publish_failed_total{reason}` | server (`src/metrics.rs:703`) | commands that did not reach the bus |
| `noetl_worker_claim_failed_total`, `noetl_worker_claim_succeeded_total` | worker (`src/metrics.rs:1147-1156`) | whether a pool is claiming work |
| `noetl_worker_materializer_skipped_total` | worker (`src/metrics.rs:1138`) | events the materializer dropped |
| `noetl_gateway_auth_bypass_enabled{mode}` | gateway (`src/ingress/mod.rs:332-360`) | 1 if `GATEWAY_AUTH_BYPASS` accepts every token |

The last one shows a design rule worth copying. It is present at `0`
on a healthy gateway, not absent. "Authentication is on" and "I cannot
tell" must not look the same. Before the gauge, the only signal was a
warning logged on every request.

## Would anyone be told? Alert policies as code

Paging rules live in `noetl/ops` as
[`ci/monitoring/alertpolicies.json`](https://github.com/noetl/ops/blob/main/ci/monitoring/alertpolicies.json):
**26 policies** at `3f63656`, each a PromQL query with a `duration`
(how long it must hold before paging). They cover the bus, claims, the
materializer, the gateway's auth gauge, the EHDB mirror and parity
checks, and volume space and inodes.

`ci/monitoring/apply-alertpolicies.sh` applies them. It matches on
display name, updates what exists, creates what does not, and **never
deletes**: a policy dropped from the file stays live and is reported,
because silently removing a paging rule is worse than leaving a stale
one. `--dry-run` shows what would change.

### Two paths, one delivers

The repository also holds Prometheus `Rules` objects
(`ci/manifests/noetl/gmp/rules-*.yaml`). They look like alerting and
they evaluate. But per the repository's own README, the managed
Alertmanager they feed has **no receiver configured**, so their alerts
reach nobody. Only the Cloud Monitoring policies page. The README calls
the `Rules` files "documentation and kind-parity".

```admonish myth
"A policy attached to a notification channel will reach someone."
Attachment is not delivery. The API does not expose whether an email
channel is verified, and an unverified one accepts every setting and
delivers nothing. Delivery was proven on 2026-08-19 by firing a
temporary policy and receiving the mail (`ci/monitoring/README.md`).
After any channel change, repeat that test.
```

### What forces the file and the live policies to agree

Nothing yet. Applying is a **manual** step. The repository's CI
(`.github/workflows/validate.yml`, added 2026-10-03) checks that files
parse; it does not compare them with what is live. That gap is
[ai-meta#471](https://github.com/noetl/ai-meta/issues/471), open:

- On 2026-10-15 the file and live had drifted **in both directions**:
  three committed policies were never applied, one live policy was in
  no file, and one live policy had a `0s` duration where the file
  intended 1800 s.
- That `0s` came from the apply script: a policy with **no `duration`
  key** is applied as `0s` (`pol.get('duration', '0s')`), so a stable
  count paged at once and kept paging. Every policy at `3f63656` now
  sets `duration` explicitly.
- On 2026-10-16 it was reconciled: **23 committed, 23 live**, none
  mismatched, none without a channel.

The file has grown to 26 since. Whether the three newer policies are
live is not in a dated public record. This book does not read the
project, so it does not say.

## Scrape coverage is a risk

An alert on a metric nobody scrapes never fires, and nothing reports
the silence. On the production cluster a `PodMonitoring` object names
the pods to scrape; pod annotations are ignored. Two selector defects
were fixed in `noetl/ops` `ceb49bc` on **2026-10-04**:

- The server's monitor selected the **Deployment's** label, but that
  Deployment had been at 0 replicas since the serving pod moved to a
  StatefulSet. The pod that served was scraped by nothing for **25
  days**.
- The workers' monitor listed four app names. Two matched nothing, and
  two pods of a newer system pool were not on the list.

Both now select by a label that every intended pod carries
(`component: server`; `worker-pool` must exist) rather than by a list
of names (`ci/manifests/noetl/gmp/podmonitoring-noetl.yaml`).

```admonish tip title="Check coverage, not configuration"
A selector that lists workloads is a copy of the workload set, and
nothing makes it follow when a workload is replaced. Select on a label
the workloads must have. Then check that every service's
`*_build_info` series is present (`noetl_server_build_info`,
`noetl_worker_build_info`, `noetl_gateway_build_info`): a missing
`build_info` means nothing scrapes that pod, which is different from a
counter that never moved.
```

## Check your understanding

{{#quiz ../quizzes/ch30-00.toml}}
