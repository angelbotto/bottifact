# Corrección de identidad Tikin

Versión 2026.09.16-tikin.1. La entrega anterior eligió incorrectamente la paleta lima/lavanda de un design system. Angel confirmó blanco, negro y rojo como identidad de Tikin. Esa indicación prevalece y coincide con los tokens de la landing citados en `marcas.json`.

- Claro: fondo blanco, superficies grises neutras, texto y logo negros.
- Oscuro: fondo negro, superficies #101010/#1C1C1C, texto y logo blancos.
- Rojo de marca #FC2929 conservado. Texto de acento #C51D24 en claro y #FF6262 en oscuro para contraste sobre las tres superficies.
- Las series y estados usan neutros y rojo con signos/rótulos; no se reutiliza verde como identidad.
- Logo SVG original, sin modificar trazos ni recortarlo; tinta pura según modo y caja de 124 × 26 px con proporción conservada.
- Fuente cromática corregida a `Tikinis/landing`, commit `bcde0b5286a51b073054580dc628963914096304`, `src/app/globals.css`. El skill y la guía explicitan la decisión para los tres agentes.

La matriz de temas vuelve a verificar 30 paletas en 320/390/1440 px, contraste de texto sobre las tres superficies, terminal y selector. `marcas-matriz.json` registra logo, cabecera, identidad conservada al cambiar paleta y modos claro/oscuro/sistema. No se cambió la geometría del logo ni se añadieron fuentes tipográficas.
