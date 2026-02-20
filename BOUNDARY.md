# BOUNDARY.md - Public Protocol vs Private Runtime

## Purpose
Define an explicit boundary between:

- **Public repo (`OpenTSR`)**: protocol authority and conformance surface.
- **Private repo(s)**: production runtime and operations implementation.

This prevents drift, protects sensitive details, and keeps OpenTSR credible as an open standard.

## Repository Roles

### Public OpenTSR Repo (Authoritative, Open)
Owns all **interoperability artifacts**:

- `spec/schema.json`
- `spec/SEMANTICS.md`
- `spec/PROFILES.md`
- `spec/vocabulary.md`
- `adapters/` hub manifests, registry, and adapter examples
- `examples/` conformance payloads
- `tests/` compliance and conformance tests
- `sdk/python/` reference SDK and ingest contract
- Public governance and docs (`docs/`, `README.md`, `CHANGELOG.md`)

### Private Backend Repo (Implementation, Restricted)
Owns all **deployment-specific and sensitive implementation**:

- Runtime service code and environment wiring
- Infrastructure-as-code deployment configuration
- Secrets, key material, signing key management, rotation automation
- Production observability, alerting, SLOs, incident workflows
- Internal runbooks and customer/environment-specific adapters

## Decision Rule (What Goes Where)
If a change affects **wire compatibility** (what producers emit or consumers accept), it belongs in the **public repo first**.

If a change affects **only runtime behavior or operations** without changing protocol compatibility, it belongs in the **private repo**.

## Quick Classification Matrix

1. Field added/removed/renamed in signal packet: **Public**
2. Validation rule changed (`required`, type, constraints): **Public**
3. Semantics/profile interpretation changed: **Public**
4. New conformance test vectors: **Public**
5. Worker retry/backoff tuning: **Private**
6. Storage retention policy implementation details: **Private**
7. Secret handling, key vault integration, KMS configuration: **Private**
8. Internal dashboard queries and ops automation: **Private**

## Data and Security Boundary

### Never Commit to Public Repo
- Secrets, credentials, tokens, private keys
- Internal service endpoints or tenant identifiers
- Customer or production telemetry payloads
- Incident details containing sensitive operational context

### Allowed in Public Repo
- Synthetic/non-sensitive examples
- Protocol-level signing requirements and algorithm identifiers
- Security policy and disclosure process (high-level)

## Change Flow

1. **Protocol-impacting change proposed** in public RFC/issue process.
2. Public repo merges schema/semantics/tests/docs updates.
3. Private repo implements runtime changes to conform to updated public contract.
4. Private runtime validates against published conformance suite before release.

## Contract for Runtime Teams

Private services must treat the public repo as source of truth for:

- Signal shape and required fields
- Normative semantics
- Compliance test expectations

Any private behavior that diverges from public conformance expectations must be treated as a defect.

## Release Synchronization

For every protocol-affecting release:

1. Tag public release (for example `v1.0.0-draft`).
2. Pin private repo dependency/compatibility target to that tag.
3. Run private conformance gate against the tagged public schema/tests.
4. Record compatibility status in private release notes.

## Ownership

- **Public repo maintainers**: protocol governance and conformance integrity.
- **Private repo maintainers**: runtime reliability, security, and operational excellence.

Both sides are required to coordinate on breaking changes before merge.
