# Credentials and Secrets

<span class="status status-real">REAL</span>

[Section 4.4](ch04-04-keychain.md) showed how a playbook *refers* to a
credential: an `auth:` alias or a `{{ keychain.<alias>.<field> }}`
template, never the secret itself. This chapter follows the secret
behind the alias: how the server stores it, how it reaches a worker,
what keeps it out of the event log, and which protections are switched
off until you turn them on.

Code facts are server **v3.161.2** and worker **v6.15.0**; manifest
facts are `noetl/ops` at **`6c55cbe`**. No secret, store path or alias
of any deployment appears here.

## Stored: encrypted, and fail-closed

Credentials and keychain entries are stored with **envelope
encryption**: each record has its own data key, wrapped by a key
encryption key (KEK) (server `src/crypto/envelope.rs:117`; one cipher
serves both stores, `src/main.rs:1451`).

- The KEK comes from **`NOETL_ENCRYPTION_KEY`**. Without it, or with an
  empty value, the server **refuses to start**; the old all-zero
  default key is gone (`src/main.rs:1119-1158`).
- `NOETL_ALLOW_INSECURE_DEFAULT_KEY=true` starts it anyway with a
  random key per process, so anything written is unreadable after a
  restart. It exists for throwaway tests.
- `NOETL_KMS_PROVIDER=gcp-kms` (with `NOETL_GCP_KMS_KEY`) moves the KEK
  into Cloud KMS. The default is `local` (`src/crypto/mod.rs:33-61`).
- Every secret variable can be given as a file: `<VAR>_FILE` is read
  into the environment at the top of `main` (`src/main.rs:1180-1184`).

## Delivered: what a worker fetches

When a step names an alias, the worker asks the server for it:
`GET /api/credentials/<alias>?include_data=true&execution_id=…`
(worker `src/client/control_plane.rs:918-946`). Without
`include_data=true` the server returns metadata only
(server `src/handlers/credentials.rs:31-33`). With it, the response is
the **decrypted** secret. If the store has no such alias, the server
can resolve it from a `provider:` keychain entry (GCP, AWS, Azure,
Vault, Kubernetes; `src/secrets/mod.rs:116-131`) and caches the result
for that execution.

Three protections sit around that call. All three are off or
permissive by default:

| Protection | Default | To turn it on |
|---|---|---|
| bearer gate on the credential routes | **shadow**: counts what it would reject, rejects nothing; a typo also means shadow (`src/auth_gate.rs:25-93`) | `NOETL_INTERNAL_AUTH_MODE=enforce`, with `NOETL_INTERNAL_API_TOKEN` on server and every caller |
| sealed delivery: the secret encrypted to the worker's own key (X25519, HKDF-SHA256, ChaCha20-Poly1305) | off; plaintext fetch (worker `src/executor/auth_alias.rs:425-460`) | `NOETL_SEALED_CREDENTIALS=true` and `WORKER_ID` on the worker |
| mTLS between worker and server | off; plain HTTP (server `src/tls.rs`, worker `src/client/tls.rs`) | `NOETL_TLS_CERT`/`NOETL_TLS_KEY`/`NOETL_TLS_CLIENT_CA` on the server, `NOETL_TLS_CLIENT_CERT`/`NOETL_TLS_CLIENT_KEY` on the worker |

```admonish warning title="Shadow means open"
With the gate in its default shadow mode, anything that can reach the
server's credential routes can read decrypted credentials. On any
deployment that holds real secrets, set `NOETL_INTERNAL_AUTH_MODE=enforce`
and make sure every legitimate caller sends the token; the shadow
counters exist to tell you which callers those are before you switch.
```

Sealed delivery covers only the `auth:` path. A `{{ keychain.* }}`
template is resolved through the plaintext fetch even when sealing is
on (worker `src/executor/keychain_namespace.rs:183`).

## Kept out of the event log

The event log is append-only and never purged, so a secret written
there stays for the life of the deployment. Three mechanisms keep it
out:

1. **The server does not render `keychain.*` templates.** It renders
   everything else in a step and leaves those for the worker
   (`orchestrate-core/src/template.rs:299-345`, used by
   `commands.rs:370-378`). The dispatched command carries the template,
   not the value.
2. **The drive command never resolves secrets.** A drive pass runs as a
   command too ([10.2](ch10-02-server.md)). The worker skips keychain
   resolution for it (`src/executor/command.rs:480-492`, marked as a
   leak fix): before the guard, a step two or more hops into a playbook
   could carry a resolved bearer token into `command.issued`. The guard
   shipped on 2026-07-08 in worker v5.70.3 (commit `2031a8b4`).
3. **Results are scrubbed** before they are stored or cached: values
   under sensitive key names, and strings that look like secrets
   (bearer tokens, JWTs, `sk-…`, `ghp_…`), become `[REDACTED]`
   (worker `src/scrub.rs:25-51`, applied at `command.rs:2068`).

```admonish warning title="The scrubber matches shapes, not your secrets"
It does not know the values in your keychain. A tool that echoes a
secret in an unrecognised shape under an innocent key name gets it
stored. Do not print credentials from a step, even to debug.
```

The server also refuses to register a playbook that contains obvious
secret material ([4.4](ch04-04-keychain.md#why-not-inline)).

## Not in the worker's environment, by convention

Business credentials belong in the keychain, not in a worker's
environment. That is a deployment rule, not something the code
enforces: `NOETL_KEYCHAIN_ENV_VARS` is an allow-list of environment
variables the worker copies into every command's secrets (empty by
default, worker `src/executor/command.rs:55-63`). Anything listed there
is visible to every step on that pool. The production manifests use it
for one platform token on the system pools only.

## Bootstrap secrets: files, not the wallet

Three secrets cannot live in the credential store, because the store
needs them:

| Secret | Why it cannot be in the wallet |
|---|---|
| `NOETL_ENCRYPTION_KEY` | it decrypts the wallet |
| `POSTGRES_PASSWORD` | the wallet is a Postgres table |
| `NOETL_INTERNAL_API_TOKEN` | it authenticates calls to the wallet |

In the production manifests they arrive as **files** projected from
Google Secret Manager through the Secrets Store CSI driver
(`*_FILE` variables), not as Kubernetes Secret references
(`ci/manifests/noetl/*-prod.yaml`). The user pool and the writer mount
no secrets. Per the dated record, the move to files finished on
2026-08-28; a file is present or absent at start-up, with nothing to
hang on.

## Built but not doing anything yet

```admonish partial title="Three features that ship inert"
- **Secret audit.** The `noetl.secret_audit` table is created at every
  start and has a read endpoint, but at v3.161.2 nothing writes to it:
  the audit service has no caller outside its own module. Expect it to
  be empty. `NOETL_SECRET_AUDIT_REQUIRED` is parsed and has no effect.
- **Residency.** Region tags, a residency policy and a cross-region
  broker exist, but with `NOETL_SERVER_REGION` unset the server runs in
  "legacy mode" and checks nothing (`src/secrets/mod.rs:96-108`).
- **KEK rotation** is an internal endpoint
  (`POST /api/internal/wallet/rotate-kek`); it runs only when someone
  calls it.
```

So "the wallet supports X" and "your deployment does X" are different
claims. Check each setting on your deployment.

## Check your understanding

{{#quiz ../quizzes/ch31-00.toml}}
