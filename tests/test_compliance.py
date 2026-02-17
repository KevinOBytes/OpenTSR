from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from opentsr import ActionIntent, Origin, Safety, TSRSignal, ingest_signal, ingest_signal_json

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "spec" / "schema.json"


def _schema_validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema=schema, format_checker=FormatChecker())


@pytest.mark.compliance
def test_all_json_examples_validate_against_schema() -> None:
    validator = _schema_validator()
    for example_path in sorted((REPO_ROOT / "examples").glob("*.json")):
        payload = json.loads(example_path.read_text(encoding="utf-8"))
        validator.validate(payload)


@pytest.mark.compliance
def test_llm_agent_requires_action_intent() -> None:
    with pytest.raises(ValueError, match="action_intent is required"):
        TSRSignal(
            env="dev",
            origin=Origin(kind="llm_agent", source_id="agent-ops", namespace="test"),
            agent_id="agent://agent-ops",
            payload={"event": "task"},
            safety=Safety(veracity_score=0.9, hazard_flag=False),
        )


@pytest.mark.compliance
def test_payload_soft_limit_warns_and_hard_limit_fails() -> None:
    soft_payload = {"event": "soft-limit", "blob": "x" * (1_048_576 + 128)}

    with pytest.warns(RuntimeWarning, match="1MB soft limit"):
        TSRSignal(
            env="dev",
            origin=Origin(kind="service", source_id="svc-a", namespace="test"),
            payload=soft_payload,
            safety=Safety(veracity_score=0.6, hazard_flag=False),
        )

    hard_payload = {"event": "hard-limit", "blob": "x" * (5 * 1024 * 1024 + 1)}
    with pytest.raises(ValueError, match="5MB hard limit"):
        TSRSignal(
            env="dev",
            origin=Origin(kind="service", source_id="svc-a", namespace="test"),
            payload=hard_payload,
            safety=Safety(veracity_score=0.6, hazard_flag=False),
        )


@pytest.mark.compliance
def test_hmac_sign_and_verify_round_trip() -> None:
    signal = TSRSignal(
        env="staging",
        origin=Origin(kind="llm_agent", source_id="planner", namespace="test"),
        agent_id="agent://planner",
        action_intent=ActionIntent(action="dispatch", target="task://123", reason="policy hit"),
        payload={"event": "dispatch", "task_id": "123"},
        safety=Safety(veracity_score=0.8, hazard_flag=False),
    )

    signature = signal.sign(key=b"example-signing-key")
    assert signature
    assert signal.verify_signature(key=b"example-signing-key") is True
    assert signal.verify_signature(key=b"wrong-key") is False


@pytest.mark.compliance
def test_ingest_contract_returns_400_and_202(tmp_path: Path) -> None:
    invalid_result = ingest_signal_json(
        payload_json="{",
        cold_store_dir=tmp_path / "cold",
    )
    assert invalid_result.status_code == 400

    signal = TSRSignal(
        env="dev",
        origin=Origin(kind="llm_agent", source_id="planner", namespace="test"),
        agent_id="agent://planner",
        action_intent=ActionIntent(action="monitor", target="asset://line-1"),
        payload={"event": "monitor", "blob_url": "https://example.com/blob", "sha256_hash": "0" * 64},
        safety=Safety(veracity_score=0.91, hazard_flag=True),
        vector=[1.0] + [0.0] * 1023,
    )
    signal.sign(key=b"verify-me")

    valid_result = ingest_signal(
        payload=signal.as_json_dict(),
        cold_store_dir=tmp_path / "cold",
        verify_signatures=True,
        signature_key=b"verify-me",
    )
    assert valid_result.status_code == 202
    assert valid_result.cold_path is not None
    assert valid_result.hot_indexed is True
