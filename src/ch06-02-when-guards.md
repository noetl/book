# `when` Guards

<span class="status status-real">REAL</span>

A `when` is a condition, written as a template. It appears in two
places, and they are evaluated at different moments.

| Where | Evaluated | If false |
|---|---|---|
| on an **arc** (`next` target or router arc) | when the step it leaves has **completed**, in the next orchestration pass | that arc is not taken |
| on a **step** (`step.when`) | when the step is **about to be dispatched** by an arc | the step is skipped (see below) |

## Arc guards: after the step completes

An arc's `when` is evaluated only in an orchestration pass, and a pass
is triggered by a completion event such as `command.completed`
(`orchestrator.rs`, v3.161.2). So the guard can use the result of the
step it leaves:

```yaml
- step: check_status
  tool:
    kind: http
    method: GET
    url: https://api.example.com/v1/jobs/{{ workload.job_id }}
  next:
    spec: { mode: exclusive }
    arcs:
      - step: done
        when: "{{ output.state == 'finished' }}"
      - step: failed
        when: "{{ output.state == 'error' }}"
      - step: wait_and_retry          # default arc: no `when`
```

In an arc guard, `output` is the completed step's result data, and
`{{ check_status.state }}` means the same thing. Everything else a
template can see ([4.2](ch04-02-workload-and-templating.md)) is
available too.

## Step guards: before the step runs

A step's own `when` is checked when an arc is about to dispatch it,
against the context that arc would give it, its `set` included. When
it is false, the server (v3.161.2, `orchestrator.rs`):

1. records a `step.skipped` event for the step;
2. **follows the skipped step's own `next`**, taking only the first
   matching arc, and checks the guard of that step in turn;
3. stops if there is no matching arc; that path of the workflow ends
   there.

So a step guard skips **one step**, not the rest of the path.

```admonish note
The `start` step's `when` is never evaluated: the server dispatches
`start` directly when the execution begins.
```

## What counts as true

The server renders the guard with minijinja. If you omit `{{ }}`, it
adds them. Then it compares the rendered **text**. These values are
false, compared case-insensitively after trimming: an empty string,
`false`, `0`, `no`, `none`, `null`, `off`, `{}` and `[]`. Anything
else is true (`evaluate_condition`, `orchestrate-core/src/template.rs`).
Two consequences:

- `{{ a and b }}` renders the *value* of `b` when `a` is true, as
  Python's `and` does, so a non-empty value counts as true.
- An **undefined** name renders as an empty string, so a guard on a
  misspelt variable is **false**.

## On the local runtime

The local runtime (CLI v6.4.0) supports a smaller condition language:
`==`, `!=`, `'x' in y`, and a bare value tested for truthiness with
the same false-like words. It has no `<` or `>` and no `and` / `or`
(`evaluate_condition`, `executor/src/condition.rs`). For anything more,
compute the decision in a `rhai` step and test its result. The local
runtime also differs from the server in two
ways that change which path a run takes. CI checks both:

```yaml
{{#include ../examples/ch06/when-undefined-local/playbook.yaml}}
```

```json
{{#include ../examples/ch06/when-undefined-local/expected.json}}
```

```admonish warning title="An undefined name is TRUE locally"
Locally, an unknown name is left in the template as text, and
non-empty text is true. So `when: "{{ workload.not_set }}"` **takes**
the arc locally (above: `a` ran). On a server, the same guard renders
empty and is false.
```

```yaml
{{#include ../examples/ch06/when-skip-local/playbook.yaml}}
```

```json
{{#include ../examples/ch06/when-skip-local/expected.json}}
```

```admonish warning title="A false step guard ends the branch locally"
Locally, a step whose `when` is false is skipped **and its branch
ends**: `b` never runs. On a server, `a` is skipped and its `next` is
followed, so `b` runs.
```

## Check your understanding

{{#quiz ../quizzes/ch06-02.toml}}
