# Appendix H: Contributing to This Book

<span class="status status-real">REAL</span>

This appendix is for people and AI agents who want to write part of
this book. It describes how the book is made **as of 2026-11-13**: the
tools named here are installed in CI and run on every pull request.

The full workflow, including the copy-paste brief for an AI agent, is in
[`CONTRIBUTING.md`](https://github.com/noetl/book/blob/main/CONTRIBUTING.md).
The house rules for prose, callouts and quizzes are on the wiki
[Style Guide](https://github.com/noetl/book/wiki/Style-Guide). This
page summarises both and shows what each building block looks like.

## H.1 How a page gets written

The book is **spec-driven**. Three files decide what gets written:

| File | Decides |
|---|---|
| [`specs/001-noetl-book/spec.md`](https://github.com/noetl/book/blob/main/specs/001-noetl-book/spec.md) | Every chapter's acceptance criteria, plus the book-wide checklist (CH-ALL) |
| [`.specify/memory/constitution.md`](https://github.com/noetl/book/blob/main/.specify/memory/constitution.md) | The non-negotiable rules: honest badges, verify before REAL, one issue per PR, checks are gates |
| [`docs/ROADMAP.md`](https://github.com/noetl/book/blob/main/docs/ROADMAP.md) | The order chapters are written in, and each chapter's badge |

Every chapter has one GitHub issue. Contributors claim it, work on one
branch, and open one PR that says `Closes #N`. The issue records status
(Todo → In progress → In review → Done), and the wiki
[Assignments](https://github.com/noetl/book/wiki/Assignments) page mirrors it.

The rule that matters most: **a claim is REAL only after someone has
checked it against the code at a named release, and the PR says where.**
Memory, older docs and other chapters do not count as checking.

## H.2 Status callouts

Pages carry one badge (see [How to Read This Book](ch00-01-how-to-read.md)).
Inside a page, three callouts mark claims whose status differs from the
page's, or that correct a common belief. They render like this:

```admonish myth
"The local runtime runs `loop:` steps once per item." It does not. At
CLI v6.4.0 it parses `loop:` and runs the step **once**, and the run
still ends `ok`. The example `examples/ch08/loop-runs-once` checks this
in CI.
```

```admonish not-yet
A TARGET subject: designed in an RFC, not built. The callout names the
RFC and says what exists today instead.
```

```admonish partial
Merged and released, but off by default or proven only on a test
cluster. The callout names the flag and its default.
```

Every `myth` also gets a row in [Appendix F](appendix-06-myths.md).

## H.3 Examples

Every playbook the book shows is a file under
[`examples/`](https://github.com/noetl/book/tree/main/examples), one
directory per example:

```text
examples/<chapter>/<name>/
  playbook.yaml        the example
  RUNTIME              local | daemon | distributed
  expected.json        the expected run outcome          ┐
  expected.txt         or the expected final result      ├ one of these
  expected-error.txt   or the error the run must fail on ┘
```

CI runs each `local` example with the pinned NoETL CLI
(`noetl run <playbook> -r local --json`) and diffs the result against
the expected file. `daemon` and `distributed` examples are listed and
skipped. A chapter includes its example from the file, so the page and
the tested playbook cannot drift apart. The pinned version is in
[Appendix E](appendix-05-status-ledger.md).

## H.4 Quizzes

Each section ends with a short quiz, written as a TOML file in
`quizzes/` and embedded with a `#quiz` directive that names the file
(the exact syntax is on the Style Guide; writing it here would embed a
quiz). Three
rules matter:

1. **Distractors are real misconceptions**: things older docs said,
   things an agent asserted confidently, or things a reader would carry
   over from another orchestrator. A wrong answer should teach.
2. **Every question explains itself** in its `context` field, citing the
   source when the answer is a fact about the code.
3. **No telemetry.** Answers stay in the reader's browser.

A malformed quiz (bad TOML, or a question without an answer) fails the
build.

## H.5 Traces

```admonish not-yet
The trace visualizer (`mdbook-noetl-trace`, issue
[#7](https://github.com/noetl/book/issues/7)) is planned for phase P3
and does not exist yet. Until it does, pages show state changes as a
table of events and the state after each one.
```

## H.6 The checks

A PR can merge only when all of these pass, in CI and locally:

| Check | Command | Fails on |
|---|---|---|
| Build | `mdbook build` | a missing chapter file, a bad quiz, a preprocessor error |
| Links | (part of `mdbook build`) | any broken internal link; external links are checked weekly |
| Examples | `tools/run-examples.sh` | an example whose output differs from its expected file |

Each check was shown to fail on a deliberately broken input before it
was trusted to pass. The README lists the pinned tool versions and how
to install them.

## Quiz

{{#quiz ../quizzes/appendix-h.toml}}
