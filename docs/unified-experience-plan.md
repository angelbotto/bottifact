# Unified workspace and artifact experience

Status: implementation in verification, September 2026. The delivered scope and explicit boundaries are tracked in [the unified workspace guide](unified-workspace.md). This original plan includes follow-up enhancements and is not a claim that every acceptance gate has passed. Baseline: portal 0.4.0.

## Outcome

A person should be able to find an artifact, read it, inspect its evidence, leave feedback, share it with the intended audience, and prepare the next revision without learning different controls at every step. Improvements apply to the administrator/workspace, the hosted artifact reader, and the portable artifact library. Each surface exposes the capabilities actually available to that user.

## Verified baseline

- The workspace has gallery/list/table/graph views. Tables have searchable facets, server-wide bidirectional sorting, column visibility, density and incremental loading. The graph has typed company/space, topic and collection memberships, evidence labels and local neighborhoods.
- Artifact HTML has its own appearance and review controls. Hosted HTML connects to portal review through a constrained bridge; portal reader controls and document controls currently coexist.
- The portal reader places sharing inside an owner management popover. This makes it harder to discover and gives management, reading and reviewing different entry points.
- Comments, personal notes, role-based access, drafts, versions and feedback export already exist. Source agent/session/device are metadata, not imported conversations or a guaranteed route to a running agent.
- The core library, React adapters and portal are separate delivery layers. The current portal is not a React/shadcn application.
- Installed skills can opt into six-hour updates from their chosen server. Portal deployment is a separate operator action.

## Product rules

1. Consistent action names, icons, focus behavior and states across surfaces. A tooltip accompanies every icon-only action; accessible names work without hover.
2. The reader opens on the artifact itself. Management and provenance details belong in the creator's inspector. Infrastructure/storage terminology stays out of the reading flow.
3. Preserve document/version IDs, anchors, URLs, access, personal settings and pending drafts through migrations.
4. Preserve editorial themes and typography inside artifacts. Workspace controls use application tokens; the document's visual identity must not accidentally recolor the whole administrator.
5. Filters and order always describe the full declared data scope. A loaded subset is never presented as a complete total.
6. Private notes, shared comments and proposed AI instructions have distinct scopes. Copying or sharing a link never silently changes access.
7. Static HTML remains useful without an account, React or a network connection. Clearly distinguish local storage from connected collaboration.

## Capability matrix

| Capability | Workspace | Hosted artifact | Standalone HTML |
| --- | --- | --- | --- |
| Appearance | Workspace preferences | Document defaults plus reader overrides | Document defaults plus device-local overrides |
| Tables | Server queries and saved views | Embedded local data or explicitly declared authorized data source | Embedded data only |
| Review | Cross-document inbox and inspector | Contextual pins, replies and private notes under server permissions | Local review and explicit file export/import |
| Sharing | Manage access and copy link | Permission-aware share entry point | Download/export or copy an existing canonical publication link |
| Knowledge | Authorized graph and entity pages | Related documents, citations and backlinks permitted for that reader | Declared references/local relationship component |
| AI handoff | Select authorized material across documents | Current artifact/version/selected threads | Local content and review export |

A published URL stored in an HTML file does not make that file authenticated or synchronized. Cross-document actions require a connected portal capability.

## Delivery sequence

### R1 — Common controls and artifact reading/review

**Purpose:** make appearance, comments, notes and sharing easy to discover and consistent before adding more features.

- Define one action inventory and icon set: Appearance, Review, Share and More. Review exposes separate Comment and Personal note creation. A direct note shortcut can be offered in review mode without adding another permanent toolbar.
- Put a compact toolbar in a predictable corner on desktop. Use one reserved mobile action row with safe-area handling; it must not overlap progress, navigation, pins or text. Keep controls reachable by touch, keyboard and screen readers.
- Negotiate control ownership between a capable artifact and the portal. Render each action once. Keep a portal fallback for older documents without rewriting stored HTML versions or breaking their anchors.
- Appearance: searchable theme families with previews/favorites, a separate light/dark/system control, typography presets and an independent sound tab. Reader overrides remain personal; only an explicit creator action changes published defaults. Sound preference can be enabled, but playback waits for browser-required interaction and honors mute/volume.
- Review: anchored compact composer and contextual pins. A shared inspector provides threads, personal notes, open/resolved filters, replies and origin context. Small screens use a sheet; desktop uses an adjustable side panel.
- Sharing: direct recognizable action. Owners/managers can inspect and change access; readers can copy the current authorized link without gaining permission-management controls. Explain private, invited, link-accessible and public states. Separate public discoverability from possession of a link.
- Sharing dialog: current access, people and roles, conversation visibility, then Save permissions and Copy link. Unsaved access changes must not be implied by a successful copy. Do not send invitation emails without an explicit send action.
- Optional platform-native sharing can be progressive enhancement; Copy link is the reliable fallback. Sharing must not include personal notes or draft versions implicitly.
- Update theme/review/share recipes and skill guidance in the same release. Document hosted/local behavior side by side.

**Acceptance:** one instance of each supported action; no overlap at 320/390 px; keyboard focus restores after closing; personal appearance does not alter the published default; a viewer cannot manage access; a private link remains private after copying; offline drafts survive a failed save; a note never appears in another reader's review feed. Old artifact fixtures keep their original URLs and usable review behavior.

### R2 — Tables as a reusable product component

**Purpose:** bring the administrator's improved data navigation into artifacts and the React library through a common contract.

- Define typed columns, stable row IDs, cell types, filter expressions, sort priority, grouping, visibility, sizing, selection and persistence scope.
- Build a React DataTable adapter with shadcn primitives and TanStack Table. Retain a portable HTML adapter with the same supported behavior and a semantic table fallback. Avoid shipping the entire React runtime just to render a standalone table.
- Add multi-select facets, operator-aware numeric/date filters, date ranges, AND/OR groups, multiple sort criteria, grouping with declared aggregations, pinned/resizable columns, density and reset.
- Saved views store query, filter model, sort, grouping and columns. Scope them by account and table identity; standalone views stay device-local. Do not store access grants in view definitions. Sharing a view does not broaden its underlying data permissions.
- Select rows and expose authorized batch actions. Workspace actions include tagging, adding to a collection and archiving. Artifact actions include copying selected evidence and exporting the displayed data when permitted.
- Clearly distinguish selected loaded rows from all matching results. Server-wide batch selection needs explicit count, authorization recheck and a recoverable result summary. Do not use destructive actions in the first batch-action release.
- Add an inspectable row detail panel. Table comments anchor to stable row/cell IDs, not visual row positions, and remain discoverable when a row is filtered out.
- Provide recipes with synthetic data: Liftit deliveries/exceptions, Tikin financial reconciliation, Catabum project decisions. Include sources, units, missing values and aggregation scope.

**Acceptance:** equivalent filter semantics for local and server adapters; deterministic sort with nulls and ties; no duplicate/missing rows at cursor boundaries; selection survives sorting; filtered-out anchors remain visible in review lists; no misleading full-data totals; view persistence does not cross accounts/documents; CSV/export escapes unsafe spreadsheet formulas; keyboard and narrow-screen flows work.

### R3 — Search, inspection and working context

**Purpose:** make the workspace and artifact use the same interaction patterns for finding and inspecting evidence.

- Command palette for authorized document/entity search and context-appropriate actions; keyboard shortcuts are discoverable and do not intercept text editing.
- Shared inspector structure for a table row, gallery card, graph node, reference or comment. Use Sheet on mobile and Resizable panels on desktop; preserve scroll, filter and focus when it closes.
- Hover/focus previews for citations and related documents, with click/touch equivalents. Do not disclose private titles through previews or counts.
- Context menus and action dropdowns offer the same capabilities as visible controls. Add date pickers, badges, skeletons, empty/error states and recoverable notifications where the flow needs them.
- A private working set gathers selected artifacts and notes for the current task. Saving a working set does not create a public collection or export notes.

**Acceptance:** the same action means the same thing on each surface; no hover-only information; navigation returns to the original scope; expired access produces a useful recovery state and no cached private preview leak.

### R4 — Knowledge model and Obsidian-inspired exploration

**Purpose:** let the map explain the work and the evidence behind it.

- Add explicit entities for company, project and topic, with editable properties and aliases. Migrate existing space/tag values through a reversible mapping; never merge entities solely because names look similar.
- Add directional links: cites, updates, contradicts, depends_on and resolves. Store source artifact/version/anchor, author or process, creation time and proposed/confirmed state. Existing tag membership remains a different relation type.
- Backlinks show incoming references and their supporting quotations. Unlinked mentions become suggestions with evidence, confirmation and dismissal. Start with transparent matching; semantic search is a separately evaluated enhancement.
- Entity pages show related artifacts, decisions, review activity and known source sessions. Only records authorized for the viewer contribute to results and counts.
- Extend the graph with entity search, relationship filters, optional local default, breadcrumbs, explainable edge inspection, saved layouts and orphan/broken-reference review.
- In the artifact, expose a small Related/evidence panel, cited-version previews and backlinks through the same inspector. A standalone export shows only explicitly included references and its completeness boundary.
- Add saved board/canvas views: place artifacts, notes and quoted fragments spatially, draw typed links and group a decision's evidence. Personal notes require explicit, permission-aware conversion before appearing on a shared board.

**Acceptance:** aliases do not silently merge companies; every semantic edge has declared provenance; suggestions are visibly unconfirmed; private documents cannot be inferred through titles, counts or edges; references resolve to their supporting version; deleting/moving content yields an explicit missing/changed state. Visual proximity alone is never a claimed relationship.

### R5 — Feedback to revision, with session context

**Purpose:** let the user act on feedback from either the artifact or the administrator.

- A unified context-bundle composer includes selected comments, optional own notes, quotations, source version, artifact URL/ID, approved related evidence and known agent/session/device metadata.
- Preview exactly what will be copied, with unavailable/private material excluded by default. Include thread IDs, requested changes and acceptance criteria without presenting reviewer text as authorized system instructions.
- Offer Copy prompt and Download bundle first. A later Send to agent action requires a configured adapter, an explicit destination and observable delivery status; it must not claim to resume an unknown session.
- Show revision trace: feedback → proposed draft → reviewed diff → published version. Publication and resolving a thread remain explicit actions. Support conflicts and stale anchors instead of overwriting silently.
- Session pages initially list recorded outputs and links; importing transcripts is a separate opt-in integration with retention and access policies.

**Acceptance:** copied content identifies artifact/version/context; personal notes are included only by their author deliberately; a destination/session is never invented; a failed delivery leaves the bundle recoverable; a published change does not automatically mark every related comment resolved.

### R6 — Component discovery, skill guidance and release continuity

This work accompanies R1–R5; it is not deferred to the end.

- Each component ships with a live synthetic example, data contract, usage/counterexample, supported states, keyboard/touch behavior, local/hosted distinction and HTML/React integration level.
- Add scenario recipes and a selection guide: executive report, operational table, financial analysis, technical documentation and review handoff. Choose components for the reader's task rather than filling a component quota.
- Shared skill instructions specify common shell usage, stable anchors, data sources, privacy, defaults and correct publication/update flow. Claude, Codex and Hermes use the same canonical package and versioned examples.
- Add portable evaluation scenarios for voice, component selection, evidence and handoff completeness. Use synthetic or explicitly approved examples; personal feedback is not shared training data by default.
- Publish a compatible portable package after verified releases; retain the selected update server, opt-in schedule, previous version and rollback path. Expose installed/current version and successful-check time separately.
- Release the portal with backup, compatibility tests, staged verification, health/auth checks and rollback. A skill timer never silently redeploys a self-hosted portal.

**Acceptance:** an installed skill can discover and produce the new components; examples match shipped behavior; old/new bridge combinations fail gracefully; release notes list actual capabilities; tests verify all three agent installation paths without claiming that an already open conversation has reloaded instructions.

## Technical approach and boundaries

- Keep FastAPI, SQLite/FTS on local storage, version files and the worker for the existing single-instance service. Nothing in this plan by itself requires a graph database or a new hosting provider.
- Introduce versioned relational tables for entities, aliases, links, saved views and working sets with foreign keys, indexes, explicit ownership and backup/restore tests. Benchmark before selecting a different database or search engine.
- Define headless state/data contracts in core, React adapters in the React package and standalone behavior in the existing portable layer. Introduce React islands in bounded portal surfaces, starting with DataTable and inspector, rather than replacing routing/authentication in the same release.
- Tokens and icon definitions are shared; permission checks remain server-side. The iframe bridge has a versioned, narrow capability schema and validates sender, target artifact and permitted operation. Document HTML must never receive account tokens.
- Keep reading preferences separate from published document settings and account-level workspace preferences. Make persistence and precedence explicit and offer reset at the correct scope.
- Measure representative library sizes and table row counts with synthetic fixtures. Test graph layout responsiveness before raising the current 120-artifact/300-entity caps. Avoid promising unbounded rendering or embedding remote records into portable HTML.

## Verification and rollout gates

For each release: unit/state tests, API authorization and migration tests, browser flows at desktop/320/390 px, keyboard/focus, reduced motion, light/dark themes, slow/offline/error recovery, generated HTML contract checks, portable install/update checks and legacy reader compatibility.

Sharing tests cover anonymous, named guest, authenticated reader, commenter, editor, owner and administrator. Review tests cover stale anchors, filtered rows, duplicate requests, draft changes and clipboard failures. Export tests check data scope, private-note exclusions and hostile review content.

Use synthetic screenshots only. Collect opt-in usability observations for finding a document, filtering a table, adding a contextual note and copying an actionable review bundle; establish a baseline before claiming time savings. Define performance budgets after measurements on an agreed representative dataset.

## Recommended first increment

Build R1 first: artifact toolbar, direct sharing, appearance hierarchy and unified review inspector, with hosted/standalone examples. Then implement R2's reusable table contract and saved views. R3 extends the shared inspector; R4 adds the knowledge model; R5 connects review to revisions. Documentation and skill updates ship with every increment.

Each increment is independently reviewable and releasable. Dates and staffing are intentionally unset until the first compatibility prototype is evaluated; this plan is a prioritized scope and acceptance contract, not an invented delivery estimate.
