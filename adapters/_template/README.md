# Adapter Template

Use this folder as a starting point for new adapter submissions.

## Required

1. Copy this folder to `adapters/<adapter-id>/`.
2. Update `manifest.json` with real metadata.
3. Add source and translated OpenTSR examples.
4. Add adapter entry to `adapters/registry.json`.

## Validation

Your adapter must pass:

- `manifest.json` validation against `adapters/manifest.schema.json`
- Registry validation in CI
- OpenTSR schema validation for translated outputs
