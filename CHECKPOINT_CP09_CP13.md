# CP09-CP13 - Pipeline, benchmark y modelo provisional

## Verificaciones

- Predicción: calendario desde `date` y lecturas exógenas contemporáneas; no incluye objetivo, rezagos ni futuro.
- Partición: Train 13.814, Validation 2.960 y Test 2.961. Test no se transforma, ajusta, predice ni puntúa.
- Ajuste: parámetros predefinidos, búsqueda acotada y semilla 2026.

## Benchmark de Validation

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| Extra Trees regularizado | 50,0311 | **85,3479** | **0,1438** |
| HistGradientBoosting shallow | 48,0908 | 87,1986 | 0,1063 |
| HistGradientBoosting medium | 50,3950 | 88,3101 | 0,0834 |
| Baseline horario Corte 1 | **36,8345** | 91,3334 | 0,0195 |

Modelo provisional: `ExtraTreesRegressor(n_estimators=300, max_features=0.7, min_samples_leaf=3, random_state=2026)`, sin `rv1/rv2`, por RMSE y R². El baseline horario conserva el mejor MAE.

## Ablación y errores

- `rv1` y `rv2` son idénticas. Una sola empeora RMSE a 85,6291 Wh; ambas logran 84,9521 Wh, efecto no independiente por duplicación. Se conserva exclusión por parsimonia.
- Normal: MAE 36,9054 Wh, RMSE 50,0652 Wh (2.737 filas).
- Alto (>=220 Wh): MAE 211,1291 Wh, RMSE 256,7566 Wh y subestimación 97,31% (223 filas).
- Mayor error: 30/04/2016 10:00, real 840 Wh, predicción 106,61 Wh, error 733,39 Wh.
- Importancia: `hour_cos`, `hour_sin`, `T3`, `T6`, `T_out` y `T2`; asociación predictiva, no causalidad.

## Evidencias

`src/corte2_pipeline.py`, benchmark, configuración, ablación, residuos, picos, importancias y las tres gráficas en `reports/`.
