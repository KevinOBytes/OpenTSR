# OpenTSR Profiles

Profiles define operational expectations on top of core schema validity.

## Core Profile

Intended for local development and integration tests.

- Required: all base schema required fields.
- Recommended: include `tags` and `trace` for observability.
- Signature: optional unless `env=prod`.

## High-Assurance Profile

Intended for regulated or safety-critical workloads.

- Required: all base fields.
- Required: `env=prod` with signature metadata.
- Required: stable producer identity (`origin.namespace`, `origin.software_version`).
- Recommended: include `resources` with digest for evidence artifacts.

## Edge Telemetry Profile

Intended for constrained sensor and edge gateways.

- Required: base schema required fields.
- Optional: omit `vector` at edge and enrich downstream.
- Required when externalizing payload blobs: include `payload.blob_url` + `payload.sha256_hash`.

## Profile Selection Guidance

- Start with **Core** in early adoption.
- Move to **High-Assurance** when controls, signing, and retention policy are in place.
- Use **Edge Telemetry** for bandwidth-constrained emitters with later enrichment.
