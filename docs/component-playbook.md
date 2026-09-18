# Component playbook

Bottifact's catalog is a selection tool, not a checklist to fill in every document. Open `examples/generated/guide.html`: search by need, narrow by family or composition journey, then open a working example, limits and copyable source. The current count comes from `VERSION.json`; manifests and recipes are authoritative.

## Three different levels

| Level | What it provides | What it does not imply |
| --- | --- | --- |
| HTML recipe | Portable semantic markup, optional local interaction and documented limits | A backend, live data or shared permissions |
| React export / recipe preview | Native wrappers or an isolated preview of the original recipe | Every recipe rewritten as a native React component |
| Connected portal feature | Authenticated persistence, authorized documents and shared review | All local recipe demonstrations are deployed administrator features |

A session brief is now a reusable recipe. A persistent session entity is still a product proposal. The local relationship explorer supports declared typed connections; the current portal graph still derives links from shared tags and collections. Keep these distinctions visible in demos and release notes.

## Choose by question

| Reader's question | Start with | Add only when useful |
| --- | --- | --- |
| What changed? | Finding, traced cards, time series | Version comparison and source annotations |
| What should we decide? | Decision record, comparison, criteria | Evidence ledger, uncertainty and sensitivity |
| Where did this come from? | References, methodology | Session brief and relationship map |
| How do I continue? | Session brief and context bundle | Review queue, original citation and version comparison |
| Which claim can I trust? | Evidence ledger | Source date, denominator, counterevidence and unresolved question |
| What happened in operations? | Route/fleet views and delivery detail | Exception queue, distribution, capacity and timeline |
| Why did a financial metric move? | Time series and waterfall | Reconciliation, scenarios and assumptions |
| How do I use this API? | Code, terminal and animated callouts | Prototype, tabs and recovery sequence |
| What do I need to review? | Review queue | Context bundle and explicit acceptance criteria |

Use the exact catalog IDs from `scripts/catalog.py`; the CLI also accepts the English aliases. Not every item above requires a new recipe. Existing decision, risk, methodology and comparison patterns should be reused before adding competing versions.

## What each component page must show

1. **Purpose:** the question it answers and a counterexample where it is inappropriate.
2. **Live example:** synthetic data and visible states; no screenshots of private accounts.
3. **Data contract:** required fields, unknown values, units, source and audience.
4. **Interaction:** keyboard, pointer, touch, empty results and reset/return behavior.
5. **Accessibility:** semantic source, focus, narrow screens, reduced motion and alternative to visual encoding.
6. **Limits:** local vs connected behavior, bounds, external dependencies and persistence.
7. **Source:** copyable HTML and dependency list, plus the correct React integration level.
8. **Composition:** useful neighboring components and a realistic document outline.

A static fixture is valid when labeled. A decorative button that promises to save, sync or resume work without doing so is not.

## New continuity recipes

| Recipe | Interaction | Example input | Boundary |
| --- | --- | --- | --- |
| `relationship-map` | Search, focus, one/two hops, relation/state filters, history, zoom, source tables | Node and edge tables with explicit directions and reasons | Local; no portal entity creation or automatic inference |
| `session-brief` | Expand continuation criteria | Objective, output version, known source, pending action | Does not import or resume a conversation |
| `context-bundle` | Review scope and copy text | Artifact, version, citation, change request, recipient | Copying is not delivery; no private notes added automatically |
| `evidence-ledger` | Accessible comparison table | Claim, epistemic state, source, missing evidence | Does not validate evidence or calculate confidence |
| `review-queue` | Expand context and resolution criteria | Shared comment vs personal note, source version | Static composition; enforce permissions before rendering |
| `version-comparison` | Side-by-side editorial comparison | Before, proposal, rationale and review status | Manual fragments, not an automatic diff engine |

## Compositions to try

**Executive decision:** finding → highlights/lowlights → evidence ledger → alternatives → decision → risks → next action. Put a question in a left margin and a caveat in a right margin only when they improve interpretation.

**Return to a conversation:** session brief → original artifact/version → review queue → context bundle → proposed version comparison. Preserve the original source reference; do not fabricate session IDs to fill the card.

**Understand a project:** objective → local relationship map → selected evidence → decision → timeline → unresolved work. The map should open near the current question, not as a wall of every known item.

## Contributor acceptance checklist

Keep original source tables readable without JavaScript. Use a unique container ID. Mount once, support destroy/remount and release listeners. Imported strings are text, not HTML instructions. Do not include inaccessible records in client payloads. Validate source and generated examples, test affected behavior and inspect mobile/desktop before packaging. See [contributing components](contributing-components.md).
