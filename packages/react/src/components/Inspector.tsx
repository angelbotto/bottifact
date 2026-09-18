import * as Dialog from "@radix-ui/react-dialog";
import {
  useRef,
  useState,
  useLayoutEffect,
  type ReactNode,
  type CSSProperties,
} from "react";
export function Inspector({
  open,
  onOpenChange,
  title,
  children,
}: {
  open: boolean;
  onOpenChange: (value: boolean) => void;
  title: string;
  children: ReactNode;
}) {
  const anchor = useRef<HTMLSpanElement>(null),
    [tokens, setTokens] = useState<CSSProperties>({});
  useLayoutEffect(() => {
    if (!open || !anchor.current) return;
    const style = getComputedStyle(anchor.current);
    setTokens(
      Object.fromEntries(
        ["--papel", "--tinta", "--linea", "--panel"].map((k) => [
          k,
          style.getPropertyValue(k),
        ]),
      ) as CSSProperties,
    );
  }, [open]);
  return (
    <>
      <span ref={anchor} hidden />
      <Dialog.Root open={open} onOpenChange={onOpenChange}>
        <Dialog.Portal>
          <Dialog.Overlay className="bf-inspector-overlay" />
          <Dialog.Content
            className="bf-inspector"
            style={tokens}
            aria-describedby={undefined}
          >
            <header>
              <Dialog.Title>{title}</Dialog.Title>
              <Dialog.Close aria-label="Close inspector">×</Dialog.Close>
            </header>
            {children}
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </>
  );
}
