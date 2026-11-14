# How to Read This Book: Status Badges, Quizzes and Traces

## Status badges

NoETL moves fast, and some of what this book covers is designed but not
yet built, or built but switched off. Every page opens with a badge:

| Badge | Meaning |
|---|---|
| <span class="status status-real">REAL</span> | Shipped and released. Shipped flags are on by default or enabled in a documented deployment. You can run the examples. |
| <span class="status status-partial">PARTIAL</span> | Some of it is real. The rest is released behind an off-by-default flag, proven only in a test cluster, or exists only as a single deployment. The page says which parts are which. |
| <span class="status status-target">TARGET</span> | Designed, usually in an RFC, but not built. These pages describe intent and are rewritten when the code lands. |
| <span class="status status-stub">STUB</span> | The page is planned but not written yet. |

Inside a page, individual claims carry the same labels the NoETL
resource model uses: **MEASURED**, **DEPLOYED**, **DEFAULT**,
**GUIDANCE**, **TARGET** and **NOT_YET_MEASURED**. A number without a
label is a bug in the book.

## Quizzes

Most sections end with a short quiz. The quizzes are there to help you
learn, not to grade you: answers are not reported anywhere, and a wrong
answer shows an explanation of the misconception behind it. If a
question is confusing, that is a bug in the book. Please report it.

## Traces

NoETL is event-sourced: an execution *is* its event log. Where it
helps, the book shows a recorded event log as a step-through trace.
You move through the events one at a time and watch the execution's
state change after each one.

## Runnable examples

Examples marked ▶ can be run in the page by the NoETL local runtime
compiled to WebAssembly. Every other example names the runtime it needs:
`local`, `daemon` or `distributed`.
