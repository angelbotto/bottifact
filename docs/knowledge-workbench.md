# Knowledge workbench: product directions

This is a proposal backlog, not a list of deployed portal features. The existing portal provides artifact search, classification, gallery/list/table views, review and shared-tag/collection graph edges. The new local `relationship-map` recipe demonstrates richer navigation using declared synthetic data; it does not change the portal's data model.

## Make the map answer a task

| Task | Entry point | Useful view | Next action |
| --- | --- | --- | --- |
| Resume yesterday's work | Session or recent artifact | One-hop neighborhood | Prepare the pending context |
| Explain a decision | Decision record | Evidence and alternatives | Open the cited version |
| Assess a changed assumption | Claim or source | Dependents and unresolved reviews | Prepare impact review |
| Find a missing link | Search result | Related pieces with reasons | Propose a connection |
| Close a review cycle | Comment | Version → session → result | Verify the change before resolving |

Avoid treating proximity as proof. Preserve type, direction, source and state. A declared edge is not automatically true; it means someone supplied it. Suggestions remain separate until reviewed. Search must explain whether it covers the local selection or the entire authorized library.

## Interaction requirements

- Start with a named piece and one hop. Offer two hops and an explicit full-map view.
- Use legible labels, visible counts and a list equivalent. Avoid anonymous circles as the only entry point.
- Preserve search and filters when switching list/map. Show exclusions, including result caps.
- Support a return trail. Clicking a neighbor should not lose the reader's starting point.
- Inspect the relationship itself: direction, reason, source version, author/process and review state.
- Offer focused views for project, timeline, impact and pending review. These are different questions, not color presets.
- Keep selection separate from opening the full document. Opening returns to the prior query and position.
- Handle isolated nodes, empty filters, expired access and missing sources as explicit states.

## More capabilities, ordered by dependency

### Foundation: model and trust

1. **Project brief:** objective, owner, status, boundaries and completion criteria.
2. **Session record:** agent, actual origin, device availability, objective and outputs.
3. **Typed links:** directed relationships with source and confirmed/suggested state.
4. **Version-aware citations:** references resolve to the version that supported the statement.
5. **Workspace profile:** audience, communication preferences and approved default compositions.
6. **Permission preview:** inspect what each recipient can actually see before sharing a bundle.

### Daily work: find, inspect, continue

7. **Saved views:** name a query and its columns/sort/scope; use the same scope in the map.
8. **Working set:** pin related artifacts, sessions and notes for the task at hand.
9. **Universal inspector:** one detail pattern for list rows, cards, nodes and comments.
10. **Review inbox:** group by artifact, project, owner or version; separate personal notes.
11. **Context preview:** inspect exact quotations and exclusions before an agent receives anything.
12. **Return trail:** revisit exploration steps with scope preserved.
13. **Reading trail:** optional personal record of recently visited pieces; not surveillance of readers.
14. **Offline handoff:** explicit queued/received/failed states and a downloadable fallback.

### Reasoning: explain rather than decorate

15. **Decision ledger:** options, evidence, accountable owner and revisit condition.
16. **Assumption register:** separate observed facts, estimates and unknowns.
17. **Counterevidence lens:** surface declared contradictions without automatically adjudicating them.
18. **Source freshness:** time and review policy per source; old does not automatically mean false.
19. **Impact preview:** list declared dependents when a source changes; report incomplete coverage.
20. **Alternative comparison:** agreed criteria and optional sensitivity, not invented scoring.
21. **Open-question map:** connect questions to missing sources and responsible next steps.
22. **Orphan review:** identify unclassified pieces and broken references without inventing links.

### Knowledge quality: supervised assistance

23. **Connection suggestions:** explain supporting excerpts; accept, reject or correct with history.
24. **Duplicate candidates:** compare content/version before proposing a merge; reversible handling.
25. **Semantic retrieval:** opt-in provider, documented data boundary and authorized citations.
26. **Editorial learning:** propose preferences based on approved examples; allow inspection and reset.
27. **Component recommendation:** map the writing task to relevant recipes with an explanation.
28. **Agent evaluation:** same tasks across agents; measure factual grounding and usability, not component count alone.

### Collaboration and portability

29. **Context delivery receipts:** distinguish exported, delivered, received and applied.
30. **Session adapters:** resume only when the agent supports it; otherwise create a fresh contextual session.
31. **Review ownership:** assign responsibility without treating assignment as acceptance.
32. **Decision review rituals:** optional digests of pending decisions; deliberate subscriptions, no unsolicited messages.
33. **Project export/import:** portable documents, reviews, IDs and relation manifests; explicit identity mapping.
34. **Workspace templates:** executive update, engineering investigation, operational review and research notebook.
35. **Release provenance:** generator/library version and source hashes for reproducible artifacts.
36. **Health dashboard:** queue age, stale previews, search latency and tested restore dates, visible to operators.

## What to build first

Deliver one end-to-end loop: choose a project → find a session's result → read a comment in its original version → preview a scoped context bundle → receive a proposed revision → verify and resolve. Measure time to resume, origin coverage and correctly applied review before expanding automation.

The next step for the portal is first-class project/session/relationship records and an inspector using those records. Replacing circles with more elaborate graphics without changing the information model would only move the problem.
