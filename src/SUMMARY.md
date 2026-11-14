# Summary

[The NoETL Book](title-page.md)
[Foreword](foreword.md)
[Introduction](ch00-00-introduction.md)
[How to Read This Book: Status Badges, Quizzes and Traces](ch00-01-how-to-read.md)

---

# Part I — Getting Started

- [Getting Started](ch01-00-getting-started.md)
    - [Installation](ch01-01-installation.md)
    - [Hello, Playbook](ch01-02-hello-playbook.md)
    - [Running It Locally with the CLI](ch01-03-running-locally.md)
- [Project: Fetch, Transform, Store — Your First Real Playbook](ch02-00-project-first-playbook.md)

# Part II — The Model

- [What NoETL Is](ch03-00-what-noetl-is.md)
    - [Declarative Orchestration](ch03-01-declarative-orchestration.md)
    - [Event Sourcing: The Log Is the Truth](ch03-02-event-sourcing.md)
    - [Ephemeral Blueprints and Stateless Workers](ch03-03-blueprints-and-workers.md)
    - [Two Catalogs: Internal Objects vs Business Data](ch03-04-two-catalogs.md)
- [Anatomy of a Playbook](ch04-00-anatomy-of-a-playbook.md)
    - [`apiVersion`, `kind`, `metadata`](ch04-01-header.md)
    - [`workload`, `vars` and Templating](ch04-02-workload-and-templating.md)
    - [`workflow`: Steps](ch04-03-steps.md)
    - [`keychain`: Credentials by Reference](ch04-04-keychain.md)
    - [`workbook`: Reusable Tasks](ch04-05-workbook.md)
- [Tools](ch05-00-tools.md)
    - [The Tool Kinds](ch05-01-tool-kinds.md)
    - [The Ordered Tool List: One Command, One Slot](ch05-02-ordered-tool-list.md)
    - [Results, References and Size Limits](ch05-03-results-and-references.md)
- [Control Flow](ch06-00-control-flow.md)
    - [`next`, Arcs and Routers](ch06-01-next-and-routers.md)
    - [`when` Guards](ch06-02-when-guards.md)
    - [`loop:` — Sequential, Parallel, Cursor](ch06-03-loop.md)
    - [Back-Edges: Loops as Goto](ch06-04-back-edges.md)
    - [Errors, Timeouts and Retries — What Is Enforced](ch06-05-errors-timeouts-retries.md)
- [Composition: Sub-Playbooks](ch07-00-sub-playbooks.md)
    - [`kind: playbook` and Child Executions](ch07-01-child-executions.md)
    - [What a Hop Costs](ch07-02-what-a-hop-costs.md)

# Part III — The Three Runtimes

- [The Local Runtime: `noetl run`](ch08-00-local-runtime.md)
    - [One Process, One Interpreter](ch08-01-in-process-interpreter.md)
    - [Local Tool Kinds and Their Limits](ch08-02-local-kinds.md)
    - [Iterating Without `loop:` — Arcs, SQL and Rhai](ch08-03-local-iteration.md)
    - [The Local Event Buffer and `noetl push`](ch08-04-event-buffer.md)
- [The Daemon: `noetl subscribe` and `noetl serve`](ch09-00-daemon.md)
    - [Subscriptions: NATS, Pub/Sub, Kafka](ch09-01-subscriptions.md)
    - [Spooling and the Event Trail](ch09-02-spool-and-trail.md)
    - [Dispatching to a Server](ch09-03-dispatch-to-server.md)
- [The Distributed Runtime](ch10-00-distributed-runtime.md)
    - [Gateway: The Gatekeeper](ch10-01-gateway.md)
    - [Server: The Orchestrate-Core Drive](ch10-02-server.md)
    - [The Command Bus and Worker Pools](ch10-03-bus-and-pools.md)
    - [Slots, Pools and KEDA Autoscaling](ch10-04-slots-and-keda.md)
    - [Following One Execution End to End](ch10-05-one-execution.md)
- [Choosing a Runtime](ch11-00-choosing-a-runtime.md)
- [Project: Taking Your Playbook Distributed](ch12-00-project-distributed.md)

# Part IV — EHDB: The Substrate

- [EHDB: The Event Horizon Database](ch13-00-ehdb.md)
    - [Why NATS Was Replaced](ch13-01-why-replace-nats.md)
    - [The Append Log: Parts, Segments, Manifest](ch13-02-append-log.md)
    - [Bloom Filters and the Prune Floor](ch13-03-bloom-and-floor.md)
    - [Two Buses: Commands and Events](ch13-04-two-buses.md)
    - [Writer Election and Fencing](ch13-05-election-and-fencing.md)
    - [Durability: Tail Replication and the Unsealed Tail](ch13-06-durability.md)
    - [The Chain Store](ch13-07-chain-store.md)
- [EHDB as the State Substrate](ch14-00-ehdb-state-substrate.md)
    - [Embedded State: One EHDB per Shard](ch14-01-embedded-state.md)
    - [The Execution-Partitioned Event Store (RFC #355)](ch14-02-partitioned-event-store.md)
    - [What Retiring Reconcile and Re-Drive Buys](ch14-03-retiring-reconcile.md)
- [ehgraph: A Graph Database for Topology](ch15-00-ehgraph.md)
    - [Model, Change Log, Snapshots](ch15-01-model.md)
    - [openCypher, Query API v2 and Bolt](ch15-02-query.md)
    - [ehgraph Inside the Server](ch15-03-embedded.md)

# Part V — Distribution: Catalog and Instances

- [The Distributed Playbook Catalog](ch16-00-distributed-catalog.md)
    - [Content Addressing and Digest Identity](ch16-01-content-addressing.md)
    - [Resolvers: `noetl://`, `s3://`, `gs://`, `db://`, `ehdb://`…](ch16-02-resolvers.md)
    - [Execution Pinning](ch16-03-pinning.md)
    - [Discovery with Bloom Adverts](ch16-04-discovery.md)
    - [Hot Reload](ch16-05-hot-reload.md)
    - [`kind: wasm`](ch16-06-kind-wasm.md)
- [Cross-Instance Execution: "Run It on B"](ch17-00-cross-instance.md)
    - [Instance Identity and the Registry](ch17-01-instance-registry.md)
    - [`remote: import` vs `remote: delegate`](ch17-02-import-vs-delegate.md)
    - [Pins Across Instances](ch17-03-pins-across-instances.md)

# Part VI — Interop and Concurrency

- [MCP and Agents](ch18-00-mcp-and-agents.md)
    - [`kind: mcp`: Calling MCP Servers](ch18-01-kind-mcp.md)
    - [`kind: agent`: Agent Steps](ch18-02-kind-agent.md)
    - [A Playbook as an MCP Server](ch18-03-playbook-as-mcp.md)
    - [A Playbook as an Agent](ch18-04-playbook-as-agent.md)
    - [The Interop Matrix Across Runtimes](ch18-05-interop-matrix.md)
- [Project: Expose a Playbook as an MCP Tool and Call It from an Agent](ch19-00-project-mcp-agent.md)
- [Coroutines and Structured Concurrency](ch20-00-coroutines.md)
    - [Concurrency Today: Fan-Out, Fan-In and Its Gaps](ch20-01-concurrency-today.md)
    - [Leaf Units and Ownership](ch20-02-leaf-units.md)
    - [`spawn`, `join`, `select`](ch20-03-spawn-join-select.md)
    - [Cancellation and Slots](ch20-04-cancellation.md)
    - [Flags and the Staged Rollout](ch20-05-flags-and-stages.md)

# Part VII — Resources and Performance

- [The Resource Model](ch21-00-resource-model.md)
    - [Labels: MEASURED, DEPLOYED, DEFAULT, GUIDANCE, TARGET](ch21-01-labels.md)
    - [Per-Step-Kind Costs](ch21-02-step-kind-costs.md)
    - [Limits: WASM Fuel, Agent Caps, Context Sizes](ch21-03-limits.md)
    - [The Slot and Pool Model](ch21-04-slot-model.md)
    - [Estimating a Playbook Before You Run It](ch21-05-estimating.md)
    - [What Is Not Yet Measured](ch21-06-not-yet-measured.md)
- [Orchestration Overhead](ch22-00-orchestration-overhead.md)
    - [Where a Step's Time Goes](ch22-01-where-time-goes.md)
    - [Postgres vs EHDB on the Hot Path](ch22-02-postgres-vs-ehdb.md)
    - [The Ranked Fixes](ch22-03-ranked-fixes.md)
    - [Measuring Honestly](ch22-04-measuring-honestly.md)
- [WASM at the Edge](ch23-00-wasm-at-the-edge.md)
    - [Purity: What Can Compile](ch23-01-purity.md)
    - [From Playbook to Module: The Compiler Stages](ch23-02-compiler-stages.md)
    - [A Playbook in a Cloudflare Worker](ch23-03-cloudflare-worker.md)
    - [Parity and Limits](ch23-04-parity-and-limits.md)
- [Project: Ship a Pure Playbook to the Edge](ch24-00-project-edge.md)

# Part VIII — Applied

- [Agent and Bot Fleets on NoETL](ch25-00-bot-fleets.md)
    - [The Shared-VM Baseline](ch25-01-shared-vm.md)
    - [Isolation and Scoped Credentials](ch25-02-isolation.md)
    - [Cost and Concurrency](ch25-03-cost-and-concurrency.md)
    - [The Architecture to Win](ch25-04-architecture.md)
- [Case Study: A Quantum-Readiness Orchestrator](ch26-00-quantum-readiness.md)
    - [A Pipeline of Sub-Playbooks on the Local Runtime](ch26-01-pipeline.md)
    - [Classifying a Crypto Surface](ch26-02-crypto-surface.md)
    - [Signed Self-Update and Rollback](ch26-03-self-update.md)

# Part IX — Operations

- [Deployment Modes](ch27-00-deployment.md)
    - [Local kind First](ch27-01-kind.md)
    - [Production on GKE](ch27-02-gke.md)
    - [Deploy by Digest](ch27-03-deploy-by-digest.md)
- [Releases and Version Pinning](ch28-00-releases.md)
- [Rollout and Rollback Discipline](ch29-00-rollout-rollback.md)
- [Observability and Alerting](ch30-00-observability.md)
- [Credentials and Secrets](ch31-00-credentials.md)
- [Representation Drift: Keeping What You Know True](ch32-00-representation-drift.md)

---

[Appendix A: DSL Reference](appendix-01-dsl-reference.md)
[Appendix B: Tool Kinds Reference](appendix-02-tool-kinds.md)
[Appendix C: Feature Flags and Environment Variables](appendix-03-flags.md)
[Appendix D: The Resource Model, Annotated](appendix-04-resource-model.md)
[Appendix E: Status Ledger — REAL vs TARGET by Chapter](appendix-05-status-ledger.md)
[Appendix F: Myths and Corrections](appendix-06-myths.md)
[Appendix G: Glossary](appendix-07-glossary.md)
[Appendix H: Contributing to This Book](appendix-08-contributing.md)
