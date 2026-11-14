# The NoETL Book — Roadmap

**Updated 2026-11-13.** This page shows the whole book at once: every
Part and chapter, what it covers and why it is there, how true it is
today, and when it gets written.

Three documents describe the book. Keep them consistent; if they
disagree, fix them in the same PR:

| Document | Role |
|---|---|
| [`src/SUMMARY.md`](../src/SUMMARY.md) | **What** — the table of contents mdBook builds. It is the contract: every page listed exists. |
| [`docs/BOOK-PLAN.md`](BOOK-PLAN.md) | **How and why** — pedagogy, status discipline, tooling, per-chapter goals and corrected facts, source map. |
| `docs/ROADMAP.md` (this page) | **The arc and the order** — one description per chapter, its badge and its authoring phase. |

Contributors work from the spec and issues described in
[`CONTRIBUTING.md`](../CONTRIBUTING.md). A summary of this page is
mirrored on the [book wiki](https://github.com/noetl/book/wiki/Roadmap).
This file is the canonical copy.

## How to read the roadmap

**Badge** is the status of the *subject*, not of the prose. Every page
is a stub today.

- **REAL**: shipped and released. Write it now from the code.
- **PARTIAL**: some of it is real; the rest is released behind an
  off-by-default flag, proven only on a test cluster, or exists only
  as one deployment. Write the real part now and label the rest.
- **TARGET**: designed (usually in an RFC), not built. Write it last
  and keep it short, because it will be rewritten when the feature lands.

**Phase** is the authoring phase from
[BOOK-PLAN §6](BOOK-PLAN.md#6-authoring-order):

| Phase | Focus | Ready to write? |
|---|---|---|
| **P0** | Tooling: CI build, linkcheck, example tests, contributor guide | now |
| **P1** | Foundations: the model, playbooks, tools, control flow | **now** |
| **P2** | Getting started, first project, local runtime, daemon | **now** |
| **P3** | Distributed runtime + the trace visualizer | now (needs P0 CI and a kind cluster) |
| **P4** | EHDB, resources, measured overhead, operations | now |
| **P5** | Interop and distribution (released, mostly behind flags) | now, with care over flag states |
| **P6** | Edge / WASM + the in-browser runner | after the runner exists |
| **P7** | TARGET designs and applied studies | later; rewrite when features land |

### At a glance

| Part | Chapters | Badges | Phases |
|---|---|---|---|
| Front matter | Introduction, How to Read | REAL | P1–P2 |
| I Getting Started | 1–2 | REAL | P2 |
| II The Model | 3–7 | REAL | P1 (Ch. 7 P2) |
| III The Three Runtimes | 8–12 | REAL | P2–P3 |
| IV EHDB | 13–15 | REAL / TARGET / PARTIAL | P4, P5, P7 |
| V Distribution | 16–17 | PARTIAL | P5 |
| VI Interop and Concurrency | 18–20 | REAL / REAL / TARGET | P5, P7 |
| VII Resources and Performance | 21–24 | REAL / PARTIAL / PARTIAL / PARTIAL | P4, P6 |
| VIII Applied | 25–26 | PARTIAL | P7 |
| IX Operations | 27–32 | REAL | P4 (Ch. 32 P7) |
| Appendices | A–H | REAL (generated / living) | P0–P4, continuous |

---

## Front matter

**Introduction** · REAL · P2 (final pass after Part II). This page
explains what NoETL is in one page: playbooks of steps and tools,
executed by one of three runtimes, with every transition recorded as an
immutable event. It also sets out the path the book takes. It is
written last among the early chapters, because it should summarise
what Parts I–II actually say.

**How to Read This Book** · REAL · P1 (drafted). This page explains the
badges, the claim labels (MEASURED, DEPLOYED, DEFAULT, GUIDANCE,
TARGET, NOT_YET_MEASURED), how the quizzes work (ungraded, explained
answers), and how to use traces and runnable examples. It comes first
because the book's honesty depends on readers knowing what a badge
promises.

## Part I — Getting Started

*Get a reader from nothing to a working playbook in minutes, so every
later concept attaches to something they have already run.*

**Ch. 1 Getting Started** · REAL · P2. It covers installing the CLI
(Homebrew, APT, or the PyPI wheel that wraps the Rust CLI), writing a
three-step playbook, and running it with `noetl run`, then reading the
output and the local event trail. It is the first chapter because
running something real comes before theory, as in the Rust Book.

**Ch. 2 Project: Fetch, Transform, Store** · REAL · P2. The first
project chapter: an `http` → `duckdb` → file pipeline with one guarded
back-edge, run locally. The reader then walks the events the run
produced. It consolidates Part I and quietly introduces the ideas Part
II names: steps, tools, arcs, the event log.

## Part II — The Model

*The concepts every runtime shares. Nothing here depends on a cluster.
This Part carries the most myth corrections, so it is written first.*

**Ch. 3 What NoETL Is** · REAL · P1. Declarative orchestration; event
sourcing (the append-only log is the source of truth); playbooks as
ephemeral blueprints and workers as stateless compute; the split
between the *internal* catalog (NoETL's own objects, in EHDB) and
*business* data (in external stores, read by steps). It is the mental
model the rest of the book refines.

**Ch. 4 Anatomy of a Playbook** · REAL · P1. Every top-level key:
`apiVersion`, `kind`, `metadata`, `vars`, `keychain`, `workbook`,
`workload`, `workflow`, and the step keys. It corrects the common
belief that playbooks have a top-level `steps:` (`workflow` *is* the
step list). It is the reference shape everything else hangs on.

**Ch. 5 Tools** · REAL · P1. The tool kinds and what each costs; the
ordered tool list, which is **one command in one slot**
(`task_sequence`), not one dispatch per tool; results, references and
size limits. It is here because "what does a step actually run, and
where" decides correctness and cost.

**Ch. 6 Control Flow** · REAL (6.5 PARTIAL) · P1. The four forms of
`next`, routers and `when` guards. Both loop forms: `loop:`
(sequential, parallel, cursor) and back-edges (loops as goto). What is
and is not enforced: `retry` and `max_in_flight` are parsed but inert,
and most kinds have no default timeout. It is the highest-value early
chapter because it corrects the most misconceptions.

**Ch. 7 Composition: Sub-Playbooks** · REAL · P2. `kind: playbook`,
child executions, and what a hop costs (time and held slots). It is
placed after control flow because composition is where design choices
start to have performance consequences, which sets up Part VII.

## Part III — The Three Runtimes

*The same playbook, three places to run it. Each chapter is precise
about what that runtime supports and refuses.*

**Ch. 8 The Local Runtime** · REAL · P2. `noetl run` as one in-process
Rust interpreter; the local tool kinds (no `python`, no `postgres`);
iteration without `loop:` (local mode parses it but does not run it),
using back-edges, DuckDB SQL or rhai; the local event buffer and
`noetl push`. Readers start here, and the "no loop locally" fact must
be learned early.

**Ch. 9 The Daemon** · REAL · P2. `noetl subscribe` (a per-message
listener over NATS, Pub/Sub or Kafka with spool and event trail) and
`noetl serve` (serving MCP and agents locally); dispatching to a
server. It shows the middle ground between a laptop and a cluster.

**Ch. 10 The Distributed Runtime** · REAL · P3. Gateway → server
(orchestrate-core drive) → EHDB command bus → worker pools. It covers
slots, pool capacity, and KEDA autoscaling on EHDB feed lag, then
follows one execution end to end. This chapter hosts the book's
flagship visualization, the first `noetl-trace` step-through, so it
waits for that tool.

**Ch. 11 Choosing a Runtime** · REAL · P2. A comparison of supported
kinds, concurrency, durability, cost and refusals across the three
runtimes, with scenario quizzes. It is a decision aid that consolidates
Ch. 8–10.

**Ch. 12 Project: Taking Your Playbook Distributed** · REAL · P3. The
Ch. 2 playbook on a kind cluster, adding a parallel `loop:`, a
`postgres` step and a sub-playbook, then reading the event log. It
proves the Part III claims with the reader's own trace.

## Part IV — EHDB: The Substrate

*What sits under the distributed runtime, and where it is heading.*

**Ch. 13 EHDB** · REAL (13.5, 13.7 PARTIAL) · P4. Why NATS was replaced
(the bus moved to EHDB in 2026-07 and NATS was deleted in 2026-08); the
append log (parts, segments, manifest); bloom filters and the prune
floor; the two buses; writer election and fencing (the lease is live,
fence enforce is staged); durability and the unsealed tail; the chain
store. Platform engineers need this to operate and debug the system.

**Ch. 14 EHDB as the State Substrate** · TARGET (14.1 PARTIAL) · P7. The
move from Postgres command/event rows to EHDB as authoritative state:
embedded state per server shard (#332) and the execution-partitioned
event store (RFC #355) that would retire reconcile/re-drive. It is
written last because it is design-only today. It links to the
overhead fixes in Ch. 22.

**Ch. 15 ehgraph** · PARTIAL · P5. A property-graph database for
topology: change log, snapshots, openCypher, Query API v2, opt-in Bolt,
and its embedding in the server. It stores no graph data in EHDB, and
the chapter says so. It completes the storage picture.

## Part V — Distribution: Catalog and Instances

*How playbooks are named, found, pinned and run across instances.
Released, with flags mostly off: each page states the flag defaults.*

**Ch. 16 The Distributed Playbook Catalog** · PARTIAL · P5. Content
addressing and digest identity; resolvers (`noetl://`, `s3://`,
`gs://`, `db://`, `ehdb://`…); per-execution pinning; discovery with
bloom adverts; hot reload; `kind: wasm`. It answers "which version did
this execution run, and where did it come from?"

**Ch. 17 Cross-Instance Execution** · PARTIAL · P5. Instance identity
and the registry; `remote: import` vs `remote: delegate`; pins held
across instances; what is still missing (push completion,
cross-instance cancel). It builds directly on Ch. 16's pinning.

## Part VI — Interop and Concurrency

**Ch. 18 MCP and Agents** · REAL (18.5 PARTIAL) · P5. Calling MCP
servers (`kind: mcp`) and agents (`kind: agent`) from playbooks;
exposing a playbook as an MCP server and as an agent; the interop
matrix across local, daemon and distributed runtimes; agent limits and
the slot cost of a long agent step. This is where NoETL meets the AI
tooling ecosystem.

**Ch. 19 Project: Expose a Playbook as an MCP Tool and Call It from an
Agent** · REAL · P5. The third project: build a tool and its caller,
locally and then distributed. It makes interop concrete and reuses
everything from Parts II–III.

**Ch. 20 Coroutines and Structured Concurrency** · TARGET (20.1 REAL)
· P7 (20.1 in P5). It describes the concurrency that exists today
(step fan-out/fan-in and its gaps), then RFC #554: leaf units,
ownership, `spawn` / `join` / `select`, cancellation that frees slots,
and the staged flags. The "today" section is written early because it
corrects beliefs; the design sections wait for the build.

## Part VII — Resources and Performance

*Honest numbers: what things cost, where time goes, and what will
change it. Every figure carries a label.*

**Ch. 21 The Resource Model** · REAL · P4. The published
`resource-model.json`: its labels, per-step-kind costs, limits (WASM
fuel, timeout and memory; agent tool-call caps; context sizes), the
slot and pool model, how to estimate a playbook before running it, and
the seven gaps not yet measured. It teaches readers and agents to plan
rather than guess.

**Ch. 22 Orchestration Overhead** · PARTIAL · P4 (22.3 in P7). It
explains where a step's time goes. The measured ~0.95 s/step of handoff
is made of the drive dispatched as its own command, the claim latency
and the reporting emits. It covers Postgres vs EHDB on the hot path
(raw Postgres is ~10–15 %), the ranked fixes (index, worker self-drive,
push-not-poll, EHDB state, WASM fusion, warm pools), and how to measure
honestly. The measurements are written now; the fixes are written as
they ship.

**Ch. 23 WASM at the Edge** · PARTIAL · P6. Purity (what can compile);
the compiler stages, of which only "embed + validate" is real and
codegen is TARGET; a playbook running in a Cloudflare Worker (the
kuksin.us proof); parity and limits. It shows how far deterministic
playbooks can go without a cluster, and it debuts the in-browser
runner.

**Ch. 24 Project: Ship a Pure Playbook to the Edge** · PARTIAL · P6. The
fourth project, which closes the tutorial track: factor out a pure
sub-playbook, compile it, verify parity, deploy it to a Worker.

## Part VIII — Applied

*Design studies that combine everything earlier. Analysis first, and
the pages state clearly what NoETL cannot claim yet.*

**Ch. 25 Agent and Bot Fleets on NoETL** · PARTIAL · P7. NoETL compared
honestly with one shared VM per account (RFC #556): isolation (no
per-bot security boundary yet), scoped credentials, cost (idle cost
scales with work, not accounts), concurrency and its failure modes, and
the staged architecture to win. It is written after the RFC settles.

**Ch. 26 Case Study: A Quantum-Readiness Orchestrator** · PARTIAL · P7.
A real multi-stage orchestrator on the **local** runtime: a pipeline of
sub-playbooks, crypto-surface classification, signed self-update and
rollback. It shows local mode at production scale. ⚠ The source repo
is private, so this chapter needs the owner's sign-off before writing.

## Part IX — Operations

*How NoETL is run in production. All REAL; written from the
operational rules NoETL's own maintainers follow.*

**Ch. 27 Deployment Modes** · REAL · P4. Kind first, production on GKE,
and deploying by digest with an explicit rollback.

**Ch. 28 Releases and Version Pinning** · REAL · P4. semantic-release
owns versions (`fix`/`feat`/`!`; `chore:` releases nothing); never
hand-edit versions or push tags.

**Ch. 29 Rollout and Rollback Discipline** · REAL · P4. Smoke before
*and* after every roll; one pool at a time; rollback by digest.

**Ch. 30 Observability and Alerting** · REAL · P4. `execution_id` as the
trace key, metrics over logs, alert policies as code, and scrape
coverage as its own risk.

**Ch. 31 Credentials and Secrets** · REAL · P4. Explicit aliases and no
default connection; business secrets in the keychain, never in worker
env or the event log.

**Ch. 32 Representation Drift: Keeping What You Know True** · REAL · P7.
Every copy (doc, dashboard, memory, this book) is true only while
something forces it to agree with the source. Worked examples. It
closes the book because it explains how the book itself stays honest.

## Appendices

| Appendix | Badge | Phase | What and why |
|---|---|---|---|
| A DSL Reference | REAL | P1 | **Generated** from `playbook.schema.json`; the lookup companion to Ch. 4–6 |
| B Tool Kinds Reference | REAL | P1 | **Generated** from the DSL manifest; companion to Ch. 5 |
| C Feature Flags and Environment Variables | REAL | P4 | **Generated**; every flag with its default, so PARTIAL chapters can cite them |
| D The Resource Model, Annotated | REAL | P4 | **Generated** from `resource-model.json`; companion to Ch. 21 |
| E Status Ledger | REAL | continuous | One row per page: badge, justifying source, last verified |
| F Myths and Corrections | REAL | P1, then continuous | Every belief the book corrects, with its source |
| G Glossary | REAL | continuous | Terms as the book defines them |
| H Contributing to This Book | REAL | P0 | Points to [`CONTRIBUTING.md`](../CONTRIBUTING.md) |

## What to write first

1. **P0**: CI (`mdbook build` + linkcheck + example runs); seed the
   spec (`specs/001-noetl-book/`, see `CONTRIBUTING.md`); bootstrap
   labels and one issue per chapter.
2. **P1**: Ch. 4 and Ch. 5 with quizzes (this enables `mdbook-quiz`),
   then Ch. 6 and Ch. 3, plus Appendices A, B and F.
3. **P2**: Ch. 1 and Ch. 2 with tested examples, then Ch. 8, 7, 9 and
   11, then the Introduction.

Everything else follows the phase column. A chapter can move earlier
when its subject becomes REAL; update its badge and phase here, in
BOOK-PLAN §5–6, and on its issue in the same PR.
