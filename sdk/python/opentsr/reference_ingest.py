from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from .models import TSRSignal

JsonObject = Dict[str, object]


@dataclass(frozen=True)
class IngestResult:
    status_code: int
    message: str
    cold_path: Optional[str]
    hot_indexed: bool


def ingest_signal(
    payload: JsonObject,
    cold_store_dir: Path,
    hot_index_path: Optional[Path] = None,
    schema_path: Optional[Path] = None,
    verify_signatures: bool = False,
    signature_key: Optional[bytes] = None,
) -> IngestResult:
    """Reference ingest contract for OpenTSR.

    Returns 400 for invalid payloads to mirror the TARE ingestion behavior.
    Persists raw payload (cold path) and optionally appends vector metadata (hot path).
    """

    try:
        signal = TSRSignal.model_validate(payload)
        signal.validate(schema_path=schema_path)
    except Exception as exc:
        return IngestResult(status_code=400, message=f"invalid signal: {exc}", cold_path=None, hot_indexed=False)

    if verify_signatures:
        if signal.safety.digital_signature is None:
            return IngestResult(
                status_code=400,
                message="invalid signal: missing safety.digital_signature for verification",
                cold_path=None,
                hot_indexed=False,
            )
        if signature_key is None:
            return IngestResult(
                status_code=400,
                message="invalid signal: signature_key is required when verify_signatures=True",
                cold_path=None,
                hot_indexed=False,
            )
        if not signal.verify_signature(signature_key):
            return IngestResult(
                status_code=400,
                message="invalid signal: signature verification failed",
                cold_path=None,
                hot_indexed=False,
            )

    cold_store_dir.mkdir(parents=True, exist_ok=True)
    cold_path = cold_store_dir / f"{signal.tsr_id}.json"
    cold_path.write_text(
        json.dumps(signal.as_json_dict(), separators=(",", ":"), sort_keys=True),
        encoding="utf-8",
    )

    hot_indexed = False
    if signal.vector is not None:
        target_hot_index_path = hot_index_path if hot_index_path is not None else cold_store_dir / "hot_vectors.ndjson"
        target_hot_index_path.parent.mkdir(parents=True, exist_ok=True)
        vector_entry: JsonObject = {
            "tsr_id": signal.tsr_id,
            "tsr_timestamp_ns": signal.tsr_timestamp_ns,
            "env": signal.env,
            "vector_dim": len(signal.vector),
            "origin_kind": signal.origin.kind,
            "hazard_flag": signal.safety.hazard_flag,
        }
        with target_hot_index_path.open("a", encoding="utf-8") as hot_file:
            hot_file.write(json.dumps(vector_entry, separators=(",", ":"), sort_keys=True))
            hot_file.write("\n")
        hot_indexed = True

    return IngestResult(
        status_code=202,
        message="accepted",
        cold_path=str(cold_path),
        hot_indexed=hot_indexed,
    )


def ingest_signal_json(
    payload_json: str,
    cold_store_dir: Path,
    hot_index_path: Optional[Path] = None,
    schema_path: Optional[Path] = None,
    verify_signatures: bool = False,
    signature_key: Optional[bytes] = None,
) -> IngestResult:
    try:
        payload: object = json.loads(payload_json)
    except json.JSONDecodeError as exc:
        return IngestResult(status_code=400, message=f"invalid JSON: {exc}", cold_path=None, hot_indexed=False)

    if not isinstance(payload, dict):
        return IngestResult(status_code=400, message="invalid JSON: root must be an object", cold_path=None, hot_indexed=False)

    return ingest_signal(
        payload=payload,
        cold_store_dir=cold_store_dir,
        hot_index_path=hot_index_path,
        schema_path=schema_path,
        verify_signatures=verify_signatures,
        signature_key=signature_key,
    )
