import { useEffect, useRef, useState, type ReactNode } from 'react';
export interface MarginNoteProps { children: ReactNode; note: string; side?: 'left' | 'right'; animate?: boolean; }
export function MarginNote({ children, note, side = 'right', animate = true }: MarginNoteProps) {
  const root = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const [revision, setRevision] = useState(0);
  useEffect(() => {
    const node = root.current;
    if (!node) return;
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (!animate || motion.matches || !('IntersectionObserver' in window)) { setVisible(true); return; }
    const observer = new IntersectionObserver(entries => setVisible(entries.some(entry => entry.isIntersecting)), { threshold: .25 });
    observer.observe(node);
    return () => observer.disconnect();
  }, [animate]);
  return <div ref={root} className="bf-margin" data-side={side}>
    <div className="bf-margin-content">{children}</div>
    <aside className="bf-margin-note" aria-label="Margin note" data-visible={visible} data-animate={animate}>
      <span key={revision}>{note}</span>
      {animate && <button type="button" className="bf-replay" aria-label="Replay margin note" onClick={() => setRevision(value => value + 1)}>↻</button>}
    </aside>
  </div>;
}
