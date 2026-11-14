# Appendix E: Status Ledger — REAL vs TARGET by Chapter

<span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this section are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md).

## Ledger

One row per written page: its badge, and the release or commit its
claims were checked against. Rows are added as chapters land.

| Page | Badge | Verified against | Landed |
|---|---|---|---|
| [Appendix B: Tool Kinds](appendix-02-tool-kinds.md) | REAL | generated at server v3.161.2 (`983e36e`); local column CLI v6.4.0 + CI examples | 2026-11-13 |
| [Appendix A: DSL Reference](appendix-01-dsl-reference.md) | REAL | generated at server v3.161.2 (`983e36e`) | 2026-11-13 |
| [Appendix F: Myths](appendix-06-myths.md) | REAL | per row (each row names its release / commit) | 2026-11-13 |
| [Ch. 6 Control Flow](ch06-00-control-flow.md) (6.0–6.4) | REAL | server v3.161.2 (`983e36e`) orchestrate-core, worker v6.15.0, tools v4.6.0, CLI v6.4.0 | 2026-11-13 |
| [6.5 Errors, Timeouts, Retries](ch06-05-errors-timeouts-retries.md) | PARTIAL | same; most keys parsed, not applied | 2026-11-13 |
| [Ch. 5 Tools](ch05-00-tools.md) (5.0–5.3) | REAL | server v3.161.2 (`983e36e`) manifest + resource model, worker v6.15.0, tools v4.6.0, CLI v6.4.0 | 2026-11-13 |
| [Ch. 4 Anatomy of a Playbook](ch04-00-anatomy-of-a-playbook.md) (4.0–4.5) | REAL | server v3.161.2 (`983e36e`), worker v6.15.0, tools v4.6.0, CLI v6.4.0 | 2026-11-13 |
| [Appendix H: Contributing](appendix-08-contributing.md) | REAL | book CI at `main` (mdbook 0.4.40, quiz 0.3.12, admonish 1.20.0, CLI 6.4.0) | 2026-11-13 |

## Versions the examples are tested against

Every example in this book is run in CI by `tools/run-examples.sh`
against one pinned NoETL CLI release. The version is the single line in
[`examples/NOETL_CLI_VERSION`](https://github.com/noetl/book/blob/main/examples/NOETL_CLI_VERSION);
the CI job log prints it (`noetl --version`).

| Component | Version | Where it is pinned |
|---|---|---|
| NoETL CLI (`noetl run`, local runtime) | **6.4.0** (released 2026-11-11) | `examples/NOETL_CLI_VERSION` |
| mdBook | 0.4.40 | `.github/workflows/book.yml` |
| mdbook-linkcheck | 0.7.7 | `.github/workflows/book.yml` |
| mdbook-quiz | 0.3.12 | `.github/workflows/book.yml` |
| mdbook-admonish | 1.20.0 | `.github/workflows/book.yml` |
