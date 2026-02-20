# OpenTSR

[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-0366d6)](https://kevinobytes.github.io/OpenTSR/)

OpenTSR is a GitHub-native, docs-as-code standard and reference implementation for high-assurance AI telemetry. It defines a strict JSON schema plus semantics and profiles so teams can emit, validate, and govern evidence envelopes consistently across autonomous systems.

**Status:** Draft `v1.0.0-draft`
**Deployment Model:** Vendor-neutral and portable across cloud providers or local infrastructure.

## Documentation

- Docs site (GitHub Pages): [https://kevinobytes.github.io/OpenTSR/](https://kevinobytes.github.io/OpenTSR/)
- Spec source: [`spec/schema.json`](spec/schema.json), [`spec/SEMANTICS.md`](spec/SEMANTICS.md), [`spec/PROFILES.md`](spec/PROFILES.md), [`spec/vocabulary.md`](spec/vocabulary.md)
- Adapter Hub: [`adapters/`](adapters), [`docs/adapter-hub.md`](docs/adapter-hub.md)
- Governance and RFC process: [`docs/governance.md`](docs/governance.md)

## Repository Contents

1. **The Law**
   - `spec/schema.json`
   - `spec/SEMANTICS.md`
   - `spec/PROFILES.md`
2. **The Translators**
   - Python SDK (`sdk/python`) using Pydantic
   - TypeScript SDK (`sdk/typescript`) using Zod
3. **The Hub**
   - Community-contributed adapter manifests and examples under `adapters/`
   - Mapping guides in `spec/MAPPINGS_OCSF.md` and `spec/MAPPINGS_OTEL.md`
4. **Testing**
   - `pytest --compliance-check` for self-certification against protocol requirements

## Quickstart

### Validate an event

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e sdk/python pytest
python examples/verify_core.py
pytest --compliance-check
```

### Sign/verify events

```bash
python - <<'PY'
from opentsr import ActionIntent, Origin, Safety, TSRSignal

signal = TSRSignal(
    env="dev",
    origin=Origin(kind="llm_agent", source_id="agent-core", namespace="demo"),
    agent_id="agent://agent-core",
    action_intent=ActionIntent(action="evaluate", target="task://42"),
    payload={"event": "verification"},
    safety=Safety(veracity_score=0.7, hazard_flag=False),
)

signal.sign(key=b"replace-with-real-secret")
print(signal.verify_signature(key=b"replace-with-real-secret"))
PY
```

## Adoption

1. Emit events that conform to [`spec/schema.json`](spec/schema.json).
2. Validate before publish (CI and runtime).
3. Select an operating profile from [`spec/PROFILES.md`](spec/PROFILES.md).
4. Use `pytest --compliance-check` in CI before merges.
5. Record schema and semantics changes in [`CHANGELOG.md`](CHANGELOG.md).

## TARE Pivot: Universal Adapter API

OpenTSR treats proprietary vendor output as input to adapter translators, not as a protocol endpoint.

- Community and vendors contribute adapter manifests and examples under [`adapters/`](adapters).
- Lightweight SDK bridges (Pydantic/Zod/etc.) map device-specific payloads to OpenTSR JSON-LD.
- The protocol remains stable while adapters evolve independently.

## Governance / RFCs

OpenTSR uses a Discussions-first RFC model. Start with a Discussion for normative changes, then implement via pull request once a maintainer marks the RFC accepted.

- Governance guide: [`docs/governance.md`](docs/governance.md)
- RFC template: [`docs/RFC_TEMPLATE.md`](docs/RFC_TEMPLATE.md)

## Non-goals

- OpenTSR is not a replacement for full domain taxonomies like OCSF.
- OpenTSR is not a SIEM or observability backend.
- OpenTSR does not mandate a single cloud deployment topology.

## License

Licensed under Apache-2.0. See [`LICENSE`](LICENSE).
