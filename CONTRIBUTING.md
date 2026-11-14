# Contributing to The NoETL Book

This book is **spec-driven**, **issue-tracked** and largely written with
AI coding agents. This page covers how to work on it, for people and
for their agents. Read [§5 Rules for AI agents](#5-rules-for-ai-agents)
before handing any of this work to an agent.

Related: [`docs/ROADMAP.md`](docs/ROADMAP.md) (what to write, in what
order) · [`docs/BOOK-PLAN.md`](docs/BOOK-PLAN.md) (pedagogy, goals,
sources) · [`src/SUMMARY.md`](src/SUMMARY.md) (the table of contents)
· [wiki](https://github.com/noetl/book/wiki) (coordination).

## 1. Where things live

| What | Where | Rule |
|---|---|---|
| Published content | `src/` (chapters), `quizzes/`, `traces/`, `examples/` | Changes only through PRs |
| The spec | `specs/001-noetl-book/` (`spec.md`, `plan.md`, `tasks.md`) and `.specify/memory/constitution.md` | **The canonical spec.** Changes only through PRs |
| Plan and roadmap | `docs/BOOK-PLAN.md`, `docs/ROADMAP.md` | Keep consistent with the spec and SUMMARY |
| Work items | GitHub issues on `noetl/book` | One issue per chapter or task |
| Coordination | [Wiki](https://github.com/noetl/book/wiki) | Working space, not published content |

**The wiki holds** the Spec front door (a summary plus links to
`specs/`; spec discussion happens there), Assignments (who or which
agent holds which issue), the Style Guide, Decisions (owner decisions
and their dates), and Roadmap and status summaries mirrored from
`docs/`. **The wiki never holds** chapter prose, quizzes, or the only
copy of a decision that changes the spec. Anything a reader will see,
or that an agent must obey, goes in the repo through a PR.

> Bootstrap status (2026-11-13): spec-kit is initialised for Claude
> Code (`.claude/skills/speckit-*`). The constitution, the spec
> (`specs/001-noetl-book/`), the labels and one issue per chapter or
> task (#3–#51) exist. **Start with an `agent-ok` issue in phase P0 or
> P1**; see `specs/001-noetl-book/tasks.md`.

## 2. The spec (spec-kit)

The book uses [GitHub Spec Kit](https://github.com/github/spec-kit). It
treats the book as the "feature" being specified:

- **constitution**: the book's non-negotiables. It contains §5's rules:
  honesty badges, verify before REAL, a public repo, tested examples.
- **spec.md**: scope, audience, structure, and **acceptance criteria
  per chapter**. These are the "done" test for every chapter PR.
- **plan.md**: how the book is built. It points at BOOK-PLAN for the
  pedagogy and tooling.
- **tasks.md**: the chapter work list. Each task maps to one GitHub
  issue.

Install (requires Python 3.11+ and [uv](https://docs.astral.sh/uv/);
these commands were checked against spec-kit v1.4.0):

```bash
uv tool install specify-cli
```

```bash
specify version
```

Initialise in this repo once, for your agent. The integration key is
`claude`, `copilot`, `gemini`, `codex`, `cursor-agent`, and so on;
list them with `specify integration list`. Commit the generated files
in their own PR.

```bash
specify init --here --force --integration claude
```

The repo is already initialised for Claude Code. To add your own
agent's files without re-initialising, install its integration. Some
integrations (Copilot among them) are not declared multi-install safe
alongside Claude and need `--force`. Review the diff before committing.

```bash
specify integration install copilot --force
```

Point spec-kit at the book spec locally. `.specify/feature.json` is
git-ignored, per-checkout state:

```bash
printf '{\n  "feature_directory": "specs/001-noetl-book"\n}\n' > .specify/feature.json
```

The process steps are **agent commands**, not terminal commands. The
spelling depends on the agent: `/speckit-specify` (Claude Code,
Copilot skills), `/speckit.specify` (dotted form), `$speckit-specify`
(Codex).

| When | Run | Effect |
|---|---|---|
| Once, at bootstrap | `/speckit-constitution <the §5 rules>` | Writes `.specify/memory/constitution.md` |
| Creating the spec | `/speckit-specify <scope, audience, structure from BOOK-PLAN>` | Writes `specs/001-noetl-book/spec.md` |
| Resolving gaps | `/speckit-clarify <focus>` | Asks questions and folds the answers into `spec.md` |
| Before chapter work | `/speckit-plan`, `/speckit-checklist`, `/speckit-tasks` | Writes `plan.md`, the checklists and `tasks.md` |
| Before merging spec changes | `/speckit-analyze` | Read-only check that spec, plan and tasks agree |
| Writing a chapter | `/speckit-implement` scoped to one task | Drafts against that task's acceptance criteria |
| After a chapter PR | `/speckit-converge` | Checks the result against the spec |

**Updating the spec when reality changes.** Examples: a feature ships
and a TARGET chapter becomes REAL; a chapter's scope grows or splits;
a fact in an acceptance criterion turns out wrong. In each case, edit
`spec.md` (with `/speckit-clarify` or by hand), re-run
`/speckit-analyze`, and update `tasks.md`, ROADMAP, BOOK-PLAN and the
affected issues **in the same PR**. The spec, the plan, the roadmap and
SUMMARY must never disagree on `main`.

Spec Kit tracks the active feature in `.specify/feature.json`, not in
the git branch. Keep it pointing at `specs/001-noetl-book`.

## 3. Issues

**One issue per chapter or task.** A chapter issue is titled
`Ch. NN — <chapter title>`. Smaller tasks (a quiz set, a trace, a
generated appendix, an accuracy fix) get their own issues. The issue
body must contain:

- **Spec**: link to the chapter's section in `specs/001-noetl-book/spec.md`.
- **Chapter**: the `src/chNN-*.md` files it covers.
- **Acceptance criteria**: copied from the spec (the spec wins if they differ).
- **Sources**: from BOOK-PLAN §7.
- **Badge**: the expected badge, and what would change it.

**Labels:**

| Group | Labels |
|---|---|
| Type | `type:chapter`, `type:quiz`, `type:trace`, `type:example`, `type:appendix`, `type:tooling`, `type:spec`, `type:accuracy` |
| Part | `part:front`, `part:I` … `part:IX`, `part:appendix` |
| Badge | `badge:real`, `badge:partial`, `badge:target` |
| Phase | `phase:P0` … `phase:P7` |
| Flags | `needs-verification` (a claim could not be checked against code), `owner-decision` (blocked on the owner), `agent-ok` (suitable for an AI agent) |

**Status flow.** The issue is the source of truth for status. The
wiki's Assignments page mirrors it.

| Status | How it shows |
|---|---|
| Todo | Open, no assignee |
| In progress | Assigned, plus a comment saying who/which agent and the branch name |
| In review | A PR that says `Closes #N` is open |
| Done | The PR is merged and the issue closed. The badge, Appendix E row and wiki Assignments are updated |

One active assignee per issue. To take over, comment and ask first.

## 4. Building and checking

Every PR must pass all of these locally before it is opened. CI will run
the same checks.

```bash
mdbook build
```

```bash
mdbook serve --open
```

`mdbook build` also runs `mdbook-linkcheck` (0.7.7) over every internal
link; install it (see README) or the check is silently skipped. CI runs
it on every PR, and checks external links weekly. The example runner
(`examples/` → `noetl run`, outputs diffed) is added in Phase 0. Once
it exists it is mandatory. Until then, run each example by hand
with the CLI version you cite and paste the command and output into
the PR.

## 5. Rules for AI agents

These rules apply to every contributor. They are written for agents
because agents are the most likely to break them confidently.

### The non-negotiables

1. **Never label TARGET as REAL.** REAL means shipped and released, on
   by default or enabled in a documented deployment. Merged code behind
   an off flag is PARTIAL. An RFC is TARGET. The same applies to every
   claim inside a page (MEASURED, DEPLOYED, DEFAULT, GUIDANCE, TARGET,
   NOT_YET_MEASURED).
2. **Verify before you write REAL.** Check each claim against the
   actual code, schema or behaviour at a named release or commit, not
   against memory, an older doc, or another chapter. Cite where you
   checked it in the PR. If you cannot verify a claim, label it lower
   or add `needs-verification` to the issue. Never guess.
3. **Spec-driven.** Before writing, read the spec, the assigned issue,
   and the wiki rules (Style Guide, Decisions). Write to the chapter's
   acceptance criteria. If the scope must change, update the spec and
   the issue first (§2), in the same PR or a preceding one.
4. **One chapter / one issue at a time.** One branch and one PR per
   issue. Do not edit chapters outside the issue's scope. Note other
   problems as new issues.
5. **Every change goes through a PR.** Never push to `main`.
6. **Run the checks** (§4): build, linkcheck and the example playbooks.
   Report their results in the PR.
7. **Record status back.** Update the issue status and the wiki
   Assignments row when you start, at each PR, and when you finish.
8. **This repo is public.** No secrets, tokens, internal hostnames,
   cloud project IDs or customer data. Material from private repos
   needs the owner's sign-off (`owner-decision`).
9. **Don't invent numbers.** Every figure has a label and a source
   (where measured, when, and n).

### The agent loop

```
┌─► 1. SYNC     git pull origin main; re-read the spec, ROADMAP and
│               the wiki rules; check the issue for new comments
│   2. CLAIM    pick an open `agent-ok` issue in the current phase;
│               assign it; comment "starting: <agent>, branch <name>";
│               update wiki Assignments
│   3. VERIFY   open every source in the issue; check each claim
│               against code or behaviour at a named release
│   4. DRAFT    write the chapter, its quiz and its examples against
│               the acceptance criteria; set the page badge truthfully
│   5. CHECK    mdbook build, linkcheck, run the examples
│   6. PR       open the PR with "Closes #N", the verification notes,
│               the check results and any spec changes; comment on the issue
│   7. RECORD   when merged: close the issue; update the badge, the
│               Appendix E row, ROADMAP if the phase/badge moved, and
└──────────────  wiki Assignments. Then pick up the next issue
```

### Staying in sync and handing off

- **Before starting, and again before opening the PR:** pull `main` and
  re-read the spec and your issue. Another contributor may have
  changed the spec, merged a chapter you depend on, or reassigned the
  issue. Rebase onto `main`. If the spec changed under you, re-check
  your draft against the new acceptance criteria.
- **Report progress on the issue,** not just in the PR. Comment at
  each milestone: started, sources verified, PR opened, blocked. That
  way another person or agent can take over cold.
- **Picking up someone else's work:** watch the issues and PRs you
  depend on (GitHub "Subscribe"). When one merges, re-pull `main` and
  the spec before continuing. Never copy text from an unmerged PR
  into yours; depend on it or wait for it.
- **Handing off:** comment with the state (what is done, what is
  verified, what is left, the branch), unassign yourself, and update
  wiki Assignments.
- **Blocked:** add `owner-decision` or `needs-verification`, explain
  why, and move to another issue rather than guessing.

### Agent brief (copy, fill in, hand to your agent)

```text
You are working on The NoETL Book (github.com/noetl/book), an mdBook.
Your task is issue #<N>: "<issue title>".

Before writing anything:
1. git pull origin main. Read CONTRIBUTING.md §5 (these rules),
   specs/001-noetl-book/spec.md (the section for this chapter),
   .specify/memory/constitution.md, docs/ROADMAP.md, and
   docs/BOOK-PLAN.md §5 and §7 for this chapter.
2. Read issue #<N> and all its comments, and the wiki pages Style-Guide
   and Decisions.
3. Comment on the issue: "starting: <agent name>, branch <branch>".

Rules (non-negotiable):
- Never label anything REAL unless you verified it against the code,
  schema or behaviour at a named release/commit, and cite that in the PR.
  Merged-but-flag-off = PARTIAL. Designed-only = TARGET. If unsure,
  label lower and add `needs-verification`.
- Every number has a label (MEASURED/DEPLOYED/DEFAULT/GUIDANCE/TARGET/
  NOT_YET_MEASURED) and a source.
- Work only on the files this issue covers. One branch, one PR.
  Never push to main.
- If the scope or acceptance criteria must change, update the spec and
  the issue in the PR, and say so.
- Public repo: no secrets, internal hostnames, project IDs or customer data.

Do:
- Draft the chapter (and its quiz in quizzes/, and examples in
  examples/) to meet every acceptance criterion in the spec.
- Run `mdbook build`, the linkcheck and the example playbooks. Fix
  every failure.
- Open a PR titled "Ch. NN: <title>" whose body has: Closes #<N>; each
  acceptance criterion with how it is met; verification notes (claim →
  where checked); check results.
- Comment on the issue with the PR link and update the wiki
  Assignments row.

Stop and ask me if: a source contradicts the spec, a claim cannot be
verified, or the work needs a private source or an owner decision.
```
