# Hello, Playbook

<span class="status status-real">REAL</span>

A playbook is a YAML file. This is the smallest valid one: the four
required keys, and a workflow with one step.

```yaml
{{#include ../examples/ch01/minimal/playbook.yaml}}
```

- `apiVersion: noetl.io/v2` and `kind: Playbook` say what the document
  is. They are the only accepted values.
- `metadata.name` names it.
- `workflow` is the list of steps. Each step has a name (`step`) and a
  `tool`. Here the tool is `rhai`, a small embedded scripting
  language, and the step's result is the value of its last
  expression.
- The first step is called `start`. A NoETL server always begins an
  execution at `start`, so name your first step that.

[Chapter 4](ch04-00-anatomy-of-a-playbook.md) covers every key.

## Adding an input and a second step

```yaml
{{#include ../examples/ch01/hello/playbook.yaml}}
```

- `workload` holds the playbook's inputs, with defaults. A template
  reads them: `{{ workload.who }}`.
- `next` sends control from `start` to `done` when `start` finishes.
- The first step runs a **shell** command. Locally the commands go
  under `cmds:`. On a cluster the shell tool's field is `command:`
  instead ([5.1](ch05-01-tool-kinds.md)). This example is for the
  local runtime.

## Check your understanding

{{#quiz ../quizzes/ch01-02.toml}}
