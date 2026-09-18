import { beforeEach, afterEach, expect, it, vi } from "vitest";
import { readFileSync } from "node:fs";
const source = readFileSync(
  process.cwd() + "/packages/core/components/reader-controls.js",
  "utf8",
);
beforeEach(() => {
  document.body.replaceChildren();
  document.documentElement.className = "";
  delete (window as any).BottifactReaderControls;
  delete (window as any).BottifactReviewBridge;
});
afterEach(() => {
  document
    .querySelectorAll("[data-bottifact-controls]")
    .forEach((e) => e.remove());
});
it("renders one toolbar for hosted legacy markup and routes sharing to the host", () => {
  const action = vi.fn().mockResolvedValue({ ok: true }),
    subscribe = vi.fn(),
    ready = vi.fn();
  (window as any).BottifactReviewBridge = {
    action,
    subscribe,
    controlsReady: ready,
  };
  window.eval(source);
  document.dispatchEvent(new Event("DOMContentLoaded"));
  window.eval(source);
  document.dispatchEvent(new Event("DOMContentLoaded"));
  expect(document.querySelectorAll(".bottifact-toolbar")).toHaveLength(1);
  (document.querySelector('summary[aria-label="Compartir"]') as HTMLElement).click();
  ([...document.querySelectorAll('.bf-menu button')].find(b=>b.textContent==='Enlace y acceso') as HTMLElement).click();
  expect(action).toHaveBeenCalledWith("share");
  expect(ready).toHaveBeenCalledOnce();
});
it("keeps the existing appearance and review controls as the action owners", () => {
  document.body.innerHTML =
    '<details data-apariencia-menu><summary>Appearance</summary><div class="apariencia-panel"></div></details><div class="revision-barra"><button>Comment</button><button aria-label="Añadir nota privada">Note</button><button>List</button></div>';
  const appearance = document.querySelector("[data-apariencia-menu]"),
    note = document.querySelector('[aria-label="Añadir nota privada"]')!,
    click = vi.fn();
  note.addEventListener("click", click);
  window.eval(source);
  document.dispatchEvent(new Event("DOMContentLoaded"));
  expect(
    document.querySelector(".bottifact-toolbar [data-apariencia-menu]"),
  ).toBe(appearance);
  const addNote = [...document.querySelectorAll(".bf-menu button")].find(
    (b) => b.textContent === "Añadir nota personal",
  ) as HTMLButtonElement;
  addNote.click();
  expect(click).toHaveBeenCalledOnce();
});
it("offers direct point actions and tracks the active review tool", () => {
  document.body.innerHTML =
    '<div class="revision-barra"><button>Comment</button><button aria-label="Añadir nota privada">Note</button><button>List</button></div>';
  const click = vi.fn();
  document
    .querySelector(".revision-barra>button")!
    .addEventListener("click", click);
  window.eval(source);
  document.dispatchEvent(new Event("DOMContentLoaded"));
  const quick = document.querySelector(
    '.bottifact-toolbar>button[aria-label="Comentar en un punto"]',
  ) as HTMLButtonElement;
  quick.click();
  expect(click).toHaveBeenCalledOnce();
  document.dispatchEvent(
    new CustomEvent("bottifact:review-mode", {
      detail: { active: true, kind: "comment" },
    }),
  );
  expect(quick.getAttribute("aria-pressed")).toBe("true");
  document.dispatchEvent(
    new CustomEvent("bottifact:review-mode", {
      detail: { active: false, kind: "comment" },
    }),
  );
  expect(quick.getAttribute("aria-pressed")).toBe("false");
});
it("applies host permissions to both shortcuts and menu actions", () => {
  let receive: any;
  (window as any).BottifactReviewBridge = {
    action: vi.fn(),
    subscribe: (fn: any) => {
      receive = fn;
    },
    controlsReady: vi.fn(),
  };
  window.eval(source);
  document.dispatchEvent(new Event("DOMContentLoaded"));
  receive({
    author: "Reader",
    verified: true,
    permissions: { comment: false, edit: false },
    preferences: {},
  });
  expect(
    (
      document.querySelector(
        '[aria-label="Comentar en un punto"]',
      ) as HTMLButtonElement
    ).disabled,
  ).toBe(false);
  const note=[...document.querySelectorAll('.bf-menu button')].find(b=>b.textContent==='Añadir nota personal') as HTMLButtonElement;
  expect(note.disabled).toBe(false);

});
it("moves between tools with arrow keys and exposes keyboard tooltip text", async () => {
  vi.useFakeTimers();
  document.body.innerHTML =
    '<div class="revision-barra"><button>Comment</button><button>List</button></div>';
  window.eval(source);
  document.dispatchEvent(new Event("DOMContentLoaded"));
  const first = document.querySelector(
    ".bottifact-toolbar>button",
  ) as HTMLButtonElement;
  first.focus();
  await vi.advanceTimersByTimeAsync(1);
  expect(document.querySelector('[role="tooltip"]')?.textContent).toBe(
    "Comentar en un punto",
  );
  first.dispatchEvent(
    new KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true }),
  );
  expect(document.activeElement?.getAttribute("aria-label")).toBe(
    "Comentarios · 0 abiertos",
  );
  vi.useRealTimers();
});

it("shows the open-thread count and removes the duplicated note and generic more shortcuts",()=>{
 document.body.innerHTML='<div class="revision-barra"><button>Comment</button><button>3</button></div>';
 window.eval(source);document.dispatchEvent(new Event('DOMContentLoaded'));
 expect(document.querySelector('.bf-review-count')?.textContent).toBe('3');
 document.dispatchEvent(new CustomEvent('bottifact:review-count',{detail:{open:5,total:8}}));
 expect(document.querySelector('.bf-review-count')?.textContent).toBe('5');
 expect(document.querySelector('summary[aria-label="Más opciones"]')).toBeNull();
 expect(document.querySelector('.bottifact-toolbar>button[aria-label="Añadir nota privada"]')).toBeNull();
});
