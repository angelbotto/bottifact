# Open-source preparation · 17 September 2026

Scope: portable installation, configurable self-hosting, documentation and repository release preparation.

- Existing portal tests and six new self-hosting contracts: 49 tests passed locally.
- Library validation, nine generation contracts, distributed review-store checks, 150 theme checks and portable skill validation passed.
- A disposable Docker Compose project started on a Linux NAS with empty named volumes and runtime UID/GID 1000. No production accounts, configuration or documents were copied.
- The integration exercise verified administrator bootstrap, account identity, private artifact creation, an anchored comment, denied anonymous access, portable ZIP SHA-256 and licensing files, backup verification and isolated restore.
- The optional Caddy configuration validated. This test did not request a real certificate for a new public domain.
- Gitleaks found no secrets in 126 historical commits, the working source tree or the retrieved historical CI logs. This is an automated scan, not proof that every possible secret or vulnerability is absent.
- Google and email self-hosted domain behavior is covered by contract tests. New operators must configure their own provider and verify actual consent/delivery.

The production library and its document permissions are separate from repository visibility. Publishing source does not publish any hosted artifact. There has been no independent third-party security audit.
