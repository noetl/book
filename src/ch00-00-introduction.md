# Introduction

<span class="status status-real">REAL</span> <span class="status status-stub">STUB</span>

NoETL is a declarative orchestration system. You describe work as a
*playbook*: a YAML document of steps, the tools each step runs, and the
arcs between them. A runtime executes it and records every transition
as an immutable event. The same playbook can run in three places:

- **in one process** on your laptop with `noetl run`;
- **as a long-lived listener** with `noetl subscribe` / `noetl serve`;
- **on a cluster**, where a gateway, a server, autoscaled worker pools
  and the EHDB event/command bus share the work.

This book teaches that model from the ground up. It starts with a
playbook you can run in a minute and works up to the internals: the
event log, the command bus, the catalog, cross-instance execution,
agents, performance, and how the system is operated in production.

> The full introduction will be written once Parts I–II exist. See the
> authoring order in `docs/BOOK-PLAN.md`.
