# Validate Before You Run

<span class="status status-real">REAL</span>

The quantum project's optimize playbook runs for hours on the local
runtime, inside a notebook session that is killed after twelve. A typo
found at hour six wastes the whole session. So the project validates
every playbook against the live grammar before anything runs: in CI on
every push, and again whenever the playbook changes. This section shows
how, and what the validator can and cannot tell you.

The source is [`noetl/quantum`](https://github.com/noetl/quantum) at
commit **`9208fa2`**: `vqcc/dsl_validate.py`,
`scripts/validate_playbooks.py` and `.github/workflows/ci.yml`. The
server side is `src/handlers/dsl.rs` at server **v3.161.2**. The public
endpoint was read on **2026-11-17**, when it reported server 3.165.1.

## The API

[Chapter 4](ch04-00-anatomy-of-a-playbook.md) introduced the
validator. It is a server route, `POST /api/dsl/validate`, that runs
registration's checks *and* the parser on a document, without
registering, storing or executing anything. On your own server it
exists only if `NOETL_DSL_KB=true`, which is off by default
(`src/handlers/dsl.rs:18-21`). The public deployment at `noetl.ai`
has it on, and no credentials are needed: the route reads only compiled
grammar.

The project posts the YAML text as it is:

```bash
curl -s -X POST https://noetl.ai/api/dsl/validate \
  -H 'Content-Type: application/yaml' \
  --data-binary @playbooks/vqcc_optimize.yaml
```

On 2026-11-17 that returned:

```json
{
  "valid": true,
  "register_verdict": "accept",
  "execute_verdict": "accept",
  "kind": "playbook",
  "path": "playbooks/vqcc_optimize",
  "findings": [],
  "schema_digest": "sha256:25071111774314cbf0c83ee9925b53701c2228232574bda3b13b1e27d58b372c",
  "api_version": "noetl.io/v2",
  "note": "Dry run: nothing was registered, stored or executed."
}
```

## Two verdicts, because registration does not parse

The response has two verdicts because they can disagree
(`validate_document`, `src/handlers/dsl.rs:230-300`):

- `register_verdict` comes from the same functions catalog registration
  calls: identity, tool kinds and inline secrets.
- `execute_verdict` adds the playbook parser, which registration does not
  run. The parser checks the `start` step, unique step names, `next`
  targets and similar rules.

A playbook with no step named `start` shows the gap. On 2026-11-17 the
public endpoint answered such a probe with
`"register_verdict": "accept"`, `"execute_verdict": "reject"` and one
finding, `playbook_rule: Workflow must have a step named 'start'`.
The catalog would accept that playbook, and every attempt to run it
would fail ([Appendix F](appendix-06-myths.md)).

The probe had a second error as well, a `next` target that does not
exist, but the response reported only the first. Registration checks
each report their own findings. The parser stops at its first error
(`parse_verdict`, server `src/services/catalog.rs:598-607`). So fix the
finding, validate again, and repeat until `findings` is empty.

## The grammar moves, so pin what you validated against

Every response carries `schema_digest`, a hash of the JSON Schema that
server accepts. The quantum playbook's header records each
revalidation with its date, the server version and the digest
(`playbooks/vqcc_optimize.yaml:1-23`). Between 2026-11-10 and
2026-11-13 the digest changed twice. A "valid" from last week is a
claim about last week's server.

The server can also tell you when your pin is stale: send the digest
you generated against as `x-noetl-schema-digest`, and if it differs
the response gains a `schema_drift` field (`validate_response`, `src/handlers/dsl.rs:302-329`
at v3.161.2; still present at v3.165.1). The project sends that header
(`vqcc/dsl_validate.py:55`).

```admonish warning title="The drift field did not arrive"
On 2026-11-17, a request to the public endpoint with a mismatched
`x-noetl-schema-digest` came back **without** `schema_drift`, in two
tries with different header casing. The server code adds it, so
something between the client and the server drops the header. Do not
treat a missing `schema_drift` as proof that your pin is current.
Compare digests on the client: fetch `GET /api/dsl/version` and
compare its `schema_digest` with the one you pinned. The project's
script prints both side by side for that reason.
```

## A fallback is not a pass

When `noetl.ai` cannot be reached, the project still runs a local
check: a step named `start`, no duplicate names, every `next` target
exists (`local_semantic_check`, `vqcc/dsl_validate.py:77-122`). That
check is labelled `"remote": false`, with its source. It never counts
as acceptance. A playbook is `accepted` only when the **remote**
answer is `valid: true` (line 152), and the CI script exits 1 when the
API was not reached at all (`scripts/validate_playbooks.py`). A
validator that quietly falls back to a weaker check and reports green
gives you less than no validator, because you believe it.

## What to copy

- Validate in CI against the server you will run on, not only against
  a local schema copy.
- Read both verdicts. `register_verdict: accept` does not mean the
  playbook can run.
- Re-validate after each fix: the parser reports one rule at a time.
- Record the digest and date of each validation, and compare digests
  yourself.
- Label any fallback as a fallback, and never count it as a pass.

## Check your understanding

{{#quiz ../quizzes/ch35-02.toml}}
