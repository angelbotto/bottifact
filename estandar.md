# Contrato de nuevos artefactos de Angel

El contrato 2 incorpora marcos punteados difusos en las figuras anchas. La base incluye **una llave sol/luna**, seis paletas con muestras y Sistema, controles de sonido,
comentarios flotantes, índice por página y regla de lectura. Es la composición predeterminada de
los nuevos HTML de Angel. No exige llenar cada artículo con todos los componentes; selecciona
las piezas a partir de las 71 recetas vigentes. Una excepción explícita de Angel prevalece.

## Crear una página

Escribe sólo el contenido de la hoja en un archivo UTF-8. No copies cabecera, estilos, scripts,
comentarios ni el panel de apariencia: los incorpora el generador desde sus fuentes canónicas.
Cada `h2` necesita un ID propio o en su sección. Las figuras anchas son hermanas de las secciones,
no hijas de ellas. Ejemplo completo de contenido:

```html
<section id="decision">
  <h2>Una decisión pendiente</h2>
  <p>Antes de avanzar, necesitamos confirmar la fuente y el alcance.</p>
</section>
<section id="evidencia">
  <h2>Evidencia disponible</h2>
  <p>Enlaza aquí la fuente real y explica lo que permite concluir.</p>
</section>
```

Ejecuta desde el directorio de este skill (o usa la ruta absoluta de los scripts):

```bash
python3 scripts/crear_artefacto.py --contenido /tmp/contenido.html --titulo 'Una decisión pendiente' --salida /tmp/informe.html
python3 scripts/validar_artefacto.py /tmp/informe.html
```

El resultado es un HTML autocontenido listo para abrir como artefacto. Conserva el archivo de
contenido para regenerarlo al editar; no modifiques a mano las copias incrustadas de los módulos.
La salida reemplaza el archivo indicado; el generador rechaza sobrescribir el contenido fuente.

## Crear capítulos

Usa un JSON con `titulo`, `descripcion` opcional y `paginas`. Cada página tiene `id`, `titulo`
y `contenido`, una ruta relativa al JSON. Los IDs son únicos, minúsculos, con números y guiones.

```json
{
  "titulo": "Revisión del proyecto",
  "paginas": [
    {"id": "decision", "titulo": "Decisión", "contenido": "decision.html"},
    {"id": "evidencia", "titulo": "Evidencia", "contenido": "evidencia.html"}
  ]
}
```

```bash
python3 scripts/crear_artefacto.py --config /tmp/informe.json --salida /tmp/informe.html
python3 scripts/validar_artefacto.py /tmp/informe.html
```

Hay una muestra reproducible en [ejemplos/estandar-capitulos.json](ejemplos/estandar-capitulos.json),
y resultados completos en [estandar.html](estandar.html) y [estandar-capitulos.html](estandar-capitulos.html).
El generador incorpora los módulos que requieren los atributos declarativos de las recetas,
en su orden, una sola vez. `recorrido` ofrece el globo declarativo; una instancia programática
personalizada de NotaGlobo necesita una extensión explícita del generador, no un script improvisado.
La receta `configuracion` referencia el archivo editorial: incluye también `archivo` o adapta ese destino.

## Qué comprueba y qué no

El verificador exige controles, módulos, seis paletas, referencias internas, rejilla y regiones
con foco/nombre. Comprueba CSS y JS contra las fuentes instaladas y registra sus hashes en un
manifiesto. Detecta una copia vieja al compararla con el skill actual; no migra documentos ni
promete compatibilidad binaria entre versiones. No modifica artefactos publicados.

El contrato es una composición de la biblioteca, **no un sanitizador de contenido no confiable**.
No admite scripts personalizados, CSS adicional fuera de los prototipos declarativos, iframes
ni recursos remotos. Para extender la biblioteca, añade primero una implementación documentada,
sus dependencias y su verificación; no desactives el control para conseguir un resultado verde.
Los ejemplos antiguos conservan su compatibilidad, pero no todos cumplen este contrato nuevo.

La comprobación estructural no acredita accesibilidad completa ni comportamiento: abre el
resultado a 320, 390 y 1440 px, prueba las seis paletas, foco, desplazamiento local, capítulos,
pines, exportación del prompt y movimiento reducido. Usa un clic real para Probar sonido.
En capítulos, sin JavaScript se ofrece lectura continua; los controles interactivos necesitan JS.

## Sonido que se puede comprobar

Apariencia abre con Sonido: interruptor, **Probar sonido**, volumen y estado. El botón de prueba
activa el audio y emite un tono de 450 ms. El interruptor solo activa/desactiva; activarlo no
reproduce nada. El volumen inicial es 65 %, independiente del volumen del dispositivo. El lápiz
sigue la duración de la escritura; no es una grabación de la referencia.

Empieza apagado en cada carga y se apaga al ocultar la pestaña. `data-escritura-sonora` permite
acompañar el trazo visible una vez habilitado; `data-audio-hover` requiere movimiento real del
ratón. Nunca suena por foco o scroll genérico. Movimiento reducido cancela la escritura y su audio.
Si el contexto no puede arrancar o el navegador lo pausa, el estado explica cómo reintentarlo.

Un contexto `running` y una señal distinta de cero no prueban que el usuario la escuche: también
intervienen la pestaña silenciada, el volumen y el dispositivo de salida. En una vista remota hay
que identificar dónde ejecuta el navegador. Para la prueba del MacBook abre la URL de Tailscale
en su propio navegador y pulsa Probar sonido; no asumas que una captura remota retransmite audio.

## Comentarios incluidos

Una sola instancia de `revision.js`, con su montaje oculto de la receta, crea los controles
flotantes. No pongas una caja grande en el flujo. El contador abre los comentarios y el prompt
con referencia y fragmento; los pines se anclan al contenido. No hay envío, colaboración remota
ni persistencia: copia el prompt antes de cerrar o recargar. Una nueva sesión empieza sin notas.

El diagnóstico, las pruebas ejecutadas y las prioridades que aún faltan están en
[auditoría de estandarización](auditoria/estandarizacion.md).
