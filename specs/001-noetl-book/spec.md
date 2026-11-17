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

## Clarifications

### Session 2026-11-15

Answered by the authoring agent from code and public sources, under the owner's grant of autonomy (book#51); each answer cites what it was checked against.

- Q: At which releases are Ch. 10's REAL claims verified? → A: server v3.161.2 (the `tools/SERVER_SCHEMA_PIN` commit), worker v6.15.0, gateway v3.22.1. A later release is cited only where it changes a claim.
- Q: Where do Ch. 10's deployment numbers come from? → A: the DEPLOYED entries of the public resource model, with its `as_of` date. Committed `noetl/ops` manifests are not evidence of what runs: the resource model records that the committed system-pool ScaledObject is not on the cluster.
- Q: What may a T-05 trace be made from? → A: only a captured event log of one real execution on a stack running tagged releases, with internal identifiers scrubbed. No hand-written or synthetic logs.
- Q: Must T-05 fold in the browser with WASM? → A: Not in the first iteration. It folds at build time with the same orchestrate-core crate at the server pin; CI re-folds and fails if stale. That is the same reducer, so correctness is unchanged.
- Q: Where does Ch. 12 run, and how is it verified? → A: on kind built with `noetl/ops` dev automation on tagged release images; examples are schema-checked in CI and the author's run is recorded in the PR.
- Q: Is a resource-model figure enough to state a number in Ch. 21? → A: Yes, with its label, its `as_of` and the model's own source. Where the code at the pin says otherwise, the page reports both; the model is a representation, not the code.
- Q: Should Appendix C list every runtime flag? → A: Every flag the chapters cite, generated from `tools/flags-cited.json`, with a CI check that no chapter cites an unlisted one. Not every variable the binaries read.
- Q: Ch. 13's draft said the chain store "cannot serve yet" and the fence is "enforce staged". What does the evidence say? → A: The chain store serves on prod behind three default-off gates, armed per the dated record (2026-09-30 to 2026-10-09). For the fence, no dated public record states its prod mode; the worker v6.15.0 code records that enforce was not armed while the election started ~5.5 min late. The page says exactly that.
- Q: Ch. 30 asks for "execution_id as trace key". What actually carries it at v3.161.2? → A: the event log. `execution_id` is a server-side snowflake (`src/handlers/execute.rs:366-371`) and every event, command and read route (`GET /api/executions/{id}`) is keyed by it. There is no span exporter (no OpenTelemetry dependency); a W3C `trace` object, if a caller supplies one, is stored on `playbook_started` and inherited by child executions as data. The ai-meta observability rule is a rule for contributors, not evidence of what ships, so the page cites code for each claim.
- Q: Which alerting facts are REAL, and as of when? → A: what `noetl/ops` commits at a named commit (26 Cloud Monitoring policies at `3f63656`, 2026-11-02; the apply script; the GMP `Rules` path documented inert), plus the dated public record of what was live (23 committed == 23 live on 2026-10-16, ai-meta#471). Whether the three policies added after that date are live is not in a dated record; the page says so. No project ids, channel ids or addresses.
- Q: How is "scrape coverage as a risk" evidenced? → A: by the two dated selector defects fixed in `noetl/ops` `ceb49bc` (2026-10-04): the server PodMonitoring selected a workload with no pods for 25 days, and an enumerated worker selector missed two pods. The lesson is the selector shape (select by a stable label that must exist, not by enumerated names).
- Q: Ch. 28's sources are a contributor rule (ai-meta `release-versioning.md`). Is that evidence? → A: No. The page cites the workflows and `.releaserc.json` at `origin/main` of each repo (read 2026-11-15), the semantic-release run logs, and the commit-analyzer's default rules. Where the rule disagrees with them, the page follows the pipeline: semantic-release reads every commit since the last tag, not the merge subject; `perf:` and `revert:` also release a patch; and on server, worker and tools the bot no longer commits the bump, so `Cargo.toml` is a floor below the tag.
- Q: Is "`chore:` releases nothing" the whole story? → A: For semantic-release, yes, and silently. But `release.yml` can be dispatched by hand with a version: server v3.153.0 (2026-11-08) was published that way after semantic-release found no relevant changes in four `chore:` PRs (both runs' logs). The page states the escape hatch and that it bypasses the commit-type check.
- Q: Ch. 27's sources are contributor rules. Which kind path does the page teach? → A: the one `noetl/ops` maintains for the current topology, `automation/ehdb/ehdb_platform.yaml` (`plan`/`converge`/`status`/`verify`/`teardown`, `profile=kind|prod` as a guard), read at ops `6c55cbe`. The older `automation/development/noetl.yaml` that the rules name still builds the legacy Python image and applies NATS manifests (last changed 2026-05-23); the page says it is stale rather than teaching it. Facts the book did not run are labelled as read, not run.
- Q: Can Ch. 27/29 describe production at all without reading it? → A: Only as the committed manifests declare it (at a named ops commit) and as dated public records describe it, and the page says which. The manifests are "shape-only" by design and are known to differ from live (ai-meta#267, open), so they are not evidence of what runs.
- Q: Which rollout facts are REAL for Ch. 29? → A: the procedure as written and executed in ai-meta `playbooks/` (516, 517, 460, 257) at a named commit, and the dated outcomes in the public record (#504, #511, #517, the wiki Sessions-Log). Smoke specifics that name private hosts or products are described generically.
- Q: The wallet umbrella calls the secrets wallet "feature-complete". Can Ch. 31 say so? → A: No. Each feature is stated at server v3.161.2 / worker v6.15.0 with its code default. Several ship off (sealed delivery, mTLS, residency, KMS), the credentials route gate defaults to shadow, and the secret-audit table has no writer at all; the page says each plainly. Ch. 4.4 already covers aliases and templates, so Ch. 31 covers storage, delivery, the event-log guarantee, worker environment and bootstrap secrets.
- Q: How does Ch. 31 treat open security issues about the production deployment? → A: It gives operators the code default and the setting that closes it, and does not describe the state of any deployment's secrets. It names no secret, store path, project or alias.

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

### Session 2026-11-17

The owner asked for a worked-examples track built from real ecosystem projects (book#99). Answers by the authoring agent, each checked as cited.

- Q: Where do the case studies go? → A: A new **Part X — In Practice: Case Studies** after Part IX (Ch. 33–36). After, because two of them (auth, platform) build on Ch. 10 and Ch. 27–31. Concept chapters link to the matching case-study section ("In practice: …") only when that section is written, so no link points at a stub. The placement map is BOOK-PLAN §2.8.
- Q: Is a case study a tutorial? → A: No. The project chapters (2, 12, 19, 24) are things the reader builds. A case study reads a real project's playbooks at a named commit and explains why each one is shaped as it is, tying every defensive pattern to the runtime rule that forces it, verified in code. Readers do not need the project's credentials or data to follow it.
- Q: What may be published from those repos? → A: Only what the public repos contain, and less: no project ids, real user or document ids, execution ids, hostnames, or third-party data, even where a source file carries them. For `noetl/quantum`: project level only, no competition data, scores, circuits or third-party hub content. All four repos were confirmed public without credentials on 2026-11-17.
- Q: How does Ch. 35 (public VQCC project) relate to Ch. 26 (private quantum-readiness source, #36)? → A: They are different projects. Ch. 35 is written from a public repo and needs no sign-off. Whether Ch. 26 stays, or #51 Q4 is answered by swapping it for Ch. 35, is the owner's decision; until then both remain in the outline.
- Q: Are the auth features the owner listed shipped? → A: Partly. At gateway v3.22.1 the two-role, deny-by-default model with a user-playbook allowlist and execution ownership is REAL (`src/authorization.rs`), and sign-in is validated by a playbook unless `NOETL_AUTH_SYNC` is on. A `grant_role` playbook, verified-email role inheritance, and admin-only rules on register / catalog get beyond the gateway's deny-by-default were not found on `main` of server, gateway, e2e or ops on 2026-11-17 (only on branches). Ch. 34 is PARTIAL and labels them until a tagged release carries them.
- Q: The quantum repo says its playbooks were checked on "NoETL 5.3.2". Which binary is that? → A: Unresolved. `noetl/noetl` has a `pypi-v5.3.2` tag (2026-10-17) whose `pyproject.toml` says it is not a distribution; the CLI the book pins is v6.4.1. Ch. 35 resolves this before any claim depends on the runtime version; sample 35.2 depends only on the server's validate API.
- Q: Does the public validate endpoint behave as the server code says? → A: Mostly. On 2026-11-17 `https://noetl.ai/api/dsl/version` reported server 3.165.1, and `POST /api/dsl/validate` returned the documented fields. But a mismatched `x-noetl-schema-digest` header produced no `schema_drift` field, although the server code adds one (v3.161.2 and v3.165.1, `src/handlers/dsl.rs`); something in front of the server drops the header. 35.2 says so and teaches comparing digests on the client.

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

**mdbook-noetl-trace: event-log step-through visualizer** · Badge **TARGET** · Phase **P3** · Issue [#7](https://github.com/noetl/book/issues/7) · Specified (clarified 2026-11-15)

Files: `tools/trace-fold/`, `tools/mdbook-noetl-trace.py`, `traces/`

Acceptance criteria:

1. Folds a recorded event log with **orchestrate-core's own reducer** (`WorkflowState::apply_event`) at the server commit in `tools/SERVER_SCHEMA_PIN`, so the visualization cannot disagree with the engine. The book never computes state itself.
2. First iteration folds **at build time** (native) and commits one state per event to `traces/<name>/states.json`; CI re-folds and fails if the committed states are stale. An in-browser WASM fold is a later iteration.
3. A trace is a **captured** event log of one real execution on a stack running tagged releases (prod, or kind on release images). It records where, when, and which releases. Hand-written or synthetic logs are refused. Identifiers that are internal (hostnames, pod names, project ids) are scrubbed, and CI checks the scrub does not change any folded digest.
4. A `{{#trace …}}` directive renders a step-through: the event at each position and the folded state (steps pending / running / done, loop counters, context), with keyboard and button navigation and a no-JS fallback table.
5. `mdbook build` and linkcheck pass.

Sources: BOOK-PLAN §2.5, §4; server `orchestrate-core/src/state.rs`

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
3. Two catalogs: internal (NoETL's own objects, `/api/catalog/*`) vs business data (external stores, read by steps). The internal catalog's storage is badged honestly: **EHDB-only is the target** (TARGET); at server v3.161.2 it is Postgres `noetl.catalog` by default with an EHDB shadow log and a staged EHDB read path (`NOETL_CATALOG_READ_SOURCE`, default `postgres`), so the storage section is PARTIAL until EHDB serving is the default. *(Refined 2026-11-15, book#51.)*
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

**The Distributed Runtime** · Badge **REAL** · Phase **P3** · Issue [#21](https://github.com/noetl/book/issues/21) · Specified (clarified 2026-11-15)

Files: `src/ch10-*.md`

Acceptance criteria:

1. The path of a request, verified at server v3.161.2, worker v6.15.0 and gateway v3.22.1: the **gateway** authenticates, authorizes and proxies (and streams results back over SSE; it keeps session state in EHDB KV; by default it validates sessions by running an auth playbook); the **server** writes `playbook_started` and builds the first commands itself, then each later drive pass runs as the `__orchestrate__` WASM command on the **system** pool (`NOETL_ORCHESTRATE_PLUGIN_DRIVE`, default true); commands travel on the **EHDB command bus** hosted by the `cmdbus-writer`; workers claim `commands.<pool>.>`. The pool is chosen **per execution** (request override, else the playbook path prefix, else `shared`); there is no step-level pool field.
2. The slot model (`WORKER_MAX_CONCURRENT`, default 4; capacity = replicas × slots) and KEDA on `ehdb_feed_subject_lag` (not NATS). Pool sizes are the **DEPLOYED** values of the public resource model (`noetl.ai/dsl/resource-model.json`) with its `as_of` date, never committed manifests alone.
3. What happens when a worker dies mid-command at default flags (the bus is acked at claim; there is no redelivery; the sweeps that end such an execution are off by default).
4. 10.5 steps through a **captured** T-05 trace. Until one exists, 10.5 stays a stub and this issue stays open; 10.0–10.4 may land first.
5. Meets [CH-ALL](#ch-all).

Sources: server, worker and gateway at the tags above; noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json); ai-meta agents/rules/execution-model.md (⚠ its KEDA/NATS line is stale)

### CH-11

**Choosing a Runtime** · Badge **REAL** · Phase **P2** · Issue [#20](https://github.com/noetl/book/issues/20) · Specified

Files: `src/ch11-00-choosing-a-runtime.md`

Acceptance criteria:

1. A comparison table across local / daemon / distributed: supported kinds, concurrency, durability, cost, what each refuses — every cell traceable to Ch. 8–10 or a named source.
2. Scenario quiz (5+ questions) mapping workloads to runtimes.
3. Meets [CH-ALL](#ch-all).

Sources: `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki; noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json); ai-meta agents/rules/execution-model.md (⚠ its KEDA/NATS line is stale)

### CH-12

**Project: Taking Your Playbook Distributed** · Badge **REAL** · Phase **P3** · Issue [#22](https://github.com/noetl/book/issues/22) · Specified (clarified 2026-11-15)

Files: `src/ch12-00-project-distributed.md`, `examples/ch12/`

Acceptance criteria:

1. The Ch. 2 playbook, ported to the distributed runtime (`set:` for the counter, `{{ step.field }}` references), plus a parallel `loop:`, a `postgres` step and a sub-playbook (`kind: playbook`, `return_result: true`), run on a **kind** cluster built with `noetl/ops` dev automation on **tagged release images**. The page names the releases and the date of the author's run.
2. Every example in `examples/ch12/` is `RUNTIME=distributed` and passes the schema check in CI; the author's run (command, releases, terminal status) is recorded in the PR.
3. The reader reads the execution's event log (`noetl` CLI or the server API) and steps through it with a T-05 trace captured from the author's run.
4. "What changed and why" lists every change from the Ch. 2 version and why the local runtime could not do it (cross-referenced to the Ch. 8.1 table).
5. Meets [CH-ALL](#ch-all).

Blocked until a release-image stack and T-05 are available.

Sources: `noetl/ops` automation/development; `noetl/cli` src/playbook_runner.rs, executor/src/playbook.rs, README, cli wiki

## Part IV — EHDB

### CH-13

**EHDB: The Event Horizon Database** · Badge **REAL** · Phase **P4** · Issue [#23](https://github.com/noetl/book/issues/23) · Specified (clarified 2026-11-15)

Files: `src/ch13-*.md`

Acceptance criteria:

1. Code facts verified at **ehdb v0.15.1** (the version server v3.161.2 and worker v6.15.0 pin); deployment facts only from a dated public record (ai-meta wiki Sessions-Log / Home, issues), each with its date. The NATS replacement is dated: bus flip 2026-07-27, NATS deleted 2026-08-01; the page also states that the transport RFC had recommended keeping NATS.
2. The append log (parts, the active part, sealing on 8 MiB / 1024 records / optional age, the manifest, fsync per append or group commit), blooms and the prune floor (scheme 2, floor-exact), and the two buses hosted by the `cmdbus-writer`.
3. 13.5 **REAL** (was PARTIAL until 2026-11-16): the lease is the code's election (15 s lease, 5 s renew, ~21 s failover) and was held on prod (epoch 29, 2026-11-04); the fence runs in **enforce**, armed on both buses, per the dated read of 2026-11-16 (ai-meta wiki Umbrella-EHDB-Primary-Serve); the worker v6.15.0 "not armed" note is presented as code history.
4. 13.6 **PARTIAL**: sealed-part N-way copies exist; tail replication (B3) is server-only and flag-gated; the bus stores on the writer are single-copy on one volume.
5. 13.7 **PARTIAL**: the chain store **serves** on prod behind three default-off gates (armed 2026-09-30, disarmed and re-armed 2026-10-06, still armed 2026-10-09 per the public record); the open comparator issue (ai-meta#360) is stated.
6. Where ehdb's own docs disagree with its code at v0.15.1, the page follows the code and says so.
7. Meets [CH-ALL](#ch-all).

Sources: `noetl/ehdb` v0.15.1 README, docs/SCOPE.md, docs/spec, crates; ai-meta docs/rfc/ehdb-*.md, nats-vs-ehdb-transport-boundary.md; ai-meta wiki Sessions-Log, Home

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

**The Resource Model** · Badge **REAL** · Phase **P4** · Issue [#31](https://github.com/noetl/book/issues/31) · Specified (clarified 2026-11-15)

Files: `src/ch21-*.md`

Acceptance criteria:

1. The source is `resource-model.json` at the server pin (`as_of` stated on every page). Every number is quoted with its label; none appears without one.
2. Teaches how to use the file (labels, per-kind costs, limits, slots, estimating), and links to Appendix D for the full listing instead of reprinting it.
3. Where the model disagrees with the code at the pin, or with itself, the page says so and cites both.
4. 21.5 works one estimate end to end with the model's GUIDANCE rule, labelled GUIDANCE, and says what would have to be measured to check it.
5. 21.6 lists the NOT_YET_MEASURED gaps verbatim (7 at `as_of` 2026-11-11).
6. Meets [CH-ALL](#ch-all).

Sources: noetl.ai/dsl/resource-model.json (= server orchestrate-core/schema/resource-model.json); worker v6.15.0 and tools v4.6.0 for code checks

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

**Deployment Modes** · Badge **REAL** · Phase **P4** · Issue [#37](https://github.com/noetl/book/issues/37) · Specified (clarified 2026-11-15)

Files: `src/ch27-*.md`

Acceptance criteria:

1. Facts from `noetl/ops` at `6c55cbe`, ai-meta `playbooks/` at a named commit, and dated public records; no project ids, registry paths with project ids, cluster contexts or hostnames.
2. 27.1 kind first: `ehdb_platform.yaml` with `profile=kind` and its guard; `ci/kind/config.yaml`; the stale `development/noetl.yaml` named as stale.
3. 27.2 GKE: the topology the manifests declare (server StatefulSet of 1, retired Deployment at 0, three worker Deployments, the writer StatefulSet, the gateway), Autopilot, images from the release pipeline; shape-only manifests and why committed ≠ live (#267, the system-pool ScaledObject).
4. 27.3 deploy by digest: image-only patch of a named container, server-side dry-run with a whole-object diff, the digest ledger and its rollback row, verify by `*_build_info`; the 2026-09-08 manifest-apply outage (~55 min).
5. Meets [CH-ALL](#ch-all).

Sources: `noetl/ops` automation/ehdb/, ci/kind/, ci/manifests/noetl/ (incl. ledger/), automation/development/noetl.yaml; ai-meta playbooks/257-*, 460-*; ai-meta#267, #323; ai-meta wiki Sessions-Log (2026-09-08); ai-meta agents/rules (checked, not trusted)

### CH-28

**Releases and Version Pinning** · Badge **REAL** · Phase **P4** · Issue [#38](https://github.com/noetl/book/issues/38) · Specified (clarified 2026-11-15)

Files: `src/ch28-00-releases.md`

Acceptance criteria:

1. Pipeline facts from each repo's `.github/workflows/semantic-release.yml`, `release.yml` and `.releaserc.json` at `origin/main` (read 2026-11-15), run logs, and `@semantic-release/commit-analyzer`'s default release rules.
2. The commit-type table (`feat` minor, `fix`/`perf`/`revert` patch, breaking major, anything else nothing and silently), and that every commit since the last tag is analysed.
3. The tag is the version: where `Cargo.toml` is a floor (server, worker, tools) and where the bot still commits it (CLI, gateway); the build stamps the tag's version into the binary (`*_build_info`).
4. Never hand-edit the version: the 2026-08-03 regression (ai-meta#224). The manual-dispatch escape hatch and its one dated use (server v3.153.0).
5. A commit type is a semver claim nothing checks (ai-meta#330, open). How the book pins versions (`examples/NOETL_CLI_VERSION`, `tools/SERVER_SCHEMA_PIN`).
6. Meets [CH-ALL](#ch-all).

Sources: noetl/{server,worker,tools,gateway,cli} workflows and `.releaserc.json`; semantic-release run logs; ai-meta#224, #330; ai-meta agents/rules/release-versioning.md (checked, not trusted)

### CH-29

**Rollout and Rollback Discipline** · Badge **REAL** · Phase **P4** · Issue [#39](https://github.com/noetl/book/issues/39) · Specified (clarified 2026-11-15)

Files: `src/ch29-00-rollout-rollback.md`

Acceptance criteria:

1. Smoke before and after every roll, regression ⇒ roll back: what the smoke exercises (described without private hosts), and that it checks it reached the intended cluster.
2. One pool at a time: the 2026-11-03 system-pool stall (~7–10 min of no-op drives while a fresh pod replays the feed; readiness says nothing); worker SIGTERM drain (v6.11.3, grace 180 s).
3. Rollback by digest, recorded before the roll; at least two dated real rollbacks or holds with their reason.
4. Ordering for multi-component changes: readers before writers, and the rollback floor that moves once writers arm (#517, 2026-11-06/07).
5. Dated restart costs (writer failover ~21 s; the lost gateway owner record, #523).
6. Meets [CH-ALL](#ch-all).

Sources: ai-meta playbooks/516-*, 517-*, 460-*, 257-*; ai-meta#504, #511, #517, #523, #202, #203; ai-meta wiki Sessions-Log

### CH-30

**Observability and Alerting** · Badge **REAL** · Phase **P4** · Issue [#40](https://github.com/noetl/book/issues/40) · Specified (clarified 2026-11-15)

Files: `src/ch30-00-observability.md`

Acceptance criteria:

1. Code facts verified at server **v3.161.2**, worker **v6.15.0**, gateway **v3.22.1**; alerting facts at `noetl/ops` commit `3f63656` plus the dated public record (ai-meta#238, #471), each with its date.
2. `execution_id` as the trace key: where it is generated, what is keyed by it, how to read one execution's events; the W3C `trace` object as an optional external join; no span exporter at these releases (said plainly, not implied).
3. The three metric surfaces (`/metrics` on the server's HTTP port, the worker's `:9090`, the gateway's `/metrics`), with metric names quoted only when found in code.
4. Alert policies as code: the file, the manual idempotent apply that never deletes, the two alerting paths (only one delivers), the `duration` default trap, and that nothing syncs file and live (ai-meta#471, open).
5. Scrape coverage as a risk, from the 2026-10-04 selector fix.
6. No private identifiers (project ids, channel ids, addresses, hostnames).
7. Meets [CH-ALL](#ch-all).

Sources: server v3.161.2, worker v6.15.0, gateway v3.22.1; `noetl/ops` `ci/monitoring/`, `ci/manifests/noetl/gmp/`; ai-meta#238, #471; ai-meta agents/rules/observability.md

### CH-31

**Credentials and Secrets** · Badge **REAL** · Phase **P4** · Issue [#41](https://github.com/noetl/book/issues/41) · Specified (clarified 2026-11-15)

Files: `src/ch31-00-credentials.md`

Acceptance criteria:

1. Code facts at server **v3.161.2** and worker **v6.15.0**; manifest facts at `noetl/ops` `6c55cbe`; dated facts from the public record.
2. Storage: envelope encryption under a KEK, fail-closed without `NOETL_ENCRYPTION_KEY`, the insecure escape hatch, optional Cloud KMS.
3. Delivery to the worker: the `include_data` fetch, the route gate and its shadow default, sealed delivery (opt-in, `auth:` path only), mTLS (opt-in).
4. Never in the event log: deferred `keychain.*` rendering, the drive-command guard, result scrubbing and its limits.
5. Never in worker env: a convention, with the `NOETL_KEYCHAIN_ENV_VARS` bridge stated; bootstrap secrets as CSI-mounted files and why they cannot live in the wallet.
6. What ships but does nothing at defaults, named plainly (the audit table has no writer).
7. Meets [CH-ALL](#ch-all).

Sources: server v3.161.2 `src/crypto/`, `src/services/credential.rs`, `src/auth_gate.rs`, `src/secrets/`; worker v6.15.0 `src/executor/auth_alias.rs`, `src/client/`, `src/scrub.rs`; `noetl/ops` `ci/manifests/noetl/`; ai-meta wiki Umbrella-Secrets-Wallet (checked, not trusted)

### CH-32

**Representation Drift: Keeping What You Know True** · Badge **REAL** · Phase **P7** · Issue [#42](https://github.com/noetl/book/issues/42) · Draft (stub; refine with /speckit-clarify before starting)

Files: `src/ch32-00-representation-drift.md`

Acceptance criteria:

1. Worked examples chosen to be safe to publish (no internal identifiers).
2. Meets [CH-ALL](#ch-all).

Sources: ai-meta agents/rules/representation-drift.md

## Part X — In Practice: Case Studies

Real projects from the NoETL ecosystem, read at a named commit. Each chapter explains why the project's playbooks are shaped as they are and points back to the concept chapter that states each rule. Placement map: BOOK-PLAN §2.8.

### CH-33

**Case Study: The Travel Playbooks** · Badge **REAL** · Phase **P5** · Issue [#95](https://github.com/noetl/book/issues/95) · Outlined 2026-11-17 (book#99); 33.2 written

Files: `src/ch33-*.md`

Acceptance criteria:

1. Facts from `noetl/travel` at a named commit (outline: `cd210d7`) and the server, worker and tools releases that run them; no project ids, real user or document ids, execution ids or hostnames, even where the source files carry them.
2. 33.1 the contract shape: the SPA posts its own object, the playbook persists it and returns a render-ready payload; the gateway allowlist that lets a regular user start these playbooks (forward to Ch. 34).
3. 33.2 the profile flow: validate → (read | save → read back) → suggestions; why `merge: true`, why read-after-write, why suggestions never fail the save, and the arc-shape rules (first match wins; a losing sibling is skipped and is not dispatched again; a python step sees only its `input:` names), each verified in code.
4. 33.3 provider calls (HotelBeds, Duffel, Places): a child playbook per provider vs inlining, the hop cost (cite Ch. 7.2, not new numbers), and the drift a second copy creates.
5. 33.4 the itinerary planner: state across turns and threads; 33.5 the `qa/regression` suite as a test harness for a playbook family.
6. Meets [CH-ALL](#ch-all).

Sources: `noetl/travel` playbooks/, qa/regression/; server orchestrate-core (`orchestrator.rs`, `state.rs`); tools `src/tools/python.rs`; gateway `src/authorization.rs`

### CH-34

**Case Study: Authentication and Authorization** · Badge **PARTIAL** · Phase **P5** · Issue [#96](https://github.com/noetl/book/issues/96) · Outlined 2026-11-17 (book#99)

Files: `src/ch34-*.md`

Acceptance criteria:

1. REAL at gateway v3.22.1: two roles (`admin`, regular user), deny by default, the user-playbook allowlist (`GATEWAY_USER_PLAYBOOKS`), execution ownership, guest mode; sign-in validated by a playbook unless `NOETL_AUTH_SYNC`.
2. Labelled as in flight until a tagged release carries them: role grants (`grant_role`), verified-email role inheritance, admin-only register / catalog get beyond what deny-by-default already implies (see Clarifications 2026-11-17).
3. Builds on Ch. 10.1 and Ch. 31 without repeating them; no tenant, client or user identifiers.
4. Meets [CH-ALL](#ch-all).

Sources: gateway `src/authorization.rs`, `src/auth/`; e2e `fixtures/playbooks/api_integration/auth0/`; ops and e2e "two roles only" (2026-10-16)

### CH-35

**Case Study: A Quantum Compilation Pipeline on the Local Runtime** · Badge **REAL** · Phase **P5** · Issue [#97](https://github.com/noetl/book/issues/97) · Outlined 2026-11-17 (book#99); 35.2 written

Files: `src/ch35-*.md`

Acceptance criteria:

1. Project level only: `noetl/quantum` at a named commit (outline: `9208fa2`). No competition data, scores, circuits or third-party hub content.
2. 35.1 the pipeline and its honest defaults (no data → no circuit, `leaderboard_score: null`); 35.2 validating against the public DSL API with a pinned digest, and why the local fallback never counts as acceptance; 35.3 long-running compute under wall-clock and transform budgets; 35.4 `kind: shell` as the local runtime's escape hatch.
3. The "NoETL 5.3.2" runtime is identified before a claim depends on it (Clarifications 2026-11-17).
4. Meets [CH-ALL](#ch-all).

Sources: `noetl/quantum` playbooks/, vqcc/dsl_validate.py, scripts/validate_playbooks.py, docs/; server `src/handlers/dsl.rs`; the public endpoint, read with a date

### CH-36

**Case Study: Standing Up the Platform** · Badge **PARTIAL** · Phase **P5** · Issue [#98](https://github.com/noetl/book/issues/98) · Outlined 2026-11-17 (book#99)

Files: `src/ch36-*.md`

Acceptance criteria:

1. What `noetl/ops` commits at a named commit: the fresh-stack provisioning playbook (itself a NoETL playbook on the local runtime), Cloud Build image definitions, KEDA ScaledObjects, Secrets Store CSI classes, the EHDB platform playbook.
2. Says which of those match the current topology and which are stale, and that committed is not live (ai-meta#267).
3. No project ids, registry paths with project ids, cluster names, contexts or hostnames. Builds on Ch. 10.4 and 27–31 without repeating them.
4. Meets [CH-ALL](#ch-all).

Sources: `noetl/ops` automation/gcp_gke/, automation/ehdb/, ci/manifests/keda/, ci/manifests/noetl/; ai-meta dated public record

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

**Appendix C: Feature Flags and Environment Variables (generated)** · Badge **REAL** · Phase **P4** · Issue [#48](https://github.com/noetl/book/issues/48) · Specified (clarified 2026-11-15)

Files: `src/appendix-03-flags.md`, `tools/flags-cited.json`

Acceptance criteria:

1. The DSL-artifact flags are generated by T-04 (as now).
2. A second generated table lists every runtime flag the chapters cite (`NOETL_*`, `WORKER_*`, `GATEWAY_*`): variable, read by, code default, source at a named release, and the sections that cite it, from `tools/flags-cited.json`.
3. CI fails if a chapter names such a variable that is not in either table.
4. Meets [CH-ALL](#ch-all).

Sources: `noetl/server` orchestrate-core/schema/ (dsl-manifest.json, resource-model.json); server, worker and gateway source at the releases the chapters cite

### AP-D

**Appendix D: The Resource Model, Annotated (generated)** · Badge **REAL** · Phase **P4** · Issue [#49](https://github.com/noetl/book/issues/49) · Specified (clarified 2026-11-15)

Files: `src/appendix-04-resource-model.md`

Acceptance criteria:

1. Generated by T-04 at the server pin, every figure with its label.
2. Each section links to the Ch. 21 section that explains it.
3. Meets [CH-ALL](#ch-all).

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
