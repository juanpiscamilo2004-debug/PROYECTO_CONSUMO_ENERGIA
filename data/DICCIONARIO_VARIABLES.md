# Diccionario básico de variables

## Dataset

**Appliances Energy Prediction - UCI Machine Learning Repository**

## Variables principales

| Variable | Tipo | Descripción / uso |
|---|---|---|
| `date` | Fecha/hora | Momento de la medición. Se utiliza para ordenar temporalmente los datos y crear características de calendario. |
| `Appliances` | Numérica | Variable objetivo. Consumo energético de electrodomésticos en Wh. |
| `lights` | Numérica | Consumo energético asociado a iluminación. |
| `T1` a `T9` | Numéricas | Mediciones de temperatura en diferentes zonas interiores del edificio. |
| `RH_1` a `RH_9` | Numéricas | Mediciones de humedad relativa en diferentes zonas interiores. |
| `T_out` | Numérica | Temperatura exterior. |
| `Press_mm_hg` | Numérica | Presión atmosférica. |
| `RH_out` | Numérica | Humedad relativa exterior. |
| `Windspeed` | Numérica | Velocidad del viento. |
| `Visibility` | Numérica | Visibilidad meteorológica. |
| `Tdewpoint` | Numérica | Temperatura de punto de rocío. |
| `rv1` | Numérica | Variable aleatoria incluida en el dataset. |
| `rv2` | Numérica | Variable aleatoria incluida en el dataset. En el archivo analizado resultó exactamente igual a `rv1`. |

## Características temporales derivadas en el proyecto

| Variable | Tipo | Descripción |
|---|---|---|
| `hour` | Entera | Hora del día, derivada de `date`. |
| `day_of_week` | Entera | Día de la semana, de 0 a 6. |
| `day_name` | Categórica | Nombre del día de la semana, utilizada principalmente en EDA. |
| `month` | Entera | Mes de la observación. |
| `weekend` | Binaria | 1 si la observación corresponde a sábado o domingo, 0 en caso contrario. |

## Variables auxiliares de análisis

Durante el EDA se construyó un indicador de consumo alto para estudiar la dificultad de predecir picos.

En el análisis predictivo, el umbral definitivo se calculó exclusivamente con Train:

**P90 Train = 220 Wh**

Este indicador se utiliza solamente para segmentar los errores y **no se utiliza como característica de entrada**, ya que está construido a partir de la variable objetivo `Appliances` y su uso como predictor produciría fuga de información.