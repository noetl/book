# `workload`, `vars` and Templating

<span class="status status-real">REAL</span>

A playbook gets its inputs from `workload` and reads them, and other
values, through **templates**: `{{ … }}` expressions inside strings.
This section covers both. It also covers the most important
portability fact in this chapter: **the server and the local runtime
do not share a variable model**. A playbook that passes values between
steps will behave differently on the two unless it is written for
both.

Server facts here were checked at **server v3.161.2** (commit
`983e36e`) and worker v6.15.0. Local facts were checked at **CLI
v6.4.0** and are asserted by CI examples.

## `workload`: inputs

`workload` is a map of inputs with their default values:

```yaml
workload:
  greeting: hello
  who: world
```

Every template can read it as `{{ workload.<key> }}`. A run can
override it:

- locally, with `noetl run … --set who=cli` (repeatable) or
  `--payload '{"who": "cli"}'`;
- on a server, with the payload of the execute request
  ([Chapter 10](ch10-00-distributed-runtime.md)).

On the server, workload keys are also available without the prefix,
as `{{ who }}` (`build_context`, `orchestrate-core/src/state.rs`).
Locally, `--set who=cli` sets both `{{ workload.who }}` and `{{ who }}`.

## Templates

### On the server: Jinja (minijinja)

The server and the worker render templates with
[minijinja](https://docs.rs/minijinja), a Rust implementation of
Jinja2. Filters, comparisons, arithmetic and `if` expressions work as
they do in Jinja. Undefined values are **chainable**:
`{{ a.b.c }}` with no `a` renders as an **empty string** rather than
an error (`UndefinedBehavior::Chainable`, `orchestrate-core/src/template.rs`,
and the same in noetl-tools).

The names a step's templates can see on the server are:

| Name | What it is |
|---|---|
| `workload.<key>`, or plain `<key>` | the workload |
| `<step>.<field>`, `<step>.data.<field>` | a completed step's result data |
| `steps.<step>` | a completed step's full result envelope |
| `<key>`, `ctx.<key>` | values set by `set:` (below) |
| `output.<field>` | in a step's own `set:` and in its `next` arcs: that step's result |
| `iter.<name>`, `<name>`, `_index`, `_total` | inside a `loop` body ([6.3](ch06-03-loop.md)) |
| `keychain.<alias>.<field>` | a credential, rendered only on the worker ([4.4](ch04-04-keychain.md)) |
| `execution_id`, `path`, `version` | the execution's identity |

### On the local runtime: token substitution

The local runtime does **not** run a Jinja engine. It substitutes
tokens in a single pass (`render_template`,
`executor/src/template.rs`, CLI v6.4.0):

- `{{ name }}` is replaced only when written with **exactly one space**
  inside each brace. `{{name}}` is left as it is.
- Four filters exist: `lower`, `upper`, `trim` and `default`.
- An unknown name is **left in place**, braces and all, not rendered
  empty.
- There are no expressions: no arithmetic, no `if`, and no comparison
  except in conditions ([6.2](ch06-02-when-guards.md)).

This example is run in CI:

```yaml
{{#include ../examples/ch04/templating/playbook.yaml}}
```

Its result, checked by CI:

```json
{{#include ../examples/ch04/templating/expected.json}}
```

So `b` stayed literal (no spaces), `c` used the `upper` filter, and
`d` (an unknown name) stayed literal. On a server, `b` would render as
`book` and `d` as an empty string.

## Passing values between steps

Here the runtimes really diverge. There are three variable mechanisms
in the grammar, and each runtime honours a different subset:

| Mechanism | Server (v3.161.2) | Local (CLI v6.4.0) |
|---|---|---|
| top-level `vars:` | parsed; **nothing reads it** | not loaded |
| step `vars:` (extract from the result) | parsed; **nothing reads it** | **works**: sets `{{ vars.<key> }}` |
| step `set:` | **works**: values persisted as a `ctx.updated` event, read as `{{ <key> }}` or `{{ ctx.<key> }}` | parsed; **nothing reads it** |
| a step's result | `{{ <step>.<field> }}`, `{{ output.<field> }}` | `{{ <step>.result }}` (the whole result as text) |

The server claims were checked by searching every reader of these
fields in the server and worker at the versions named. Step `vars` and
top-level `vars` have none. Step `set:` is applied in the orchestrator
(`orchestrate-core/src/orchestrator.rs`, "a step's `set:` fires once
per completion, and the rendered values are persisted to the event
log as a `ctx.updated` event").

This local example uses all three mechanisms. CI checks what each one
produced:

```yaml
{{#include ../examples/ch04/variables-local/playbook.yaml}}
```

```json
{{#include ../examples/ch04/variables-local/expected.json}}
```

Step `vars:` worked locally (`step_vars=42`). Top-level `vars` and
`set:` did not, and their tokens were left in place.

```admonish myth
"Use `vars:` to pass a value to the next step." That is true **only on
the local runtime**. On a server at v3.161.2, nothing reads step
`vars:` or top-level `vars:`. Use `set:` there, for example
`set: {ctx.answer: "{{ output.value }}"}`, then read it as
`{{ answer }}`. No single mechanism works on both runtimes today.
```

### How `set:` names work on the server

A `set:` key may carry a scope prefix. `ctx.`, `iter.` and `step.` are
stripped, so `ctx.offset` writes a variable called `offset`. Any other
key is written exactly as given, dots included (`apply_set_mutations`,
`orchestrate-core/src/state.rs`). Because each completion's values go
into the event log, they survive the re-dispatch that loops need
([6.4](ch06-04-back-edges.md)).

## Check your understanding

{{#quiz ../quizzes/ch04-02.toml}}
