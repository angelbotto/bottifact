import { useEffect, useState, type CSSProperties } from 'react';
import { createRecipeDocument, type RecipeId, type ThemeFamily, type ThemeMode } from '@bottifact/core';
export interface ArtifactFrameProps { html: string; title: string; height?: number | string; style?: CSSProperties; }
/** Deliberately excludes allow-same-origin, top-navigation, forms and popups. */
export function ArtifactFrame({ html, title, height = 620, style }: ArtifactFrameProps) {
  return <iframe className="bf-artifact-frame" title={title} srcDoc={html} loading="lazy" sandbox="allow-scripts allow-downloads" referrerPolicy="no-referrer" style={{ width: '100%', height, border: 0, ...style }} />;
}
export interface RecipePreviewProps { id: RecipeId; theme?: ThemeFamily; mode?: ThemeMode; height?: number | string; }
export function RecipePreview({ id, theme = 'editorial', mode = 'system', height }: RecipePreviewProps) {
  const [html, setHtml] = useState('');
  const [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    setHtml(''); setError('');
    createRecipeDocument(id, { theme, mode }).then(value => { if (active) setHtml(value); }).catch(() => { if (active) setError('This component could not be loaded.'); });
    return () => { active = false; };
  }, [id, theme, mode]);
  if (error) return <p role="alert">{error}</p>;
  if (!html) return <p role="status">Loading component…</p>;
  return <ArtifactFrame html={html} title={`Bottifact component: ${id}`} height={height} />;
}
