# Introduction

<span class="status status-real">REAL</span>

NoETL is a declarative orchestration system. You describe work as a
**playbook**: a YAML document that lists **steps**, the **tool** each
step runs (an HTTP call, a SQL query, a script, another playbook), and
the **arcs** that move control from one step to the next
([Chapter 4](ch04-00-anatomy-of-a-playbook.md),
[Chapter 5](ch05-00-tools.md), [Chapter 6](ch06-00-control-flow.md)).

A runtime executes the playbook and records what happens as
**events**: the execution started, a step ran and returned this
result, the execution completed. You can watch a local run write them
([1.3](ch01-03-running-locally.md), [Chapter 2](ch02-00-project-first-playbook.md)).
On a server, the events are the execution: its state is computed from
them, and they are never edited
([Chapter 3](ch03-02-event-sourcing.md)).

The same grammar runs in three places
([Chapter 11](ch11-00-choosing-a-runtime.md)):

- **in one process** on your machine, with `noetl run`
  ([Chapter 8](ch08-00-local-runtime.md));
- **as a long-lived listener**, with `noetl subscribe` and
  `noetl serve` ([Chapter 9](ch09-00-daemon.md));
- **on a cluster**, where a server decides what runs next and
  autoscaled worker pools do the work
  ([Chapter 10](ch10-00-distributed-runtime.md)).

They are three implementations, and they do not behave identically.
This book says where they differ, and tests its examples to keep
those statements true ([8.1](ch08-01-in-process-interpreter.md)).

## How this book is written

NoETL changes every week, so every page carries a badge that says
whether its subject is shipped (REAL), partly shipped (PARTIAL) or only
designed (TARGET), and every number says whether it was measured,
deployed or planned ([How to Read This Book](ch00-01-how-to-read.md)).
Claims are checked against the code at a named release, and the
[status ledger](appendix-05-status-ledger.md) records which release
each page was checked against. Where a common belief about NoETL is
wrong, the page says so, and [Appendix F](appendix-06-myths.md)
collects the corrections.

## The arc of the book

| Part | You will learn |
|---|---|
| I Getting Started | install the CLI, run a playbook, build a small real pipeline |
| II The Model | what NoETL is; every key of a playbook; tools; control flow; sub-playbooks |
| III The Three Runtimes | local, daemon and distributed, and how to choose |
| IV EHDB | the storage engine under the event log and the command bus |
| V Distribution | the distributed catalog and cross-instance execution |
| VI Interop & Concurrency | MCP and agents; the planned coroutine model |
| VII Resources & Performance | what a playbook costs, where the time goes, WASM at the edge |
| VIII Applied | larger systems built on NoETL |
| IX Operations | deploying, releasing, rolling out, observing and securing NoETL |

Parts I and II and most of Part III are written first. The rest follows the
[roadmap](https://github.com/noetl/book/blob/main/docs/ROADMAP.md).
A page that is not written yet says so with a STUB badge.

## Check your understanding

{{#quiz ../quizzes/ch00-00.toml}}
