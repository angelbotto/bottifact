import type { ReactNode } from 'react';
export interface EditorialCard { id: string; title: string; description: ReactNode; meta?: string; href?: string; }
const safeHref = (value: string) => /^(https?:\/\/|\/[^/]|#|\.\.?\/)/i.test(value);
export function CardGrid({ items, label = 'Related documents' }: { items: readonly EditorialCard[]; label?: string }) {
  return <section className="bf-card-grid" aria-label={label}>{items.map(item => <article key={item.id}>
    <h3>{item.href && safeHref(item.href) ? <a href={item.href}>{item.title}</a> : item.title}</h3>
    <div>{item.description}</div>{item.meta && <p className="bf-meta">{item.meta}</p>}
  </article>)}</section>;
}
