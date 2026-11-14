# Examples

Every example playbook the book shows lives here, and CI runs it
(`tools/run-examples.sh`, job `examples` in `.github/workflows/book.yml`)
against the **pinned** NoETL CLI in [`NOETL_CLI_VERSION`](NOETL_CLI_VERSION).
A chapter includes its example with `{{#include ../examples/<chapter>/<name>/playbook.yaml}}`,
so the page and the tested file cannot drift apart.

## Layout

```
examples/<chapter>/<name>/
  playbook.yaml        the example
  RUNTIME              local | daemon | distributed
  expected.json        normalised RunOutcome envelope   ┐
  expected.txt         the run's final_result as text   ├ exactly one
  expected-error.txt   stderr substring; run must FAIL  ┘
  args                 optional: extra `noetl run` args, one per line
```

## What is compared

`noetl run <playbook> -r local --json` prints one `RunOutcome` JSON
object on stdout: `status`, `playbook_name`, `executed_steps` (in
order), `step_results`, `final_result`, plus run-specific fields. The
runner deletes `started_at`, `completed_at`, `duration_seconds` and
`playbook_path`, sorts keys (`jq -S`) and diffs the rest. Nothing else
is normalised.

`daemon` and `distributed` examples are listed and skipped on PRs with
a visible notice. They need a running daemon or cluster; a nightly
kind job may run them later.

## Adding an example

```bash
mkdir -p examples/ch04/my-example
$EDITOR examples/ch04/my-example/playbook.yaml
echo local > examples/ch04/my-example/RUNTIME
noetl run examples/ch04/my-example/playbook.yaml -r local --json \
  | jq -S 'del(.started_at,.completed_at,.duration_seconds,.playbook_path)' \
  > examples/ch04/my-example/expected.json
tools/run-examples.sh
```

**Read `expected.json` before committing it.** Generating it from a run
records whatever the runtime did, including a bug. If the output is
not what the chapter says should happen, the chapter or the example is
wrong, and the PR must say which.

## Bumping the pinned CLI

Change `NOETL_CLI_VERSION`, run `tools/run-examples.sh`, and treat
every diff as a possible change in behaviour that the chapters must
reflect. Update Appendix E with the new version in the same PR.
