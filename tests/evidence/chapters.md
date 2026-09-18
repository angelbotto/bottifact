# Capítulos, pestañas y tres paletas · 14-sep-2026

La solicitud de Angel fue mostrar una versión multipágina/con tabs, corregir la cabecera
“nota / tikin”, añadir colores y analizar nuevas piezas. Se implementa `examples/generated/report.html`, con
Resumen/Evidencia/Prototipo/Próximos pasos, y se mantiene `examples/generated/chapters.html` como ejemplo mínimo.

La firma pasa a “tikin” serif con leyenda sans. La llave de apariencia conserva su contrato.
Las paletas Oliva, Arcilla y Ciruela son optativas y completas: tokens base, gráficas, calor,
sonido, escritura, escenas y globo. Componentes editoriales heredan los tokens existentes.
Ningún tema base cambia. No se añade dependencia ni recurso remoto. El informe no usa Three.

Dos piezas nuevas: pestañas locales con activación manual y ficha de hallazgo. El catálogo
reúne 32 recetas copiables. El informe completo también está documentado en docs/components.md,
con la distinción entre navegación de capítulos y tablist, instalación, criterios y límites.

`data-historial` es optativo: añade pushState y popstate a la navegación por capítulos; el
contrato anterior conserva replaceState. El salto al contenido apunta al capítulo visible y
los botones activos quedan alcanzables en su barra local. La cabecera común aparece al cargar
un enlace directo; el hash sigue identificando el capítulo. Los tablists no modifican la URL.

## Ejecutado

- `python3 scripts/build.py` y `python3 scripts/validate.py`: cinco artefactos sincronizados,
  CSP, referencias, sintaxis JS, rejilla y regiones; se comprueba la integridad de las tres
  paletas adicionales además de los cuatro selectores originales.
- `python3 scripts/check_chapters.py`: 8 contratos de interacción (historial real
  Atrás/Adelante, cuatro páginas, pestañas/foco/roles, destroy/reintento, visor oculto al inicio,
  elección de seis paletas/iconos). `capitulos-interaccion.json`.
- 72 combinaciones: 320×740, 390×844, 1639×939 × seis temas × cuatro capítulos. Se mide
  ancho del documento, figuras/texto concéntricos, regiones con foco y nombre, extremo del
  scroll alcanzable y panel de apariencia dentro de pantalla. `capitulos-pantallas.json`.
- 36 combinaciones del catálogo completo: tres viewports × seis colores × preferencia de
  sistema clara/oscura. CSS computado: texto y escalas mantienen sus umbrales de contraste,
  rótulos SVG dentro del viewBox y documento sin desbordamiento. `capitulos-paletas.json`.
- 21 regresiones de componentes anteriores (`capitulos-regresion.json`), más las 19 pruebas
  originales de barra, multipágina, copia, índice de página única y rejilla por sección,
  ejecutadas contra el servidor de desarrollo (`capitulos-base.json`).
- PDF desde Prototipo: 7 páginas físicas; pypdf confirma los cuatro capítulos, paneles ocultos
  de tabs y alternativa del visor. La página activa vuelve a Prototipo tras imprimir.
  Movimiento reducido emulado: transiciones de navegación y tabs en cero. `capitulos-salida.json`.
- Capturas inspeccionadas: Oliva/escritorio/Resumen, Arcilla390/Evidencia, Ciruela/escritorio/
  Prototipo, y firma de catálogo390. Rehechas usando los radios reales para sincronizar icono.

La fuente de cada medida es el DOM/CSS calculado del navegador de Orca; identidad del navegador,
fecha y servidor en `capitulos-ejecucion.json`. No son medidas atribuidas a cmrg.me.

## Límites

Foco y teclado comprobados con DOM/eventos explícitos; no se afirma teclado físico ni lector
de pantalla. Viewports emulados, no hardware móvil. PDF extraído, no impresión física.
Sin JS el informe multipágina sólo presenta el primer capítulo en pantalla; tabs aisladas
muestran todas sus secciones. Los siguientes componentes son propuestas, no funcionalidades
entregadas: véase [capitulos-propuesta.md](chapters-proposal.md).
