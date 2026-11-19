# Case Study: Standing Up the Platform

<span class="status status-partial">PARTIAL</span> <span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this chapter are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md)
> (Part X and §2.8).

Standing up the distributed platform from nothing, as `noetl/ops` commits it.

Planned sections:

- **35.1 NoETL Provisions NoETL** — the fresh-stack playbook: a NoETL playbook, run on the local runtime, that provisions a GKE cluster and deploys the stack.
- **35.2 Images: Cloud Build and the Release Pipeline** — Cloud Build definitions next to the release pipeline of Ch. 28, and which one produces what prod runs.
- **35.3 Worker Pools and KEDA** — the ScaledObjects per pool, on bus lag and CPU.
- **35.4 Secrets and the EHDB Substrate** — CSI-mounted bootstrap secrets and the EHDB platform playbook.
- **35.5 What the Recipe Declares vs What Runs** — which parts of the recipe are current, which are stale, and why committed is not live.
