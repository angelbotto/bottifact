# Pulido de interacción · TIKIN-629

Responde a la petición de Angel sobre comentarios flotantes, tablas, visor, grano, escritura, sonido y código. Plan previo en Linear: comentario `47fc6d5e-464b-4b68-9feb-e88cd9909cb5`.

## Referencias de criterio

- [Figma, rediseño de comentarios](https://www.figma.com/blog/stay-in-the-flow-with-redesigned-comments/): pines y edición en contexto.
- [Guía de comentarios de Figma](https://help.figma.com/hc/en-us/articles/360039825314-Guide-to-comments-in-Figma): el modo de comentario suspende las acciones del documento.
- [Data Table de shadcn](https://ui.shadcn.com/docs/components/base/data-table): búsqueda visible, controles de columna y orden contextual.
- [Retool Table](https://retool.com/blog/supercharging-the-retool-table): herramientas de filtro y agrupación asociadas a la tabla.

Son referencias de interacción consultadas en esta iteración. Las dimensiones de Nota son decisiones propias; no se atribuyen a una captura ni a cmrg. El inventario medido original permanece en referencia-cmrg.md.

## Cambios y correcciones

- `revision.js`: capa fija de pines, fuera del flujo. El editor es un diálogo no modal de hasta 304 px; el pin mide 28 × 30 px. Contexto plegado, lista y prompt con capítulo, referencia estable, fragmento y coordenadas relativas. El modo Comentar suspende enlaces/controles dentro del documento. Edición desde otro capítulo abre el capítulo del comentario. `destroy()` retira capas y referencias temporales.
- `controles.js`, `explorador.js`: búsqueda y menús de filtro, agrupación, columnas y orden. Paneles limitados al viewport, Escape devuelve foco; scroll exterior y clic fuera cierran. API anterior y tabla HTML intactas.
- `visor.js`: ancho de dispositivo, cinco proporciones, rotación y escala para encajar. Estado separa dimensiones CSS de porcentaje visual. Shadow DOM, alternativa textual y restricciones de HTML local se conservan. La composición de informe también usa la nueva barra.
- `audio.js`: interruptor central en Apariencia; empieza apagado y vuelve a apagado al ocultar pestaña. Sólo botones marcados y eventos reales reproducen. Señal de lápiz de 650 ms y ganancia pico programada 0,045; señales breves de 90 ms y pico 0,018. Fuente: parámetros del módulo, no nivel acústico medido. `sonido.js` mantiene los canales independientes y añade el lápiz para recetas copiadas sin cabecera.
- Escritura en Edición, enlazada desde Apariencia; entrada al viewport en silencio, repetición explícita con sonido optativo. El acceso se oculta si el documento no incluye escritura.
- `codigo.js`: nueve lenguajes, nodos de texto seguros; conserva resaltado manual y contenido copiable. El léxico distingue comentarios por lenguaje.
- Trama: mismo SVG de ruido incrustado para cuerpo y cabecera de capítulos.
- Bug real: una regla de Apariencia ocultaba todos los `span` de un botón apagado, incluido el nombre del interruptor. Ahora se limita a las marcas decorativas.
- Bug real: el renderizador de guía dejaba `**` literales cuando un énfasis Markdown atravesaba un salto de línea; se admite ese salto en el formato inline.

## Evidencia

Los scripts `comprobar_pulido.py`, `comprobar_revision.py` y `comprobar_biblioteca.py` guardan resultados y dimensiones calculadas en JSON junto a este archivo. Las capturas `pulido-*` permiten inspeccionar tabla, visor y burbuja. No son mediciones de hardware móvil ni de un lector de pantalla.

La prueba de audio distingue preparación DOM de apertura/foco del menú y clics nativos de Orca (`isTrusted`). La síntesis offline mide muestras, envolvente y cancelación, sin afirmar audición manual. La preferencia de movimiento reducido se emula y se notifica explícitamente al MediaQueryList para probar la cancelación.

## Límites mantenidos

Los comentarios son un borrador en memoria: copiar antes de recargar, indicado en el panel. No colaboración remota ni comentarios dentro del Shadow DOM. Un punto relativo puede cambiar respecto a una palabra al redistribuirse texto; el prompt conserva el fragmento. El visor no es un navegador remoto ni un emulador; usa HTML de confianza y consultas de contenedor. Ajustar reduce visualmente el texto; 100 % sirve para evaluar legibilidad. Los menús no convierten la tabla local de cuatro columnas en una grilla con servidor o virtualización.

## Resultado ejecutado

- Ensamblado y validación estática: seis documentos y 44 recetas correctos.
- `comprobar_pulido.py`: ocho contratos y 144 aperturas de menú correctas, seis colores a 320×740, 390×844 y 1440×960. Clic nativo en activación y repetición; scroll sin reproducción, apagado sin voces.
- `comprobar_revision.py`: ocho contratos, 18 combinaciones de geometría y contraste, fuentes copiables y escritura al entrar/cancelación por movimiento reducido.
- `comprobar_biblioteca.py`: 162 combinaciones, ocho comprobaciones de edición, ocho de capítulos, 21 del catálogo y exportación PDF.
- Repaso final: 15 comprobaciones originales de componentes; cinco de audio offline a 48 kHz, incluido lápiz (última muestra sobre umbral a 649,79 ms) y cancelación de resume; ocho contratos del pulido, edición de comentario desde otro capítulo y los 44 HTML comparados carácter por carácter.
- Después de pulir tipografía y centrar el visor: 12 repasos del menú de dispositivo en los seis colores a 320 y 390 px; entradas calculadas a 16 px. Evidencia en `pulido-movil-final.json`. Capturas finales de tabla y visor inspeccionadas a 1024×900; burbuja a 390×844.
