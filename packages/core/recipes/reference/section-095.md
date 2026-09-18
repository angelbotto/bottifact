## Liftit, Blueprint and Hacker examples

Theme family and light/dark/system mode are independent. Components inherit tokens rather than needing separate markup per theme. Use the generator options below for initial appearance. Liftit supports logistics, Blueprint architectural specifications, and Hacker code/runbooks. Color never replaces status words; a Blueprint grid is not a chart scale. Do not attribute fictional data to a company.

Blueprint uses a static 24/120px grid omitted in print; Hacker does not execute commands or blink. Brand sources and current token choices live in brands.md and themes.md. Declared initial presentation is overridden by later route-local preferences; changing the route starts from declared defaults. Without an initial presentation, global preferences remain. Complete examples are in examples/generated/{liftit,blueprint,hacker,guide}.html.

```bash
python3 scripts/create_artifact.py --contenido operacion.html --titulo 'Lectura de operación' --tema liftit --modo system --estilo sobrio --salida examples/generated/report.html
python3 scripts/create_artifact.py --contenido especificacion.html --titulo 'Plano del sistema' --tema blueprint --modo dark --estilo tecnico --salida plano.html
python3 scripts/create_artifact.py --contenido runbook.html --titulo 'Diagnóstico y recuperación' --tema hacker --modo dark --estilo tecnico --salida diagnostico.html
```

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
