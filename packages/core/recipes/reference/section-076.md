## Contrato común de la ampliación analítica

Copia las dependencias indicadas en el registro, incrustadas en un `<script>` cada una. Las
recetas completas anteriores son la fuente de datos; no necesitan objetos JS paralelos.
`NotaAnalitica.init(raíz)` devuelve las instancias nuevas o existentes y
`NotaAnalitica.get(figura).destroy()` retira controles y SVG conservando la tabla original.
Si corriges una entrada inválida, vuelve a llamar `init`; el aviso anterior se elimina.
No modifica una instancia al editar su tabla: destrúyela y vuelve a inicializar para actualizar.
Las etiquetas de ejes deben ser breves; las explicaciones largas pertenecen a caption/figcaption.
La selección permite consultar valores exactos; no filtra ni recalcula series o totales.
El calendario puede plegar su tabla con `details`: se despliega completa al imprimir.

`NotaEscena` conserva su contrato para XYZ y etapas y añade `columnas`, `arcos` y `almacen`.
Comparte una sola inclusión de Three con el globo. Las escenas arrancan sin giro; los controles
manuales funcionan con movimiento reducido y `resume()` no puede saltarse esa preferencia.
Cada color procede de tokens ya definidos en las seis paletas. Ninguna vista nueva usa audio,
red, shaders externos ni mapas de terceros en tiempo de lectura.
