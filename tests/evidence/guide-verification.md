# Verificación de la guía · 15 septiembre 2026

Ejecutado en el Mac mini, navegador de Orca y servidor local con la CSP de scripts/serve.py.

- `python3 scripts/build.py`: genera biblioteca, guías, estándares y ejemplos de temas.
- `python3 scripts/validate.py`: CSP, hashes de fuentes, módulos, referencias, anchos, regiones,
  nueve paletas, contrato 3 y cobertura exacta de las 71 recetas en la guía.
- `python3 scripts/test_contract.py`: seis grupos, incluida composición independiente de
  todas las recetas y rechazo de omisiones/IDs/anchos inválidos.
- `python3 scripts/test_portability.py`: dos grupos. ZIP verificado, instalación temporal,
  actualización con respaldo, generación desde otro cwd y rechazo de integridad/presentación inválida.
- Validador `skill-creator/scripts/quick_validate.py`: skill válido.
- `python3 scripts/check_guide.py`: **351 combinaciones**, 13 páginas × nueve paletas ×
  320×740, 390×844 y 1440×960. Sin desborde de documento, errores declarados de componentes,
  rótulos SVG fuera de límites ni fallos en los contrastes de tokens medidos. Regiones con
  foco/nombre y acceso al final. `guia-navegador.json` conserva cada combinación.
- Nueve vistas de los tres presets a esos tamaños; presentación inicial correcta y persistencia
  por archivo al cambiar y recargar. `guia-presets.json` y capturas `guia-tema-*.png`.
- `python3 scripts/check_guide_interactions.py`: ocho interacciones de tabla, visor, revisión,
  reinicialización y estado de audio; las 71 fuentes coloreadas conservan exactamente su HTML.
  Entrada de manuscrita antes no reproducida; Probar sonido y Repetir apunte con clic nativo.
- Lápiz: RMS máximo 0.00175778, pico 0.00733154, contexto running, gesto confiable. Son muestras
  de señal después del volumen maestro, **no audición humana**. Reducción por evento MQL explícito:
  cero animaciones, cero voces y todos los caracteres visibles. `guia-audio.json`.
- Los comentarios se guardan/editan/exportan con contexto y se borran en la prueba de DOM.
  La ruta de teclado se comprueba con eventos sintéticos, no con teclado físico/lector de pantalla.

La primera prueba de audio abrió el menú por JavaScript sin mover el foco. Al recuperar la ventana,
Orca restauraba el foco fuera y el menú se cerraba antes del clic. Se corrigió el montaje de la prueba
para enfocar la llave antes de abrir; el clic nativo posterior llegó al botón y reprodujo el MP3.
No se modificó el motor de audio para sortear la activación real.

Después de la matriz completa sólo se añadieron un enlace a la documentación oficial de Hermes,
un párrafo sobre piezas base y la aclaración del esqueleto histórico en docs/components.md. Se volvió
a ensamblar/validar. Las dos páginas documentales afectadas se revisaron a 320/390 en nueve paletas
(`guia-textos-finales.json`); no cambiaron CSS ni módulos respecto de la matriz de 351 vistas.

Claude, Codex y Hermes del Mac mini leen la misma instalación. Hermes descubrió una sola entrada y
leyó el skill con éxito. La instalación portable se probó en temporal, **no en el MacBook**.
La guía contiene el comando para instalar allí. No se afirma prueba de hardware o salida de audio remota.

Tailscale Serve ya existente apunta :8767 a localhost:8766. Ese proceso sirve este worktree;
la otra copia canónica se mantiene sincronizada para los agentes. Se verifica la entrega HTTPS
comparando bytes, no sólo que el servidor responda 200. No se crearon enlaces públicos.
