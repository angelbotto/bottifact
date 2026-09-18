# Acceso propio e instalación · 17 septiembre 2026

Versión 2026.09.17-portal.3.

- `/` exige sesión y redirige a `/login`; `/api/artifacts` responde 401 sin identidad verificada, incluida la vista pública. Los enlaces directos públicos/no listados conservan lectura anónima.
- Acceso por código de correo propio: useSend confirmó SENT y DELIVERED del código de prueba dirigido al propietario. Se comprobó el paso de correo a código en navegador. La recepción humana y el ingreso manual del código no se atribuyen a esta prueba.
- Tres direcciones de administrador se configuraron en el env privado como una sola identidad canónica. El catálogo autenticado devuelve las 15 entradas existentes: un artefacto nativo y 14 enlaces anteriores. Los enlaces anteriores conservan las reglas de su origen.
- Google OIDC implementado y probado con JWT firmado sintético, estado, nonce, PKCE, audiencia, vencimiento y correo verificado. Deshabilitado en producción: el cliente web existente devuelve `redirect_uri_mismatch` para el callback de Bottifact. Se requiere añadirlo en Google Cloud; sus credenciales están fuera del repositorio.
- 17 grupos de pruebas: permisos de documentos, comentarios, versiones, tokens, login legado, correo, administrador, OAuth y actualizador. Los intentos incorrectos se confirman en SQLite incluso al devolver 401.
- Navegador: pantalla de entrada inspeccionada; 320 y 390 px sin desbordamiento horizontal. Tema oscuro conserva la identidad editorial.
- Paquete portable público, SHA-256 y manifiesto. Descarga desde el dominio real e instalación completada en ambos Macs. Las tres rutas de agentes apuntan a la copia estable; las conexiones personales existentes siguen funcionando. Esto no acredita que una sesión de un agente ya abierta haya recargado el skill.
- Publicación con token: privado por defecto, `--visibilidad public|unlisted` explícito al crear. Actualizar un documento conserva sus permisos; el token no puede acuñar otros tokens ni cambiar ACL de documentos existentes.
- Copia de seguridad anterior al despliegue: `2026-09-17-before-native-auth`. El checkout de desarrollo concurrente quedó intacto.

La ruta histórica de Access queda como compatibilidad; la nueva interfaz no la utiliza. Los instaladores no fuerzan actualizaciones automáticas, no reemplazan checkouts Git ni carpetas de skills propias, y conservan respaldo. El checksum compartido por el mismo servidor es una comprobación de integridad, no una firma independiente.

## Seguimiento · versión 2026.09.17-portal.4

- Se investigó el código no recibido en Liftit: useSend aceptó la solicitud, pero SES la rechazó por destinatario no verificado en su sandbox. El envío DELIVERED al propietario de la prueba anterior no demostraba entrega a otros dominios.
- El portal ahora usa Resend con el dominio botto.is verificado. Su API confirmó DELIVERED para la prueba dirigida a owner@example.com el 17 de septiembre a las 06:42 UTC. Esto acredita recepción del servidor, no ubicación en la bandeja ni lectura humana.
- El formulario consulta el estado real del envío con un challenge vinculado a su navegador. Distingue procesamiento, envío, entrega y rechazo; no expone códigos ni identificadores del proveedor.
- Instalador Bash público en /install.sh y guía /install. Instala o actualiza la biblioteca para Codex, Claude Code y Hermes. Utiliza Python 3.10+ internamente; ChatGPT requiere importar manualmente el ZIP cuando el espacio admite skills.
- El lector ofrece Google y correo sin bloquear la lectura pública. Los documentos privados piden acceso; una cuenta autenticada sin permisos puede cambiar de cuenta sin entrar en un bucle.
- Google activado en producción: proyecto botticlaw, cliente web Botto apps, callback https://artifacts.botto.is/auth/google/callback agregado conservando los cinco existentes. Se completó un ingreso real en Dia del MacBook como me@angelbotto.com y el retorno al documento privado. La cuenta fue reconocida como verificada y el documento denegó acceso por carecer de permisos. No se añadieron scopes de Gmail/Drive ni se rotaron secretos de otras aplicaciones.
- 20 pruebas del portal y del instalador pasan, incluida la vinculación del estado de entrega al navegador y la limpieza de temporales al fallar curl. Contratos de biblioteca, revisión distribuida, 150 comprobaciones de temas y validación del skill pasan.
- Guía de instalación inspeccionada a 1639 y 390 px sin desbordamiento; copiar comando funciona. Lector privado muestra ambas opciones de acceso.

El proyecto Google conserva audiencia externa en estado Prueba. Bottifact solo solicita `openid email profile`, cubiertos por la excepción oficial que permite acceso sin lista de testers; no se modificó la configuración compartida de marca ni los permisos de otras aplicaciones. Referencia: https://developers.google.com/identity/protocols/oauth2/production-readiness/overview .
