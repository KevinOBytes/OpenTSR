# ARCHITECTURE.md - OpenTSR System Design

## Overview
OpenTSR is a deployment-agnostic signal normalization and ingestion standard. The architecture consists of a public Adapter Hub, language SDK translators, and a portable ingest pattern that can run on any cloud or local infrastructure.

## System Diagram
```mermaid
graph TD
    A["Vendor Device / Agent Output"] -->|"Proprietary Payload"| B["Adapter SDK (Community/Vendor)"]
    B -->|"Mapped OpenTSR JSON-LD"| C["OpenTSR SDK (Pydantic / Zod)"]
    C -->|"Normalize & Sign"| D{"Protocol Validation"}
    D -->|"Invalid"| E["Reject / Error Log"]
    D -->|"Valid JSON-LD"| F["Ingest API Service"]

    subgraph "Portable Runtime (AWS / Azure / GCP / On-Prem / Local)"
    F -->|"1. Archive Raw"| G[("Cold Object Storage")]
    F -->|"2. Generate Embedding"| H["Embedding Service"]
    H -->|"3. Index Vector"| I[("Vector Database")]
    F -->|"4. Store Metadata"| J[("Relational / Time-Series DB")]
    end

    I -->|"Semantic Search"| K["Dashboards / Agents"]
    J -->|"Analytics"| K
```

## Component Definitions

1. Adapter Hub (`adapters/`)
Role: Public registry for vendor/community translators that map proprietary outputs into OpenTSR JSON-LD.

2. Translators (`sdk/`)
Role: Language SDKs that generate and validate compliant OpenTSR signals.

Current reference translators:
- Python (`sdk/python`) using Pydantic.
- TypeScript (`sdk/typescript`) using Zod.

3. Reference Ingest Stub
Role: Local contract test stub for vendors and contributors.

Reference implementation:
- `sdk/python/opentsr/reference_ingest.py` provides a local ingest contract used in tests.
- Invalid payloads return `400` style results.
- Valid payloads are persisted to cold storage and vector metadata is appended to a hot index.

4. Storage Roles
- Cold Object Storage: full raw JSON signal payload.
- Vector Database: embedding index for semantic retrieval.
- Relational/Time-Series DB: query metadata (time, origin, safety indicators).

---
