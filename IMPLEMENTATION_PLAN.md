# OpenTSR Implementation Plan (v1.0 Track)

## Execution Principles
- Veracity before velocity: no implied dependencies, no schema shortcuts.
- Security by default: strict validation, explicit policy checks, fail closed.
- Deployment-agnostic protocol path: equivalent behavior across cloud and local runtimes.

## Phase 1: The Core Standard

### Objective
Establish a canonical, machine-verifiable signal format and a reference Python SDK that produces compliant payloads by construction.

### Deliverables
1. `spec/schema.json` (Draft 2020-12 JSON Schema with JSON-LD envelope).
2. `sdk/python/opentsr/models.py` (strict Pydantic models with invariant checks).
3. `sdk/python/opentsr/__init__.py` and `sdk/python/pyproject.toml`.
4. `examples/verify_core.py` proving generation + schema compliance.

### Design Decisions
1. UUIDv7 generator implemented in-SDK to avoid unverified third-party dependency.
2. Nanosecond timestamps generated from `time.time_ns()` and persisted as signed 64-bit-safe integer.
3. Compliance check uses JSON Schema validator against the canonical schema file.
4. `env=prod` triggers mandatory signature enforcement.
5. LLM-origin signals require `agent_id`.

### Exit Criteria
- A valid signal can be generated and serialized via SDK.
- Schema validation passes for compliant payloads and fails for policy violations.
- Example verification script runs successfully in local environment.

### Risks and Mitigations
- Risk: JSON-LD ambiguity in field naming.
  - Mitigation: lock required envelope fields (`@context`, `@type`) and reject extra top-level keys.
- Risk: vector normalization numerical tolerance.
  - Mitigation: enforce bounded epsilon in SDK (`abs(norm - 1.0)` threshold).

## Phase 2: The Ingest Engine

### Objective
Deploy an edge-native gatekeeper that accepts only compliant OpenTSR packets and stores them with forensic traceability.

### Deliverables
1. Reference ingest service contract and portability guidance.
2. Schema-validation middleware with deterministic error responses.
3. Cold object storage archival integration pattern.
4. Metadata persistence pattern for relational/time-series databases.

### Execution Strategy
1. Build validation-first ingest middleware.
2. Apply payload-size controls before downstream processing.
3. Persist raw signal to cold object storage with immutable keying by `tsr_id`.
4. Emit structured ingest logs with reason codes for rejects.

### Exit Criteria
- Non-compliant packets are rejected with reasoned 400 responses.
- Compliant packets are stored in cold object storage and metadata path is populated.
- Timeout and retry boundaries are explicit for all external calls.

## Phase 3: The Verification Layer

### Objective
Bind telemetry to cryptographic trust and semantic retrieval quality.

### Deliverables
1. Signature verification pipeline (high-assurance mode).
2. Embedding generation and vector database indexing flow.
3. Veracity-aware retrieval constraints for downstream analytics.

### Execution Strategy
1. Implement canonical payload signing/verification contract.
2. Integrate embedding provider path with pluggable runtime backends.
3. Enforce vector dimensionality and normalization prior to indexing.
4. Capture trust metadata for search-time filtering and audit.

### Exit Criteria
- Production packets without valid signatures are rejected.
- Vectors are indexed with enforced dimensional integrity.
- End-to-end replay shows auditability from emit to retrieval.

## Sequence and Governance
1. Complete Phase 1 before provisioning ingest runtime logic.
2. Update `ARCHITECTURE.md` and `BOUNDARY.md` on flow/boundary changes.
3. Log major decisions in `MEMORY.md` at each phase gate.
