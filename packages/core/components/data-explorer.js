/* Tabla local: filtros, selección, grupos, paginación y CSV. Conserva la fuente. */
(() => {
  "use strict";
  const instances = new WeakMap(),
    normal = (s) =>
      s
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();
  function init(root = document) {
    return [
      ...(root.matches?.("[data-explorador]") ? [root] : []),
      ...root.querySelectorAll("[data-explorador]"),
    ].map((el) => {
      if (instances.has(el)) return instances.get(el);
      const form = el.querySelector("form"),
        table = el.querySelector("table"),
        status = el.querySelector("[data-explorador-estado]"),
        initial = table?.tBodies[0],
        rows = [...(initial?.rows || [])],
        headers = [...(table?.tHead?.rows[0]?.cells || [])];
      if (
        !form ||
        !status ||
        !rows.length ||
        !headers.length ||
        headers.length > 16 ||
        rows.length > 2000 ||
        rows.some((r) => r.cells.length !== headers.length)
      )
        return null;
      const abort = new AbortController(),
        listen = (node, type, fn) =>
          node.addEventListener(type, fn, { signal: abort.signal }),
        make = (tag, text) => {
          const e = document.createElement(tag);
          if (text !== undefined) e.textContent = text;
          return e;
        },
        button = (label, fn) => {
          const b = make("button", label);
          b.type = "button";
          listen(b, "click", fn);
          return b;
        };
      const names = headers.map((h) =>
          (h.querySelector("summary") || h).textContent
            .replace(/[↕↑↓]/g, "")
            .trim(),
        ),
        values = rows.map((r) => [...r.cells].map((c) => c.textContent.trim())),
        raw = rows.map((r) =>
          [...r.cells].map((c) => c.dataset.valor ?? c.textContent.trim()),
        );
      const types = headers.map(
        (h, c) =>
          h.dataset.tipo ||
          (rows.every((r) => r.cells[c].hasAttribute("data-valor"))
            ? "numero"
            : "texto"),
      );
      if (
        types.some((t) => !["texto", "numero", "fecha"].includes(t)) ||
        raw.some((row) =>
          row.some(
            (v, c) =>
              (types[c] === "numero" &&
                v !== "" &&
                (!Number.isFinite(Number(v)) || Math.abs(Number(v)) > 1e12)) ||
              (types[c] === "fecha" &&
                v !== "" &&
                (!/^\d{4}-\d{2}-\d{2}$/.test(v) ||
                  !Number.isFinite(Date.parse(v)) ||
                  new Date(v).toISOString().slice(0, 10) !== v)),
          ),
        )
      )
        return null;
      rows.forEach((r, i) => {
        r.dataset.rowId ||= el.id + "-record-" + (i + 1);
        if (!r.id) r.id = r.dataset.rowId;
        [...r.cells].forEach((c, j) => {
          c.dataset.cellId = r.dataset.rowId + ":" + j;
          if (!c.id) c.id = r.dataset.rowId + "-cell-" + j;
        });
      });
      const previous = {
          status: status.textContent,
          sort: headers.map((h) => h.getAttribute("aria-sort")),
          hidden: rows.map((r) => [...r.cells].map((c) => c.hidden)),
          headers: headers.map((h) => h.hidden),
        },
        parts = [],
        selected = new Set(),
        collapsed = new Set();
      let sorts = [{ col: 0, dir: 1 }],
        page = 0,
        visible = [],
        pageRows = [],
        destroyed = false,
        renderAbort = new AbortController();
      const tools = make("div");
      tools.className = "explorador-utilidades";
      const advanced = make("details"),
        summary = make("summary", "Filtrar columna");
      advanced.className = "control-menu";
      const panel = make("div");
      panel.className = "control-panel";
      panel.tabIndex = 0;
      panel.setAttribute("role", "region");
      panel.setAttribute("aria-label", "Filtro por columna");
      const field = make("select"),
        match = make("input"),
        min = make("input"),
        max = make("input");
      field.setAttribute("aria-label", "Columna a filtrar");
      field.append(make("option", "Todas"));
      field.firstChild.value = "";
      names.forEach((n, c) => {
        const o = make("option", n);
        o.value = c;
        field.append(o);
      });
      match.placeholder = "Contiene…";
      match.setAttribute("aria-label", "Texto del filtro");
      min.type = max.type = "number";
      min.placeholder = "Desde";
      max.placeholder = "Hasta";
      min.setAttribute("aria-label", "Valor mínimo");
      max.setAttribute("aria-label", "Valor máximo");
      min.hidden = max.hidden = true;
      panel.append(field, match, min, max);
      advanced.append(summary, panel);
      const density = make("select");
      density.setAttribute("aria-label", "Densidad de filas");
      for (const [v, n] of [
        ["normal", "Espaciado cómodo"],
        ["compacta", "Espaciado compacto"],
      ]) {
        const o = make("option", n);
        o.value = v;
        density.append(o);
      }
      const selectAll = make("input");
      selectAll.type = "checkbox";
      selectAll.setAttribute("aria-label", "Seleccionar filas de esta página");
      const selectionLabel = make("label", "Seleccionar página ");
      selectionLabel.prepend(selectAll);
      const selectedCount = make("span", ""),
        csv = button("Exportar CSV", () => downloadCSV()),
        clear = button("Limpiar selección", () => {
          selected.clear();
          update();
        });
      tools.append(
        advanced,
        density,
        selectionLabel,
        selectedCount,
        clear,
        csv,
      );
      form.after(tools);
      window.NotaControles?.init(tools);
      const footer = make("div");
      footer.className = "explorador-paginacion";
      const prev = button("←", () => {
          page--;
          update();
        }),
        next = button("→", () => {
          page++;
          update();
        }),
        pageStatus = make("span"),
        size = make("select");
      prev.setAttribute("aria-label", "Página anterior de tabla");
      next.setAttribute("aria-label", "Página siguiente de tabla");
      size.setAttribute("aria-label", "Filas por página");
      for (const n of [10, 25, 50, 100]) {
        const o = make("option", n + " filas");
        o.value = n;
        size.append(o);
      }
      size.value = String(
        [10, 25, 50, 100].includes(Number(el.dataset.paginaTamano))
          ? Number(el.dataset.paginaTamano)
          : 25,
      );
      footer.append(pageStatus, prev, next, size);
      el.querySelector(".tabla-caja").after(footer);
      const model = window.BottifactTableModel;
      let query = model?.empty(),
        viewState = [],
        pinned = new Set();
      const key =
        "bottifact-table:" +
        (document.querySelector('meta[name="nota-documento"]')?.content ||
          location.pathname) +
        ":" +
        (el.id ||
          [...document.querySelectorAll("[data-explorador]")].indexOf(el));
      const filters = make("details"),
        filterBody = make("div"),
        join = make("select");
      filters.className = "control-menu";
      filterBody.className = "control-panel";
      filters.append(make("summary", "Condiciones"), filterBody);
      join.append(
        new Option("Todas las condiciones", "and"),
        new Option("Cualquier condición", "or"),
      );
      join.setAttribute("aria-label", "Combinar condiciones");
      filterBody.append(join);
      listen(join, "change", () => {
        query.join = join.value;
        resetPage();
      });
      function drawRules() {
        filterBody.querySelectorAll("[data-rule]").forEach((n) => n.remove());
        query.rules.forEach((rule, index) => {
          const row = make("div");
          row.dataset.rule = "";
          row.style.cssText =
            "display:flex;gap:6px;flex-wrap:wrap;margin-block:8px";
          const col = make("select"),
            op = make("select"),
            value = make("input"),
            upper = make("input");
          names.forEach((n, c) => col.append(new Option(n, String(c))));
          col.value = rule.column;
          col.setAttribute("aria-label", "Columna de condición " + (index + 1));
          for (const [v, n] of [
            ["contains", "Contiene"],
            ["eq", "Igual a"],
            ["in", "Uno de"],
            ["gte", "Desde"],
            ["lte", "Hasta"],
            ["between", "Entre"],
            ["empty", "Sin valor"],
          ])
            op.append(new Option(n, v));
          op.value = rule.operator;
          op.setAttribute("aria-label", "Operador de condición " + (index + 1));
          value.setAttribute("aria-label", "Valor de condición " + (index + 1));
          value.style.width = "130px";
          value.type =
            op.value === "in"
              ? "text"
              : types[Number(col.value)] === "numero"
                ? "number"
                : types[Number(col.value)] === "fecha"
                  ? "date"
                  : "text";
          value.value = Array.isArray(rule.value)
            ? rule.value.join(",")
            : (rule.value ?? "");
          value.hidden = op.value === "empty";
          upper.type = value.type;
          upper.style.width = "130px";
          upper.value = rule.upper ?? "";
          upper.hidden = op.value !== "between";
          upper.setAttribute("aria-label", "Límite superior " + (index + 1));
          listen(col, "change", () => {
            rule.column = col.value;
            rule.value = "";
            drawRules();
            resetPage();
          });
          listen(op, "change", () => {
            rule.operator = op.value;
            rule.value = "";
            drawRules();
            resetPage();
          });
          listen(value, "input", () => {
            rule.value =
              op.value === "in"
                ? value.value.split(",").map((v) => v.trim())
                : value.value;
            resetPage();
          });
          listen(upper, "input", () => {
            rule.upper = upper.value;
            resetPage();
          });
          row.append(
            col,
            op,
            value,
            upper,
            button("×", () => {
              query.rules.splice(index, 1);
              drawRules();
              resetPage();
            }),
          );
          filterBody.append(row);
        });
      }
      filterBody.append(
        button("Añadir condición", () => {
          if (query.rules.length < 12) {
            query.rules.push({ column: "0", operator: "contains", value: "" });
            drawRules();
          }
        }),
      );
      if (model) tools.prepend(filters);
      const views = make("details"),
        viewBody = make("div"),
        viewSelect = make("select"),
        viewName = make("input"),
        viewMessage = make("p");
      views.className = "control-menu";
      viewBody.className = "control-panel";
      viewName.placeholder = "Nombre de la vista";
      viewName.setAttribute("aria-label", "Nombre de la vista");
      viewSelect.setAttribute("aria-label", "Vista guardada");
      views.append(make("summary", "Vistas"), viewBody);
      viewBody.append(viewSelect, viewName);
      try {
        viewState = JSON.parse(localStorage.getItem(key) || "[]");
        if (!Array.isArray(viewState)) viewState = [];
      } catch {
        viewState = [];
      }
      function viewOptions() {
        viewSelect.replaceChildren(
          new Option("Vistas en este dispositivo", ""),
        );
        viewState.forEach((v, i) =>
          viewSelect.append(new Option(v.name, String(i))),
        );
      }
      viewOptions();
      viewBody.append(
        button("Guardar vista", () => {
          const name = viewName.value.trim().slice(0, 80);
          if (!name) return;
          const view = {
            name,
            query,
            sorts,
            group: form.elements.grupo?.value || "",
            search: form.elements.buscar?.value || "",
            state: form.elements.estado?.value || "",
            hidden: [
              ...form.querySelectorAll("[data-columna]:not(:checked)"),
            ].map((c) => c.dataset.columna),
            density: density.value,
            field: field.value,
            match: match.value,
            min: min.value,
            max: max.value,
          };
          try {
            const next = [
              ...viewState.filter((v) => v.name !== name),
              view,
            ].slice(-20);
            localStorage.setItem(key, JSON.stringify(next));
            viewState = JSON.parse(JSON.stringify(next));
            viewOptions();
            viewMessage.textContent =
              "Vista guardada sólo en este dispositivo.";
          } catch {
            viewMessage.textContent = "No se pudo guardar en este navegador.";
          }
        }),
        button("Eliminar vista", () => {
          if (viewSelect.value === "") return;
          const next = viewState.filter(
            (_, i) => i !== Number(viewSelect.value),
          );
          try {
            localStorage.setItem(key, JSON.stringify(next));
            viewState = next;
            viewOptions();
          } catch {
            viewMessage.textContent = "No se pudo eliminar.";
          }
        }),
        viewMessage,
      );
      listen(viewSelect, "change", () => {
        const v = viewState[Number(viewSelect.value)];
        if (viewSelect.value === "" || !v) return;
        query = JSON.parse(JSON.stringify(v.query || model.empty()));
        join.value = query.join;
        sorts = v.sorts || [];
        for (const [name, value] of [
          ["grupo", v.group],
          ["buscar", v.search],
          ["estado", v.state],
        ])
          if (form.elements[name]) form.elements[name].value = value || "";
        for (const c of form.querySelectorAll("[data-columna]"))
          c.checked = !(v.hidden || []).includes(c.dataset.columna);
        density.value = v.density || "normal";
        el.dataset.densidad = density.value;
        field.value = v.field || "";
        match.value = v.match || "";
        min.value = v.min || "";
        max.value = v.max || "";
        drawRules();
        resetPage();
      });
      if (model) tools.append(views);
      const layout = make("details"),
        layoutBody = make("div");
      layout.className = "control-menu";
      layoutBody.className = "control-panel";
      layout.append(make("summary", "Ajustar columnas"), layoutBody);
      headers.forEach((h, c) => {
        const line = make("label", names[c] + " "),
          pin = make("input"),
          width = make("input");
        pin.type = "checkbox";
        pin.setAttribute("aria-label", "Fijar " + names[c]);
        width.type = "range";
        width.min = "100";
        width.max = "480";
        width.value = "180";
        width.setAttribute("aria-label", "Ancho de " + names[c]);
        listen(width, "input", () => {
          [h, ...rows.map((r) => r.cells[c])].forEach((cell) => {
            cell.style.minWidth = width.value + "px";
            cell.style.width = width.value + "px";
          });
          positionColumns();
        });
        listen(pin, "change", () => {
          pin.checked ? pinned.add(c) : pinned.delete(c);
          positionColumns();
        });
        line.append(pin, width);
        layoutBody.append(line);
      });
      tools.append(layout);
      function positionColumns() {
        let left = 0;
        headers.forEach((h, c) => {
          const fixed = pinned.has(c);
          for (const cell of [h, ...rows.map((r) => r.cells[c])]) {
            cell.style.position = fixed ? "sticky" : "";
            cell.style.left = fixed ? left + "px" : "";
            cell.style.zIndex = fixed ? "2" : "";
            cell.style.background = fixed ? "var(--papel)" : "";
          }
          if (fixed && !h.hidden) left += h.getBoundingClientRect().width;
        });
      }
      const detail = make("dialog");
      detail.className = "explorador-detalle";
      detail.style.cssText =
        "max-width:min(460px,calc(100vw - 32px));max-height:80vh;overflow:auto;background:var(--papel);color:var(--tinta);padding:24px;border:1px solid var(--linea)";
      detail.setAttribute("aria-label", "Detalle del registro");
      document.body.append(detail);
      rows.forEach((row, i) => {
        const inspect = button("↗", () => {
          detail.replaceChildren(
            make("h3", "Registro " + row.dataset.rowId),
            button("Cerrar", () => detail.close()),
          );
          const dl = make("dl");
          names.forEach((name, c) =>
            dl.append(make("dt", name), make("dd", values[i][c])),
          );
          detail.append(dl);
          detail.showModal();
        });
        inspect.setAttribute("aria-label", "Ver detalle de " + values[i][0]);
        inspect.className = "explorador-inspeccionar";
        row.cells[row.cells.length - 1].append(inspect);
      });
      const boxes = rows.map((r, i) => {
        const c = make("input");
        c.type = "checkbox";
        c.className = "explorador-seleccion";
        c.setAttribute("aria-label", "Seleccionar " + values[i][0]);
        r.cells[0].prepend(c);
        listen(c, "change", () => {
          c.checked ? selected.add(i) : selected.delete(i);
          update();
        });
        return c;
      });
      const colValue = (i, c) =>
        raw[i][c] === ""
          ? null
          : types[c] === "numero"
            ? Number(raw[i][c])
            : types[c] === "fecha"
              ? Date.parse(raw[i][c])
              : values[i][c];
      function update() {
        if (destroyed) return;
        renderAbort.abort();
        renderAbort = new AbortController();
        parts.splice(0).forEach((p) => p.remove());
        initial.remove();
        rows.forEach((r) => (r.hidden = false));
        const words = normal(form.elements.buscar?.value || "")
            .trim()
            .split(/\s+/),
          state = form.elements.estado?.value || "",
          group = form.elements.grupo?.value || "",
          fc = field.value === "" ? null : Number(field.value),
          numeric = fc !== null && types[fc] !== "texto";
        min.hidden = max.hidden = !numeric;
        match.hidden = numeric;
        min.type = max.type =
          fc !== null && types[fc] === "fecha" ? "date" : "number";
        const stateCol = Number(el.dataset.columnaEstado ?? 2),
          groupCol = group === "" ? null : Number(group);
        visible = rows
          .map((r, i) => i)
          .filter(
            (i) =>
              (!state || values[i][stateCol] === state) &&
              words.every((w) => normal(values[i].join(" ")).includes(w)) &&
              (numeric
                ? (raw[i][fc] !== "" ||
                    (min.value === "" && max.value === "")) &&
                  (min.value === "" ||
                    colValue(i, fc) >=
                      (types[fc] === "fecha"
                        ? Date.parse(min.value)
                        : Number(min.value))) &&
                  (max.value === "" ||
                    colValue(i, fc) <=
                      (types[fc] === "fecha"
                        ? Date.parse(max.value)
                        : Number(max.value)))
                : normal(
                    fc === null ? values[i].join(" ") : values[i][fc],
                  ).includes(normal(match.value))),
          );
        if (model && query)
          visible = model.query(
            visible,
            {
              ...query,
              sort: sorts.map((s) => ({
                column: String(s.col),
                direction: s.dir === 1 ? "asc" : "desc",
              })),
            },
            (i) =>
              Object.fromEntries(
                values[i].map((v, c) => [
                  String(c),
                  raw[i][c] === ""
                    ? null
                    : types[c] === "numero"
                      ? Number(raw[i][c])
                      : types[c] === "fecha"
                        ? raw[i][c]
                        : v,
                ]),
              ),
          );
        if (!model)
          visible.sort((a, b) => {
            for (const s of sorts) {
              const av = colValue(a, s.col),
                bv = colValue(b, s.col),
                c =
                  types[s.col] === "texto"
                    ? av.localeCompare(bv, "es", {
                        numeric: true,
                        sensitivity: "base",
                      })
                    : av - bv;
              if (c) return s.dir * c;
            }
            return a - b;
          });
        const pages = Math.max(
          1,
          Math.ceil(visible.length / Number(size.value)),
        );
        page = Math.max(0, Math.min(page, pages - 1));
        pageRows = visible.slice(
          page * Number(size.value),
          (page + 1) * Number(size.value),
        );
        const hidden = new Set(
          [...form.querySelectorAll("[data-columna]:not(:checked)")].map((e) =>
            Number(e.dataset.columna),
          ),
        );
        if (hidden.size >= headers.length) {
          hidden.delete(0);
          const box = form.querySelector('[data-columna="0"]');
          if (box) box.checked = true;
        }
        headers.forEach((h, c) => (h.hidden = hidden.has(c)));
        rows.forEach((r, i) => {
          [...r.cells].forEach((c, j) => (c.hidden = hidden.has(j)));
          r.setAttribute("aria-selected", String(selected.has(i)));
          boxes[i].checked = selected.has(i);
        });
        const groups = new Map();
        pageRows.forEach((i) => {
          const key = groupCol === null ? "" : (values[i][groupCol] ?? "");
          if (!groups.has(key)) groups.set(key, []);
          groups.get(key).push(i);
        });
        if (!visible.length) {
          const body = make("tbody"),
            tr = body.insertRow(),
            td = tr.insertCell();
          td.colSpan = headers.length - hidden.size;
          td.textContent =
            "No hay resultados. Limpia los filtros para volver a ver los registros.";
          table.append(body);
          parts.push(body);
        }
        for (const [name, items] of groups) {
          const body = make("tbody");
          if (groupCol !== null) {
            const tr = body.insertRow(),
              th = make("th");
            th.scope = "rowgroup";
            th.colSpan = headers.length - hidden.size;
            th.className = "tabla-grupo";
            const b = make(
              "button",
              (collapsed.has(name) ? "▸ " : "▾ ") +
                name +
                " · " +
                items.length +
                " en esta página",
            );
            b.type = "button";
            b.addEventListener(
              "click",
              () => {
                collapsed.has(name)
                  ? collapsed.delete(name)
                  : collapsed.add(name);
                update();
              },
              { signal: renderAbort.signal },
            );
            b.setAttribute("aria-expanded", String(!collapsed.has(name)));
            th.append(b);
            tr.append(th);
          }
          items.forEach((i) => {
            rows[i].hidden = groupCol !== null && collapsed.has(name);
            body.append(rows[i]);
          });
          table.append(body);
          parts.push(body);
        }
        const totalCol = Number(el.dataset.columnaTotal ?? 3),
          hasTotal = types[totalCol] === "numero",
          total = hasTotal
            ? visible.reduce((n, i) => n + Number(raw[i][totalCol]), 0)
            : 0;
        status.textContent =
          visible.length +
          " de " +
          rows.length +
          " registros" +
          (hasTotal
            ? " · " +
              total.toLocaleString("es-CO") +
              " " +
              (el.dataset.unidad || "COP") +
              " en la vista filtrada."
            : ".") +
          (sorts.length > 1
            ? " Orden: " + sorts.map((s) => names[s.col]).join(" → ")
            : "");
        headers.forEach((h, c) => {
          const s = sorts.find((s) => s.col === c);
          h.setAttribute(
            "aria-sort",
            sorts[0]?.col === c
              ? sorts[0].dir === 1
                ? "ascending"
                : "descending"
              : "none",
          );
          const hint = h.querySelector("[data-indicador-orden]");
          if (hint) hint.textContent = s ? (s.dir === 1 ? "↑" : "↓") : "↕";
        });
        positionColumns();
        selectedCount.textContent =
          selected.size +
          " seleccionados · " +
          [...selected].filter((i) => !visible.includes(i)).length +
          " fuera del filtro";
        clear.disabled = !selected.size;
        csv.textContent = selected.size
          ? "Exportar selección (" + selected.size + ")"
          : "Exportar vista";
        selectAll.checked =
          !!pageRows.length && pageRows.every((i) => selected.has(i));
        selectAll.indeterminate =
          pageRows.some((i) => selected.has(i)) && !selectAll.checked;
        pageStatus.textContent = "Página " + (page + 1) + " de " + pages;
        prev.disabled = page === 0;
        next.disabled = page === pages - 1;
        const count = form.querySelector("[data-filtros-cuenta]");
        if (count) count.textContent = state ? "1 · " : "";
      }
      function exportCSV() {
        const indices = selected.size
          ? rows.map((_, i) => i).filter((i) => selected.has(i))
          : visible;
        const columns = headers
          .map((_, i) => i)
          .filter((c) => !headers[c].hidden);
        const safe = (v, numeric = false) =>
          '"' +
          (!numeric && /^[\s]*[=+@\-]/.test(v) ? "'" + v : v).replaceAll(
            '"',
            '""',
          ) +
          '"';
        return [
          columns.map((c) => safe(names[c])).join(","),
          ...indices.map((i) =>
            columns
              .map((c) =>
                safe(
                  types[c] === "numero"
                    ? String(Number(raw[i][c]))
                    : values[i][c],
                  types[c] === "numero",
                ),
              )
              .join(","),
          ),
        ].join("\r\n");
      }
      function downloadCSV() {
        const url = URL.createObjectURL(
            new Blob(["\ufeff" + exportCSV()], {
              type: "text/csv;charset=utf-8",
            }),
          ),
          a = make("a");
        a.href = url;
        a.download = "tabla.csv";
        a.click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
      }
      const resetPage = () => {
        page = 0;
        collapsed.clear();
        update();
      };
      listen(form, "input", resetPage);
      listen(form, "change", resetPage);
      listen(form, "submit", (e) => e.preventDefault());
      listen(form, "reset", () =>
        queueMicrotask(() => {
          if (destroyed) return;
          sorts = [{ col: 0, dir: 1 }];
          if (model) {
            query = model.empty();
            join.value = "and";
            drawRules();
          }
          field.value = match.value = min.value = max.value = "";
          resetPage();
        }),
      );
      for (const input of [field, match, min, max, size])
        listen(input, "input", resetPage);
      listen(field, "change", () => {
        match.value = min.value = max.value = "";
        resetPage();
      });
      listen(density, "change", () => (el.dataset.densidad = density.value));
      listen(selectAll, "change", () => {
        pageRows.forEach((i) =>
          selectAll.checked ? selected.add(i) : selected.delete(i),
        );
        update();
      });
      el.querySelectorAll("[data-orden-col]").forEach((b) =>
        listen(b, "click", (e) => {
          const c = Number(b.dataset.ordenCol),
            requested = Number(b.dataset.direccion) || 0,
            dir =
              b.parentElement === headers[c] && sorts[0]?.col === c
                ? -sorts[0].dir
                : requested;
          if (c < 0 || c >= headers.length) return;
          sorts =
            dir === 0
              ? []
              : e.shiftKey
                ? [...sorts.filter((s) => s.col !== c), { col: c, dir }]
                : [{ col: c, dir }];
          resetPage();
        }),
      );
      listen(window, "beforeprint", () => {
        parts.splice(0).forEach((p) => p.remove());
        headers.forEach((h) => (h.hidden = false));
        rows.forEach((r) => {
          r.hidden = false;
          [...r.cells].forEach((c) => (c.hidden = false));
          initial.append(r);
        });
        table.append(initial);
      });
      listen(window, "afterprint", update);
      const instance = {
        update,
        exportCSV,
        get selected() {
          return [...selected].map((i) => values[i]);
        },
        get visible() {
          return visible.map((i) => values[i]);
        },
        destroy() {
          destroyed = true;
          detail.remove();
          el.querySelectorAll(".explorador-inspeccionar").forEach((b) =>
            b.remove(),
          );
          abort.abort();
          renderAbort.abort();
          parts.forEach((p) => p.remove());
          boxes.forEach((b) => b.remove());
          rows.forEach((r, i) => {
            r.hidden = false;
            r.removeAttribute("aria-selected");
            [...r.cells].forEach((c, j) => (c.hidden = previous.hidden[i][j]));
            initial.append(r);
          });
          headers.forEach((h, i) => {
            h.hidden = previous.headers[i];
            previous.sort[i] === null
              ? h.removeAttribute("aria-sort")
              : h.setAttribute("aria-sort", previous.sort[i]);
          });
          table.append(initial);
          tools
            .querySelectorAll(".control-menu")
            .forEach((m) => window.NotaControles?.get(m)?.destroy());
          tools.remove();
          footer.remove();
          delete el.dataset.densidad;
          status.textContent = previous.status;
          instances.delete(el);
        },
      };
      instances.set(el, instance);
      update();
      return instance;
    });
  }
  window.NotaExplorador = { init, get: (el) => instances.get(el) };
  init();
})();
