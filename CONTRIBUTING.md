# Contributing to OpenTSR

Thanks for contributing to OpenTSR.

## Before You Start

- Read [`docs/governance.md`](docs/governance.md).
- Review the spec source in [`spec/`](spec).
- Keep pull requests focused and small when possible.

## Discussions vs Issues

- Use **GitHub Discussions (RFC category)** for proposed normative changes to schema semantics, profiles, and governance.
- Use **GitHub Issues** for bugs, tasks, editorial fixes, and implementation work.
- Use **Security Advisories** for vulnerability reports. Do not open public issues for active security vulnerabilities.

## Versioning and Breaking Changes

OpenTSR follows a SemVer-like policy for the schema and normative docs.

- `MAJOR`: breaking schema/semantic changes.
- `MINOR`: backward-compatible additions.
- `PATCH`: clarifications, typo fixes, non-normative tooling/documentation updates.

A change is considered **breaking** if it does one or more of the following:

- Removes or renames an existing field.
- Changes field type or constraints such that previously valid events become invalid.
- Changes normative semantics in a way that alters interoperability expectations.

## Required Artifacts for Schema Changes

Every PR that changes schema behavior must include:

- `spec/schema.json` update.
- `spec/SEMANTICS.md` update.
- `CHANGELOG.md` entry.
- Updated `examples/` payloads if behavior changes.

## Pull Request Checklist

- [ ] Tests pass locally.
- [ ] Schema validation workflow passes.
- [ ] Docs updated for user-visible behavior.
- [ ] `CHANGELOG.md` updated for spec or behavior changes.
- [ ] Breaking changes include migration notes.

## Local Validation

```bash
python -m pip install -e sdk/python
python examples/verify_core.py
python -m json.tool spec/schema.json > /dev/null
```
