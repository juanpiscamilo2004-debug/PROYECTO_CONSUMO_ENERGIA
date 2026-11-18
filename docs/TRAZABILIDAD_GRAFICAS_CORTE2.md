# Trazabilidad de gráficas — Corte 2

Todas las visualizaciones de la presentación revisada proceden de resultados ejecutados en CP09–CP13. No se utilizaron valores simulados ni ilustrativos.

| Diapositiva | Visualización | Archivo o datos originales | Script generador | Modelo | Partición | Verificación de ejes, cifras y leyendas |
|---:|---|---|---|---|---|---|
| 8 | Ranking de RMSE y tarjetas MAE/R² | `reports/cp10_benchmark_validacion.csv` | Gráfico nativo construido por el generador de la presentación a partir del CSV; resultados producidos por `src/corte2_pipeline.py` | Todos los modelos del benchmark | Validation, 2.960 filas | Barras en RMSE (Wh); orden ascendente; ET 85,3479, HGB shallow 87,1986 y baseline horario 91,3334. Tarjetas: MAE 36,8345 y R² 0,1438 |
| 9 | Serie real vs. predicha | `reports/cp12_serie_temporal_validacion.png`; datos de `reports/cp12_residuos_validacion.csv` | `src/corte2_pipeline.py`, función de generación de figuras | Extra Trees regularizado | Primera semana de Validation | Eje x fecha; eje y `Appliances` (Wh); leyendas consumo real, predicción y P90 Train = 220 Wh |
| 10 | Residuos frente al consumo real | `reports/cp12_residuos_validacion.png`; `reports/cp12_residuos_validacion.csv`; `reports/cp12_metricas_por_segmento.csv` | `src/corte2_pipeline.py`, función de generación de figuras | Extra Trees regularizado | Validation completa | Eje x consumo real (Wh); eje y real − predicción (Wh); color por umbral 220 Wh. Tarjetas coinciden con 2.737/223 casos y MAE 36,9054/211,1291 Wh |
| 11 | Tarjetas del peor pico | `reports/cp12_picos_peores_predichos.csv` | Resultados producidos por `src/corte2_pipeline.py`; composición nativa en la presentación | Extra Trees regularizado | Validation | 2016-04-30 10:00; real 840 Wh; predicción 106,61 Wh; error absoluto 733,39 Wh |
| 12 | Ablación `rv1/rv2` | `reports/cp12_ablacion_rv.csv` | Gráfico nativo construido por el generador de la presentación a partir del CSV; experimento en `src/corte2_pipeline.py` | Extra Trees regularizado en cuatro configuraciones | Misma Validation | RMSE (Wh): 85,3479; 85,6291; 85,6291; 84,9521. Mismo modelo, mismas filas y misma semilla |
| 13 | Importancia por permutación | `reports/cp12_importancia_permutacion.png`; `reports/cp12_importancia_permutacion.csv` | `src/corte2_pipeline.py` | Extra Trees regularizado | Validation, diez permutaciones | Eje x aumento de MAE (Wh); eje y variables; `hour_cos` 8,5589 y `hour_sin` 7,6906 encabezan; barras de error representan variabilidad |

## Controles adicionales

- Los títulos de cada gráfica identifican Validation y nunca Test.
- Las cifras de diapositivas y guion se formatean a cuatro decimales, sin cambiar los valores de los CSV.
- Las gráficas PNG originales se insertan sin edición de datos; solo se ajustan de tamaño con relación de aspecto conservada.
- Las gráficas nativas de benchmark y ablación se construyen directamente con los valores de los CSV y se validaron contra ellos.

