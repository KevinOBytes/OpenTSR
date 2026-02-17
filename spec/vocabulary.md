# OpenTSR Vocabulary

This document defines canonical namespaced vocabulary terms used by OpenTSR payloads.

## Namespaces

- `physical:sensor` for physical-world sensor measurements.

## `physical:sensor`

`physical:sensor` is a structured payload extension for cyber-physical correlation.

### Shape

```json
{
  "physical:sensor": {
    "sensor_id": "temp-3",
    "sensor_type": "temperature",
    "unit": "celsius",
    "value": 101.7,
    "location": "mixing-tank-a"
  }
}
```

### Field Semantics

- `sensor_id`: stable identifier for the physical sensor.
- `sensor_type`: measurement class (for example `temperature`, `pressure`, `vibration`).
- `unit`: measurement unit (for example `celsius`, `kpa`, `rpm`).
- `value`: numeric measurement value.
- `location`: optional physical placement descriptor.

## Extension Guidance

- Producers MAY add additional namespaced keys under `payload`.
- Extensions SHOULD avoid unqualified keys that conflict with base OpenTSR fields.
- Any new normative vocabulary terms MUST be proposed through the RFC process.
