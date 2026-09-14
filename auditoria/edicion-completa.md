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
