# Appendix G: Glossary

<span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this section are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md).

## Terms defined so far

Terms are added as the chapters that define them land. The full
glossary is [#50](https://github.com/noetl/book/issues/50).

| Term | Meaning | Defined in |
|---|---|---|
| playbook | A YAML document (`kind: Playbook`, `apiVersion: noetl.io/v2`) describing a workflow of steps | [Ch. 4](ch04-00-anatomy-of-a-playbook.md) |
| step | One named entry of `workflow`: runs one tool, then routes with `next` | [4.3](ch04-03-steps.md) |
| `start` | The step every server execution begins with; the validator requires it | [4.3](ch04-03-steps.md) |
| workload | A playbook's inputs, read as `{{ workload.<key> }}`, overridable per run | [4.2](ch04-02-workload-and-templating.md) |
| template | A `{{ … }}` expression in a string; minijinja on the server, token substitution locally | [4.2](ch04-02-workload-and-templating.md) |
| `set:` | Server-side step mutations, persisted as a `ctx.updated` event | [4.2](ch04-02-workload-and-templating.md) |
| keychain alias | The name a playbook uses for a credential; resolved by the worker at run time | [4.4](ch04-04-keychain.md) |
| workbook | Named, reusable tool definitions a step references with `kind: workbook` | [4.5](ch04-05-workbook.md) |
| tool / kind | What a step runs; `kind` names the tool (`http`, `python`, …) | [Ch. 5](ch05-00-tools.md) |
| gated kind | A kind refused unless a server flag turns it on (`agent`, `mcp`) | [5.1](ch05-01-tool-kinds.md) |
| slot | A worker's unit of concurrency; a command holds one from claim until its tool returns | [Ch. 5](ch05-00-tools.md) |
| `task_sequence` | The single command a `tool:` list becomes; runs its sub-tasks in order on one worker | [5.2](ch05-02-ordered-tool-list.md) |
| label | A sub-task's name in a tool list; later items read its result as `{{ <label>.field }}` | [5.2](ch05-02-ordered-tool-list.md) |
| result store | Where a step result above 100 KiB is spilled; the event then carries a reference | [5.3](ch05-03-results-and-references.md) |
