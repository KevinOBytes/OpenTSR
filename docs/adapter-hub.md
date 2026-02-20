---
layout: default
title: Adapter Hub
---

# Adapter Hub

OpenTSR Adapter Hub is the public contribution surface for translating proprietary vendor/device output into OpenTSR JSON-LD.

## Why This Exists

- Vendor payload formats are fragmented.
- OpenTSR defines a stable interoperability contract.
- Adapters let community and vendors map legacy/proprietary data into that contract.

## What Gets Contributed

- Adapter manifests (`adapters/<adapter-id>/manifest.json`)
- Source-to-OpenTSR examples
- Lightweight translator implementations (Pydantic/Zod/etc.)

## Governance Boundary

- Protocol compatibility lives in public OpenTSR spec artifacts.
- Runtime deployment and operational internals stay in private implementation repos.

See:

- [`adapters/README.md`](https://github.com/KevinOBytes/OpenTSR/blob/main/adapters/README.md)
- [`adapters/manifest.schema.json`](https://github.com/KevinOBytes/OpenTSR/blob/main/adapters/manifest.schema.json)
- [`adapters/registry.json`](https://github.com/KevinOBytes/OpenTSR/blob/main/adapters/registry.json)
- [`BOUNDARY.md`](https://github.com/KevinOBytes/OpenTSR/blob/main/BOUNDARY.md)
