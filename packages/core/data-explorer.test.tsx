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
