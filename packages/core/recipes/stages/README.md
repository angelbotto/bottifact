## Three.js: etapas con duración

Misma instalación de `packages/core/components/scene.js` y la misma inclusión única de Three.js.

<!-- nota:ejemplo etapas -->
```html
{{EXAMPLE}}
```

**Cuándo:** explicar etapas de un proceso junto con su duración. Seleccionar una etapa
conecta su caja con la explicación escrita. Empieza inmóvil; el giro continuo es optativo.
Usa las barras SVG para comparar muchas categorías o cuando girar no aporte información.

**Límite:** 1–12 etapas en orden, duraciones no negativas. La altura cero no se infla para
hacer visible una caja. No representa dependencias, paralelismo, un waterfall acumulado
ni una simulación física. No sumes duraciones como tiempo total si las etapas se solapan.
Los números 1…N identifican las filas de la tabla. Rotar puede superponer etiquetas; los
valores exactos permanecen en la tabla y «Vista inicial» devuelve la composición inicial.

### Ciclo de vida de NotaEscena

| Operación | Contrato |
|---|---|
| `NotaEscena.init(raíz)` | Inicializa `data-escena` una vez por figura; el segundo llamado devuelve la instancia existente. |
| `new NotaEscena(figura)` | Alternativa manual; rechaza una segunda instancia para el mismo contenedor. |
| `NotaEscena.get(figura)` | Recupera la instancia automática. |
| `select(índice)` / `select(null)` | Selecciona una fila, índice desde cero, o muestra todas. Rechaza índices inexistentes. |
| `rotate(dx,dy)` | Giro manual inmediato, en radianes. |
| `pause()` / `resume()` | Desactiva/solicita giro. `resume()` respeta movimiento reducido, visibilidad y estado WebGL. |
| `destroy()` | Cancela RAF, aborta listeners, desconecta observers, libera geometrías/materiales/texturas/renderer y devuelve la tabla original. Es idempotente. |

El giro es 0,15 rad/s, limitado por tiempo, no por cuadros. Sólo hay RAF mientras la vista
es visible, la pestaña está activa, se pidió girar y no hay movimiento reducido. Cambiar
esa preferencia cancela el RAF pendiente; el giro manual sigue siendo instantáneo.
Colores leídos de los tokens claros/oscuros/Sea; los rótulos son canvas locales. Al retirar
la figura de una aplicación llama `destroy()`. Para reemplazar datos: destruye, modifica
la tabla e inicializa otra vez. No hay `fetch`, modelos, mapas ni imágenes externas.
