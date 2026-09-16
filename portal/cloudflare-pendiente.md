# Activar artifacts.botto.is

El servidor ya está en el NAS y comparte la red Docker con el conector existente. La credencial disponible permite administrar Access, pero devuelve 401 al consultar la configuración del túnel; no permite completar la ruta pública.

En Cloudflare Zero Trust, abre el túnel con ID `dfa2b99e-a481-43b3-b73d-e1b1306e0729`. Añade una aplicación publicada sin cambiar las existentes:

- Hostname: `artifacts.botto.is`
- Service: `HTTP`, dirección `bottifact:8080` (nombre del servicio en la red `botto-site_default`).
- Si el panel no crea DNS automáticamente: CNAME `artifacts` → `dfa2b99e-a481-43b3-b73d-e1b1306e0729.cfargotunnel.com`, proxied.

Ya existe la aplicación Access «Bottifact · Inicio de sesión» para `artifacts.botto.is/auth/login`. Su política Allow acepta personas autenticadas; los documentos privados se autorizan después en Bottifact. No agregues un bypass sobre esa ruta ni protejas todos los artefactos con la misma lista de correos del propietario. El servidor comprueba firma/audiencia/emisor del JWT; una cabecera inventada no sirve.

Después de conectar la ruta:

1. Comprobar `https://artifacts.botto.is/health` y que la portada carga.
2. Cambiar `BOTTIFACT_ORIGIN=https://artifacts.botto.is` en `/volume1/docker/bottifact/config.env`. Mantener el origen privado en `BOTTIFACT_EXTRA_ORIGINS` si se desea conservar la vista Tailscale.
3. Recrear sólo Bottifact: `docker compose -f /volume1/docker/bottifact/source/portal/compose.yaml up -d`.
4. Probar ingreso real con el correo del propietario. Compartir un ejemplo con una segunda identidad autorizada; comprobar privado, invitado, público, comentario y revocación.
5. Reconectar el cliente de los agentes al origen público. Mantener los tokens fuera de Git y de los HTML.

No es necesario abrir puertos públicos del NAS ni cambiar los servicios `pages.botto.is` o `pages-api.botto.is`. La ruta HTTPS privada de prueba es `https://namakarius.tailf63ddf.ts.net:8788/`; requiere pertenecer a la red Tailscale. Su login por correo no pasa por Cloudflare: para el administrador se usa un enlace temporal emitido por SSH.
