/** Shared query semantics for local artifacts, React tables and server parity fixtures. */
export type TableValue = string | number | null;
export type TableOperator =
  | "contains"
  | "eq"
  | "in"
  | "gte"
  | "lte"
  | "between"
  | "empty";
export interface TableRule {
  column: string;
  operator: TableOperator;
  value?: string | number | string[];
  upper?: string | number;
}
export interface TableQuery {
  search: string;
  join: "and" | "or";
  rules: TableRule[];
  sort: { column: string; direction: "asc" | "desc" }[];
}
export const emptyTableQuery = (): TableQuery => ({
  search: "",
  join: "and",
  rules: [],
  sort: [],
});
export const normalizeTableText = (value: unknown) =>
  String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
export function matchesTableRule(value: TableValue, rule: TableRule): boolean {
  if (rule.operator === "empty") return value === null || value === "";
  if (value === null || value === "") return false;
  if (
    ["gte", "lte", "between"].includes(rule.operator) &&
    (rule.value === "" || rule.value === undefined || Array.isArray(rule.value))
  )
    return false;
  const text = normalizeTableText(value),
    expected = normalizeTableText(rule.value);
  switch (rule.operator) {
    case "contains":
      return text.includes(expected);
    case "eq":
      return text === expected;
    case "in":
      return (
        Array.isArray(rule.value) &&
        rule.value.some((v) => normalizeTableText(v) === text)
      );
    case "gte":
      return typeof value === "number"
        ? Number.isFinite(Number(rule.value)) && value >= Number(rule.value)
        : text >= expected;
    case "lte":
      return typeof value === "number"
        ? Number.isFinite(Number(rule.value)) && value <= Number(rule.value)
        : text <= expected;
    case "between":
      return (
        matchesTableRule(value, { ...rule, operator: "gte" }) &&
        matchesTableRule(value, { ...rule, operator: "lte", value: rule.upper })
      );
    default:
      return false;
  }
}
export function queryTableRows<Row>(
  rows: readonly Row[],
  query: TableQuery,
  values: (row: Row) => Record<string, TableValue>,
): Row[] {
  const words = normalizeTableText(query.search)
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  const result = rows
    .map((row, index) => ({ row, index, values: values(row) }))
    .filter(
      (entry) =>
        words.every((w) =>
          normalizeTableText(Object.values(entry.values).join(" ")).includes(w),
        ) &&
        (!query.rules.length ||
          (query.join === "or"
            ? query.rules.some((rule) =>
                matchesTableRule(entry.values[rule.column] ?? null, rule),
              )
            : query.rules.every((rule) =>
                matchesTableRule(entry.values[rule.column] ?? null, rule),
              ))),
    );
  result.sort((a, b) => {
    for (const sort of query.sort) {
      const x = a.values[sort.column],
        y = b.values[sort.column];
      if (x == null || x === "") {
        if (y != null && y !== "") return 1;
        continue;
      }
      if (y == null || y === "") return -1;
      const d =
        typeof x === "number" && typeof y === "number"
          ? x - y
          : normalizeTableText(x).localeCompare(normalizeTableText(y), "en", {
              numeric: true,
            });
      if (d) return sort.direction === "desc" ? -d : d;
    }
    return a.index - b.index;
  });
  return result.map((e) => e.row);
}
export function tableCSV(
  headers: readonly string[],
  rows: readonly (readonly TableValue[])[],
): string {
  const cell = (v: TableValue) => {
    const s = String(v ?? "");
    return (
      '"' +
      (
        (typeof v !== "number" && /^\s*[=+@-]/.test(s) ? "'" : "") + s
      ).replaceAll('"', '""') +
      '"'
    );
  };
  return [headers, ...rows].map((row) => row.map(cell).join(",")).join("\r\n");
}
export const TableModel = {
  empty: emptyTableQuery,
  normalize: normalizeTableText,
  matches: matchesTableRule,
  query: queryTableRows,
  csv: tableCSV,
};
