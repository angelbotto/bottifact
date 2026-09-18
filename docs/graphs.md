# Search, classification and graphs

The graph explains connections among artifacts available to the signed-in viewer. It is a navigation aid, not a claim that the system understands every idea or has read your agent conversations.

## Inputs and meaning

SQLite FTS indexes document text and metadata for search. Local classification rules in `portal/knowledge.py` inspect normalized titles and body text, propose up to five tags and expose matching terms. The current vocabulary is primarily Spanish; English documents do not have equivalent classification coverage yet. Manual tags, category overrides and collections remain useful regardless of document language.

A graph node represents an authorized artifact. An edge exists when two artifacts share tags or collections. Its reasons name those shared items; the weight is `3 × shared collections + shared tags`. Category alone does not create an edge. The graph bounds each node to four retained edges, preferring stronger relationships, to avoid unreadable clusters. The portal also limits the graph to the 120 most recently updated matching documents; it is not an exhaustive graph of an arbitrarily large library.

## Access and privacy

Graph input is filtered through artifact permissions before relationships are calculated. An invisible artifact must not leak through a label, edge, count or preview. Personal notes do not automatically become shared knowledge edges. Publishing origin remains separate from inferred subject matter.

A shared tag means topical overlap, not dependency, causation or agreement. Users should be able to inspect the edge reason and refine classification instead of treating suggestions as facts.

## Sessions and review context

An artifact can record its publishing agent/session/device. Feedback exports use that provenance to explain where a requested change belongs. The graph does not import the session transcript, infer discussion history or send comments back automatically. See [feedback and sessions](feedback-and-sessions.md).

## Extension points

- Expand language-specific rules with tests and visible matching evidence.
- Add explicit typed links such as “supersedes”, “supports” or “contradicts”, with author and rationale.
- Add a semantic search adapter only with a documented data boundary and an opt-in provider configuration.
- Keep permission filtering before scoring and before returning graph payloads.
- Separate source-session links from subject links; they answer different questions.
- Test sparse, dense, empty and access-revoked graphs before increasing limits.

These are extension directions, not shipped embedding search, automatic model training or transcript synchronization. Tests in `portal/test_knowledge.py` exercise classification and graph access behavior.
