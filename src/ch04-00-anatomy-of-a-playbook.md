# Anatomy of a Playbook

<span class="status status-real">REAL</span>

A **playbook** is a YAML document that describes a workflow: a list of
steps, each of which runs one tool, plus the rules for moving from one
step to the next. NoETL reads the playbook, runs the steps, and records
every transition as an event. This chapter walks through every part of
the document. The next two chapters cover the tools a step can run
([Chapter 5](ch05-00-tools.md)) and how control moves between steps
([Chapter 6](ch06-00-control-flow.md)).

Everything in this chapter was checked against the grammar the NoETL
server publishes, `orchestrate-core/schema/playbook.schema.json`, at
**server v3.161.2** (commit `983e36e`, 2026-11-12), against the server's
validator (`src/playbook/parser.rs`) at the same commit, and against
the local runtime in **CLI v6.4.0**. The full key-by-key reference is
generated from that file in [Appendix A](appendix-01-dsl-reference.md).

## The whole thing on one page

Here is a complete playbook. Every example in this book is a file the
book's CI runs; this one is `examples/ch04/anatomy/playbook.yaml`.

```yaml
{{#include ../examples/ch04/anatomy/playbook.yaml}}
```

Run it with the local runtime:

```console
$ noetl run examples/ch04/anatomy/playbook.yaml -r local --json
```

The `--json` flag prints one result object on standard output. Among
its fields are the steps that ran, in order, and each step's result:

```json
{{#include ../examples/ch04/anatomy/expected.json}}
```

## Top-level keys

A playbook has eight top-level keys. Four are required.

| Key | Required | What it holds | Section |
|---|---|---|---|
| `apiVersion` | yes | The grammar version. Must be `noetl.io/v2`. | [4.1](ch04-01-header.md) |
| `kind` | yes | The document type. Must be `Playbook`. | [4.1](ch04-01-header.md) |
| `metadata` | yes | `name` (required), `path`, `description`, `labels`, and opt-in extensions | [4.1](ch04-01-header.md) |
| `workload` | | Inputs: values the steps read as `{{ workload.<key> }}` | [4.2](ch04-02-workload-and-templating.md) |
| `vars` | | Top-level variables | [4.2](ch04-02-workload-and-templating.md) |
| `workflow` | yes | **The list of steps** | [4.3](ch04-03-steps.md) |
| `keychain` | | How credential aliases are sourced | [4.4](ch04-04-keychain.md) |
| `workbook` | | Named, reusable tool definitions | [4.5](ch04-05-workbook.md) |

```admonish myth
"The steps go under `steps:`." There is no `steps:` key. The step list
is `workflow`. A playbook that uses `steps:` fails before it runs: the
local runtime reports ``missing field `workflow` `` and the schema
check reports `'workflow' is a required property`. The example
`examples/ch04/no-steps-key` checks both in CI.
```

## Two checks, at two different times

A playbook passes two kinds of check, and they are not run at the same
moment.

1. **The schema** (`playbook.schema.json`) checks *shape*: required
   keys, value types, and which `tool.kind` values exist. It is
   deliberately permissive in one way: **unknown keys are not
   rejected**. A misspelt optional key, such as `worklaod:`, is
   silently ignored rather than reported.
2. **The validator** in the server checks *meaning*. At v3.161.2,
   `validate_playbook` (`src/playbook/parser.rs:164`) requires:
   - `apiVersion` is exactly `noetl.io/v2`, and `kind` is exactly
     `Playbook`;
   - **a step named `start` exists**;
   - step names are unique;
   - every `next` target names a step that exists;
   - `when` and `loop.in` expressions are non-empty, and contain no
     stray `{` outside a `{{ … }}` (this is the whole check; the
     expression itself is not parsed until it runs);
   - a `loop` has a non-empty `iterator`, plus `in:` (or, for
     `mode: cursor`, a `cursor` block);
   - a pipeline (a list under `tool:`) has at least one task.

   It also refuses the old `case:` blocks outright.

The server runs the validator when an execution **starts**, not when a
playbook is registered. As the server's own comment puts it
(`src/handlers/dsl.rs:227`), "a document can register and still be
unexecutable". The server has a dry-run endpoint, `POST
/api/dsl/validate`, that runs both registration's checks and the
validator and lists every problem at once. It is mounted only when the
server sets `NOETL_DSL_KB=true`, which is off by default.

```admonish warning title="The local runtime is more forgiving"
The local runtime in CLI v6.4.0 does not run the server's validator.
It starts at the **first** step in `workflow`, whatever its name, and
does not require a `start` step. A playbook that runs locally can
therefore still be refused by a server. Name your first step `start`
and it works in both places. [Chapter 8](ch08-00-local-runtime.md)
lists every difference.
```

## Check your understanding

{{#quiz ../quizzes/ch04-00.toml}}
