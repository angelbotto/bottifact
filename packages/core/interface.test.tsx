import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
const source = readFileSync(
  process.cwd() + "/packages/core/components/interface.js",
  "utf8",
);
const ui = () => (window as any).BottifactUI;
beforeEach(() => {
  document.body.replaceChildren();
  delete (window as any).BottifactUI;
});
afterEach(() => {
  document
    .querySelectorAll("[data-bottifact-interface]")
    .forEach((n) => n.remove());
});
it("preserves a live counter and its event handlers without duplicating icons", () => {
  window.eval(source);
  const button = document.createElement("button"),
    counter = document.createElement("span"),
    click = vi.fn();
  counter.textContent = "3";
  button.append("Comments ", counter);
  counter.addEventListener("click", click);
  ui().decorate(button, "comment");
  ui().decorate(button, "comment");
  counter.click();
  expect(button.textContent).toBe("Comments 3");
  expect(button.querySelectorAll("svg")).toHaveLength(1);
  expect(button.contains(counter)).toBe(true);
  expect(click).toHaveBeenCalledOnce();
});
it("keeps icon-only controls named and unavailable controls hidden", () => {
  window.eval(source);
  document.dispatchEvent(new Event("DOMContentLoaded"));
  const button = document.createElement("button");
  button.textContent = "Close preview";
  button.hidden = true;
  document.body.append(button);
  ui().decorate(button, "close", true);
  expect(button.getAttribute("aria-label")).toBe("Close preview");
  expect(button.title).toBe("Close preview");
  expect(button.querySelector("svg")?.getAttribute("aria-hidden")).toBe("true");
  expect(getComputedStyle(button).display).toBe("none");
});
it("uses the external account stylesheet without injecting inline styles under CSP", () => {
  const link = document.createElement("link");
  link.dataset.bottifactInterface = "";
  document.head.append(link);
  window.eval(source);
  document.dispatchEvent(new Event("DOMContentLoaded"));
  expect(document.querySelector("style[data-bottifact-interface]")).toBeNull();
});
