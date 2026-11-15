# Event Sourcing: The Log Is the Truth

<span class="status status-real">REAL</span>

Every execution has an **event log**: a sequence of records, one for
each thing that happened. "The execution started." "This step's
command was issued." "A worker claimed it." "It completed with this
result." The log is **append-only**. Events are added and are never
edited or deleted. A server comment states the rule directly: the
event log "is append-only, immutable, and never purged"
(`src/services/secret_material.rs`, server v3.161.2). That is why
registration refuses inline secrets ([4.4](ch04-04-keychain.md)): once
something is in the log, it stays there.

## State is a fold over events

NoETL does not keep an "execution status" record that it updates in
place. When the orchestrator needs to decide what to do next, it is
handed the execution's **events** and the **playbook**, rebuilds the
execution's state from the events, and computes the next commands. The
input of the server's orchestration drive is exactly that:

```rust
pub struct OrchestrateInput {
    pub events: Vec<Event>,              // the execution's events
    pub playbook: Playbook,              // the blueprint
    pub trigger_event_type: Option<String>,
    // ...
}
```

(`plugins/orchestrate/src/lib.rs`, v3.161.2.) The output is the next
commands and the next events to append. Nothing else carries state
from one decision to the next. Even a `set:` value survives between
steps only because it is written into the log as a `ctx.updated`
event ([4.2](ch04-02-workload-and-templating.md)).

By default this drive runs as a WASM plug-in on a worker in the
system pool (`orchestrate_plugin_drive`, default `true`,
`src/config/app.rs`). The server keeps an in-process fallback. Both
run the same `orchestrate-core` code, which is why it can be compiled
to WASM at all: it is a pure function of its inputs.

## The events you will see

These event types appear in the server and orchestrator code at
v3.161.2, among others:

| Event | Records |
|---|---|
| `playbook.started` | the execution began |
| `step.enter` | a step was entered (dispatched) |
| `command.issued` | a command for a step was put on the command bus |
| `command.claimed`, `command.started` | a worker took it and began |
| `call.done` | the tool call returned |
| `command.completed`, `command.failed` | the command's outcome, with its result or error |
| `step.exit`, `step.skipped` | a step finished, or was not taken ([6.2](ch06-02-when-guards.md)) |
| `ctx.updated` | `set:` values were persisted |
| `playbook.completed`, `playbook.failed` | the execution's terminal outcome |

[Chapter 10](ch10-05-one-execution.md) follows one execution through
all of them, in order, on a real cluster.

## Why it matters to you

- **Replay.** Because state is computed from events, any past moment
  of an execution can be reconstructed by folding its events up to
  that point.
- **No hidden state.** If something is not in the log, the engine does
  not know it. A value a step computed but did not return, or `set`,
  is gone after the step.
- **Big things don't belong in it.** A step result travels in an
  event. Above 100 KiB it is moved out to the result store and
  referenced ([5.3](ch05-03-results-and-references.md)). Large data
  belongs in a data store a step reads and writes.

## Check your understanding

{{#quiz ../quizzes/ch03-02.toml}}
