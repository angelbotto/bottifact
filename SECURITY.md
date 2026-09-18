# Security policy

Report vulnerabilities privately through [GitHub's vulnerability reporting form](https://github.com/angelbotto/margen/security/advisories/new). If that form is unavailable, email security details to angel@botto.is. Do not post live tokens, login links, private documents or exploit data in public issues.

Include the affected release/commit, deployment configuration with secrets removed, reproduction steps, expected impact and any proposed mitigation. Use a local disposable installation to reproduce. Do not test against someone else's hosted instance without authorization.

## Supported versions

Security fixes target the latest published release and `main`. Older snapshots are not maintained separately. This early public release has automated contract and permission tests; it has not received an independent security audit.

## Deployment boundaries

Administrators can access all artifacts on their own instance. Restrict administrator emails and server access. Owner aliases merge identities and must only include addresses belonging to one person. Protect `.env`, database files, backups and agent tokens. Serve remote users over HTTPS, keep the internal app port private and apply dependency/release updates.

Artifacts may contain active HTML/JavaScript. The reader uses a sandboxed iframe and server-side access controls; sandboxing does not make arbitrary third-party code trustworthy or prevent all external network requests made by document content. Review what you publish and configure network/content restrictions for your use case. Do not host hostile workloads under assumptions of audited multi-tenant isolation.

The default standalone reader keeps local comments in browser storage. Central identity/permission enforcement requires the portal. A public source repository does not make any document in a running instance public. Generated exports, backups and screenshots can still contain sensitive content: review them before sharing.

A maintainer will triage reports and coordinate fixes/disclosure where possible. There is no guaranteed response time or paid bug bounty.
