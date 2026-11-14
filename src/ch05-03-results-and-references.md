# Results, References and Size Limits

<span class="status status-real">REAL</span>

When a tool finishes, the worker reports its **result** in an event.
Later steps read that result through templates. This section covers
what a result looks like to a template, and what happens when a result
is too big to travel in an event.

## Reading a result on the server

The worker wraps a tool's output in an envelope: status, data, stdout,
stderr and so on. The server unwraps the **data** part
(`extract_user_data`, `orchestrate-core/src/state.rs`, v3.161.2) and
exposes it to later templates under the step's name:

| Write | To get |
|---|---|
| `{{ fetch_user.email }}` | the field `email` of step `fetch_user`'s data |
| `{{ fetch_user.data.email }}` | the same thing (an alias, so both spellings work) |
| `{{ steps.fetch_user }}` | the full envelope, status included |
| `{{ output.email }}` | inside `fetch_user`'s own `set:` and `next` arcs: its data |

To keep a value as a named variable, use `set:` on the step
([4.2](ch04-02-workload-and-templating.md)):

```yaml
- step: fetch_user
  tool:
    kind: http
    method: GET
    url: "https://api.example.com/v1/users/{{ workload.user_id }}"
  set:
    ctx.email: "{{ output.email }}"     # later: {{ email }}
  next:
    - step: notify
```

A loop step's result is a **list**, one entry per iteration, in the
order the iterations *finished*, which in parallel mode need not be
the order they started ([6.3](ch06-03-loop.md)). A tool list's result
is a map keyed by label ([5.2](ch05-02-ordered-tool-list.md)).

## Reading a result locally

The local runtime (CLI v6.4.0) keeps each step's result as **text**:

- `{{ fetch_user.result }}` is the whole result as a string;
- inside that step's own `vars:`, `{{ result.email }}` reads a field
  of the result, if it parses as JSON.

So `{{ fetch_user.email }}`, the server form, is left unrendered
locally, and `{{ fetch_user.result }}`, the local form, renders empty
on a server. [Chapter 8](ch08-00-local-runtime.md) has the full list
of differences.

## Size limits

A step's result travels in an event, and a step's command carries a
rendered context. Both have size limits. Above them, the data moves
**by reference** instead of inline. All values are code defaults from
the resource model at v3.161.2; a deployment may override them.

| What | Limit | Setting | Above the limit |
|---|---|---|---|
| A step result in an event | **100 KiB** (102,400 bytes) | `NOETL_EVENT_RESULT_CONTEXT_MAX_BYTES` (worker) | spilled to the result store and replaced by a reference, so a later read costs a fetch |
| A command's context | **512 KiB** (524,288 bytes) | `NOETL_COMMAND_CONTEXT_MAX_BYTES` (server) | offloaded as a `__context_ref__` |
| A request body to `/api/execute` or `/api/events` | **2 MiB** (2,097,152 bytes) | none: the HTTP framework's default | the request is refused |

Each is labelled **DEFAULT** in the resource model
([Appendix D](appendix-04-resource-model.md)), with sources
worker `src/executor/command.rs` and server `src/config/app.rs`,
`src/main.rs`.

Two practical consequences:

- Returning a large payload from a step is not free. Every later read
  of it fetches it back. If a later step needs only a count or an id,
  return just that.
- Large data belongs in a data store that a step writes to and the
  next step reads from: a table, a bucket, a DuckDB file. Do not pass
  it through results. This is also the execution model's rule: data
  access happens inside steps, and the event log records what
  happened, not the data itself ([Chapter 3](ch03-00-what-noetl-is.md)).

## Check your understanding

{{#quiz ../quizzes/ch05-03.toml}}
