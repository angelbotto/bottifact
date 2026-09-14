# Edición completa · TIKIN-629

## Referencias consultadas el 14 de septiembre de 2026

- https://ui.shadcn.com/docs : código abierto a modificación, composición y distribución de componentes con dependencias. Aplicación aquí: recetas propias, HTML visible y registro local generado. No se copia su lenguaje visual ni se declara compatibilidad con su CLI.
- https://ui.shadcn.com/docs/registry : un registro puede distribuir componentes, páginas, configuración y otros archivos; no se limita a React. Aplicación: inventario versionado de 40 recetas con dependencias explícitas.
- https://docs.ghost.org/themes/structure : plantillas separadas para lista, artículo, página, autor y etiqueta; parciales compartidos. Aplicación: portada/archivo, piezas de artículo y autoría; no se entrega un tema Ghost instalable.
- https://docs.ghost.org/themes/custom-settings : configuración tipada, grupos de contexto y valores por defecto; cambiar claves pierde valores anteriores. Aplicación: configuración editorial local versionada, lista/rejilla, extractos y metadatos; color y tipografía ya tienen su propio control.

La referencia original cmrg.me y sus medidas siguen en referencia-cmrg.md y las auditorías previas. Esta ampliación no atribuye a cmrg los nuevos componentes ni inventa nuevas mediciones de esa web.

## Alcance construido

Nueve capítulos y 40 recetas documentadas; ocho nuevas: archivo buscable, autor, relacionadas, anotaciones, revisiones, criterios, riesgos y configuración editorial. Registro JSON generado desde las mismas fuentes. Navegación profunda optativa, conservando la multipágina anterior. La edición de cuatro capítulos sigue siendo el ejemplo narrativo completo; biblioteca.html es la referencia organizada para construir.

Los tamaños añadidos son decisiones propias: archivo min 250 px por columna; plano SVG 720 × 210; controles min 44 px; titular de ficha 28 px / 1.2; tarjeta de navegación 30 px / 1.15. Fuente de estos números: sección 17 de estilo.css y HTML de la receta anotaciones, no medidas de una web externa. Todos los colores se resuelven desde --pieza-* existentes en las seis paletas.

No se implementan servicios de newsletter, pagos, comentarios, cuentas ni instalación Ghost. No hay nuevas dependencias de ejecución. Sonido y WebGL conservan sus contratos previos; editorial.js no usa RAF, transiciones, red ni almacenamiento.

## Correcciones encontradas durante esta ampliación

- La documentación junto al visor contenía una llamada larga y las dependencias de Three una URL larga. Al abrir el código, provocaban desbordamiento a 320 px. Se permite partir palabras sólo en la documentación de la biblioteca; el código de los ejemplos sigue desplazándose localmente.
- El archivo nuevo usaba `data-tema` para la categoría de publicaciones. Ese atributo ya pertenece al `<select>` de apariencia: la inicialización del cuaderno fallaba intentando leer `options` de un artículo. Se cambió **el atributo nuevo** a `data-publicacion-tema`, conservando la API de apariencia existente. El validador ahora detecta reutilizar `data-tema` fuera de un select. Esto es una corrección de esta ampliación, no un cambio silencioso del sistema publicado.

## Verificación ejecutada

- `python3 scripts/ensamblar.py` y `python3 scripts/validar.py`: seis HTML sincronizados, CSP, IDs, regiones, rejilla, seis paletas, sintaxis JS y 40 entradas del registro.
- `python3 scripts/comprobar_biblioteca.py`: navegador integrado de Orca, UA Chrome 150 en macOS; 162 combinaciones (320×740, 390×844, 1440×960 × seis paletas × nueve capítulos). Medición DOM/CSS de ancho, regiones desplazables, contraste de tokens y rótulos SVG. Abre también la documentación copiable para detectar cortes ocultos.
- Ocho pruebas de interacción nuevas; ocho regresiones de capítulos y 21 del catálogo anterior, todas pasan. Se ejercitan búsqueda con acentos, filtros combinados, estado vacío, reset, destroy/init, configuración CSS/JSON, enlace profundo, foco DOM e historial Atrás/Adelante.
- `python3 scripts/comprobar_biblioteca_apariencia.py`: 12 combinaciones reales del control sol/luna a 320/390 px; paleta, luminosidad del icono y límites del panel. El enlace del configurador abre el archivo sin perder su presentación.
- Exportación PDF desde el capítulo Prototipos: 36 páginas; incluye contenidos de los otros capítulos y recupera el capítulo activo. Capturas inspeccionadas en `capturas/biblioteca-inicio.png`, `biblioteca-archivo.png` y `biblioteca-390.png`.

Evidencia JSON en `biblioteca-*.json`. Los checks de foco usan DOM/eventos programáticos: no acreditan lector de pantalla, teclado físico, audición manual ni hardware móvil. No se ejecutó Ghost/GScan. El fallback sin JS está documentado e incluido; esta ronda no deshabilitó JavaScript en el navegador.

`python3 scripts/comprobar_biblioteca_movimiento.py` también pasó: escena XYZ visible con RAF activo; cambiar a Inicio cancela RAF y el observer marca la escena fuera de pantalla; movimiento reducido detiene RAF y el contador de dibujos. Método: preferencia emulada por Orca y evento MediaQueryListEvent explícito para verificar el listener, porque el host entrega ese cambio de forma intermitente. No se afirma un cambio físico del ajuste del sistema. Evidencia en `biblioteca-movimiento.json`.
