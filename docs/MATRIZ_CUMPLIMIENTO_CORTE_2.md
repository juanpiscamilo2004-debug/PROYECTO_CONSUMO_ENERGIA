# Matriz de cumplimiento - Corte 2

Fuente revisada: `Guia_Banco_Proyectos_Profundizacion_III_IA_2026-II.pdf`, páginas 2, 3, 7 y 8.

| Requisito de la guía | Implementación prevista o existente | Evidencia | Estado |
|---|---|---|---|
| Pipeline reproducible de preprocesamiento y entrenamiento | Script con rutas relativas, semilla y separación cronológica | `src/corte2_pipeline.py` | Cumplido |
| Benchmark de alternativas comparables | Baselines, Ridge, HistGradientBoosting y Extra Trees bajo la misma partición | `reports/cp10_benchmark_validacion.csv` | Cumplido |
| Validación temporal | Train/Validation/Test consecutivos: 13.814/2.960/2.961; selección solo en Validation | `reports/cp08_auditoria_corte1.json`, `reports/cp11_configuracion_y_metadatos.json`, diapositiva 6 revisada | Cumplido |
| Ajuste razonable de hiperparámetros | Configuraciones acotadas de regularización/capacidad, solo Train/Validation | `reports/cp11_configuracion_y_metadatos.json` | Cumplido |
| Características temporales sin datos futuros | Seno/coseno de hora, día semanal y día del año, más `weekend`, derivados solo de `date` | `src/corte2_pipeline.py`, diapositiva 4 revisada | Cumplido |
| Métricas MAE, RMSE y R² | Las tres métricas en Validation y errores por segmentos normal/alto | `reports/cp10_benchmark_validacion.csv`, `reports/cp12_metricas_por_segmento.csv`, diapositivas 8 y 10 | Cumplido |
| Análisis de residuos y picos | Residuos, extremos, segmentos P90 y gráficas | `reports/cp12_*` | Cumplido |
| Importancia de variables | Permutación sobre Validation del modelo provisional | `reports/cp12_importancia_permutacion.csv` | Cumplido |
| Ablación de `rv1` y `rv2` | Sin variables aleatorias, con cada una por separado y con ambas; mismo modelo y Validation | `reports/cp12_ablacion_rv.csv`, diapositiva 12 revisada | Cumplido |
| Modelo provisional y alternativas descartadas | Extra Trees regularizado seleccionado por RMSE/R², declarando que el baseline horario conserva mejor MAE | `CHECKPOINT_CP09_CP13.md`, diapositivas 8 y 14 revisadas | Cumplido |
| README, diagrama de flujo y bitácora de IA actualizados | Documentación de reproducibilidad, flujo y uso de IA actualizada en CP13 | `README.md`, `docs/DIAGRAMA_PIPELINE_CORTE2.md`, `AI_USE_LOG.md` | Cumplido |
| Presentación de Corte 2 con evidencia y gráfica temporal | Presentación profesional de 14 diapositivas y guion equilibrado para cuatro integrantes | `reports/presentacion/*CORTE2_FINAL_REVISADO*`, `docs/AUDITORIA_CP14_R1.md` | Cumplido |
| Test reservado para Corte 3 | Prohibir su uso en selección, ajuste y comparación de Corte 2 | `AGENTS.md`, `CHECKPOINT_CP08.md` y la auditoría conservan el bloque sin evaluar | Cumplido |
| Fuente y trazabilidad del dataset | Conservar referencia UCI, DOI y la guía oficial | `data/README.md`, SHA-256 en CP08 y copia idéntica de la guía en `docs/` | Cumplido |

## Nota de interpretación

La guía define el Corte 2 como benchmark, validación y análisis de errores. La evaluación final del bloque Test, la función de inferencia y la profundización final pertenecen al Corte 3. Cualquier resultado nuevo de Corte 2 debe declararse como validación, no como desempeño final.

La revisión CP14-R1 verificó la trazabilidad de todas las gráficas y cifras. Véanse `docs/TRAZABILIDAD_GRAFICAS_CORTE2.md` y `CHECKPOINT_CP14_R1.md`.
