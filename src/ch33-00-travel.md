# Case Study: The Travel Playbooks

<span class="status status-real">REAL</span> <span class="status status-stub">STUB</span>

> Not yet written. Goals, sources and the quiz plan for this chapter are in
> [`docs/BOOK-PLAN.md`](https://github.com/noetl/book/blob/main/docs/BOOK-PLAN.md)
> (Part X and §2.8).

`noetl/travel`: a family of playbooks behind a travel app, read at commit `cd210d7`.

Planned sections:

- **33.1 From Screen to Playbook to Firestore** — the contract shape every playbook in the family shares: the app posts its own object, the playbook persists it and returns a render-ready payload; and the gateway allowlist that lets a signed-in user start these playbooks.
- **33.2 The Profile Flow: Read, Save, Read Back** — [written](ch33-02-profile-flow.md).
- **33.3 Provider Calls: Inline or Child Playbook** — HotelBeds, Duffel and Places through MCP playbooks; when a child playbook's hop cost is worth paying and when the planner inlines the call; how two copies of one provider drifted.
- **33.4 The Itinerary Planner: State Across Turns** — a conversational planner: threads, per-turn state, guards and routers in a long playbook.
- **33.5 Regression-Testing a Playbook Family** — `qa/regression`: cases, a suite, and a self-test that proves the harness can fail.
