# Tools

<span class="status status-real">REAL</span>

Every step runs a **tool**: a piece of work of a given `kind`, such as
an HTTP request, a SQL query, a Python script or a call to another
playbook. NoETL itself does no work in a step. It decides *which*
step runs next, and hands the step's tool to a worker, which runs it
and reports the result back as an event.

```yaml
- step: start
  tool:
    kind: http          # which tool
    method: GET         # the tool's own fields
    url: https://api.example.com/v1/items
```

A step's `tool` is one of two things:

- **one tool**, a map with a `kind` (sections [5.1](ch05-01-tool-kinds.md)
  and [5.3](ch05-03-results-and-references.md)); or
- **an ordered list of tools**, run one after another as a single unit
  of work ([5.2](ch05-02-ordered-tool-list.md)).

Three facts shape everything in this chapter. They are checked at
server v3.161.2, worker v6.15.0 and tools v4.6.0, the tool library
that worker version uses:

1. **A step holds one worker slot from the moment it is claimed until
   its tool returns.** Waiting inside a tool keeps the slot: an awaited
   sub-playbook, a polled Kubernetes Job, an LLM call. (Resource
   model `step_kinds.slot_rule`, DEFAULT; worker `src/worker.rs`.)
2. **The worker sets no wall-clock timeout on a command.** A step is
   bounded only by its own tool's timeout, and several kinds have
   none by default (`step_kinds.no_global_timeout`, DEFAULT).
3. **Tools do not retry by themselves.** A retry configuration exists
   in the tool library, but no executor applies it
   (`step_kinds.retry_config_inert`, DEFAULT). Section
   [6.5](ch06-05-errors-timeouts-retries.md) covers what *does* retry.

## Check your understanding

{{#quiz ../quizzes/ch05-00.toml}}
