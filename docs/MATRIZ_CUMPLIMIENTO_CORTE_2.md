# Matriz de cumplimiento - Corte 2

Fuente revisada: `Guia_Banco_Proyectos_Profundizacion_III_IA_2026-II.pdf`, páginas 2, 3, 7 y 8.

| Requisito de la guía | Implementación prevista o existente | Evidencia | Estado |
|---|---|---|---|
| Pipeline reproducible de preprocesamiento y entrenamiento | Scripts nuevos bajo `src/`, con rutas relativas, semilla y separación cronológica | `src/audit_corte1.py`; pipeline CP09 pendiente | En progreso |
| Benchmark de alternativas comparables | Comparar regresores sobre el mismo Train/Validation, sin usar Test | Auditoría deja la referencia del Corte 1; benchmark CP10 pendiente | Pendiente |
| Validación temporal | Corte 1 definió Train/Validation/Test consecutivos: 13.814/2.960/2.961 | `reports/cp08_auditoria_corte1.json` confirma límites temporales | Cumplido para el protocolo; falta aplicar a CP10-CP12 |
| Ajuste razonable de hiperparámetros | Búsqueda acotada con parámetros y justificación explícitos, solo sobre validación | Registro de configuración CP11 pendiente | Pendiente |
| Características temporales sin datos futuros | Calendario derivado de `date`; documentar disponibilidad de cada entrada | Corte 1 usa `hour`, día, mes y fin de semana; extensión CP09 pendiente | En progreso |
| Métricas MAE, RMSE y R² | Calcular las tres métricas en validación y por segmentos normal/alto | Réplica CP08 confirmó las métricas base | Cumplido como referencia; falta para modelos CP10 |
| Análisis de residuos y picos | Residuos, errores extremos, alto consumo según P90 entrenado, gráficas temporales | P90 Train=220 Wh confirmado; análisis CP12 pendiente | En progreso |
| Importancia de variables | Importancia por permutación o mecanismo compatible con el modelo seleccionado | Análisis CP12 pendiente | Pendiente |
| Ablación de `rv1` y `rv2` | Ejecutar configuraciones sin aleatorias, con `rv1`, con `rv2` y con ambas | CP08 confirma igualdad exacta de ambas; experimento CP12 pendiente | En progreso |
| Modelo provisional y alternativas descartadas | Selección basada en validación, interpretabilidad y errores, no solo una métrica | Decisión CP13 pendiente | Pendiente |
| README, diagrama de flujo y bitácora de IA actualizados | Actualizar documentos y registrar validaciones de IA | README y bitácora existentes; actualización Corte 2 pendiente | En progreso |
| Presentación de Corte 2 con evidencia y gráfica temporal | Preparar sustentación de 8-10 minutos con benchmark, validación, errores, decisión y gráfica temporal | Presentación CP14 pendiente | Pendiente |
| Test reservado para Corte 3 | Prohibir su uso en selección, ajuste y comparación de Corte 2 | `AGENTS.md`, `CHECKPOINT_CP08.md` y la auditoría conservan el bloque sin evaluar | Cumplido |
| Fuente y trazabilidad del dataset | Conservar referencia UCI, DOI y la guía oficial | `data/README.md`, SHA-256 en CP08 y copia idéntica de la guía en `docs/` | Cumplido |

## Nota de interpretación

La guía define el Corte 2 como benchmark, validación y análisis de errores. La evaluación final del bloque Test, la función de inferencia y la profundización final pertenecen al Corte 3. Cualquier resultado nuevo de Corte 2 debe declararse como validación, no como desempeño final.
