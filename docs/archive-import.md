# Recover existing artifacts

The library provides gallery, list, table and graph views with progressive loading. Search covers title and indexed content. Renaming, categorizing, tagging and collecting an artifact edits its metadata without changing its document identity.

Use `scripts/publish.py --help` for the supported import interface. Inspect candidate HTML files from authorized workspace/session locations before upload. Exclude credentials, private transcripts, generated caches, unrelated websites and duplicates. A file's presence in a session is not proof of authorship or permission to publish it publicly.

Prefer stable document metadata to filenames for deduplication. Preserve existing account artifact IDs when adding revisions. Record agent, device and session only when verified from actual provenance; use an explicit unknown state otherwise. Review preview and extracted title before publication. New imports default to private visibility and retain the selected account/server.

The portal stores uploaded artifact versions and comment context centrally. Standalone browser comments are separate; uploading HTML does not import localStorage. See [installation](installation.md), [portal operations](portal-operations.md) and [connected library](connected-library.md).
