# Appendix F: Myths and Corrections

<span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this section are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md).

## Corrections recorded so far

Rows are added as each page that corrects a myth lands. The full
appendix is written in [#45](https://github.com/noetl/book/issues/45).

| Myth | Fact | Verified at | Checked by | Page |
|---|---|---|---|---|
| The local runtime runs a `loop:` step once per item. | It parses `loop:` and runs the step **once**; the run ends `ok` with no warning. | CLI v6.4.0: `Step.loop_config` (`executor/src/playbook.rs`) has no reader | `examples/ch08/loop-runs-once` (CI) | [Appendix H](appendix-08-contributing.md) |
| The step list goes under `steps:`. | There is no `steps:` key; `workflow` is the step list. A playbook with `steps:` fails: ``missing field `workflow` ``. | server v3.161.2 `playbook.schema.json` (required: `workflow`); CLI v6.4.0 | `examples/ch04/no-steps-key` (CI) | [Ch. 4](ch04-00-anatomy-of-a-playbook.md) |
| Registering a playbook validates it. | Registration checks tool kinds and inline secrets only; the validator (`start` step, unique names, `next` targets) runs when an execution starts. | server v3.161.2 `src/handlers/dsl.rs:227`, `src/services/catalog.rs` `registration_checks` | code read | [Ch. 4](ch04-00-anatomy-of-a-playbook.md) |
| Use step `vars:` to pass a value to the next step. | Only the local runtime reads step `vars:`. On a server nothing reads step or top-level `vars:`; use `set:`. | server v3.161.2 (no reader of `Step.vars`); CLI v6.4.0 | `examples/ch04/variables-local` (CI, local side) | [Ch. 4.2](ch04-02-workload-and-templating.md) |
| The local runtime renders templates like the server does. | Locally it is token substitution: exactly `{{ name }}`, four filters, unknown names left in place. The server uses minijinja, where undefined renders empty. | CLI v6.4.0 `executor/src/template.rs`; server v3.161.2 `orchestrate-core/src/template.rs` | `examples/ch04/templating` (CI) | [Ch. 4.2](ch04-02-workload-and-templating.md) |
| There is no default database connection. | It is a convention, not enforced: a `postgres` step with no `auth` connects to `localhost:5432` as `postgres`. | tools v4.6.0 `src/tools/postgres.rs` `build_connection_string`; worker v6.15.0 `src/executor/auth_alias.rs` | code read | [Ch. 4.4](ch04-04-keychain.md) |
