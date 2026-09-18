import * as Popover from "@radix-ui/react-popover";
import { useRef, useState, type CSSProperties, type ReactNode } from "react";

/** Radix/shadcn composition with artifact-scoped tokens carried across the portal. */
export function TablePopover({ label, icon, children }: { label: string; icon?: ReactNode; children: ReactNode }) {
  const trigger = useRef<HTMLButtonElement>(null);
  const [tokens, setTokens] = useState<CSSProperties>({});
  function capture(open: boolean) {
    if (!open || !trigger.current) return;
    const style = getComputedStyle(trigger.current);
    setTokens(Object.fromEntries(["--papel", "--tinta", "--tinta-2", "--panel", "--panel-2", "--linea", "--foco", "--naranja"].map(key => [key, style.getPropertyValue(key)])) as CSSProperties);
  }
  return <Popover.Root onOpenChange={capture}>
    <Popover.Trigger ref={trigger} className="bf-tool-button">{icon}{label}</Popover.Trigger>
    <Popover.Portal>
      <Popover.Content className="bf-table-popover" style={tokens} sideOffset={8} align="end" collisionPadding={12} aria-label={label}>
        <div className="bf-popover-heading"><strong>{label}</strong><Popover.Close aria-label={`Close ${label}`} className="bf-icon-button">×</Popover.Close></div>
        {children}
      </Popover.Content>
    </Popover.Portal>
  </Popover.Root>;
}
