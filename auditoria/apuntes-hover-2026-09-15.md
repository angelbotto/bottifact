# Apuntes: repetición flotante y gesto visible

Petición de Angel: revelar la repetición con hover, sin una fila bajo el texto, y animar al
encontrar el contenido durante el scroll. Versión 2026.09.15-gesto.1, contrato 4, 74 recetas.

El control se coloca sobre el extremo superior del corchete: derecha en el apunte izquierdo,
izquierda en el derecho. Opacidad cero sólo con ratón fino y hover disponible; hover o foco
lo revelan. En táctil se conserva visible. Se elimina el margen inferior reservado al botón.
Usa tokens existentes en todas las paletas. No añade transiciones, temporizadores ni RAF.

El motor mano.js ya iniciaba la escritura y subrayado al ver un 30 % de la caja, una sola vez.
Se conserva ese comportamiento y la cancelación al salir o reducir movimiento. Se añade la
variante optativa `<del data-subrayar="tachado">` al mismo motor, con trazo a media altura y
semántica/fallback nativos. La clase estática .tachado conserva su comportamiento.

Documentación y receta completa actualizadas. Se corrige en guia-uso.md la instrucción antigua
que exigía activar Sonidos en Apariencia: la base habilita la preferencia y espera un primer
clic real, respetando el silencio guardado. También se refuerza la regla de impresión del
botón lateral: la regla común de iconos posterior anulaba el display:none anterior.

Pruebas ejecutadas:

- ensamblar.py y validar.py: 13 documentos, fuentes, contratos, inventario y sintaxis.
- validar_artefacto.py sobre el plan generado.
- comprobar_apuntes_hover.py: scroll mediante Orca y entrega real de IntersectionObserver;
  nota derecha y tachado no se habían reproducido fuera de vista, luego animaron al entrar.
  Salir y reducir movimiento dejaron cero animaciones activas. Foco por DOM reveló el control.
- Geometría a 320×740, 390×844 y 1440×960, claro/cálido/Sea: quitar el botón no modifica la
  altura de la nota; no queda margen inferior; botones dentro del ancho del viewport; sin
  desborde horizontal del documento. Evidencia: apuntes-hover.json.
- Orca hover sobre referencias del navegador: opacidad 0 antes y 1 después; altura 88 px
  en ambos casos. El host devolvió un viewport de 1639 px al usar hover. Evidencia en
  apuntes-hover-puntero.json. La captura se inspeccionó; la pseudoclase :hover consultada
  por eval no fue estable entre llamadas, por lo que no se usa como prueba independiente.

No se acredita teclado físico, tacto real, impresión física ni audición humana. El audio y
las fuentes originales permanecen iguales. Las ocho ideas adicionales del plan son propuestas,
no componentes implementados en esta entrega.
