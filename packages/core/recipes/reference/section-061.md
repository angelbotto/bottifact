## Component library and local registry

`examples/generated/library.html` groups recipes into navigable chapters with guidance and dependencies. template.html is the continuous catalog; report.html is a narrative example. Use the generated registry for current counts.

`data-enlaces-internos` enables descendant deep links and history in the multipage library. Navigation activates and focuses the target outside the fixed bar; link to the recipe rather than a hidden inner tab. Each chapter has its own outline/progress. Printing includes all chapters; without JS all content remains.

The library is a local HTML catalog, not an installable CMS theme. The optional portal supplies separate authentication/collaboration. registry.json contains versioned HTML, chapter, modules and documentation; it is not the shadcn schema and should not be fetched at reader runtime. `NotaEditorial.init(root)` and get(element).destroy() manage archive/configurator lifecycle. Do not nest archives or duplicate IDs. A Ghost integration would additionally require CMS templates, context and GScan validation.
