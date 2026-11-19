# Data Governance on NoETL

<span class="status status-partial">PARTIAL</span> <span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md)
> (§2.9 and Part XI).

Who may run and read what, what can be audited and reproduced, how secrets and personal data are kept out of the record, and the gaps, stated first.

Planned sections:

- **37.1 Access Control** (PARTIAL) — deny-by-default at the gateway with two roles and a playbook allowlist; execution ownership; role grants and verified-email inheritance in flight.
- **37.2 Audit and Reproducibility** (PARTIAL) — the event log and catalog versions as an audit trail; replay vs re-run; the secret-audit table that has no writer.
- **37.3 Secrets and Personal Data** (PARTIAL) — credentials by reference; the shape-matching result scrubber; no PII classifier.
- **37.4 Retention and the Right to Erasure** (PARTIAL) — an append-only, never-purged event log against deletion requests: keep personal data out of results and events by design.
- **37.5 Policy in Playbooks** (PARTIAL) — what is enforced at registration (inline-secret scan, tool-kind gates) and what is not (no policy-as-code engine).
