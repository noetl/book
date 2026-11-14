#!/usr/bin/env python3
"""Validate every example playbook against the server's playbook.schema.json.

Constitution / CH-04 AC5: every example validates against the schema at the
pinned server commit (tools/SERVER_SCHEMA_PIN). Run after
`tools/gen-appendices.py --fetch` (which downloads the schema into
.schema-cache/).

An example that is *meant* to be invalid (to show an error) contains a file
`schema-invalid` whose first line is a substring of the expected validation
error. Anything else must validate cleanly.

Usage: tools/validate-examples.py [examples-dir] [schema-path]
Needs: pip install jsonschema pyyaml
"""
import os
import sys

import jsonschema
import yaml

root = sys.argv[1] if len(sys.argv) > 1 else "examples"
schema_path = sys.argv[2] if len(sys.argv) > 2 else ".schema-cache/playbook.schema.json"
schema = yaml.safe_load(open(schema_path))
validator = jsonschema.Draft202012Validator(schema)

ok = bad = 0
for dirpath, _, files in sorted(os.walk(root)):
    if "playbook.yaml" not in files:
        continue
    name = os.path.relpath(dirpath, root)
    doc = yaml.safe_load(open(os.path.join(dirpath, "playbook.yaml")))
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    msgs = [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors]
    marker = os.path.join(dirpath, "schema-invalid")
    if os.path.exists(marker):
        want = open(marker).readline().strip()
        if errors and any(want in m for m in msgs):
            print(f"PASS  {name} (invalid as expected: {want})"); ok += 1
        else:
            print(f"FAIL  {name}: expected a schema error containing {want!r}, got {msgs or 'none'}"); bad += 1
    elif errors:
        print(f"FAIL  {name}:"); [print(f"        {m}") for m in msgs]; bad += 1
    else:
        print(f"PASS  {name}"); ok += 1
print(f"\nschema: {ok} passed, {bad} failed (schema {schema.get('$id')})")
sys.exit(1 if bad else 0)
