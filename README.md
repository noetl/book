# The NoETL Book

The complete guide to the NoETL ecosystem: the playbook DSL; the local,
daemon and distributed runtimes; EHDB; the distributed catalog;
cross-instance execution; MCP and agents; concurrency; the resource and
performance model; WASM at the edge; and operations.

It follows the structure of *The Rust Programming Language* and adds
the interactive layer from Brown University's Cognitive Engineering Lab
edition: quizzes after sections, check-your-understanding checkpoints,
step-through visualizations of execution state, and runnable examples.

**This book is written iteratively.** Every page carries a status badge:
**REAL** (shipped), **PARTIAL**, **TARGET** (designed, not built) or
**STUB** (not written yet).

- Outline: [`src/SUMMARY.md`](src/SUMMARY.md)
- Roadmap (every chapter: what it covers, its badge, when it gets written):
  [`docs/ROADMAP.md`](docs/ROADMAP.md)
- Plan (pedagogy, per-chapter goals, tooling, sources):
  [`docs/BOOK-PLAN.md`](docs/BOOK-PLAN.md)
- **Contributing** (spec-kit, issues, wiki, and the rules for AI agents):
  [`CONTRIBUTING.md`](CONTRIBUTING.md). Agents also read [`AGENTS.md`](AGENTS.md).
- Coordination (assignments, style guide, decisions): the
  [wiki](https://github.com/noetl/book/wiki)

## Building

```bash
cargo install mdbook --version 0.4.40 --locked
cargo install mdbook-linkcheck --version 0.7.7 --locked
mdbook serve --open
```

### Running the CI checks locally

CI (`.github/workflows/book.yml`) runs exactly this, with the same pinned
versions (mdbook 0.4.40, mdbook-linkcheck 0.7.7):

```bash
mdbook build          # html + internal link check; fails on any broken link
```

```bash
MDBOOK_OUTPUT__LINKCHECK__FOLLOW_WEB_LINKS=true mdbook build   # also external links (CI: weekly)
```

With more than one renderer the HTML lands in `book/html/`, not `book/`.
`mdbook-linkcheck` is marked `optional` in `book.toml`, so a machine
without it still builds, but **skips the link check silently**. Install
it before you open a PR.

The book builds with plain `mdbook` today. The interactive preprocessors
(`mdbook-quiz`, `mdbook-admonish`, `mdbook-mermaid`, and the NoETL-specific
`mdbook-noetl-trace` / `mdbook-noetl-play`) are enabled one at a time, as
their first real uses land. See `book.toml` and `docs/BOOK-PLAN.md` §4.

## Layout

```
book.toml          mdBook config (planned preprocessors commented out)
src/SUMMARY.md     the table of contents — the contract for the book
src/*.md           chapters (chNN-MM-slug.md), appendices
docs/BOOK-PLAN.md  the plan
docs/ROADMAP.md    chapter-by-chapter roadmap
specs/             spec-kit spec (specs/001-noetl-book/: spec, plan, tasks)
.specify/          spec-kit scaffold + constitution (.specify/memory/constitution.md)
.claude/skills/    spec-kit skills for Claude Code (/speckit-*)
CONTRIBUTING.md    workflow + AI-agent rules
AGENTS.md          short rules auto-read by coding agents
examples/          example playbooks, tested in CI
quizzes/           mdbook-quiz TOML files
traces/            recorded event logs for the trace visualizer
tools/             NoETL-specific preprocessors
theme/status.css   status badges
```

## Tracking

The book is a submodule of [`noetl/ai-meta`](https://github.com/noetl/ai-meta)
at `repos/book`.
