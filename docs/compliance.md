---
layout: default
title: Compliance
---

# Compliance

OpenTSR compliance checks are executable via pytest.

## Run Compliance Suite

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e sdk/python pytest
pytest --compliance-check
```

## What Is Verified

- Schema conformance of all `examples/*.json`.
- UUIDv7, timestamp, payload-size, and vector constraints.
- `hazard_flag`, `action_intent`, and production signature requirements.
- Ingest contract behavior (`400` for invalid signals).
