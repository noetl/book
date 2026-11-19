# Data Lineage on NoETL

<span class="status status-partial">PARTIAL</span> <span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md)
> (§2.9 and Part XI).

Where did this output come from? What NoETL records for every run (execution lineage), what is built but off by default, and what the author must declare (data lineage).

Planned sections:

- **36.1 What the Event Log Records About a Run** — [written](ch36-01-event-log-record.md).
- **36.2 References That Name Their Producer** (PARTIAL) — result-store references as provenance: the server's `noetl://execution/…` form, the worker-stamped canonical URI and its staged server consumption (off by default).
- **36.3 Declared Lineage: the Registry** (PARTIAL) — the `noetl.registry` of models, datasets, evals and releases, with author-declared `lineage` parents and `registry://` URNs; built, and off by default.
- **36.4 Recording Dataset Lineage Yourself** (REAL) — what NoETL does not track (datasets, columns, external code versions), and how a playbook can record it today; no lineage standard is emitted.
