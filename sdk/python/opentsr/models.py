from __future__ import annotations

import base64
import hashlib
import hmac
import json
import math
import secrets
import time
import warnings
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, cast
from uuid import UUID

from jsonschema import Draft202012Validator, FormatChecker
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

JsonObject = Dict[str, object]

MAX_INT64: int = 9_223_372_036_854_775_807
MAX_PAYLOAD_SOFT_BYTES: int = 1 * 1024 * 1024
MAX_PAYLOAD_HARD_BYTES: int = 5 * 1024 * 1024
UUID_V7_PATTERN: str = r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
SUPPORTED_SIGNATURE_ALGS: Tuple[str, ...] = ("hmac-sha256",)


def _generate_uuid7() -> str:
    unix_ms: int = time.time_ns() // 1_000_000
    if unix_ms < 0 or unix_ms >= (1 << 48):
        raise ValueError("uuidv7 timestamp is out of range")

    rand_a: int = secrets.randbits(12)
    rand_b: int = secrets.randbits(62)
    uuid_int: int = (unix_ms << 80) | (0x7 << 76) | (rand_a << 64) | (0b10 << 62) | rand_b
    return str(UUID(int=uuid_int))


def _default_timestamp_ns() -> int:
    return time.time_ns()


def _default_schema_path() -> Path:
    return Path(__file__).resolve().parents[3] / "spec" / "schema.json"


def _canonical_json_bytes(payload: object) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


@lru_cache(maxsize=8)
def _load_schema(schema_path: str) -> JsonObject:
    with Path(schema_path).open("r", encoding="utf-8") as schema_file:
        raw_schema: object = json.load(schema_file)
    if not isinstance(raw_schema, dict):
        raise ValueError(f"Schema must be a JSON object: {schema_path}")
    return cast(JsonObject, raw_schema)


class Origin(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    kind: Literal["llm_agent", "sensor", "service", "human_operator", "simulator"]
    source_id: str = Field(min_length=1)
    namespace: Optional[str] = Field(default=None, min_length=1)
    device_id: Optional[str] = Field(default=None, min_length=1)
    software_version: Optional[str] = Field(default=None, min_length=1)
    region: Optional[str] = Field(default=None, min_length=1)


class Safety(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    veracity_score: float = Field(ge=0.0, le=1.0)
    hazard_flag: bool = Field(default=False)
    digital_signature: Optional[str] = Field(default=None, min_length=1)
    signature_alg: Optional[str] = Field(default=None, min_length=1)


class ActionIntent(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    action: str = Field(min_length=1)
    target: str = Field(min_length=1)
    reason: Optional[str] = Field(default=None, min_length=1)
    requested_by: Optional[str] = Field(default=None, min_length=1)


class Trace(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    trace_id: Optional[str] = Field(default=None, min_length=1)
    span_id: Optional[str] = Field(default=None, min_length=1)
    parent_span_id: Optional[str] = Field(default=None, min_length=1)


class ResourceRef(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    blob_url: str = Field(min_length=1)
    sha256_hash: str = Field(min_length=64, max_length=64)
    content_type: Optional[str] = Field(default=None, min_length=1)
    size_bytes: Optional[int] = Field(default=None, ge=0)

    @field_validator("sha256_hash")
    @classmethod
    def validate_sha256_hash(cls, value: str) -> str:
        if any(character not in "0123456789abcdefABCDEF" for character in value):
            raise ValueError("sha256_hash must be a 64-character hex digest")
        return value


class TSRSignal(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, populate_by_name=True)

    context: str = Field(default="https://opentsr.org/context/v1", alias="@context")
    signal_type: str = Field(default="OpenTSRSignal", alias="@type")
    schema_version: Literal["1.0.0-draft"] = Field(default="1.0.0-draft")
    tsr_id: str = Field(default_factory=_generate_uuid7, pattern=UUID_V7_PATTERN)
    tsr_timestamp_ns: int = Field(default_factory=_default_timestamp_ns, ge=0, le=MAX_INT64)
    env: Literal["dev", "staging", "prod"] = Field(default="dev")
    origin: Origin
    payload: JsonObject
    safety: Safety
    agent_id: Optional[str] = Field(default=None, min_length=1)
    action_intent: Optional[ActionIntent] = None
    vector: Optional[List[float]] = None
    tags: Optional[List[str]] = None
    trace: Optional[Trace] = None
    resources: Optional[List[ResourceRef]] = None

    @field_validator("tsr_id")
    @classmethod
    def validate_tsr_id(cls, value: str) -> str:
        try:
            parsed = UUID(value)
        except ValueError as exc:
            raise ValueError("tsr_id must be a valid UUID") from exc
        if parsed.version != 7:
            raise ValueError("tsr_id must be UUIDv7")
        return value

    @field_validator("payload")
    @classmethod
    def validate_payload(cls, payload: JsonObject) -> JsonObject:
        serialized: bytes = _canonical_json_bytes(payload)
        if len(serialized) > MAX_PAYLOAD_SOFT_BYTES:
            warnings.warn("payload exceeds 1MB soft limit", RuntimeWarning, stacklevel=2)
        if len(serialized) > MAX_PAYLOAD_HARD_BYTES:
            raise ValueError("payload exceeds 5MB hard limit")
        if "blob_url" in payload and "sha256_hash" not in payload:
            raise ValueError("payload.blob_url requires payload.sha256_hash")
        sha256_hash: Optional[object] = payload.get("sha256_hash")
        if sha256_hash is not None:
            if not isinstance(sha256_hash, str):
                raise ValueError("payload.sha256_hash must be a string")
            if len(sha256_hash) != 64 or any(character not in "0123456789abcdefABCDEF" for character in sha256_hash):
                raise ValueError("payload.sha256_hash must be a 64-character hex digest")
        return payload

    @field_validator("vector")
    @classmethod
    def validate_vector(cls, vector: Optional[List[float]]) -> Optional[List[float]]:
        if vector is None:
            return None
        length: int = len(vector)
        if length not in (1024, 1536):
            raise ValueError("vector length must be exactly 1024 or 1536")

        l2_norm: float = math.sqrt(sum(component * component for component in vector))
        if not math.isfinite(l2_norm) or l2_norm == 0.0:
            raise ValueError("vector norm must be finite and non-zero")
        if abs(l2_norm - 1.0) > 1e-3:
            raise ValueError("vector must be L2-normalized (norm ~= 1.0)")
        return vector

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: Optional[List[str]]) -> Optional[List[str]]:
        if tags is None:
            return None
        if len(tags) > 64:
            raise ValueError("tags must contain at most 64 values")
        if len(set(tags)) != len(tags):
            raise ValueError("tags must contain unique values")
        if any(len(tag) == 0 for tag in tags):
            raise ValueError("tags cannot contain empty strings")
        return tags

    @model_validator(mode="after")
    def validate_cross_field_constraints(self) -> "TSRSignal":
        if self.origin.kind == "llm_agent" and not self.agent_id:
            raise ValueError("agent_id is required when origin.kind is llm_agent")
        if self.origin.kind == "llm_agent" and self.action_intent is None:
            raise ValueError("action_intent is required when origin.kind is llm_agent")
        if self.env == "prod" and not self.safety.digital_signature:
            raise ValueError("safety.digital_signature is required when env=prod")
        if self.safety.digital_signature and not self.safety.signature_alg:
            raise ValueError("safety.signature_alg is required when safety.digital_signature is present")
        if self.safety.signature_alg and not self.safety.digital_signature:
            raise ValueError("safety.digital_signature is required when safety.signature_alg is present")
        return self

    def _signable_dict(self) -> JsonObject:
        instance: JsonObject = self.as_json_dict()
        safety_value: object = instance.get("safety")
        if not isinstance(safety_value, dict):
            raise ValueError("safety must be an object")
        safety_obj: JsonObject = cast(JsonObject, dict(safety_value))
        safety_obj.pop("digital_signature", None)
        instance["safety"] = safety_obj
        return instance

    def sign(self, key: bytes, signature_alg: str = "hmac-sha256") -> str:
        if signature_alg not in SUPPORTED_SIGNATURE_ALGS:
            supported: str = ", ".join(SUPPORTED_SIGNATURE_ALGS)
            raise ValueError(f"unsupported signature algorithm: {signature_alg}. Supported: {supported}")

        self.safety.signature_alg = signature_alg
        signable_bytes: bytes = _canonical_json_bytes(self._signable_dict())
        if signature_alg == "hmac-sha256":
            signature_bytes: bytes = hmac.new(key, signable_bytes, hashlib.sha256).digest()
            signature: str = base64.b64encode(signature_bytes).decode("ascii")
            self.safety.digital_signature = signature
            return signature

        raise ValueError(f"unsupported signature algorithm: {signature_alg}")

    def verify_signature(self, key: bytes) -> bool:
        if self.safety.digital_signature is None or self.safety.signature_alg is None:
            return False
        if self.safety.signature_alg not in SUPPORTED_SIGNATURE_ALGS:
            return False

        signable_bytes: bytes = _canonical_json_bytes(self._signable_dict())
        expected_signature: str = base64.b64encode(
            hmac.new(key, signable_bytes, hashlib.sha256).digest()
        ).decode("ascii")
        return hmac.compare_digest(expected_signature, self.safety.digital_signature)

    def as_json_dict(self) -> JsonObject:
        return cast(JsonObject, self.model_dump(mode="json", by_alias=True, exclude_none=True))

    def validate(self, schema_path: Optional[Path] = None) -> bool:
        resolved_schema_path: Path = schema_path if schema_path is not None else _default_schema_path()
        schema: JsonObject = _load_schema(str(resolved_schema_path))
        validator = Draft202012Validator(schema=schema, format_checker=FormatChecker())
        instance: JsonObject = self.as_json_dict()
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
        if errors:
            first_error = errors[0]
            error_path: str = ".".join(str(part) for part in first_error.absolute_path) or "<root>"
            raise ValueError(f"OpenTSR schema validation failed at {error_path}: {first_error.message}")
        return True
