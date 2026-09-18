## Componer un artefacto estándar

Las recetas anteriores son piezas de contenido. Para un nuevo artefacto completo de Angel,
usa [el contrato de composición](artifact-contract.md): incluye HTML mínimo completo para copiar,
comandos de una página y capítulos, criterio y límites del generador. La apariencia circular,
el sonido optativo y los comentarios flotantes se incorporan una sola vez automáticamente.
El índice se deriva de los h2 y la regla acompaña cada página. No insertes otra receta de
apariencia o revisión dentro del contenido de esa base.

Apariencia organiza Temas / Letras / Sonido y conserva el interruptor en Sonido. Sonido ofrece Probar sonido, volumen
inicial 65 % y estado. Probar sonido activa y reproduce el clic original de cmrg.me; el interruptor por sí solo
no emite audio. Un error al iniciar Web Audio mantiene el contexto inactivo y explica el reintento; la preferencia habilitada no equivale a salida audible.
La señal de lápiz dura lo que el trazo y se cancela con él. Estos controles están en el HTML
completo de la receta `apariencia`, en sus tres variantes; la llave circular es la predeterminada.

**Cuándo:** artículos, informes y prototipos entregados como artefactos HTML de Angel. Selecciona
las piezas de contenido por utilidad; los controles comunes deben estar presentes en cada entrega.
**Límite:** el validador estructural no prueba audición, lector de pantalla ni layout. Tampoco
actualiza HTML publicado. Sonido habilitado inicialmente, silencio persistido, pausa al ocultar y comentarios en memoria solamente.
