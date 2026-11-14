# Iterating Without `loop:` — Arcs, SQL and Rhai

<span class="status status-real">REAL</span>

```admonish myth
"The local runtime runs `loop:`." At CLI v6.4.0 it parses `loop:` into
`Step.loop_config`, and **nothing reads that field**
(`git grep loop_config` finds only its declaration). A loop step runs
**once**, as if `loop:` were absent, and the run ends `ok` with no
warning. CI checks this: `examples/ch08/loop-runs-once`.
```

The reference page `docs/reference/rust_local_execution.md` in
`noetl/docs` lists `step.loop` under "current DSL semantics (what local
mode must preserve)". That is a requirement, and at v6.4.0 the code
does not meet it.

Three ways to iterate locally actually work. All three are CI
examples.

## 1. A back-edge with a `when` guard

Route back to an earlier step until a counter reaches its limit. The
counter travels in step `vars:` locally ([6.4](ch06-04-back-edges.md),
`examples/ch06/back-edge-local`; [Chapter 2](ch02-00-project-first-playbook.md)
uses one too). Each pass is a full step, and the guard is the only
thing that stops it.

## 2. Set-based SQL in one `duckdb` step

When the work is "do this to every item", let one query do it:

```yaml
{{#include ../examples/ch08/iterate-sql/playbook.yaml}}
```

```json
{{#include ../examples/ch08/iterate-sql/expected.json}}
```

This is usually the best choice: one step, no orchestration per item,
and the database does the iteration. The list goes in as a bound
parameter and `unnest(from_json(…))` turns it into rows.

## 3. A loop inside one `rhai` step

```yaml
{{#include ../examples/ch08/iterate-rhai/playbook.yaml}}
```

```json
{{#include ../examples/ch08/iterate-rhai/expected.json}}
```

Rhai has `for`, `while` and arrays. Use it for small in-memory
transformations. Rhai has no default timeout and no operation limits
([Appendix B](appendix-02-tool-kinds.md)), so keep the loop bounded.

## Which to use

| Need | Use |
|---|---|
| A per-item side effect (an HTTP call per item) | a back-edge |
| Transform or aggregate a collection | set-based SQL |
| A small in-memory computation | Rhai |
| The same playbook must also run on a server | write `loop:` for the server and test it there. Locally it runs once. |

## Check your understanding

{{#quiz ../quizzes/ch08-03.toml}}
