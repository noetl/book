# Ephemeral Blueprints and Stateless Workers

<span class="status status-real">REAL</span>

Two words describe how NoETL is built: **blueprint** and **worker**.

## Playbooks are blueprints

A playbook is control flow and policy for one request. It is invoked
on demand, and it holds no state between invocations beyond what the
event log records. Nothing of a playbook "runs" while no execution of
it is in progress. There is no resident process per playbook, and no
long-lived agent or MCP server sitting inside NoETL waiting for work.
When a playbook is published as an MCP tool or an agent
([Chapter 18](ch18-00-mcp-and-agents.md)), each call is a new
execution of the blueprint.

## Workers are stateless compute

A worker is a process with a fixed number of **slots**
(`WORKER_MAX_CONCURRENT`, default 4, resource model DEFAULT). For each
slot it repeats one cycle:

1. **claim** one command from the command bus;
2. **run** that command's tool, the step's single tool or a whole tool
   list ([5.2](ch05-02-ordered-tool-list.md));
3. **emit** the outcome as events;
4. **release** the slot.

The slot is held from claim until the tool returns (resource model
`slot_rule`, citing worker v6.15.0 `src/worker.rs`). The worker keeps
nothing about the execution between commands. The next command of
the same execution may run on any worker.

## Where data access happens

The project's execution-model rule (in `noetl/ai-meta`,
`agents/rules/execution-model.md`) states the shape every feature
must keep:

- **All data access happens inside playbook steps.** A read, a write,
  a third-party API call: each is a tool in a step, under that
  playbook's policy. Clients never reach a database directly.
- **The gateway is a gatekeeper only.** It authenticates and routes
  requests and delivers results; it never reads or writes domain data
  on a client's behalf ([Chapter 10](ch10-01-gateway.md)).
- **NoETL's own tables are reached through the server's API.** Workers
  call the server rather than holding their own connections to
  NoETL's database.

These are design rules. They describe how the system is meant to be
built, and code review enforces them. When this book finds code that
does not follow one, the chapter says so. Ch. 4.4's postgres default
connection is one such case.

## Check your understanding

{{#quiz ../quizzes/ch03-03.toml}}
