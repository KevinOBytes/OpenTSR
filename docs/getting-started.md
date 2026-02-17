# Getting Started

## Validate an Example Event

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e sdk/python
python examples/verify_core.py
```

## Run Compliance Checks

```bash
source .venv/bin/activate
python -m pip install pytest
pytest --compliance-check
```

## Sign and Verify a Signal

```bash
source .venv/bin/activate
python - <<'PY'
from opentsr import ActionIntent, Origin, Safety, TSRSignal

signal = TSRSignal(
    env="dev",
    origin=Origin(kind="llm_agent", source_id="sentinel-core", namespace="tareops"),
    agent_id="agent://sentinel-core",
    action_intent=ActionIntent(action="evaluate", target="task://demo"),
    payload={"event": "signed_example"},
    safety=Safety(veracity_score=0.8, hazard_flag=False),
)

signal.sign(key=b"replace-with-real-secret")
print("signature valid:", signal.verify_signature(key=b"replace-with-real-secret"))
PY
```

## Validate Raw JSON Against the Schema

```bash
python - <<'PY'
import json
from jsonschema import Draft202012Validator

with open('spec/schema.json', 'r', encoding='utf-8') as f:
    schema = json.load(f)

with open('examples/minimal_signal.json', 'r', encoding='utf-8') as f:
    instance = json.load(f)

Draft202012Validator(schema).validate(instance)
print('schema validation: PASS')
PY
```

## Next Steps

- Review semantic requirements in [`spec/SEMANTICS.md`](../spec/SEMANTICS.md).
- Select a deployment posture in [`spec/PROFILES.md`](../spec/PROFILES.md).
- Review namespaced terms in [`spec/vocabulary.md`](../spec/vocabulary.md).
- Read governance rules in [`governance.md`](governance.md).
