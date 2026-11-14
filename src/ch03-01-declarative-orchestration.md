# Declarative Orchestration

<span class="status status-real">REAL</span>

In an imperative workflow, a script calls each task in turn: it
decides the order as it goes, it holds the state in its variables,
and if it crashes, the state dies with it. In NoETL the playbook does
not call anything. It **declares**:

- the steps and the tool each one runs ([Chapter 5](ch05-00-tools.md));
- the arcs between steps and their `when` guards
  ([Chapter 6](ch06-00-control-flow.md));
- inputs (`workload`) and credential references (`keychain`)
  ([Chapter 4](ch04-00-anatomy-of-a-playbook.md)).

The **orchestrator** decides what runs and when. On a server it is
`orchestrate-core`'s `WorkflowOrchestrator`. Each time something
happens, such as an execution starting or a step finishing, it looks
at the playbook and the execution's history, and returns the next
commands to dispatch. It does no work itself, and it keeps no memory
of its own between calls.

That split has consequences you will meet throughout the book:

- **Order comes from arcs, not from position.** A step's place in
  `workflow` does not decide when it runs ([4.3](ch04-03-steps.md)).
- **Steps dispatched together run together.** If two arcs are taken
  in the same pass, both steps run at once on different workers
  ([6.0](ch06-00-control-flow.md)).
- **The engine needs nothing from the run but its events.** Any
  orchestrator instance can take the next decision for any execution,
  because the decision depends only on the playbook and the event
  history (next section).

```admonish note
Declarative does not mean "anything you write is honoured". Several
keys in the grammar are parsed and then ignored at the versions this
book covers: `max_in_flight`, `spec.on_error`, `spec.timeout` and
`tool.eval`, for example ([6.5](ch06-05-errors-timeouts-retries.md)). The
grammar says what is accepted; the chapters say what is applied.
```

## Check your understanding

{{#quiz ../quizzes/ch03-01.toml}}
