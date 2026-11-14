# Running It Locally with the CLI

<span class="status status-real">REAL</span>

## `noetl run`

```console
$ noetl run examples/ch01/hello/playbook.yaml
runtime: local (…)
📋 Running playbook: hello
   API Version: noetl.io/v2

🔹 Step: start

🔹 Step: done
```

The first line says **which runtime** ran the playbook and why. The
CLI picks it in this order (`noetl run --help`, CLI v6.4.0):

1. the `-r` / `--runtime` flag: `local`, `distributed` or `auto`;
2. otherwise, the active **context**'s runtime, if it sets one
   (`noetl context`);
3. otherwise, **local**.

So `noetl run <file>` runs locally unless you have selected a context
that says otherwise. Add `-r local` to be sure. The progress lines go to
standard error. They name the steps, but they **do not print the
steps' output**: the `echo` in `start` is captured as the step's
result, not shown. Add `-v` to see routing decisions (`✓ Route: done
(default)`).

## Reading the result: `--json`

```console
$ noetl run examples/ch01/hello/playbook.yaml -r local --json
```

With `--json`, the CLI prints one JSON object on standard output and
nothing else there:

```json
{{#include ../examples/ch01/hello/expected.json}}
```

(The book's CI runs exactly this command and compares this output,
minus the run's timestamps, duration and file path.)

| Field | Meaning |
|---|---|
| `status` | `ok` if the run finished |
| `executed_steps` | the steps that ran, in the order they first ran |
| `step_results` | each step's result, as text |
| `final_result` | the result of the last step that ran |

Passing a value in for one run:

```console
$ noetl run examples/ch01/hello/playbook.yaml -r local --json --set who=reader
```

overrides `workload.who` for that run.

## The local event trail

NoETL records an execution as events ([Chapter 3](ch03-02-event-sourcing.md)).
The local runtime can record them too. Add `--event-buffer`:

```console
$ noetl run examples/ch01/hello/playbook.yaml -r local --event-buffer
$ noetl buffer list --json
$ noetl buffer cat <execution_id>
```

Each run gets a directory under `$NOETL_LOCAL_DIR` (default
`~/.noetl/local`), holding `events.feather` (Apache Arrow) and
`metadata.json`. `noetl buffer cat` prints the events as JSON lines.
For the hello playbook on CLI v6.4.0 it printed four events, shown
here trimmed to their key fields. Ids and times differ per run:

```json
{"event_type":"playbook.started","status":"RUNNING","step":""}
{"event_type":"step.exit","status":"COMPLETED","step":"start","result":{"data":"hello world"}}
{"event_type":"step.exit","status":"COMPLETED","step":"done","result":{"data":42}}
{"event_type":"playbook.completed","status":"COMPLETED","step":"","result":{"duration_seconds":0.318}}
```

`noetl push` sends closed buffers to a NoETL server's event log
(`POST /api/events/batch`) so a local run can be inspected alongside
cluster runs ([Chapter 8](ch08-04-event-buffer.md)).

```admonish warning title="What the local runtime cannot run"
The local runtime runs only some tool kinds, and it ignores some of the
grammar. It has no `python` and no `postgres`, and it does not execute
`loop:`, for example. It tells you before running when a kind is
unsupported. [Chapter 8](ch08-00-local-runtime.md) has the full list.
```

## Check your understanding

{{#quiz ../quizzes/ch01-03.toml}}
