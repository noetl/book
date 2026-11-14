# Appendix G: Glossary

<span class="status status-real">REAL</span>

Each term links to the section that defines it. The glossary grows with
the book: every chapter that introduces a term adds it here in the same
pull request ([#50](https://github.com/noetl/book/issues/50)). Chapters
not written yet have not added their terms.

| Term | Meaning | Defined in |
|---|---|---|
| arc | One outgoing transition in `next`, optionally guarded by `when` | [6.1](ch06-01-next-and-routers.md) |
| back-edge | An arc to a step that has already run; forms a loop bounded only by its `when` | [6.4](ch06-04-back-edges.md) |
| exclusive / inclusive | Routing modes: first matching arc vs every matching arc (default exclusive) | [6.1](ch06-01-next-and-routers.md) |
| gated kind | A kind refused unless a server flag turns it on (`agent`, `mcp`) | [5.1](ch05-01-tool-kinds.md) |
| keychain alias | The name a playbook uses for a credential; resolved by the worker at run time | [4.4](ch04-04-keychain.md) |
| label | A sub-task's name in a tool list; later items read its result as `{{ <label>.field }}` | [5.2](ch05-02-ordered-tool-list.md) |
| orchestration pass | The server's evaluation of arcs, triggered by a completion event | [Ch. 6](ch06-00-control-flow.md) |
| playbook | A YAML document (`kind: Playbook`, `apiVersion: noetl.io/v2`) describing a workflow of steps | [Ch. 4](ch04-00-anatomy-of-a-playbook.md) |
| policy rules | `spec.policy.rules` on a tool-list sub-task: continue, retry, jump, break, fail | [6.5](ch06-05-errors-timeouts-retries.md) |
| result store | Where a step result above 100 KiB is spilled; the event then carries a reference | [5.3](ch05-03-results-and-references.md) |
| `set:` | Server-side step mutations, persisted as a `ctx.updated` event | [4.2](ch04-02-workload-and-templating.md) |
| slot | A worker's unit of concurrency; a command holds one from claim until its tool returns | [Ch. 5](ch05-00-tools.md) |
| `start` | The step every server execution begins with; the validator requires it | [4.3](ch04-03-steps.md) |
| step | One named entry of `workflow`: runs one tool, then routes with `next` | [4.3](ch04-03-steps.md) |
| `step.skipped` | The event recorded for a target not taken, or a step whose guard was false | [6.2](ch06-02-when-guards.md) |
| `task_sequence` | The single command a `tool:` list becomes; runs its sub-tasks in order on one worker | [5.2](ch05-02-ordered-tool-list.md) |
| template | A `{{ … }}` expression in a string; minijinja on the server, token substitution locally | [4.2](ch04-02-workload-and-templating.md) |
| tool / kind | What a step runs; `kind` names the tool (`http`, `python`, …) | [Ch. 5](ch05-00-tools.md) |
| workbook | Named, reusable tool definitions a step references with `kind: workbook` | [4.5](ch04-05-workbook.md) |
| workload | A playbook's inputs, read as `{{ workload.<key> }}`, overridable per run | [4.2](ch04-02-workload-and-templating.md) |

## Check your understanding

{{#quiz ../quizzes/appendix-g.toml}}
