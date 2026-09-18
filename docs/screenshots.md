# Public screenshots and fixtures

Public images must be captured from `examples/react` or another explicitly synthetic, committed fixture. Do not capture the production artifact library, an authenticated account menu, personal notes, agent conversations or a real customer's document.

## Capture process

1. Open the local fixture in a clean preview with no account session.
2. Use illustrative titles, values and identifiers. Use `example.com` for any necessary addresses.
3. Capture only the application viewport; exclude browser tabs, URLs with tokens, desktop notifications and developer tools.
4. Inspect the resulting image at full size before committing it. Check visible text, selected options and accidental overlays.
5. Add/update `docs/assets/manifest.json` with the file, synthetic source and purpose. Run `python3 scripts/check_public_assets.py`.

The automated check verifies the allowlist, checksums and README references. It cannot prove that pixels contain no private data; human visual inspection remains required. Do not rely on blurring or cropping a production capture when a synthetic fixture can demonstrate the same feature.

Historical screenshots were removed from the current tree during the source reorganization. That does not erase previous Git commits. If an earlier image is found to expose a credential, rotate it first and handle history cleanup as a separate coordinated security change.
