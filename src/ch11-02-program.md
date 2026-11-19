# When a Program Is Better

<span class="status status-real">REAL</span>

NoETL charges **per step**. A program charges per unit of work. When
the job is one tight computation, the per-step charge buys you nothing,
and a program, script or library call is the better tool. This section
shows what a step costs, so you can do that arithmetic yourself.

## What a step costs

Each row is a measurement, with where, when and how many runs. These
numbers change with releases: the distributed figures fell by more than
two thirds in November 2026 alone. Re-measure before you budget.

| Where | Cost | Label and source |
|---|---|---|
| Local runtime: starting the CLI | ~166 ms per run | MEASURED by this book, 2026-11-19: CLI 6.4.1 on an Apple M1 Max, n = 10, p50 wall time of a one-step playbook |
| Local runtime: a trivial `shell` step | ~3.3 ms | same run: (p50 of a 21-step chain − p50 of a 1-step run) ÷ 20 |
| Local runtime: a trivial `rhai` step | ~259 ms | same run and method |
| Distributed, kind, idle | 32–36 ms p50 of orchestration per step | MEASURED, kind benchmark harness, 2026-11-14, server 3.161.2 / worker 6.15.0, two reps (ai-meta wiki Sessions-Log) |
| Distributed, production | **217 ms p50, 546 ms p95** of orchestration per step (712 / 1483 ms before that day's changes) | MEASURED, prod, 2026-11-15 (ai-meta wiki Sessions-Log; the record does not state n) |
| Distributed, production: an awaited child playbook | ~1.0 s p50 (2026-11-15); ~0.83 s (2026-11-16) | MEASURED, same record |

That is the overhead alone, before the step does any work. The
resource model's guidance turns it into an estimate: wall clock ≈ steps
× per-step overhead + the sum of the work + hops × hop overhead
([7.2](ch07-02-what-a-hop-costs.md), [21.5](ch21-05-estimating.md)).

The `rhai` row is not a typo. In this measurement, a `rhai` step that
returns a constant cost about as much as a quarter of a second, while a
`shell` step that spawns a process cost 3 ms. The book has not traced
why. Treat it as a measured fact about CLI 6.4.1 on one machine, not as
a property of Rhai.

## Same work, two shapes

The same million-addition loop, run 10 times each on the same machine
on 2026-11-19 (p50 wall time, process start included):

| Shape | p50 |
|---|---|
| A Python 3.12 script: `for i in range(1000000): s += i` | **93 ms** |
| One NoETL `rhai` step running the same loop (`noetl run -r local`) | **540 ms** |

The loop is not the expensive part. The NoETL run spends most of its
time starting the CLI and paying for the step. Now imagine making each
addition its own step, for example with a `loop:` over a million items
on the distributed runtime. A parallel `loop:` dispatches one command
per item and needs a free slot for each (resource model guidance,
server v3.161.2). At ~0.2 s of overhead per step, the overhead alone is
measured in hours. Never put a hot loop's iterations into steps.

## When to reach for a program

Use a plain program, script or library when **all** of these hold:

- **It is one computation.** No step needs to wait for, retry against,
  or be resumed after a different system.
- **Latency matters per call.** It has to answer in tens of
  milliseconds, or it runs thousands of times a second.
- **The work is a loop.** The cost scales with items, not with stages.
- **Nobody needs the record.** No one will ask later which inputs
  produced which output, or replay a run.

If any of them fails, read on: that is where NoETL starts to earn its
overhead.

## Usually the answer is both

Most real pipelines are a few coarse stages around one or two heavy
computations. The shape that works is **a program inside a step**:

```yaml
- step: score
  tool:
    kind: shell
    cmds:
      - python3 -m scoring.run --in data/batch.parquet --out data/scored.parquet
```

The program does the hot loop at full speed. NoETL does what a program
does badly: it records which playbook version ran the stage, with
which inputs and what result ([3.2](ch03-02-event-sourcing.md)),
sequences it with the other stages, and lets you rerun or inspect it
later. You pay the per-step cost once per stage, not once per item.
The quantum case study (Chapter 26) is built exactly this way: hours of
compute inside `shell` steps, with NoETL around them.

```admonish warning title="What wrapping does not give you"
Putting a program in a step does **not** make it retry, time out or
resume by itself. At these releases, a failed step fails
([6.5](ch06-05-errors-timeouts-retries.md)), and the local runtime keeps
no resume point ([Chapter 11](ch11-00-choosing-a-runtime.md)). If you
need those, build them: a guarded back-edge for retries, the tool's own
`timeout_seconds`, and the distributed runtime for durability.
```

## Check your understanding

{{#quiz ../quizzes/ch11-02.toml}}
