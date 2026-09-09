# Predicción del consumo energético de un edificio

## Proyecto de Profundización III - Inteligencia Artificial

**Proyecto seleccionado:** Proyecto 4 - Predicción del consumo energético de un edificio  
**Corte:** 1 - Formulación, datos y línea base  
**Tipo de problema:** Regresión con estructura temporal  
**Dataset:** Appliances Energy Prediction - UCI Machine Learning Repository  
**Variable objetivo:** `Appliances` (Wh)

## Integrantes

- Juan Camilo Duran Ávila
- Josep Stiven Londoño Leon
- Jeferson Steven Prieto Guzman
- Juan Esteban Lopez Moreno 

## 1. Descripción del proyecto

El proyecto busca desarrollar y evaluar modelos de regresión capaces de predecir el consumo energético de los electrodomésticos de un edificio a partir de información temporal y variables ambientales disponibles en el momento de realizar la predicción.

El conjunto de datos presenta una estructura temporal con mediciones realizadas aproximadamente cada 10 minutos. Por esta razón, la evaluación se diseñó respetando el orden cronológico de las observaciones y evitando una separación aleatoria entre entrenamiento, validación y prueba.

### Pregunta del proyecto

¿En qué medida es posible predecir el consumo energético de los electrodomésticos de un edificio a partir de información temporal y condiciones ambientales disponibles en el momento de realizar la predicción?

## 2. Objetivo general

Desarrollar y evaluar un modelo de regresión para predecir el consumo energético de los electrodomésticos de un edificio a partir de variables temporales y ambientales, utilizando un protocolo de evaluación temporal que evite fugas de información y permita comparar el modelo contra líneas base sencillas.

### Objetivos específicos

1. Explorar y caracterizar el dataset e identificar su estructura temporal y calidad de datos.
2. Analizar los patrones diarios y semanales del consumo energético.
3. Examinar las variables de temperatura, humedad, condiciones meteorológicas y las variables aleatorias `rv1` y `rv2`.
4. Diseñar una separación cronológica de entrenamiento, validación y prueba.
5. Construir líneas base cuantitativas para establecer referencias de desempeño.
6. Implementar y evaluar modelos iniciales de Regresión Lineal y Ridge.
7. Comparar los modelos mediante MAE, RMSE y R².
8. Analizar los errores durante periodos de consumo normal y consumo elevado.

## 3. Dataset

Se utiliza el conjunto de datos **Appliances Energy Prediction** del UCI Machine Learning Repository.

El archivo utilizado es:

`energydata_complete.csv`

Características verificadas durante el análisis:

- 19.735 observaciones.
- 29 columnas en el archivo CSV, incluyendo `date`.
- Mediciones aproximadamente cada 10 minutos.
- Periodo comprendido entre el 11 de enero y el 27 de mayo de 2016.
- Variable objetivo: `Appliances`, expresada en Wh.
- No se identificaron valores faltantes.
- No se identificaron filas completamente duplicadas.

El conjunto contiene información sobre consumo energético, temperaturas y humedades interiores, condiciones meteorológicas externas y variables adicionales.

Durante la auditoría se comprobó que `rv1` y `rv2` son exactamente iguales entre sí en el archivo analizado. Estas variables fueron tratadas con precaución debido a su naturaleza aleatoria y no fueron utilizadas en los primeros modelos lineales.

## 4. Protocolo de evaluación

Debido a la naturaleza temporal del problema, no se utilizó una partición aleatoria.

Los datos fueron ordenados cronológicamente y separados de la siguiente manera:

| Conjunto | Proporción | Registros | Periodo |
|---|---:|---:|---|
| Train | 70% | 13.814 | 11/01/2016 17:00 - 16/04/2016 15:10 |
| Validation | 15% | 2.960 | 16/04/2016 15:20 - 07/05/2016 04:30 |
| Test | 15% | 2.961 | 07/05/2016 04:40 - 27/05/2016 18:00 |

La estructura de evaluación es:

**Pasado → Train → Validation → Test → Futuro**

El conjunto de prueba final permanece reservado y no se utiliza para seleccionar características, modelos o hiperparámetros.

Esta estrategia busca evitar que observaciones temporalmente cercanas sean distribuidas artificialmente entre entrenamiento y evaluación, lo que podría generar una estimación demasiado optimista del desempeño.

## 5. Modelos evaluados

Durante el Corte 1 se evaluaron cuatro aproximaciones:

1. Baseline de mediana histórica.
2. Baseline temporal basado en la mediana por hora del día.
3. Regresión Lineal.
4. Regresión Ridge con estandarización de características.

Los modelos fueron comparados sobre el mismo conjunto temporal de validación.

### Métricas

Se utilizaron:

- **MAE (Mean Absolute Error):** representa la magnitud promedio del error absoluto.
- **RMSE (Root Mean Squared Error):** penaliza con mayor intensidad los errores grandes.
- **R²:** permite evaluar la proporción de variabilidad explicada por el modelo respecto a una referencia basada en la media.

MAE y RMSE se reportan en Wh.

## 6. Resultados del Corte 1

| Modelo | MAE (Wh) ↓ | RMSE (Wh) ↓ | R² ↑ |
|---|---:|---:|---:|
| Baseline - Mediana histórica | 42,60 | 98,11 | -0,1313 |
| Baseline - Mediana por hora | **36,83** | 91,33 | 0,0195 |
| Regresión Lineal | 52,72 | **86,20** | **0,1266** |
| Ridge | 52,76 | 86,21 | 0,1265 |

El baseline horario obtuvo el menor MAE, mientras que la Regresión Lineal obtuvo el menor RMSE y el mayor R².

Esto demuestra que no existe un único método superior bajo todos los criterios evaluados.

## 7. Análisis de periodos de alto consumo

Para el análisis predictivo se calculó el percentil 90 de `Appliances` utilizando exclusivamente el conjunto de entrenamiento.

El umbral obtenido fue:

**P90 Train = 220 Wh**

Por lo tanto:

- Consumo normal: `< 220 Wh`
- Consumo alto: `>= 220 Wh`

Los resultados segmentados fueron:

| Segmento | MAE Baseline horario | MAE Regresión Lineal | RMSE Baseline horario | RMSE Regresión Lineal |
|---|---:|---:|---:|---:|
| Consumo normal | **16,17** | 39,69 | **23,89** | 50,57 |
| Consumo alto | 290,40 | **212,64** | 322,06 | **259,33** |

El baseline horario representa mejor los consumos habituales, mientras que la Regresión Lineal reduce parcialmente los errores durante episodios de consumo elevado.

Sin embargo, ambos métodos presentan dificultades importantes ante los picos:

- El baseline horario subestimó el **100%** de los episodios de alto consumo.
- La Regresión Lineal subestimó el **95,07%**.

El peor error absoluto identificado para la Regresión Lineal fue aproximadamente **732,02 Wh**, correspondiente a un consumo real de 840 Wh y una predicción cercana a 107,98 Wh.

Estos resultados muestran que la predicción de episodios de consumo elevado constituye una de las principales limitaciones del modelo inicial.


## 8. Estructura del repositorio

El repositorio está organizado de la siguiente manera:

```text
PROYECTO_CONSUMO_ENERGIA/
│
├── README.md
├── AI_USE_LOG.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── README.md
│
├── notebooks/
│   ├── 01_eda_diagnostico.ipynb
│   └── 02_baseline_modelo_inicial.ipynb
│
├── reports/
├── src/
└── models/
```

### Contenido principal

- `notebooks/01_eda_diagnostico.ipynb`: carga, diagnóstico y análisis exploratorio de datos.
- `notebooks/02_baseline_modelo_inicial.ipynb`: partición temporal, líneas base, Regresión Lineal, Ridge y análisis de errores.
- `data/README.md`: instrucciones para obtener el dataset desde su fuente original.
- `requirements.txt`: dependencias principales del proyecto.
- `AI_USE_LOG.md`: bitácora del uso de inteligencia artificial generativa.
- `reports/`: carpeta destinada a figuras y materiales de presentación.
- `src/`: carpeta preparada para código reutilizable en etapas posteriores.
- `models/`: carpeta preparada para modelos generados en etapas posteriores.

## 9. Reproducción del proyecto

### Requisitos

Se recomienda utilizar Python 3 y las dependencias incluidas en `requirements.txt`.

Las principales librerías utilizadas son:

- pandas
- numpy
- matplotlib
- scikit-learn
- jupyter

Para instalar las dependencias localmente:

```bash
pip install -r requirements.txt
```

### Obtención de los datos

El dataset no se almacena directamente en este repositorio.

Las instrucciones para obtener `energydata_complete.csv` desde el UCI Machine Learning Repository se encuentran en:

`data/README.md`

### Ejecución de los notebooks

Los notebooks deben ejecutarse en el siguiente orden:

1. `notebooks/01_eda_diagnostico.ipynb`
2. `notebooks/02_baseline_modelo_inicial.ipynb`

Los experimentos originales del Corte 1 fueron desarrollados utilizando Google Colab.

Antes de ejecutar los notebooks en Colab se debe cargar el archivo:

`energydata_complete.csv`

La ruta utilizada durante los experimentos fue:

`/content/energydata_complete.csv`

## 10. Limitaciones

Los resultados obtenidos durante el Corte 1 deben interpretarse considerando las siguientes limitaciones:

1. **Dificultad para predecir picos:** los errores aumentan considerablemente durante los episodios de consumo elevado.

2. **Subestimación del consumo alto:** el baseline horario subestimó el 100% de los episodios de alto consumo y la Regresión Lineal el 95,07%.

3. **Capacidad explicativa limitada:** aunque la Regresión Lineal obtuvo el mejor RMSE y R² entre los modelos evaluados, su R² de 0,1266 indica que una parte considerable de la variabilidad del consumo continúa sin ser explicada.

4. **Posibles relaciones no lineales:** las relaciones entre las variables temporales, ambientales y el consumo pueden presentar comportamientos que los modelos lineales iniciales no representan adecuadamente.

5. **Variabilidad temporal:** la proporción de episodios de alto consumo presentó diferencias entre Train, Validation y Test, lo que refuerza la necesidad de conservar una evaluación temporal.

6. **Predicción no implica causalidad:** una variable que resulte útil para predecir el consumo no necesariamente constituye una causa del consumo. Por lo tanto, no puede concluirse que modificar una variable predictora produzca directamente un ahorro energético.

7. **Alcance de los datos:** los resultados corresponden al edificio y al periodo temporal representados en el dataset analizado, por lo que no deben generalizarse automáticamente a otros edificios o condiciones.

8. **Conjunto de prueba reservado:** el conjunto Test permanece sin utilizar para la selección de modelos o hiperparámetros. Los resultados principales reportados en este Corte corresponden al conjunto temporal de Validation.

## 11. Próximos pasos

Los resultados del Corte 1 establecen una línea base reproducible y permiten identificar las principales dificultades del problema. En las siguientes etapas del proyecto se propone:

- desarrollar características temporales y rezagos de manera controlada;
- evaluar modelos capaces de representar relaciones no lineales;
- comparar los nuevos modelos contra las líneas base establecidas en el Corte 1;
- mantener un protocolo de validación que respete el orden temporal de los datos;
- profundizar en el análisis de los episodios de alto consumo;
- estudiar la importancia y utilidad predictiva de las variables;
- analizar el compromiso entre desempeño, interpretabilidad y costo computacional;
- conservar el conjunto Test para la evaluación final independiente.

## 12. Uso de inteligencia artificial generativa

Durante el desarrollo del Corte 1 se utilizó ChatGPT de OpenAI como herramienta de apoyo para la estructuración metodológica, generación y revisión de código, interpretación de resultados y elaboración de documentación.

Las sugerencias generadas mediante IA fueron verificadas a través de la ejecución directa del código sobre el dataset y la revisión de las métricas, tablas y visualizaciones obtenidas.

La IA se utilizó como herramienta de apoyo y no como sustituto de la validación técnica ni de la interpretación de los resultados por parte del equipo.

La bitácora de interacciones relevantes, propósito de uso, validaciones realizadas y aporte propio se encuentra en:

`AI_USE_LOG.md`

## 13. Referencias

- UCI Machine Learning Repository. *Appliances Energy Prediction*. DOI: 10.24432/C5VC8G.

- Candanedo, L. M., Feldheim, V., & Deramaix, D. (2017). *Data driven prediction models of energy use of appliances in a low-energy house*. Energy and Buildings, 140, 81-97.

- Scikit-learn Developers. *Scikit-learn documentation*. Documentación consultada para Regresión Lineal, Ridge, StandardScaler y métricas de regresión.

- The pandas development team. *pandas documentation*. Documentación utilizada para manipulación, análisis y transformación de datos.

- NumPy Developers. *NumPy documentation*. Documentación utilizada para operaciones numéricas.

- Matplotlib Development Team. *Matplotlib documentation*. Documentación utilizada para la construcción de visualizaciones.

- OpenAI. *ChatGPT*. Herramienta de inteligencia artificial generativa utilizada como apoyo metodológico, técnico y documental. El detalle de su utilización se encuentra en `AI_USE_LOG.md`.










