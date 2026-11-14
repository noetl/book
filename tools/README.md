# Tools

Home of the NoETL-specific mdBook preprocessors planned in docs/BOOK-PLAN.md §4: `mdbook-noetl-trace`, `mdbook-noetl-play`, `mdbook-noetl-ref`.

## What is here now

| File | Does |
|---|---|
| `run-examples.sh` | T-02: runs every `examples/*/*/playbook.yaml` against the pinned CLI and diffs its output |
| `gen-appendices.py` | T-04: generates Appendices A–D from the server's DSL artifacts at the commit in `SERVER_SCHEMA_PIN` |
| `SERVER_SCHEMA_PIN` | the noetl/server commit (and tag, date) the appendices are generated from |
| `appendix-links.json` | which chapter teaches each DSL key (Appendix A's *Taught in* column) |
| `local-kinds.json` | the local runtime's accepted kinds at the pinned CLI, with the source (Appendix B's *Accepted locally* column) |

Regenerate the appendices (CI fails if the committed pages differ):

```bash
python3 tools/gen-appendices.py --fetch
```
