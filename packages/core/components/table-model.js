/* Generated from core/src/table-model.ts; run node scripts/build_table_model.mjs. */
(()=>{
const emptyTableQuery = () => ({
    search: "",
    join: "and",
    rules: [],
    sort: [],
});
const normalizeTableText = (value) => String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
function matchesTableRule(value, rule) {
    if (rule.operator === "empty")
        return value === null || value === "";
    if (value === null || value === "")
        return false;
    if (["gte", "lte", "between"].includes(rule.operator) &&
        (rule.value === "" || rule.value === undefined || Array.isArray(rule.value)))
        return false;
    const text = normalizeTableText(value), expected = normalizeTableText(rule.value);
    switch (rule.operator) {
        case "contains":
            return text.includes(expected);
        case "eq":
            return text === expected;
        case "in":
            return (Array.isArray(rule.value) &&
                rule.value.some((v) => normalizeTableText(v) === text));
        case "gte":
            return typeof value === "number"
                ? Number.isFinite(Number(rule.value)) && value >= Number(rule.value)
                : text >= expected;
        case "lte":
            return typeof value === "number"
                ? Number.isFinite(Number(rule.value)) && value <= Number(rule.value)
                : text <= expected;
        case "between":
            return (matchesTableRule(value, { ...rule, operator: "gte" }) &&
                matchesTableRule(value, { ...rule, operator: "lte", value: rule.upper }));
        default:
            return false;
    }
}
function queryTableRows(rows, query, values) {
    const words = normalizeTableText(query.search)
        .trim()
        .split(/\s+/)
        .filter(Boolean);
    const result = rows
        .map((row, index) => ({ row, index, values: values(row) }))
        .filter((entry) => words.every((w) => normalizeTableText(Object.values(entry.values).join(" ")).includes(w)) &&
        (!query.rules.length ||
            (query.join === "or"
                ? query.rules.some((rule) => matchesTableRule(entry.values[rule.column] ?? null, rule))
                : query.rules.every((rule) => matchesTableRule(entry.values[rule.column] ?? null, rule)))));
    result.sort((a, b) => {
        for (const sort of query.sort) {
            const x = a.values[sort.column], y = b.values[sort.column];
            if (x == null || x === "") {
                if (y != null && y !== "")
                    return 1;
                continue;
            }
            if (y == null || y === "")
                return -1;
            const d = typeof x === "number" && typeof y === "number"
                ? x - y
                : normalizeTableText(x).localeCompare(normalizeTableText(y), "en", {
                    numeric: true,
                });
            if (d)
                return sort.direction === "desc" ? -d : d;
        }
        return a.index - b.index;
    });
    return result.map((e) => e.row);
}
function tableCSV(headers, rows) {
    const cell = (v) => {
        const s = String(v ?? "");
        return ('"' +
            ((typeof v !== "number" && /^\s*[=+@-]/.test(s) ? "'" : "") + s).replaceAll('"', '""') +
            '"');
    };
    return [headers, ...rows].map((row) => row.map(cell).join(",")).join("\r\n");
}
const TableModel = {
    empty: emptyTableQuery,
    normalize: normalizeTableText,
    matches: matchesTableRule,
    query: queryTableRows,
    csv: tableCSV,
};

globalThis.BottifactTableModel=TableModel;
})();
