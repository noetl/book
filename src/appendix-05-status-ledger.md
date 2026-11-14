# Appendix E: Status Ledger — REAL vs TARGET by Chapter

<span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this section are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md).

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
