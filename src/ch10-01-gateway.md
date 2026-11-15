# Gateway: The Gatekeeper

<span class="status status-real">REAL</span>

The gateway is the only part a client talks to. It decides **who** is
calling and **whether** they may, then passes the request to the server
and streams the results back. It never runs a tool and never reads or
writes your data on a client's behalf. Everything here is gateway
**v3.22.1** unless a page says otherwise.

## What it serves

| Route | What it is | Auth |
|---|---|---|
| `/api/auth/*` (`login`, `validate`, `check-access`, `logout`, providers) | sign-in and session checks | public |
| `/noetl/{*path}` (GET, POST, PUT, DELETE, PATCH) | the proxy: forwarded to the server's `/api/{path}` | session |
| `/graphql` | a GraphQL front for the same calls | session |
| `/noetl/mcp/*`, `/noetl/agents/*` | MCP and agent proxies ([Chapter 18](ch18-00-mcp-and-agents.md)) | session |
| `GET /events` | the client's live result stream (SSE) | session |
| `/ingress/{listener}` | push ingress for webhooks; refused unless `NOETL_INTERNAL_API_TOKEN` is set | token |

(`src/main.rs:350-523`.)

The session token can arrive as `Authorization: Bearer`, an
`X-Session-Token` header or a `session_token` cookie
(`src/auth/middleware.rs:111-142`).

## What the proxy does to a request

Before forwarding, the gateway:

1. checks that the session may use that route and owns the execution it
   names (`src/proxy.rs:214-257`);
2. **rewrites** `uid` / `user_uid` in the body to the verified session's
   user, so a client cannot act as someone else
   (`src/proxy.rs:286-311`);
3. forwards the body, `Content-Type`, `Accept` and `x-*` headers
   (`src/proxy.rs:358-380`).

It can also pick a server shard by `execution_id`
(`src/proxy.rs:118-150`).

## Sign-in is a playbook

```admonish myth
"The gateway checks sessions itself." By default it does not. It
validates a session by **starting a playbook** on the server
(`GATEWAY_SESSION_VALIDATE_VIA_PLAYBOOK`, default `true`,
`src/auth/mod.rs:177-181`) through `POST /api/execute`
(`src/noetl_client.rs:85-97`). It is an ordinary execution. Its default
path, `api_integration/auth0/auth0_validate_session`
(`src/config/gateway_config.rs:247`), has no `system/` prefix and the
gateway sends no pool override, so it runs on the **shared** pool
alongside user work ([10.3](ch10-03-bus-and-pools.md#which-pool-runs-a-step)). The synchronous REST
paths are off by default (`NOETL_AUTH_SYNC`, `NOETL_AUTHZ_SYNC`). The
gateway still decides; the check is a workflow.
```

That is the **code default**. A deployment can turn the synchronous
path on, and a code comment in gateway v3.22.1 says login and
validation sync (`NOETL_AUTH_SYNC`) "is already live in prod"
(`src/auth/mod.rs:224`). This book has not read the cluster, so it
states only the default and that comment.

Validated sessions are cached, so a request does not start a playbook
every time.

## Gatekeeper, not stateless

```admonish myth
"The gateway is stateless." It keeps three kinds of state:

- **sessions, the request store and execution owners** in EHDB
  key-value storage (`NOETL_KV_ADDR`, required at start-up,
  `src/main.rs:132-161`);
- the **open SSE connections**, in process (`ConnectionHub`);
- pending **callbacks**, in process (`CallbackManager`).

What it does not keep is *your* data. That is the rule that matters:
the gateway never reaches a database to satisfy a client request.
```

## How results get back

The gateway subscribes to the EHDB **events feed**
(`NOETL_EVENT_FEED_ADDR`, required, `src/main.rs:181-197`). For each
event it looks up which client started that execution and pushes it to
that client's `GET /events` stream (`src/event_feed.rs`).

```admonish warning title="The feed only carries what the server publishes"
At server v3.161.2 the server publishes an event to that feed only when
`NOETL_EVENT_INGEST_PUBLISH_ONLY=true` (code default `false`) and the
execution is not a `system/` playbook (`should_publish`,
`src/handlers/event_write.rs:304-318`). With code defaults the SSE
stream receives nothing. A deployment that streams results sets the
flag; this book has not read whether a given cluster does.
```

## Check your understanding

{{#quiz ../quizzes/ch10-01.toml}}
