# Ocho componentes de evidencia · 15 septiembre 2026

Versión `2026.09.15-evidencia.1`, contrato 4, 82 recetas. La ampliación autorizada incorpora relato visual por pasos, Sankey de dos columnas, cohortes, sensibilidad de escenarios declarados, Gantt editorial, embudo explicado, bandas de incertidumbre e imagen de evidencia ampliable.

## Entrega

`evidencia.html` contiene las ocho demostraciones con datos ficticios, HTML copiable, criterios y límites. `componentes.md` es la fuente de recetas; el ensamblador deriva registro, biblioteca, guía y demostración. El generador detecta `data-evidencia` e incrusta el módulo una sola vez. `SKILL.md` y `casos-uso.json` enseñan a elegir las piezas según la pregunta. Los controles comunes de apariencia, sonido, comentarios e índice siguen en la base estándar.

El módulo `evidencia.js` usa SVG y DOM locales. No agrega red, dependencias de terceros, temporizadores de animación ni RAF. Cada instancia ofrece init/get/select/destroy; destruye sus escuchas y su IntersectionObserver, conserva la fuente y admite volver a inicializarla. Un error de datos muestra un motivo y conserva la tabla o lista original.

## Contratos relevantes

- Sankey conserva un total común entre dos columnas; ancho proporcional a magnitud, cero sin grosor artificial. Hasta 24 conexiones y ocho nodos por lado. No representa ciclos ni un grafo arbitrario de etapas.
- Cohortes muestra numerador, base y porcentaje, con cinco niveles y escala visible. Pendiente sólo al final de una fila; cero observado es distinto. No agrupa eventos automáticamente.
- Sensibilidad ordena por amplitud los dos resultados declarados de cada supuesto frente a una misma base. Admite efectos inversos; no interpola ni combina parámetros ni calcula un modelo financiero.
- Gantt valida fechas UTC, IDs y dependencias fin a inicio, rechaza ciclos y referencias inexistentes. Un hito es un intervalo de duración cero. No calcula días laborables ni ruta crítica.
- Embudo requiere enteros no crecientes de una misma población; muestra conversión desde la etapa anterior, proporción de la base y abandonos. Una base anterior cero no produce una conversión inventada.
- Incertidumbre conserva inferior ≤ central ≤ superior, fechas crecientes y método escrito. Una banda de escenarios no recibe una probabilidad implícita.
- Relato conserva una escala común. IntersectionObserver selecciona evidencia al recorrer pasos; el control manual suspende esa selección automática. En móvil los pasos mantienen sus cifras en texto.
- Imagen conserva el original incrustado, zonas porcentuales, descripción y lista. Zoom entre 100 y 400 %, desplazamiento local y selector alternativo. No aumenta la resolución del original; zonas muy cercanas pueden solaparse y deben revisarse editorialmente.

Valores finitos hasta 10¹², nombres hasta 100 caracteres; restricciones específicas constan en cada receta. La vista redondea a ocho cifras significativas y usa notación científica para extremos. Los valores originales siguen en la tabla. Las regiones anchas se desplazan localmente y tienen nombre y foco; impresión conserva las fuentes.

## Validación

- `scripts/validar.py`: módulos sincronizados, sintaxis JS, CSP, IDs, nueve paletas, contratos estándar y 82 recetas.
- `scripts/probar_contrato.py`: siete grupos correctos, incluida generación individual de todas las recetas y rechazo de bases incompletas.
- `scripts/comprobar_evidencia.py`: 88 comprobaciones correctas de datos, selección, destrucción, inicialización idempotente, extremos numéricos y fechas alineadas con el eje. Resultados en `evidencia-pruebas.json`.
- Geometría a 320×740, 390×844 y 1440×960 en nueve temas: sin desbordamiento global, textos SVG dentro de su vista y acceso al extremo de regiones con desplazamiento local. `evidencia-geometria.json` registra las medidas efectivas.
- Capturas inspeccionadas de las ocho piezas. Orca restablece el tamaño del navegador al capturar; las imágenes de escritorio no acreditan por sí solas las medidas móviles anteriores.
- `scripts/comprobar_evidencia_contexto.py`: los tres pasos cambian mediante IntersectionObserver al desplazar la página; una selección manual persiste al recorrer otro paso. Las 82 fuentes de la guía coinciden exactamente con el registro y las ocho instancias nuevas cargan sin errores. Resultados en `evidencia-scroll.json` y `evidencia-guia.json`.
- Movimiento reducido: cero animaciones en las ocho nuevas piezas. El módulo no introduce RAF.

Las interacciones automatizadas usan DOM y eventos sintéticos; el seguimiento del relato usa el IntersectionObserver del navegador. Estas pruebas no acreditan teclado físico, lector de pantalla, gestos táctiles, audición humana, otros navegadores ni instalación en el MacBook. Las fuentes y el sonido manuscrito existentes no se modificaron en esta ampliación.
