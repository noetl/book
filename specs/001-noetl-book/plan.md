# Implementation Plan: The NoETL Book

**Spec**: [spec.md](spec.md) · **Constitution**: [constitution](../../.specify/memory/constitution.md) · **Tasks**: [tasks.md](tasks.md)

This plan does not repeat the pedagogy or the per-chapter goals.
Those live in [`docs/BOOK-PLAN.md`](../../docs/BOOK-PLAN.md), and the
authoring phases live in [`docs/ROADMAP.md`](../../docs/ROADMAP.md).
This file records the technical context spec-kit expects.

## Technical context

| Item | Choice |
|---|---|
| Format | mdBook 0.4.40 (pinned); `create-missing = false` |
| Content | Markdown under `src/`; table of contents `src/SUMMARY.md` |
| Quizzes | `mdbook-quiz` (Brown CEL), TOML under `quizzes/` — enabled by T-03 |
| Callouts / diagrams | `mdbook-admonish` (T-03), `mdbook-mermaid` (first diagram PR) |
| Link check | `mdbook-linkcheck` in CI (T-01) |
| Examples | `examples/<chapter>/<name>/` run by a pinned NoETL CLI in CI (T-02) |
| Generated references | Appendices A–D from `noetl/server` `orchestrate-core/schema/*` at a pinned commit (T-04) |
| Traces | `mdbook-noetl-trace` folding with orchestrate-core WASM (T-05, P3) |
| Runnable playbooks | `mdbook-noetl-play` (T-06, P6; pure playbooks only) |
| Hosting | pending owner decision ([#51](https://github.com/noetl/book/issues/51)) |

## Constitution check

| Principle | How the plan satisfies it |
|---|---|
| I Honesty badges | Badges in `theme/status.css`; issue `badge:` labels; Appendix E ledger |
| II Verify before REAL | PR template section "claim → where checked" (added with T-01) |
| III Spec-driven | Issues link spec anchors; spec PRs precede scope changes |
| IV One issue / one PR | One issue per chapter or task ([tasks.md](tasks.md)) |
| V Checks are gates | T-01 and T-02 each prove a red run before trusting green |
| VI Record status back | Issue comments + wiki Assignments |
| VII Public | No internal identifiers; owner-decision label for private sources |
| VIII Sources over memory | T-04 generation; BOOK-PLAN §7 source map |

## Phases

As in [ROADMAP](../../docs/ROADMAP.md#how-to-read-the-roadmap): P0
tooling → P1 foundations → P2 getting started and local → P3
distributed and traces → P4 substrate, resources, operations → P5
interop and distribution → P6 edge → P7 TARGET and applied.
