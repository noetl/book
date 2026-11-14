# Project: Fetch, Transform, Store — Your First Real Playbook

<span class="status status-real">REAL</span>

In this project you build a playbook that does real work on your
machine, with only the CLI installed:

1. **fetch** two JSON documents over HTTP;
2. **store** each response in a DuckDB table;
3. **loop** back to fetch the next one, and stop after two;
4. **transform** the table into a summary and **write** it to a CSV file;
5. **read** the file back, as a check.

The documents are two of NoETL's own published files, the DSL manifest
and the playbook schema, fetched at a **pinned commit** of the server
repository so that the data never changes. That lets the book's CI run
this exact playbook on every change and compare its result.

Everything here runs on the **local runtime** of CLI v6.4.0. It uses
only kinds the local runtime supports: `duckdb`, `rhai` and `http`.

## The playbook

```yaml
{{#include ../examples/ch02/fetch-transform-store/playbook.yaml}}
```

Run it:

```console
$ noetl run examples/ch02/fetch-transform-store/playbook.yaml -r local --json
```

Its `final_result` is the CSV read back by `check`:

```json
{{#include ../examples/ch02/fetch-transform-store/expected.txt}}
```

and `/tmp/noetl-book-ch02-summary.csv` contains:

```text
i,name,http_status,top_level_keys
0,dsl-manifest.json,200,10
1,playbook.schema.json,200,8
```

## Walking through it

**`start`** creates the table. `CREATE OR REPLACE` makes the playbook
safe to run twice. Its `vars:` sets the loop counter `i` to `0`.

**`pick`** turns the counter into a file name. A `rhai` step's result
is the value of its last expression. The template `{{ vars.i }}` is
replaced before the script runs, so the script the engine sees is
`["dsl-manifest.json", "playbook.schema.json"][0]`.

**`fetch`** is an `http` step. Its result is a JSON object with the
response's `status` and `body`.

**`load`** inserts one row. The values go in as bound **parameters**
(`?` in the SQL, `params:` in the step), never pasted into the SQL
text. The response body contains quotes, and parameters need no
escaping.

**`advance`** adds one to the counter and stores it back in
`vars.i`. Its `next` is the decision point:

```yaml
next:
  - step: pick                 # the back-edge ...
    when: "{{ vars.i != 2 }}"  # ... taken while i is not 2
  - step: report               # otherwise, carry on
```

A list of targets is **exclusive**: the first one whose `when` is true
wins ([6.1](ch06-01-next-and-routers.md)). The arc back to `pick` is a
**back-edge**, an arc to a step that has already run
([6.4](ch06-04-back-edges.md)).

**`report`** does the transform in SQL and writes the file with DuckDB's
`COPY … TO`. **`check`** reads it back with `read_csv_auto`.

Every `duckdb` step names its database file with `db:`. Without one,
the local runtime uses `.noetl/state.duckdb` **next to the playbook
file** (`default_duckdb_path`, CLI v6.4.0). A relative `db:` is also
resolved against the playbook's directory, not your current directory.

### Does the loop terminate?

Always ask this of a back-edge. Nothing in NoETL stops a loop for you;
the guard is the only bound ([6.4](ch06-04-back-edges.md)). Here:
`i` starts at `0`, `advance` is the only step that changes it, it adds
exactly 1 each time, and the loop exits when `i` is `2`. So the loop
body runs exactly twice. Had `advance` added 2, `i` would go 0, 2 and
exit after one pass. Had it added 3, `i` would skip past 2 and the
loop would never end: guard on `!=` only when you are sure the
counter hits the value exactly.

## What the run recorded

Run it with `-v` to watch the routing decisions:

```text
🔹 Step: advance
   ✓ Route matched: pick ({{ vars.i != 2 }})
🔹 Step: pick
…
🔹 Step: advance
   ✗ Route skipped: pick ({{ vars.i != 2 }})
   ✓ Route: report (default)
```

and with `--event-buffer` to record the run's events
([1.3](ch01-03-running-locally.md)). On CLI v6.4.0 the buffer held:

```text
playbook.started
step.exit  start
step.exit  pick
step.exit  fetch
step.exit  load
step.exit  advance
step.exit  report
step.exit  check
playbook.completed
```

This is the vocabulary the rest of the book uses:

- a **step** is a named unit of the workflow (`fetch`);
- a **tool** is what a step runs (`http`);
- an **arc** is a transition in `next`, with an optional `when`
  guard;
- an **event** is a record of something that happened, and the
  sequence of events is the execution's history.

```admonish warning title="The local trail shows each step once"
`pick`, `fetch`, `load` and `advance` ran **twice**, but the local
buffer has one `step.exit` for each of them. At CLI v6.4.0 it records
one exit per step, at its first run, so a back-edge loop's later passes
do not appear. `executed_steps` in the `--json` output works the same
way. A NoETL server records every pass ([Chapter 10](ch10-05-one-execution.md)).
```

## What changed and why

| Choice | Why |
|---|---|
| Data from a pinned commit | Deterministic input, so the result can be checked automatically |
| `CREATE OR REPLACE` in `start` | Re-running the playbook does not fail or duplicate rows |
| Parameters, not string pasting | HTTP bodies contain quotes; parameters are never parsed as SQL |
| Counter in step `vars:` | That is how the **local** runtime passes values between steps; a server would use `set:` ([4.2](ch04-02-workload-and-templating.md)) |
| A guard that is reached exactly | The `!=` guard is safe only because the counter steps by 1 from 0 |
| Transform in SQL inside one step | One step does all the rows. A loop of steps would pay the orchestration cost once per row |

## Checkpoint

{{#quiz ../quizzes/ch02-00.toml}}

## Extend it

- Add a third file (`resource-model.json`) to `pick` and change the
  guard. Re-check the termination argument.
- Add a column to the report: the number of `tool_kinds` in the
  manifest (`json_array_length(doc->'$.body.tool_kinds')`).
- Make the output path an input: run it with
  `--set out=/tmp/mine.csv`.
- Read [Chapter 8](ch08-00-local-runtime.md) and list what you would
  have to change to run this playbook on a cluster. Hints: the counter
  (`vars:` → `set:`) and the `{{ <step>.result }}` references.
