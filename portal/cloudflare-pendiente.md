# artifacts.botto.is está activo

El dominio público apunta al NAS mediante el túnel existente. Se agregó únicamente la ruta `artifacts.botto.is` → `http://bottifact:8080` y su CNAME proxied, conservando las otras 35 reglas. La credencial administrativa se resolvió desde Infisical; no está en este repositorio ni en el contenedor.

La portada está en https://artifacts.botto.is/. Cada cuenta ve sus documentos y los compartidos con ella. El catálogo del propietario incorpora 14 enlaces del portal anterior, privados dentro de esta biblioteca: abrirlos conserva las políticas de su sitio de origen. No se migraron sus versiones ni comentarios.

## Acceso por persona

En el documento, pulsa **Compartir**, elige **Personas invitadas**, añade el correo y escoge **Ver**, **Comentar** o **Editar**. Guarda y comparte el enlace. También puedes hacerlo desde la tarjeta de la biblioteca. Añadir un correo a un documento privado cambia el formulario a invitados; guardar es lo que aplica los permisos.

La persona entra con su correo y un código personal de Cloudflare Access. No hay contraseña compartida por documento. El código verifica la identidad y Bottifact comprueba que ese correo tenga permiso. Las invitaciones automáticas por email aún no están implementadas: añadir una persona no le envía un mensaje.

Quitar un correo y guardar revoca su acceso restringido. En un documento público o con enlace, quitar una invitación no impide la lectura general: para restringirla elige Invitados o Privado.

## Configuración operativa

- NAS: `bottifact-portal`, volumen `/volume1/docker/bottifact/data`.
- Origen principal: `BOTTIFACT_ORIGIN=https://artifacts.botto.is`.
- Origen adicional: `https://namakarius.tailf63ddf.ts.net:8788` para administración privada.
- Login protegido por Access: `artifacts.botto.is/auth/login`; la API de documentos valida sus propios permisos.
- Proveedor de identidad: One-time PIN. Firma, audiencia y emisor del JWT se verifican en el servidor.
- DNS: CNAME `artifacts` → `dfa2b99e-a481-43b3-b73d-e1b1306e0729.cfargotunnel.com`, proxied.
- Ruta añadida al túnel `dfa2b99e-a481-43b3-b73d-e1b1306e0729`: `http://bottifact:8080`.

Se verificaron HTTPS, portada, redirección al formulario de código, API autenticada de agentes, aislamiento del catálogo y controles de acceso. La entrega real del código por correo requiere que la persona complete el ingreso; no se enviaron correos de prueba a terceros.
