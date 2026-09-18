import * as Avatar from "@radix-ui/react-avatar";
import { useState, type ReactNode } from "react";

function imageSource(src?: string) {
  return src && (/^https?:\/\//i.test(src) || /^data:image\/(png|jpeg|webp|gif);base64,/i.test(src) || /^\/(?!\/)/.test(src)) ? src : undefined;
}

/** Keep the column's scalar `value` separate from its rich rendering. */
export function TablePerson({ name, detail, src }: { name: string; detail?: string; src?: string }) {
  return <span className="bf-person"><Avatar.Root className="bf-avatar">
    <Avatar.Image src={imageSource(src)} alt="" />
    <Avatar.Fallback>{name.trim().split(/\s+/).slice(0, 2).map(part => part[0]).join("")}</Avatar.Fallback>
  </Avatar.Root><span><strong>{name}</strong>{detail && <small>{detail}</small>}</span></span>;
}

export function TableStatus({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "success" | "warning" | "danger" | "info" }) {
  return <span className="bf-status" data-tone={tone}><span aria-hidden="true" />{children}</span>;
}

export function TableMedia({ src, alt, title, detail }: { src: string; alt: string; title: string; detail?: string }) {
  const [failed, setFailed] = useState(false);
  return <span className="bf-media">{imageSource(src) && !failed ? <img src={imageSource(src)} alt={alt} width={64} height={44} loading="lazy" onError={() => setFailed(true)} /> : <span className="bf-media-fallback" role="img" aria-label={alt}>▧</span>}<span><strong>{title}</strong>{detail && <small>{detail}</small>}</span></span>;
}

export function TableDetailCard({ title, children }: { title: string; children: ReactNode }) {
  return <section className="bf-detail-card"><h4>{title}</h4>{children}</section>;
}
