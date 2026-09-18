## Invitación editorial tramada

<!-- nota:ejemplo invitacion -->
```html
{{EXAMPLE}}
```

**Cuándo:** cerrar una lectura con una invitación concreta. Incluye packages/core/components/invitation.js; al copiar se
añaden título del documento y referencia del bloque. La trama de puntos y curvas es CSS estático,
un tratamiento de semitono independiente del grano de papel de Apariencia.

**Límite:** no envía, guarda ni sincroniza mensajes. El botón dice copiar porque no hay backend.
Hasta 1000 caracteres; vacío no se copia. Si el portapapeles falla, selecciona el texto para copia
manual y lo explica. `NotaInvitacion.init/get/destroy` permite montar y retirar la mejora. Sin JS
queda un espacio para escribir, sin envío. No usar la trama para información ni para simular una gráfica.
