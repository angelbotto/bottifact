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
