# OpenTSR Semantics

`spec/schema.json` defines structure. This document defines normative meaning.

## Normative Keywords

The key words "MUST", "MUST NOT", "SHOULD", and "MAY" are to be interpreted as described in RFC 2119.

## Envelope Identity

- `@context` MUST be `https://opentsr.org/context/v1`.
- `@type` MUST be `OpenTSRSignal`.
- `schema_version` MUST match the schema line used by the producer.

## Event Identity and Time

- `tsr_id` MUST be UUIDv7.
- `tsr_timestamp_ns` MUST be Unix epoch nanoseconds in signed 64-bit range.
- Producers SHOULD use stable clock sources and monotonic ordering when batching.

## Environment

- `env` identifies deployment context and MUST be one of `dev`, `staging`, `prod`.
- `prod` events MUST include `safety.digital_signature` and `safety.signature_alg`.

## Origin and Attribution

- `origin.kind` describes source class (`llm_agent`, `sensor`, `service`, `human_operator`, `simulator`).
- `origin.source_id` MUST uniquely identify the source within its namespace.
- `agent_id` MUST be present when `origin.kind = llm_agent`.

## Payload and External Blobs

- `payload` contains domain-specific content.
- Binary artifacts MUST NOT be embedded directly when payload size is large.
- If `payload.blob_url` is present, `payload.sha256_hash` MUST also be present.

## Safety and Veracity

- `safety.veracity_score` MUST be between `0.0` and `1.0`.
- `safety.digital_signature` and `safety.signature_alg` MUST be provided together.
- Consumers MAY set policy thresholds for acceptable veracity.

## Embeddings

- `vector` MAY be omitted.
- If present, vector length MUST be exactly `1024` or `1536`.
- Producers SHOULD emit L2-normalized vectors for cosine-similarity compatibility.

## Tags and Traceability

- `tags` SHOULD be used for coarse filtering, not domain payload encoding.
- `trace` SHOULD connect OpenTSR events to external traces/spans where available.
- `resources` SHOULD reference immutable blobs using URL + SHA-256 digest.
