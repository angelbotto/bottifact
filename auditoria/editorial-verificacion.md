# Composición editorial, tooltip y lápiz — TIKIN-629

Propuesta previa en Linear: 90ef0f55-9450-4ccb-a405-684acfd43e8f.

## Referencia observada

Orca, estilos calculados y DOM de cmrg.me. `/now` a 1440×960: navegación 1024×32,
enlaces 13.7 px/19.5714 px, conversación con separación 8 px y padding 12×16 px,
proyectos separados 24 px y estados con símbolo separado 4 px, fila 24 px.
En `/#top`, la navegación restableció el viewport a 1639×939: líneas discontinuas de
1 px, prolongación 64 px, máscaras horizontales 15 %/85 % y verticales 35 %/65 %.
Los valores originales están en `editorial-referencia-*.json`; la invitación se inspeccionó
en `/shelf`. No se enviaron formularios de la referencia ni se copiaron sus portadas.

La adaptación usa un marco que reserva 12–32 px dentro de la caja y desvanece únicamente
las líneas, sin offsets negativos ni máscaras sobre texto. Las cubiertas de la estantería
son originales de CSS; el semitono es CSS estático. Se reutilizan tokens completos de las
seis paletas, no colores locales exclusivos del modo oscuro.

## Implementación

Ocho recetas nuevas (65 en total): marco, estantería, invitación, estados, proyectos,
conversación, navegación y footer. HTML íntegro, criterio y límites en componentes.md.
La barra principal utiliza la variante editorial; la fila de capítulos tiene desplazamiento
local propio y conserva índice y regla. Las barras anteriores siguen disponibles.

El tooltip del attention map contiene valor, porcentaje redondeado a un decimal, total y
contexto opcional tomado del texto de la fila. Ratón/foco/toque, Escape, permanencia al pasar
al tooltip y limpieza en destroy. El foco conserva el tooltip al desplazar; el puntero lo cierra.

Angel pidió sonido durante la escritura: `data-escritura-sonora` es un opt-in nuevo además
de la activación real de Sonidos. Sin el atributo se conserva la entrada silenciosa. El lápiz
usa una única fuente de ruido filtrado, dura lo mismo que el trazo y se corta con finish,
salida, movimiento reducido, ocultación y apagado. Hover no interrumpe una escritura activa.
No se sonorizan eventos genéricos de scroll ni foco.

## Bug encontrado

`fitLabels()` comparaba `scrollWidth` entero con anchuras fraccionarias de foreignObject.
Ejemplo medido: 558 contra 557.6226 px; 223 contra 222.717 px. La diferencia de redondeo
sustituía incluso rótulos que cabían por números. Se añadió tolerancia de 1 px, manteniendo
la protección para desbordes reales. Evidencia: editorial-etiquetas-diagnostico.json.

## Verificación

- `python3 scripts/ensamblar.py` y `python3 scripts/validar.py`.
- `scripts/comprobar_editorial.py`: tooltip, Escape, foco/evento DOM, permanencia, destroy/init,
  copia de texto literal con portapapeles simulado, validación de vacío y semántica de listas.
  180 combinaciones: diez piezas × seis temas × 320×740, 390×844 y 1440×960. Anchos del
  documento, extremos del marco, cubiertas y tooltip. Navegación móvil al último capítulo.
- `scripts/comprobar_lapiz.py`: botón de Sonidos y repetición con clic nativo de Orca;
  lápiz durante entrada, sigue activo tras 850 ms adicionales, cancela al salir y no vuelve
  a sonar por reentrada. Reduce mediante evento MQL explícito cancela animación/voces.
  Apagado y tooltip con movimiento nativo del puntero también comprobados.

- `scripts/comprobar_biblioteca.py`: 162 combinaciones, ocho interacciones, regreso entre
  capítulos/recetas, regresiones del informe y catálogo anterior e impresión PDF.

- Tras corregir el redondeo de rótulos se repitieron contratos y 18 combinaciones del mapa
  (tres tamaños × seis temas), comprobando al menos tres etiquetas grandes conservadas.

- Regresión de hover y lápiz breve: `comprobar_gesto_audio.py` retira
  `data-escritura-sonora` para verificar la variante anterior de entrada silenciosa. Dos hover,
  una repetición sonora y apagado; scroll y foco no añaden señales.

- Apariencia a 320×740: panel entre x=12 y x=308, y=62 y y=728,
  región nombrada con foco y desplazamiento vertical local. Captura incluida.

No audición manual, lector de pantalla ni dispositivo móvil físico. El formulario sólo copia;
no tiene backend ni persistencia. El ensayo del portapapeles simulado comprueba el texto generado,
no la entrega al portapapeles del sistema. La escritura es un alfabeto SVG acotado, no cualquier fuente.
