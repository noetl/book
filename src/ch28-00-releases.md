# Releases and Version Pinning

<span class="status status-real">REAL</span>

Every NoETL release you can run (a server image, a worker image, a CLI
tarball) is cut by a machine from commit messages. Knowing how that
machine decides tells you two things: why a merged fix may never ship,
and which number to trust when two disagree.

Facts here are each repository's `.github/workflows/semantic-release.yml`,
`release.yml` and `.releaserc.json` on `main`, read on **2026-11-15**,
plus the run logs and issues cited.

## The pipeline

1. A PR merges to `main`. By convention it is a merge commit, though
   the repositories' settings also allow squash.
2. `semantic-release` runs on the push (`semantic-release.yml`,
   semantic-release 24.2.3, preset `conventionalcommits`). It reads
   **every commit since the last tag** and picks a version, or none.
3. If it picks one, it tags it and dispatches `release.yml` with that
   version. It has to dispatch explicitly: a tag pushed with the
   workflow's own token does not trigger other workflows.
4. `release.yml` builds and publishes: the crate, the container image
   (`ghcr.io/noetl/<repo>:<version>`), and a GitHub Release.

## Which commits release

From `@semantic-release/commit-analyzer`'s default rules
(`lib/default-release-rules.js`), which the `.releaserc.json` files do
not override:

| Commit | Releases |
|---|---|
| `feat!: …`, or `BREAKING CHANGE:` in the body | major |
| `feat: …` | minor |
| `fix: …`, `perf: …`, a revert | patch |
| `chore:`, `docs:`, `test:`, `refactor:`, anything else | **nothing** |

```admonish myth
"Only the merge subject counts." semantic-release analyses each commit
on the branch, not just the merge. The logs show it: on 2026-11-08 the
server run analysed ten commits, four "Merge pull request" subjects and
six `chore:` commits, and ended "There are no relevant changes, so no
new version is released" (`semantic-release.yml` run of `5cf0712d`). A
"Merge pull request" subject is not a conventional commit and counts
for nothing.
```

The last row of the table is the trap. A `chore:` merge produces a
green build and no release, and nothing says so. The change sits on
`main`, correct and undeployable. If a change must reach a cluster, it
needs a releasing type. After merging, check that the tag moved:

```bash
git fetch origin --tags && git tag --sort=-v:refname | head -1
```

### The escape hatch

`release.yml` also accepts a manual dispatch with a `version` input.
That publishes whatever version you type, bypassing the commit check.
It has been used. Server **v3.153.0** was published by a manual
dispatch at 19:02 UTC on 2026-11-08, about fourteen hours after
semantic-release had declined that commit (the two runs above, and
the release's own timestamps). Its four PRs were all `chore:`.

## The tag is the version

```admonish myth
"`Cargo.toml` says which version this is." On the server, worker and
tools repositories it does not. The release bot no longer commits the
version bump to `main` (a required status check rejects that push), so
the committed `version` is a **floor** that lags behind the tags. On
2026-11-15: server `Cargo.toml` 3.112.3, newest tag v3.163.1; worker
6.0.0 vs v6.18.0; tools 4.0.1 vs v4.7.0. `release.yml` says it
directly: "THE TAG IS AUTHORITATIVE, NOT Cargo.toml".
```

Each build job writes the tag's version into `Cargo.toml` before
compiling (`ci/stamp-version.sh`), so the binary knows its real
version. A running service reports it as the `version` label of its
`*_build_info` metric (server `src/metrics.rs:885-900`). That label is
the version a cluster runs. A manifest, a note or `Cargo.toml` is a copy.

The CLI and gateway repositories still commit the bump (`chore(release):
version 6.4.1 [skip ci]` on the CLI), so there the two agree.

## Never set the version by hand

On 2026-08-03 a runbook step told an operator to bump the worker's
`Cargo.toml` by hand before tagging. semantic-release ran on the same
merge without knowing:

- main ended up at **5.91.3**, below the hand-pushed tag **v5.92.0**;
- two images had identical code and different versions;
- the next automatic release would have sorted below 5.92.0.

Prod was unaffected, because it was rolled by image digest, not tag. It
took two more releases to climb back above the hand-made number
([ai-meta#224](https://github.com/noetl/ai-meta/issues/224), closed
2026-08-04). Merge with a conventional type and let the pipeline choose.

## A commit type is an unchecked semver claim

semantic-release knows only the prefix. On 2026-09-07 `noetl-tools`
v3.27.0 added a public field to a struct that another crate builds with
a struct literal. In Rust that breaks the caller, yet it shipped as a
**minor**, because the commit said `feat:`. It stayed hidden until a
consumer next resolved its caret range
([ai-meta#330](https://github.com/noetl/ai-meta/issues/330), open).
So pin exact versions where breakage would hurt, and treat a caret
range as a decision the resolver makes later.

## How this book pins

The book follows its own advice:

| Pin | What it fixes |
|---|---|
| `examples/NOETL_CLI_VERSION` (`6.4.1`) | the CLI that CI downloads, checksum-verified, to run every example |
| `tools/SERVER_SCHEMA_PIN` (server `v3.161.2`, commit `983e36e`) | the server the generated appendices come from |

Every REAL page names the release its claims were checked against.
Bumping a pin is a reviewed change: the generated diff shows what moved.

## Check your understanding

{{#quiz ../quizzes/ch28-00.toml}}
