# Ampliación analítica y corrección de laterales — TIKIN-629

Propuesta registrada antes de construir: comentario c17f9da6-3b4d-41fc-a290-85e017f2033c.

Referencias primarias consultadas el 14 de septiembre de 2026:
- GitHub, calendario de contribuciones: https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile
- Apache Superset, exploración de datos y familias de gráficas: https://superset.apache.org/docs/creating-charts-dashboards/exploring-data/
- Natural Earth, dominio público: https://www.naturalearthdata.com/about/terms-of-use/
- Geometría de Colombia: https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson

Se añadió variedad de preguntas y codificaciones visuales; no se copiaron estilos o medidas de
GitHub/Superset. La referencia editorial cmrg.me sigue documentada en referencia-cmrg.md.
Los números de los ejemplos son ficticios. No son cifras de Liftit ni de Tikin.
La geometría se extrajo por ADM0_A3=COL, se redondeó a cinco decimales y se incrustó en
geografia.js. Vista continental generalizada 1:110m; no mapa vial o cartografía de barrios.

## Diez componentes

| Vista | Pregunta | Codificación / límite principal |
|---|---|---|
| Calendario | ¿Cuándo hubo actividad? | Conteo diario; cero separado de ausencia; UTC |
| Torta/donut | ¿De qué se compone un total? | Ángulo proporcional, 1–6 partes no negativas |
| Áreas | ¿Cómo cambian total y mezcla? | Tres series aditivas; fechas a distancia real |
| Caja y bigotes | ¿Cómo varía la distribución? | Cinco estadísticas; bigotes mínimo/máximo |
| Velas | ¿Cómo abrió, osciló y cerró? | OHLC; serie sintética, sin mercado conectado |
| Mapa de rutas | ¿Qué corredores concentran viajes? | Grosor lineal; curvas no viales |
| Mapa de volumen | ¿Dónde se concentra cantidad? | Área proporcional; no cobertura territorial |
| Columnas geográficas | ¿Cómo cambia volumen por sede? | Altura común desde cero sobre Colombia |
| Arcos 3D | ¿Qué conexiones se cruzan? | Sección de tubo proporcional; elevación visual constante |
| Almacén 3D | ¿Dónde queda capacidad? | Ocupación sólida/capacidad delineada; X/Z en metros |

## Bug confirmado

El offset fijo ignoraba el borde inferior de la barra antes de quedar sticky. Su z-index tapaba
el índice y la regla. Ahora ambos reservan espacio bajo la barra medida; el porcentaje tiene
un canal separado del cursor y el tramo recorrido se colorea. El patrón legado sin lectura-guiada conserva su umbral y composición; también recibe
la separación del porcentaje y el color del tramo leído. Se ensayó el inicio, no sólo un enlace profundo con la cabecera ya pegada.
