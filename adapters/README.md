# OpenTSR Adapter Hub

OpenTSR Adapter Hub is the public translation layer that turns proprietary vendor/device output into compliant OpenTSR JSON-LD.

This is where community maintainers and vendors publish lightweight adapters (for example Pydantic or Zod translators) without exposing private runtime infrastructure.

## Objective

- Make OpenTSR the universal API contract.
- Standardize adapter metadata and validation.
- Allow independent verification of adapter compliance.

## Directory Layout

Each adapter lives in its own folder:

```text
adapters/
  <adapter-id>/
    manifest.json
    README.md
    examples/
```

Optional implementation code can live in:

```text
adapters/<adapter-id>/sdk/python/
adapters/<adapter-id>/sdk/typescript/
```

## Adapter ID Convention

Use lowercase kebab-case:

- `vendor-device`
- `vendor-device-protocol`

Examples:

- `woehrsh-rm-compound-microscope`
- `generic-ph-meter`

## Required Files

1. `manifest.json` that validates against `adapters/manifest.schema.json`.
2. `README.md` describing source formats, mapping strategy, and limitations.
3. At least one example source payload and one OpenTSR output payload.

## Contribution Rules

- No secrets, credentials, or customer data.
- No closed binaries or opaque blobs.
- All payload examples must be synthetic or sanitized.
- Adapter output must validate against `spec/schema.json`.
- Adapter manifests must be registered in `adapters/registry.json`.

## Validation Contract

CI validates:

- `adapters/registry.json` against `adapters/registry.schema.json`.
- Every `manifest.json` against `adapters/manifest.schema.json`.
- Registry entries point to valid manifest paths.
- Adapter IDs are unique and consistent between registry and manifest.
