# OpenTSR v1.0 Release Backlog

## 0. Program Controls
- [ ] Establish CI validation workflow in `.github/workflows/validate.yml`.
- [ ] Add reproducible local compliance command (`pytest --compliance-check` target).
- [ ] Define release criteria and sign-off checklist in `README.md`.
- [ ] Record architectural milestones in `MEMORY.md`.

## 1. Phase 1 - The Core Standard

### 1.1 Canonical Schema
- [x] Publish strict JSON-LD schema in `spec/schema.json`.
- [x] Enforce UUIDv7 format for `tsr_id`.
- [x] Enforce nanosecond epoch integer for `tsr_timestamp_ns`.
- [x] Enforce veracity range (`0.0` to `1.0`).
- [x] Enforce production signature requirement (`env=prod` requires `safety.digital_signature`).
- [x] Enforce LLM-origin agent identity requirement.
- [x] Enforce vector dimensions (`1024` or `1536`) and normalization semantics.
- [x] Enforce blob reference requirements (`blob_url` + `sha256_hash`) for externalized binaries.

### 1.2 Translator SDKs (High-Assurance References)
- [x] Create package metadata and runtime dependencies in `sdk/python/pyproject.toml`.
- [x] Implement strict Pydantic models in `sdk/python/opentsr/models.py`.
- [x] Auto-generate UUIDv7 `tsr_id` for every signal.
- [x] Auto-generate nanosecond timestamp for every signal.
- [x] Add schema-backed `validate()` method for emitter-side compliance.
- [x] Export public SDK interface in `sdk/python/opentsr/__init__.py`.
- [ ] Add usage documentation in `sdk/python/README.md`.
- [x] Scaffold TypeScript/Zod translator SDK in `sdk/typescript/`.
- [ ] Add TypeScript examples and parity tests against Python translator behavior.

### 1.3 Core Verification
- [x] Add `examples/verify_core.py` for canonical signal generation and validation.
- [ ] Add unit tests for happy-path and rejection-path schema cases.
- [ ] Add property tests for UUIDv7 ordering and timestamp monotonicity assumptions.

## 2. Phase 2 - The Ingest Engine

### 2.1 Ingest Gatekeeper
- [ ] Create deployment-agnostic ingest API skeleton.
- [ ] Validate inbound payloads against `spec/schema.json`.
- [ ] Return deterministic `400` responses on compliance failures.
- [ ] Implement payload hard-limit enforcement (5 MB).
- [ ] Add explicit request timeout and retry policy for downstream calls.

### 2.2 Storage and Routing
- [ ] Persist raw payload to cold object storage.
- [ ] Split metadata for relational/time-series indexing.
- [ ] Add ingestion idempotency keying by `tsr_id`.
- [ ] Emit structured audit logs for acceptance/rejection decisions.

### 2.3 Operational Safety
- [ ] Add environment-specific signature policy checks.
- [ ] Add Zero Trust authenticated administrative endpoints for replay/debug.
- [ ] Define retention lifecycle and object lock policy for forensic integrity.

## 3. Phase 3 - The Verification Layer

### 3.1 Signing
- [ ] Define signing profile and canonicalization strategy.
- [ ] Implement signature verification pipeline in portable ingest runtime.
- [ ] Add key rotation workflow and trust-store management.

### 3.2 Vector Assurance
- [ ] Implement embedding generation pipeline with pluggable provider adapters.
- [ ] Enforce dimensionality and normalization pre-index checks.
- [ ] Insert vectors into vector database index.
- [ ] Add drift checks for embedding model transitions.

### 3.3 Safety and Search
- [ ] Implement veracity-weighted retrieval filters for downstream consumers.
- [ ] Define incident response workflow for corrupted or unsigned production signals.
- [ ] Validate end-to-end semantic recall and precision against benchmark corpora.

## 4. Release Hardening
- [ ] Build threat model and abuse-case suite.
- [ ] Run performance/load test for edge ingestion throughput.
- [ ] Run backward compatibility checks for schema evolution policy.
- [ ] Publish v1.0 changelog and migration notes.
