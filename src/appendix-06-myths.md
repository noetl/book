# Appendix F: Myths and Corrections

<span class="status status-real">REAL</span>

Each row is a belief about NoETL that is wrong, or was true once, and
the fact that replaces it. Every **Truth** was checked at the source
named, and the **Checked by** column says how: a CI example (re-run on
every pull request, so the row breaks if the behaviour changes), or a
reading of the code at that release. Rows are grouped by the chapter
that teaches the truth.

Found a myth that is not here? Open an issue; Appendix H explains how
a correction gets into the book.

| Myth | Truth | Source | Checked by | Chapter |
|---|---|---|---|---|
| The local event trail records every run of every step. | It records one `step.exit` per step, at its first run; a back-edge loop's later passes are missing (as are they from `executed_steps`). | CLI v6.4.0 (`ExecutionContext::set_step_result`, `src/playbook_runner.rs`) | run of `examples/ch02/fetch-transform-store` with `--event-buffer` | [Ch. 2](ch02-00-project-first-playbook.md) |
| The step list goes under `steps:`. | There is no `steps:` key; `workflow` is the step list. A playbook with `steps:` fails: ``missing field `workflow` ``. | server v3.161.2 `playbook.schema.json` (required: `workflow`); CLI v6.4.0 | `examples/ch04/no-steps-key` (CI) | [Ch. 4](ch04-00-anatomy-of-a-playbook.md) |
| Registering a playbook validates it. | Registration checks tool kinds and inline secrets only; the validator (`start` step, unique names, `next` targets) runs when an execution starts. | server v3.161.2 `src/handlers/dsl.rs:227`, `src/services/catalog.rs` `registration_checks` | code read | [Ch. 4](ch04-00-anatomy-of-a-playbook.md) |
| Use step `vars:` to pass a value to the next step. | Only the local runtime reads step `vars:`. On a server nothing reads step or top-level `vars:`; use `set:`. | server v3.161.2 (no reader of `Step.vars`); CLI v6.4.0 | `examples/ch04/variables-local` (CI, local side) | [Ch. 4.2](ch04-02-workload-and-templating.md) |
| The local runtime renders templates like the server does. | Locally it is token substitution: exactly `{{ name }}`, four filters, unknown names left in place. The server uses minijinja, where undefined renders empty. | CLI v6.4.0 `executor/src/template.rs`; server v3.161.2 `orchestrate-core/src/template.rs` | `examples/ch04/templating` (CI) | [Ch. 4.2](ch04-02-workload-and-templating.md) |
| There is no default database connection. | It is a convention, not enforced: a `postgres` step with no `auth` connects to `localhost:5432` as `postgres`. | tools v4.6.0 `src/tools/postgres.rs` `build_connection_string`; worker v6.15.0 `src/executor/auth_alias.rs` | code read | [Ch. 4.4](ch04-04-keychain.md) |
| Each tool in a `tool:` list is dispatched separately, so a list spreads work across workers. | A tool list is ONE `task_sequence` command on one worker in one slot; its sub-tasks run sequentially inside it. | server v3.161.2 `orchestrate-core/src/commands.rs` `build_tool_from_definition`; tools v4.6.0 `task_sequence.rs` | code read | [Ch. 5.2](ch05-02-ordered-tool-list.md) |
| NoETL dropped Python, so `kind: python` is gone. | The Python *platform* was retired (noetl/noetl `25bef859`); `kind: python` is a worker kind (a `python3` subprocess). Only the local runtime lacks it. | tools v4.6.0 `src/tools/python.rs`; CLI v6.4.0 | `examples/ch08/python-refused` (CI) | [Ch. 5.1](ch05-01-tool-kinds.md) |
| A `shell` step works the same on both runtimes. | Workers read `command:`; the local runtime reads `cmds:` and silently ignores `command:` (the step runs nothing, the run ends `ok`). | tools v4.6.0 `ShellConfig`; CLI v6.4.0 `Tool::Shell` | `examples/ch05/shell-command-local` (CI) | [Ch. 5.1](ch05-01-tool-kinds.md) |
| `next: [{step: a}, {step: b}]` runs both. | A list of targets is exclusive by default: only `a` runs. `next: [a, b]` (names) fans out. | server v3.161.2 `orchestrate-core/src/evaluator.rs` | `examples/ch06/next-targets` (CI, same on local) | [Ch. 6.1](ch06-01-next-and-routers.md) |
| `loop.spec.max_in_flight` throttles a parallel loop. | It is parsed and nothing reads it; parallel mode dispatches every item at once. | server v3.161.2 (`orchestrator.rs` `dispatch_count`; no reader of `max_in_flight`); resource model | code read | [Ch. 6.3](ch06-03-loop.md) |
| `spec.on_error: retry` / `retry:` / `tool.eval` retries a failed step. | None is applied. Only `spec.policy.rules` inside a tool list retries. | server v3.161.2, worker v6.15.0, tools v4.6.0 (no readers); tools `task_sequence.rs` | code read | [Ch. 6.5](ch06-05-errors-timeouts-retries.md) |
| `spec.timeout` limits a step. | No reader; the worker sets no command timeout. Only a tool's own timeout applies. | server v3.161.2 `StepSpec`; resource model `no_global_timeout` | code read | [Ch. 6.5](ch06-05-errors-timeouts-retries.md) |
| The server caps loop iterations / back-edge re-runs. | No cap exists; the playbook's `when` is the only bound. The only iteration cap is inside one tool list. | server v3.161.2, worker v6.15.0, tools v4.6.0 (grep for limits) | code read | [Ch. 6.4](ch06-04-back-edges.md) |
| If no arc matches, the execution just ends. | A step that has arcs, none taken, is not an ending: the execution stalls with no terminal event (sweep off by default). | server v3.161.2 `check_completion`; `src/handlers/nonconvergence_sweep.rs` | code read | [Ch. 6.0](ch06-00-control-flow.md) |
| The local runtime routes like the server. | Locally `next: name` and `next: [names]` are ignored, a false step `when` ends the branch, and an undefined name in a guard is truthy. | CLI v6.4.0 | `examples/ch06/next-names-ignored-local`, `when-skip-local`, `when-undefined-local` (CI) | [Ch. 6.1](ch06-01-next-and-routers.md), [6.2](ch06-02-when-guards.md) |
| The local runtime can run `postgres` steps. | It refuses `kind: postgres` (and `python`) before any step runs: "Run it on a cluster instead". | CLI v6.4.0 `reject_unsupported_kinds` (`src/playbook_runner.rs`) | `examples/ch08/postgres-refused` (CI) | [Ch. 8](ch08-00-local-runtime.md) |
| Worker autoscaling (KEDA) reads NATS consumer lag. | NATS was removed. The deployed trigger is `ehdb_feed_subject_lag{subject="commands.shared.shard.0"}` from the command-bus writer, `replicas ≈ ceil(lag / 2)`, 2–20 replicas. | server v3.161.2 resource model `concurrency.autoscaling.deployed` (DEPLOYED, as of 2026-11-11) | resource-model read | [Ch. 10.4](ch10-04-slots-and-keda.md) |
| ehgraph stores its graphs in EHDB. | It does not: EHDB is a design reference for its change-log format only, and no ehgraph crate depends on EHDB. | noetl/ehgraph `f200516` README ("never stores graph data in an EHDB dataset"), `Cargo.toml` (no ehdb dependency) | code read | [Ch. 15](ch15-00-ehgraph.md) |
| The local runtime runs a `loop:` step once per item. | It parses `loop:` and runs the step **once**; the run ends `ok` with no warning. | CLI v6.4.0: `Step.loop_config` (`executor/src/playbook.rs`) has no reader | `examples/ch08/loop-runs-once` (CI) | [Appendix H](appendix-08-contributing.md) |

Not yet added: the edge-compilation myth (planned for Ch. 23), which needs its source verified first.

## Check your understanding

{{#quiz ../quizzes/appendix-f.toml}}
