# Bottifact: stack y decisiones

Bottifact reúne una biblioteca de componentes, un generador y un skill portable. El nombre combina Bottico y artifact. El repositorio y el skill se llaman `bottifact`; una marca de un cliente, como Liftit, es una elección del documento, no el nombre de la biblioteca.

## Qué está implementado

| Capa | Implementación comprobable | Qué resuelve |
| --- | --- | --- |
| Artefacto | HTML semántico, CSS con tokens, SVG y JavaScript sin framework | Lectura, datos, interacción y exportación del archivo |
| Biblioteca | 82 recetas en componentes.md y registro.json; 26 módulos JS de raíz | Composición por intención y dependencias seleccionadas |
| Temas | temas.json y scripts/temas.py; 15 familias, 30 paletas, tres modos | Identidad visual separada de Claro / Oscuro / Sistema y tipografía |
| Generación | Python 3.10+, sólo biblioteca estándar | Incrusta fuentes y módulos usados; valida el contrato |
| Gráficas y tablas | SVG/DOM local, tablas como fuente de datos | Ordenación, filtros, grupos, selección, CSV y alternativas textuales |
| Mapas 3D | Three.js 0.160.1 desde CDN fijado, con alternativa textual | Globo y escenas; esta parte necesita red para cargar Three |
| Comentarios standalone | Eventos en localStorage e intercambio JSON | Hilos e historial local |
| Portal NAS | FastAPI + Uvicorn, SQLite WAL y HTML por hash | Cuentas, permisos, versiones, comentarios e inbox |
| Sonido y escritura | Web Audio, MP3 y fuentes aprobados, recursos incrustados | Interacción tras un gesto real y preferencia de silencio |
| Skill | SKILL.md breve, referencias a demanda y scripts deterministas | Mismo procedimiento para Claude, Codex y Hermes |
| Distribución | Git privado, Actions, ZIP público, instalador y manifiesto SHA-256 | Generación reproducible y copia verificable del sistema |

Los HTML no exigen Python para leerse. Node sólo participa en pruebas. El HTML no depende de React ni Vite. El portal opcional sí incorpora servidor, base de datos, autenticación y revisión entre dispositivos. Orca es una herramienta local de desarrollo y comprobación, no una dependencia de los lectores ni del skill instalado.

## Evaluación del stack

Conservar esta base es mi recomendación para artículos, informes, documentación y prototipos que se comparten como archivos. El valor es poder entregar el documento y sus interacciones con pocas dependencias. Una migración completa a React añadiría un proceso de compilación; por sí sola no resolvería permisos, identidad o colaboración.

La mayor deuda está en mantener y probar la biblioteca: CSS extenso, módulos con estilos de ciclo de vida distintos y pruebas antiguas ligadas a catálogos anteriores. La recomendación es separar responsabilidades por etapas, conservar las exportaciones y medir el peso de documentos representativos antes de optimizar. Las seis combinaciones de fuentes se incrustan para poder cambiarlas: eso tiene un coste de tamaño deliberado.

## Skill: investigación y decisiones

El formato Agent Skills admite una entrada con nombre y descripción y recursos que se consultan según la tarea. Bottifact mantiene las instrucciones comunes en SKILL.md y usa `catalogo.py --id` para recuperar una receta sin cargar todos sus HTML. La carpeta instalada y `name` deben llamarse `bottifact`. [Especificación Agent Skills](https://agentskills.io/specification).

Claude Code, Codex y Hermes tienen sus propios mecanismos de descubrimiento. Usamos el formato común, rutas relativas y Python estándar; no introducimos una dependencia obligatoria de herramientas de un agente. La instalación y los contextos de carga se documentan por separado. [Claude Code](https://code.claude.com/docs/en/skills), [Codex](https://developers.openai.com/codex/skills/), [Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/).

Una validación estructural no prueba que un agente elija bien las piezas. [evaluacion-skill.md](evaluacion-skill.md) define tareas y criterios de aceptación para comprobar el comportamiento en cada agente, sin atribuir resultados a un dispositivo o modelo no ejecutado. Esta separación sigue la recomendación de probar skills con tareas representativas. [Buenas prácticas de Agent Skills](https://agentskills.io/skill-creation/best-practices).

## Evolución recomendada

| Prioridad | Trabajo | Criterio de salida |
| --- | --- | --- |
| 1 | Evaluación de generación en Claude, Codex y Hermes | Mismo encargo, datos correctos, componentes pertinentes y controles conservados |
| 2 | Pruebas de navegador en CI independientes de Orca | Teclado, tamaños, modos y comentarios comprobados sobre un archivo generado |
| 3 | Contrato de ciclo de vida y tipos de datos | init/get/destroy o montaje único documentado por módulo; pruebas de desmontaje y datos inválidos |
| 4 | Medición de tamaño y tiempo de apertura | Presupuestos basados en artículo, informe y globo reales; distinguir archivo standalone de sitio con caché |
| 5 | Revisión conectada | Identidad, permisos por documento, historial durable, reconexión y conflictos probados |

No están implementados los cinco trabajos completos. La revisión actual sí dispone de pruebas locales de contrato, store, temas y geometría; la CI ejecuta comprobaciones de Python/Node y el empaquetado.

## Portal conectado en el NAS

La revisión conectada está implementada en `portal/` y se despliega por separado. Usa FastAPI + Uvicorn, SQLite WAL en disco local y versiones HTML inmutables. El frontend conserva JavaScript y la biblioteca existente. No incorpora Supabase. Un proceso con transacciones basta para esta primera revisión asíncrona; moveríamos a PostgreSQL si las mediciones exigen varios nodos o más concurrencia de escritura.

El acceso propio verifica correo con códigos de correo (Resend; adaptador useSend opcional) o Google OIDC configurado; Cloudflare Access queda como ruta de compatibilidad. Bottifact comprueba propietario y permisos por documento en cada lectura/escritura. Los HTML se aíslan de la sesión mediante CSP e iframe sin `allow-same-origin`; un puente de mensajes limitado transporta la revisión. El agente usa una conexión personal revocable y publica privado por defecto. [portal-nas.md](portal-nas.md) explica operación, privacidad y límites.

La vista consulta cambios cada 12 segundos. No hay presencia en vivo ni coedición del texto. El dominio público artifacts.botto.is está activo. La portada reúne documentos propios, compartidos y enlaces del portal anterior sin alterar sus permisos. Sigue pendiente acreditar recepción real de códigos con usuarios invitados, migración de comentarios locales y comparación visual entre versiones. CRDT sólo merece evaluación si varias personas editan simultáneamente el cuerpo.

## Cambio de nombre y compatibilidad

El repositorio, los paquetes, las instrucciones y las cabeceras públicas usan Bottifact. `compatibilidad.json` conserva las identidades de los ejemplos publicados antes del cambio. Los espacios de almacenamiento `nota-*`, las APIs `Nota*` y el metadato histórico de versión permanecen para evitar una migración innecesaria de datos. Su presencia en código no representa la marca del producto.

El checkout que da soporte a los worktrees de desarrollo puede conservar una ruta histórica. Las instalaciones nuevas y los accesos de los agentes usan `bottifact`. No muevas un repositorio principal dentro de una carpeta de skills sin revisar sus worktrees y registros del entorno.
