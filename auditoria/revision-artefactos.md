# Revisión sobre capturas · TIKIN-629

## Cambios pedidos por Angel

- El trazo discontinuo a todo el ancho era el foco de article.pagina. El foco del capítulo se representa ahora en su título; no se quita la señal de foco del teclado. Summary abierto tiene 16 px de separación respecto a sus dependencias.
- Copia: cabecera de código y terminal pasa a dos columnas; el estado ocupa otra fila y desaparece cuando está vacío. Botón al extremo derecho con área mínima 44×44 px. El icono se centra en esa área.
- Resaltado HTML local: etiquetas, atributos, valores y comentarios en los tokens existentes; sólo nodos de texto/span. La cadena que se copia se mantiene exacta.
- Grano de papel: SVG feTurbulence monocromo incrustado, semilla 17, varias octavas, estático y sin solicitudes. Sustituye el punteado regular porque el usuario pidió textura de papel. Se desactiva en impresión.
- Escritura: `data-al-ver` optativo ejecuta una primera animación al alcanzar 30 % de visibilidad de la caja. Sigue cancelándose al ocultar/reducir movimiento. Entrar al viewport no dispara audio; activar el canal y pulsar Repetir sí permite acompañarla con la señal breve existente.
- Terminal: su texto tenue daba 3,94:1 en la superficie #171614 y 4,29:1 en Sea. Corrección real de contraste: #998f83 y Sea HSL(212 22% 58%). Fuente de las mediciones: colores calculados por Orca y fórmula de luminancia WCAG; no números de una referencia externa.

## Nuevos componentes y flujos

Tabla exploradora con búsqueda insensible a acentos, filtro de estado, grupos semánticos, orden estable y suma de filas visibles. Contrato explícito de cuatro columnas e importe COP; no pretende ser un datagrid arbitrario.

Cards de artículo, indicador con cobertura y proyecto con estado y acción. No se hacen clicables contenedores con controles anidados.

Visor: importar HTML local declarativo, Móvil/Escritorio, conservar anchos CSS, reiniciar a la fuente original. Rechaza iframe, scripts, manejadores, recursos externos, envíos y CSS url()/@import. El contenido sigue siendo de confianza: no se afirma sanitización de código hostil ni compatibilidad con sitios remotos.

Comentarios: barra local, selección de texto o elección de bloque por clic/Tab+Enter, diálogos nativos, marcas numeradas, lista, editar, borrar, volver al bloque y prompt copiable. No red ni almacenamiento; el usuario debe copiar antes de recargar. No comentarios dentro del Shadow DOM ni coordenadas de imagen. Alcance explicado junto a la receta.

43 recetas en nueve capítulos. No se añade una dependencia remota. Las fuentes y métodos siguen en componentes.md y SKILL.md.

## Verificación ejecutada de los cambios nuevos

`python3 scripts/comprobar_revision.py`: ocho casos de interacción (tabla, cards, importación/rechazo/reset, comentarios por teclado DOM, edición/borrado/destroy, audio apagado); 18 combinaciones de viewport y seis paletas (320×740, 390×844, 1440×960), límites de barra y diálogo, área/alineación de copia y contraste de colores del código y terminal >=4,5:1. Los 43 códigos coloreados se compararon carácter por carácter contra registro.json.

Escritura verificada en el navegador de Orca: sin animaciones fuera del viewport; seis trazos activos al entrar y audio apagado; cero animaciones al reducir movimiento. Preferencia emulada por Orca y MediaQueryListEvent explícito para verificar listener. No se afirma gesto físico de SO ni audición manual.

Captura revision-codigo.png inspeccionada: color de código, botón a la derecha, grano y separación. Evidencia: revision-interaccion.json, revision-pantallas.json, revision-escritura.json. Eventos de teclado/selección se comprueban por DOM; no equivalen a prueba física con lector de pantalla.

La regresión completa `python3 scripts/comprobar_biblioteca.py` pasó de nuevo con 43 recetas: 162 combinaciones, ocho interacciones de edición, ocho de capítulos y 21 del catálogo. PDF: 39 páginas con todos los capítulos; recupera la vista activa. También pasaron las 15 comprobaciones originales de componentes y cuatro de audio offline (tres señales y cancelación de resume), sin audición manual. Se verificó «Ver fragmento» desde otro capítulo y se inspeccionó revision-comentarios-390.png. Las referencias exportadas evitan los IDs temporales añadidos por las marcas.
