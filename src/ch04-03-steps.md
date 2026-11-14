# `workflow`: Steps

<span class="status status-real">REAL</span>

`workflow` is a list. Each item is one **step**: a named unit that runs
one tool and then says where to go next.

```yaml
workflow:
  - step: start
    desc: Build a greeting
    tool:
      kind: rhai
      code: |
        "{{ workload.greeting }}, {{ workload.who }}"
    next:
      - step: shout
  - step: shout
    tool:
      kind: rhai
      code: |
        "{{ workload.greeting }}, {{ workload.who }}!".to_upper()
```

## Step keys

These are all the keys a step has in the grammar at server v3.161.2
(`Step` in `orchestrate-core/src/playbook.rs`, and the `Step` type in
[Appendix A](appendix-01-dsl-reference.md#step)).

| Key | Required | What it is | Covered in |
|---|---|---|---|
| `step` | yes | The step's name. It must be unique within the playbook; `next` targets refer to it. | here |
| `tool` | yes (server) | What the step runs: one tool, or an ordered list of tools | [Chapter 5](ch05-00-tools.md) |
| `desc` | | A description | here |
| `next` | | Where control goes after the step: one name, a list, or a router of arcs with `when` guards | [6.1](ch06-01-next-and-routers.md) |
| `when` | | An enable guard: an expression checked before the step runs | [6.2](ch06-02-when-guards.md) |
| `loop` | | Run the step once per item of a collection | [6.3](ch06-03-loop.md) |
| `spec` | | Step behaviour: `next_mode`, `timeout`, `on_error` | [6.5](ch06-05-errors-timeouts-retries.md) |
| `args` | | Input arguments for the step | [5.3](ch05-03-results-and-references.md) |
| `vars` | | Values to extract from the step's result into variables | [5.3](ch05-03-results-and-references.md) |
| `set` | | Variable mutations applied when the step completes | [5.3](ch05-03-results-and-references.md) |

Two rules from the server's validator apply to the list as a whole
(`validate_playbook`, `src/playbook/parser.rs`, server v3.161.2):

- **One step must be named `start`.** The server begins every
  execution there, wherever it sits in the list.
- **Step names are unique**, and every name used in a `next` must
  exist.

There is no special `end` step to declare. A step with no `next`
simply ends its branch. [Chapter 6](ch06-00-control-flow.md) explains
when the whole execution counts as finished.

```admonish warning title="Where the local runtime differs"
Checked in CLI v6.4.0 (`src/playbook_runner.rs`):

- It starts at the **first** step in the list, not at `start`. You can
  change that with `--target <step>`.
- `tool` is optional. A step without one runs nothing and just
  routes.
- It still runs the old `case:` blocks, which the server refuses.

Write playbooks for the server's rules (a `start` step, a `tool` on
every step, no `case:`) and both runtimes accept their structure. A
tool's own fields can still differ between the two;
[Chapter 5](ch05-00-tools.md) shows where.
```

## Step order is not run order

The position of a step in `workflow` decides nothing except, locally,
which step runs first. Run order comes from `next`. This playbook
lists `done` before `start`. It is still valid, and on a server it runs
`start` and then `done`:

```yaml
{{#include ../examples/ch04/step-order/playbook.yaml}}
```

The local runtime runs it differently. It starts at the first step in
the list, `done`, which has no `next`, so the run ends there and
`start` never runs. The book's CI checks exactly that
(`examples/ch04/step-order`):

```json
{{#include ../examples/ch04/step-order/expected.json}}
```

## Check your understanding

{{#quiz ../quizzes/ch04-03.toml}}
