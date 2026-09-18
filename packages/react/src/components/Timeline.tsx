import type { ReactNode } from 'react';
export interface TimelineItem { id: string; title: string; date: string; children?: ReactNode; current?: boolean; }
export function Timeline({ items, label = 'Timeline' }: { items: readonly TimelineItem[]; label?: string }) {
  return <ol className="bf-timeline" aria-label={label}>{items.map(item => <li key={item.id} data-current={item.current || undefined}>
    <h3>{item.title}</h3><p className="bf-meta">{item.date}</p>{item.children}
  </li>)}</ol>;
}
