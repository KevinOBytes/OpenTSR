from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
SDK_PYTHON_DIR: Path = REPO_ROOT / "sdk" / "python"
if str(SDK_PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(SDK_PYTHON_DIR))

from opentsr import Origin, Safety, TSRSignal


def main() -> None:
    signal = TSRSignal(
        env="dev",
        origin=Origin(kind="llm_agent", source_id="sentinel-core", namespace="tareops"),
        agent_id="agent://sentinel-core",
        payload={
            "event": "verification_pass",
            "detail": "Phase 1 core schema validation",
            "blob_url": "https://r2.example.com/tare/signals/packet-0001.json",
            "sha256_hash": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        },
        safety=Safety(veracity_score=0.5),
        vector=[1.0] + [0.0] * 1023
    )

    signal.validate()
    serialized = json.dumps(signal.as_json_dict(), indent=2, sort_keys=True)
    print("OpenTSR core verification: PASS")
    print(serialized)


if __name__ == "__main__":
    main()
