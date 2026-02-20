# Generic pH Meter Adapter

This adapter maps generic pH meter exports and serial readings into OpenTSR JSON-LD.

## Mapping

- Input value -> `payload.physical:sensor.value`
- Unit -> `payload.physical:sensor.unit`
- Device ID -> `origin.source_id` and `payload.physical:sensor.sensor_id`
- Timestamp -> `tsr_timestamp_ns`

## Notes

- Intended as a baseline reference adapter.
- Constrained to OpenTSR `core` profile.
