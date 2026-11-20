# What the Event Log Records About a Run

<span class="status status-real">REAL</span>

Lineage answers one question: *where did this output come from?* On
NoETL, part of the answer is recorded for every run with no extra work.
The rest you have to declare. This section covers the part you get for
free, and is exact about its edges. Facts are server **v3.161.2**.

## Every event names its run and its playbook

An execution's events are rows in `noetl.event`. Each row is written
with these columns (`src/db/queries/event.rs:40-45`):

```text
event_id, execution_id, catalog_id, parent_event_id, parent_execution_id,
event_type, node_id, node_name, node_type, status,
context, meta, result, worker_id, attempt, created_at,
prev_event_id, error
```

Three of them make lineage possible:

- **`catalog_id`** points at one row of `noetl.catalog`, which holds
  a playbook's `path`, its `version` and its full `content`, unique per
  `(path, version)` (`db/ddl/postgres/schema_ddl.sql:42-53`). From any
  event you can recover the exact playbook text that ran, not just its
  name.
- **`parent_execution_id`** links a child execution to the run that
  started it ([7.1](ch07-01-child-executions.md)). A pipeline built from
  sub-playbooks is a tree you can walk upward from any node.
- **`node_name`** is the step. With `event_type` and `result`, it says
  which step produced which value, and when.

The log is append-only and never purged
([3.2](ch03-02-event-sourcing.md)). So the record is still there when
someone asks months later.

## Asking the questions

| Question | Where the answer is |
|---|---|
| Which playbook, at which version, produced this run? | the event's `catalog_id` → `noetl.catalog` (`path`, `version`, `content`) |
| With what inputs? | the execution's workload, read from its start event (`context->'workload'`) |
| Which step produced this value, and when? | the event's `node_name`, `event_type`, `result`, `created_at` |
| Which run started this one? | `parent_execution_id` |
| Where did a large result go? | its reference, which names the execution that produced it (below) |

`GET /api/executions/{id}` returns most of this in one call:
`catalog_id`, `path`, `parent_execution_id`, `workload`, and the events
with type, step, status, time, result and error
(`src/services/execution.rs:28-50`).

```admonish warning title="The API returns a window, not the whole log"
That endpoint loads at most the **2,000 most recent** events of an
execution (`MAX_EVENTS_RETURNED`, `src/services/execution.rs:694`). It
was capped after a large run's full log exhausted the server's memory.
For a long run, the earliest steps are not in the response. Read them
from the log itself. The API also leaves out `worker_id`, `attempt`,
`context` and `meta`, which the rows have.
```

## Large results keep their producer's name

A result over 100 KiB does not stay in the event. It moves to the
result store, and the event holds a reference instead
([5.3](ch05-03-results-and-references.md)). The reference is an
address that names its producer:

- the server's reference, `noetl://execution/<eid>/result/<name>/<id>`,
  which is what is resolved today;
- a canonical form the worker also stamps,
  `noetl://<tenant>/<project>/results/<eid>/<step>/<frame>/<row>/<attempt>`,
  which the server does **not** consume yet. Accepting it is behind
  `NOETL_RESULT_URI_ACCEPT`, off by default (`src/config/app.rs:442-470`).

So a large output found anywhere can be traced back to the execution
that wrote it, and with the canonical form, to the step.

## What the log does not record

The record covers what NoETL ran. It does not cover the data your steps
touched outside it:

- **Datasets.** If a `postgres` step reads `orders` and writes
  `daily_revenue`, nothing records "this step read `orders`" as a
  structured fact. The SQL is part of the step's configuration, but
  NoETL does not parse it into dataset names. There is no dataset- or
  column-level lineage.
- **Lineage standards.** No lineage emitter (OpenLineage or any other)
  exists in the server, worker, tools, CLI or gateway. The book searched
  each at its newest tag on 2026-11-19.
- **The code behind a command.** A `shell` step that runs
  `python3 -m scoring.run` records the command, not the version of
  `scoring`. Pin it yourself ([Chapter 28](ch28-00-releases.md)).
- **What a re-run would do.** Replay folds the recorded events, so it
  reproduces NoETL's *decisions* exactly. Running the playbook again
  calls the tools again, against today's data and services.

```admonish tip title="The honest summary"
NoETL gives you **execution lineage** for free: which playbook version
ran, with what inputs, which step produced what, and which run started
which. **Data lineage**, meaning which datasets flowed into which, is
yours to declare. The next sections show the places to declare it.
```

## Check your understanding

{{#quiz ../quizzes/ch36-01.toml}}
