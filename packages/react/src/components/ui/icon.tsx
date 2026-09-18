/** Small decorative controls; the adjacent label owns the accessible name. */
const paths = {
  filter: "M4 6h16M7 12h10M10 18h4",
  columns: "M3 4h18v16H3ZM10 4v16M16 4v16",
  more: "M5 12h.01M12 12h.01M19 12h.01",
  bookmark: "M6 3h12v18l-6-4-6 4Z",
  table: "M3 4h18v16H3ZM3 10h18M10 4v16",
  cards: "M4 3h16v7H4ZM4 14h16v7H4Z",
  download: "M12 3v12m-4-4 4 4 4-4M4 16v5h16v-5",
} as const;
export function ControlIcon({ name }: { name: keyof typeof paths }) {
  return (
    <svg
      className="bf-control-icon"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.65"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      <path d={paths[name]} />
    </svg>
  );
}
