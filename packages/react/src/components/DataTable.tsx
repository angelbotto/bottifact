import {
  Fragment,
  useId,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
  type CSSProperties,
} from "react";
import {
  useTable,
  tableFeatures,
  columnVisibilityFeature,
  columnOrderingFeature,
  rowSelectionFeature,
  type RowData,
} from "@tanstack/react-table";
import {
  emptyTableQuery,
  queryTableRows,
  tableCSV,
  type TableQuery,
} from "@bottifact/core";
import { TablePopover } from "./ui/popover.js";
import { ButtonGroup } from "./ui/button-group.js";
import { ControlIcon } from "./ui/icon.js";
import { FilterBuilder } from "./FilterBuilder.js";
import { Inspector } from "./Inspector.js";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "./ui/table.js";
export interface Column<Row> {
  id: string;
  header: string;
  value: (row: Row) => string | number | null;
  render?: (row: Row) => ReactNode;
  sortable?: boolean;
  type?: "text" | "number" | "date";
  aggregate?: "sum" | "mean";
  /** Detail-only fields stay in the inspector on narrow record layouts. */
  mobile?: "primary" | "visible" | "detail";
  width?: number;
}
export interface DataTableProps<Row> {
  rows: readonly Row[];
  columns: readonly Column<Row>[];
  rowKey: (row: Row) => string;
  caption: string;
  searchable?: boolean;
  selectable?: boolean;
  inspectable?: boolean;
  persistenceKey?: string;
  renderExpanded?: (row: Row) => ReactNode;
  /** Automatic uses readable records below 640px; readers can still compare columns. */
  presentation?: "auto" | "table" | "cards" | "list" | "board";
}
const features = tableFeatures({
  columnVisibilityFeature,
  columnOrderingFeature,
  rowSelectionFeature,
});
interface View {
  presentation?: "auto" | "table" | "list" | "cards" | "board";
  name: string;
  query: TableQuery;
  hidden: Record<string, boolean>;
  group: string;
  density: string;
  pinned: string[];
  sizes: Record<string, number>;
  order?: string[];
}
export function DataTable<Row extends RowData>({
  rows,
  columns,
  rowKey,
  caption,
  searchable = true,
  selectable = false,
  inspectable = false,
  persistenceKey,
  presentation = "auto",
  renderExpanded,
}: DataTableProps<Row>) {
  const id = useId(),
    [query, setQuery] = useState(emptyTableQuery),
    [group, setGroup] = useState(""),
    [density, setDensity] = useState("comfortable"),
    [pinned, setPinned] = useState<string[]>([]),
    [sizes, setSizes] = useState<Record<string, number>>({}),
    [detail, setDetail] = useState<Row | null>(null),
    [message, setMessage] = useState(""),
    [viewName, setViewName] = useState(""),
    [layout, setLayout] = useState(presentation),
    [narrow, setNarrow] = useState(false),
    [expanded, setExpanded] = useState<Set<string>>(new Set()),
    [columnSearch, setColumnSearch] = useState("");
  useEffect(() => {
    const media = window.matchMedia?.("(max-width: 640px)");
    if (!media) return;
    const update = () => setNarrow(media.matches);
    update();
    media.addEventListener?.("change", update);
    return () => media.removeEventListener?.("change", update);
  }, []);
  const effectiveLayout =
    layout === "auto" ? (narrow ? "cards" : "table") : layout;
  const storageKey = persistenceKey
    ? "bottifact-table:" + persistenceKey
    : null;
  const [views, setViews] = useState<View[]>(() => {
    try {
      const data = JSON.parse(
        storageKey ? localStorage.getItem(storageKey) || "[]" : "[]",
      );
      return Array.isArray(data)
        ? data
            .filter(
              (v) =>
                typeof v.name === "string" &&
                Array.isArray(v.query?.rules) &&
                Array.isArray(v.query?.sort),
            )
            .slice(0, 20)
        : [];
    } catch {
      return [];
    }
  });
  const values = (row: Row) =>
    Object.fromEntries(columns.map((c) => [c.id, c.value(row)]));
  const visible = useMemo(
    () => queryTableRows(rows, query, values),
    [rows, columns, query],
  );
  const defs = useMemo(
    () =>
      columns.map((c) => ({ id: c.id, header: c.header, accessorFn: c.value })),
    [columns],
  );
  const table = useTable({
    features,
    columns: defs,
    data: visible,
    getRowId: rowKey,
  });
  const ordered = table.getAllLeafColumns();
  function moveColumn(from: string, to: string) {
    const order = ordered.map(c => c.id);
    const fromIndex = order.indexOf(from), toIndex = order.indexOf(to);
    if (fromIndex < 0 || toIndex < 0 || from === to) return;
    order.splice(fromIndex, 1); order.splice(toIndex, 0, from);
    table.setColumnOrder(order);
    setMessage(`${columns.find(c => c.id === from)?.header} moved to position ${toIndex + 1}.`);
  }
  const shown = table.getVisibleLeafColumns(),
    selected = rows.filter((r) => table.state.rowSelection[rowKey(r)]);
  const effectiveGroup=group || (effectiveLayout === "board" ? (columns.find(c=>/status|state|team|category/i.test(c.id)) || columns.find(c=>c.type!=="number"))?.id || "" : "");
  const groups = new Map<string, Row[]>();
  for (const row of visible) {
    const label = effectiveGroup
      ? String(columns.find((c) => c.id === effectiveGroup)?.value(row) ?? "Missing")
      : "";
    if (!groups.has(label)) groups.set(label, []);
    groups.get(label)!.push(row);
  }
  function toggle(column: Column<Row>, multiple: boolean) {
    setQuery((q) => {
      const old = q.sort.find((s) => s.column === column.id),
        next = {
          column: column.id,
          direction:
            old?.direction === "asc" ? ("desc" as const) : ("asc" as const),
        };
      return {
        ...q,
        sort: multiple
          ? [...q.sort.filter((s) => s.column !== column.id), next]
          : [next],
      };
    });
  }
  function save() {
    if (!storageKey || !viewName.trim()) return;
    const view: View = {
      name: viewName.trim().slice(0, 80),
      presentation: layout,
      query,
      hidden: table.state.columnVisibility,
      group,
      density,
      pinned,
      sizes,
      order: ordered.map(c => c.id),
    };
    const next = [...views.filter((v) => v.name !== view.name), view].slice(
      -20,
    );
    try {
      localStorage.setItem(storageKey, JSON.stringify(next));
      setViews(next);
      setMessage("View saved on this device.");
    } catch {
      setMessage("Storage unavailable. Keep this tab open.");
    }
  }
  function apply(v: View) {
    setLayout(v.presentation && ["auto","table","list","cards","board"].includes(v.presentation) ? v.presentation : "auto");
    setQuery(v.query);
    setGroup(v.group);
    setDensity(v.density);
    setPinned(v.pinned || []);
    setSizes(v.sizes || {});
    table.setColumnVisibility(v.hidden || {});
    table.setColumnOrder((v.order || []).filter(id => columns.some(c => c.id === id)));
  }
  function exportRows(data: readonly Row[]) {
    const active = shown.map(column => columns.find(c => c.id === column.id)!),
      blob = new Blob(
        [
          tableCSV(
            active.map((c) => c.header),
            data.map((r) => active.map((c) => c.value(r))),
          ),
        ],
        { type: "text/csv;charset=utf-8" },
      ),
      url = URL.createObjectURL(blob),
      a = document.createElement("a");
    a.href = url;
    a.download = "table.csv";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function columnWidth(id: string) {
    const column = columns.find(c => c.id === id)!;
    return sizes[id] || Math.max(100, Math.min(480, column.width || (column.type === "number" ? 100 : 180)));
  }
  function style(column: string): CSSProperties {
    const offset =
      shown
        .filter((c) => pinned.includes(c.id))
        .slice(
          0,
          shown
            .filter((c) => pinned.includes(c.id))
            .findIndex((c) => c.id === column),
        )
        .reduce((sum, c) => sum + columnWidth(c.id), 0);
    return {
      width: columnWidth(column),
      minWidth: columnWidth(column),
      ...(effectiveLayout === "table" && pinned.includes(column)
        ? {
            position: "sticky",
            left: offset,
            zIndex: 2,
            background: "var(--papel, #fff)",
          }
        : {}),
    };
  }
  const extra = Number(selectable) + Number(inspectable) + Number(Boolean(renderExpanded));
  return (
    <section
      className="bf-table-section"
      data-density={density}
      data-layout={effectiveLayout}
      data-table-id={persistenceKey || id}
    >
      <div className="bf-table-tools">
        {searchable && (
          <label htmlFor={id} className="bf-table-search">
            <span className="bf-visually-hidden">Search rows</span>
            <input
              id={id}
              type="search"
              placeholder="Search all records…"
              value={query.search}
              onChange={(e) => setQuery({ ...query, search: e.target.value })}
            />
          </label>
        )}
        <ButtonGroup aria-label="Table tools"><FilterBuilder columns={columns.map((c, index) => {
          const options = new Map<string, number>();
          if (index && c.type !== "number" && c.type !== "date") rows.forEach(row => { const value = c.value(row); if (typeof value === "string" && value) options.set(value, (options.get(value) || 0) + 1); });
          return {...c, choices: options.size <= 12 ? [...options].map(([value, count]) => ({value, count})) : undefined};
        })} value={query} onChange={setQuery} />
        <TablePopover label="Columns" icon={<ControlIcon name="columns" />}>
          <input type="search" aria-label="Find a column" placeholder="Find a column…" value={columnSearch} onChange={e => setColumnSearch(e.target.value)} />
          <p className="bf-popover-help">Drag to reorder, or use the arrow buttons.</p>
          <div className="bf-column-list">
          {ordered.map((entry, index) => {
            const c = columns.find(c => c.id === entry.id)!;
            if (!c.header.toLowerCase().includes(columnSearch.toLowerCase())) return null;
            return <div key={c.id} className="bf-column-control" draggable
              onDragStart={e => { e.dataTransfer.setData("application/x-margen-column", c.id); e.dataTransfer.effectAllowed = "move"; }}
              onDragOver={e => e.preventDefault()}
              onDrop={e => { e.preventDefault(); moveColumn(e.dataTransfer.getData("application/x-margen-column"), c.id); }}>
              <span className="bf-drag-handle" aria-hidden="true">⠿</span>
              <label><input type="checkbox" aria-label={`Show ${c.header}`} checked={entry.getIsVisible()}
                onChange={e => entry.toggleVisibility(e.target.checked)} disabled={shown.length === 1 && entry.getIsVisible()} />{c.header}</label>
              <div className="bf-column-actions">
                <button type="button" className="bf-icon-button" title={`Move ${c.header} earlier`} aria-label={`Move ${c.header} earlier`} disabled={index === 0} onClick={() => moveColumn(c.id, ordered[index - 1].id)}>↑</button>
                <button type="button" className="bf-icon-button" title={`Move ${c.header} later`} aria-label={`Move ${c.header} later`} disabled={index === ordered.length - 1} onClick={() => moveColumn(c.id, ordered[index + 1].id)}>↓</button>
                <button type="button" className="bf-icon-button" title={`Pin ${c.header}`} aria-label={`Pin ${c.header}`} aria-pressed={pinned.includes(c.id)} onClick={() => setPinned(p => p.includes(c.id) ? p.filter(x => x !== c.id) : [...p, c.id])}><ControlIcon name="pin" /></button>
              </div>
              <details className="bf-column-width"><summary>Width · {columnWidth(c.id)} px</summary><input aria-label={`Width of ${c.header}`} type="range" min="100" max="480" step="10" value={columnWidth(c.id)} onChange={e => setSizes({ ...sizes, [c.id]: Number(e.target.value) })} /></details>
            </div>;
          })}
          </div>
          {!ordered.some(c => columns.find(d => d.id === c.id)!.header.toLowerCase().includes(columnSearch.toLowerCase())) && <p>No matching columns.</p>}
          <div className="bf-display-options">
            <label>Group<select value={group} onChange={e => setGroup(e.target.value)}><option value="">None</option>{columns.map(c => <option key={c.id} value={c.id}>{c.header}</option>)}</select></label>
            <label>Density<select value={density} onChange={e => setDensity(e.target.value)}><option value="comfortable">Comfortable</option><option value="compact">Compact</option></select></label>
          </div>
          <button type="button" onClick={() => { table.setColumnOrder([]); table.setColumnVisibility({}); setPinned([]); setSizes({}); setDensity("comfortable"); }}>Reset columns</button>
        </TablePopover>
        <button type="button" className="bf-tool-button" onClick={() => exportRows(visible)}><ControlIcon name="download" />Export</button>
        {storageKey && (
          <TablePopover label="Views" icon={<ControlIcon name="bookmark" />}>
            <div className="bf-popover-stack">
              {views.map((v) => (
                <div key={v.name}>
                  <button type="button" onClick={() => apply(v)}>
                    {v.name}
                  </button>
                  <button
                    type="button"
                    aria-label={`Delete view ${v.name}`}
                    onClick={() => {
                      const next = views.filter((x) => x !== v);
                      try {
                        localStorage.setItem(storageKey, JSON.stringify(next));
                        setViews(next);
                      } catch {
                        setMessage("Storage unavailable.");
                      }
                    }}
                  >
                    ×
                  </button>
                </div>
              ))}
              <input
                aria-label="View name"
                value={viewName}
                onChange={(e) => setViewName(e.target.value)}
                maxLength={80}
              />
              <button type="button" onClick={save} disabled={!viewName.trim()}>
                Save view
              </button>
              <small>Private to this browser and table.</small>
            </div>
          </TablePopover>
        )}
        </ButtonGroup>
      </div>
      <div className="bf-table-overview">
        <p role="status">
          {visible.length} of {rows.length} rows
        </p>
        <div className="bf-table-presentation" aria-label="Record presentation">
          {(["table","list","cards","board"] as const).map(value=><button key={value} type="button" aria-pressed={effectiveLayout===value} onClick={()=>setLayout(value)}><ControlIcon name={value==="table"?"table":value==="list"?"review":value==="board"?"columns":"cards"}/>{{table:"Table",list:"List",cards:"Cards",board:"Board"}[value]}</button>)}
        </div>
      </div>
      {(query.search || query.rules.length > 0) && (
        <div className="bf-table-chips" aria-label="Active filters">
          {query.search && (
            <button
              type="button"
              aria-label="Clear search filter"
              onClick={() => setQuery({ ...query, search: "" })}
            >
              Search: {query.search} ×
            </button>
          )}
          {query.rules.map((r, i) => (
            <button
              type="button"
              key={i}
              aria-label={`Remove filter ${i + 1}`}
              onClick={() =>
                setQuery({
                  ...query,
                  rules: query.rules.filter((_, j) => j !== i),
                })
              }
            >
              {columns.find((c) => c.id === r.column)?.header}: {r.operator}{" "}
              {Array.isArray(r.value) ? r.value.join(", ") : r.value}
              {r.upper !== undefined ? ` – ${r.upper}` : ""} ×
            </button>
          ))}
        </div>
      )}
      {effectiveLayout !== "table" && (
        <label className="bf-card-sort">
          Order records
          <select
            aria-label="Order records"
            value={
              query.sort[0]
                ? `${query.sort[0].column}:${query.sort[0].direction}`
                : ""
            }
            onChange={(e) => {
              const [column, direction] = e.target.value.split(":");
              setQuery({
                ...query,
                sort: column
                  ? [{ column, direction: direction as "asc" | "desc" }]
                  : [],
              });
            }}
          >
            <option value="">Original order</option>
            {columns
              .filter((c) => c.sortable !== false)
              .flatMap((c) => [
                <option key={c.id + "asc"} value={c.id + ":asc"}>
                  {c.header} ↑
                </option>,
                <option key={c.id + "desc"} value={c.id + ":desc"}>
                  {c.header} ↓
                </option>,
              ])}
          </select>
        </label>
      )}
      <p className="bf-scroll-hint">
        Swipe across the table to compare columns →
      </p>
      {query.sort.length > 0 && (
        <p className="bf-table-hint">
          Order:{" "}
          {query.sort
            .map(
              (s) =>
                (columns.find((c) => c.id === s.column)?.header || s.column) +
                " " +
                s.direction,
            )
            .join(" → ")}{" "}
          · Shift-click a heading to add a sort.
        </p>
      )}
      {selectable && selected.length > 0 && (
        <div className="bf-table-selection">
          {selected.length} selected in the supplied dataset ·{" "}
          {selected.filter((r) => !visible.includes(r)).length} hidden by
          filters
          <button type="button" onClick={() => exportRows(selected)}>
            Export selected
          </button>
          <button type="button" onClick={() => table.setRowSelection({})}>
            Clear selection
          </button>
        </div>
      )}
      {message && <p aria-live="polite">{message}</p>}
      <div
        className="bf-table-scroll"
        role="region"
        aria-label={caption}
        tabIndex={0}
      >
        <Table role="table">
          <caption>{caption}</caption>
          <TableHeader role="rowgroup">
            <TableRow role="row">
              {selectable && (
                <TableHead>
                  <input
                    type="checkbox"
                    aria-label="Select visible rows"
                    tabIndex={effectiveLayout !== "table" ? -1 : undefined}
                    checked={
                      visible.length > 0 &&
                      visible.every((r) => table.state.rowSelection[rowKey(r)])
                    }
                    onChange={(e) =>
                      table.setRowSelection((previous) => {
                        const next = { ...previous };
                        for (const r of visible) {
                          if (e.target.checked) next[rowKey(r)] = true;
                          else delete next[rowKey(r)];
                        }
                        return next;
                      })
                    }
                  />
                </TableHead>
              )}
              {renderExpanded && <TableHead><span className="bf-visually-hidden">Expand record</span></TableHead>}
              {shown.map((c) => {
                const def = columns.find((d) => d.id === c.id)!,
                  sort = query.sort.find((s) => s.column === c.id);
                return (
                  <TableHead
                    key={c.id}
                    scope="col"
                    style={style(c.id)}
                    role="columnheader"
                    aria-sort={
                      query.sort[0]?.column === c.id
                        ? sort?.direction === "asc"
                          ? "ascending"
                          : "descending"
                        : "none"
                    }
                  >
                    {def.sortable === false ? (
                      def.header
                    ) : (
                      <button
                        type="button"
                        tabIndex={effectiveLayout !== "table" ? -1 : undefined}
                        onClick={(e) => toggle(def, e.shiftKey)}
                      >
                        {def.header}
                        <span aria-hidden="true">
                          {" "}
                          {sort ? (sort.direction === "asc" ? "↑" : "↓") : "↕"}
                        </span>
                      </button>
                    )}
                  </TableHead>
                );
              })}
              {inspectable && <TableHead>Details</TableHead>}
            </TableRow>
          </TableHeader>
            {[...groups].map(([label, members]) => (
              <TableBody role="rowgroup" key={label}>
                {effectiveGroup && (
                  <TableRow className="bf-group">
                    <TableHead colSpan={shown.length + extra}>
                      {label} · {members.length} matching rows
                      {columns
                        .filter((c) => c.aggregate)
                        .map((c) => {
                          const nums = members
                            .map(c.value)
                            .filter(
                              (v): v is number =>
                                typeof v === "number" && Number.isFinite(v),
                            );
                          return (
                            <span key={c.id}>
                              {" "}
                              · {c.header} {c.aggregate}:{" "}
                              {nums.length
                                ? (
                                    nums.reduce((a, b) => a + b, 0) /
                                    (c.aggregate === "mean" ? nums.length : 1)
                                  ).toLocaleString()
                                : "—"}{" "}
                              ({nums.length} values)
                            </span>
                          );
                        })}
                    </TableHead>
                  </TableRow>
                )}
                {members.map((row) => (
                  <Fragment key={rowKey(row)}><TableRow
                    role="row"
                    key={rowKey(row)}
                    data-row-id={rowKey(row)}
                    data-selected={Boolean(
                      table.state.rowSelection[rowKey(row)],
                    )}
                  >
                    {selectable && (
                      <TableCell role="cell" className="bf-row-select">
                        <input
                          type="checkbox"
                          aria-label={`Select row ${rowKey(row)}`}
                          checked={Boolean(
                            table.state.rowSelection[rowKey(row)],
                          )}
                          onChange={(e) =>
                            table.setRowSelection((p) => {
                              const next = { ...p };
                              if (e.target.checked) next[rowKey(row)] = true;
                              else delete next[rowKey(row)];
                              return next;
                            })
                          }
                        />
                      </TableCell>
                    )}
                    {renderExpanded && <TableCell className="bf-row-expand"><button type="button" aria-label={`Expand row ${rowKey(row)}`} aria-expanded={expanded.has(rowKey(row))} aria-controls={`${id}-detail-${rowKey(row)}`} onClick={() => setExpanded(current => { const next = new Set(current); next.has(rowKey(row)) ? next.delete(rowKey(row)) : next.add(rowKey(row)); return next; })}><ControlIcon name={expanded.has(rowKey(row)) ? "chevronDown" : "chevronRight"} /></button></TableCell>}
                    {shown.map((c) => {
                      const def = columns.find((d) => d.id === c.id)!;
                      return (
                        <TableCell
                          key={c.id}
                          style={style(c.id)}
                          data-cell-id={rowKey(row) + ":" + c.id}
                          role="cell"
                          data-label={def.header}
                          data-primary={def.mobile === "primary" || (!columns.some(c => c.mobile === "primary") && shown[0]?.id === c.id)}
                          data-mobile={inspectable && def.mobile === "detail" ? "detail" : undefined}
                          data-numeric={
                            def.type === "number" ||
                            typeof def.value(row) === "number"
                          }
                        >
                          {def.render
                            ? def.render(row)
                            : (def.value(row) ?? "—")}
                        </TableCell>
                      );
                    })}
                    {inspectable && (
                      <TableCell role="cell" className="bf-row-inspect">
                        <button
                          type="button"
                          aria-label={`Inspect row ${rowKey(row)}`}
                          onClick={() => setDetail(row)}
                        >
                          ↗
                        </button>
                      </TableCell>
                    )}
                  </TableRow>
                  {renderExpanded && <TableRow className="bf-expanded-row" hidden={!expanded.has(rowKey(row))} id={`${id}-detail-${rowKey(row)}`}><TableCell colSpan={shown.length + extra}><div className="bf-expanded-content">{expanded.has(rowKey(row)) && renderExpanded(row)}</div></TableCell></TableRow>}
                  </Fragment>
                ))}
              </TableBody>
            ))}
            {!visible.length && (
              <TableBody role="rowgroup"><TableRow role="row">
                <TableCell colSpan={shown.length + extra}>
                  No matching rows.
                </TableCell>
              </TableRow></TableBody>
            )}
        </Table>
      </div>
      <Inspector
        open={detail !== null}
        onOpenChange={(open) => !open && setDetail(null)}
        title="Row detail"
      >
        {detail !== null && (
          <>
            <p>Record: {rowKey(detail)}</p>
            <dl>
              {columns.map((c) => (
                <Fragment key={c.id}>
                  <dt>{c.header}</dt>
                  <dd>
                    {c.render ? c.render(detail) : (c.value(detail) ?? "—")}
                  </dd>
                </Fragment>
              ))}
            </dl>
          </>
        )}
      </Inspector>
    </section>
  );
}
