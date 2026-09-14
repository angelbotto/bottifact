# Segunda tanda · 14-sep-2026

Encargo autorizado por Angel: ampliar para reportes, artefactos, artículos y visualización
de prototipos; ejecutar la tanda propuesta y mejorar apariencia/legibilidad.

Se conserva la rama nota-libreria y la instalación tikin-629/libreria. Base a2307b2.

## Alcance construido

- Apariencia con muestras etiquetadas, sistema y lectura cómoda optativa.
- Ficha de decisión, cronología, cascada, conciliación, pequeños múltiples,
  calculadora de escenarios y globo narrado.
- Ficha editorial, referencias con retorno, glosario y metodología desplegable.
- Antes/después, visor de prototipos con anchos reales y estados navegables.
- Catálogo con búsqueda de recetas, ejemplos y HTML copiable junto a cada pieza.

El visor usa Shadow DOM y consultas de contenedor: no necesita iframes bloqueados
por la CSP. No promete emular el navegador de un teléfono ni ejecutar una app remota.
El globo narrado reutiliza NotaGlobo, sin tocar su shader ni crear otra carga de Three.
No se modifican paletas/tamaños de documentos previos; la lectura cómoda es optativa.
Las nuevas decisiones visuales (muestras de tema, rótulos más grandes) responden al
pedido explícito de Angel. No son medidas atribuidas a cmrg.me.

Más ideas para posteriores tandas: bibliografía por tipo de fuente, historial de
revisiones de artículos, galerías con pies extensos, anotaciones sobre capturas,
comparación de alternativas de prototipo, documentación de estados vacíos y de error,
secuencias API, matriz de criterios y cohortes.

## Verificación

- `python3 scripts/ensamblar.py` y `python3 scripts/validar.py`: pasan los cuatro HTML,
  CSP, sincronización de fuentes, IDs, rejilla, sintaxis JS y tokens de los cuatro selectores.
- Validador de skill-creator `quick_validate.py .`: válido.
- `python3 scripts/comprobar_segunda_tanda.py`: 21 pruebas nuevas y 15 de la base;
  evidencia en `segunda-componentes.json` y `segunda-base.json`.
- Navegador de Orca/WebKit: 320×740, 390×844 y 1639×939; Claro, Cálido y Sea;
  lectura normal y cómoda: 18 combinaciones. Anchos reales, scroll local alcanzable,
  nombres/foco de regiones, cajas de texto SVG dentro del viewBox y contraste calculado.
  Texto nuevo ≥4,5:1 y marcas de la cascada ≥3:1 en los tres temas. Los números se
  calculan desde CSS computado y geometría DOM/SVG, no se atribuyen a cmrg.me.
  Registro: `segunda-navegador.json`; navegador/fecha en `segunda-ejecucion.json`.
- Inspección visual de seis capturas en `capturas/segunda-*`: apariencia390 claro,
  cascada1639 cálido, múltiples1639 claro, visor320 Sea y1639 claro, recorrido1639 cálido.
  Apariencia capturada de nuevo tras separar 8px el control Lectura cómoda.

- `python3 scripts/comprobar_segunda_salida.py`: 10 comprobaciones de ancla inicial,
  ciclo del globo, movimiento reducido, transiciones, foco programático y salida PDF.
  Reducir se emula con Orca y el listener recibe MediaQueryListEvent explícito; visibilidad
  usa scroll real/IntersectionObserver. El foco se verifica con focus() y presencia de la
  regla CSS, no navegación física. Método detallado en `segunda-salida-metodo.json`.
- PDF del catálogo en Sea: 20 páginas; `orca pdf` y extracción con pypdf confirman
  tablas, método desplegado, resultados, relato y alternativa del visor. Los details
  recuperan su estado tras imprimir. Evidencia: `segunda-impresion.json`.

Correcciones dentro de esta tanda: cifras diminutas ya no aparecen como cero, coordenadas
geográficas fuera de rango se rechazan, etiquetas largas reservan la altura que realmente
ocupan, y la lista nativa del globo sincroniza la etapa del relato. El catálogo corrige el
salto inicial al ancla después de insertar gráficas/cargar fuentes, sin reposicionar si el
lector ya intervino. No se cambió el comportamiento del globo base: la ruta seleccionada
mantiene su orientación; Vista inicial libera esa selección, documentado en la receta.

Límites de esta verificación: no acredita teléfono físico, zoom del navegador al 200%,
teclado físico, lector de pantalla ni audición manual. La auditoría de la primera tanda
se conserva por separado. El visor usa ancho de contenedor, no emulación de dispositivo.
