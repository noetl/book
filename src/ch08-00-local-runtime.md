# The Local Runtime: `noetl run`

<span class="status status-real">REAL</span>

The **local runtime** runs a playbook inside the `noetl` CLI process,
with no server, no bus and no workers. It is the fastest way to try a
playbook, and it is how the book's CI runs its examples. It is also a
**different implementation** from the server's: it parses the same
grammar, but it supports fewer tool kinds, ignores some keys, and has
its own template and condition rules. This chapter is the complete
list of those differences at **CLI v6.4.0**. Every claim here is
either a CI example or a line of the CLI's source at that tag.

## Which runtime runs a playbook

`noetl run <ref>` picks its runtime with a three-rung ladder
(`resolve_runtime`, `src/lib.rs`, CLI v6.4.0):

1. **`-r` / `--runtime`**, if it is `local` or `distributed`. The value
   `auto`, which is also the default, means "not set".
2. Otherwise, the **active context's** `runtime`, unless that is `auto`
   or unset. Contexts are managed with `noetl context`.
3. Otherwise, **local**.

Every run prints its choice and where it came from on standard error,
for example `runtime: local (default)`, `runtime: local (--runtime
flag)` or `runtime: distributed (from context 'prod')`. A stale
context therefore never silently sends a run to a server.

The `<ref>` can be a file path, a `catalog://name@version` reference or
a catalog id. The local runtime runs **files**. A catalog reference
needs `-r distributed`.

## What the local runtime is good for

- learning the DSL, and fast iteration on control flow;
- playbooks built from `http`, `duckdb`, `rhai`, `shell` and `playbook`
  steps that run on one machine;
- CI checks of playbook logic, as this book does.

What it is not: a way to test a cluster playbook end to end. Sections
[8.2](ch08-02-local-kinds.md) and [8.3](ch08-03-local-iteration.md)
show why.

## Sections

- [8.1 One process, one interpreter](ch08-01-in-process-interpreter.md)
- [8.2 Local tool kinds and their limits](ch08-02-local-kinds.md)
- [8.3 Iterating without `loop:`](ch08-03-local-iteration.md)
- [8.4 The local event buffer and `noetl push`](ch08-04-event-buffer.md)

## Check your understanding

{{#quiz ../quizzes/ch08-00.toml}}
