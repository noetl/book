# Production on GKE

<span class="status status-real">REAL</span>

Production runs on GKE **Autopilot**, which provisions nodes per pod
(the manifests carry `autopilot.gke.io/*` annotations; a new node takes
about 60-90 s, [10.4](ch10-04-slots-and-keda.md#what-has-been-measured)).
This page describes it as the committed manifests in `noetl/ops`
`ci/manifests/noetl/` declare it, at `6c55cbe`.

## What the manifests declare

| Workload | Kind | Replicas | Note |
|---|---|---|---|
| `noetl-server-rust-embedded` | StatefulSet | **1**, must stay 1 | a second replica is a second snowflake generator with the same machine id, so duplicate `event_id`s (`server-rust-embedded-sts-prod.yaml`) |
| `noetl-server-rust` | Deployment | **0** | retired; held at 0 for the same reason |
| `noetl-worker-rust` | Deployment | 2 | the user pool (`shared`), autoscaled by KEDA |
| `noetl-worker-system-pool`, `-shard1` | Deployments | 1 each | the system pool, not autoscaled |
| `noetl-cmdbus-writer` | StatefulSet | 1 | both buses ([10.3](ch10-03-bus-and-pools.md)) |
| gateway | Deployment | | captured from the live cluster, "STAGED, NOT APPLIED" (`ci/manifests/gateway/deployment.yaml`) |

Images come from the release pipeline ([Chapter 28](ch28-00-releases.md)):
`release.yml` publishes them to GHCR, the artifact of record, and they
are copied to the cluster's registry.

## Shape-only manifests

```admonish myth
"The manifest says which image runs." Not in production. The worker
and system-pool manifests have **no `image:` field**: "DECLARED BY THE
DEPLOY, NOT HERE" (`worker-rust-deployment-prod.yaml:134-142`). The
pins they used to carry fell behind live, so re-applying one rolled
prod back past shipped fixes (ai-meta#323). Server-side apply leaves a
field the manifest does not claim, so a shape-only file cannot roll an
image back. `shape-only-check.sh` fails if a pin creeps back in.
```

The server StatefulSet is the exception: its manifest still carries a
digest, marked as an as-built record to be treated as documentation.

## Committed is not live

A manifest is a copy of the cluster, and nothing forces it to agree:

- [ai-meta#267](https://github.com/noetl/ai-meta/issues/267) (opened
  2026-08-14, open) found the production manifests omitted **84** live
  environment variables. A full re-apply would have silently
  unconfigured production.
- A system-pool ScaledObject (3-10 replicas) is committed
  (`ci/manifests/keda/`), but the public resource model records on
  2026-11-11 that it is not on the cluster.

So read a manifest as intent. What runs is what the cluster reports,
and the version is what each pod's `*_build_info` says
([Chapter 30](ch30-00-observability.md)).

## Check your understanding

{{#quiz ../quizzes/ch27-02.toml}}
