# How to Read This Book: Status Badges, Quizzes and Traces

<span class="status status-real">REAL</span>

## Status badges

NoETL moves fast, and some of what this book covers is designed but not
yet built, or built but switched off. Every page opens with a badge:

| Badge | Meaning |
|---|---|
| <span class="status status-real">REAL</span> | Shipped and released. Shipped flags are on by default or enabled in a documented deployment. You can run the examples. |
| <span class="status status-partial">PARTIAL</span> | Some of it is real. The rest is released behind an off-by-default flag, proven only in a test cluster, or exists only as a single deployment. The page says which parts are which. |
| <span class="status status-target">TARGET</span> | Designed, usually in an RFC, but not built. These pages describe intent and are rewritten when the code lands. |
| <span class="status status-stub">STUB</span> | The page is planned but not written yet. |

Inside a page, individual claims, numbers above all, carry one of the
six labels the NoETL resource model defines. The meanings below are
quoted from it (`labels`, `resource-model.json`, server v3.161.2):

| Label | Meaning |
|---|---|
| **MEASURED** | observed on a cluster or harness; read environment/date/source before reusing it |
| **DEPLOYED** | read off the production cluster on as_of; configuration, not code |
| **DEFAULT** | a code default (env var + value); a deployment may override it |
| **GUIDANCE** | a planning rule derived from the figures; not a measurement |
| **TARGET** | a goal or budget; not a measurement |
| **NOT_YET_MEASURED** | a real question with no number; do not invent one |

A MEASURED number in this book also says where, when and over how many
runs it was measured. A number without a label is a bug in the book.

## Quizzes

Most sections end with a short quiz. The quizzes are there to help you
learn, not to grade you: answers are not reported anywhere (the book has
no quiz telemetry), and a wrong
answer shows an explanation of the misconception behind it. If a
question is confusing, that is a bug in the book. Please report it.

## Examples

Every playbook in this book is a file under `examples/` in the book's
repository, and CI checks it on every change:

- **local** examples are run with the pinned NoETL CLI, and their
  output must match what the page shows;
- **distributed** examples are checked against the server's schema,
  but not run, because they need a cluster. The page says so where it
  shows one.

The CLI version the examples are tested against is in
[Appendix E](appendix-05-status-ledger.md).

```admonish not-yet
Two interactive features are planned and not built yet:

- **Traces** ([#7](https://github.com/noetl/book/issues/7)): a recorded
  event log shown as a step-through, with the execution's state after
  each event.
- **▶ runnable examples** ([#8](https://github.com/noetl/book/issues/8)):
  examples that run in the page, on the local runtime compiled to
  WebAssembly.

Until they exist, no page shows a trace widget or a ▶ button.
```

## Where the book is going

The [roadmap](https://github.com/noetl/book/blob/main/docs/ROADMAP.md) shows every chapter, its status and when it will be written. To help write it, see [Appendix H](appendix-08-contributing.md).

## Try it

This is what an end-of-section quiz looks like. It checks the three ideas above.

{{#quiz ../quizzes/ch00-01.toml}}
