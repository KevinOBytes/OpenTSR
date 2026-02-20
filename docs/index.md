---
layout: default
title: OpenTSR
---

# OpenTSR

OpenTSR is a standard plus reference implementation for AI telemetry evidence envelopes. It defines a strict JSON schema, semantic rules, and operating profiles so teams can exchange and validate high-assurance signals.

## Quick Links

- Schema: [`spec/schema.json`](https://github.com/KevinOBytes/OpenTSR/blob/main/spec/schema.json)
- Semantics: [`spec/SEMANTICS.md`](https://github.com/KevinOBytes/OpenTSR/blob/main/spec/SEMANTICS.md)
- Profiles: [`spec/PROFILES.md`](https://github.com/KevinOBytes/OpenTSR/blob/main/spec/PROFILES.md)
- Vocabulary: [`spec/vocabulary.md`](https://github.com/KevinOBytes/OpenTSR/blob/main/spec/vocabulary.md)
- Python SDK: [`sdk/python`](https://github.com/KevinOBytes/OpenTSR/tree/main/sdk/python)
- TypeScript SDK: [`sdk/typescript`](https://github.com/KevinOBytes/OpenTSR/tree/main/sdk/typescript)
- Adapter Hub: [`adapter-hub.md`](adapter-hub.md)
- Examples: [`examples/`](https://github.com/KevinOBytes/OpenTSR/tree/main/examples)
- Compliance guide: [`compliance.md`](compliance.md)
- Reference ingest: [`reference-ingest.md`](reference-ingest.md)

## How to Adopt

1. Validate emitted events against [`spec/schema.json`](https://github.com/KevinOBytes/OpenTSR/blob/main/spec/schema.json).
2. Follow normative behavior in [`spec/SEMANTICS.md`](https://github.com/KevinOBytes/OpenTSR/blob/main/spec/SEMANTICS.md).
3. Select an operating profile from [`spec/PROFILES.md`](https://github.com/KevinOBytes/OpenTSR/blob/main/spec/PROFILES.md).
4. Keep implementation docs and changelog synchronized with spec changes.

## How to Propose Changes

1. Open an RFC Discussion using the template in [`docs/RFC_TEMPLATE.md`](RFC_TEMPLATE.md).
2. Build consensus in Discussion first for normative changes.
3. Open a PR that includes schema, semantics, and changelog updates.
4. Wait for maintainer decision and required approvals.
