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
- Plan (pedagogy, per-chapter goals, tooling, authoring order):
  [`docs/BOOK-PLAN.md`](docs/BOOK-PLAN.md)

## Building

```bash
cargo install mdbook --version 0.4.40 --locked
mdbook serve --open
```

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
examples/          example playbooks, tested in CI
quizzes/           mdbook-quiz TOML files
traces/            recorded event logs for the trace visualizer
tools/             NoETL-specific preprocessors
theme/status.css   status badges
```

## Tracking

The book is a submodule of [`noetl/ai-meta`](https://github.com/noetl/ai-meta)
at `repos/book`.
