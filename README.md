# OpenTSR

[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-0366d6)](https://<org-or-user>.github.io/OpenTSR/)

OpenTSR is a GitHub-native, docs-as-code standard and reference implementation for high-assurance AI telemetry. It defines a strict JSON schema plus semantics and profiles so teams can emit, validate, and govern evidence envelopes consistently across autonomous systems.

**Status:** Draft `v1.0.0-draft`

## Documentation

- Docs site (GitHub Pages): [https://<org-or-user>.github.io/OpenTSR/](https://<org-or-user>.github.io/OpenTSR/)
- Spec source: [`spec/schema.json`](spec/schema.json), [`spec/SEMANTICS.md`](spec/SEMANTICS.md), [`spec/PROFILES.md`](spec/PROFILES.md)
- Governance and RFC process: [`docs/governance.md`](docs/governance.md)

## Quickstart

### Validate an event

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e sdk/python
python examples/verify_core.py
```

### Sign/verify events

Signing and verification helpers are planned for a follow-up SDK release. Until then, use `safety.digital_signature` and `safety.signature_alg` fields per [`spec/SEMANTICS.md`](spec/SEMANTICS.md) and verify signatures in your platform boundary.

## Adoption

1. Emit events that conform to [`spec/schema.json`](spec/schema.json).
2. Validate before publish (CI and runtime).
3. Select an operating profile from [`spec/PROFILES.md`](spec/PROFILES.md).
4. Record schema and semantics changes in [`CHANGELOG.md`](CHANGELOG.md).

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
