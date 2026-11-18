# Checkpoint CP08 - auditoría inicial

Fecha: 2026-11-18

## Actividades ejecutadas

- Se verificó Git y se clonó el repositorio oficial en esta carpeta.
- Se verificó `main` contra `origin/main`, con `HEAD` en `5dd4183` (`Documentar diccionario de variables`) y sin cambios de trabajo previos.
- Se descargó el archivo oficial de UCI y se extrajo `data/energydata_complete.csv`. El ZIP temporal se eliminó. El CSV queda protegido de Git por `.gitignore`.
- Se revisaron README, requisitos, diccionario, bitácora y el código de los dos notebooks de Corte 1 sin modificarlos.
- Se creó un entorno local `.venv` ignorado por Git para auditorías y experimentos reproducibles.

## Datos y evidencia inicial

- Fuente: UCI Appliances Energy Prediction, identificador 374, DOI `10.24432/C5VC8G`.
- Archivo local: `data/energydata_complete.csv`.
- SHA-256 registrado: `2820BF712AD0275CB18B85A05250926100D8E65EBB9F4D2D016CA91EA152A25D`.
- La auditoría programática pendiente debe confirmar forma, columnas, duplicados, valores ausentes y equivalencia `rv1 == rv2` antes de citar cualquier métrica.

## Hallazgos y riesgos

- Los notebooks de Corte 1 no contienen celdas ejecutadas guardadas. El README presenta métricas históricas, pero aún no constituyen una reproducción local.
- Los notebooks usan la ruta de Colab `/content/energydata_complete.csv`; no se deben ejecutar tal cual para la auditoría local. La réplica debe ser un artefacto nuevo y reproducible.
- El README describe carpetas `reports/`, `src/` y `models/`, pero no estaban versionadas porque Git no conserva directorios vacíos.
- La guía oficial `Guia_Banco_Proyectos_Profundizacion_III_IA_2026-II.pdf` no se encontró en el workspace. Se requiere el archivo para certificar cumplimiento académico literal.

## Siguiente paso

1. Ejecutar la auditoría independiente de Corte 1 contra el CSV oficial y comparar métricas con las referencias documentadas.
2. Entregar la guía oficial para contrastar los entregables y criterios de Corte 2.
3. Después de confirmar CP08, crear el pipeline temporal de CP09 sin usar Test.

## Resultados verificados

La réplica independiente `src/audit_corte1.py` se ejecutó con el CSV oficial y escribió `reports/cp08_auditoria_corte1.json`.

| Modelo | MAE (Wh) | RMSE (Wh) | R² |
|---|---:|---:|---:|
| Mediana histórica | 42.6047 | 98.1076 | -0.1313 |
| Mediana por hora | 36.8345 | 91.3334 | 0.0195 |
| Regresión Lineal | 52.7217 | 86.2030 | 0.1266 |
| Ridge (`alpha=1.0`) | 52.7614 | 86.2064 | 0.1265 |

La réplica confirma 19.735 filas y 29 columnas originales, cero valores ausentes, cero filas duplicadas, fechas de `2016-01-11 17:00:00` a `2016-05-27 18:00:00`, y equivalencia exacta entre `rv1` y `rv2`. La división cronológica coincide con 13.814/2.960/2.961 registros y P90 de Train igual a 220 Wh.

## Guía académica revisada

La guía oficial se recibió, se copió sin alteraciones a `docs/Guia_Banco_Proyectos_Profundizacion_III_IA_2026-II.pdf` y se verificó contra el original mediante SHA-256 `6046700A312ABDB228E746A0A760F8D32C1ACCAB64F460A15BAC6EE007268958`.

Para el Proyecto 4, Corte 2, la guía exige características temporales sin futuro, benchmark con validación temporal, residuos y picos, importancia de variables, verificación de `rv1/rv2`, selección de modelo provisional y presentación con una gráfica temporal. La trazabilidad requisito-evidencia queda en `docs/MATRIZ_CUMPLIMIENTO_CORTE_2.md`.
