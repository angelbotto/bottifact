import type { TableQuery, TableRule } from "@bottifact/core";
import { ControlIcon } from "./ui/icon.js";
export interface FilterColumn {
  id: string;
  header: string;
  type?: "text" | "number" | "date";
}
export function FilterBuilder({
  columns,
  value,
  onChange,
}: {
  columns: readonly FilterColumn[];
  value: TableQuery;
  onChange: (q: TableQuery) => void;
}) {
  const update = (index: number, rule: TableRule) =>
    onChange({
      ...value,
      rules: value.rules.map((r, i) => (i === index ? rule : r)),
    });
  return (
    <details className="bf-filter-builder">
      <summary>
        <ControlIcon name="filter" /> Filters{" "}
        {value.rules.length > 0 && `(${value.rules.length})`}
      </summary>
      <div className="bf-filter-panel">
        <label>
          Match
          <select
            value={value.join}
            onChange={(e) =>
              onChange({ ...value, join: e.target.value as "and" | "or" })
            }
          >
            <option value="and">All conditions</option>
            <option value="or">Any condition</option>
          </select>
        </label>
        {value.rules.map((rule, i) => {
          const column = columns.find((c) => c.id === rule.column);
          return (
            <div className="bf-filter-rule" key={i}>
              <select
                aria-label={`Filter column ${i + 1}`}
                value={rule.column}
                onChange={(e) =>
                  update(i, {
                    column: e.target.value,
                    operator: "contains",
                    value: "",
                  })
                }
              >
                {columns.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.header}
                  </option>
                ))}
              </select>
              <select
                aria-label={`Filter operator ${i + 1}`}
                value={rule.operator}
                onChange={(e) =>
                  update(i, {
                    ...rule,
                    operator: e.target.value as TableRule["operator"],
                  })
                }
              >
                {[
                  ["contains", "Contains"],
                  ["eq", "Equals"],
                  ["in", "Is one of"],
                  ["gte", "At least / after"],
                  ["lte", "At most / before"],
                  ["between", "Between"],
                  ["empty", "Is empty"],
                ].map(([id, label]) => (
                  <option key={id} value={id}>
                    {label}
                  </option>
                ))}
              </select>
              {rule.operator !== "empty" && (
                <input
                  aria-label={`Filter value ${i + 1}`}
                  type={
                    rule.operator === "in"
                      ? "text"
                      : column?.type === "number"
                        ? "number"
                        : column?.type === "date"
                          ? "date"
                          : "text"
                  }
                  placeholder={
                    rule.operator === "in" ? "Comma-separated values" : "Value"
                  }
                  value={
                    Array.isArray(rule.value)
                      ? rule.value.join(",")
                      : (rule.value ?? "")
                  }
                  onChange={(e) =>
                    update(i, {
                      ...rule,
                      value:
                        rule.operator === "in"
                          ? e.target.value.split(",").map((s) => s.trim())
                          : e.target.value,
                    })
                  }
                />
              )}
              {rule.operator === "between" && (
                <input
                  aria-label={`Upper bound ${i + 1}`}
                  type={column?.type === "date" ? "date" : "number"}
                  value={rule.upper ?? ""}
                  onChange={(e) =>
                    update(i, { ...rule, upper: e.target.value })
                  }
                />
              )}
              <button
                type="button"
                aria-label={`Remove filter ${i + 1}`}
                onClick={() =>
                  onChange({
                    ...value,
                    rules: value.rules.filter((_, index) => index !== i),
                  })
                }
              >
                ×
              </button>
            </div>
          );
        })}
        <button
          type="button"
          disabled={value.rules.length >= 12 || !columns.length}
          onClick={() =>
            onChange({
              ...value,
              rules: [
                ...value.rules,
                { column: columns[0].id, operator: "contains", value: "" },
              ],
            })
          }
        >
          Add condition
        </button>
      </div>
    </details>
  );
}
