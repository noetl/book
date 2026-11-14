# The Local Event Buffer and `noetl push`

<span class="status status-real">REAL</span>

A local run normally leaves no history. With `--event-buffer`, it
records its events the way a server would, in a local file you can
read or ship to a server later (`noetl run --help`, `noetl buffer
--help`, `noetl push --help`, CLI v6.4.0).

```console
$ noetl run playbook.yaml -r local --event-buffer
$ noetl buffer list --json
$ noetl buffer cat <execution_id>
```

- Each run gets a directory `$NOETL_LOCAL_DIR/<execution_id>/`. The
  default is `~/.noetl/local`. It holds `events.feather` (Apache
  Arrow Feather V2) and `metadata.json` (status, event count, start and
  end times).
- The events are `playbook.started`, one `step.exit` per step, and
  `playbook.completed` or `playbook.failed`. A step that ran several
  times appears **once** ([Chapter 2](ch02-00-project-first-playbook.md)).
- `noetl buffer cat` prints the events as JSON lines.
  `noetl buffer append` lets a `shell` step add its own events, for
  example infrastructure facts.

## Shipping a run to a server

```console
$ noetl push <execution_id>
$ noetl push --all --dry-run
```

`noetl push` POSTs each closed buffer to the server's
`/api/events/batch` as an Arrow file. The server appends the events to
its event log **without orchestrating** them: it records the history
and does not resume or re-run anything. Buffers are pushed oldest
first, and `pushed_at` is written to `metadata.json` so each one is
sent once.

```admonish note
Pushing needs a reachable server and the right context or
`--server`. That is distributed-runtime territory
([Chapter 10](ch10-00-distributed-runtime.md)). The book's CI does not
push.
```

## Check your understanding

{{#quiz ../quizzes/ch08-04.toml}}
