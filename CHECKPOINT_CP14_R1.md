# Checkpoint CP14-R1 — Revisión final de presentación y guion

Fecha: 2026-11-18.

## Actividades ejecutadas

1. Auditoría de la guía, matriz de cumplimiento, checkpoint CP09–CP13, pipeline, reportes y artefactos CP14 existentes.
2. Contraste de métricas contra los CSV de benchmark, segmentos, picos, ablación e importancia.
3. Rediseño completo de la presentación en 14 diapositivas 16:9, preservando los archivos anteriores.
4. Actualización del guion para coincidir diapositiva por diapositiva y repartir la exposición entre cuatro integrantes.
5. Renderizado y revisión visual de todas las diapositivas y de las seis páginas del guion.
6. Verificación de apertura, estructura y contenido de PowerPoint y Word.

## Entregables

- `reports/presentacion/Corte2_CORTE2_FINAL_REVISADO.pptx`
- `reports/presentacion/Guion_Corte2_CORTE2_FINAL_REVISADO.docx`
- `docs/AUDITORIA_CP14_R1.md`
- `docs/TRAZABILIDAD_GRAFICAS_CORTE2.md`

## Distribución del guion

| Integrante | Diapositivas | Tiempo estimado | Tema principal |
|---|---:|---:|---|
| Juan Camilo Duran Ávila | 1–3 | 2:00 | Problema, continuidad y datos |
| Josep Stiven Londoño Leon | 4–7 | 2:30 | Características, pipeline y validación |
| Jeferson Stiven Prieto Guzman | 8–10 | 2:15 | Benchmark, serie temporal y residuos |
| Juan Esteban Lopez Moreno | 11–14 | 2:30 | Picos, ablación, importancia y cierre |

## Verificaciones

- 14 diapositivas, formato 16:9 y al menos una gráfica temporal real.
- Cero defectos y cero advertencias del validador geométrico.
- Seis páginas del guion revisadas visualmente después de abrir el DOCX con Word.
- Extra Trees se presenta como candidato provisional por RMSE/R², no como mejor MAE.
- La subestimación de picos queda explícita: 97,31 % de 223 casos altos.
- `rv1/rv2` se excluyen por duplicación exacta y parsimonia.
- Test permanece reservado; no se reentrenó ni reejecutó el benchmark.
- SHA-256 PPTX: `2A5D68EF9666913F6E71EC3991C97306D1C7B31722C2EF17E82D8E118C892471`.
- SHA-256 DOCX: `BD4FD6EDAB1E0A75D135AE06E6B5E1CF0B7E114DA01E63D654D47B7B248710B5`.

## Pendiente para Corte 3

Evaluar el candidato una sola vez sobre Test, estudiar robustez y sensibilidad, y construir el flujo de inferencia. Estas tareas no forman parte de CP14-R1.

