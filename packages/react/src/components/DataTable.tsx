import {
  Fragment,
  useId,
  useMemo,
  useState,
  type ReactNode,
  type CSSProperties,
} from "react";
import {
  useTable,
  tableFeatures,
  columnVisibilityFeature,
  rowSelectionFeature,
  type RowData,
} from "@tanstack/react-table";
import {
  emptyTableQuery,
  queryTableRows,
  tableCSV,
  type TableQuery,
} from "@bottifact/core";
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
}
const features = tableFeatures({
  columnVisibilityFeature,
  rowSelectionFeature,
});
interface View {
  name: string;
  query: TableQuery;
  hidden: Record<string, boolean>;
  group: string;
  density: string;
  pinned: string[];
  sizes: Record<string, number>;
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
}: DataTableProps<Row>) {
  const id = useId(),
    [query, setQuery] = useState(emptyTableQuery),
    [group, setGroup] = useState(""),
    [density, setDensity] = useState("comfortable"),
    [pinned, setPinned] = useState<string[]>([]),
    [sizes, setSizes] = useState<Record<string, number>>({}),
    [detail, setDetail] = useState<Row | null>(null),
    [message, setMessage] = useState(""),
    [viewName, setViewName] = useState("");
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
  const shown = table.getVisibleLeafColumns(),
    selected = rows.filter((r) => table.state.rowSelection[rowKey(r)]);
  const groups = new Map<string, Row[]>();
  for (const row of visible) {
    const label = group
      ? String(columns.find((c) => c.id === group)?.value(row) ?? "Missing")
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
      query,
      hidden: table.state.columnVisibility,
      group,
      density,
      pinned,
      sizes,
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
    setQuery(v.query);
    setGroup(v.group);
    setDensity(v.density);
    setPinned(v.pinned || []);
    setSizes(v.sizes || {});
    table.setColumnVisibility(v.hidden || {});
  }
  function exportRows(data: readonly Row[]) {
    const active = columns.filter((c) => shown.some((s) => s.id === c.id)),
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
  function style(column: string): CSSProperties {
    const offset =
      (selectable ? 44 : 0) +
      shown
        .filter((c) => pinned.includes(c.id))
        .slice(
          0,
          shown
            .filter((c) => pinned.includes(c.id))
            .findIndex((c) => c.id === column),
        )
        .reduce((sum, c) => sum + (sizes[c.id] || 180), 0);
    return {
      width: sizes[column] || 180,
      minWidth: sizes[column] || 180,
      ...(pinned.includes(column)
        ? {
            position: "sticky",
            left: offset,
            zIndex: 2,
            background: "var(--papel, #fff)",
          }
        : {}),
    };
  }
  const extra = Number(selectable) + Number(inspectable);
  return (
    <section
      className="bf-table-section"
      data-density={density}
      data-table-id={persistenceKey || id}
    >
      <div className="bf-table-tools">
        {searchable && (
          <label htmlFor={id}>
            Search rows
            <input
              id={id}
              type="search"
              value={query.search}
              onChange={(e) => setQuery({ ...query, search: e.target.value })}
            />
          </label>
        )}
        <FilterBuilder columns={columns} value={query} onChange={setQuery} />
        <details>
          <summary>Columns</summary>
          <div className="bf-filter-panel">
            {columns.map((c) => (
              <div key={c.id} className="bf-column-control">
                <label>
                  <input
                    type="checkbox"
                    checked={table.getColumn(c.id)!.getIsVisible()}
                    onChange={(e) =>
                      table.getColumn(c.id)!.toggleVisibility(e.target.checked)
                    }
                    disabled={
                      shown.length === 1 &&
                      table.getColumn(c.id)!.getIsVisible()
                    }
                  />
                  {c.header}
                </label>
                <button
                  type="button"
                  aria-pressed={pinned.includes(c.id)}
                  onClick={() =>
                    setPinned((p) =>
                      p.includes(c.id)
                        ? p.filter((x) => x !== c.id)
                        : [...p, c.id],
                    )
                  }
                >
                  Pin
                </button>
                <input
                  aria-label={`Width of ${c.header}`}
                  type="range"
                  min="100"
                  max="480"
                  step="10"
                  value={sizes[c.id] || 180}
                  onChange={(e) =>
                    setSizes({ ...sizes, [c.id]: Number(e.target.value) })
                  }
                />
              </div>
            ))}
          </div>
        </details>
        <label>
          Group
          <select value={group} onChange={(e) => setGroup(e.target.value)}>
            <option value="">None</option>
            {columns.map((c) => (
              <option key={c.id} value={c.id}>
                {c.header}
              </option>
            ))}
          </select>
        </label>
        <label>
          Density
          <select value={density} onChange={(e) => setDensity(e.target.value)}>
            <option value="comfortable">Comfortable</option>
            <option value="compact">Compact</option>
          </select>
        </label>
        <button
          type="button"
          onClick={() => {
            setQuery(emptyTableQuery());
            setGroup("");
            setPinned([]);
            setSizes({});
            table.setColumnVisibility({});
            table.setRowSelection({});
          }}
        >
          Reset
        </button>
        <button type="button" onClick={() => exportRows(visible)}>
          Export visible
        </button>
        {storageKey && (
          <details>
            <summary>Views</summary>
            <div className="bf-filter-panel">
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
          </details>
        )}
      </div>
      <p role="status">
        {visible.length} of {rows.length} rows
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
        <Table>
          <caption>{caption}</caption>
          <TableHeader>
            <TableRow>
              {selectable && (
                <TableHead>
                  <input
                    type="checkbox"
                    aria-label="Select visible rows"
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
              {shown.map((c) => {
                const def = columns.find((d) => d.id === c.id)!,
                  sort = query.sort.find((s) => s.column === c.id);
                return (
                  <TableHead
                    key={c.id}
                    scope="col"
                    style={style(c.id)}
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
          <TableBody>
            {[...groups].map(([label, members]) => (
              <Fragment key={label}>
                {group && (
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
                  <TableRow
                    key={rowKey(row)}
                    data-row-id={rowKey(row)}
                    data-selected={Boolean(
                      table.state.rowSelection[rowKey(row)],
                    )}
                  >
                    {selectable && (
                      <TableCell>
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
                    {shown.map((c) => {
                      const def = columns.find((d) => d.id === c.id)!;
                      return (
                        <TableCell
                          key={c.id}
                          style={style(c.id)}
                          data-cell-id={rowKey(row) + ":" + c.id}
                        >
                          {def.render
                            ? def.render(row)
                            : (def.value(row) ?? "—")}
                        </TableCell>
                      );
                    })}
                    {inspectable && (
                      <TableCell>
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
                ))}
              </Fragment>
            ))}
            {!visible.length && (
              <TableRow>
                <TableCell colSpan={shown.length + extra}>
                  No matching rows.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
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
