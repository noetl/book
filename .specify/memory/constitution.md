<!--
Sync Impact Report
- Version change: template → 1.0.0 (initial ratification)
- Principles added: I Honesty Badges; II Verify Before REAL; III Spec-Driven;
  IV One Issue, One PR; V Checks Are Gates; VI Record Status Back;
  VII Public by Default; VIII Sources Over Memory
- Sections added: Content Standards; Workflow; Governance
- Templates: spec/plan/tasks templates unchanged (book-specific rules live here
  and in specs/001-noetl-book/spec.md "CH-ALL")
- Follow-up TODOs: none
-->

# The NoETL Book Constitution

This constitution governs every change to `noetl/book`, whether a person
or an AI agent makes it. It encodes the non-negotiable rules in
[`CONTRIBUTING.md` §5](../../CONTRIBUTING.md#5-rules-for-ai-agents). If
the two ever disagree, this file wins, and CONTRIBUTING is fixed in the
same PR.

## Core Principles

### I. Honesty Badges (NON-NEGOTIABLE)

Every page carries exactly one badge, and it describes the **subject**,
not the prose:

- **REAL**: shipped and released, on by default or enabled in a
  documented deployment.
- **PARTIAL**: some of it is real; the rest is behind an off-by-default
  flag, proven only on a test cluster, or a single deployment. The page
  says which part is which.
- **TARGET**: designed but not built.

A TARGET subject MUST NOT be labelled REAL. Merged code behind an off
flag is PARTIAL. Every number inside a page carries one of MEASURED,
DEPLOYED, DEFAULT, GUIDANCE, TARGET or NOT_YET_MEASURED. A MEASURED
number states where it was measured, when, and n.

*Rationale:* the book describes a system that changes weekly; a badge
readers cannot trust makes every page untrustworthy.

### II. Verify Before REAL (NON-NEGOTIABLE)

A claim may be written as REAL only after it has been checked against
the actual code, schema or observed behaviour at a **named release or
commit**, and that check is cited in the PR. Memory, older docs and
other chapters are not verification. If a claim cannot be verified, it
MUST be labelled lower or flagged `needs-verification`. Guessing is
never allowed.

### III. Spec-Driven

All work is written against `specs/001-noetl-book/spec.md`. Before
writing, a contributor reads the spec, the assigned issue and the wiki
Style Guide and Decisions pages. When scope or acceptance criteria must
change, the spec and the issue are updated first: in the same PR, or in
a preceding spec PR. On `main`, `src/SUMMARY.md`, `docs/ROADMAP.md`,
`docs/BOOK-PLAN.md`, the spec and the issues MUST NOT disagree.

### IV. One Issue, One Branch, One PR

Each change addresses one issue, on one branch, through one PR. Nobody
pushes to `main` directly. A PR edits only files within its issue's
scope; problems found elsewhere become new issues.

### V. Checks Are Gates

A PR is mergeable only when `mdbook build`, the link check and the
example-playbook runner pass. Their results are reported in the PR.
A new gate is proven able to fail (a deliberately broken input turns it
red) before it is trusted to be green.

### VI. Record Status Back

The issue is the source of truth for status: Todo → In progress → In
review → Done. A contributor comments on the issue at start, at PR and
at finish, and updates the wiki Assignments page. When a chapter
merges, its badge, its Appendix E row and (if it moved) its ROADMAP row
are updated.

### VII. Public by Default

The repository and wiki are public. No secrets, tokens, internal
hostnames, cloud project IDs or customer data may appear. Material
derived from a private repository requires the owner's sign-off
(`owner-decision`) before it is written.

### VIII. Sources Over Memory

Every chapter cites its sources (see BOOK-PLAN §7). Where the
authoritative source is machine-readable (the DSL schema, the DSL
manifest, the resource model), the book generates from it instead of
copying it by hand.

## Content Standards

- The DSL is described with its real keys (`workflow`, not `steps`), as
  `playbook.schema.json` defines them at a named commit.
- Production facts are version-stamped ("as of vX.Y, date"), never
  written as "currently".
- A page says what exists today before what is planned.
- Every example is a file under `examples/`, run by CI, and names the
  runtime it needs.
- Every section ends with a 2–5 question quiz. Distractors come from
  real misconceptions, and every answer has an explanation.

## Workflow

The loop is: sync (pull `main` and re-read the spec) → claim the issue
→ verify sources → draft against the acceptance criteria → run the
checks → open a PR (`Closes #N`, verification notes, check results) →
record status. Hand-offs happen on the issue: the state, what is
verified, what is left, the branch. Full detail is in `CONTRIBUTING.md`.

## Governance

This constitution supersedes all other book practices. Amendments are
made through a PR that changes this file and bumps the version:
MAJOR to remove or redefine a principle, MINOR to add one, PATCH for
clarifications. The PR also updates `CONTRIBUTING.md` and any affected
spec sections. Every PR review checks compliance with Principles I–VII.

**Version**: 1.0.0 | **Ratified**: 2026-11-13 | **Last Amended**: 2026-11-13
