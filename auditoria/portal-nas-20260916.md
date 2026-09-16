# Portal NAS · verificación 2026-09-16

Implementado en `portal/`, desplegado como contenedor independiente `bottifact-portal` en Synology. La vista privada usa HTTPS de Tailscale en el puerto 8788; `artifacts.botto.is` aún requiere DNS y ruta de Tunnel. La aplicación Access de `/auth/login` está creada. No se afirma recepción de OTP ni inicio de sesión público de extremo a extremo.

- Ocho grupos de pruebas API pasan: autorización cruzada, roles, invitados, revocación, idempotencia, versiones, reinicio, exportación, CSRF, JWT RS256 sintético y payload inválido.
- Navegador Orca sobre el portal real: comentario creado desde el editor del iframe, guardado en el NAS, autor asignado por el servidor, pin visible y mensaje de persistencia correcto.
- Portal medido a 320, 390 y 1280 px: ancho del documento igual al viewport; iframe contenido y diálogo de acceso operativo.
- Revisión standalone comprobada con un documento de prueba separado: guardar cierra el editor; destruir/iniciar conserva el comentario local.
- Respaldo inicial generado y restaurado en un directorio temporal: integridad SQLite y hashes de todos los HTML correctos; una publicación privada conservada.
- El NAS usa SQLite WAL en volumen local y archivo por hash; el contenedor corre sin root y su healthcheck responde.

La navegación de prueba del iframe usa acciones DOM sintéticas; no acredita audición humana ni lector de pantalla. Se mantienen las pruebas existentes del contrato y del skill. No hay migración automática de comentarios locales ni cola offline durable. No hay invitados reales ni correos enviados como parte de estas pruebas.
