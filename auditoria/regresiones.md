# Regresiones reproducidas · TIKIN-629

13-sep-2026. Orca, navegador incrustado, viewport 1639 × 939. Fixture `pruebas.html`
generada por `scripts/fixture_regresion.py`. Observaciones anteriores a la corrección:

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
