# Regresiones reproducidas · TIKIN-629

13-sep-2026. Orca, navegador incrustado, viewport 1639 × 939. Fixture `examples/generated/checks.html`
generada por `scripts/fixture_regression.py`. Observaciones anteriores a la corrección:

- Copia terminal: se sustituyó `navigator.clipboard.writeText` por un stub resuelto
  para aislar el manejador. Tras el clic, `svg=false`, estado vacío, texto copiado correcto.
  Después: `svg=true`, estado «Código copiado.». La API real y el caso denegado se
  verifican aparte; el stub no demuestra permiso del portapapeles.
- Índice, sección Dos visible: `aria-current=location` estaba en `#cuatro`, oculto.
  Después sólo `#dos` tiene `aria-current`, `aqui-actual` y peso calculado 600.
- Selector aislado `.multipagina .indice li.aqui-actual a[aria-current=location]`:
  peso calculado 400 antes; la neutralización ganaba por especificidad. Ahora 600.
- `orca pdf --json`, primera página activa: el PDF de dos páginas físicas no contenía
  «Segunda página.» ni «Datos de prueba» y cortaba la línea de terminal. Después contiene
  ambos textos, el final «desplazamiento local» y cuatro páginas físicas (la fixture
  incluye espaciadores altos para probar scroll). Extracción con `pypdf`, ya instalado.

Cambios de base acotados: el índice global delega el multipágina; este último mantiene
`aria-current` y limpia páginas ocultas. La copia conserva el DOM del botón y encuentra
el estado en terminal. Print muestra todas las páginas, elimina mínimos de pantalla en
tablas, permite envolver terminal y abre/restaura detalles de datos. El programador de
índice cancela RAF pendiente al activar movimiento reducido y actualiza sin RAF.

No cambia el diseño base, sus anchos ni sus paletas. Las correcciones restauran contratos
documentados de navegación, copia e impresión íntegra.

La exportación del catálogo con Sea activo mostró otro fallo de impresión: terminal,
anotaciones, captions y unidades retenían la tinta pálida de Sea sobre papel blanco.
Se comprobó visualmente la página 8 de un PDF de 13 páginas (`orca pdf`, rasterizado con
`pypdfium2`, ya instalado). Se acotan tokens de tinta/superficie y de terminal a `@media print`;
las tres paletas de pantalla permanecen intactas. Los colores de la librería se definen
también en cada tema antes de cualquier regla print.

Barra multipágina a 320 × 740: `nav` se comprimía a 19,91 px mientras sus botones
ocupaban x=132,84…323,52. El selector empezaba en x=166,75: se superponían. El contenido
medía sólo 324 px, por lo que casi no existía recorrido para separarlos. `flex-shrink:0`
en la navegación mantiene su tamaño natural dentro del desplazamiento local de `.barra`;
no modifica la rejilla del documento.
