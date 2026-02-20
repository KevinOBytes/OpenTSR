# Decision Log

## 2026-02-17

- Adopt GitHub-native docs-as-code (`/docs` on `main`) as the canonical public documentation surface.
- Adopt Discussions-first RFC governance for normative spec changes, with issues reserved for bugs/tasks.
- Extend core schema with `safety.hazard_flag`, `action_intent`, and `physical:sensor` vocabulary.
- Add executable compliance gate (`pytest --compliance-check`) and reference ingest contract with explicit `400` rejects.

## 2026-02-20

- Adopt the TARE pivot: OpenTSR becomes the universal translation API with a public Adapter Hub (`adapters/`) for community/vendor-maintained translators.
- Define adapter manifest and registry schemas, plus CI validation, to keep contributions deterministic and auditable.
