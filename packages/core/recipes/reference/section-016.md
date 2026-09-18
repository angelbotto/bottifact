## Route globe

The complete executable example is `examples/generated/globe.html`. Land-mask data is embedded in globe.js; there are no map keys or fetch requests. Load the pinned Three dependency once.

| Input / method | Contract |
|---|---|
| `points` | Unique string id; latitude −90…90, longitude −180…180; optional label. |
| `arcs` | Existing from/to IDs; optional unique id, label and detail. |
| `select(id)` | Selects and centers a route; null selects all; unknown ID throws. |
| `setData({points,arcs})` | Validates before replacing geometry; invalid data throws TypeError and retains prior data. |
| `rotate(dx,dy)` | Radians; tilt is limited to ±1.2. |
| `pause()` / `resume()` | Rotation control; resume respects reduced motion. |
| `destroy()` | Stops RAF, disconnects listeners/observers, frees WebGL and empties the container. |

Coincident points avoid degenerate curves; antipodes use a deterministic axis. Labels enter through textContent. Escape `<` as `\u003c` in embedded JSON. Curves have 64 segments and hide behind the sphere. Time-based rotation is 0.072rad/s; reduced motion makes selection immediate. Buttons and keyboard remain available; touch rotation preserves vertical page scrolling. Without WebGL, retain the complete route list and an explanation. The 256×128 land mask is not a political map or measured distance source. Label invented routes as illustrative.

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
