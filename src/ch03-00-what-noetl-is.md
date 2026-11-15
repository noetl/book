# What NoETL Is

<span class="status status-real">REAL</span>

NoETL is a **declarative, event-sourced workflow engine**. You describe
a workflow as a playbook: steps, the tools they run, and the rules for
moving between them. NoETL runs it, and it records every transition as
an immutable event. The execution's state is never stored anywhere
else: it is computed from those events whenever it is needed.

The same playbook can run in three places: in-process on your machine
(the **local** runtime), as a long-running listener (the **daemon**),
or on a cluster of servers and workers (the **distributed** runtime).
Part III covers the three. This chapter covers the ideas they share:

- [3.1 Declarative orchestration](ch03-01-declarative-orchestration.md):
  you say what should happen, and the engine decides when.
- [3.2 Event sourcing](ch03-02-event-sourcing.md): the log is the
  truth.
- [3.3 Ephemeral blueprints and stateless workers](ch03-03-blueprints-and-workers.md):
  nothing stays resident between invocations.
- [3.4 Two catalogs](ch03-04-two-catalogs.md): NoETL's own objects
  versus your business data.

Each idea is tied to the code that implements it at **server v3.161.2**
(commit `983e36e`) and **worker v6.15.0**, or to the project's
written execution-model rule where the idea is a rule about how
features must be built.

## Check your understanding

{{#quiz ../quizzes/ch03-00.toml}}
