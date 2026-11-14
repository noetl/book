#!/usr/bin/env bash
# T-02 (#4): run every example playbook and diff it against its expected output.
#
# Layout: examples/<chapter>/<name>/
#   playbook.yaml        the example (what the chapter shows, byte for byte)
#   RUNTIME              local | daemon | distributed
#   exactly one of:
#     expected.json      the normalised RunOutcome envelope (see below)
#     expected.txt       the run's `final_result`, as text
#     expected-error.txt a substring that must appear on stderr; the run must FAIL
#   args (optional)      extra `noetl run` arguments, one per line (e.g. --set who=book)
#
# Normalisation: `noetl run <pb> -r local --json` prints one RunOutcome JSON
# object on stdout. The fields that change on every run (started_at,
# completed_at, duration_seconds) and the machine-specific playbook_path are
# deleted; the rest is compared after `jq -S` (sorted keys). Nothing else is
# rewritten, so a change in what a step returns is a real diff.
#
# Only `local` examples run here. `daemon` / `distributed` examples are listed
# and skipped with a visible notice (they need a running daemon or cluster).
#
# Usage: tools/run-examples.sh [examples-dir]     (needs `noetl` and `jq` on PATH)
set -uo pipefail

ROOT="${1:-examples}"
NOETL="${NOETL:-noetl}"
pass=0; fail=0; skip=0
failed=()

echo "noetl CLI: $("$NOETL" --version)  (pinned: $(cat "$ROOT/NOETL_CLI_VERSION" 2>/dev/null || echo '?'))"

normalise() { jq -S 'del(.started_at, .completed_at, .duration_seconds, .playbook_path)'; }

while IFS= read -r pb; do
  dir="$(dirname "$pb")"; name="${dir#"$ROOT"/}"
  runtime="$(tr -d '[:space:]' < "$dir/RUNTIME" 2>/dev/null || echo missing)"
  case "$runtime" in
    local) ;;
    daemon|distributed)
      echo "::notice title=example skipped::$name needs the $runtime runtime; not run on PRs"
      echo "SKIP  $name ($runtime)"; skip=$((skip+1)); continue ;;
    *) echo "FAIL  $name: RUNTIME file missing or invalid ('$runtime')"; fail=$((fail+1)); failed+=("$name"); continue ;;
  esac

  extra=()
  if [[ -f "$dir/args" ]]; then while IFS= read -r a; do [[ -n "$a" ]] && extra+=("$a"); done < "$dir/args"; fi

  out="$(mktemp)"; err="$(mktemp)"
  "$NOETL" run "$pb" -r local --json "${extra[@]+"${extra[@]}"}" >"$out" 2>"$err"; rc=$?

  ok=1; why=""
  if [[ -f "$dir/expected-error.txt" ]]; then
    want="$(cat "$dir/expected-error.txt")"
    if [[ $rc -eq 0 ]]; then ok=0; why="expected the run to fail, it exited 0"
    elif ! grep -qF -- "$want" "$err"; then ok=0; why="stderr does not contain: $want"; fi
  elif [[ $rc -ne 0 ]]; then
    ok=0; why="exit $rc"
  elif [[ -f "$dir/expected.json" ]]; then
    if ! diff -u <(normalise < "$dir/expected.json") <(normalise < "$out") > "$out.diff"; then ok=0; why="output differs"; fi
  elif [[ -f "$dir/expected.txt" ]]; then
    if ! diff -u "$dir/expected.txt" <(jq -r '.final_result // ""' < "$out") > "$out.diff"; then ok=0; why="final_result differs"; fi
  else
    ok=0; why="no expected.json / expected.txt / expected-error.txt"
  fi

  if [[ $ok -eq 1 ]]; then
    echo "PASS  $name"; pass=$((pass+1))
  else
    echo "FAIL  $name: $why"; fail=$((fail+1)); failed+=("$name")
    [[ -s "$out.diff" ]] && cat "$out.diff"
    echo "--- stderr ---"; cat "$err"
    echo "::error title=example failed::$name: $why"
  fi
  rm -f "$out" "$err" "$out.diff"
done < <(find "$ROOT" -mindepth 2 -name playbook.yaml | LC_ALL=C sort)

echo
echo "examples: $pass passed, $fail failed, $skip skipped (of $((pass+fail+skip)))"
[[ $fail -eq 0 ]]
