# OpenTSR

OpenTSR is a standard plus reference implementation for AI telemetry evidence envelopes. It defines a strict JSON schema, semantic rules, and operating profiles so teams can exchange and validate high-assurance signals.

## Quick Links

- Schema: [`spec/schema.json`](../spec/schema.json)
- Semantics: [`spec/SEMANTICS.md`](../spec/SEMANTICS.md)
- Profiles: [`spec/PROFILES.md`](../spec/PROFILES.md)
- SDK: [`sdk/python`](../sdk/python)
- Examples: [`examples/`](../examples)

## How to Adopt

1. Validate emitted events against [`spec/schema.json`](../spec/schema.json).
2. Follow normative behavior in [`spec/SEMANTICS.md`](../spec/SEMANTICS.md).
3. Select an operating profile from [`spec/PROFILES.md`](../spec/PROFILES.md).
4. Keep implementation docs and changelog synchronized with spec changes.

## How to Propose Changes

1. Open an RFC Discussion using the template in [`docs/RFC_TEMPLATE.md`](RFC_TEMPLATE.md).
2. Build consensus in Discussion first for normative changes.
3. Open a PR that includes schema, semantics, and changelog updates.
4. Wait for maintainer decision and required approvals.
