# Composition: Sub-Playbooks

<span class="status status-real">REAL</span>

A step can run **another playbook**. That is how NoETL composes larger
workflows from smaller ones, and how one playbook reuses another, such
as a provider integration, an MCP wrapper or a shared clean-up. The tool
is `kind: playbook`.

This chapter covers what such a call creates
([7.1](ch07-01-child-executions.md)) and what it costs
([7.2](ch07-02-what-a-hop-costs.md)). The cost is often more than the work
inside the child. Facts are from **tools v4.6.0** (the tool library
worker v6.15.0 uses) and the resource model at **server v3.161.2**.

## Check your understanding

{{#quiz ../quizzes/ch07-00.toml}}
