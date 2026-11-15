# The Resource Model

<span class="status status-real">REAL</span>

How long will a playbook take, how many worker slots will it hold, and
what can stop it? NoETL publishes its answers as one machine-readable
file, the **resource model**:
[`noetl.ai/dsl/resource-model.json`](https://noetl.ai/dsl/resource-model.json),
the same file as `orchestrate-core/schema/resource-model.json` in the
server repository. This chapter teaches you to use it.

Every page here reads the file at server **v3.161.2**, model version
**1**, **`as_of` 2026-11-11**. The full listing, every figure with its
label, is [Appendix D](appendix-04-resource-model.md); this chapter
does not reprint it.

## Read this first

The file opens with three rules (`read_first`). In short:

1. **Orchestration dominates.** On NoETL a step's latency is mostly the
   cost of orchestrating it, not the work it does. Count steps and
   sub-playbook hops before estimating anything else.
2. **Figures are dated and local.** A number from kind does not
   transfer to prod, and an old number may predate a fix.
3. **Live values beat the file.** A running server answers
   `/api/dsl/version`; a worker's limits are its environment; what a
   run actually cost is in its events.

## What is in it

| Section | Answers | Chapter section |
|---|---|---|
| `labels` | what kind of number each figure is | [21.1](ch21-01-labels.md) |
| `step_kinds` | what each tool kind holds and how long it may run | [21.2](ch21-02-step-kind-costs.md) |
| `limits` | the caps a worker enforces, with their environment variables | [21.3](ch21-03-limits.md) |
| `concurrency` | pools, slots, autoscaling, queueing | [21.4](ch21-04-slot-model.md) |
| `heuristics`, `orchestration_overhead` | how to turn the figures into an estimate | [21.5](ch21-05-estimating.md) |
| `not_yet_measured` | the questions with no number yet | [21.6](ch21-06-not-yet-measured.md) |
| `metrics` | where a real run's cost is recorded | [21.5](ch21-05-estimating.md#check-the-estimate) |

## The model is a representation

The file is generated from Rust source written by people from code,
measurements and cluster reads (`orchestrate-core/src/resource_model.rs`).
The server's tests check that the committed JSON is what that source
generates (`tests/dsl_artifacts.rs:46`) and refuse a number with no
label. Nothing checks that each figure is still true. So treat
it like any copy: true only while something forces it to agree. This
chapter checked its code claims against worker v6.15.0 and tools v4.6.0
and reports two places where it disagrees with the code or with itself
([21.4](ch21-04-slot-model.md#where-the-model-disagrees)).

## Check your understanding

{{#quiz ../quizzes/ch21-00.toml}}
