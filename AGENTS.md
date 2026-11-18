# Instrucciones permanentes del proyecto

## Alcance y preservación

- Este repositorio continúa el proyecto académico "Predicción del consumo energético de un edificio". No crear un proyecto paralelo ni sobrescribir los notebooks de Corte 1.
- `notebooks/01_eda_diagnostico.ipynb` y `notebooks/02_baseline_modelo_inicial.ipynb` son artefactos históricos de Corte 1. Cualquier ejecución, auditoría o desarrollo nuevo debe vivir en archivos nuevos.
- El dataset canónico es `data/energydata_complete.csv`, obtenido desde UCI. Los CSV y ZIP permanecen locales y no se versionan (`.gitignore`). No fabricar ni sustituir datos.
- Mantener el conjunto Test estrictamente reservado para Corte 3. En Corte 2, toda comparación, selección y ajuste usa solo Train y Validation cronológicos.

## Contrato de predicción y prevención de fuga

- Definir el instante de predicción antes de incluir variables: la predicción corresponde al consumo `Appliances` del registro actual y solo puede usar calendario y mediciones exógenas disponibles entonces. Nunca usar `Appliances` contemporáneo, futuro ni rezagos no disponibles.
- Transformadores, imputadores, escaladores, selectores y modelos se ajustan exclusivamente en Train. La validación se usa para evaluación y ajuste razonable, sin reordenar ni mezclar el tiempo.
- `rv1` y `rv2` se evalúan con ablaciones controladas. No interpretar mejoras como causalidad.

## Reproducibilidad

- Usar rutas relativas desde la raíz del repositorio. Documentar versiones, semilla, fuente de datos, hash, particiones, columnas y parámetros.
- Guardar resultados nuevos en archivos versionables bajo `reports/` y código reutilizable bajo `src/`; no depender de salidas efímeras de notebooks.
- Cada checkpoint debe registrar actividades, evidencia verificable, resultados reales y pendientes. Etiquetar resultados históricos como tales hasta reproducirlos.
- No enviar cambios a remoto. Se permiten commits locales pequeños y descriptivos tras verificaciones relevantes.

## Guía académica

- La guía oficial `Guia_Banco_Proyectos_Profundizacion_III_IA_2026-II.pdf` no está disponible en el workspace al iniciar CP08. No declarar cumplimiento académico integral hasta revisarla.
