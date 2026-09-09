# Bitácora de uso de IA generativa

## Herramienta utilizada

ChatGPT - OpenAI

## Propósito de uso

La herramienta de IA generativa fue utilizada como apoyo para:

- interpretar la guía del proyecto;
- estructurar el Corte 1;
- proponer código para carga, diagnóstico y EDA;
- orientar la partición temporal;
- implementar baselines y modelos lineales;
- interpretar MAE, RMSE, R² y residuos;
- documentar decisiones metodológicas;
- organizar el repositorio y la documentación.

## Interacciones relevantes

### 1. Formulación del proyecto
Se utilizó IA para estructurar el problema, objetivo general, objetivos específicos, beneficiario, riesgos y criterio de éxito.

### 2. Análisis exploratorio
Se utilizaron sugerencias de código para analizar:
- estructura del dataset;
- valores faltantes;
- duplicados;
- distribución de Appliances;
- patrones diarios y semanales;
- variables ambientales;
- correlaciones;
- variables v1 y v2.

### 3. Partición temporal
La IA sugirió una división cronológica 70/15/15 y se verificó manualmente que no existiera solapamiento temporal entre Train, Validation y Test.

### 4. Línea base y modelos
Se utilizaron sugerencias para implementar:
- baseline de mediana histórica;
- baseline de mediana por hora;
- Regresión Lineal;
- Ridge con StandardScaler.

### 5. Análisis de errores
Se utilizó IA para orientar el análisis de:
- MAE;
- RMSE;
- R²;
- residuos;
- episodios de alto consumo;
- subestimación de picos.

## Validación realizada

Todas las métricas, tablas y resultados reportados fueron obtenidos ejecutando directamente el código sobre el archivo energydata_complete.csv.

Las salidas fueron revisadas antes de incorporarse a las conclusiones.

No se utilizaron valores inventados como resultados experimentales.

## Aporte propio

Las decisiones finales del proyecto, la ejecución de los notebooks, la validación de resultados, la interpretación de las salidas y la organización de los entregables fueron realizadas y revisadas por el equipo.

La IA fue utilizada como herramienta de apoyo y no como sustituto de la validación técnica del trabajo.
