# CP14-R1 — Auditoría académica, visual y técnica

Fecha de revisión: 2026-11-18. Punto de partida: commit `d1a0da2`.

## Resultado ejecutivo

La presentación original de CP14 contenía los temas requeridos, pero dependía en exceso de texto, usaba gráficas pequeñas y no hacía visible toda la trazabilidad experimental. La versión `CORTE2_FINAL_REVISADO` reorganiza la defensa en 14 diapositivas, conserva las cifras verificadas de CP09–CP13 y separa claramente selección provisional, limitaciones y trabajo futuro. No se reentrenó ningún modelo ni se utilizó Test.

## Auditoría por diapositiva

| Diapositiva final | Requisito auditado | Evidencia incorporada | Corrección aplicada |
|---:|---|---|---|
| 1 | Alcance del Corte 2 | Validation: 2.960 filas; Test reservado | Portada simplificada, integrantes completos y alcance visible |
| 2 | Problema y continuidad | Objetivo `Appliances` y continuidad desde Corte 1 | Se sustituyó texto extenso por una comparación visual Corte 1/Corte 2 |
| 3 | Contrato de predicción | 19.735 registros, 29 columnas, variables disponibles y excluidas | Se explicitó el instante de predicción y la exclusión del objetivo |
| 4 | Características temporales sin futuro | `hour_sin/cos`, `dow_sin/cos`, `doy_sin/cos`, `weekend` | Se muestran fórmulas cíclicas y el control de fuga |
| 5 | Pipeline reproducible | `src/corte2_pipeline.py`, semilla 2026, ajuste solo con Train | Se creó un diagrama de flujo y se aisló visualmente Test |
| 6 | Validación temporal | Train 13.814, Validation 2.960, Test 2.961; P90 220 Wh calculado en Train | Se reemplazó la explicación textual por una línea temporal |
| 7 | Benchmark de regresores | Dos baselines, tres Ridge, dos HGB y dos Extra Trees | Se agruparon familias, ajuste acotado y métricas comparables |
| 8 | Comparación MAE/RMSE/R² | CSV real `cp10_benchmark_validacion.csv` | Se creó una gráfica nativa de RMSE y tarjetas con los mejores criterios |
| 9 | Gráfica temporal real | `cp12_serie_temporal_validacion.png` | Se amplió la gráfica y se añadió una conclusión interpretativa |
| 10 | Residuos y errores | `cp12_residuos_validacion.png` y métricas por segmento | Se amplió el gráfico y se destacaron 2.737 casos normales, 223 altos y el sesgo |
| 11 | Picos mal predichos | Peor caso: 840 Wh reales, 106,61 Wh predichos, error 733,39 Wh | Se convirtió el caso extremo en evidencia central y limitación explícita |
| 12 | Ablación `rv1/rv2` | Cuatro configuraciones de `cp12_ablacion_rv.csv` | Se creó una comparación de RMSE y se justificó la exclusión por parsimonia |
| 13 | Importancia de variables | `cp12_importancia_permutacion.png` | Se amplió la gráfica y se añadió la advertencia de no causalidad |
| 14 | Selección y limitaciones | Extra Trees regularizado; Test reservado | Se justificó la selección por RMSE/R² sin presentarlo como ganador en MAE |

## Cifras contrastadas

- Extra Trees regularizado: MAE 50,0311 Wh; RMSE 85,3479 Wh; R² 0,1438.
- Baseline horario: MAE 36,8345 Wh; RMSE 91,3334 Wh.
- Consumo alto: 223 casos; MAE 211,1291 Wh; 97,31 % subestimados; residuo medio +209,39 Wh.
- Ablación: sin `rv` 85,3479 Wh; solo `rv1` o solo `rv2` 85,6291 Wh; ambas 84,9521 Wh.
- `rv1` y `rv2` son idénticas en las 19.735 filas; la mejora con ambas no representa dos fuentes independientes.

## Auditoría de fuga y uso de Test

- Las características temporales se calculan únicamente a partir de `date` en la misma fila.
- No se usan rezagos ni agregados de `Appliances`, ni observaciones posteriores.
- La división conserva el orden cronológico y el umbral P90 se calcula exclusivamente con Train.
- El escalado de Ridge está dentro de un `Pipeline` ajustado con Train.
- El bloque Test solo se delimita para reservarlo; no recibe predicciones ni métricas en CP09–CP13.

## Control visual y de apertura

- Formato verificado: 16:9, 14 diapositivas, tipografía Arial y paleta azul oscuro/blanco/cian/naranja.
- Se renderizaron y revisaron las 14 diapositivas. Se corrigieron desbordamientos en las diapositivas 2, 3, 6, 7, 10 y 12.
- El validador geométrico reportó cero defectos y cero advertencias de disposición.
- El paquete PowerPoint contiene 14 diapositivas y dos gráficos nativos; fue reabierto para verificar estructura y contenido.
- El guion fue abierto con Microsoft Word, exportado a PDF y revisado en sus seis páginas. Se corrigió un encabezado recortado y una fuente huérfana.

## Limitación técnica del validador

Los gráficos nativos de las diapositivas 8 y 12 contienen valores literales y caché de datos. El validador auxiliar intentó exigir y materializar un libro Excel embebido, pero su operación falló por permisos de su directorio temporal en Windows. La integridad del paquete, la importación de la presentación, la geometría y la apertura fueron verificadas por rutas independientes; este incidente no altera los datos ni el contenido visible.

