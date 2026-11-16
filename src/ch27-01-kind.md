# Local kind First

<span class="status status-real">REAL</span>

[kind](https://kind.sigs.k8s.io/) runs Kubernetes in containers on one
machine. NoETL's kind cluster runs the same components as production:
server, worker pools, the `cmdbus-writer` and the gateway
([Chapter 10](ch10-00-distributed-runtime.md)).

## The cluster

`noetl/ops` `ci/kind/config.yaml` defines a cluster named **`noetl`**
(kube context `kind-noetl`). It maps host ports to the services, among
them:

| Host port | Service |
|---|---|
| 8082 | NoETL server API |
| 38090 | gateway API |
| 54321 | Postgres |

`automation/infrastructure/kind.yaml` creates it (`kind create cluster
--config=ci/kind/config.yaml`), on a Podman machine named `noetl-dev`.

## Converge the topology

The current kind path is a set of NoETL playbooks, run with the CLI in
local mode (`automation/ehdb/README.md`):

```bash
# from a clone of noetl/ops
noetl run automation/ehdb/ehdb_platform.yaml --runtime local \
  --set action=converge --set profile=kind --set context=kind-noetl
```

| `action` | Does |
|---|---|
| `plan` | renders every object and server-side dry-runs it; changes nothing |
| `converge` | reconciles the topology, then verifies it |
| `status` | reports what is deployed and checks the EHDB-only invariants |
| `verify` | the functional proof on an already-converged cluster |
| `teardown` | removes the ScaledObject and the writer; keeps the volumes |

It drives four child playbooks: the writer (`ehdb_writer.yaml`), the
server, pools and gateway (`ehdb_runtime.yaml`), the user pool's
autoscaler (`ehdb_autoscaler.yaml`) and the proof (`ehdb_verify.yaml`).

```admonish tip title="The profile is a guard"
`profile=kind` refuses any context that is not `kind-*`, and
`profile=prod` refuses one that is. A kind command cannot reach
production by a wrong default context. Pass `context` explicitly
anyway: the default kube context is whatever you last used.
```

Under `profile=kind`, images are local (`imagePullPolicy: Never`),
volumes small, and the writer image is set by `writer_image`. Build the
images from the tagged release you mean to test and load them with
`kind load`. This topology exists as code only because it was
reconstructed: after NATS was deleted (2026-08-01) the production shape
had been made by hand and "never written back" (`automation/ehdb/README.md`).

## The older playbook is stale

```admonish warning title="automation/development/noetl.yaml"
The contributor rules still name `automation/development/noetl.yaml`
(`action=redeploy`). At `6c55cbe` it builds the legacy Python image
(`docker/noetl/dev/Dockerfile`), applies NATS manifests, and rewrites
the image in every file under `ci/manifests/noetl/`, which now includes
the production manifests. It was last changed 2026-05-23. Do not use it
for the current stack.
```

## Check your understanding

{{#quiz ../quizzes/ch27-01.toml}}
