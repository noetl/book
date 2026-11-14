# One Process, One Interpreter

<span class="status status-real">REAL</span>

The local runtime is a tree-walking interpreter in
`src/playbook_runner.rs` (CLI v6.4.0). It reads the YAML, checks the
kinds, and then **calls** steps: running a step means running its tool
and then calling `execute_step` on each `next` target it takes. So:

- **Everything is sequential.** An inclusive router or a fan-out runs
  its targets one after another, in one process.
- **A back-edge is a recursive call.** A loop of N passes is N nested
  calls. An unguarded back-edge simply keeps running: one was observed
  still running, with no output, when it was stopped at 60 seconds.
- **The first failing step ends the run** with an error. There is no
  failure routing ([6.5](ch06-05-errors-timeouts-retries.md)).
- **It starts at the first step in `workflow`**, not at `start`, unless
  you pass `--target <step>` ([4.3](ch04-03-steps.md)).

## The differences from the server

Every difference the book has found so far, in one place. Each row
links to where it is shown, and most are CI examples that would fail
if the behaviour changed.

| Area | Server (v3.161.2) | Local (CLI v6.4.0) | Shown in |
|---|---|---|---|
| First step | `start` | first in the list | `examples/ch04/step-order` |
| Templates | minijinja; undefined → empty | exact `{{ name }}` tokens, 4 filters; unknown left in place | `examples/ch04/templating` |
| Passing values | step `set:` | step `vars:` | `examples/ch04/variables-local` |
| A step's result | `{{ step.field }}` | `{{ step.result }}` (text) | [5.3](ch05-03-results-and-references.md) |
| `next: name`, `next: [a, b]` | taken | **ignored** | `examples/ch06/next-names-ignored-local` |
| False step `when` | skip, follow its `next` | skip, **branch ends** | `examples/ch06/when-skip-local` |
| Undefined name in a guard | false | **true** | `examples/ch06/when-undefined-local` |
| Conditions | full Jinja | `==`, `!=`, `in`, truthy | [6.2](ch06-02-when-guards.md) |
| `loop:` | iterates | **runs once** | `examples/ch08/loop-runs-once` |
| Tool list (`task_sequence`) | one command | **parse error** | `examples/ch05/pipeline-refused-local` |
| `shell` field | `command:` | `cmds:` (`command:` ignored) | `examples/ch05/shell-command-local` |
| `case:` blocks | refused | still run | [4.3](ch04-03-steps.md) |
| Event trail | every pass | each step once | [Ch. 2](ch02-00-project-first-playbook.md) |

```admonish warning
Several of these differences fail **silently**: the run ends with
status `ok` and no warning. A playbook that "works locally" has been
checked against the local runtime, not against a server.
```

## Check your understanding

{{#quiz ../quizzes/ch08-01.toml}}
