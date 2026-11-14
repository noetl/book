# The Ordered Tool List: One Command, One Slot

<span class="status status-real">REAL</span>

A step's `tool` can be a **list**. The tools run in order, each one can
use the results of the ones before it, and the step completes when the
last one finishes.

```yaml
{{#include ../examples/ch05/pipeline/playbook.yaml}}
```

Each item needs a **label**, the name its result is known by. There
are two ways to write one, and both appear above:

- **flat**: a `name:` field next to `kind:` (`fetch`, `report`);
- **nested**: a one-key map whose key is the label (`double`).

The server's validator refuses a nested item with more than one key,
and an empty list (`validate_tool_definition`, `src/playbook/parser.rs`,
server v3.161.2).

## What actually runs

The list is **not** dispatched one tool at a time. The server turns
the whole list into **one command** of kind `task_sequence`
(`build_tool_from_definition`, `orchestrate-core/src/commands.rs`,
v3.161.2):

- **One worker** claims that command, and **one slot** is held for the
  whole list.
- The sub-tasks run **one after another, inside that one command**
  (tools v4.6.0 `src/tools/task_sequence.rs`).
- To the rest of NoETL the list is a single step: one command
  dispatched, one result reported.

```admonish myth
"Each tool in a list is its own task, so a list spreads work across
workers." It does not. A three-tool list is **one** `task_sequence`
command on **one** worker in **one** slot, for as long as all three
take. Splitting work across workers means separate steps, a parallel
`loop` ([6.3](ch06-03-loop.md)), or sub-playbooks
([Chapter 7](ch07-00-sub-playbooks.md)).
```

That makes the list a good fit for several small, related operations.
It saves the per-step orchestration cost between them, which
[Chapter 22](ch22-00-orchestration-overhead.md) shows is usually the
largest cost. It is a poor fit for work that should run in parallel.

## Passing results along the list

Inside the list, each finished sub-task's result is available to the
later ones by its label: `{{ fetch.value }}` or
`{{ fetch.data.value }}`. The `double` item above reads `fetch`'s
result that way. A sub-task can also have:

- `args:` (or `input:`), rendered against everything so far, before
  the sub-task runs;
- `set:`, rendered after it runs, with its result available as
  `output`, to carry values forward to the later items;
- `spec.policy.rules`, which decide what happens after the sub-task:
  continue, retry, jump to another label, break or fail. This is the
  retry mechanism that actually works
  ([6.5](ch06-05-errors-timeouts-retries.md)).

The server leaves `args`/`input` and `set` unrendered when it builds
the command, because they refer to results that only exist on the
worker as the list runs.

The step's own result is a map from each label to that sub-task's
data. The server also copies each label's fields to the top level, so
a later step can read `{{ start.double.value }}` and also
`{{ start.value }}` (`flatten_task_sequence_data`,
`orchestrate-core/src/state.rs`). If two sub-tasks return the same
field name, which one ends up at the top level is not specified, so
use the labelled form.

## The iteration cap

A `do: jump` rule can send the list back to an earlier label, so a
list can loop. To stop a loop that never reaches its `break`, the
sequence counts **every sub-task execution**, jumps and retries
included. Above the cap it stops with the error
`max_iterations_exceeded`.

| Setting | Default | Label |
|---|---|---|
| `NOETL_TASK_SEQUENCE_MAX_ITERATIONS` (worker env) | **1,000,000** sub-task executions per step | DEFAULT (tools v4.6.0 `task_sequence.rs`) |

It is the **only** iteration cap in the server, worker and tools code at these versions. Loops
and back-edges *between* steps have none
([Chapter 6](ch06-00-control-flow.md)).

## Not on the local runtime

```admonish warning title="The local runtime cannot read a tool list"
At CLI v6.4.0 a step whose `tool:` is a list fails to parse, with
`workflow[0].tool[0]: invalid type: map, expected variant identifier`,
and nothing runs. CI checks this (`examples/ch05/pipeline-refused-local`).
The example above is a distributed one: CI validates it against the
schema but does not run it.
```

## Check your understanding

{{#quiz ../quizzes/ch05-02.toml}}
