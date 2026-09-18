import type { ReactNode } from 'react';
export interface CalloutProps { title: string; children: ReactNode; tone?: 'note' | 'caution' | 'success'; }
export function Callout({ title, children, tone = 'note' }: CalloutProps) {
  return <aside className="bf-callout" data-tone={tone} aria-label={title}>
    <span className="bf-callout-icon" aria-hidden="true">{tone === 'caution' ? '!' : tone === 'success' ? '✓' : 'i'}</span>
    <strong>{title}</strong><div>{children}</div>
  </aside>;
}
