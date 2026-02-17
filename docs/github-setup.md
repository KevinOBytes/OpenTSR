---
layout: default
title: GitHub Setup
---

# GitHub Setup Checklist

These actions must be completed in the GitHub UI by a repository administrator.

## 1. Enable GitHub Pages

1. Open **Settings** -> **Pages**.
2. Set **Source** to `GitHub Actions`.
3. Ensure workflow `Deploy Docs` is enabled.
4. Save and wait for the first publish.

## 2. Enable Discussions

1. Open **Settings** -> **General**.
2. Enable **Discussions**.
3. Create an `RFC` category and attach the RFC template if prompted.

## 3. Branch Protection

1. Open **Settings** -> **Branches**.
2. Add a protection rule for `main`.
3. Require pull requests before merge.
4. Require status checks:
   - `Validate Schema and Examples`
   - `Lint Docs`

## 4. Labels

Create or verify these labels:

- `rfc`
- `spec`
- `breaking-change`
- `docs`
- `good-first-issue`
