import { useId, useMemo, useState, type ReactNode } from 'react';
export interface Column<Row> { id: string; header: string; value: (row: Row) => string | number | null; render?: (row: Row) => ReactNode; sortable?: boolean; }
export interface DataTableProps<Row> { rows: readonly Row[]; columns: readonly Column<Row>[]; rowKey: (row: Row) => string; caption: string; searchable?: boolean; }
const collator = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });
export function DataTable<Row>({ rows, columns, rowKey, caption, searchable = true }: DataTableProps<Row>) {
  const id = useId();
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState<{ id: string; direction: 'ascending' | 'descending' } | null>(null);
  const visible = useMemo(() => {
    const filtered = rows.filter(row => !query || columns.some(column => String(column.value(row) ?? '').toLocaleLowerCase().includes(query.toLocaleLowerCase())));
    const column = columns.find(candidate => candidate.id === sort?.id);
    if (!column || !sort) return filtered;
    return [...filtered].sort((a, b) => {
      const left = column.value(a), right = column.value(b);
      const order = left == null ? (right == null ? 0 : 1) : right == null ? -1 :
        typeof left === 'number' && typeof right === 'number' ? left - right : collator.compare(String(left), String(right));
      return order * (sort.direction === 'ascending' ? 1 : -1);
    });
  }, [rows, columns, query, sort]);
  function toggle(column: Column<Row>) {
    setSort(previous => ({ id: column.id, direction: previous?.id === column.id && previous.direction === 'ascending' ? 'descending' : 'ascending' }));
  }
  return <section className="bf-table-section">
    {searchable && <div className="bf-table-tools"><label htmlFor={id}>Search rows</label><input id={id} type="search" value={query} onChange={event => setQuery(event.target.value)} /><span role="status">{visible.length} of {rows.length} rows</span></div>}
    <div className="bf-table-scroll" role="region" aria-label={caption} tabIndex={0}><table><caption>{caption}</caption><thead><tr>{columns.map(column => <th key={column.id} scope="col" aria-sort={sort?.id === column.id ? sort.direction : 'none'}>
      {column.sortable === false ? column.header : <button type="button" onClick={() => toggle(column)}>{column.header}<span aria-hidden="true"> {sort?.id === column.id ? (sort.direction === 'ascending' ? '↑' : '↓') : '↕'}</span></button>}
    </th>)}</tr></thead><tbody>{visible.map(row => <tr key={rowKey(row)}>{columns.map(column => <td key={column.id}>{column.render ? column.render(row) : column.value(row) ?? '—'}</td>)}</tr>)}
      {visible.length === 0 && <tr><td colSpan={columns.length}>No matching rows.</td></tr>}
    </tbody></table></div>
  </section>;
}
