# Familias y modos

La apariencia tiene tres ejes independientes: **familia**, **modo** y **tipografía**. La pestaña Temas ofrece 15 familias con muestras, búsqueda y categoría. Arriba se elige Claro, Oscuro o Sistema. Letras conserva las seis combinaciones tipográficas y Sonido sus controles. Cambiar una familia conserva el modo; cambiar el dispositivo sólo afecta al modo Sistema.

Prueba [examples/generated/themes.html](../examples/generated/themes.html). Todas las familias tienen versión clara y oscura; hay 30 paletas. Las muestras siguen el modo efectivo. Linear tiene una sola tarjeta.

| Familia | Uso sugerido |
| --- | --- |
| Editorial | Artículos y notas, papel cálido y cobre |
| Sea | Lectura azul oceánica y menta |
| Oliva | Investigación y síntesis, tonos botánicos |
| Arcilla | Narración, arena y terracota |
| Ciruela | Ensayos y portafolios, malva |
| Liftit | Operación logística, Ribbon/Bay y coral del LMS |
| Tikin | Finanzas, blanco y negro con rojo Tikin; identidad confirmada de la landing |
| Catabum | Comunidad, violeta, magenta y naranja de la app |
| Blueprint | Arquitectura, planos y cuadrícula |
| Hacker | Terminal y documentación técnica, verde |
| Linear | Producto y revisión, neutros y lavanda |
| Modern | Documentación técnica, referencia VS Code |
| GitHub | Código e informes de ingeniería |
| Catppuccin | Lectura suave, Latte / Mocha |
| Solarized | Lectura prolongada, marfil / petróleo |

## Generación y preferencias

```bash
python3 scripts/create_artifact.py --contenido contenido.html --titulo 'Informe' --tema liftit --modo system --estilo sobrio --salida examples/generated/report.html
```

En configuración JSON: `"tema": "liftit", "modo": "system"`. Con las familias nuevas el modo inicial es Sistema. Para fijar el aspecto de cualquier documento, pasa siempre ambos argumentos. Sin preferencias iniciales se usa Editorial/Sistema. La elección guardada por el lector prevalece sobre la inicial. Los documentos con tema/modo/estilo inicial usan preferencias por ruta; los demás comparten la preferencia del origen. Un navegador que bloquea almacenamiento conserva la interacción durante esa sesión.

Los IDs anteriores siguen siendo entradas válidas: `light` → Editorial/Claro; `dark` → Editorial/Oscuro; `system` → Editorial/Sistema; `linear-light` y `linear-dark` → Linear y su modo. Los nombres existentes Sea, Oliva, Arcilla, Ciruela, Liftit, Blueprint y Hacker conservan su modo original si no se pasa `--modo`. Una selección nueva en la interfaz mantiene el modo actual.

Se migra `nota-tema` a `nota-apariencia-v2` (familia y modo), manteniendo su ámbito. El ID CSS `data-theme` es la paleta resuelta para conservar los observadores de gráficas y globos. `data-theme-family`, `data-theme-mode` y `data-color-mode` describen familia, preferencia y modo efectivo. El evento `nota:tema` notifica los cuatro valores. `NotaTemas.get()` consulta y `NotaTemas.set({family:'github',mode:'system'})` cambia mediante la misma ruta validada que los controles.

## Añadir una familia

1. Añade un archivo en `packages/core/themes/families/` y regístralo en [el índice](../packages/core/themes/index.json), con nombre, categoría, descripción y semillas `light` y `dark`. Cada semilla contiene papel, dos superficies, tres tintas y acentos naranja/verde/rojo/azul; naranja es el nombre histórico del acento principal, no un color obligatorio.
2. Las referencias a IDs de paleta existentes preservan su CSS. Para familias nuevas usa las diez semillas hexadecimales por modo. [scripts/themes.py](../scripts/themes.py) deriva tokens semánticos de gráficas, calor, piezas, código y apariencia. No edites el bloque generado de CSS ni el registro incrustado en JS.
3. Actualiza los metadatos de VERSION.json y el catálogo descriptivo. Ejecuta `python3 scripts/build.py`, los validadores del skill y `node scripts/test_themes.cjs`. Comprueba ambas versiones en el navegador con `python3 scripts/check_themes.py` y servidor local activo.
4. Verifica legibilidad en las tres superficies, código, terminal, gráficas y formularios; las diferencias deben ser comprensibles sin depender únicamente del color. Comprueba Sistema al cambiar la apariencia del dispositivo, persistencia y geometría móvil.

## Referencias y alcance

Paletas adaptadas por Bottifact, no extensiones oficiales ni una integración con un editor. Se conservan el carácter y los fondos de referencia; ciertos acentos y textos secundarios se ajustan para mantener contraste al usarlos en datos y superficies. Las nuevas contrapartes de los temas anteriores son diseños propios. No se descarga ningún tema durante la lectura.

- [VS Code: temas y modos del dispositivo](https://code.visualstudio.com/docs/configure/themes); [paletas Modern originales](https://github.com/microsoft/vscode/tree/main/extensions/theme-defaults/themes).
- [GitHub para VS Code](https://github.com/primer/github-vscode-theme): familias claras y oscuras de Primer.
- [Catppuccin](https://github.com/catppuccin/catppuccin): referencia Latte para claro y Mocha para oscuro.
- [Solarized, de Ethan Schoonover](https://ethanschoonover.com/solarized/): referencia de fondos marfil y petróleo y sus acentos.

No se afirma que estos temas vengan preinstalados en Cursor: son referencias del ecosistema de editores, adaptadas a nuestros artefactos.

Las identidades de empresa, logos y la distinción entre color original y adaptación están en [docs/brands.md](brands.md). Cambiar la paleta del lector conserva la empresa que firma el documento.

El catálogo `themes.json` es generado. Sigue [la guía de contribución](contributing-components.md) para registrar familias, reconstruir las muestras y validar React.
