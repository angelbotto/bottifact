# Connected library

Margen connects generated artifacts to a personal portal at the configured server. The skill generates HTML; the portal stores versions, permissions, comments, private notes and organization. The hosted service is `https://artifacts.botto.is`; self-hosters choose their own origin.

Gallery, list, table and graph share authorized search and filters. Search covers titles and indexed document text. Scrolling loads more records without page-number navigation. Previews use static isolated HTML, not active scripts from the uploaded artifact. Renaming and organization do not create a new document version.

## Organization
Assign a company/space, category, collections and tags. Automatic classification is rule-based and correctable; the UI explains matching evidence. Manual organization remains under the owner's control. Tags and collection membership do not grant access or prove causality. Archive removes an item from the normal library while preserving its shared link and history.

## Relationships and provenance
The graph connects accessible artifacts through declared organization and typed references. Companies, projects and topics can have aliases and properties. Inspect a relationship's origin instead of treating proximity as semantic proof. The same topic can span companies. Filters, search, zoom, keyboard interaction and the list alternative remain available.

Version provenance records the real creating agent, session reference and device. Missing historical provenance is not inferred. Session browsing groups recorded outputs; it does not load private conversations. The context composer exports selected authorized evidence and feedback, with private notes opt-in. Copy/download does not execute or send to an agent.

## Access
Owners control audience, versions and organization. Review permissions govern comments; personal notes remain author-private. Search, graph endpoints, related-document lookups and exports enforce access independently. Avoid embedding management metadata into the reader's document.

See [graphs](graphs.md), [feedback and sessions](feedback-and-sessions.md), [unified workspace](unified-workspace.md) and [portal operations](portal-operations.md).
