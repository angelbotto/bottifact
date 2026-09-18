# Dirección de interfaz y marca

Revisión del 18 de septiembre de 2026. Alcance: lector compartido, biblioteca, tablas portables y React, controles de apariencia y revisión. La evaluación combina inspección del código, referencias públicas y pruebas de comportamiento; no es un estudio con usuarios ni demuestra ahorro de tiempo.

## Diagnóstico

La sensación de prototipo viene de la acumulación de decisiones locales: demasiados botones con borde completo, símbolos con pesos distintos, controles secundarios que compiten con el contenido y nombres que describen la implementación. Redondear todo no resuelve ese problema. La dirección es reducir ruido y hacer predecibles las acciones.

Hay dos registros que deben convivir: el documento conserva su composición editorial y su tema; la interfaz utiliza controles compactos, familiares y consistentes. La marca no debe obligar a que todos los informes parezcan un dashboard.

## Referencias y decisiones

- [Figma UI3](https://www.figma.com/blog/behind-our-redesign-ui3/): agrupar herramientas en una barra inferior y dar espacio al contenido. Aquí se aplica a lectura, anotación y revisión; no se incorpora una barra de edición gráfica que el producto no tiene.
- [Linear, renovación de interfaz](https://linear.app/now/behind-the-latest-design-refresh): consistencia y menor competencia visual de la navegación. Aquí se traduce en controles secundarios discretos y una acción principal por contexto.
- [NN/g, usabilidad de iconos](https://www.nngroup.com/articles/icon-usability/): los símbolos no siempre son evidentes. Las acciones del administrador conservan texto; los controles compactos del lector tienen nombre accesible y ayuda al recibir foco o pasar el cursor.

Estas son decisiones de diseño propias, no una reproducción ni una asociación con esas marcas.

| Antes | Después | Criterio |
| --- | --- | --- |
| Botones con el mismo peso | Acción principal, secundaria y discreta | El énfasis corresponde a la tarea |
| Comentario y nota dentro de un menú | Accesos directos separados | Reducir pasos sin mezclar privacidad |
| Símbolos heterogéneos | SVG de trazo coherente | Reconocimiento y alineación |
| Barra inferior con controles aislados | Tres grupos en una superficie flotante | Dar orden sin ocupar el documento |
| Acciones de datos sólo con texto | Icono y etiqueta en filtros, diseño y vistas | Escaneo sin sacrificar comprensión |
| «Entidades» | «Empresas y temas» | Usar el vocabulario del trabajo |
| «Guardar tema en favoritos» con símbolo textual | «Guardar tema» con icono | Menor longitud y estado explícito |
| Estilos dinámicos para toda la interfaz | CSS externo en el administrador | Respetar su política de seguridad |

## Sistema de controles

Iconos de 16–19 px, trazo 1.65, sin relleno; estados de foco, selección y deshabilitado explícitos. Bordes suaves y radios de 8 px en controles, 13–17 px en superficies flotantes. Transiciones de color y fondo de 120 ms; se respeta movimiento reducido. En móvil, las herramientas del lector tienen 44 px de área táctil y consideran el área segura del dispositivo.

La barra contiene apariencia; comentario, nota privada y revisión; compartir y más opciones. Las flechas, Inicio y Fin recorren los controles. Escape cierra los menús. Los controles originales conservan la responsabilidad sobre persistencia, permisos y eventos. El generador y el adaptador del portal usan la misma implementación.

Una nota local no se convierte en una nota sincronizada por cambiar su apariencia. Compartir no cambia permisos. El creador mantiene sus herramientas de administración separadas del contenido del lector.

## Redacción de interfaz

Usar verbos y resultados: «Guardar», «Copiar contexto», «Compartir», «Publicar versión». Mantener texto en acciones ambiguas o de impacto. Explicar consecuencias antes de publicar o cambiar audiencia; no esconderlas en un tooltip. Los estados deben decir qué ocurrió y qué puede hacerse después. Los detalles de servidores y almacenamiento pertenecen a documentación operativa, no al documento compartido.

Los términos «comentario», «nota privada», «borrador» y «versión compartida» tienen significados distintos. La brevedad no debe borrar esas diferencias.

## Nombre propuesto

**Margen** es la dirección recomendada: una palabra corta, editorial y vinculada al espacio donde una observación se convierte en una decisión. Descriptor: **Documentos, decisiones y contexto.** Firma posible: **Margen by Botto**. El nombre funciona para un informe, una biblioteca y un paquete abierto; no depende de un proveedor de IA.

Es una propuesta de posicionamiento, no una marca elegida ni una verificación de disponibilidad. Hay usos comerciales de [MARGEN](https://www.trabajaconmargen.com/); habría que revisar dominio, mercados y marca antes de adoptarla.

Se exploraron y descartaron por proximidad: [Atrio](https://atrio.cc/) ya aloja dashboards con permisos; [Rastro](https://www.rastro.tools/) trabaja con documentos y grafos; [Pliego](https://pliegoapp.com/terminos) ya es software documental; [Lintra](https://www.lintra.com/) y [Relatum](https://relatum.dev/) también tienen usos tecnológicos. No conviene resolver la búsqueda con otro nombre genérico sin investigar.

El paquete, skill, dominio e identificadores siguen siendo Bottifact. Una futura migración deberá conservar aliases, actualizador, configuración personal, IDs y enlaces compartidos, con un período de compatibilidad.

## Próximas mejoras con mayor valor

1. Probar con personas tres recorridos: encontrar un informe, comentar un dato y devolver contexto a su agente. Registrar dónde dudan y cuántos pasos requieren, antes de ampliar la interfaz.
2. En revisión, priorizar pendientes y la cita del documento; ofrecer respuestas y resolución con historial y confirmación apropiada. No añadir una conversación paralela que pierda su ancla.
3. En el grafo, comenzar por empresa, proyecto o pregunta y explicar cada conexión; mantener lista y búsqueda como caminos equivalentes. La densidad visual no demuestra conocimiento.
4. Añadir controles visuales de regresión con fixtures sintéticos en claro, oscuro y móvil. Las capturas de cuentas reales no entran en documentación pública.
5. Consolidar gradualmente los patrones repetidos de diálogos y estados vacíos. No hace falta reescribir el lector portable en React para compartir un lenguaje visual.

La versión publicada del ejemplo demuestra el nuevo sistema; los HTML históricos permanecen inmutables. El adaptador actualiza la barra del lector alojado, pero para renovar tablas y estilos del documento hay que generar y publicar otra revisión.
