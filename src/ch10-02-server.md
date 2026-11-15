# Server: The Orchestrate-Core Drive

<span class="status status-real">REAL</span>

The server is the control plane. It owns the event log, the catalog and
the command records, and it is the only service that talks to NoETL's
own Postgres schema. It **runs no tools**: the tools registry is kept
off it on purpose (`Cargo.toml`, "must not land on the control plane").
Everything here is server **v3.161.2**.

## What happens on `POST /api/execute`

The handler is `execute_one` (`src/handlers/execute.rs`). In order, it:

1. resolves the playbook from the catalog and parses it, and merges the
   request's workload into the playbook's;
2. writes the first event, **`playbook_started`**
   (`execute.rs:948-1018`);
3. builds the **first commands itself**, in process, with
   orchestrate-core's `CommandBuilder` (`generate_initial_commands`,
   `execute.rs:1667-1876`);
4. for each command, writes a **`command.issued`** event and a
   `noetl.command` row, then publishes a notification to the command bus
   (`execute.rs:1286`, `1883-1933`, `1952`).

The pool the notification goes to is chosen here, once, for the whole
execution ([10.3](ch10-03-bus-and-pools.md#which-pool-runs-a-step)).

## The drive

After the first commands, every decision is made by a **drive pass**.
One pass is a pure function:

| In | Out |
|---|---|
| the playbook, and the `WorkflowState` folded from the execution's events | the next commands, events to emit, and whether the execution is complete |

(`evaluate_state`, `orchestrate-core/src/orchestrator.rs:384`; the
result type is `OrchestrationResult`, `:290-302`.) The same crate is the
reducer that folds events into state (`WorkflowState::apply_event`,
`orchestrate-core/src/state.rs:519`).

A pass is triggered when a worker reports `command.completed` or
`command.failed` (`src/handlers/events.rs:769-779`).

## Where the drive runs

```admonish myth
"The server runs the orchestrator." By default it does not. It issues
the drive as a **command**, step name `__orchestrate__`, that runs the
`system/orchestrate` WASM plug-in on a worker in the **system** pool
(`dispatch_orchestrate_command`, `execute.rs:1568-1650`). The switch is
`NOETL_ORCHESTRATE_PLUGIN_DRIVE`, **default `true`**
(`src/config/app.rs:70-87`). Set to `false`, the server drives in
process instead (`events.rs:4018`).
```

When the plug-in finishes, its result comes back on the meta-step's
`call.done`. The server applies it: emits the events, issues the
commands as a batch, and writes `playbook.completed` or
`playbook.failed` when the pass says the execution is done
(`apply_worker_orchestration`, `events.rs:4163-4200`).

The drive leaves **no trace in the event log**. Its command writes no
`command.issued` (`execute.rs:1603`: "The meta-command writes NOTHING
to noetl.event"), and its lifecycle events are not stored
(`events.rs:676-711`). The state is a function of the real step events,
so storing the drive's own would only add load.

```admonish note title="Two consequences"
- The **system pool is on every execution's critical path**. A user
  step waits for a system-pool slot between steps ([10.4](ch10-04-slots-and-keda.md)).
- The **first** commands are built by the server, not by the drive. A
  bug that shows up only on the first step and not later ones is
  looking at two different code paths.
```

## The events of a one-step execution

For a playbook whose `start` step has no `next`, with default flags,
the stored events are, in order:

| # | Event | Written by | Where |
|---|---|---|---|
| 1 | `playbook_started` | server | `execute.rs:1006` |
| 2 | `command.issued` (step `start`) | server | `execute.rs:1286` |
| 3 | `command.claimed` | server, in the claim handler | `events.rs:1177` |
| 4 | `command.started` | worker | worker `src/executor/command.rs:547` |
| 5 | `call.done` | worker | `command.rs:1099` |
| 6 | `command.completed` | worker | `command.rs:3679-3689` |
| 7 | `playbook.completed` | server, applying the drive's result | `events.rs:4184` |

Between 6 and 7 the drive ran on the system pool and stored nothing.
There is no `step.enter` for a start step that does not loop
(`execute.rs:1778`). The names are not uniform: `playbook_started` has
an underscore and `playbook.completed` a dot. The reducer matches
`playbook_started` and both spellings of each terminal event
(`state.rs:528-550`).

Workers write their events through the server's API
(`POST /api/events`, worker `src/client/control_plane.rs:577`). No
worker connects to NoETL's Postgres.

## Check your understanding

{{#quiz ../quizzes/ch10-02.toml}}
