# Gesto editorial y piezas recuperadas — TIKIN-629

Se recuperaron recetas ausentes del catálogo por capítulos: apuntes manuscritos a ambos lados,
cards delineadas y attention map de áreas. La receta manuscrita existente ahora ofrece una
frase dibujada con paths. Las clases anteriores siguen disponibles; no se sustituyó su CSS.

Propuesta previa: comentario 874ee7b4-6c30-4a53-992b-200e94aeaa76.
Referencia: capturas de Angel y cmrg.me medido con Orca a 1639×939. El SVG del attention map
mide 1008×380; las cards tienen transición calculada 0.15 s, fondo transparente y borde propio
0 px. El delineado visible pertenece a su composición. Las medidas anteriores y el hover de
107.1458 ms están en referencia-cmrg.md; aquí se usa síntesis propia de 60 ms.

## Qué se comprobó

- Ensamblar y validar: 57 recetas, dependencias incrustadas, IDs, rejilla, regiones y seis paletas.
- `scripts/comprobar_gesto.py`: nueve contratos de entrada, avance, repetición y cancelación de
  escritura, texto equivalente, fallback de caracteres/palabras, subrayados, ciclo destroy/init,
  proporción de áreas, cobertura sin superposición, datos inválidos y audio inicialmente apagado.
- 120 combinaciones: cuatro piezas × seis temas × 320×740, 390×844, 1000×900, 1200×900 y
  1440×960. Sin desborde del documento, apuntes en su rejilla y SVG de palabras sin compresión.
  Treemap y tabla conservan scroll local en móvil, con foco y nombre.
- Movimiento reducido emulado por Orca y evento MQL explícito: cero animaciones activas;
  repetición desactivada con etiqueta que explica la preferencia. No cambio físico del sistema.
- `scripts/comprobar_gesto_audio.py`: clics, movimientos y rueda nativos de Orca. Dos entradas
  de hover produjeron dos señales; mover dentro de la misma card no añadió señales. Foco,
  rueda y entrada automática de escritura fueron silenciosos. Repetir produjo un lápiz; el
  interruptor apagó el contexto y las voces. No acredita audición manual. El CLI necesita
  coordenadas enteras para `mouse move`; las decimales devolvieron error y se corrigieron.

- `scripts/comprobar_biblioteca.py`: 162 combinaciones (nueve capítulos × seis paletas ×
  320, 390 y 1440 px), interacciones, regresiones de informe y catálogo e impresión PDF.

- Acceso «Ver escritura animada» desde Apariencia: nota visible a 1440×960, 80 paths
  y 80 animaciones activas a los 600 ms; resultado en gesto-acceso.json.

## Otro bug confirmado

Al repetir un enlace profundo ya alineado, multipagina iniciaba scroll suave hacia cero antes
de revelar el destino. Si scrollIntoView no movía nada, el desplazamiento pendiente acababa en
la cabecera. Los destinos profundos ahora cancelan ese desplazamiento con posicionamiento
instantáneo; el cambio normal de capítulo mantiene su transición. Regresión incluida.

## Límites

Alfabeto SVG original, no reproducción exacta de Reenie Beanie. Minúsculas latinas, acentos, ñ,
dígitos y puntuación sencilla; máximo 240 caracteres y palabras de hasta 160 px al tamaño
actual. Fuera de ese contrato queda texto estático, sin comprimir. No selección por letra del
SVG; alternativa completa para acceso y comentarios. El treemap no mide productividad ni
captura actividad: sus 212 horas son ficticias. No se probó lector de pantalla ni móvil físico.
