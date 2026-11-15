# Appendix G: Glossary

<span class="status status-real">REAL</span>

Each term links to the section that defines it. The glossary grows with
the book: every chapter that introduces a term adds it here in the same
pull request ([#50](https://github.com/noetl/book/issues/50)). Chapters
not written yet have not added their terms.

| Term | Meaning | Defined in |
|---|---|---|
| active part | The EHDB file being appended to; its records are the unsealed tail until it seals | [13.2](ch13-02-append-log.md) |
| arc | One outgoing transition in `next`, optionally guarded by `when` | [6.1](ch06-01-next-and-routers.md) |
| back-edge | An arc to a step that has already run; forms a loop bounded only by its `when` | [6.4](ch06-04-back-edges.md) |
| bloom filter | A per-part summary that can say a key is definitely absent (no false negatives) or maybe present | [13.3](ch13-03-bloom-and-floor.md) |
| blueprint | What a playbook is: control flow and policy, with no resident state between invocations | [3.3](ch03-03-blueprints-and-workers.md) |
| business data | Domain data in your own stores, touched only by playbook steps | [3.4](ch03-04-two-catalogs.md) |
| chain store | Each execution's events linked by `prev_event_id`, read by following links | [13.7](ch13-07-chain-store.md) |
| child execution | The separate execution a `kind: playbook` step starts, linked by `parent_execution_id` | [7.1](ch07-01-child-executions.md) |
| claim | A worker taking a command: the bus hands it out, and the server's claim endpoint (`command.claimed`) makes it exclusive | [10.3](ch10-03-bus-and-pools.md) |
| `cmdbus-writer` | The worker binary in host mode, run as a StatefulSet: it hosts the EHDB command bus (and usually the event bus) | [10.3](ch10-03-bus-and-pools.md) |
| command bus | The durable log of commands per pool and shard, with a claim coordinator; EHDB, not NATS | [10.3](ch10-03-bus-and-pools.md) |
| context | A named CLI configuration (`noetl context`) that can pin a runtime and server | [Ch. 8](ch08-00-local-runtime.md) |
| drive pass | One run of the orchestrator: playbook + folded state in, next commands out; by default a `__orchestrate__` command on the system pool | [10.2](ch10-02-server.md) |
| EHDB | NoETL's append-only storage engine; the command and event buses and the server's event-log tier | [Ch. 13](ch13-00-ehdb.md) |
| epoch fence | Refuses durable writes from a writer whose election epoch is stale (`off`, `shadow`, `enforce`) | [13.5](ch13-05-election-and-fencing.md) |
| event buffer | A local run's recorded events, `$NOETL_LOCAL_DIR/<id>/events.feather`; shipped with `noetl push` | [8.4](ch08-04-event-buffer.md) |
| event log | An execution's append-only record of everything that happened; state is folded from it | [3.2](ch03-02-event-sourcing.md) |
| exclusive / inclusive | Routing modes: first matching arc vs every matching arc (default exclusive) | [6.1](ch06-01-next-and-routers.md) |
| gated kind | A kind refused unless a server flag turns it on (`agent`, `mcp`) | [5.1](ch05-01-tool-kinds.md) |
| gateway | The client-facing gatekeeper: authenticates, authorizes, proxies to the server and streams results back | [10.1](ch10-01-gateway.md) |
| hop | One `kind: playbook` call; costs a whole child execution | [Ch. 7](ch07-02-what-a-hop-costs.md) |
| internal catalog | NoETL's own objects (playbooks, …) behind `/api/catalog/*` | [3.4](ch03-04-two-catalogs.md) |
| keychain alias | The name a playbook uses for a credential; resolved by the worker at run time | [4.4](ch04-04-keychain.md) |
| label | A sub-task's name in a tool list; later items read its result as `{{ <label>.field }}` | [5.2](ch05-02-ordered-tool-list.md) |
| local runtime | The CLI's in-process interpreter (`noetl run -r local`); a separate implementation from the server | [Ch. 8](ch08-00-local-runtime.md) |
| manifest | The versioned list of an EHDB store's sealed parts and its retention point | [13.2](ch13-02-append-log.md) |
| orchestration pass | The server's evaluation of arcs, triggered by a completion event | [Ch. 6](ch06-00-control-flow.md) |
| orchestrator | `orchestrate-core`'s engine: playbook + events in, next commands out; runs as WASM on a worker by default | [3.1](ch03-01-declarative-orchestration.md) |
| playbook | A YAML document (`kind: Playbook`, `apiVersion: noetl.io/v2`) describing a workflow of steps | [Ch. 4](ch04-00-anatomy-of-a-playbook.md) |
| policy rules | `spec.policy.rules` on a tool-list sub-task: continue, retry, jump, break, fail | [6.5](ch06-05-errors-timeouts-retries.md) |
| pool | A set of workers claiming one subject family, `commands.<pool>.>`; chosen per execution (`shared`, `system`, `subscription`) | [10.3](ch10-03-bus-and-pools.md) |
| prune floor | The lowest sequence retention must keep, set by the oldest execution not safe to prune | [13.3](ch13-03-bloom-and-floor.md) |
| resource model | `noetl.ai/dsl/resource-model.json`: NoETL's labelled, dated figures for time, slots, limits and fuel | [Ch. 21](ch21-00-resource-model.md) |
| resource-model label | MEASURED, DEPLOYED, DEFAULT, GUIDANCE, TARGET or NOT_YET_MEASURED: what kind of number a figure is | [21.1](ch21-01-labels.md) |
| result store | Where a step result above 100 KiB is spilled; the event then carries a reference | [5.3](ch05-03-results-and-references.md) |
| seal | Closing the active part into an immutable part (8 MiB, 1024 records, or an optional age) | [13.2](ch13-02-append-log.md) |
| `set:` | Server-side step mutations, persisted as a `ctx.updated` event | [4.2](ch04-02-workload-and-templating.md) |
| slot | A worker's unit of concurrency; a command holds one from claim until its tool returns | [Ch. 5](ch05-00-tools.md) |
| spool | Store-and-forward buffer (local_disk in the daemon) that keeps messages while the downstream is down | [9.2](ch09-02-spool-and-trail.md) |
| `start` | The step every server execution begins with; the validator requires it | [4.3](ch04-03-steps.md) |
| step | One named entry of `workflow`: runs one tool, then routes with `next` | [4.3](ch04-03-steps.md) |
| step run | One execution of a step; a step re-run by a back-edge counts once per run when estimating | [21.5](ch21-05-estimating.md) |
| `step.skipped` | The event recorded for a target not taken, or a step whose guard was false | [6.2](ch06-02-when-guards.md) |
| subscription | A `kind: Subscription` document: a message source plus the playbook to run per message | [9.1](ch09-01-subscriptions.md) |
| `task_sequence` | The single command a `tool:` list becomes; runs its sub-tasks in order on one worker | [5.2](ch05-02-ordered-tool-list.md) |
| template | A `{{ … }}` expression in a string; minijinja on the server, token substitution locally | [4.2](ch04-02-workload-and-templating.md) |
| tool / kind | What a step runs; `kind` names the tool (`http`, `python`, …) | [Ch. 5](ch05-00-tools.md) |
| unsealed tail | Records in the active part, on the local disk only until it seals | [13.6](ch13-06-durability.md) |
| workbook | Named, reusable tool definitions a step references with `kind: workbook` | [4.5](ch04-05-workbook.md) |
| workload | A playbook's inputs, read as `{{ workload.<key> }}`, overridable per run | [4.2](ch04-02-workload-and-templating.md) |

## Check your understanding

{{#quiz ../quizzes/appendix-g.toml}}
