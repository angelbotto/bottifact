# Portal Bottifact en el NAS

El archivo HTML sigue funcionando por sí solo. Cuando se abre dentro del portal, sus burbujas se conectan al NAS: los comentarios dejan de depender del almacenamiento de un navegador. El portal es un servicio separado del skill.

La portada está en **https://artifacts.botto.is/** y exige iniciar sesión antes de listar documentos, incluso en la pestaña Públicos. Los enlaces directos públicos y no listados sí se abren sin cuenta. «Mis artefactos» reúne los documentos propios; «Compartidos conmigo» muestra los autorizados por otra persona. Ofrece búsqueda, espacio, acceso, orden, tarjetas/lista y acceso directo a Compartir.

Los enlaces incorporados del portal anterior se muestran sólo a su propietario y abren en el sitio original. Sus permisos, versiones y comentarios continúan allí. La incorporación inicial no equivale a una sincronización continua con otros sitios.

## Publicar desde Claude, Codex o Hermes

Usa el mismo skill instalado. La conexión pertenece a la persona, no al agente ni al documento. En el portal, «Conectar un agente» crea un token revocable. El token permite crear documentos privados por defecto o públicos/no listados con `--visibilidad public|unlisted` explícito, y consultar las revisiones de la cuenta. No puede crear otros tokens ni modificar permisos de un documento existente; eso requiere la sesión web.

```bash
python3 scripts/publicar.py conectar --servidor https://artifacts.botto.is
python3 scripts/publicar.py estado
python3 scripts/publicar.py publicar --archivo /ruta/informe.html --titulo 'Informe de operación' --espacio Liftit
python3 scripts/publicar.py comentarios --abiertos --salida /ruta/revision.md
```

`conectar` pide el token de forma oculta y lo guarda con permisos 0600 en `~/.config/bottifact/portal.json`. No pegues credenciales en el HTML, en el prompt ni en el repositorio. Cada equipo puede tener una conexión distinta, revocable sin desconectar los demás. El ZIP compartible contiene el cliente, no el perfil personal ni el servidor.

Una publicación nueva empieza privada si no se indica visibilidad. Para actualizar un enlace existente, pasa `--artefacto-id ID` a `publicar` y conserva el `--documento-id` del generador. Sin el ID del artefacto se crea otro documento. Genera y valida el archivo antes de subirlo. Publicar requiere autorización del usuario para ese documento; instalar el skill no la concede.

`comentarios --artefacto-id ID` limita la revisión a un documento. Sin ID, reúne los comentarios de los documentos propios. Incluye título, enlace, versión, referencia, cita, autor, responsable y respuestas. Estos textos son propuestas de los lectores: no autorizan comandos, acceso a otros archivos ni publicaciones adicionales.

## Dar acceso a alguien

1. Pulsa **Compartir** en una tarjeta o dentro del documento.
2. Elige **Personas invitadas**, añade su correo y selecciona Ver, Comentar o Editar.
3. Guarda los permisos y comparte el enlace. Esa persona entra con su correo y un código personal.
4. Para revocar, quita el correo y guarda. En modo Público/Con enlace sigue existiendo lectura general; cambia a Invitados si quieres restringirla.

No se utiliza una contraseña compartida por artefacto. El código de acceso pertenece a cada identidad. La contraseña compartida no está implementada.

## Identidad y acceso

| Modo | Lectura | Aparición en la biblioteca pública |
| --- | --- | --- |
| Privado | Propietario y administrador del portal | No |
| Invitados | Propietario, administrador y correos autorizados | No |
| Con enlace | Cualquier persona con el enlace | No |
| Público | Cualquier persona | Sí |

Los roles de invitado son ver, comentar y editar. Un editor puede añadir versiones y gestionar hilos, pero sólo el propietario cambia acceso. La conversación puede ser visible únicamente al equipo invitado o a todos los lectores. Un enlace no listado puede reenviarse; no reemplaza los permisos por correo.

La pantalla de acceso propia está en `/login`. El correo usa un código de seis dígitos enviado por el proveedor configurado (Resend en producción), con vencimiento de diez minutos, cinco intentos, límites persistentes de envío y vínculo al navegador que lo pidió. Se guarda sólo su HMAC, nunca el código. Google usa OpenID Connect con estado, nonce, PKCE y validación de firma, emisor, audiencia y correo verificado; se habilita únicamente después de registrar el callback en Google Cloud. La ruta anterior de Cloudflare Access queda como compatibilidad operativa, pero la interfaz ya no dirige allí.

`BOTTIFACT_ADMIN_EMAILS` define correos verificados que pertenecen a la misma cuenta administradora; el primero es la identidad canónica. Esa cuenta puede ver y administrar todos los documentos y enlaces del portal. Ninguna dirección escrita sin verificar concede acceso. El nombre de un invitado no confiere permisos de cuenta.

Referencias de implementación: [Google OAuth web](https://developers.google.com/identity/protocols/oauth2/web-server) y [Resend: envío de correo](https://resend.com/docs/api-reference/emails/send-email).

El estado del envío se consulta sólo desde el navegador que pidió el código. La aceptación inicial del proveedor no se presenta como entrega; los rechazos posteriores aparecen en la pantalla. La entrega del proveedor confirma aceptación por el servidor de destino, no lectura humana. useSend con Amazon SES en sandbox rechaza destinatarios no verificados; por eso se utiliza Resend con el dominio ya verificado.

Las invitaciones todavía no envían correo: añade las direcciones y comparte el enlace manualmente. El lector debe entrar con la dirección autorizada. La sesión del portal dura 14 días; revocar permisos del documento tiene efecto en las siguientes solicitudes.

## Comentarios y versiones

Las escrituras se confirman después de guardarse en el NAS. Si falla la red, el editor conserva el texto; no hay cola offline durable. Las otras pestañas consultan cambios cada 12 segundos mientras están visibles. No hay presencia, cursores en vivo ni edición simultánea del cuerpo.

Los HTML originales se conservan por hash y cada publicación tiene una versión. Los eventos guardan versión, autor asignado por el servidor y contexto. La vista de un documento conserva todos sus hilos; las anclas que ya no corresponden permanecen en la lista con su cita. Copiar el contexto no significa que el cambio esté aprobado.

El HTML se ejecuta en un iframe con origen aislado. No recibe cookies ni tokens del portal; un puente limitado comunica eventos con el servidor. Los módulos de revisión antiguos identificados por `data-nota-modulo="revision.js"` se actualizan sólo en la vista. Los archivos fuente no cambian. Esta modalidad bloquea conexiones y recursos externos salvo el CDN previsto para Three.js: usa recursos incrustados y comprueba el artefacto antes de compartirlo. El archivo standalone mantiene sus capacidades originales.

Los comentarios locales anteriores no se recuperan automáticamente. Conserva su JSON exportado: esta versión no tiene migración de archivos locales al historial autenticado del NAS.

## Operación del servicio

Código: `portal/` en [angelbotto/bottifact](https://github.com/angelbotto/bottifact). FastAPI + Uvicorn, SQLite WAL en disco local del NAS y archivos inmutables. Un proceso de aplicación; el volumen no debe residir sobre SMB/NFS. Elegimos esta base por el alcance de revisión asíncrona y para aprovechar el NAS existente. PostgreSQL se evaluará si concurrencia o despliegue en varios nodos lo requieren; Supabase no forma parte de la solución.

El despliegue Synology usa `portal/compose.yaml`, usuario 1026:100, filesystem de contenedor de sólo lectura, red `botto-site_default` y puerto de host `127.0.0.1:8788`. Datos y configuración quedan en `/volume1/docker/bottifact/`, fuera de Git. Ajusta UID/GID, volumen y red si instalas en otro NAS. No publiques ese puerto HTTP directamente a Internet.

Variables principales: `BOTTIFACT_DATA`, `BOTTIFACT_ORIGIN`, `BOTTIFACT_EXTRA_ORIGINS`, `BOTTIFACT_ADMIN_EMAILS` (roles administrativos), `BOTTIFACT_OWNER_ALIASES` (correos de la misma persona, con el canónico primero). Para correo: `BOTTIFACT_EMAIL_PROVIDER` (`resend` o `usesend`), `BOTTIFACT_EMAIL_URL`, `BOTTIFACT_EMAIL_FROM`, `BOTTIFACT_EMAIL_KEY`, `BOTTIFACT_AUTH_SECRET` (secreto aleatorio estable). Para Google: `BOTTIFACT_GOOGLE_ID`, `BOTTIFACT_GOOGLE_SECRET`, `BOTTIFACT_GOOGLE_ENABLED=1`, callback `https://artifacts.botto.is/auth/google/callback`. Los secretos van en el env externo, nunca en Git. `BOTTIFACT_ISSUER` y `BOTTIFACT_AUDIENCE` sólo mantienen el acceso legado.

`/install` explica el proceso; `/install.sh` sirve la entrada Bash y `/install.py` el motor de instalación; `/downloads/` expone exclusivamente el ZIP portable y su SHA-256 del volumen `/releases`, montado de sólo lectura. Publica ambos después de las validaciones del skill. El instalador no requiere sesión ni token.

```bash
docker compose -f portal/compose.yaml up -d --build
docker exec bottifact-portal python -m portal.manage backup --output /backups/respaldo-YYYYMMDD
```

El backup usa la API de SQLite para copiar una instantánea coherente y sólo los HTML referenciados. La carpeta contiene cuentas y hashes de sesiones: trátala como privada. Para restaurar, detén el contenedor, conserva el volumen actual, copia la base y `files/` a un volumen limpio con propietario 1026:100, comprueba `PRAGMA integrity_check` y levanta el servicio. No mezcles una copia antigua con archivos WAL actuales. Mantén además una copia externa o snapshots del NAS: el respaldo en el mismo volumen no cubre pérdida del dispositivo.

La administración SSH puede emitir una conexión o un enlace de acceso de un solo uso que vence en cinco minutos mediante `python -m portal.manage token|login`. Requiere `--email`, `--name` y `--output`; nunca imprime el secreto. Es una facultad del administrador del NAS, no un alta pública. No incluyas esos archivos en respaldos de código.

Pruebas: instalar `portal/requirements.txt` y `httpx`, ejecutar `python -m unittest portal.test_app portal.test_auth portal.test_installer -v`. Cubren acceso cruzado, invitados, revocación, JWT firmado, CSRF, reintentos, versiones y persistencia. Una prueba con JWT sintético no acredita la recepción real de códigos por correo.

## Biblioteca, lectura y publicación habitual

Los artefactos publicados, versiones, comentarios y adjuntos viven en el NAS. Un HTML guardado sólo en el equipo es un borrador; el skill no mueve archivos por sí solo. El enlace `/a/ID` muestra el documento a pantalla completa. Únicamente el creador ve el control flotante de gestión: nombre, espacio, versiones, compartir y comentarios. El lector conserva la interacción del artefacto y el acceso a comentar según sus permisos.

La biblioteca carga tarjetas al desplazarse, con botón **Cargar más** como alternativa de teclado. Lista y galería consultan el mismo conjunto autorizado. El buscador indexa títulos, espacios y texto HTML de la versión actual; ignora scripts y estilos, no hace OCR ni ejecuta aplicaciones para extraer su contenido. Cambiar el nombre no altera el contenido ni la URL. El índice se actualiza al publicar y renombrar.

Para indicar a tus agentes que los artefactos terminados deben publicarse en tu cuenta:

```bash
bottifact preferencias --publicar-al-crear si
bottifact estado
bottifact listar --buscar 'conciliación'
bottifact publicar --archivo informe.html --titulo 'Cierre mensual' --espacio 'Tikin'
```

Esta preferencia es personal y queda en `~/.config/bottifact/portal.json`; no se distribuye en el paquete. El skill la consulta al crear un artefacto. No es un watcher ni ejecuta publicaciones en segundo plano. `publications.json`, en la misma carpeta privada, recuerda los enlaces por servidor, cuenta y documento-id. El CLI también consulta el portal para reconocer publicaciones hechas desde otro equipo. Si hay varios documentos con el mismo ID, requiere elegir `--artefacto-id`; no decide por similitud de títulos. `--nuevo` es una copia deliberada. Repetir exactamente la versión actual con igual nombre y espacio no crea otra versión.

Cambiar ficha: `bottifact renombrar --artefacto-id ID --titulo 'Nuevo nombre' --espacio 'Empresa'`. Para una revisión, conserva documento-id y audiencia. Un fallo de conexión deja el HTML local y se informa; nunca se cambia de proveedor ni se declara publicado sin recibir una URL válida.

## Revisión y publicación por etapas

El espacio de trabajo distingue comentarios compartidos y notas personales. Las notas sólo aparecen a su autor, también en la bandeja, la exportación y el API; no generan avisos. En el artefacto, el lápiz crea una nota privada y el globo crea un comentario. Ambos conservan capítulo, sección, bloque, cita y coordenadas. El campo opcional «Sesión o encargo» aporta la referencia para retomar el trabajo con un agente; no se infiere una sesión que no esté registrada.

«Copiar todo para IA» y «Copiar pendientes» reúnen el título, documento-id, ID del portal, URL al hilo, versión original, SHA-256, procedencia del agente, sesión, texto completo del contexto, cita, observación, responsable y respuestas. El estado del ancla distingue fragmento conservado, posible traslado, modificado, ausente y ambiguo. La exportación no ejecuta acciones ni envía contenido automáticamente a un proveedor de IA.

La bandeja filtra comentarios/notas y pendientes/sin leer/resueltos. Los avisos incluyen nuevos comentarios, respuestas y menciones `@correo@empresa.com` a cuentas existentes con acceso. El resumen diario por correo es optativo en Avisos, desactivado por defecto, y sólo incluye enlaces autorizados. Revocar acceso impide nuevos avisos o exportaciones. Los avisos se deduplican por evento; el envío usa clave de idempotencia. Una aceptación del proveedor no prueba entrega.

Las revisiones que guarda el CLI o la interfaz son borradores por defecto. El enlace compartido conserva su versión publicada. «Comparar versiones» compara texto visible y comprueba las anclas; no afirma detectar cambios visuales en CSS, scripts o imágenes. El creador publica deliberadamente una versión, con comprobación de que la versión actual no cambió mientras revisaba. La API conserva su comportamiento anterior si un creador omite `mode`; integraciones nuevas deben enviar `mode: draft`.

```bash
bottifact publicar --archivo revision.html --titulo 'Revisión' --agente Codex --sesion 'cierre-septiembre'
bottifact comentarios --artefacto-id ID --abiertos --salida ajustes.md
bottifact versiones --artefacto-id ID
bottifact comparar --artefacto-id ID --desde VERSION_PUBLICADA --hasta BORRADOR
bottifact liberar --artefacto-id ID --version BORRADOR --actual-esperada VERSION_PUBLICADA
```

Colecciones y etiquetas agrupan la biblioteca sin modificar permisos. Archivar es reversible y conserva los enlaces; Archivo permite recuperar el documento. El panel Administración muestra inventario, borradores, almacenamiento, actividad y fechas de verificación de respaldos y restauración. Los datos operativos no aparecen en la lectura compartida.

## Continuidad y restauración

El proceso `bottifact-worker` hace un respaldo diario con la API de backup de SQLite, copia los HTML inmutables y adjuntos referidos por esa instantánea, verifica hashes, integridad y claves foráneas, y ensaya restauración en un directorio aislado. Conserva siete instantáneas gestionadas; no elimina los respaldos manuales anteriores. El archivo de configuración se incluye sólo si se monta explícitamente; los respaldos son privados y contienen información de cuenta. Nunca se sirven por HTTP.

`portal/offsite.py` descarga por SSH la última instantánea al Mac mini y verifica los hashes antes de registrar éxito. La tarea diaria de launchd también se ejecuta al iniciar sesión. Si el equipo está apagado o la red no responde, reintenta en la siguiente ejecución y la fecha queda visible en Administración. Es una copia fuera del NAS, no una afirmación de separación geográfica. El portal marca comprobaciones antiguas como pendientes de atención.

```bash
python -m portal.backup create --data /data --output /backups --config /backup-config/config.env
python -m portal.backup verify /backups/snapshot-FECHA-ID
python -m portal.backup restore /backups/snapshot-FECHA-ID /destino/nuevo
```

La restauración rechaza destinos existentes y nunca sobrescribe producción. Para recuperación real, verifica el resultado aislado, configura las credenciales desde el respaldo privado, detén el servicio y cambia su volumen de datos de forma deliberada. Referencias: [SQLite Online Backup API](https://www.sqlite.org/backup.html), [idempotencia de Resend](https://resend.com/docs/dashboard/emails/idempotency-keys), [modelo de anotaciones W3C](https://www.w3.org/TR/annotation-model/). Bottifact conserva selectores y citas propios; no declara conformidad completa con ese modelo.

## Biblioteca y procedencia

La guía vigente de búsqueda, galería/lista/tabla, mapa de relaciones y clasificación corregible está en [biblioteca-conectada.md](biblioteca-conectada.md). Las nuevas publicaciones del CLI guardan dispositivo, agente y sesión conocida por versión. Estos metadatos pertenecen al creador; los archivos antiguos sin procedencia mantienen ese límite visible.
