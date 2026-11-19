# Case Study: A Quantum Compilation Pipeline on the Local Runtime

<span class="status status-real">REAL</span> <span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this chapter are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md)
> (Part VIII and §2.8).

`noetl/quantum`: a NoETL entry in a public quantum-circuit compilation competition, read at commit `9208fa2`. Project level only: no competition data, scores or circuits.

Planned sections:

- **26.1 The Pipeline and Its Honest Defaults** — the baseline and optimize playbooks; with no data the pipeline writes no circuit and records no score rather than inventing one.
- **26.2 Validate Before You Run** — [written](ch26-02-validate.md).
- **26.3 Long-Running Compute: Budgets and Deadlines** — a seven-hour wall clock split per task, a per-transform budget, and a hard deadline that keeps the unmodified circuit when a transform overruns.
- **26.4 Shell as the Escape Hatch** — why every step is `kind: shell` on the local runtime, and what that costs.
