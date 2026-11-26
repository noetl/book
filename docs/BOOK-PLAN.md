# The NoETL Book — Plan

**Status of this plan:** v1.1, 2026-11-13. The outline lives in
[`src/SUMMARY.md`](../src/SUMMARY.md). The per-chapter descriptions,
badges and phases are in [`docs/ROADMAP.md`](ROADMAP.md). How to
contribute (spec-kit, issues, wiki, AI agents) is in
[`CONTRIBUTING.md`](../CONTRIBUTING.md). This document explains why the
book is shaped the way it is and what each chapter must achieve. The book is an
**iterative** project: the plan, the outline and the status of every
chapter are expected to change as NoETL changes.

Contents:

1. [Purpose and audience](#1-purpose-and-audience)
2. [Pedagogy](#2-pedagogy)
3. [Keeping the book true: status discipline](#3-keeping-the-book-true-status-discipline)
4. [Interactive tooling](#4-interactive-tooling)
5. [Chapter-by-chapter plan](#5-chapter-by-chapter-plan)
6. [Authoring order](#6-authoring-order)
7. [Where the truth lives: source map](#7-where-the-truth-lives-source-map)
8. [Maintenance loop](#8-maintenance-loop)
9. [Open decisions](#9-open-decisions)

---

## 1. Purpose and audience

The NoETL Book is meant to be the **complete, rigorous** account of the
NoETL ecosystem, in the way *The Rust Programming Language* is for Rust.
It covers the playbook DSL, the three runtimes, EHDB, the catalog,
cross-instance execution, MCP/agent interop, concurrency, the
resource and performance model, edge execution, and operations.

Readers, in priority order:

1. **Playbook authors.** People who want to automate something. Parts
   I–III and the project chapters are written for them.
2. **Platform engineers.** People who run NoETL or extend it. Parts
   IV–VII and IX are written for them.
3. **Evaluators.** People deciding whether to adopt NoETL. Chapters 3,
   11, 21, 22 and 25 give them honest, labelled numbers.
4. **Agents.** LLM agents that author and plan playbooks. The book links
   to the machine-readable DSL knowledge base on noetl.ai
   (`/dsl/resource-model.json`, the DSL manifest and the schema). It
   never forks that material; it explains it.

Assumed background: comfort with YAML, a shell, basic SQL and HTTP.
Rust is *not* required except in the internals chapters, which say so.

## 2. Pedagogy

The model is the Rust Book's structure plus the research-driven
interactive layer that Brown University's Cognitive Engineering Lab
(Will Crichton, Shriram Krishnamurthi et al.) added in their
experimental edition (rust-book.cs.brown.edu). Seven principles:

### 2.1 Progressive concept building

Each chapter uses only concepts introduced earlier. The dependency
chain is explicit:

```
playbook ─► step ─► tool ─► arc/when ─► loop/back-edge ─► sub-playbook
   │                                                        │
   └──────► local runtime ─► daemon ─► distributed runtime ◄┘
                                        │
             event log ─► EHDB ─► state substrate ─► catalog/pinning
                                        │
             slots/pools ─► resource model ─► overhead ─► WASM fusion/edge
```

A chapter that needs a forward reference says so in a callout ("you
will see why in Chapter 13") rather than explaining it half-way.

### 2.2 Project chapters interleaved with concept chapters

Like the Rust Book's guessing game (ch. 2), `minigrep` (ch. 12) and the
web server (ch. 20), four project chapters consolidate what came before.
Together they form the **hands-on tutorial track**:

| Project | After | Builds | Runtime |
|---|---|---|---|
| Ch. 2 — Fetch, transform, store | Part I | An http → duckdb → file pipeline with one guarded back-edge | local |
| Ch. 12 — Taking it distributed | Part III | The same playbook on a kind cluster, adding a `loop:` (parallel), a `postgres` step and a sub-playbook. Read the event log. | distributed (kind) |
| Ch. 19 — MCP tool + agent | Ch. 18 | Expose a playbook through `metadata.expose.mcp`, then call it from a `kind: agent` step | local, then distributed |
| Ch. 24 — To the edge | Ch. 23 | Factor out a pure sub-playbook, compile it with `playbook-wasm`, check parity, and run it in a Cloudflare Worker | edge |

Each project ends with a "what changed and why" section, a quiz, and
an "extend it" list.

### 2.3 In-line quizzes after sections (CEL)

Every section (`chNN-MM`) ends with a short quiz of 2–5 questions. Rules
taken from the CEL work:

- **Distractors encode real misconceptions.** Wrong options come from
  mistakes people actually make. Examples: "a tool list dispatches one
  command per tool"; "local mode honours `loop:`"; "`retry:` re-runs a
  failed tool"; "a container step holds its slot until the Job ends".
  Appendix F collects them.
- **Every answer has an explanation.** The explanation is shown for
  right answers too.
- **Not graded.** Answers are not reported to anyone. The point is
  retrieval practice. (Brown's edition collected anonymous telemetry
  to improve its questions; whether to do that is an open decision, §9.)
- **Question types:** multiple choice, short answer, and *trace
  questions*: "given this playbook and this event, which event comes
  next / what is the step state now?". This is NoETL's analogue of
  Brown's "does this program compile / what does it print" questions.

### 2.4 "Check your understanding" checkpoints

At the end of each chapter, a longer checkpoint (5–10 questions) mixes
in concepts from earlier chapters (spaced retrieval). Part-level
checkpoints close each Part.

### 2.5 Visualizing execution and state

Brown's edition uses Aquascope to draw Rust ownership and permissions
at each program point. NoETL's equivalent subject is **the event log
and the state folded from it**. The book plans three visualizations:

1. **Event-log step-through** (`mdbook-noetl-trace`, §4). A recorded
   execution is rendered as a timeline. Stepping through it shows each
   event (`command.issued`, `command.claimed`, `call.done`,
   `step.exit` …) and the `WorkflowState` folded so far: which steps
   are pending, running or done; loop counters; the fan-in barrier;
   the variables in scope.
2. **Topology diagrams** (Mermaid). The gateway → server → bus → pool
   path, the slot model, the catalog resolver chain, and import vs
   delegate across instances.
3. **Latency waterfalls.** Per-step time decomposition (issue → claim
   → tool → emit → drive), drawn from measured traces. These anchor
   Chapter 22.

### 2.6 Runnable, inspectable examples

- Every example playbook lives in `examples/` and is **tested in CI**
  against the runtime it names. If an example breaks, the build
  breaks.
- Examples marked ▶ run in the page with a WebAssembly build of the
  local runner (§4, TARGET). Until that exists, each example shows
  the exact `noetl run` command and the expected output, captured
  by CI.

### 2.7 Honest by construction

Every number carries a label (§3). A chapter about a TARGET feature
says what exists today before it says what is planned. The book corrects
myths openly; Appendix F lists them.

### 2.8 Case studies: real projects, read at a commit

Four chapters read real projects from the ecosystem: Ch. 26 in Part
VIII (it needs only the local runtime) and Ch. 33–35 in Part X (they
build on the distributed runtime and operations). Unlike a project
chapter, the reader does not build anything; they read playbooks that
run (or ran) for real and learn why each is shaped as it is. Every
defensive pattern is tied to the runtime rule that forces it, and that
rule is verified in code, not taken from the project's comments.

Concept chapters link forward ("In practice: …") to the section that
shows their rule in a real project. A link is added only when the
target section is written, so nothing points at a stub:

| Concept | In practice | Status |
|---|---|---|
| 4.2 `workload`, templating · 5.1 `kind: python` | 33.2 a python step sees only its `input:` names | 33.2 written |
| 6.1 `next`, exclusive arcs | 33.2 arc order is load-bearing; a losing sibling is skipped for good | 33.2 written |
| 7.2 what a hop costs | 33.3 inline vs child playbook per provider | planned |
| 4.4 keychain · 18.1 `kind: mcp` | 33.3 provider calls through MCP playbooks | planned |
| 10.1 gateway | 34.2 deny by default, two roles, the allowlist | planned |
| 31 credentials | 34.1 sign-in as a playbook | planned |
| 4.0 validation · 8 local runtime | 26.2 validate before you run | 26.2 written |
| 6.5 timeouts · 21 resource model | 26.3 wall-clock and transform budgets | planned |
| 8.2 local kinds | 26.4 `kind: shell` as the escape hatch | planned |
| 10.4 slots and KEDA · 27 deployment | 35.3 worker pools and KEDA | planned |
| 27–31 operations · 32 drift | 35.5 what the playbook declares vs what runs | planned |

Publishing rules: only what the public repos contain, and less: no
project ids, real user or document ids, execution ids, hostnames or
third-party data, even where a source file carries them. For
`noetl/quantum`, project level only.

### 2.9 Honest positioning: what NoETL is not for

The owner's brief, verbatim: "what noetl can do and what it can't. When
it is benefit and when it's better to use old way of computation -
programs, tools, AI agents, MCP servers, or even microservices." The
book answers in Ch. 11.1–11.7 and, for data teams, in Part XI.

Rules for these pages:

- **Costs before benefits.** Every comparison starts with what NoETL
  charges (per-step and per-hop overhead, operational weight), as
  labelled, dated measurements with n where the source gives it.
- **"Reach for X instead when…" must be true.** Each alternative gets
  criteria a reader could act on, not a straw man.
- **Composition is the usual answer.** Most real systems put a program,
  tool, agent or service *inside* a step, or call a playbook *from* a
  service. Say where the boundary goes.
- **Built ≠ on.** Anything behind an off-by-default flag, on a branch, or
  only designed is labelled PARTIAL or TARGET where it appears.

## 3. Keeping the book true: status discipline

The book describes a moving system, so it borrows the rule ai-meta
uses for its own records (*representation drift*): a copy is true only
while something forces it to agree with the source.

- **Page badges.** Each page has one of REAL / PARTIAL / TARGET / STUB.
  The CSS is in `theme/status.css`.
- **Claim labels.** These are the resource model's labels: MEASURED,
  DEPLOYED, DEFAULT, GUIDANCE, TARGET, NOT_YET_MEASURED. A MEASURED
  number cites where and when it was measured (kind or prod, date, n).
- **Status ledger (Appendix E).** One row per page: badge, the source
  that justifies it (release tag, PR, RFC), and the date last verified.
- **Generated references.** Appendices A, B, C and D are *generated* from
  `orchestrate-core/schema/{playbook.schema.json, dsl-manifest.json,
  resource-model.json}` in `noetl/server`. A schema change regenerates
  them; prose cannot drift from the schema.
- **Myths are tracked.** When a page corrects a common belief, the
  correction is added to Appendix F with its source.
- **Prod facts are never hardcoded as "current".** A page says
  "as of vX.Y (date)" and links to the release. Server and worker
  versions change most days.
- **This repository is public.** No secrets, internal hostnames,
  project IDs or customer data. Case studies built on private repos
  need the owner's sign-off before their details go in (§9).

## 4. Interactive tooling

Today only `mdbook` is needed: `mdbook build` / `mdbook serve`.
Preprocessors are switched on one at a time, each in the PR that adds
its first real use. `book.toml` holds commented-out stanzas for each.

| Need | Tool | Status | Notes |
|---|---|---|---|
| Quizzes | **`mdbook-quiz`** (Brown CEL, `cognitive-engineering-lab/mdbook-quiz`) | adopt | Quizzes are TOML files under `quizzes/`, embedded with `{{#quiz ../quizzes/chNN-MM.toml}}`. It supports multiple choice and short answer, per-question context/explanations, and a fullscreen mode. Its built-in *Tracing* type compiles **Rust** programs, so NoETL trace questions are written as multiple choice that embeds a trace (see `noetl-trace`). Pin the version in CI to one compatible with the pinned `mdbook`. |
| Callouts (REAL/TARGET notes, warnings, myths) | `mdbook-admonish` | adopt | Badge-styled admonitions; "Myth" and "Not yet" admonition types. |
| Diagrams | `mdbook-mermaid` | adopt | Architecture, flows, sequence diagrams; source stays in Markdown. |
| Link integrity | `mdbook-linkcheck` | adopt (CI) | Internal links always; external links weekly. |
| Event-log step-through | **`mdbook-noetl-trace`** (new, in this repo under `tools/`) | build | The analogue of Brown's `mdbook-aquascope`. Input: a recorded execution (`traces/*.json`, the event stream exported from a run). Output: an interactive timeline that shows the folded state at each event. **Fold with orchestrate-core compiled to WASM** — the same reducer the server uses — so the visualization cannot disagree with the engine. |
| Runnable playbooks | **`mdbook-noetl-play`** (new) | build, later | Embeds an editor and a "Run" button backed by orchestrate-core in WASM. ⚠ Today the shipped WASM module runs only **pure** playbooks (`noop`; `rhai` is not pure as shipped). In-browser examples are therefore limited to control flow — arcs, `when`, back-edges, `set` — until a browser host for `http`/`duckdb` exists. Anything else shows a captured CLI run instead. |
| Generated references | **`mdbook-noetl-ref`** (new) or a CI generation step | build | Renders the schema, DSL manifest and resource model into Appendices A–D at a pinned server commit. |
| Example testing | CI job (`examples/` → `noetl run`) | build | Runs every local example with the pinned CLI and diffs the output; kind-only examples are marked and run nightly. |

Why build two NoETL-specific preprocessors rather than only use
off-the-shelf ones: the most important thing this book teaches is how
an *event log becomes state*, and no generic tool can show that. Brown's
edition got its biggest lift from a domain-specific visualizer
(Aquascope). `noetl-trace` is that visualizer for NoETL.

## 5. Chapter-by-chapter plan

Notation: **Status** is the page badge as of this plan. **Sources**
point at the material each chapter must be written from (§7 has the
full map). **Interactive** lists the planned quiz focus (Q), traces (T),
diagrams (D) and runnable examples (▶).

### Part I — Getting Started

| Ch. | Goal — after reading, the reader can… | Status | Interactive |
|---|---|---|---|
| 1 Getting Started | install the CLI (Homebrew tap, APT, the PyPI wheel, which wraps the Rust CLI), write a three-step playbook, run it with `noetl run`, and read its output and local event trail | REAL | Q: what a playbook is; ▶ hello playbook |
| 2 Project: first real playbook | build http → duckdb → file, guard a back-edge with `when`, and explain each event the run produced | REAL | T: the run's own trace; Q: trace questions |

### Part II — The Model

| Ch. | Goal | Status | Key content and corrections | Interactive |
|---|---|---|---|---|
| 3 What NoETL is | explain declarative orchestration; the event log as the source of truth (append-only, never edited); playbooks as ephemeral blueprints; workers as stateless compute that claim one command, run it, emit events and release the slot; the two catalogs (internal objects in EHDB, business data in external stores read by steps) | REAL | Execution-model rule; "all data access happens inside playbook steps" | D: the blueprint/worker split; Q: misconceptions about resident agents and state |
| 4 Anatomy of a playbook | read and write every top-level key: `apiVersion: noetl.io/v2`, `kind: Playbook`, `metadata`, `vars`, `keychain`, `workbook`, `workload`, `workflow` | REAL | ⚠ **There is no top-level `steps:`; `workflow` *is* the step list.** Required keys: `apiVersion`, `kind`, `metadata`, `workflow`. Step keys: `step`, `desc`, `spec`, `when`, `loop`, `tool`, `next`, `set`, `args`, `vars`. | Q; ▶ editing a playbook |
| 5 Tools | choose a tool kind; know what each costs; use an ordered tool list | REAL | ⚠ **An ordered `tool:` list is one command on one worker in one slot** (`task_sequence`), not one dispatch per tool; it has an iteration cap. `python` *is* a distributed-runtime kind (a subprocess on the worker): the Python **platform** was retired, not the tool. `agent` and `mcp` are gated kinds. Result size limits: event result context 100 KiB, command context 512 KiB; large results travel by reference. | Q: "how many slots does this step hold?"; D: task_sequence |
| 6 Control flow | route with the four forms of `next` (name, list, list of `{step, when, args}`, router `{spec:{mode: exclusive\|inclusive}, arcs:[…]}`); guard with Jinja2 `when`; loop two ways | REAL / 6.5 PARTIAL | ⚠ **Both loop forms are real:** `loop: {in, iterator, spec:{mode: sequential\|parallel\|cursor, max_in_flight}}` *and* back-edges (an arc to an earlier step). There is no server cap on iterations or back-edge repeats; the playbook's own guard is the only bound. ⚠ `loop.spec.max_in_flight` is parsed but not read by anything, so a parallel loop dispatches every item at once. ⚠ 6.5: `retry` is parsed but no executor applies it; most kinds have no default timeout. | T: a back-edge loop and a parallel loop side by side; Q: "will this loop terminate?" |
| 7 Sub-playbooks | compose with `kind: playbook`; know that a child execution is a full execution with `parent_execution_id` | REAL | What a hop costs (MEASURED 9–15 s in 2026-08; the plan targets ~3–5 s, NOT_YET_MEASURED). `return_result` makes the parent poll every 2 s while holding a slot. Heuristic: inline a one-call child. | Q; D: parent/child slots |

### Part III — The Three Runtimes

| Ch. | Goal | Status | Key content and corrections | Interactive |
|---|---|---|---|---|
| 8 Local runtime | run anything locally and know exactly what is not supported | REAL | `noetl run <ref> -r local\|distributed\|auto` (flag → context → default local). Everything runs in one in-process Rust interpreter. **Local kinds:** shell, http, playbook, duckdb, auth, sink, rhai, provider, agent, noop. ⚠ **No `python`, no `postgres` locally** (rejected up front: "run it on a cluster instead"). ⚠ **`loop:` is parsed but not executed locally.** Iterate with a back-edge arc plus `when`, set-based DuckDB SQL inside one step, or rhai. The local Feather event buffer can be replayed with `noetl push`. | Q: "which of these runs locally?"; ▶ a back-edge loop |
| 9 Daemon | run a playbook per message with `noetl subscribe`; serve MCP and agents with `noetl serve` / `subscribe --serve` | REAL | A standalone `kind: Subscription` listener over NATS, Pub/Sub or Kafka. No Kubernetes, no server. It has a local disk spool and a JSONL event trail, can `--dispatch server`, and keeps durable tasks in `--task-db`. It is not a general-purpose daemon. | D; Q |
| 10 Distributed runtime | trace one execution through gateway → server → EHDB command bus → worker pools, and reason about slots | REAL | The gateway is a gatekeeper only (auth, SSE, push ingress). The server drive is orchestrate-core running as WASM on the system pool. Pools claim `commands.<pool>.>`. A slot is held from claim until the tool returns; capacity = replicas × slots. KEDA scales on `ehdb_feed_subject_lag` (`replicas ≈ ceil(lag/2)`), **not** on NATS consumer lag (NATS is removed). Pool sizes as DEPLOYED in the resource model, with a date. | **T: the flagship trace, one execution end to end**; D: topology; Q |
| 11 Choosing a runtime, and when not to use NoETL | pick local, daemon or distributed for a workload; and decide whether NoETL fits at all | REAL (11.4, 11.5 PARTIAL) | Comparison table: kinds supported, concurrency, durability, cost, what each runtime refuses. 11.1–11.7 (§2.9): good at; a program (11.2 written: per-step cost table, a hot loop as one step vs many); an existing tool; AI agents; MCP servers; microservices; a decision guide | Q: scenario questions |
| 12 Project: distributed | move the Ch. 2 playbook to kind, add a parallel loop, a postgres step and a sub-playbook, and read the event log | REAL | | T, Q |

### Part IV — The Substrate: EHDB and ehgraph

| Ch. | Goal | Status | Key content and corrections | Interactive |
|---|---|---|---|---|
| 13 EHDB | explain what EHDB is (Arrow-native storage; event log, projection, KV and object engines) and how it carries both buses | REAL; 13.6, 13.7 PARTIAL | Why NATS was replaced: the command bus flipped 2026-07-27; NATS was deleted (T5) 2026-08-01. Sealed parts + active part + manifest. Bloom filters (scheme 2 on prod since 2026-11-07) and the prune floor. One writer process hosts both buses. 13.5: the writer lease/epoch is observed in prod; the fence runs in enforce, armed on both buses (read 2026-11-16); the code's "not armed" note is history. 13.6: tail replication ships the unsealed tail every 60 s, asynchronously; tail replication is server-only; the bus stores are single-copy on one volume. 13.7: the chain store serves on prod behind three default-off gates (armed per the 2026-10 record); its comparator (ai-meta#360) is open. | D: part lifecycle; T: append → seal → prune; Q |
| 14 EHDB as state substrate | understand the in-flight move from Postgres command/event rows to EHDB as the authoritative state | TARGET (14.1 PARTIAL) | Embedded state (#332): the owner decided one embedded EHDB per server shard, and the server runs an embedded STS today; sharding, routing and rebalancing are TARGET. **RFC #355**, the execution-partitioned event store: partition by `execution_id`, strong order within a partition, eventual consistency across replicas, retiring reconcile/re-drive. Design only, PR open. It links to Ch. 22 stage 3. | D: before/after; Q |
| 15 ehgraph | know what ehgraph is for, what it supports today, and what it does not | PARTIAL (15.1 written REAL, 15.3 written PARTIAL) | At git `f200516` (pinned by server v3.161.2; no release tag). 15.1 three stores: Postgres the system of record, EHDB the buses + mirror (not yet state), ehgraph a topology read model that stores nothing in EHDB; embedded + writer on, idle on prod (graph_written = 0, 2026-11-22); nothing reads it. 15.2 model (one label per node, soft delete, versions, change log, snapshots, sessions). 15.3 openCypher subset + gap table, Query API v2, Bolt (standalone, opt-in, no TLS), TCK 2024.3 recounted: 2,292/434/1,170 of 3,896 = 58.8% all, 84.1% in-model; 391 failures are unlabeled nodes. 15.4 transactions (serializable OCC, `expect`). 15.5 the embedded instance and switches. 15.6 GCS backup, compaction (off), budgets (the Roadmap page is stale on both). 15.7 TARGET: read model for RFC #586 runtime topology, cells, catalog peers; read replicas not built | Q; ▶ a Cypher query against a recorded graph (later) |

### Part V — Distribution

| Ch. | Goal | Status | Key content and corrections | Interactive |
|---|---|---|---|---|
| 16 Distributed catalog | explain content-addressed playbooks and how a reference is resolved, pinned and discovered | PARTIAL (released, flags off) | Phase 1, v3.157.0: digest identity over semantic sorted-key JSON, blob dedup, per-execution `catalog_id` watermark pin. Phase 2, v3.158.0: bloom adverts (`p:`/`v:`/`d:`), signed `peer/resolve`, import under `peer/<id>/`. Phase 3, v3.159.0: hot reload, gated three ways (flag, policy, `@latest`). v3.160.0: `db://`, `ehdb://`. Schemes: `noetl://<ni>/path@v`, `gs://`, `s3://`, `az://`, `minio+http(s)://`, `https://`, `db://<alias>/<schema>.<table>?…`, `ehdb://catalog/<id>`. ⚠ Only S3 has been tested (against a mock); gs/az are untested. Enable order: `NOETL_CATALOG_CAS` → `_PINNING` → `_DISCOVERY` → `_REMOTE_*`. `kind: wasm`: worker fuel/time/memory limits (worker v6.13.0, on by default); AOT codegen is TARGET. | D: the resolver chain; Q: "which version will this execution run?" |
| 17 Cross-instance | delegate or import a playbook to another instance | PARTIAL | Instance identity (ML-DSA-87) and signed register/discover (v3.156.0). On prod the registry is on but admits nobody (no trusted IDs). `remote: import\|delegate` on `kind: playbook` (server v3.161.0, tools v4.6.0, worker v6.15.0, cli v6.4.0): released, flags off, proven between two kind runtimes. The pin is held across instances, first writer wins. The CLI and `serve` refuse remote references. TARGET: push completion (A polls every 2 s today), cross-instance cancel, batch delegation. | D: import vs delegate sequence; Q |

### Part VI — Interop and Concurrency

| Ch. | Goal | Status | Key content and corrections | Interactive |
|---|---|---|---|---|
| 18 MCP and agents | call MCP servers and agents from playbooks, and expose playbooks as both | REAL (18.5 PARTIAL) | `kind: mcp` / `kind: agent` (server gates `NOETL_TOOL_KIND_MCP`/`_AGENT`; the worker needs `NOETL_WORKER_AGENT_TOOL`), on in the reference prod since 2026-11-11. Playbook as MCP server: `/api/mcp`, opt-in per playbook via `metadata.expose.mcp`. Playbook as agent: `/api/agents` (cards; callbacks need allowed origins, otherwise poll). Local and daemon: `kind: mcp`, `noetl serve`. Released but off: playbook-bound agent tools as child executions. Limits: 32 tool calls per agent step, 180 s per playbook-bound child, so the worst case is ~96 min of one held slot. Execution-model rule: no resident agents or MCP servers. | D: the interop matrix; Q |
| 19 Project: MCP + agent | expose a playbook as an MCP tool and call it from an agent step, local then distributed | REAL | | T, Q |
| 20 Coroutines | reason about concurrency inside one execution today and under RFC #554 | TARGET (20.1 REAL) | 20.1 today: step-level fan-out (`next` lists, inclusive routers, parallel loops) and fan-in (the reduce barrier, the loop join); no concurrency inside a local run; one command holds one slot (`WORKER_MAX_CONCURRENT` default 4); WASM serialises per worker process; no mid-run cancel or timeout; cancel does not cascade. 20.2–20.5 (RFC #554, accepted 2026-11-12, nothing built): **leaf units** (a tool unit, or a playbook unit = a child execution); no sub-graphs inside a coroutine; the owner step owns its group, which cannot outlive the execution. `spawn.units` / `spawn.each`; `join: all` (default, fail-fast) \| `race` \| `any` \| `settled` \| `{at_least: k}`; `max_in_flight`, `timeout_s`, `restart`. Cancel cascades down the ownership tree; the waiting owner holds no slot. All flags off (`NOETL_COROUTINES` …). Shipped prerequisite: the cancel-spelling fixes (server v3.161.1–.2). | T: a race join; Q: "what happens to siblings when one fails?" |

### Part VII — Resources and Performance

| Ch. | Goal | Status | Key content and corrections | Interactive |
|---|---|---|---|---|
| 21 Resource model | estimate a playbook's time, slots and risk before running it, using `noetl.ai/dsl/resource-model.json` | REAL | Top-level keys: `step_kinds`, `limits`, `concurrency`, `heuristics`, `orchestration_overhead`, `not_yet_measured`, `labels`. Per-kind: execution, holds_slot, timeout, measured. Limits: WASM fuel 1e10, wall clock 30 000 ms, memory 1024 MiB; agent 32 calls; 4 slots per worker; 100 KiB / 512 KiB / 2 MiB size caps. Heuristic: `steps × per_step + Σwork + hops × hop`; count slots, not steps; budget 2 slots per awaiting parent; guard every loop. **Seven NOT_YET_MEASURED gaps**, listed verbatim. | Q: estimation exercises; ▶ a small estimator widget (later) |
| 22 Orchestration overhead | explain where a step's time goes and what the ranked fixes buy | PARTIAL (measurements REAL, fixes TARGET) | MEASURED (prod 2026-11-02, n=4, a 7-step turn, p50 8.69 s with 1.84 s of tool time): **~0.95 s/step of handoff** = completed→issued ~0.46 s (the drive is itself a dispatched command, so each step is handed off twice) + issued→claimed ~0.33 s + three reporting emits ~0.16 s. Raw Postgres is only ~10–15 % of it. Earlier figures: ~4.5 s/step and 82 % orchestration (2026-08). **Ranked fixes:** 0 `noetl.command(event_id)` index (#283); 0b benchmark harness (#557); 1 worker self-drive (#558); 2 push-not-poll to a waiting parent (#559); 3 EHDB state (#560 / RFC #355); 4 WASM fusion of deterministic chains (#561); 5 warm pools (#562). The worked example (8.69 → ~3.6 → ~3.1 s) is TARGET arithmetic. 22.4 covers measuring honestly: same-period baselines, labelled n, instruments that cannot see the fix. Source: ai-meta PR #556 (`docs/rfc/latency-reduction-plan.md`), open. | D: latency waterfall; Q: "which fix removes which bar?" |
| 23 WASM at the edge | decide whether a playbook can run at the edge, and ship it | PARTIAL (23.3 REAL, one deployment) | Purity: only pure playbooks compile; anything with I/O stays in the host. ⚠ **What is real is stage 1, "embed + validate"**: a generic orchestrate-core runner module plus a custom section holding the playbook JSON, with a compile-time purity check. Template pre-parse (stage 2), AOT Rust codegen (stage 3) and auto-routing of pure sub-graphs (stage 4) are TARGET. **Do not describe it as "compiled to Rust".** The kuksin.us proof: three pure playbooks in one module inside a Cloudflare Worker, with no server round trip, slot or event; the model call and email send run in the Worker's JS; parity checked by test harnesses. The edge latency distribution is NOT_YET_MEASURED. | D; ▶ (this chapter is where `noetl-play` debuts); Q |
| 24 Project: edge | factor out a pure sub-playbook, compile it, verify parity, deploy to a Worker | PARTIAL | | Q |

### Part VIII — Applied

| Ch. | Goal | Status | Key content | Interactive |
|---|---|---|---|---|
| 25 Bot fleets | compare running agent/bot fleets on NoETL against one shared VM per account, honestly | PARTIAL (RFC #556 open) | Isolation: **NoETL cannot claim a per-bot security boundary today.** Shared worker processes; subprocesses inherit the worker environment; named credentials resolve for any caller; the auth gate runs in shadow. What it can claim: execution-scoped declared credentials, a WASM sandbox for pure logic, a pod boundary for `container`, and a better audit trail. Cost: idle cost scales with work, not accounts (a 0.5 vCPU pool floor vs ~8 vCPU per account VM, GIVEN). Concurrency: fan-out spreads across pods, but there is no throttle, waiting parents can deadlock a small pool, and new nodes take 60–90 s. Proposed stages: an env allowlist + auth enforce first, then sandbox tiers, overhead collapse, scale-to-zero, session sandboxes. | Q: trade-off scenarios |
| 26 Quantum pipeline (replaced the private quantum-readiness study, 2026-11-17) | run long compute on the local runtime, validated against the live grammar | REAL (26.2 written) | `noetl/quantum` at `9208fa2`, project level only: honest defaults (no data, no score); validate with a pinned digest, fallback never counts as acceptance; seven-hour wall clock split per task, transform budget, hard deadline; `kind: shell` cmds | Q |

### Part IX — Operations

| Ch. | Goal | Status | Key content | Interactive |
|---|---|---|---|---|
| 27 Deployment modes | deploy to kind, then GKE; deploy by digest | REAL | Kind first via `ehdb_platform.yaml` (`profile=kind` refuses non-kind contexts); the legacy `development/noetl.yaml` named as stale; prod topology as the shape-only manifests declare it, and why committed ≠ live (#267); image-only patch of a named container by digest after a whole-object server-side dry-run, rollback from the ledger; the 2026-09-08 apply outage | Q |
| 28 Releases | understand semantic-release ownership of versions | REAL | `feat` minor, `fix`/`perf`/revert patch, `!` major, anything else nothing (silently); every commit since the last tag is read; the tag is the version (`Cargo.toml` a floor on server/worker/tools, stamped at build, reported by `*_build_info`); never hand-edit (ai-meta#224); manual dispatch bypasses the check (server v3.153.0); commit type is an unchecked semver claim (ai-meta#330) | Q |
| 29 Rollout/rollback | roll safely | REAL | Smoke (fixtures + a server-API turn + a guest gateway turn) before *and* after each roll, and it proves which cluster it hit; one pool at a time (system-pool stall ~7–10 min, #504); SIGTERM drain since worker v6.11.3; rollback by recorded digest with four dated cases; readers before writers and the moving rollback floor (#517); restart costs | Q |
| 30 Observability | find out what an execution did and get alerted | REAL | `execution_id` as the trace key: the event log, with a W3C `trace` object as an optional join and no span exporter; three unauthenticated `/metrics` surfaces; alert policies as code (only the Cloud Monitoring path delivers; the `duration` default trap; file vs live unsynced, ai-meta#471); scrape coverage from the 2026-10-04 selector fix | Q |
| 31 Credentials | use credentials without leaking them | REAL | Storage: envelope encryption, fail-closed key, optional KMS; delivery: `include_data` fetch, route gate default shadow, sealed delivery and mTLS opt-in; event log: deferred `keychain.*`, drive guard (worker v5.70.3), result scrubbing and its limit; worker env a convention (`NOETL_KEYCHAIN_ENV_VARS`); bootstrap secrets as CSI files; inert features (audit has no writer, residency off) | Q |
| 32 Representation drift | keep docs, dashboards and memory true | REAL | "What forces this copy to agree, and how would anyone find out if it disagreed?" Worked examples from NoETL's own history, chosen for being instructive and safe to publish. | Q |

### Part X — In Practice: Case Studies

| Ch. | Goal | Status | Key content | Interactive |
|---|---|---|---|---|
| 33 Travel playbooks | read a real playbook family and see why each step is shaped as it is | REAL (33.2 written) | `noetl/travel` at `cd210d7`: contract shape; profile flow (validate → read \| save → read back → best-effort suggestions; `merge: true`; arc order; skip semantics; python bindings); providers inline vs child (cite 7.2); itinerary planner state; `qa/regression` | Q; T (a recorded profile run, once T-05 exists) |
| 34 Auth | see access control enforced by the gateway and by playbooks | PARTIAL | gateway v3.22.1 `authorization.rs`: two roles, deny by default, `GATEWAY_USER_PLAYBOOKS`, ownership, guest; Auth0 validation playbook vs `NOETL_AUTH_SYNC`. In flight, labelled: `grant_role`, verified-email role inheritance | Q |
| 35 Platform | stand the platform up and know which parts of the recipe are current | PARTIAL | `noetl/ops`: fresh-stack playbook (a NoETL playbook provisioning NoETL), Cloud Build, KEDA ScaledObjects, CSI secrets, EHDB platform playbook; stale vs current; committed ≠ live (#267) | Q |

### Part XI — Data Pipelines: Lineage, Governance and Mesh

| Ch. | Goal | Status | Key content | Interactive |
|---|---|---|---|---|
| 36 Data lineage | know which lineage NoETL records and which you must declare | PARTIAL (36.1 written, REAL) | Automatic execution lineage: `catalog_id` → `(path, version, content)`, workload, `parent_execution_id`, step events and results, producer-naming result references; the API's 2,000-event window. Built, off: the registry with declared `lineage` (`NOETL_REGISTRY_ENABLED`), canonical result URI consumption (`NOETL_RESULT_URI_ACCEPT`). Not done: dataset/column lineage, any lineage-standard emitter | Q; T (a recorded run's lineage, once T-05 exists) |
| 37 Data governance | govern pipelines on NoETL and know the gaps | PARTIAL | Access control (Ch. 34), audit and reproducibility (replay vs re-run), secrets and PII (scrubber limits), policy at registration; gaps first: no secret-audit writer, shadow-default gate, no policy engine, never-purged log vs erasure | Q |
| 38 Data mesh | see which data-mesh principles NoETL can serve | PARTIAL | Ownership by path/label convention (no owner field), playbooks as product interfaces (no contracts/SLOs), self-serve from laptop to cluster, federation behind Part V flags; no platform claim | Q |

### Appendices

A DSL reference, B tool kinds, C flags and env vars, D the resource model
annotated: **generated** (§3). E status ledger. F myths and corrections.
G glossary. H contributing: style, badge rules, how to write a quiz,
how to record a trace.

**Seed list for Appendix F** (each confirmed by the sources in §7):

| Myth | Truth |
|---|---|
| "The Python tool was removed." | The Python *platform* was retired; `python` is still a distributed-runtime tool kind. It is not available locally. |
| "Local mode iterates with `loop:`." | Local mode parses `loop:` but ignores it; use back-edges, DuckDB SQL or rhai. |
| "A `tool:` list dispatches each tool separately." | It is one `task_sequence` command in one slot. |
| "NoETL uses NATS." | The server transport is EHDB; NATS was deleted in 2026-08. `nats` survives only as a subscription source / tool kind. |
| "KEDA scales on NATS lag." | It scales on `ehdb_feed_subject_lag`. (`agents/rules/execution-model.md` in ai-meta still says NATS and needs a fix.) |
| "`retry:` re-runs a failed tool." | It is parsed and not applied. |
| "`max_in_flight` throttles a parallel loop." | It is parsed and not read. |
| "Edge playbooks are compiled to Rust." | Stage 1 embeds the playbook JSON in a generic runner module; codegen is TARGET. |
| "ehgraph stores graphs in EHDB." | It does not; domain data stays out of EHDB. |
| "Postgres is the orchestration bottleneck." | Raw Postgres is ~10–15 % of per-step overhead; handoffs dominate. |

## 6. Authoring order

The order follows two rules: **write what is REAL first**, and **write
each foundation before the chapters that build on it**. TARGET chapters
are written last and kept short, so they are cheap to rewrite when the
feature lands.

| Phase | Chapters | Why now | Exit criteria |
|---|---|---|---|
| **0 Tooling** | `book.toml`, CI (build + linkcheck), `examples/` test harness, the spec (`specs/001-noetl-book/`), labels + one issue per chapter, Appendix H / `CONTRIBUTING.md` | Every later chapter depends on tested examples and badge rules | `mdbook build` and the example tests run green in CI |
| **1 Foundations** | Ch. 3, 4, 5, 6, How to Read; Appendices A, B (generated) and F (myths seed) | The concepts everything else uses, all REAL | Each section has a quiz; Appendix F has ≥10 entries |
| **2 Getting started + local** | Ch. 1, 2, 8, 7, 9, 11, then the Introduction | The tutorial track's first leg; local mode needs no cluster | Ch. 2 runs end to end in CI |
| **3 Distributed + the trace visualizer** | Build `mdbook-noetl-trace`; Ch. 10, 12 | Ch. 10.5 is the book's flagship visualization | One recorded execution steps through correctly, folded by orchestrate-core |
| **4 Substrate and resources** | Ch. 13, 21, 22 (measurements), 30, 27–29, 31 | REAL internals and operations; resource model numbers already labelled | Appendices C and D generated |
| **5 Interop and distribution** | Ch. 18, 19, 16, 17, 15, and 20.1 (concurrency today); case studies Ch. 26 and 33–35, each after the concept chapters it cites; Ch. 11.1–11.7 and Part XI (§2.9) | Released (some flags off); write "what is on where" carefully | Every flag named with its default |
| **6 Edge** | Build `mdbook-noetl-play`; Ch. 23, 24 | Needs the WASM runner; the kuksin.us proof is real | One ▶ example runs in the browser |
| **7 TARGET and applied** | Ch. 14, 20, 22.3, 25, 32 | In-flight designs: write them last, short, and tied to their RFCs | Each page states what exists today first |
| **Continuous** | Status ledger, myths, regenerated appendices | §8 | |

**First concrete deliverables** (the next PRs after this one):

1. CI: `mdbook build` + linkcheck + example-run job.
2. Ch. 4 *Anatomy of a playbook* and Ch. 5 *Tools*, with quizzes
   (this is where `mdbook-quiz` gets enabled).
3. Ch. 1 + Ch. 2, with tested examples.
4. Ch. 6 *Control flow*. It carries the most myth corrections, so it
   is high value.

## 7. Where the truth lives: source map

Write from these sources, cite them on the page, and re-check them
against the code when versions move.

| Topic | Source of truth |
|---|---|
| DSL schema, kinds, resource model | `noetl/server` → `orchestrate-core/schema/playbook.schema.json`, `dsl-manifest.json`, `resource-model.json` (generator: `orchestrate-core/src/resource_model.rs`); published at `noetl.ai/dsl/` |
| Local runtime behaviour | `noetl/cli` → `src/playbook_runner.rs` (local kinds, back-edge routing), `executor/src/playbook.rs`; CLI README and wiki |
| Daemon | `noetl/cli` → `src/subscribe/`; cli wiki `subscribe.md` |
| Execution model | ai-meta `agents/rules/execution-model.md` (⚠ its KEDA/NATS line is stale) |
| EHDB | `noetl/ehdb` README, `docs/SCOPE.md`, the ehdb wiki; ai-meta RFCs `ehdb-*.md`, `ehdb-nats-takeover-plan.md` |
| State substrate | ai-meta `docs/rfc/ehdb-embedded-state.md` (#332), `ehdb-execution-partitioned-event-store.md` (PR #355) |
| ehgraph | `noetl/ehgraph` README |
| Catalog | ai-meta `docs/rfc/distributed-playbook-catalog.md` (#548, PRs #549/#551) and the wiki Umbrella page |
| Cross-instance, MCP and agents | ai-meta `docs/rfc/interop-topology-and-ai-mcp-playbooks.md`, `interop-missing-tools-build-plan.md` |
| Coroutines | ai-meta `docs/rfc/coroutines.md` (PR #554) |
| Overhead and ranked fixes | ai-meta PR #556: `docs/rfc/latency-reduction-plan.md`; issues #283, #557–#562 |
| Bot fleets, edge proof | ai-meta PR #556: `docs/rfc/bot-fleets-vs-shared-account-vm.md` (§2.5 is the edge proof) |
| Operations | ai-meta `agents/rules/{deployment-validation, ops-deploy, apply-safety, release-versioning, observability, no-default-connection, representation-drift}.md` |
| Release history | ai-meta wiki `Releases.md`, `Sessions-Log.md` |

## 8. Maintenance loop

- **Tracked in ai-meta.** The book is a submodule at `repos/book` and is
  tracked by an ai-task issue on `noetl/ai-meta`. When a feature
  changes status (released, flag flipped on, RFC accepted), the PR that
  records it in ai-meta should also flip the book chapter's badge, or
  open a book issue to do so.
- **Per server/worker release:** regenerate Appendices A–D at the new
  commit and re-run the example tests. A diff in a generated appendix
  is a review prompt for the matching chapter.
- **Quarterly status audit:** walk Appendix E and re-verify every REAL
  and PARTIAL row against the code and release notes, not against this
  book.
- **Quizzes are maintained like tests.** A question whose answer
  changes with a release is updated in the same PR as the chapter.

## 9. Open decisions

For the owner:

1. **Hosting**: a book subdomain on noetl.dev, noetl.ai or GitHub Pages?
2. **License** for the book text (the Rust Book uses MIT/Apache-2.0
   for code and examples).
3. **Quiz telemetry**: none (default), or anonymous telemetry to
   improve questions, as Brown's edition did?
4. ~~**Quantum-readiness case study (Ch. 26)**: its source repo is
   private. Publish a sanitized version, or swap in a different case
   study?~~ **Decided 2026-11-17 (owner): swapped.** Ch. 26 is now the
   public `noetl/quantum` case study (REAL, project level only); the
   private study is retired (#36).
5. **Edge runner scope**: should the in-browser runner (Ch. 23) get a
   browser host for `http` so more examples are runnable?
