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
      comment: "M21 11a8 8 0 0 1-8 8H5l-3 3V11a9 9 0 0 1 19 0Z",
      review: "M21 11a8 8 0 0 1-8 8H5l-3 3V11a9 9 0 0 1 19 0Z",
      share: "M12 16V3m-4 4 4-4 4 4M5 12v8h14v-8",
      more: "M5 12h.01M12 12h.01M19 12h.01",
      note: "m15 4 5 5-10 10-6 1 1-6Z",
    };
    const style = make("style");
    style.dataset.bottifactControls = "";
    style.textContent = `
    .bottifact-toolbar{position:fixed;bottom:max(16px,env(safe-area-inset-bottom));left:0;right:0;width:max-content;margin-inline:auto;z-index:130;display:flex;align-items:center;gap:3px;padding:7px;border:1px solid color-mix(in srgb,var(--tinta,#252322) 13%,transparent);border-radius:17px;background:var(--papel,#faf9f7);color:var(--tinta,#252322);box-shadow:0 2px 5px #00000009,0 12px 32px #00000014,0 0 0 1px color-mix(in srgb,var(--papel,#faf9f7) 70%,transparent) inset;font:13px/1.45 var(--sans,system-ui)}
    .bottifact-toolbar>button,.bottifact-toolbar>details>summary,.bottifact-toolbar .apariencia-menu>summary{position:relative;display:grid;place-items:center;width:40px;height:40px;min-width:40px;min-height:40px;padding:0;border:0;border-radius:10px;background:transparent;color:var(--tinta-2,#625f5a);cursor:pointer;list-style:none;margin:0;box-shadow:none}
    .bottifact-toolbar svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:1.65;stroke-linecap:round;stroke-linejoin:round}
    .bottifact-toolbar .bf-dock-divider{width:1px;height:22px;margin-inline:4px;background:var(--linea,#d8d5ce)}
    .bottifact-toolbar>details[open]>summary,.bottifact-toolbar>button[aria-pressed=true]{color:var(--foco,#6865c8);background:color-mix(in srgb,var(--foco,#6865c8) 10%,var(--papel,#faf9f7))}
    .bottifact-toolbar>button:disabled{opacity:.38;cursor:not-allowed}
    @media(hover:hover){.bottifact-toolbar>button:hover:not(:disabled),.bottifact-toolbar>details>summary:hover{background:var(--panel,#edeae5);color:var(--tinta,#252322)}}
    .bottifact-toolbar :focus-visible{outline:2px solid var(--foco,#6865c8);outline-offset:3px}
    .bottifact-toolbar>details,.bottifact-toolbar>.apariencia-menu{position:static;margin:0}.bottifact-toolbar summary::-webkit-details-marker{display:none}
    .bottifact-toolbar .bf-menu{position:absolute;bottom:65px;left:50%;transform:translateX(-50%);width:min(300px,calc(100vw - 24px));max-height:min(60dvh,480px);overflow:auto;background:var(--papel,#faf9f7);border:1px solid var(--linea,#d8d5ce);border-radius:13px;box-shadow:0 4px 8px #00000008,0 16px 48px #0000001c;padding:6px;color:inherit}
    .bottifact-toolbar .bf-menu button{display:flex;width:100%;align-items:center;justify-content:flex-start;gap:10px;text-align:left;padding:10px 11px;border:0;border-radius:7px;background:transparent;color:inherit;font:inherit;min-height:38px;box-shadow:none}
    .bottifact-toolbar .bf-menu button:hover:not(:disabled){background:var(--panel,#edeae5)}.bottifact-toolbar .bf-menu button:disabled{opacity:.4;cursor:not-allowed}
    .bottifact-toolbar .bf-menu button svg{width:16px;height:16px;color:var(--tinta-2,#625f5a)}.bottifact-toolbar .bf-menu p{margin:8px 11px;font-size:11px;line-height:1.5;color:var(--tinta-2,#625f5a)}
    .bottifact-toolbar .bf-menu-heading{font-size:11px;font-weight:600;color:var(--tinta-2,#625f5a);padding:8px 11px 5px}
    .bottifact-toolbar [hidden]{display:none!important}.bottifact-controls-ready .revision-barra{display:none!important}.bottifact-controls-ready body{padding-bottom:calc(96px + env(safe-area-inset-bottom))}
    .bf-dock-tooltip{position:fixed;z-index:160;max-width:calc(100vw - 24px);pointer-events:none;border-radius:7px;padding:7px 10px;background:var(--tinta,#252322);color:var(--papel,#faf9f7);font:500 12px/1.3 var(--sans,system-ui);box-shadow:0 3px 12px #0002;white-space:nowrap}
    .bf-controls-status{position:fixed;bottom:88px;left:50%;transform:translateX(-50%);z-index:131;max-width:min(440px,calc(100vw - 32px));padding:10px 14px;border-radius:10px;background:var(--papel,#faf9f7);color:var(--tinta,#252322);border:1px solid var(--linea,#d8d5ce);box-shadow:0 3px 16px #0001;font:13px/1.4 var(--sans,system-ui)}.bf-controls-status:empty{display:none}
    .bottifact-controls-ready .revision-panel-v2[open]{position:fixed;inset:12px 12px 90px auto;margin:0;width:min(460px,calc(100vw - 24px));max-width:calc(100vw - 24px);height:auto;max-height:calc(100dvh - 102px);resize:horizontal;overflow:auto;border-radius:16px;padding:22px;border-color:var(--linea);box-shadow:0 16px 64px #0002}.bottifact-controls-ready .revision-panel-v2::backdrop{background:#0002}
    .bf-theme-favorite{margin:8px 0!important;width:auto!important;font-size:12px!important;min-height:34px;border:0!important;background:transparent!important}.bf-theme-hint{font-size:12px;color:var(--tinta-2,#625f5a)}
    @media(prefers-reduced-motion:no-preference){.bottifact-toolbar>button,.bottifact-toolbar>details>summary{transition:background-color 120ms ease-out,color 120ms ease-out}.bottifact-toolbar>button:active:not(:disabled),.bottifact-toolbar>details>summary:active{transform:scale(.95)}}
    @media(max-width:540px){.bottifact-toolbar{bottom:max(10px,env(safe-area-inset-bottom));max-width:calc(100vw - 16px);padding:5px;gap:0;border-radius:16px}.bottifact-toolbar>button,.bottifact-toolbar>details>summary,.bottifact-toolbar .apariencia-menu>summary{width:44px;height:44px;min-width:44px}.bottifact-toolbar .bf-dock-divider{margin-inline:2px;height:20px}.bottifact-controls-ready .revision-panel-v2[open]{inset:auto 8px max(80px,env(safe-area-inset-bottom)) 8px;width:calc(100vw - 16px);max-height:75dvh;resize:none}.bf-controls-status{bottom:80px}}
    .bottifact-toolbar>details>summary,.bottifact-toolbar .apariencia-menu>summary{width:auto;min-width:88px;height:48px;padding:5px 10px;display:flex;flex-direction:column;gap:3px}
    .bf-tool-label{font:500 10px/1.2 var(--sans,system-ui);white-space:nowrap}
    .bottifact-toolbar>details>summary.bf-tool-active{color:var(--foco,#6865c8);background:var(--panel,#edeae5)}
    .bottifact-toolbar [data-review-tool]>summary .bf-review-count{top:1px;right:22px}
    @media(max-width:360px){.bottifact-toolbar>details>summary,.bottifact-toolbar .apariencia-menu>summary{min-width:84px;padding-inline:6px}}
    @media print{.bottifact-toolbar,.bf-controls-status,.bf-dock-tooltip{display:none!important}}
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
      if (window.BottifactUI) return window.BottifactUI.icon(name);
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
    function menu(label, icon) {
      const d = make("details"),
        s = make("summary");
      s.dataset.tooltip = label;
      s.setAttribute("aria-label", label);
      s.append(svg(icon));
      const p = make("div", null, "bf-menu");
      p.append(make("div", label, "bf-menu-heading"));
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
      const actionIcons = {
        "Añadir comentario": "comment",
        "Añadir nota personal": "note",
        "Ver comentarios y notas": "review",
        "Preparar contexto para IA": "copy",
        "Gestionar artefacto": "settings",
        "Referencias y conexiones": "graph",
        "Buscar artefactos": "search",
        "Volver al inicio": "up",
        Imprimir: "print",
      };
      window.BottifactUI?.decorate(b, actionIcons[label] || "arrow");
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
    const reviewMenu = menu("Comentarios", "comment");
    reviewMenu.d.dataset.reviewTool = "";
    document.addEventListener("bottifact:review-mode", (event) => {
      reviewMenu.d.querySelector("summary").classList.toggle("bf-tool-active", event.detail.active);
      if (!event.detail.active) say("");
    });
    const reviewCount=make("span", "0", "bf-review-count");
    reviewMenu.d.querySelector("summary").append(reviewCount);
    function updateCount(count){
      reviewCount.textContent=String(count);
      const label="Comentarios · "+count+" abiertos";
      reviewMenu.d.querySelector("summary").setAttribute("aria-label",label);
      reviewMenu.d.querySelector("summary").dataset.tooltip=label;
    }
    updateCount(Number(review?.querySelector("button:last-child")?.textContent)||0);
    document.addEventListener("bottifact:review-count",e=>updateCount(e.detail.open));
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
    const shareMenu=menu("Compartir", "share");
    action(shareMenu, "Enlace y acceso", async () => {
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
    const manage = action(shareMenu, "Gestionar artefacto", () => bridge?.action("manage"));
    manage.hidden = true;
    if (bridge) {
      action(reviewMenu, "Referencias y conexiones", () => bridge.action("related"));
      action(reviewMenu, "Buscar en mi biblioteca", () => bridge.action("search"));
    } else action(shareMenu, "Imprimir o guardar PDF", () => print());
    if (appearance) {
      bar.append(appearance);
      const trigger = appearance.querySelector("summary");
      trigger.removeAttribute("title");
      trigger.dataset.tooltip = "Preferencias";
      trigger.setAttribute("aria-label", "Preferencias");
      if (window.BottifactUI) trigger.replaceChildren(svg("appearance"));
    }
    for (const trigger of bar.querySelectorAll(":scope>details>summary")) {
      trigger.append(make("span", trigger.getAttribute("aria-label").split(" · ")[0], "bf-tool-label"));
    }
    document.body.append(bar, status);
    const tooltip = make("div", null, "bf-dock-tooltip");
    tooltip.id = "bf-dock-tooltip";
    tooltip.setAttribute("role", "tooltip");
    tooltip.hidden = true;
    document.body.append(tooltip);
    let tipTimer,
      tipTarget,
      recentTip = 0;
    const hideTip = () => {
      clearTimeout(tipTimer);
      tooltip.hidden = true;
      tipTarget?.removeAttribute("aria-describedby");
      tipTarget = null;
    };
    const showTip = (target, immediate = false) => {
      hideTip();
      if (!target?.dataset.tooltip) return;
      tipTimer = setTimeout(
        () => {
          if (!target.isConnected) return;
          tipTarget = target;
          tooltip.textContent = target.dataset.tooltip;
          tooltip.hidden = false;
          target.setAttribute("aria-describedby", tooltip.id);
          const r = target.getBoundingClientRect(),
            t = tooltip.getBoundingClientRect();
          tooltip.style.left =
            Math.max(
              12,
              Math.min(
                innerWidth - t.width - 12,
                r.left + r.width / 2 - t.width / 2,
              ),
            ) + "px";
          tooltip.style.top = Math.max(8, r.top - t.height - 16) + "px";
          recentTip = Date.now();
        },
        immediate || Date.now() - recentTip < 700 ? 0 : 350,
      );
    };
    bar.addEventListener("pointerover", (e) => {
      if (e.pointerType === "touch") return;
      const target = e.target.closest("[data-tooltip]");
      if (target && !target.contains(e.relatedTarget)) showTip(target);
    });
    bar.addEventListener("pointerout", (e) => {
      const target = e.target.closest("[data-tooltip]");
      if (target && !target.contains(e.relatedTarget)) hideTip();
    });
    bar.addEventListener("focusin", (e) =>
      showTip(e.target.closest("[data-tooltip]"), true),
    );
    bar.addEventListener("focusout", hideTip);
    bar.addEventListener("pointerdown", hideTip);
    window.addEventListener("resize", hideTip);
    bar.addEventListener("keydown", (e) => {
      if (e.key === "Escape") hideTip();
      const controls = [
        ...bar.querySelectorAll(":scope>button,:scope>details>summary"),
      ].filter((b) => !b.disabled && !b.hidden);
      const index = controls.indexOf(e.target);
      if (index < 0) return;
      if (["ArrowLeft", "ArrowRight", "Home", "End"].includes(e.key)) {
        e.preventDefault();
        const next =
          e.key === "Home"
            ? 0
            : e.key === "End"
              ? controls.length - 1
              : (index + (e.key === "ArrowRight" ? 1 : -1) + controls.length) %
                controls.length;
        controls[next].focus();
      }
    });
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
      const projectAppearance=document.querySelector('meta[name="margen-theme-policy"]')?.content==="project";
      if (!projectAppearance && p.theme && p.mode)
        window.NotaTemas?.set({ family: p.theme, mode: p.mode });
      const type = document.querySelector(
        '[data-elegir-estilo][value="' + (p.typography || "editorial") + '"]',
      );
      if (type && !projectAppearance) {
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
        ? "Tema guardado"
        : "Guardar tema";
      window.BottifactUI?.decorate(favoriteButton, "star");
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
      favoriteOnly = make("button", "Favoritos", "bf-theme-favorite");
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
        // Legacy documents can use the host review panel without a local review module.
        if (Array.isArray(value.snapshot?.events)) {
          const events=[...value.snapshot.events].sort((a,b)=>a.time-b.time||String(a.id).localeCompare(String(b.id)));
          const threads=new Map(events.filter(e=>e.kind==="create").map(e=>[e.thread,{resolved:false,deleted:false}]));
          for(const event of events){const thread=threads.get(event.thread);if(!thread)continue;if(event.kind==="resolve")thread.resolved=event.resolved;if(event.kind==="delete")thread.deleted=true;}
          updateCount([...threads.values()].filter(t=>!t.resolved&&!t.deleted).length);
        }
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
