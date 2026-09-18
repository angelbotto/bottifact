# Portal público · 2026-09-16

- Cloudflare: hostname y CNAME añadidos mediante credencial de Infisical. Las 35 reglas previas del túnel permanecen intactas. HTTPS y `/health` responden; `/auth/login` redirige al formulario One-time PIN de la aplicación correcta.
- API de agentes: conexión autenticada por token comprobada sobre el dominio público. El cliente identifica su User-Agent como Bottifact; las solicitudes genéricas Python recibían el bloqueo 1010 del filtro de navegador de Cloudflare.
- Portada privada del propietario: 15 entradas, un documento Bottifact y 14 enlaces a proyectos existentes en pages.botto.is. No se publicaron metadatos de esos enlaces ni se cambiaron permisos del sitio anterior.
- Navegador: filtros, lista/tarjetas y diálogo Compartir medidos a 320, 390 y 1440 px sin desbordamiento. Añadir un correo a un documento privado cambia el formulario a Invitados; la prueba cerró sin guardar y confirmó que el documento permanecía privado.
- Diez grupos de pruebas API: aislamiento entre usuarios, roles, revocación, JWT sintético firmado, invitados, versiones, CSRF, catálogo propio/compartido/público y enlaces personales idempotentes.
- No se enviaron invitaciones ni códigos de prueba a terceros. El navegador del administrador se abrió mediante enlace temporal de SSH; esto no acredita entrega de OTP por correo.
