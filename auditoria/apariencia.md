# Llave de apariencia · 14-sep-2026

Angel pidió sustituir el grupo de temas visible por una llave pequeña sol/luna que
abra las paletas, ofrecer variantes y explorar temas más allá del color.

Implementado: disclosure nativo `details`/`summary`, SVG sol/luna según tema efectivo,
panel con cuatro opciones (Claro, Cálido, Dark Sea, Sistema), muestras de papel/tinta/acento,
y tres variantes copiables: círculo, etiqueta y cápsula con nombre del tema. La cabecera
extrae el círculo desde componentes.md para no mantener dos versiones distintas.

Además del color: títulos Editorial (original), Sobrio (Geist) y Técnico (Geist Mono),
lectura cómoda y trama de papel. No se cambia la familia del cuerpo ni de los datos.
Las opciones son independientes y sólo se restauran donde existen sus controles.
La tipografía original y los selectores anteriores se conservan en artefactos existentes.
La trama usa CSS local; ningún recurso ni dependencia nueva. Todos los nuevos colores
están definidos en claro, oscuro del sistema, oscuro explícito y Sea.

El panel se mantiene dentro de la ventana, no tapa su disparador y tiene desplazamiento
local cuando falta altura. Escape devuelve foco, pointerdown fuera cierra, focusin fuera
cierra sin desplazar foco. Sólo un panel abierto. No hay animación, RAF ni sonido propios.
Sin JS: disclosure en el flujo; preferencias sin efecto, contenido legible.

## Verificación ejecutada

- Ensamblar y validar pasan en los cuatro HTML. El validador comprueba también aria-controls,
  regiones del panel y los cuatro juegos de tokens de apariencia.
- `scripts/comprobar_apariencia.py`: 8 contratos de interacción y 21 regresiones de la
  tanda anterior; evidencia en apariencia-interaccion.json / apariencia-regresion.json.
- 54 combinaciones: 320×740, 390×844, 1639×939; tres colores × tres estilos × extras
  apagados/encendidos (lectura cómoda y trama). CSS computado y DOM: documento sin
  desbordamiento, títulos sin corte, panel completo en ventana, disparador libre,
  desplazamiento local alcanzable. Texto principal/secundario del panel supera 4,5:1
  tanto en fondo normal como seleccionado; cuerpo/secundario sobre la peor mezcla
  de trama al 38% supera 4,5:1. `apariencia-pantallas.json` contiene cada medición.
- `multipagina.html`, con preferencias guardadas de Técnico/trama/cómoda: conserva
  ausencia de atributos optativos y cuerpo16px. `apariencia-ejecucion.json`.
- Ventana baja320×568: panel de92 a556px, región de462px de alto y618px de contenido,
  extremo del scroll156px alcanzable. `comprobar_apariencia_salida.py`.
- Movimiento reducido emulado con Orca: controles sin transiciones calculadas.
- PDF Sea/Técnico:20 páginas; texto extraído con pypdf confirma tabla y alternativa
  del visor, controles excluidos. La regla print elimina la trama. `apariencia-salida.json`.
- Capturas Orca en capturas/apariencia-*; inspección visual de móvil y variantes.

## Límites del método

El host actualiza activeElement con focus() pero no entregó eventos focus/focusin en
esa operación (registro observado vacío). La prueba de cierre usa focusin explícito;
Escape y pointerdown también se ensayan con eventos. No acredita teclado físico ni
lector de pantalla. No prueba de teléfono físico ni zoom200%. La impresión se comprueba
por extracción del PDF, no por una impresora física. Fuentes de medidas: scripts y JSON
anteriores, no cmrg.me; son decisiones nuevas solicitadas para este control.
