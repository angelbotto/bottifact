## Globo de rutas

```html
<figure class="ancho">
  <div id="mi-globo"></div>
  <figcaption>Rutas ilustrativas. La lista permanece disponible sin WebGL.</figcaption>
</figure>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.1/three.min.js"></script>
<script>/* Pegar aquí packages/core/components/globe.js completo, con su licencia MIT */</script>
<script>
const rutas = new NotaGlobo(document.getElementById('mi-globo'), {
  points: [
    {id:'BOG',label:'Bogotá',lat:4.711,lon:-74.0721},
    {id:'MAD',label:'Madrid',lat:40.4168,lon:-3.7038},
    {id:'HND',label:'Tokio',lat:35.5494,lon:139.7798}
  ],
  arcs: [
    {id:'bog-mad',from:'BOG',to:'MAD',label:'BOG → MAD',detail:'Bogotá · Madrid'},
    {id:'mad-hnd',from:'MAD',to:'HND',label:'MAD → HND',detail:'Madrid · Tokio'}
  ]
});
</script>
```

`examples/generated/globe.html` es la versión completa ejecutable de ese contrato, sin comentarios por sustituir.
La máscara terrestre está incrustada dentro de `packages/core/components/globe.js`. No necesita APIs, claves, imágenes
externas ni solicitudes `fetch`.

| Entrada / método | Contrato |
|---|---|
| `points` | Array; `id` string único, `lat` número entre −90 y 90, `lon` entre −180 y 180; `label` opcional. |
| `arcs` | Array; `from` y `to` son IDs existentes; `id` opcional pero único, `label` y `detail` opcionales. Las coordenadas y unidades son geográficas. |
| `select(id)` | Selecciona y centra una ruta; `select(null)` vuelve a todas. Error si el ID no existe. |
| `setData({points,arcs})` | Reemplaza los datos validados, libera geometrías anteriores y reconstruye la lista. Datos inválidos lanzan `TypeError` y conservan el conjunto anterior. |
| `rotate(dx,dy)` | Radianes; giro horizontal e inclinación limitada a ±1,2. |
| `pause()` / `resume()` | Controlan el giro; `resume()` sigue respetando movimiento reducido. |
| `destroy()` | Detiene RAF, desconecta listeners/observers, libera WebGL y vacía el contenedor. |

Los puntos coincidentes no dibujan una curva degenerada; los antípodas usan un eje determinista.
Las etiquetas entran por `textContent`, no por HTML. Cuando serialices JSON dentro de un script,
escapa `<` como `\u003c`; nunca interpoles datos sin escapar dentro de `innerHTML`.

La proyección y la atmósfera siguen COBE; los arcos son bandas cuadráticas con 64 segmentos,
con ocultación tras la esfera. El giro es `0.072rad/s`, equivalente a los `0.0012rad/cuadro`
originales a 60 Hz, pero estable a otras frecuencias. El suavizado conserva el factor original
`0.09` a 60 Hz. En modo reducido el cambio de selección se resuelve inmediatamente; hay
botones y flechas de teclado. Con touch se puede girar horizontalmente y conservar el scroll
vertical de la página. Sin WebGL queda un mensaje y la lista completa de rutas.

El globo no es un mapa político ni una medición de distancias. La máscara de 256×128 describe
masas terrestres; no añade fronteras. No inventes kilómetros, vuelos o sedes: recibe datos reales
o identifica el ejemplo como ilustrativo. Los arcos y marcadores se han aclarado frente al
original, una decisión deliberada para informes, no una afirmación de igualdad píxel a píxel.
