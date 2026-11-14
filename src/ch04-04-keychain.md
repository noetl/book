# `keychain`: Credentials by Reference

<span class="status status-real">REAL</span>

A playbook never contains a secret. It contains a **reference**, an
alias such as `pg_main` or `openai_token`, and NoETL resolves the alias
to the secret only at the moment a worker runs the step. This section
explains why, and the two ways to write a reference.

## Why not inline?

Everything a NoETL server knows about an execution is in its event
log, which is append-only and never purged ([Chapter 3](ch03-02-event-sourcing.md)).
A step's rendered configuration travels in the event that dispatches
it. A password typed into a playbook would therefore live in the log
for the life of the deployment, with no way to remove it.

So the server **refuses** a playbook at registration if it finds
unambiguous secret material in it: a PEM private-key block, a
service-account JSON with both `private_key` and `client_email`, a
three-part JWT, or a provider-prefixed token such as `AKIA…` or `ghp_…`.
The error names the YAML path and the kind of material. It never
echoes any part of the value (`src/services/secret_material.rs`,
called from `registration_checks`, server v3.161.2). The check is
deliberately conservative: it does not guess from entropy, so a
secret that matches none of those patterns gets through, and keeping
it out remains the author's job.

## Two ways to reference a credential

### 1. `auth: <alias>` on the tool

```yaml
- step: load_users
  tool:
    kind: postgres
    auth: pg_main
    query: "SELECT id, email FROM users LIMIT 10"
```

When the worker runs the step, it fetches the credential stored under
`pg_main` from the server (`GET /api/credentials/<alias>`). It then
merges the credential into the tool's configuration according to the
credential's `type`: `postgres` becomes host, port, user, password and
database; `bearer`, `api_key` and `basic` become an HTTP auth block;
`nats`, `pubsub` and `kafka` become source connection fields;
`snowflake` becomes Snowflake fields. Any other type is an error
(`src/executor/auth_alias.rs`, worker v6.15.0). The worker also
accepts the key `credential:` in place of `auth:`.

An alias that is not in the keychain fails the step cleanly, with
``Credential alias '<name>' not found in keychain``. It does not hang.

### 2. `{{ keychain.<alias>.<field> }}` in a template

```yaml
- step: call_api
  tool:
    kind: http
    method: GET
    url: https://api.example.com/v1/items
    headers:
      Authorization: "Bearer {{ keychain.example_api.api_key }}"
```

The server renders every other template in a step before dispatching
it, but it **leaves `keychain.*` templates unrendered**
(`render_value_deferring_keychain`, `orchestrate-core/src/template.rs`,
server v3.161.2). The worker resolves the alias, renders the template
in memory, and runs the step. The secret is therefore never written
into the dispatched command or the event log.

```admonish warning title="An unresolved keychain template renders as empty"
By default, if `{{ keychain.example_api.api_key }}` cannot be
resolved, it renders to an **empty string**, and the step runs anyway.
In the example above it would send `Authorization: Bearer ` and get a
401 from the API, which looks like a problem with the API rather than
with the alias. A worker started with `NOETL_KEYCHAIN_STRICT=true`
fails the step instead. That setting is off by default
(`src/executor/keychain_namespace.rs`, worker v6.15.0).
```

## The `keychain:` block

The top-level `keychain:` list says how an alias is **sourced**, when
it is not simply a credential registered with the server. Each entry
has a `name` (the alias) and, among other fields:

- `provider`: the secret backend that resolves it: `gcp` (Google
  Secret Manager), `aws`, `azure`, `vault` or `k8s`;
- `map`: output key → secret-path template;
- `auth`: the credential used to authenticate to the provider itself;
- `region`, `residency`, `allowed_regions`, `no_broker_fallback`:
  data-residency controls.

The full field list is generated in
[Appendix A](appendix-01-dsl-reference.md#keychaindef). [Chapter 31](ch31-00-credentials.md)
covers how keychain entries are stored, sealed and rotated.

## There is no default connection, by convention

The NoETL convention is that **every step that touches a credentialed
resource names its credential explicitly**. There is no ambient
database, and no environment-level fallback.

```admonish warning title="The postgres tool does not enforce this"
Checked at tools v4.6.0 (the version worker v6.15.0 uses): if a
`postgres` step has no `auth` (or `credential`) and no connection
fields, `PostgresTool` **builds a default connection** to
`localhost:5432`, user `postgres`, database `postgres`, with no
password (`build_connection_string`, `src/tools/postgres.rs`). The
worker does not refuse such a step: its alias resolver returns
early when there is no alias (`src/executor/auth_alias.rs`). The
worker's own comment says such a step "fell back to a default
(unreachable) connection".

So the rule holds only if you follow it. Always give a `postgres`
step an `auth`.
```

## Locally

The local runtime has its own credential store, outside any server:

```console
$ noetl credential set example_api      # prompts for the secret
$ noetl credential list                 # aliases and types, never values
```

At CLI v6.4.0, `credential: <alias>` in `http` and `agent` steps reads
from this store ([Chapter 8](ch08-00-local-runtime.md)).

## Check your understanding

{{#quiz ../quizzes/ch04-04.toml}}
