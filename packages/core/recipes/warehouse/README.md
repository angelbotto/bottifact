## Capacidad de almacén 3D

<!-- nota:ejemplo almacen -->
```html
{{EXAMPLE}}
```

**Cuándo:** ver dónde queda espacio dentro de una distribución de almacén. No para decidir seguridad estructural, altura real de estibas o rutas de evacuación.

**Límite:** Incluye Three 0.160.1 y packages/core/components/scene.js. 1–12 ubicaciones con X/Z finitos en metros, capacidad positiva y 0 ≤ ocupados ≤ capacidad. X/Z comparten escala en metros; la huella de cada caja es constante, no mide la estantería. La altura representa cantidad de posiciones, no metros. No evita superposición si duplicas coordenadas; usa ubicaciones distintas y separadas. Comparte ciclo de vida de NotaEscena y tabla permanente; no es un gemelo digital conectado.
