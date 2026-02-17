# Reference Ingest

OpenTSR includes a lightweight Python reference ingest contract in [`sdk/python/opentsr/ingest.py`](../sdk/python/opentsr/ingest.py).

## Contract

- Invalid JSON or invalid signals return `400`.
- Valid signals return `202`.
- Raw signal payload is persisted to a cold path.
- Vector metadata is appended to a hot index path when `vector` is present.

## Usage

```python
from pathlib import Path
from opentsr import ingest_signal_json

result = ingest_signal_json(
    payload_json='{"@context":"https://opentsr.org/context/v1","@type":"OpenTSRSignal"}',
    cold_store_dir=Path("./var/cold"),
)

print(result.status_code, result.message)
```
