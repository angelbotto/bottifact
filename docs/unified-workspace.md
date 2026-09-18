# Reading, tables and connected context

Margen has three delivery surfaces: portable HTML, React components and the hosted workspace. They share concepts but do not have identical capabilities. Nothing in the reader grants extra permissions.

## Reader controls

The generated shell includes Appearance, Review, Share and More once. A capable hosted reader hides the portal's fallback controls. Old stored HTML is not rewritten; the render endpoint adds the compatible shell. Standalone review remains local and explicitly exported.

Appearance is personal. Theme family and light/dark/system mode remain separate from typography and sound. Favorites and per-document settings use the reader's device storage; hosted overrides are scoped to account and artifact. Sound still requires the browser's first interaction and respects mute. No action in this toolbar changes the published theme.

Owners can manage access through Share. Other readers can copy the canonical link; copying never grants access or publishes a draft. More opens authorized references and search in connected documents. Infrastructure details stay out of the document.

## Tables

See [mobile reading and table controls](mobile-and-tables.md) for the responsive Table/Cards presentation and the current control hierarchy.

- Core `TableQuery`: search, AND/OR conditions, seven operators, stable multi-sort, nulls last and formula-safe CSV. React and portable tables use the same executable query model.
- React `DataTable`: TanStack Table v9 with semantic table primitives, FilterBuilder, column visibility, fixed columns, width controls, density, explicit aggregation, stable selection, optional row inspector and local saved views. Pass `selectable`, `inspectable` and an account/document/table-specific `persistenceKey` when needed. Avoid using a shared persistence key on shared devices.
- Portable `[data-explorador]`: semantic fallback, conditions, saved views, grouping, page-sized subsets, column width/fixing, stable row/cell anchors and detail dialog. Data remains in the HTML. Limits: 2,000 rows, 16 columns, no editable cells or virtualized rendering.
- Workspace: full authorized-set filters, cursor-scoped queries, private saved filters and explicit selected-record batch tagging, collection assignment and reversible archive/restore. All records are reauthorized before the transaction commits. No implicit “select every matching document”.

The administrator remains a vanilla JavaScript application. React components are available for adopters; this release does not pretend to have migrated the portal to React.

Try the [synthetic scenarios](../examples/generated/workbench.html). Group totals must declare units and whether they cover a page or the complete filtered dataset. Missing values are not zero. Use immutable row IDs for future-version comments.

## Context workbench

**Search / Cmd-Ctrl K** opens authorized document search and actions. **Entities** stores personal companies, projects and topics with aliases, properties and assigned owned artifacts. Names and aliases never merge records automatically. Existing space/tag/collection metadata is preserved.

**References and connections** shows outgoing links and backlinks with source version and quotation. `cites`, `updates`, `contradicts`, `depends_on` and `resolves` are explicit directional relations. The API verifies the quote against the source version and optional section ID. Only the source owner creates or changes links; both endpoints must be readable to display the link. Draft evidence is hidden from readers without editing access. Withdrawn links disappear from the view. Unlinked literal title matches are suggestions for review, not confirmed knowledge; they can be dismissed.

The graph keeps membership and evidence relations distinct. Filter by relationship, inspect the edge, explore one/two hops, search entity aliases and save the node positions privately. The graph's existing 120-artifact scope is still disclosed. Entity views are personal; there is no shared global taxonomy migration.

**Working sets and boards** are private to the account. Collect artifacts and your own notes. Drag board cards, or focus a card and move it with arrow keys; Save persists the arrangement. Verified typed links between cards are displayed independently of their position. Use Connect cards with evidence to create a relation; reopen the board to refresh newly created relations. Position alone does not establish a semantic relationship. Revoked documents are removed from returned saved views. Notes are never converted to public content. Board notes are working-set text, distinct from anchored review notes.

**Sessions** lists recorded artifact versions grouped by agent, session and device for the owner. These are source metadata, not imported transcripts or an automatic connection to a running agent.

## Preparing a revision

1. Review → Prepare context for AI.
2. Select the comment threads you intend to share. Enable personal notes explicitly, then select the relevant notes.
3. Select any verified references you need, then generate and inspect the exact prompt.
4. Copy it or download the structured bundle.
5. Give it to the intended agent, preserve the artifact ID and publish changes as a draft. Compare and release explicitly.

The bundle contains artifact/version URLs, thread IDs, quotations, anchor status and recorded provenance. Reviewer text remains feedback, not system instructions. Source session/device information is restricted to the creator. Copying does not send to an agent, resolve comments or publish a revision.

## Implementation map

| Layer | Entry point |
| --- | --- |
| Portable shell | `packages/core/components/reader-controls.js` |
| Query contract | `packages/core/src/table-model.ts` |
| Generated browser query module | `packages/core/components/table-model.js` |
| React primitives | `packages/react/src/components/{DataTable,FilterBuilder,Inspector}.tsx` |
| Portal context UI | `portal/static/context-workbench.js` |
| Portal review composer | `portal/static/reader-workspace.js` |
| Knowledge persistence/API | `portal/context_graph.py` |
| Server filter adapter | `portal/table_query.py` |

The generated table module is committed so Python-only skill installations need no Node compiler. `npm run build` regenerates it; CI checks that it matches the source. SQLite migrations are additive and covered by authorization tests. Back up before deploying, retain the previous image and update the portable skill separately.

## Current boundaries

No automatic agent delivery, semantic embeddings, transcript imports, shared boards or editable spreadsheet cells. Workbench dialogs use a common layout; the existing artifact preview remains the sidebar. Saved views are personal. Local views cannot synchronize from an opaque iframe without a connected capability; unavailable storage is reported. Account settings do not yet follow a person across devices for every appearance choice. Each surface's actual support is documented rather than inferred from a component name.


### Review and presentation update

The reader dock exposes Appearance, one writing action, counted Comments, and Share. Privacy is selected inside the composer; existing thread types stay immutable. The count includes open threads visible to the current reader, including their own private notes, and excludes replies/resolved threads. Nearby pins group by position and open every contained thread. Share owns link/access and creator management; there is no generic More dock.

Record explorers support Table, List, Cards and Board. List reduces per-record spacing; Board groups the existing rows by the selected field (preferring a categorical status/team field initially). The portable board shows the current filtered page, with per-lane counts explicitly scoped to that page. React uses its supplied filtered dataset. Both preserve source records and selection. This is a read-only presentation, not drag-and-drop state editing or an inferred workflow. Saved portable views include presentation. Horizontal scrolling stays local to the board; print returns to a table.
