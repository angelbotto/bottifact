# Stack y evolución de Nota Tikin

## Decisión

Mantener HTML semántico, CSS con tokens, JavaScript modular sin framework y generación/validación con Python para los artefactos portables. Esta salida funciona descargada, carga sólo módulos usados y conserva tablas/texto cuando falta JavaScript. Cambiar toda la biblioteca a React impondría un runtime y un empaquetado sin resolver por sí solo identidad, permisos o colaboración.

Para una aplicación colaborativa conectada: TypeScript + React/Vite en el cliente, TanStack Table para tablas de producto, y PostgreSQL con autenticación y políticas por documento. Supabase es una opción coherente para Auth/Postgres/Realtime. Este proyecto todavía no provisiona ese servicio ni introduce claves. Las fuentes del artefacto siguen independientes de la aplicación: una exportación es una instantánea verificable, no una sesión conectada.

## Evaluación

| Área | Actual | Decisión |
|---|---|---|
| Documentos editoriales | HTML, CSS, SVG y JS local | Conservar semántica y exportación autocontenida. |
| Generación por agentes | Python estándar, registro y validadores | Conservar; entrada corta del skill y referencias por necesidad. |
| Tablas de informe | Motor DOM local, hasta 2000 filas | Mejorado con tipos, filtros, selección, páginas y CSV. Medir antes de ampliar límites. |
| Tablas de aplicación | No hay backend ni consulta remota | Usar TanStack Table en la capa conectada; paginación en servidor si el volumen lo requiere. |
| Revisión | Eventos locales e intercambio JSON | Útil para revisión asíncrona; no sustituye permisos ni sincronización remota. |
| Colaboración simultánea | No implementada | Postgres para contenido durable; Realtime para cambios y presencia. |
| Edición simultánea de texto | Fuera del alcance actual | Evaluar CRDT sólo si varias personas editan el mismo texto; no hace falta para hilos de comentarios. |
| Distribución | Skill y ZIP verificado | Repositorio, CI de contratos, paquete reproducible e instalación independiente del agente. |

## Buenas prácticas y próximos límites

Los datos y los ejemplos deben distinguirse; los totales conservan unidad y alcance. Los módulos nuevos requieren init/get/destroy, texto seguro, limpieza de listeners, foco y alternativa accesible. El registro es fuente para agentes y no un registro shadcn compatible por nombre.

Las pruebas deben separar contrato, datos e interacción de inspección visual. CI valida fuentes, ejemplos, ciclos de vida y paquetes; una captura no demuestra lector de pantalla ni audio audible. La revisión conectada necesita pruebas de autorización entre usuarios/documentos, conflicto de versiones, reconexión y recuperación antes de presentarse como multiusuario.

Los temas Linear Light y Linear Dark son adaptaciones propias inspiradas en superficies neutras, bordes discretos y acento lavanda. No son un tema oficial de Linear ni una réplica de su producto. El color y la combinación tipográfica permanecen independientes; Sobrio da una composición de producto más próxima a la referencia.

Fuentes primarias consultadas: [Agent Skills](https://agentskills.io/specification), [TanStack Table](https://tanstack.com/table/v8/docs/overview), [Supabase Realtime](https://supabase.com/docs/guides/realtime), [Linear Brand](https://linear.app/brand) y [preferencias de Linear](https://linear.app/docs/account-preferences). TanStack es un motor headless; Supabase ofrece eventos, presencia y cambios de Postgres. La elección anterior es una recomendación para este proyecto, no un requisito de esas herramientas.
