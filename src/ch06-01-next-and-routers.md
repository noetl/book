# `next` and Routers

<span class="status status-real">REAL</span>

`next` says where control goes when a step finishes. It has **four
forms**. The server tries them in this order when it parses the YAML
(`NextSpec`, `orchestrate-core/src/playbook.rs`, v3.161.2):

| # | Form | Example | Taken on the server |
|---|---|---|---|
| 1 | one step name | `next: report` | always |
| 2 | a list of names | `next: [a, b]` | **all of them**, in parallel |
| 3 | a list of targets `{step, when?, args?}` | `next: [{step: a, when: …}, {step: b}]` | by mode, **exclusive** by default |
| 4 | a router `{spec: {mode}, arcs: [{step, when?, set?}]}` | see below | by mode, **exclusive** by default |

All four in one playbook (`examples/ch06/next-forms`, a distributed
example that CI validates against the schema):

```yaml
{{#include ../examples/ch06/next-forms/playbook.yaml}}
```

## Exclusive and inclusive

Forms 3 and 4 decide which targets to take by **mode**
(`evaluator.rs`, v3.161.2):

- **`exclusive`** (the default): take the **first** target, in the
  order written, whose `when` is true or absent. Later targets are not
  evaluated at all; they are recorded as skipped.
- **`inclusive`**: take **every** target whose `when` is true or
  absent. All are dispatched in the same pass, so they run in
  parallel.

A router reads its mode from `next.spec.mode`. A list of targets reads
it from the step's `spec.next_mode`. If neither is set, the mode is
exclusive. A misspelt mode value also means exclusive: any string
other than `inclusive` does.

```admonish myth
"`next: [{step: a}, {step: b}]` runs `a` and `b`." It runs only `a`.
A list of **targets** is exclusive by default, and a target without
`when` always matches, so the first one wins and `b` is skipped. To
run both, write a list of **names** (`next: [a, b]`), or set
`spec.next_mode: inclusive` on the step, or use a router with
`mode: inclusive`.
```

## Passing values along an arc

- A target in form 3 may carry **`args`**, a map merged as-is into the
  target step's dispatch context. It is not rendered.
- An arc in form 4 may carry **`set`**, a map whose values are rendered
  against the current context and written with the same `ctx.` / `iter.`
  / `step.` prefix-stripping as step-level `set:`
  ([4.2](ch04-02-workload-and-templating.md)). It affects the context of
  the step it dispatches. Unlike a step's own `set:`, it is not written
  to the event log as a `ctx.updated` event.

Routers do not take `args`, and the grammar's own comment says arc
`args:` is not supported. Use `set`.

## On the local runtime

The local runtime (CLI v6.4.0) implements forms 3 and 4 the way the
server does, except that "in parallel" becomes "one after another" in
one process. CI checks both:

- `examples/ch06/next-targets`: a list of targets runs only the first,
  so `executed_steps` is `["start","a"]`;
- `examples/ch06/next-router-inclusive`: an inclusive router runs both,
  so `executed_steps` is `["start","a","b"]`.

It does **not** implement forms 1 and 2:

```yaml
{{#include ../examples/ch06/next-names-ignored-local/playbook.yaml}}
```

```json
{{#include ../examples/ch06/next-names-ignored-local/expected.json}}
```

```admonish warning title="Locally, `next: b` and `next: [a, b]` do nothing"
At CLI v6.4.0, a `next` that is a bare name or a list of bare names
is ignored. The run stops after the step, with status `ok` and no
warning. For a playbook that must run locally too, write targets
(`next: [{step: b}]`) or a router.
```

## Check your understanding

{{#quiz ../quizzes/ch06-01.toml}}
