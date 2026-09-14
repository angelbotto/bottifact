# Segunda tanda · 14-sep-2026

Encargo autorizado por Angel: ampliar para reportes, artefactos, artículos y visualización
de prototipos; ejecutar la tanda propuesta y mejorar apariencia/legibilidad.

Se conserva la rama nota-libreria y la instalación tikin-629/libreria. Base a2307b2.

## Alcance a construir

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

Pendiente de ejecución. Se registrará por separado de la auditoría de la primera tanda.
