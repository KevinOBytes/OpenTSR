# OpenTSR Python SDK

Reference Python SDK for producing, validating, signing, and ingesting OpenTSR signals.

## Install

```bash
python -m pip install -e .
```

## Example

```python
from opentsr import ActionIntent, Origin, Safety, TSRSignal

signal = TSRSignal(
    env="dev",
    origin=Origin(kind="llm_agent", source_id="agent-core", namespace="demo"),
    agent_id="agent://agent-core",
    action_intent=ActionIntent(action="evaluate", target="task://42"),
    payload={"event": "evaluation_complete"},
    safety=Safety(veracity_score=0.8, hazard_flag=False),
)

signal.validate()
signal.sign(key=b"replace-with-secure-key")
assert signal.verify_signature(key=b"replace-with-secure-key")
```
