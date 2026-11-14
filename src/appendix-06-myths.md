# Appendix F: Myths and Corrections

<span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this section are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md).

## Corrections recorded so far

Rows are added as each page that corrects a myth lands. The full
appendix is written in [#45](https://github.com/noetl/book/issues/45).

| Myth | Fact | Verified at | Checked by | Page |
|---|---|---|---|---|
| The local runtime runs a `loop:` step once per item. | It parses `loop:` and runs the step **once**; the run ends `ok` with no warning. | CLI v6.4.0: `Step.loop_config` (`executor/src/playbook.rs`) has no reader | `examples/ch08/loop-runs-once` (CI) | [Appendix H](appendix-08-contributing.md) |
