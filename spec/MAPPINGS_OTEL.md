# OpenTSR to OpenTelemetry Mapping (Draft)

This document is non-normative guidance for interoperability.

| OpenTSR Field | OTel Attribute/Concept | Notes |
| --- | --- | --- |
| `tsr_id` | event attribute `opentsr.id` | Keep original value for cross-system correlation. |
| `tsr_timestamp_ns` | event timestamp | Native OTel time types can preserve precision. |
| `trace.trace_id` | `trace_id` | Use direct mapping when available. |
| `trace.span_id` | `span_id` | Use direct mapping when available. |
| `origin.*` | resource attributes | Prefix as `opentsr.origin.*`. |
| `safety.veracity_score` | attribute `opentsr.safety.veracity_score` | Useful for routing and policy checks. |

## Notes

- OpenTSR events can be emitted as logs or span events with attached attributes.
- Keep signatures and hashes intact to preserve evidence integrity.
