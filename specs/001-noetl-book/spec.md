# Feature Specification: The NoETL Book

**Feature Directory**: `specs/001-noetl-book`
**Created**: 2026-11-13
**Status**: Draft v1 (book-wide). Chapter sections marked *Specified* are ready to work; *Draft* sections must be refined before starting.
**Input**: "Write the complete NoETL book: full, rigorous coverage of the ecosystem in the manner of the Rust Book, with Brown CEL's interactive layer (quizzes, checkpoints, execution-state visualization, runnable examples). It must track reality: every page badged REAL / PARTIAL / TARGET."

Governed by [the constitution](../../.specify/memory/constitution.md).
Structure: [`src/SUMMARY.md`](../../src/SUMMARY.md). Order:
[`docs/ROADMAP.md`](../../docs/ROADMAP.md). Pedagogy, goals and sources:
[`docs/BOOK-PLAN.md`](../../docs/BOOK-PLAN.md). Plan: [plan.md](plan.md).
Tasks and issues: [tasks.md](tasks.md).

## Scope

**In scope**: the playbook DSL; the local, daemon and distributed
runtimes; EHDB and its move toward the state substrate; ehgraph; the
distributed catalog; cross-instance execution; MCP/agent interop;
coroutines; the resource and performance model, orchestration overhead
and its fixes; WASM at the edge; bot fleets; a security case study; and
operations. There are four project chapters forming a tutorial track
(local → distributed → MCP/agent → edge).

**Out of scope**: API reference for every server endpoint (the book
links to it); internal incident history beyond what teaches a
principle; anything that requires publishing private or internal
identifiers.

## Audience

1. Playbook authors (Parts I–III, projects). 2. Platform engineers
(Parts IV–VII, IX). 3. Evaluators (Ch. 3, 11, 21, 22, 25). 4. AI agents
that author and plan playbooks (the book links to and explains the
machine-readable DSL knowledge base; it never forks it).

Assumed background: YAML, a shell, basic SQL and HTTP. Rust is not
required except where a page says so.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — A new author runs a real playbook locally (Priority: P1)

A reader with no NoETL experience installs the CLI and, by the end of
Ch. 2, has built and run an http → duckdb → file pipeline and can
explain the events it produced.

**Why this priority**: every later chapter assumes it.
**Independent Test**: follow Ch. 1–2 on a clean machine with the pinned CLI. The CI example runner proves the same.

**Acceptance Scenarios**:
1. **Given** a clean machine, **When** the reader follows Ch. 1, **Then** `noetl run` executes the hello playbook and the output matches the book.
2. **Given** Ch. 2's playbook, **When** it runs locally, **Then** it terminates via its guarded back-edge and the output matches `examples/ch02/`.

### User Story 2 — A reader learns the model without being misled (Priority: P1)

After Part II, the reader can read any playbook and predict its routing,
its loops and its slot usage. They also do not hold any of the
Appendix F myths.

**Independent Test**: the end-of-Part checkpoint quiz. Every
misconception distractor maps to an Appendix F entry.

**Acceptance Scenarios**:
1. **Given** a playbook with a `tool:` list, **When** asked how many slots it holds, **Then** the book has taught "one" (task_sequence).
2. **Given** a `loop:` in local mode, **When** asked what happens, **Then** the book has taught that it is parsed and not executed.

### User Story 3 — A reader can tell what is real (Priority: P1)

On any page, a reader can tell whether a subject ships today and where
each number came from.

**Independent Test**: sample 10 claims from any page. Each has a badge
or label, and each REAL one cites a release or commit that confirms it.

### User Story 4 — A platform engineer operates and reasons about performance (Priority: P2)

After Parts IV, VII and IX, the reader can estimate a playbook's time
and slots from the resource model, explain the per-step overhead, and
roll out and roll back safely.

### User Story 5 — A contributor's AI agent writes a chapter correctly (Priority: P2)

An agent given the CONTRIBUTING agent brief and one issue produces a PR
that meets the issue's acceptance criteria and the constitution, without
supervision beyond review.

**Independent Test**: one P1 chapter written this way passes review with no badge or verification corrections.

### Edge Cases

- A feature changes status mid-draft (released, flag flipped, RFC abandoned): the badge and acceptance criteria change in the same PR as the spec update (constitution III).
- A source contradicts the spec: stop, flag `needs-verification`, and open a spec PR.
- A claim can only be verified on a private source: it needs `owner-decision`, and is not written until signed off.
- A number drifts (versions change most days): it is version-stamped, so it stays true *as of* its stamp.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The book MUST follow the structure in `src/SUMMARY.md`. Every listed page exists (`create-missing = false`).
- **FR-002**: Every page MUST carry exactly one status badge, consistent with ROADMAP and its issue (constitution I).
- **FR-003**: Every REAL claim MUST be verified at a named release or commit and cited in its PR (constitution II).
- **FR-004**: Every section MUST end with a 2–5 question quiz; every chapter with a 5–10 question checkpoint mixing earlier concepts.
- **FR-005**: Every example MUST be a file under `examples/` run by CI against its named runtime.
- **FR-006**: Appendices A–D MUST be generated from the server schema files at a pinned commit.
- **FR-007**: Every corrected misconception MUST appear in Appendix F with its source.
- **FR-008**: The book MUST build with `mdbook` alone until each preprocessor is enabled with its first use.
- **FR-009**: Traces MUST be folded by the engine's own reducer (orchestrate-core compiled to WASM), not by a reimplementation.
- **FR-010**: Nothing published may contain secrets, internal hostnames, project IDs or customer data.

### Key Entities

- **Page**: a file in `src/` with a badge, sources, a quiz and a ledger row.
- **Issue**: one per chapter or task; it links here.
- **Example**: `examples/<chapter>/<name>/` containing a playbook, its expected output and its runtime.
- **Quiz**: `quizzes/chNN-MM.toml` (mdbook-quiz).
- **Trace**: `traces/*.json`, a recorded event log.

## Book-wide chapter criteria

### CH-ALL

Every chapter and appendix PR must satisfy all of these, in addition to
its own criteria below:

1. The page badge is truthful (constitution I) and matches ROADMAP and the issue's `badge:` label.
2. Every REAL claim is verified at a named release or commit; the PR lists claim → where checked.
3. Every number has a label; MEASURED numbers state where, when and n.
4. Each section ends with a 2–5 question quiz with explained answers, once T-03 has landed. Before then, the quiz is drafted in the PR description.
5. Examples are files in `examples/` and pass the runner, once T-02 has landed. Before then, the PR shows the manual run's command and output with the CLI version.
6. The page's Appendix E entry is added or updated in `tools/ledger.json` (the ledger is generated; CI checks it); Appendix F gains any myth the page corrects; Appendix G gains new terms.
7. `mdbook build` and the link check pass.
8. The page states what exists today before what is planned.
9. Nothing private or internal is published.

## Chapter acceptance criteria

## Tooling

### T-01

**CI: mdbook build + linkcheck on every PR** · Badge **REAL** · Phase **P0** · Issue [#3](https://github.com/noetl/book/issues/3) · Specified

Files: `.github/workflows/`, `book.toml`

Acceptance criteria:

1. A GitHub Actions workflow runs `mdbook build` on every PR and on `main`, with pinned mdbook (0.4.40) installed from a cached binary or `cargo install --locked`.
2. `mdbook-linkcheck` is enabled in `book.toml` (internal links on every PR; external links on a weekly schedule, not blocking PRs).
3. A deliberately broken internal link fails the job (prove the gate is red before calling it green; record the failing run in the PR).
4. README documents how to run the same checks locally.

Sources: mdBook docs; mdbook-linkcheck docs; CONTRIBUTING.md §4

### T-02

**Example-playbook runner in CI (examples/ → noetl run, output diffed)** · Badge **REAL** · Phase **P0** · Issue [#4](https://github.com/noetl/book/issues/4) · Specified

Files: `examples/`, `.github/workflows/`

Acceptance criteria:

1. Each example is a directory `examples/<chapter>/<name>/` with `playbook.yaml`, `expected.txt` (or `expected.json`) and a `RUNTIME` file (`local` | `daemon` | `distributed`).
2. CI installs a **pinned** NoETL CLI version, runs every `local` example with `noetl run`, and diffs output against the expected file (with documented normalisation for ids/timestamps).
3. `distributed` examples are listed and skipped on PRs with a visible notice; a nightly job may run them on kind later (out of scope here).
4. A deliberately wrong expected file fails the job (red proven before green).
5. The pinned CLI version is printed in the job log and referenced from Appendix E.

Sources: `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki; BOOK-PLAN §2.6

### T-03

**Enable mdbook-quiz and mdbook-admonish with a first quiz** · Badge **REAL** · Phase **P1** · Issue [#5](https://github.com/noetl/book/issues/5) · Specified

Files: `book.toml`, `quizzes/`, `.github/workflows/`

Acceptance criteria:

1. `[preprocessor.quiz]` and `[preprocessor.admonish]` are uncommented in `book.toml`; CI installs pinned versions compatible with mdbook 0.4.40.
2. One sample quiz (`quizzes/ch00-01.toml`) renders on How to Read; answers are not reported anywhere (no telemetry, per Decisions).
3. Admonition types `myth`, `not-yet` (TARGET) and `partial` exist and are documented in Appendix H / the wiki Style Guide.

Sources: github.com/cognitive-engineering-lab/mdbook-quiz; mdbook-admonish docs; BOOK-PLAN §4

### T-04

**Generate Appendices A–D from the server schema files** · Badge **REAL** · Phase **P1** · Issue [#6](https://github.com/noetl/book/issues/6) · Specified

Files: `tools/`, `src/appendix-01-dsl-reference.md`, `src/appendix-02-tool-kinds.md`, `src/appendix-03-flags.md`, `src/appendix-04-resource-model.md`

Acceptance criteria:

1. A generator (script under `tools/` or a preprocessor) renders the appendices from `playbook.schema.json`, `dsl-manifest.json` and `resource-model.json` at a **pinned server commit** recorded in the output.
2. Regenerating at the same commit is byte-identical; CI fails if committed output is stale versus the pinned commit.
3. Each generated page states the commit and date it was generated from.

Sources: `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json); BOOK-PLAN §3

### T-05

**mdbook-noetl-trace: event-log step-through visualizer** · Badge **TARGET** · Phase **P3** · Issue [#7](https://github.com/noetl/book/issues/7) · Draft (stub; refine with /speckit-clarify before starting)

Files: `tools/`, `traces/`

Acceptance criteria:

1. Folds a recorded event log with orchestrate-core compiled to WASM (the engine's reducer), so it cannot disagree with the engine.

Sources: BOOK-PLAN §2.5, §4

### T-06

**mdbook-noetl-play: in-browser runnable playbooks** · Badge **TARGET** · Phase **P6** · Issue [#8](https://github.com/noetl/book/issues/8) · Draft (stub; refine with /speckit-clarify before starting)

Files: `tools/`

Acceptance criteria:

1. Pure playbooks only until a browser host for http/duckdb exists (owner decision 5).

Sources: BOOK-PLAN §4

## Front matter

### FM-01

**How to Read This Book** · Badge **REAL** · Phase **P1** · Issue [#9](https://github.com/noetl/book/issues/9) · Specified

Files: `src/ch00-01-how-to-read.md`

Acceptance criteria:

1. Defines the four page badges and the six claim labels exactly as BOOK-PLAN §3 / the resource model `labels` define them.
2. Explains quizzes (ungraded, explained answers, no telemetry unless the owner decides otherwise), traces and ▶ runnable examples — marking traces and ▶ as not yet available until T-05 / T-06 land.
3. Ends with a 3-question quiz on badge meanings (requires T-03).
4. Meets [CH-ALL](#ch-all).

Sources: BOOK-PLAN §2–3; noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json)

### FM-02

**Introduction** · Badge **REAL** · Phase **P2** · Issue [#10](https://github.com/noetl/book/issues/10) · Specified

Files: `src/ch00-00-introduction.md`

Acceptance criteria:

1. One page: what NoETL is (playbooks of steps and tools; three runtimes; every transition an immutable event) and the arc of the book, consistent with ROADMAP.
2. Written **after** Parts I–II exist; every claim it makes is backed by a chapter it links to.
3. No version-specific numbers (they live in their chapters).
4. Meets [CH-ALL](#ch-all).

Sources: docs/ROADMAP.md; ai-meta agents/rules/execution-model.md (⚠ its KEDA/NATS line is stale)

## Part I — Getting Started

### CH-01

**Getting Started** · Badge **REAL** · Phase **P2** · Issue [#11](https://github.com/noetl/book/issues/11) · Specified

Files: `src/ch01-*.md`

Acceptance criteria:

1. Install paths that actually exist at a named version: Homebrew tap, APT, and the PyPI wheel (a PyO3 wrapper over the Rust CLI) — each verified by running it, with the version printed.
2. Hello playbook: the minimal valid playbook per `playbook.schema.json` (`apiVersion: noetl.io/v2`, `kind: Playbook`, `metadata`, `workflow`), committed under `examples/ch01/` and run by T-02.
3. Running locally: `noetl run <ref>` (and `-r local`), reading the output and the local event trail.
4. Quiz per section (2–5 questions) with misconception-based distractors.
5. Meets [CH-ALL](#ch-all).

Sources: `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki; `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json); `noetl/homebrew-tap`, `noetl/apt`, `noetl/noetl` README

### CH-02

**Project: Fetch, Transform, Store — Your First Real Playbook** · Badge **REAL** · Phase **P2** · Issue [#12](https://github.com/noetl/book/issues/12) · Specified

Files: `src/ch02-00-project-first-playbook.md`

Acceptance criteria:

1. Builds an `http` → `duckdb` → file pipeline that runs on the **local** runtime (only local kinds), with one back-edge guarded by `when` that provably terminates.
2. The full playbook and its expected output live in `examples/ch02/` and pass T-02.
3. Walks the events the run produced, introducing the vocabulary Part II defines (step, tool, arc, event).
4. Ends with 'what changed and why', an end-of-chapter checkpoint (5–10 questions), and an 'extend it' list.
5. Meets [CH-ALL](#ch-all).

Sources: `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki; `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json)

## Part II — The Model

### CH-03

**What NoETL Is** · Badge **REAL** · Phase **P1** · Issue [#13](https://github.com/noetl/book/issues/13) · Specified

Files: `src/ch03-*.md`

Acceptance criteria:

1. Declarative orchestration and event sourcing: the append-only event log is the source of truth (never edited); state is folded from it.
2. Ephemeral blueprints and stateless workers: claim one command, run it, emit events, release the slot; no resident agents or MCP servers; all data access inside playbook steps.
3. Two catalogs: internal (NoETL's own objects, EHDB-only, `/api/catalog/*`) vs business data (external stores, read by steps).
4. Each section has a quiz; at least 2 Appendix F entries are added or cited.
5. Meets [CH-ALL](#ch-all).

Sources: ai-meta agents/rules/execution-model.md (⚠ its KEDA/NATS line is stale); ai-meta docs/rfc/distributed-playbook-catalog.md; ai-meta wiki Umbrella-EHDB-North-Star-Registry

### CH-04

**Anatomy of a Playbook** · Badge **REAL** · Phase **P1** · Issue [#14](https://github.com/noetl/book/issues/14) · Specified

Files: `src/ch04-*.md`

Acceptance criteria:

1. Covers every top-level key in `playbook.schema.json` at a named server commit: `apiVersion`, `kind`, `metadata`, `vars`, `keychain`, `workbook`, `workload`, `workflow`; required = `apiVersion`, `kind`, `metadata`, `workflow`.
2. States explicitly that there is **no top-level `steps:`** — `workflow` is the step list — and adds this to Appendix F.
3. Step keys covered: `step`, `desc`, `spec`, `when`, `loop`, `tool`, `next`, `set`, `args`, `vars`; gated metadata (`expose.mcp`, `expose.agent`, `catalog.hot_reload`) mentioned with forward links.
4. Keychain section: credentials by alias, never inline; no default connection.
5. Every example validates against the schema (CI or documented manual check); quiz per section.
6. Meets [CH-ALL](#ch-all).

Sources: `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json); ai-meta agents/rules/no-default-connection.md

### CH-05

**Tools** · Badge **REAL** · Phase **P1** · Issue [#15](https://github.com/noetl/book/issues/15) · Specified

Files: `src/ch05-*.md`

Acceptance criteria:

1. Lists tool kinds from `dsl-manifest.json` (`enabled_tool_kinds`) at a named commit, marking gated kinds (`agent`, `mcp`) and their flags.
2. The ordered tool list: **one `task_sequence` command, one worker, one slot**, with its iteration cap — quiz question 'how many slots does this step hold?'.
3. Corrects the Python myth: the Python *platform* was retired; `python` remains a distributed-runtime kind (worker subprocess) and is not a local kind.
4. Results, references and size limits (event result context 100 KiB, command context 512 KiB, 2 MiB request body) with DEFAULT labels and env var names from the resource model.
5. Appendix F gains the task_sequence and Python entries.
6. Meets [CH-ALL](#ch-all).

Sources: `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json); noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json); `noetl/noetl` README ('What is in this repository')

### CH-06

**Control Flow** · Badge **REAL** · Phase **P1** · Issue [#16](https://github.com/noetl/book/issues/16) · Specified

Files: `src/ch06-*.md`

Acceptance criteria:

1. The four forms of `next` (name; list; list of `{step, when, args}`; router `{spec:{mode: exclusive|inclusive}, arcs:[...]}`) each with an example: a distributed example for all four (schema-validated), and local CI examples for the forms the local runtime implements (at CLI v6.4.0 it ignores the bare-name forms, which is itself asserted).
2. `when` guards (Jinja2): arc guards are evaluated after the source step completes; a step's own `when` is evaluated just before it is dispatched.
3. Both loop forms: `loop: {in, iterator, spec:{mode: sequential|parallel|cursor, max_in_flight}}` and back-edges; no server cap on iterations or back-edge repeats — the playbook guard is the only bound.
4. 6.5 is badged PARTIAL and states: `retry` is parsed but not applied; `loop.spec.max_in_flight` is parsed but not read; most kinds have no default timeout — each verified at a named commit.
5. Notes that local mode ignores `loop:` (forward link to Ch. 8).
6. Quiz per section including 'will this loop terminate?'; Appendix F gains retry / max_in_flight entries.
7. Meets [CH-ALL](#ch-all).

Sources: `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json); noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json); `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki

### CH-07

**Composition: Sub-Playbooks** · Badge **REAL** · Phase **P2** · Issue [#17](https://github.com/noetl/book/issues/17) · Specified

Files: `src/ch07-*.md`

Acceptance criteria:

1. `kind: playbook` creates a child execution with `parent_execution_id`.
2. Slot behaviour: holds the slot only for the start request, unless `return_result` (then polls every 2 s while holding a slot) — from the resource model `step_kinds`.
3. What a hop costs: MEASURED 9–15 s (2026-08) vs the ~3–5 s TARGET (NOT_YET_MEASURED), each labelled with source; heuristic 'inline a one-call child'.
4. Quiz per section.
5. Meets [CH-ALL](#ch-all).

Sources: noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json); ai-meta PR #556 docs/rfc/latency-reduction-plan.md

## Part III — The Three Runtimes

### CH-08

**The Local Runtime: noetl run** · Badge **REAL** · Phase **P2** · Issue [#18](https://github.com/noetl/book/issues/18) · Specified

Files: `src/ch08-*.md`

Acceptance criteria:

1. `noetl run <ref> -r local|distributed|auto` and its precedence (flag → context → default local), verified at a named CLI version.
2. Local kinds listed from `LOCAL_KINDS_FOR_MESSAGE` at that version (shell, http, playbook, duckdb, auth, sink, rhai, provider, agent, noop); **no `python`, no `postgres`**; the up-front refusal message quoted.
3. **`loop:` is parsed but not executed locally** — stated plainly, with the three working alternatives (back-edge + `when`, set-based DuckDB SQL, rhai), each with a runnable example in `examples/ch08/`.
4. Local event buffer and `noetl push`.
5. Quiz per section ('which of these runs locally?'); Appendix F gains the local-loop entry.
6. Meets [CH-ALL](#ch-all).

Sources: `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki; ai-meta docs: repos/docs/docs/reference/rust_local_execution.md:28 (⚠ says loop is preserved — TARGET, not code)

### CH-09

**The Daemon: noetl subscribe and noetl serve** · Badge **REAL** · Phase **P2** · Issue [#19](https://github.com/noetl/book/issues/19) · Specified

Files: `src/ch09-*.md`

Acceptance criteria:

1. `noetl subscribe`: a standalone `kind: Subscription` listener (NATS, Pub/Sub, Kafka), one local run per message, local disk spool, JSONL event trail; `--dispatch server`.
2. `noetl serve` / `subscribe --serve` serve MCP and agents; durable tasks via `--task-db` (with the CLI version that introduced it).
3. States it is not a general-purpose daemon and needs no Kubernetes or server.
4. Quiz per section.
5. Meets [CH-ALL](#ch-all).

Sources: `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki; `noetl/cli` src/subscribe/, cli wiki subscribe.md

### CH-10

**The Distributed Runtime** · Badge **REAL** · Phase **P3** · Issue [#21](https://github.com/noetl/book/issues/21) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch10-*.md`

Acceptance criteria:

1. Gateway (gatekeeper only) → server (orchestrate-core drive on the system pool) → EHDB command bus → pools claiming `commands.<pool>.>`.
2. Slot model and KEDA on `ehdb_feed_subject_lag` (not NATS), pool sizes DEPLOYED with a date.
3. 10.5 uses the first `noetl-trace` (T-05).
4. Meets [CH-ALL](#ch-all).

Sources: noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json); ai-meta agents/rules/execution-model.md (⚠ its KEDA/NATS line is stale); ai-meta wiki Home / Sessions-Log

### CH-11

**Choosing a Runtime** · Badge **REAL** · Phase **P2** · Issue [#20](https://github.com/noetl/book/issues/20) · Specified

Files: `src/ch11-00-choosing-a-runtime.md`

Acceptance criteria:

1. A comparison table across local / daemon / distributed: supported kinds, concurrency, durability, cost, what each refuses — every cell traceable to Ch. 8–10 or a named source.
2. Scenario quiz (5+ questions) mapping workloads to runtimes.
3. Meets [CH-ALL](#ch-all).

Sources: `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki; noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json); ai-meta agents/rules/execution-model.md (⚠ its KEDA/NATS line is stale)

### CH-12

**Project: Taking Your Playbook Distributed** · Badge **REAL** · Phase **P3** · Issue [#22](https://github.com/noetl/book/issues/22) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch12-00-project-distributed.md`

Acceptance criteria:

1. Ch. 2 playbook on kind with a parallel `loop:`, a `postgres` step and a sub-playbook.
2. Reader reads the event log; trace via T-05.
3. Meets [CH-ALL](#ch-all).

Sources: `noetl/ops` automation/development; `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki

## Part IV — EHDB

### CH-13

**EHDB: The Event Horizon Database** · Badge **REAL** · Phase **P4** · Issue [#23](https://github.com/noetl/book/issues/23) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch13-*.md`

Acceptance criteria:

1. NATS replacement dated (bus flip 2026-07-27, NATS deleted 2026-08-01); append log, bloom/floor, two buses.
2. 13.5 PARTIAL: lease live, fence enforce staged; 13.7 PARTIAL: chain store cannot serve yet.
3. Meets [CH-ALL](#ch-all).

Sources: `noetl/ehdb` README, docs/SCOPE.md, ehdb wiki; ai-meta docs/rfc/ehdb-*.md

### CH-14

**EHDB as the State Substrate** · Badge **TARGET** · Phase **P7** · Issue [#24](https://github.com/noetl/book/issues/24) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch14-*.md`

Acceptance criteria:

1. States what exists today first (embedded EHDB STS) then #332 and RFC #355 as TARGET.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta docs/rfc/ehdb-embedded-state.md; ai-meta PR #355

### CH-15

**ehgraph: A Graph Database for Topology** · Badge **PARTIAL** · Phase **P5** · Issue [#25](https://github.com/noetl/book/issues/25) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch15-*.md`

Acceptance criteria:

1. Stores no graph data in EHDB (say so); embedded in server since v3.156.x at `/ehgraph/<graph>`; TCK rate MEASURED with date.
2. Meets [CH-ALL](#ch-all).

Sources: `noetl/ehgraph` README

## Part V — Distribution

### CH-16

**The Distributed Playbook Catalog** · Badge **PARTIAL** · Phase **P5** · Issue [#26](https://github.com/noetl/book/issues/26) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch16-*.md`

Acceptance criteria:

1. Phases 1–3 + resolvers with release versions; every flag and its default (all off on the reference prod) named; gs/az untested stated.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta docs/rfc/distributed-playbook-catalog.md; ai-meta wiki Umbrella-Distributed-Playbook-Catalog

### CH-17

**Cross-Instance Execution: Run It on B** · Badge **PARTIAL** · Phase **P5** · Issue [#27](https://github.com/noetl/book/issues/27) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch17-*.md`

Acceptance criteria:

1. import vs delegate with versions; registry admits nobody on prod; TARGET gaps (push completion, cancel) listed.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta docs/rfc/distributed-playbook-catalog.md §12; ai-meta docs/rfc/interop-missing-tools-build-plan.md

## Part VI — Interop and Concurrency

### CH-18

**MCP and Agents** · Badge **REAL** · Phase **P5** · Issue [#28](https://github.com/noetl/book/issues/28) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch18-*.md`

Acceptance criteria:

1. kind:mcp / kind:agent with gates; playbook-as-MCP (`metadata.expose.mcp`) and playbook-as-agent; interop matrix (18.5 PARTIAL); agent limits 32 calls / 180 s.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta docs/rfc/interop-topology-and-ai-mcp-playbooks.md; noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json)

### CH-19

**Project: Expose a Playbook as an MCP Tool and Call It from an Agent** · Badge **REAL** · Phase **P5** · Issue [#29](https://github.com/noetl/book/issues/29) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch19-00-project-mcp-agent.md`

Acceptance criteria:

1. Local then distributed; examples in `examples/ch19/`.
2. Meets [CH-ALL](#ch-all).

Sources: `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki; ai-meta interop RFCs

### CH-20

**Coroutines and Structured Concurrency** · Badge **TARGET** · Phase **P7** · Issue [#30](https://github.com/noetl/book/issues/30) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch20-*.md`

Acceptance criteria:

1. 20.1 (concurrency today, REAL) may be written in P5; 20.2–20.5 describe RFC #554 as TARGET with all flags named off.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta docs/rfc/coroutines.md

## Part VII — Resources and Performance

### CH-21

**The Resource Model** · Badge **REAL** · Phase **P4** · Issue [#31](https://github.com/noetl/book/issues/31) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch21-*.md`

Acceptance criteria:

1. Every number with its label from `resource-model.json` at a named `as_of`; the 7 NOT_YET_MEASURED gaps listed verbatim.
2. Meets [CH-ALL](#ch-all).

Sources: noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json)

### CH-22

**Orchestration Overhead** · Badge **PARTIAL** · Phase **P4** · Issue [#32](https://github.com/noetl/book/issues/32) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch22-*.md`

Acceptance criteria:

1. ~0.95 s/step decomposition MEASURED (prod 2026-11-02, n=4); Postgres ~10–15 %; 22.3 ranked fixes TARGET (written in P7).
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta PR #556 docs/rfc/latency-reduction-plan.md; ai-meta issues #283, #557–#562; noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json)

### CH-23

**WASM at the Edge** · Badge **PARTIAL** · Phase **P6** · Issue [#33](https://github.com/noetl/book/issues/33) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch23-*.md`

Acceptance criteria:

1. Only stage 1 'embed + validate' is REAL; never 'compiled to Rust'; kuksin.us proof as one deployment; edge latency NOT_YET_MEASURED.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta PR #556 §2.5; ai-meta docs/rfc/distributed-playbook-catalog.md §7

### CH-24

**Project: Ship a Pure Playbook to the Edge** · Badge **PARTIAL** · Phase **P6** · Issue [#34](https://github.com/noetl/book/issues/34) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch24-00-project-edge.md`

Acceptance criteria:

1. Factor, compile, parity-check, deploy; needs T-06.
2. Meets [CH-ALL](#ch-all).

Sources: `noetl/server` plugins/playbook-wasm

## Part VIII — Applied

### CH-25

**Agent and Bot Fleets on NoETL** · Badge **PARTIAL** · Phase **P7** · Issue [#35](https://github.com/noetl/book/issues/35) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch25-*.md`

Acceptance criteria:

1. States NoETL cannot claim a per-bot security boundary today; numbers labelled (GIVEN/MEASURED/TARGET).
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta PR #556 docs/rfc/bot-fleets-vs-shared-account-vm.md

### CH-26

**Case Study: A Quantum-Readiness Orchestrator** · Badge **PARTIAL** · Phase **P7** · Issue [#36](https://github.com/noetl/book/issues/36) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch26-*.md`

Acceptance criteria:

1. Owner sign-off obtained before any detail from the private source repo is written.
2. Meets [CH-ALL](#ch-all).

Sources: private repo — owner

## Part IX — Operations

### CH-27

**Deployment Modes** · Badge **REAL** · Phase **P4** · Issue [#37](https://github.com/noetl/book/issues/37) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch27-*.md`

Acceptance criteria:

1. Kind first; GKE; deploy by digest with explicit rollback; no project IDs or internal hostnames.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta agents/rules/{deployment-validation,ops-deploy,apply-safety}.md

### CH-28

**Releases and Version Pinning** · Badge **REAL** · Phase **P4** · Issue [#38](https://github.com/noetl/book/issues/38) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch28-00-releases.md`

Acceptance criteria:

1. semantic-release rules; `chore:` releases nothing; tag vs Cargo.toml may disagree.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta agents/rules/release-versioning.md

### CH-29

**Rollout and Rollback Discipline** · Badge **REAL** · Phase **P4** · Issue [#39](https://github.com/noetl/book/issues/39) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch29-00-rollout-rollback.md`

Acceptance criteria:

1. Smoke before and after; one pool at a time; rollback by digest.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta wiki Deployment-Validation.md; ai-meta playbooks/

### CH-30

**Observability and Alerting** · Badge **REAL** · Phase **P4** · Issue [#40](https://github.com/noetl/book/issues/40) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch30-00-observability.md`

Acceptance criteria:

1. execution_id as trace key; alert policies as code; scrape coverage as a risk.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta agents/rules/observability.md; `noetl/ops` ci/monitoring/

### CH-31

**Credentials and Secrets** · Badge **REAL** · Phase **P4** · Issue [#41](https://github.com/noetl/book/issues/41) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch31-00-credentials.md`

Acceptance criteria:

1. Explicit aliases; keychain; never in worker env or the event log.
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta agents/rules/no-default-connection.md; ai-meta wiki Umbrella-Secrets-Wallet.md

### CH-32

**Representation Drift: Keeping What You Know True** · Badge **REAL** · Phase **P7** · Issue [#42](https://github.com/noetl/book/issues/42) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch32-00-representation-drift.md`

Acceptance criteria:

1. Worked examples chosen to be safe to publish (no internal identifiers).
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta agents/rules/representation-drift.md

## Appendices

### AP-A

**Appendix A: DSL Reference (generated)** · Badge **REAL** · Phase **P1** · Issue [#43](https://github.com/noetl/book/issues/43) · Specified

Files: `src/appendix-01-dsl-reference.md`

Acceptance criteria:

1. Generated by T-04 from `playbook.schema.json` at a pinned commit; no hand-written prose beyond a short intro.
2. Every key links back to the chapter that teaches it (Ch. 4–6).
3. Meets [CH-ALL](#ch-all).

Sources: `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json)

### AP-B

**Appendix B: Tool Kinds Reference (generated)** · Badge **REAL** · Phase **P1** · Issue [#44](https://github.com/noetl/book/issues/44) · Specified

Files: `src/appendix-02-tool-kinds.md`

Acceptance criteria:

1. Generated by T-04 from `dsl-manifest.json` + resource-model `step_kinds` (execution, holds_slot, timeout, measured) at a pinned commit.
2. Gated kinds show their flags; local availability column cross-checked against Ch. 8.
3. Meets [CH-ALL](#ch-all).

Sources: `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json); noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json)

### AP-C

**Appendix C: Feature Flags and Environment Variables (generated)** · Badge **REAL** · Phase **P4** · Issue [#48](https://github.com/noetl/book/issues/48) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/appendix-03-flags.md`

Acceptance criteria:

1. Generated by T-04.
2. Meets [CH-ALL](#ch-all).

Sources: `noetl/server` orchestrate-core/schema/ (playbook.schema.json, dsl-manifest.json, resource-model.json)

### AP-D

**Appendix D: The Resource Model, Annotated (generated)** · Badge **REAL** · Phase **P4** · Issue [#49](https://github.com/noetl/book/issues/49) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/appendix-04-resource-model.md`

Acceptance criteria:

1. Generated by T-04, with annotations linking to Ch. 21.
2. Meets [CH-ALL](#ch-all).

Sources: noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json)

### AP-E

**Appendix E: Status Ledger** · Badge **REAL** · Phase **P1** · Issue [#47](https://github.com/noetl/book/issues/47) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/appendix-05-status-ledger.md`

Acceptance criteria:

1. One row per page: badge, justifying source, last verified; updated by every chapter PR.
2. Meets [CH-ALL](#ch-all).

Sources: BOOK-PLAN §3

### AP-F

**Appendix F: Myths and Corrections (seed)** · Badge **REAL** · Phase **P1** · Issue [#45](https://github.com/noetl/book/issues/45) · Specified

Files: `src/appendix-06-myths.md`

Acceptance criteria:

1. Contains at least the 10 seed entries in BOOK-PLAN §5, each with a source (file + commit/release) and a link to the chapter that teaches the truth.
2. Each entry is phrased as Myth / Truth / Source / Chapter.
3. Meets [CH-ALL](#ch-all).

Sources: BOOK-PLAN §5 seed list

### AP-G

**Appendix G: Glossary** · Badge **REAL** · Phase **P1** · Issue [#50](https://github.com/noetl/book/issues/50) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/appendix-07-glossary.md`

Acceptance criteria:

1. Each term defined where a chapter introduces it; grows with every chapter PR.
2. Meets [CH-ALL](#ch-all).

Sources: chapters

### AP-H

**Appendix H + wiki Style Guide: how to write a quiz and record a trace** · Badge **REAL** · Phase **P0** · Issue [#46](https://github.com/noetl/book/issues/46) · Specified

Files: `src/appendix-08-contributing.md`

Acceptance criteria:

1. Appendix H links CONTRIBUTING; the wiki Style Guide gains 'how to write a quiz' (distractors from real misconceptions, explanation for every answer) and 'how to record a trace' (placeholder until T-05).
2. Meets [CH-ALL](#ch-all).

Sources: CONTRIBUTING.md; BOOK-PLAN §2.3


## Success Criteria *(mandatory)*

- **SC-001**: P0–P2 chapters (Part I, Part II, Ch. 8, 9, 11, front matter, Appendices A, B, F, H) are merged with all CH-ALL criteria met.
- **SC-002**: Zero merged pages carry a badge higher than their subject's verified status (audited quarterly via Appendix E).
- **SC-003**: 100 % of examples run in CI; 0 hand-maintained copies of schema content (Appendices A–D generated).
- **SC-004**: Every Appendix F myth is taught against in at least one quiz question.

## Assumptions

- The reference CLI and server versions are pinned per chapter and recorded in Appendix E. Prod facts are stamped, not assumed current.
- Quiz telemetry is **off** unless the owner decides otherwise ([#51](https://github.com/noetl/book/issues/51)).
- Hosting and license are pending ([#51](https://github.com/noetl/book/issues/51)) and do not block writing.
- The Ch. 26 source is private and blocked on owner sign-off ([#51](https://github.com/noetl/book/issues/51)).
