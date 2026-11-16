# Deployment Modes

<span class="status status-real">REAL</span>

NoETL runs in three places. The **local runtime** is one process on
your machine ([Chapter 8](ch08-00-local-runtime.md)); it needs no
deployment. This chapter covers the other two: a **kind** cluster on
your laptop, and **production on GKE**. It ends with the one way
production is changed: an image patched in by digest.

All deployment code and manifests live in the public `noetl/ops`
repository. Facts here are read at ops commit **`6c55cbe`** (2026-11-15)
and ai-meta `playbooks/` at **`0e835fd`**, plus dated public records.
This book has not run these against a cluster; each fact is labelled
as read. No project ids, registry paths or hostnames appear here.

## The order is fixed

```text
code + unit tests ─▶ kind (same images, same topology) ─▶ production, by digest
```

Kind first, always: a wrong config key, a missing variable or a broken
probe costs minutes there and hours in production. Then production
changes one workload at a time, by an image-only patch, never by
applying a manifest ([27.3](ch27-03-deploy-by-digest.md), and
[Chapter 29](ch29-00-rollout-rollback.md) for the rollout itself).

## Sections

- [27.1 Local kind first](ch27-01-kind.md): the EHDB-only topology on
  kind, and the guard that keeps a kind command off production.
- [27.2 Production on GKE](ch27-02-gke.md): what the manifests declare,
  and why they are not a picture of what runs.
- [27.3 Deploy by digest](ch27-03-deploy-by-digest.md): the patch, the
  dry-run, the rollback row, and the outage that made it the rule.

## Check your understanding

{{#quiz ../quizzes/ch27-00.toml}}
