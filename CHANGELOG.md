# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows SemVer-like versioning for schema and reference implementation artifacts.

## [Unreleased]

### Added

- GitHub Pages docs site scaffold under `docs/` with navigation and onboarding guides.
- Discussions-first governance documentation and RFC templates.
- OSS hygiene files: `CONTRIBUTING.md`, `SECURITY.md`, `CODEOWNERS`, issue/PR templates.
- CI workflows for schema/example validation and lightweight docs linting.
- Valid example event payloads in `examples/` for schema conformance checks.
- Physical telemetry vocabulary in `spec/vocabulary.md` with `physical:sensor` term.
- Compliance test suite runnable via `pytest --compliance-check`.
- Reference ingest contract with `400` reject semantics and split hot/cold persistence behavior.
- Adapter Hub scaffolding (`adapters/`) with manifest and registry schemas.
- Adapter registry validation integrated into schema CI workflow.

### Changed

- Repository README upgraded to standard + reference implementation positioning.
- Schema and SDK now include `safety.hazard_flag` and `action_intent`.
- SDK now supports HMAC-SHA256 sign/verify helpers and 1MB soft payload limit warnings.
- Architecture and docs now model OpenTSR as universal API with vendor/community adapter contribution path.
