# `workbook`: Reusable Tasks

<span class="status status-real">REAL</span>

When several steps run the same tool with mostly the same
configuration, define it once in `workbook` and refer to it by name.

```yaml
workbook:
  - name: fetch_rates
    tool:
      kind: http
      method: GET
      url: https://api.example.com/v1/rates
      args:
        currency: USD

workflow:
  - step: start
    tool:
      kind: workbook
      name: fetch_rates          # the workbook entry to use
      args:
        currency: EUR            # overrides the entry's default
    next:
      - step: done
  - step: done
    tool:
      kind: noop
```

## How a reference is resolved

The server resolves references when it parses the playbook, before
validating it (`resolve_workbook_references`,
`src/playbook/parser.rs`, server v3.161.2). For every step whose
`tool.kind` is `workbook`:

1. It looks up the entry whose `name` matches the step's `tool.name`.
   A step without `name` is an error (``tool.kind=workbook requires a
   'name' field``), and so is an unknown name. That error lists the
   names that do exist.
2. It **replaces** the step's tool with the entry's tool, so the step
   above runs `kind: http`.
3. It merges the step's `args` over the entry's `args`, key by key, and
   the step's value wins. `input:` is accepted as another name for
   `args`. If either side is not a map, the step's `args` replace the
   entry's entirely.

What a tool then does with its `args` depends on the kind. A `python`
step, for example, sees them as an `args` dict
([Chapter 5](ch05-00-tools.md)). The workbook only decides which
`args` the tool receives.

From then on, nothing else in the system knows a workbook was
involved. The orchestrator and the worker see an ordinary `http` step.

Each entry has a `name`, a single `tool`, and an optional `sink`. An
entry holds one tool, not a list, so an ordered tool list
([5.2](ch05-02-ordered-tool-list.md)) cannot live in a workbook entry.

```admonish warning title="Not on the local runtime"
At CLI v6.4.0 the local runtime does not accept `kind: workbook`. A
playbook that uses it is refused before any step runs, with the list
of kinds the local runtime supports.
```

## Check your understanding

{{#quiz ../quizzes/ch04-05.toml}}
