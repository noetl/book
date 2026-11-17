# Case Study: Authentication and Authorization

<span class="status status-partial">PARTIAL</span> <span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this chapter are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md)
> (Part X and §2.8).

How a NoETL deployment decides who may start which playbook and read which execution.

Planned sections:

- **34.1 Sign-In Is a Playbook** — Auth0 session validation as an ordinary execution, the session cache, and the synchronous path that can replace it.
- **34.2 Deny by Default: Two Roles and an Allowlist** — exactly two roles, `admin` and regular user; the user-playbook allowlist; guest sessions.
- **34.3 Who Owns an Execution** — a regular user may read or cancel only executions they started; how ownership is recorded.
- **34.4 Granting Roles and Verified Email** — role grants by playbook and verified-email role inheritance: in flight at the time of writing, labelled until a release carries them.
