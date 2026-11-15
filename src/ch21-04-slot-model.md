# The Slot and Pool Model

<span class="status status-real">REAL</span>

[Section 10.4](ch10-04-slots-and-keda.md) showed how slots and pools
work on a cluster. This section is about using that model to plan: how
many slots a playbook needs at its peak, and where it can get stuck.

## The rule

"Every command holds one worker slot from claim until its tool
returns, including case evaluation and its lifecycle event emits"
(`step_kinds.slot_rule`, DEFAULT). A pool's capacity is replicas ×
slots; commands beyond it queue on the bus. On the cluster read on
2026-11-11 (DEPLOYED): the user pool had **8 slots at minimum and 80
at maximum**, and the system pool **4**.

## Counting slots, not steps

Two GUIDANCE rules from `heuristics`:

- **A parallel loop takes N slots at once.** A `loop:` in parallel
  mode dispatches every item together, and `max_in_flight` does not
  throttle it ([6.3](ch06-03-loop.md)). 30 items need 30 free slots on
  the pool, or the rest queue. At the 8-slot minimum, a 30-item loop
  runs in about four waves until KEDA adds replicas.
- **An awaiting parent needs two slots.** A `kind: playbook` step with
  `return_result` or `return_step`, or an agent's playbook tool, holds
  the parent's slot while the child needs another
  ([Chapter 7](ch07-00-sub-playbooks.md)).

## The deadlock you can build

The model's note on `kind: playbook`: "an awaited child needs a free
slot on its own pool while the parent holds one; if both target the
same small pool, enough concurrent awaiting parents can occupy every
slot." With 8 slots, **8 parents awaiting children at the same time
hold all 8**, and no child can start. Each parent waits until its
await times out (180 s by default for `return_result`).

The pool is chosen per execution ([10.3](ch10-03-bus-and-pools.md#which-pool-runs-a-step)),
so a parent and its children land on the same pool unless the child is
started with a pool override. Keep awaiting fan-outs smaller than the
pool, or do not await.

## Where the model disagrees

Checking the model against worker v6.15.0 and against itself:

1. **`slot_rule` misses the callback release.** It says a slot is
   released early "only on a failed or refused claim". But the
   worker also frees the slot when a step parks on an external
   callback: it skips its own `call.done` and returns, "freeing the
   slot while an external system works" (worker
   `src/executor/command.rs:1326-1333`).
2. **The model contradicts itself.** Its own `container` entry says
   the slot is freed once the Job is created (the callback pattern),
   which is that same early release.

So for planning: a `container` step, or any step that returns a pending
callback, costs its slot only until it hands off, not for the whole
external job.

## Check your understanding

{{#quiz ../quizzes/ch21-04.toml}}
