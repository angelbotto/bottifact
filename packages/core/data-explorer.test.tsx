import { beforeEach, afterEach, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
const source = readFileSync(
  "packages/core/components/data-explorer.js",
  "utf8",
);
const model = readFileSync("packages/core/components/table-model.js", "utf8");
const recipe = readFileSync(
  "packages/core/recipes/data-explorer/example.html",
  "utf8",
);
let root: HTMLElement;
const engine = () => (window as any).NotaExplorador.get(root);
beforeEach(() => {
  document.body.innerHTML = recipe;
  root = document.querySelector("[data-explorador]")!;
  vi.stubGlobal("matchMedia", () => ({
    matches: true,
    addEventListener() {},
    removeEventListener() {},
  }));
  window.eval(model);
  window.eval(source);
});
afterEach(() => {
  engine()?.destroy();
  vi.unstubAllGlobals();
  document.body.replaceChildren();
});
it("changes mobile presentation without cloning cells or losing selection and stable anchors", () => {
  const cell = root.querySelector("tbody td")!,
    id = cell.id;
  expect(root.dataset.layout).toBe("cards");
  (root.querySelector(".explorador-seleccion") as HTMLInputElement).click();
  (
    root.querySelector(
      ".explorer-presentation [data-layout=table]",
    ) as HTMLButtonElement
  ).click();
  expect(root.dataset.layout).toBe("table");
  expect(document.getElementById(id)).toBe(cell);
  expect(engine().selected).toHaveLength(1);
  (
    root.querySelector(
      ".explorer-presentation [data-layout=cards]",
    ) as HTMLButtonElement
  ).click();
  expect(document.querySelectorAll('[id="' + id + '"]').length).toBe(1);
});
it("combines facet values, removes chips and restores the complete dataset", () => {
  (
    root.querySelector('[data-facet-value="Producto"]') as HTMLInputElement
  ).click();
  expect(engine().visible).toHaveLength(2);
  (
    root.querySelector('[data-facet-value="Ingeniería"]') as HTMLInputElement
  ).click();
  expect(engine().visible).toHaveLength(4);
  (
    root.querySelector(".explorer-filter-chips button") as HTMLButtonElement
  ).click();
  expect(engine().visible).toHaveLength(6);
  expect(root.querySelectorAll("[data-facet-column]:checked")).toHaveLength(0);
});
it("retains hidden selections in export, and searches values rather than UI labels", () => {
  const box = root.querySelector(".explorador-seleccion") as HTMLInputElement;
  box.click();
  const selected = engine().selected[0];
  const search = root.querySelector("[name=buscar]") as HTMLInputElement;
  search.value = "no coincidencias";
  search.dispatchEvent(new Event("input", { bubbles: true }));
  expect(engine().visible).toHaveLength(0);
  expect(engine().exportCSV()).toContain(selected[0]);
  expect(engine().exportCSV()).not.toContain("↗");
  expect(root.querySelector(".explorer-batch")?.textContent).toContain(
    "1 fuera del filtro",
  );
});
it("tears down and remounts without losing original form controls or duplicating menus", () => {
  engine().destroy();
  expect(root.querySelectorAll(".explorer-overview")).toHaveLength(0);
  expect(root.querySelectorAll("[data-columna]")).toHaveLength(3);
  (window as any).NotaExplorador.init(root);
  expect(root.querySelectorAll(".explorer-presentation")).toHaveLength(1);
  expect(engine().visible).toHaveLength(6);
});
it('reuses filtered records and selection across board, list and table views',()=>{
 const cell=root.querySelector('tbody td')!,id=cell.id;
 (root.querySelector('.explorador-seleccion') as HTMLInputElement).click();
 (root.querySelector('.explorer-presentation [data-layout=board]') as HTMLElement).click();
 expect(root.dataset.layout).toBe('board');
 expect((root.querySelector('[name=grupo]') as HTMLSelectElement).value).not.toBe('');
 expect(root.querySelectorAll('tbody')).toHaveLength(3);
 (root.querySelector('[data-facet-value="Producto"]') as HTMLInputElement).click();
 expect(engine().visible).toHaveLength(2);
 (root.querySelector('.explorer-presentation [data-layout=list]') as HTMLElement).click();
 expect(engine().visible).toHaveLength(2);expect(engine().selected).toHaveLength(1);
 (root.querySelector(".explorer-filter-chips button") as HTMLElement).click();
 expect(document.getElementById(id)).toBe(cell);
});

it('reorders original cells, hides by identity and exports in the chosen column order', () => {
  const sourceCell = root.querySelector('[data-cell-id$=":3"]')!;
  const identity = sourceCell.id;
  (root.querySelector('[aria-label="Mover Importe COP antes"]') as HTMLElement).click();
  expect([...root.querySelectorAll('thead th')].map(n => n.textContent?.trim().split(' ')[0])).toEqual(['Nombre', 'Equipo', 'Importe', 'Estado']);
  expect(document.getElementById(identity)).toBe(sourceCell);
  (root.querySelector('[data-columna="2"]') as HTMLInputElement).click();
  expect(sourceCell.hasAttribute('hidden')).toBe(false);
  expect(engine().exportCSV().split(/\r?\n/)[0]).toBe('"Nombre","Equipo","Importe COP"');
  const search = root.querySelector('[name=buscar]') as HTMLInputElement;
  search.value = 'Producto'; search.dispatchEvent(new Event('input', {bubbles:true}));
  expect(engine().visible).toHaveLength(2);
  engine().destroy();
  expect(root.querySelector('thead th:last-child')?.textContent).toContain('Importe COP');
});

it('restores column order and widths with a saved view', () => {
  const name = root.querySelector('[aria-label="Nombre de la vista"]') as HTMLInputElement;
  (root.querySelector('[aria-label="Mover Estado antes"]') as HTMLElement).click();
  const width = root.querySelector('[aria-label="Ancho de Estado"]') as HTMLInputElement;
  width.value = '260'; width.dispatchEvent(new Event('input', {bubbles:true}));
  name.value = 'Review layout';
  [...root.querySelectorAll('button')].find(b => b.textContent === 'Guardar vista')!.click();
  (root.querySelector('[aria-label="Mover Estado después"]') as HTMLElement).click();
  const view = root.querySelector('[aria-label="Vista guardada"]') as HTMLSelectElement;
  view.value = '0'; view.dispatchEvent(new Event('change', {bubbles:true}));
  expect(root.querySelectorAll('thead th')[1].textContent).toContain('Estado');
  expect((root.querySelectorAll('thead th')[1] as HTMLElement).style.width).toBe('260px');
  localStorage.clear();
});
