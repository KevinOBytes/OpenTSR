# Decision Log

## 2026-02-17

- Adopt GitHub-native docs-as-code (`/docs` on `main`) as the canonical public documentation surface.
- Adopt Discussions-first RFC governance for normative spec changes, with issues reserved for bugs/tasks.
- Extend core schema with `safety.hazard_flag`, `action_intent`, and `physical:sensor` vocabulary.
- Add executable compliance gate (`pytest --compliance-check`) and reference ingest contract with explicit `400` rejects.
