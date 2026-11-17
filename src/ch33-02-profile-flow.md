# The Profile Flow: Read, Save, Read Back

<span class="status status-real">REAL</span>

The travel app's profile page calls one playbook for two jobs. At
sign-in it reads the user's profile. On the settings page it saves
whatever section the user just edited. Either way, it returns the
stored profile plus a few suggested places near the user's home. The
playbook is short, but almost every step in it exists because of a
runtime rule. This section shows which rule, and how you would find it.

The source is `playbooks/profile.yaml` in
[`noetl/travel`](https://github.com/noetl/travel) at commit **`cd210d7`**
(catalog path `muno/playbooks/profile`). Runtime rules are checked
against server **v3.161.2** and tools **v4.6.0**. It is one of the
playbooks a signed-in regular user may start: it is on the gateway's
default allowlist (gateway v3.22.1 `src/authorization.rs:41-49`;
Chapter 34 covers that list).

## The shape

```text
start ─▶ validate_input ─┬─▶ begin_read ──────────────┐
                         ├─▶ save_profile ────────────┴─▶ load_profile ─▶ plan_suggestions ─┬─▶ suggest_pois ───┐
                         └─▶ reject_input ─▶ end                                           └─▶ skip_suggestions ┴─▶ build_response ─▶ end
```

The app sends `uid`, a `profile` object, and `read_only: true` at
sign-in. The playbook checks the input, writes if it should, and then
reads the document back. It plans suggestions from the stored profile,
calls Places if there are coordinates, and builds the response.

## Three decisions in the header

The playbook's description explains each design choice before any step
does it:

- **Merge, not overwrite** (lines 37-42). The settings page saves one
  section at a time. A plain `set_doc` replaces the whole document, so
  saving "personal info" would delete saved trips. The save passes
  `merge: true` (line 273), so a partial save stays partial.
- **Read back, don't echo** (lines 44-47). Returning the request as if
  it were the result is free, and it is wrong. It reports success for
  fields the store may have changed or refused. `load_profile` reads
  the document after the write, so the response shows what is actually
  stored. The header records a dated two-write test against the live
  store: after the second, partial write, the read-back held the fields
  of both writes.
- **The save is the contract; suggestions are extra** (lines 49-54). A
  save that worked must report success even if Places is down. See the
  warning below for how far the runtime enforces this.

There is also a fourth decision, about reads (lines 112-121). Sign-in
used to go through `save_profile` too, merging an empty object. That
deleted nothing. But every sign-in wrote to the store, and because a
merge creates a missing document, "never saved a profile" could no
longer be told apart from "saved an empty one". The `read_only` flag
gives reads their own branch.

## Rules the runtime forces

### First match wins, so arc order matters

`validate_input` routes with `mode: exclusive` (lines 212-216):

```yaml
- when: "{{ validate_input.ok and validate_input.read_only }}"
  step: begin_read
- when: "{{ validate_input.ok }}"
  step: save_profile
- step: reject_input
```

An exclusive arc set takes the first arc whose `when` is true
([6.1](ch06-01-next-and-routers.md#exclusive-and-inclusive)). A valid
read matches both of the first two conditions. If the two arcs were
swapped, every sign-in would write again. The comment above the arcs
says so, because the edit that breaks this looks harmless.

### A skipped step is skipped for good

Why does `begin_read` exist? It is a `noop` that only forwards to
`load_profile`. Why not route the read straight to `load_profile`?

When an exclusive arc set picks one arc, the other targets are recorded
as skipped ([6.1](ch06-01-next-and-routers.md#exclusive-and-inclusive)).
Skipped counts as done, the same as completed or failed
(orchestrate-core `state.rs:1044-1054`). And a later arc to a step that
is already done is ignored, unless it is a loop back-edge
(`orchestrator.rs:1364-1368`).

So suppose `load_profile` were one of `validate_input`'s targets.

1. A save wins the arc set, so `load_profile` is recorded as skipped.
2. `save_profile` then routes to `load_profile`, and that arc is ignored.
3. The run stops dispatching. It never fails, and it never finishes.

The playbook did this twice. First `build_response` was a direct target
of the suggestions router, and a profile with coordinates stranded the
run after every real step had succeeded (lines 359-368). Then
`load_profile` was a target of the read/save router, and every save
stranded. `begin_read`, `skip_suggestions` and `reject_input` are the
fix. Each branch gets its own entry step, and a step that several
branches lead to is never itself a target in an exclusive set.

```admonish tip title="Make the rule mechanical"
The repository has a guard for this, `scripts/playbook_skip_topology_test.py`.
CI runs it on every playbook change (`.github/workflows/playbook-tests.yml`).
It fails any playbook that can route to a step its own branch already
skipped. A rule that lives only in a comment works until someone forgets
to read the comment.
```

### A python step sees only what you bind

`validate_input` is `kind: python`. Its comment (lines 141-145) records
how the playbook's first real run failed: the code read `workload.get("uid")`
and got `NameError`. The python tool runs your code with each key of
`input:` as a global, plus `input_data`, `args`, `variables`,
`execution_id` and `step` (tools v4.6.0 `src/tools/python.rs:557-573`).
`workload` is not one of them. Templates can read `workload`; `code:`
can read only what `input:` passes to it:

```yaml
input:
  uid: "{{ workload.uid | default('') }}"
  read_only: "{{ workload.read_only | default(false) }}"
```

### Don't trust a type that crossed a template

`read_only` reaches the code through a template, so the playbook does
not assume it is a boolean. In Python, `bool("false")` is `True`, which
would send a real save down the read branch and look like success. The
code accepts only explicit spellings (`true`, `1`, `yes`, `on`) as
true. It treats anything it does not recognise as a write
(lines 159-171), because reading by mistake would quietly stop saving
profiles. It also checks coordinates with `bool` excluded, since `True`
is an `int` in Python and would read as a latitude (lines 178-186).

## How far "never fail the save" is enforced

```admonish warning title="Not verified: the suggestions fallback"
`suggest_pois` is meant to be optional. It carries a policy rule,
`when: "{{ output.status == 'error' }}"` → `do: continue`, under its
`tool:` (lines 400-408). [Section 6.5](ch06-05-errors-timeouts-retries.md)
verified that policy rules are applied for the sub-tasks of an
**ordered tool list**. This step has a single `kind: playbook` tool,
and for a single tool the server renders the whole tool config when it
builds the command (`orchestrate-core/src/commands.rs`, `build_tool_command`).
That happens before any `output` exists. This book has **not** verified
that the rule turns a Places failure into `continue` for this step.
That question is tracked in [book#95](https://github.com/noetl/book/issues/95).

If you need a step to be optional, use a form you have seen work: a
one-item tool list with a policy rule
([6.5](ch06-05-errors-timeouts-retries.md#what-does-retry-policy-rules-in-a-tool-list)),
tested by making the provider fail.
```

## What to copy

- Write the reason for each design choice in the playbook header, next to the code.
- Merge partial writes, then read back what the store actually holds.
- Give every branch its own entry step. Never make a join step an
  alternative in an exclusive arc set. Then add a check that enforces it.
- Bind everything a `code:` block needs through `input:`, and normalise
  values that cross a template.
- Before you rely on an error-handling key, check that something
  actually applies it.

## Check your understanding

{{#quiz ../quizzes/ch33-02.toml}}
