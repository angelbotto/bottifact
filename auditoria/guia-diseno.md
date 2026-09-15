# Guía, temas y portabilidad · 15 septiembre 2026

## Alcance

13 páginas de guía, las 71 recetas del registro con fuente completa, criterios y límites, ocho
recorridos por caso de uso y una composición de notas a izquierda y derecha. Apariencia y revisión
se muestran como componentes de la base y su receta copiable; no se duplica su montaje.

Tres temas aditivos: Liftit, Blueprint y Hacker. Tres artefactos completos independientes para
verlos aplicados. El contrato 3 conserva controles y añade presentación inicial opcional; las
preferencias posteriores se guardan por ruta cuando el documento declara una presentación.

## Procedencia y decisiones

Liftit: getComputedStyle en https://liftit.co/es/index.html, viewport 1440×960. Botón «Agenda un DEMO»
con fondo rgb(0,81,244), #0051F4; botones oscuros rgb(42,45,70), #2A2D46. Evidencia completa y
selectores en liftit-tema-fuente.json. El sitio usa Inter y Eina03_Bold; se conservaron Geist,
Instrument Serif y Reenie Beanie incrustadas. No se presenta como manual oficial ni se copian
fuentes propietarias. Los demás colores de Liftit son adaptación de lectura y visualización.

Blueprint y Hacker son propuestas propias solicitadas por Angel. Cuadrícula Blueprint: 24 px con
línea mayor cada 120 px, colores #ffffff0c y #ffffff18 sobre #082c62. También en la navegación;
no ocupa una capa por encima de texto, datos o controles. Sólo pantalla, sin RAF. Hacker: fondo
#080f0c, acento #82ed9b, títulos mono en su ejemplo y sintaxis diferenciada. No hay parpadeo/escaneo.

Audio y manuscrita conservan exactamente los archivos aprobados: MP3 originales de cmrg.me,
Reenie Beanie y revelado al entrar en pantalla. No se añadió síntesis, bucle ni normalización.

## Problemas encontrados y corregidos

- La documentación estandar.md describía todavía un tono sintetizado de 450 ms y negaba que el
  lápiz fuera una grabación de referencia. Se actualizó a los MP3 actuales; no cambia el motor.
- La nueva guía no tenía la clase `.biblioteca`: los nombres técnicos largos de `.receta-guia`
  heredaban un salto normal y producían 419 px de documento en 320 px. La regla de salto ya
  existente se amplió a `.nota-estandar .receta-guia`. Se conservan los datos completos.
- El último intervalo de calor de Blueprint daba 4.35:1; se oscureció de #427aa5 a #3b759f para
  superar 4.5:1 con #f4f9ff. Es corrección de la paleta nueva, no de un tema publicado anterior.

- componentes.md abría con un selector histórico e instrucciones que podían llevar a omitir
  controles actuales. Se identificó explícitamente como compatibilidad y se dirigió la creación
  nueva al contrato estándar. Se conserva el HTML anterior para mantenimiento.

## Portabilidad

Paquete explícito de fuentes, instrucciones, recetas, ejemplos y scripts; sin git, capturas ni
configuración de agentes. Manifiesto SHA-256 por archivo. El instalador comprueba integridad,
rechaza sustitución no indicada y conserva la copia anterior fuera del directorio de skills.
No modifica controles de confianza ni instala dependencias.

La prueba temporal instaló, actualizó conservando un archivo anterior y generó/validó desde un
cwd distinto. Un archivo alterado falla antes de copiar. Hermes del Mac mini descubre una sola
nota-tikin y skill_view(preprocess=False) lee guia-uso.md, casos-uso.json y Blueprint. Los enlaces
Claude/Codex/Hermes resuelven la misma copia canónica. Hermes avisa por el enlace externo a su
raíz confiable, pero devuelve success:true; no se cambió su política. El paquete para el MacBook
instala una copia dentro del directorio de skills. No se ejecutó instalación en el MacBook.

Referencia de descubrimiento: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
contrastada con tools/skills_tool.py de la instalación local (HERMES_HOME/skills).

## Método de navegador

scripts/comprobar_guia.py usa el CLI público de Orca contra localhost:8768 con la CSP de
scripts/servir.py. Presenta un frame por página y mide cada paleta tras su evento de cambio y
observers. Inspecciona ancho de documento, regiones locales con foco/nombre y acceso al final,
rótulos SVG y contrastes de tokens. Las paletas agrupadas evitan repetir transportes de captura;
no equivalen a una revisión manual de cada píxel. Los presets se capturan individualmente.

Los resultados finales se documentan en guia-verificacion.md. Las capturas, la señal Web Audio
y las pruebas de DOM no acreditan lector de pantalla ni audición en el MacBook.
