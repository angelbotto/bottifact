import { useEffect, useState, type CSSProperties, type HTMLAttributes } from 'react';
import { getThemeTokens, type ThemeFamily, type ThemeMode } from '@bottifact/core/themes';

export interface ArtifactProps extends HTMLAttributes<HTMLElement> {
  theme?: ThemeFamily;
  mode?: ThemeMode;
}

/** Theme state is scoped to this artifact; it never changes the host application's document. */
export function Artifact({ theme = 'editorial', mode = 'system', children, className = '', style, ...props }: ArtifactProps) {
  const [systemDark, setSystemDark] = useState(false);
  useEffect(() => {
    if (mode !== 'system') return;
    const media = window.matchMedia('(prefers-color-scheme: dark)');
    const update = () => setSystemDark(media.matches);
    update();
    media.addEventListener('change', update);
    return () => media.removeEventListener('change', update);
  }, [mode]);
  const resolved = mode === 'system' ? (systemDark ? 'dark' : 'light') : mode;
  const tokens = Object.fromEntries(Object.entries(getThemeTokens(theme, resolved)).map(([key, value]) => ['--' + key, value]));
  return <article {...props} className={`bf-artifact ${className}`} data-theme-family={theme} data-color-mode={resolved}
    style={{ ...tokens, colorScheme: resolved, ...style } as CSSProperties}>{children}</article>;
}
