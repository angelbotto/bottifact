/* Shared reader shell. Hosts negotiate capabilities; document HTML never receives credentials. */
(() => {
  "use strict";
  if (window.BottifactReaderControls) return;
  window.BottifactReaderControls = { version: 1 };
  function mount() {
    if (document.querySelector(".bottifact-toolbar")) return;
    const bridge = window.BottifactReviewBridge;
    const appearance = document.querySelector("[data-apariencia-menu]");
    const review = document.querySelector(".revision-barra");
    if (!bridge && !appearance && !review) return;
    const make = (tag, text, cls) => {
      const e = document.createElement(tag);
      if (text) e.textContent = text;
      if (cls) e.className = cls;
      return e;
    };
    const icons = {
      review: "M21 11a8 8 0 0 1-8 8H5l-3 3V11a9 9 0 0 1 19 0Z",
      share: "M12 16V3m-4 4 4-4 4 4M5 12v8h14v-8",
      more: "M5 12h.01M12 12h.01M19 12h.01",
      note: "m15 4 5 5-10 10-6 1 1-6Z",
    };
    const style = make("style");
    style.dataset.bottifactControls = "";
    style.textContent = `
    .bottifact-toolbar{position:fixed;bottom:max(12px,env(safe-area-inset-bottom));left:0;right:0;width:max-content;margin-inline:auto;z-index:130;display:flex;align-items:center;gap:3px;padding:5px;border:1px solid var(--linea,#cfcac4);border-radius:14px;background:var(--papel,#fffaf5);color:var(--tinta,#241e19);box-shadow:0 4px 24px #0002;font:13px/1.45 var(--sans,system-ui)}
    .bottifact-toolbar>button,.bottifact-toolbar>details>summary,.bottifact-toolbar .apariencia-menu>summary{display:grid;place-items:center;width:44px;height:44px;min-width:44px;min-height:44px;padding:0;border:0;border-radius:9px;background:transparent;color:inherit;cursor:pointer;list-style:none;margin:0}
    .bottifact-toolbar svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}.bottifact-toolbar>details:last-of-type svg{stroke-width:4}
    .bottifact-toolbar button:hover,.bottifact-toolbar summary:hover{background:var(--panel,#eee8e1)}.bottifact-toolbar :focus-visible{outline:2px solid var(--foco,#a13f19);outline-offset:3px}
    .bottifact-toolbar>details,.bottifact-toolbar>.apariencia-menu{position:static;margin:0}.bottifact-toolbar summary::-webkit-details-marker{display:none}
    .bottifact-toolbar .bf-menu{position:absolute;bottom:62px;left:50%;transform:translateX(-50%);width:min(310px,calc(100vw - 24px));max-height:60vh;overflow:auto;background:var(--papel,#fffaf5);border:1px solid var(--linea,#cfcac4);border-radius:12px;box-shadow:0 8px 28px #0002;padding:8px;color:inherit}
    .bottifact-toolbar .bf-menu button{display:block;width:100%;text-align:left;padding:11px 12px;border:0;border-radius:6px;background:transparent;color:inherit;font:inherit;min-height:42px}.bottifact-toolbar .bf-menu p{margin:6px 12px;font-size:12px;color:var(--tinta-2,#625952)}
    .bottifact-toolbar [hidden]{display:none!important}.bottifact-controls-ready .revision-barra{display:none!important}.bottifact-controls-ready body{padding-bottom:calc(90px + env(safe-area-inset-bottom))}
    .bf-controls-status{position:fixed;bottom:84px;left:50%;transform:translateX(-50%);z-index:131;max-width:min(440px,calc(100vw - 32px));padding:8px 14px;border-radius:9px;background:var(--papel,#fffaf5);color:var(--tinta,#241e19);border:1px solid var(--linea,#cfcac4);font:13px/1.4 system-ui}.bf-controls-status:empty{display:none}
    .bottifact-controls-ready .revision-panel-v2[open]{position:fixed;inset:12px 12px 84px auto;margin:0;width:min(460px,calc(100vw - 24px));max-width:calc(100vw - 24px);height:auto;max-height:calc(100dvh - 100px);resize:horizontal;overflow:auto;border-radius:14px;padding:22px}.bottifact-controls-ready .revision-panel-v2::backdrop{background:#0002}
    .bf-theme-favorite{margin:8px 0!important;width:auto!important;font-size:12px!important;min-height:36px}.bf-theme-hint{font-size:12px;color:var(--tinta-2,#625952)}
    @media(max-width:540px){.bottifact-toolbar{bottom:max(10px,env(safe-area-inset-bottom));max-width:calc(100vw - 24px)}.bottifact-toolbar>button,.bottifact-toolbar>details>summary{width:44px;height:44px}.bottifact-controls-ready .revision-panel-v2[open]{inset:auto 8px max(76px,env(safe-area-inset-bottom)) 8px;width:calc(100vw - 16px);max-height:75dvh;resize:none}.bf-controls-status{bottom:80px}}
    @media print{.bottifact-toolbar,.bf-controls-status{display:none!important}}
    `;
    document.head.append(style);
    const bar = make("nav", null, "bottifact-toolbar");
    bar.setAttribute("aria-label", "Herramientas del artefacto");
    const status = make("p", null, "bf-controls-status");
    status.setAttribute("role", "status");
    let timer, remote;
    const say = (text) => {
      status.textContent = text;
      clearTimeout(timer);
      timer = setTimeout(() => (status.textContent = ""), 5500);
    };
    const svg = (name) => {
      const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      s.setAttribute("viewBox", "0 0 24 24");
      s.setAttribute("aria-hidden", "true");
      const p = document.createElementNS(s.namespaceURI, "path");
      p.setAttribute("d", icons[name]);
      s.append(p);
      return s;
    };
    const run = (fn) => async () => {
      try {
        await fn();
      } catch (e) {
        say(e.message || "No se completó la acción.");
      }
    };
    function button(label, icon, fn, parent = bar) {
      const b = make("button");
      b.type = "button";
      b.title = label;
      b.setAttribute("aria-label", label);
      b.append(svg(icon));
      b.addEventListener("click", run(fn));
      parent.append(b);
      return b;
    }
    function menu(label, icon) {
      const d = make("details"),
        s = make("summary");
      s.title = label;
      s.setAttribute("aria-label", label);
      s.append(svg(icon));
      const p = make("div", null, "bf-menu");
      d.append(s, p);
      bar.append(d);
      d.addEventListener("toggle", () => {
        if (d.open)
          for (const other of bar.querySelectorAll(":scope>details[open]"))
            if (other !== d) other.open = false;
      });
      return { d, p };
    }
    function action(menu, label, fn) {
      const b = make("button", label);
      b.type = "button";
      b.addEventListener(
        "click",
        run(async () => {
          menu.d.open = false;
          await fn();
        }),
      );
      menu.p.append(b);
      return b;
    }
    if (appearance) {
      bar.append(appearance);
      appearance.querySelector("summary").title = "Apariencia";
      const hint = make(
        "p",
        "Cambios para tu lectura. El diseño publicado se conserva.",
        "bf-theme-hint",
      );
      appearance.querySelector(".apariencia-panel")?.prepend(hint);
    }
    const reviewMenu = menu("Comentarios y notas", "review");
    const original = (label) =>
      review?.querySelector('[aria-label="' + label + '"]');
    const comment = action(reviewMenu, "Añadir comentario", () => {
      if (review) review.querySelector("button").click();
      else return bridge?.action("comment");
      say("Elige un punto del documento. Escape cancela.");
    });
    const note = action(reviewMenu, "Añadir nota personal", () => {
      if (review) original("Añadir nota privada")?.click();
      else return bridge?.action("note");
      say("Elige dónde dejar tu nota.");
    });
    action(reviewMenu, "Ver comentarios y notas", () => {
      if (review) review.querySelector("button:last-child").click();
      else return bridge?.action("review");
    });
    const bundle = action(reviewMenu, "Preparar contexto para IA", () => {
      if (bridge) return bridge.action("bundle");
      review?.querySelector("button:last-child")?.click();
      say("Selecciona los hilos y usa Copiar contexto en la revisión local.");
    });
    reviewMenu.p.append(
      make(
        "p",
        bridge
          ? "Los permisos del documento determinan quién participa."
          : "Revisión local en este navegador. Exporta para compartirla.",
      ),
    );
    button("Compartir", "share", async () => {
      if (bridge) return bridge.action("share");
      const canonical = document.querySelector("link[rel=canonical]")?.href;
      const url =
        canonical ||
        (/^https?:$/.test(location.protocol) ? location.href : null);
      if (!url) {
        say(
          "Publica este archivo en tu portal para obtener un enlace compartible.",
        );
        return;
      }
      try {
        await navigator.clipboard.writeText(url);
        say("Enlace copiado. Los permisos no cambian.");
      } catch {
        const d = make("dialog"),
          p = make("p", "Copia el enlace"),
          input = make("input"),
          close = make("button", "Cerrar");
        input.value = url;
        input.readOnly = true;
        input.setAttribute("aria-label", "Enlace");
        close.onclick = () => d.close();
        d.append(p, input, close);
        document.body.append(d);
        d.addEventListener("close", () => d.remove());
        d.showModal();
        input.select();
      }
    });
    const more = menu("Más opciones", "more");
    const manage = action(more, "Gestionar artefacto", () =>
      bridge?.action("manage"),
    );
    manage.hidden = true;
    if (bridge) {
      action(more, "Referencias y conexiones", () => bridge.action("related"));
      action(more, "Buscar artefactos", () => bridge.action("search"));
    }
    action(more, "Volver al inicio", () =>
      scrollTo({ top: 0, behavior: "instant" }),
    );
    if (!bridge) action(more, "Imprimir", () => print());
    document.body.append(bar, status);
    document.documentElement.classList.add("bottifact-controls-ready");
    document.addEventListener("pointerdown", (e) => {
      for (const d of bar.querySelectorAll(":scope>details[open]"))
        if (!d.contains(e.target)) d.open = false;
    });
    bar.addEventListener("keydown", (e) => {
      if (e.key === "Escape")
        for (const d of bar.querySelectorAll(":scope>details[open]")) {
          d.open = false;
          d.querySelector("summary").focus();
        }
    });
    let favorites = [];
    try {
      favorites = JSON.parse(
        localStorage.getItem("bottifact-theme-favorites") || "[]",
      );
    } catch {}
    function preference() {
      return {
        theme: window.NotaTemas?.get().family,
        mode: window.NotaTemas?.get().mode,
        typography: document.documentElement.dataset.estilo || "editorial",
        favorites,
        sound: window.NotaAudio?.preferred,
        volume: window.NotaAudio?.volume,
      };
    }
    let applied = false;
    function applyPreferences(p) {
      if (!p) return;
      if (p.theme && p.mode)
        window.NotaTemas?.set({ family: p.theme, mode: p.mode });
      const type = document.querySelector(
        '[data-elegir-estilo][value="' + (p.typography || "editorial") + '"]',
      );
      if (type) {
        type.checked = true;
        type.dispatchEvent(new Event("change", { bubbles: true }));
      }
      if (Array.isArray(p.favorites))
        favorites = p.favorites.filter((s) => typeof s === "string");
      window.NotaAudio?.configure?.({ preferred: p.sound, volume: p.volume });
      updateFavorite();
    }
    if (!Array.isArray(favorites)) favorites = [];
    let favoriteButton,
      favoriteOnly,
      onlyFavorites = false;
    function filterFavorites() {
      if (!appearance) return;
      for (const label of appearance.querySelectorAll("[data-tema-familia]"))
        if (
          onlyFavorites &&
          !favorites.includes(label.querySelector("[data-elegir-tema]")?.value)
        )
          label.hidden = true;
      if (onlyFavorites) {
        const count = [
          ...appearance.querySelectorAll("[data-tema-familia]"),
        ].filter((l) => !l.hidden).length;
        const status = appearance.querySelector("[data-temas-resultados]");
        if (status) status.textContent = count + " temas favoritos visibles";
      }
    }
    function updateFavorite() {
      if (!favoriteButton) return;
      const id = window.NotaTemas?.get().family;
      favoriteButton.textContent = favorites.includes(id)
        ? "★ Tema guardado en favoritos"
        : "☆ Guardar tema en favoritos";
      favoriteButton.setAttribute(
        "aria-pressed",
        String(favorites.includes(id)),
      );
      for (const label of appearance.querySelectorAll("[data-tema-familia]"))
        label.dataset.favorite = String(
          favorites.includes(label.querySelector("[data-elegir-tema]")?.value),
        );
      filterFavorites();
    }
    if (appearance) {
      favoriteButton = make("button", null, "bf-theme-favorite");
      favoriteButton.type = "button";
      const themePanel = appearance.querySelector(
        '[data-preferencia-panel="temas"]',
      );
      themePanel?.prepend(favoriteButton);
      favoriteOnly = make("button", "Sólo favoritos", "bf-theme-favorite");
      favoriteOnly.type = "button";
      favoriteOnly.setAttribute("aria-pressed", "false");
      themePanel?.prepend(favoriteOnly);
      favoriteOnly.addEventListener("click", () => {
        onlyFavorites = !onlyFavorites;
        favoriteOnly.setAttribute("aria-pressed", String(onlyFavorites));
        appearance
          .querySelector("[data-buscar-tema]")
          ?.dispatchEvent(new Event("input", { bubbles: true }));
        filterFavorites();
      });
      appearance.addEventListener("input", () =>
        queueMicrotask(filterFavorites),
      );
      appearance.addEventListener("change", () =>
        queueMicrotask(filterFavorites),
      );
      favoriteButton.addEventListener("click", () => {
        const id = window.NotaTemas?.get().family;
        if (!id) return;
        favorites = favorites.includes(id)
          ? favorites.filter((f) => f !== id)
          : [...favorites, id];
        try {
          localStorage.setItem(
            "bottifact-theme-favorites",
            JSON.stringify(favorites),
          );
        } catch {}
        updateFavorite();
        if (bridge)
          bridge.preferences(preference()).catch((e) => say(e.message));
      });
      updateFavorite();
    }
    if (bridge) {
      bridge.subscribe((value) => {
        remote = value;
        manage.hidden = !value.reader?.manage;
        comment.disabled = !value.permissions.comment && !!value.author;
        note.disabled = !value.verified;
        bundle.disabled = !value.verified;
        if (!applied && value.reader) {
          applyPreferences(value.reader.preferences);
          applied = true;
        }
      });
      bridge.controlsReady?.();
    }
    document.addEventListener("change", (e) => {
      if (!bar.contains(e.target)) return;
      updateFavorite();
      if (bridge && applied)
        bridge.preferences(preference()).catch((e) => say(e.message));
    });
    document.addEventListener("nota:tema", updateFavorite);
    // Sound toggles are buttons; commit after their own handlers update the preference.
    bar.addEventListener("click", (e) => {
      if (e.target.closest("[data-audio-global]") && bridge && applied)
        queueMicrotask(() => bridge.preferences(preference()).catch(() => {}));
    });
    window.BottifactReaderControls.get = () => ({
      connected: !!bridge,
      preferences: preference(),
      permissions: remote?.permissions,
    });
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", mount, { once: true });
  else mount();
})();
