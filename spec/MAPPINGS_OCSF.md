# OpenTSR to OCSF Mapping (Draft)

This document captures non-normative field mapping guidance.

| OpenTSR Field | OCSF Concept | Notes |
| --- | --- | --- |
| `tsr_id` | `metadata.uid` | Preserve UUIDv7 ordering property where possible. |
| `tsr_timestamp_ns` | `time` | OCSF generally uses milliseconds; convert carefully. |
| `origin.kind` | `actor.type` | Map source class to actor taxonomy. |
| `origin.source_id` | `actor.uid` | Use stable service/device identifiers. |
| `safety.veracity_score` | extension field | No canonical OCSF equivalent; store as custom extension. |
| `vector` | extension field | Typically stored out-of-band in vector DB. |

## Notes

- OpenTSR focuses on interoperable safety envelopes rather than replacing full domain event taxonomies.
- Mapping losses can occur for nanosecond precision and embedding vectors.
