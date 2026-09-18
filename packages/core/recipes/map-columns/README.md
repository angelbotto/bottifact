## Columnas geográficas 3D

<!-- nota:ejemplo columnas-mapa -->
```html
{{EXAMPLE}}
```

**Cuándo:** explorar la relación entre ubicación y volumen desde distintos ángulos. Si sólo interesa un ranking, usa barras; la perspectiva dificulta comparar alturas cercanas.

**Límite:** Incluye Three 0.160.1 una sola vez, packages/core/components/geography.js y packages/core/components/scene.js. Hasta 12 ubicaciones en Colombia, cantidades no negativas; eje de altura común desde cero. Huella de columna constante, proyección equirectangular. No incluye elevación del terreno. Giro apagado inicialmente; cancela RAF fuera de pantalla y con movimiento reducido; destroy libera recursos. Tabla permanente.
