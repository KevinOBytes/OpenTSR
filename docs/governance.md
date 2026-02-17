# Governance and RFC Process

OpenTSR uses a Discussions-first workflow for specification governance.

## When to Use Discussions vs Issues

- Use **Discussions (RFC)** for normative schema, semantics, profile, and governance proposals.
- Use **Issues** for bugs, implementation tasks, docs fixes, and maintenance work.
- Use **Security Advisories** for vulnerabilities.

## RFC Lifecycle

1. **Draft:** Open Discussion with RFC template.
2. **Review:** Collect feedback and resolve open design questions.
3. **Decision:** Maintainers mark proposal as Accepted, Rejected, or Needs Revision.
4. **Implementation:** Accepted RFC is implemented by pull request.

## Maintainer Decision Process

- Non-breaking RFCs require at least one maintainer approval.
- Breaking RFCs require at least two maintainer approvals and migration guidance.
- Maintainers may use lazy consensus with a minimum 7-day review window for normative changes.

## Versioning Rules

OpenTSR uses a SemVer-like versioning model.

- `MAJOR`: incompatible schema or semantic changes.
- `MINOR`: backward-compatible additions.
- `PATCH`: editorial or tooling updates with no interoperability impact.

A breaking change includes:

- Removal/rename of existing fields.
- New constraints that invalidate previously valid events.
- Semantic reinterpretation that changes interoperability behavior.

## Required Artifacts for Schema Changes

Every schema-impacting PR MUST include:

- Update to [`spec/schema.json`](../spec/schema.json).
- Update to [`spec/SEMANTICS.md`](../spec/SEMANTICS.md).
- Update to [`spec/vocabulary.md`](../spec/vocabulary.md) when introducing or changing namespaced terms.
- Entry in [`CHANGELOG.md`](../CHANGELOG.md).
- Updated examples in [`examples/`](../examples) when applicable.

## RFC Template

- Discussion form: [`.github/DISCUSSION_TEMPLATE/rfc.yml`](../.github/DISCUSSION_TEMPLATE/rfc.yml)
- Markdown fallback: [`RFC_TEMPLATE.md`](RFC_TEMPLATE.md)
