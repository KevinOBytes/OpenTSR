# Getting Started

## Validate an Example Event

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e sdk/python
python examples/verify_core.py
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
- Read governance rules in [`governance.md`](governance.md).
