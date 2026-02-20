# Woehrsh RM Compound Microscope Adapter

This adapter maps Woehrsh RM compound microscope event payloads into OpenTSR JSON-LD.

## Mapping

- Capture metadata -> `payload` fields (`capture_mode`, `objective`, `magnification`)
- Device serial -> `origin.source_id`
- Image references -> `payload.blob_url` and `payload.sha256_hash`
- Confidence/trust signal -> `safety.veracity_score`

## Notes

- Image binaries are not embedded; only hash and object reference are stored.
- Optional vector embeddings can be generated downstream by runtime services.
