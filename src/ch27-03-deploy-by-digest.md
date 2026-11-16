# Deploy by Digest

<span class="status status-real">REAL</span>

Production is changed by patching **one container's image, by
digest**, in one workload at a time. A digest (`image@sha256:…`) names
exact bytes; a tag can be moved, a digest cannot. This is the
procedure the public playbooks write down and have executed (ai-meta
`playbooks/257-worker-5115-noop-roll/README.md`, 2026-08-11;
`playbooks/516-ehdb-426-rollout/README.md`, 2026-11-04).

## The steps

1. **Record the rollback first.** Read the digest each workload runs
   now and write it down. `noetl/ops` keeps an append-only ledger per
   component (`ci/manifests/noetl/ledger/*.tsv`: version, digest,
   released, git sha, note); "the rollback target is the row above the
   one currently running".
2. **Dry-run against the server, and diff the whole object.** Render
   the patch with `--dry-run=server` and compare it with the live
   object. Proceed only if the diff is exactly the change you meant.
   `playbooks/517-floor-exact/roll2.sh` mechanizes this: it "refuses
   unless the diff is exactly the one intended change".
3. **Patch the named container only.** `kubectl set image <workload>
   <container>=<image>@sha256:<digest>`. A wildcard (`*=`) also
   replaces init containers; that broke a start-up check on kind
   (516 README). Container names differ between kind and production, and
   a wrong name makes `set image` a silent no-op
   (`playbooks/210-t5-readiness/ROLLBACK.md`).
4. **Verify from the process**, by the `version` on its `*_build_info`
   series, not from the Deployment spec.
5. **Rollback** is the same command with the recorded digest.

## Why not apply the manifest

```admonish warning title="2026-09-08: a 55-minute outage from one apply"
Reworked production manifests were applied after a server-side dry-run
that checked one field: that the running image would not change. It did
not. But the same manifest declared a volume for a claim that had never
existed. The writer pod could not schedule, and because it hosts both
buses, dispatch stopped for about **55 minutes**. Three of five
workloads also rolled, because removing pod-template annotations
changes the template hash. A whole-object diff would have shown the
volume at once (ai-meta wiki Sessions-Log, 2026-09-08).
```

The lesson is in step 2: a dry-run answers only the question you ask
it. Diff everything, and know before you patch whether the change
touches `spec.template`, because then the workload restarts.

## Check your understanding

{{#quiz ../quizzes/ch27-03.toml}}
