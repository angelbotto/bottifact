# Hosting history

This page records the original managed deployment, not the recommended self-host installation procedure. The shared service at `artifacts.botto.is` runs on the owner's NAS behind an existing Cloudflare tunnel. Artifact versions and review data are stored centrally, with backup and restore procedures documented separately.

The hosting arrangement is an instance-specific choice. Margen does not require a NAS, Tailscale, Cloudflare or the owner's domains. Follow [self-hosting](../self-hosting.md) for an independent deployment and [the hosted service](../hosted-service.md) for using the existing account service.

Do not copy instance credentials, tunnel configuration, private addresses, account aliases or production data into a public package. Storage implementation details belong in operational documentation, not the shared artifact UI.
