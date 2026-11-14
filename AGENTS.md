# Instructions for AI agents working on this repo

This is **The NoETL Book**, an mdBook. Before doing anything, read
[`CONTRIBUTING.md`](CONTRIBUTING.md) §5 "Rules for AI agents". It is
binding. In short:

1. **Never label TARGET as REAL.** Verify every REAL claim against code,
   schema or behaviour at a named release/commit, and cite it in the PR.
   Merged-but-flag-off is PARTIAL; designed-only is TARGET. If unsure,
   label lower and add `needs-verification`.
2. **Spec-driven.** Read `specs/001-noetl-book/spec.md`,
   `.specify/memory/constitution.md`, your assigned issue and the wiki
   Style-Guide/Decisions pages first. Write to the chapter's acceptance
   criteria. Update the spec and issue when scope changes.
3. **One issue, one branch, one PR.** Never push to `main`. Stay
   inside the issue's files.
4. **Run** `mdbook build`, the linkcheck and the example playbooks
   before opening the PR.
5. **Record status** on the issue and the wiki Assignments page when
   you start, at the PR, and when you finish.
6. **Public repo.** No secrets, internal hostnames, project IDs or
   customer data.

Work items: `specs/001-noetl-book/tasks.md` (one GitHub issue each). The outline is `src/SUMMARY.md`, the order is `docs/ROADMAP.md`, and the
goals and sources are in `docs/BOOK-PLAN.md`.
