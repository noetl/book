# Tasks: The NoETL Book

**Input**: `specs/001-noetl-book/spec.md` · **Order**: `docs/ROADMAP.md` phases

Each task is one GitHub issue, and the issue tracks its status. A box here is ticked only when the issue is closed by a merged PR. `[P]` means it can run in parallel with other tasks in the same phase.

## Phase P0

- [ ] AP-H [P] Appendix H + wiki Style Guide: how to write a quiz and record a trace — [#46](https://github.com/noetl/book/issues/46) · `src/appendix-08-contributing.md`
- [ ] T-01 CI: mdbook build + linkcheck on every PR — [#3](https://github.com/noetl/book/issues/3) · `.github/workflows/`, `book.toml`
- [ ] T-02 Example-playbook runner in CI (examples/ → noetl run, output diffed) — [#4](https://github.com/noetl/book/issues/4) · `examples/`, `.github/workflows/`

## Phase P1

- [ ] AP-A [P] Appendix A: DSL Reference (generated) — [#43](https://github.com/noetl/book/issues/43) · `src/appendix-01-dsl-reference.md`
- [ ] AP-B [P] Appendix B: Tool Kinds Reference (generated) — [#44](https://github.com/noetl/book/issues/44) · `src/appendix-02-tool-kinds.md`
- [ ] AP-E [P] Appendix E: Status Ledger — [#47](https://github.com/noetl/book/issues/47) · `src/appendix-05-status-ledger.md`
- [ ] AP-F [P] Appendix F: Myths and Corrections (seed) — [#45](https://github.com/noetl/book/issues/45) · `src/appendix-06-myths.md`
- [ ] AP-G [P] Appendix G: Glossary — [#50](https://github.com/noetl/book/issues/50) · `src/appendix-07-glossary.md`
- [ ] CH-03 [P] What NoETL Is — [#13](https://github.com/noetl/book/issues/13) · `src/ch03-*.md`
- [ ] CH-04 [P] Anatomy of a Playbook — [#14](https://github.com/noetl/book/issues/14) · `src/ch04-*.md`
- [ ] CH-05 [P] Tools — [#15](https://github.com/noetl/book/issues/15) · `src/ch05-*.md`
- [ ] CH-06 [P] Control Flow — [#16](https://github.com/noetl/book/issues/16) · `src/ch06-*.md`
- [ ] FM-01 [P] How to Read This Book — [#9](https://github.com/noetl/book/issues/9) · `src/ch00-01-how-to-read.md`
- [ ] T-03 Enable mdbook-quiz and mdbook-admonish with a first quiz — [#5](https://github.com/noetl/book/issues/5) · `book.toml`, `quizzes/`, `.github/workflows/`
- [ ] T-04 Generate Appendices A–D from the server schema files — [#6](https://github.com/noetl/book/issues/6) · `tools/`, `src/appendix-01-dsl-reference.md`, `src/appendix-02-tool-kinds.md`, `src/appendix-03-flags.md`, `src/appendix-04-resource-model.md`

## Phase P2

- [ ] CH-01 [P] Getting Started — [#11](https://github.com/noetl/book/issues/11) · `src/ch01-*.md`
- [ ] CH-02 [P] Project: Fetch, Transform, Store — Your First Real Playbook — [#12](https://github.com/noetl/book/issues/12) · `src/ch02-00-project-first-playbook.md`
- [ ] CH-07 [P] Composition: Sub-Playbooks — [#17](https://github.com/noetl/book/issues/17) · `src/ch07-*.md`
- [ ] CH-08 [P] The Local Runtime: noetl run — [#18](https://github.com/noetl/book/issues/18) · `src/ch08-*.md`
- [ ] CH-09 [P] The Daemon: noetl subscribe and noetl serve — [#19](https://github.com/noetl/book/issues/19) · `src/ch09-*.md`
- [ ] CH-11 [P] Choosing a Runtime — [#20](https://github.com/noetl/book/issues/20) · `src/ch11-00-choosing-a-runtime.md`
- [ ] FM-02 [P] Introduction — [#10](https://github.com/noetl/book/issues/10) · `src/ch00-00-introduction.md`

## Phase P3

- [ ] CH-10 [P] The Distributed Runtime — [#21](https://github.com/noetl/book/issues/21) · `src/ch10-*.md`
- [ ] CH-12 [P] Project: Taking Your Playbook Distributed — [#22](https://github.com/noetl/book/issues/22) · `src/ch12-00-project-distributed.md`
- [ ] T-05 mdbook-noetl-trace: event-log step-through visualizer — [#7](https://github.com/noetl/book/issues/7) · `tools/`, `traces/`

## Phase P4

- [ ] AP-C [P] Appendix C: Feature Flags and Environment Variables (generated) — [#48](https://github.com/noetl/book/issues/48) · `src/appendix-03-flags.md`
- [ ] AP-D [P] Appendix D: The Resource Model, Annotated (generated) — [#49](https://github.com/noetl/book/issues/49) · `src/appendix-04-resource-model.md`
- [ ] CH-13 [P] EHDB: The Event Horizon Database — [#23](https://github.com/noetl/book/issues/23) · `src/ch13-*.md`
- [ ] CH-21 [P] The Resource Model — [#31](https://github.com/noetl/book/issues/31) · `src/ch21-*.md`
- [ ] CH-22 [P] Orchestration Overhead — [#32](https://github.com/noetl/book/issues/32) · `src/ch22-*.md`
- [ ] CH-27 [P] Deployment Modes — [#37](https://github.com/noetl/book/issues/37) · `src/ch27-*.md`
- [ ] CH-28 [P] Releases and Version Pinning — [#38](https://github.com/noetl/book/issues/38) · `src/ch28-00-releases.md`
- [ ] CH-29 [P] Rollout and Rollback Discipline — [#39](https://github.com/noetl/book/issues/39) · `src/ch29-00-rollout-rollback.md`
- [ ] CH-30 [P] Observability and Alerting — [#40](https://github.com/noetl/book/issues/40) · `src/ch30-00-observability.md`
- [ ] CH-31 [P] Credentials and Secrets — [#41](https://github.com/noetl/book/issues/41) · `src/ch31-00-credentials.md`

## Phase P5

- [ ] CH-15 [P] ehgraph: A Graph Database for Topology — [#25](https://github.com/noetl/book/issues/25) · `src/ch15-*.md`
- [ ] CH-16 [P] The Distributed Playbook Catalog — [#26](https://github.com/noetl/book/issues/26) · `src/ch16-*.md`
- [ ] CH-17 [P] Cross-Instance Execution: Run It on B — [#27](https://github.com/noetl/book/issues/27) · `src/ch17-*.md`
- [ ] CH-18 [P] MCP and Agents — [#28](https://github.com/noetl/book/issues/28) · `src/ch18-*.md`
- [ ] CH-19 [P] Project: Expose a Playbook as an MCP Tool and Call It from an Agent — [#29](https://github.com/noetl/book/issues/29) · `src/ch19-00-project-mcp-agent.md`

## Phase P6

- [ ] CH-23 [P] WASM at the Edge — [#33](https://github.com/noetl/book/issues/33) · `src/ch23-*.md`
- [ ] CH-24 [P] Project: Ship a Pure Playbook to the Edge — [#34](https://github.com/noetl/book/issues/34) · `src/ch24-00-project-edge.md`
- [ ] T-06 mdbook-noetl-play: in-browser runnable playbooks — [#8](https://github.com/noetl/book/issues/8) · `tools/`

## Phase P7

- [ ] CH-14 [P] EHDB as the State Substrate — [#24](https://github.com/noetl/book/issues/24) · `src/ch14-*.md`
- [ ] CH-20 [P] Coroutines and Structured Concurrency — [#30](https://github.com/noetl/book/issues/30) · `src/ch20-*.md`
- [ ] CH-25 [P] Agent and Bot Fleets on NoETL — [#35](https://github.com/noetl/book/issues/35) · `src/ch25-*.md`
- [ ] CH-26 [P] Case Study: A Quantum-Readiness Orchestrator — [#36](https://github.com/noetl/book/issues/36) · `src/ch26-*.md`
- [ ] CH-32 [P] Representation Drift: Keeping What You Know True — [#42](https://github.com/noetl/book/issues/42) · `src/ch32-00-representation-drift.md`

## Owner decisions

- [ ] OD-01 Hosting, license, quiz telemetry, Ch. 26 source, edge runner scope — [#51](https://github.com/noetl/book/issues/51)
