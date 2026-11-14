# `apiVersion`, `kind`, `metadata`

<span class="status status-real">REAL</span>

The first three keys say what the document is and where it lives.

```yaml
apiVersion: noetl.io/v2
kind: Playbook
metadata:
  name: anatomy
  path: book/ch04/anatomy
  description: The parts of a playbook, smallest useful form.
  labels:
    chapter: "4"
```

## `apiVersion` and `kind`

Both are required strings with exactly one accepted value each. The
server's validator compares them with constants in the grammar
(`noetl_orchestrate_core::dsl::API_VERSION` and `PLAYBOOK_KIND`) and
refuses anything else, for example `Unsupported API version: noetl.io/v1.
Expected noetl.io/v2` (`src/playbook/parser.rs:164-183`, server
v3.161.2). The same constant is what a server reports from `GET
/api/dsl/version`, so the two cannot disagree.

`kind` is also how the catalog tells document types apart: the same
catalog holds other kinds, such as `Subscription` documents for the
daemon ([Chapter 9](ch09-00-daemon.md)), which are validated
differently.

## `metadata`

| Key | Required | Meaning |
|---|---|---|
| `name` | yes | The playbook's name. Appears in every run result as `playbook_name`. |
| `path` | | Its address in the catalog, such as `book/ch04/anatomy`. Other playbooks call it by this path. |
| `description` | | Free text. |
| `labels` | | A map of string to string, for filtering. |

When a playbook is registered without a `path`, the catalog uses its
`name` as the path (`registration_identity`, `src/services/catalog.rs:498`).
Registration fails only if both are missing.

`metadata` also carries three **opt-in extensions**. The schema does
not list them, because each is read only when a server flag turns its
feature on. With the flag off, the key is ignored. Each one has its
own chapter:

| Key | What it does | Server flag (default off) | Chapter |
|---|---|---|---|
| `metadata.expose.mcp` | Publishes the playbook as one MCP tool at `POST /api/mcp` | `NOETL_MCP_SERVER` | [18](ch18-00-mcp-and-agents.md) |
| `metadata.expose.agent` | Publishes it as an agent with a card at `/api/agents/*` | `NOETL_AGENT_ENDPOINT` | [18](ch18-00-mcp-and-agents.md) |
| `metadata.catalog.hot_reload` | Lets named sub-playbooks resolve `@latest` inside a pinned run | `NOETL_CATALOG_HOT_RELOAD` (also needs `NOETL_CATALOG_PINNING` and `NOETL_CATALOG_CAS`) | [16](ch16-00-distributed-catalog.md) |

The table is generated from the server's DSL manifest
(`metadata_extensions`, `dsl-manifest.json` at v3.161.2). The full list of
flags is in [Appendix C](appendix-03-flags.md).

```admonish partial
All three extensions are released code, but every one of them is off
unless the server sets its flag. This book does not say whether any
particular deployment sets them.
```

## Check your understanding

{{#quiz ../quizzes/ch04-01.toml}}
