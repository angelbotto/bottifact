# Knowledge graph in the administrator

The administrator's **Graph** view connects the documents you can access through explicit companies/spaces, topics, and collections. It is distinct from the standalone `relationship-map` component inside an artifact.

## What each node means

| Node | Source | Connection explanation |
| --- | --- | --- |
| Artifact | Published artifact in the current authorized result set | Title and existing preview |
| Company / space | The artifact's assigned `space` | Assigned workspace; never guessed from a company name in its body |
| Topic | Manual tags and enabled rule-based classification | Manual tag, or automatic tag plus matched evidence |
| Collection | Assigned collection | Membership in that collection |

Two companies can meet through a topic shared by their artifacts. Entity counts describe **the loaded, authorized set**, not an organization-wide total. Automatic topics use transparent rules, not embeddings or an LLM. You can correct organization metadata or turn automatic classification off from the artifact preview.

## Explore

1. Apply library filters or search across titles, indexed content, and authorized metadata.
2. Switch to Graph. Choose all connections, companies, topics, or collections.
3. Search for a node within the loaded graph, or select it directly. Its inspector explains each connection and offers the artifact preview.
4. Choose **Explore connections** for a local neighborhood. One hop shows immediate membership; two hops can reach other artifacts through a shared topic or company. Return restores the previous selection and scope.
5. Drag the background to pan, drag nodes to arrange them, and use the wheel or zoom buttons. Names can be toggled; hovering reveals a hidden name and highlights its edges. A list in the inspector provides an alternative to spatial exploration.

Keyboard: Tab reaches controls and nodes; Enter/Space selects a node. When the canvas itself has focus, arrow keys pan, Shift increases the step, and +/− zoom. There is no continuous motion or simulation loop after layout.

## Boundaries

The graph loads at most 120 recently updated artifacts and 300 membership nodes, plus up to 200 personal explicit entities. The interface discloses truncation; narrow the library filters to explore another subset. Local graph search searches that subset; the main library search searches the authorized library. Unassigned artifacts remain visible, without invented company edges.

The server checks access **before** producing nodes or edges. Other users' private artifacts, unpublished content, private notes, and owner-only session/device details do not become graph entities. No session history is imported. The older artifact-to-artifact `nodes`/`edges` API remains available for the related-documents preview; typed membership is returned under `network`.

Version 0.5 adds personal company/project/topic entities, aliases, version-pinned directional links, backlinks, literal title mentions for review, relation filters and saved node layouts. See [connected context](unified-workspace.md). Confirmed relationships carry a literal source quote; only the source owner can create or withdraw them. Existing space/tag membership remains distinct. Semantic similarity and automatic entity merging are not provided.
