## Presentaciones Liftit, Blueprint y Hacker

La receta `apariencia` ofrece 15 familias con muestras y modos Claro / Oscuro / Sistema. Los
componentes de todas las familias usan sus tokens; no hace falta copiar una variante de cada tabla.
Para empezar un documento con una presentación concreta usa el generador estándar:

```bash
python3 scripts/create_artifact.py --contenido operacion.html --titulo 'Lectura de operación' --tema liftit --modo system --estilo sobrio --salida examples/generated/report.html
python3 scripts/create_artifact.py --contenido especificacion.html --titulo 'Plano del sistema' --tema blueprint --modo dark --estilo tecnico --salida plano.html
python3 scripts/create_artifact.py --contenido runbook.html --titulo 'Diagnóstico y recuperación' --tema hacker --modo dark --estilo tecnico --salida diagnostico.html
```

En capítulos, la configuración completa es:

```json
{
  "titulo": "Plano del sistema",
  "tema": "blueprint",
  "estilo": "tecnico",
  "paginas": [
    {"id": "contrato", "titulo": "Contrato", "contenido": "contrato.html"},
    {"id": "evidencia", "titulo": "Evidencia", "contenido": "examples/generated/evidence.html"}
  ]
}
```

**Cuándo:** Liftit para operación/logística; Blueprint para arquitectura, planos conceptuales y
especificaciones; Hacker para código, terminal, runbooks e incidentes. El color no impone una
estructura ni reemplaza las palabras de estado. Se pueden elegir desde Apariencia en cualquier pieza.

**Cuándo no:** no uses el verde de Hacker como única prueba de éxito, la cuadrícula de Blueprint
como escala de una gráfica ni el nombre Liftit para atribuir datos ficticios a la empresa.

**Límites:** Liftit es una adaptación editorial de #0051F4 y #2A2D46 medidos en su web, sin sustituir
las fuentes incrustadas por fuentes propietarias. Blueprint dibuja una cuadrícula estática de 24/120 px
que se omite en impresión. Hacker no simula una terminal ejecutable ni incluye parpadeos. La
presentación inicial guarda cambios posteriores por ruta del archivo; al renombrarlo se inicia con
sus valores declarados. Sin parámetros se conserva la preferencia global original.

Los ejemplos completos están en [examples/generated/liftit.html](../examples/generated/liftit.html), [examples/generated/blueprint.html](../examples/generated/blueprint.html) y
[examples/generated/hacker.html](../examples/generated/hacker.html). La guía con todas las recetas y combinaciones está en [examples/generated/guide.html](../examples/generated/guide.html).
