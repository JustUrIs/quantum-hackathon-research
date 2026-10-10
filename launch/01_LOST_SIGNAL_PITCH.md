# LOST SIGNAL: guion y estrategia

## La escena de apertura

Mostrar el mapa antes de explicar física. Apagar GPS. Dar al espectador una decisión: elegir un instrumento con un presupuesto fijo. La sorpresa ocurre cuando el instrumento que ganaba pierde al subir el ruido.

## Video de 2:30, narración en inglés

| Tiempo | Pantalla | Voz |
|---|---|---|
| 0:00–0:15 | Mapa, botón Cut GPS | “You are flying south over Patagonia. The position signal disappears. You still have the Earth's magnetic field. What would you need to measure it well?” |
| 0:15–0:40 | Cuatro probes, η 0.08, 256 readings | “We built LOST SIGNAL to explore that question. These two sensors use the same number of probes and readings. In this fixed-time model, entanglement improves local phase precision by about 1.57 times.” |
| 0:40–1:05 | Subir ruido hasta superar cruce | “Now increase noise. The entangled state loses coherence faster, and the independent probes win. You can locate the crossover instead of assuming quantum is better.” |
| 1:05–1:25 | Franjas y curva | “The fringes come from Ramsey and GHZ circuits. We check the noise equations independently with Qiskit density matrices. Random outputs contain no phase information.” |
| 1:25–1:50 | Molecular, quitar anisotropía | “The second experiment uses two electron spins and a nuclear spin. A directional coupling makes the reaction yield depend on the field angle. Remove that coupling, and the compass response goes flat.” |
| 1:50–2:10 | Backend y JSON | “One circuit checks both sensor responses on the selected backend. The exported record includes the exact settings, counts and uncertainty. The geographic context comes from WMM2025.” |
| 2:10–2:30 | Mapa con nota de alcance | “This is a sensing experiment, not a flight-navigation system. Our next step is to replace the illustrative noise with recorded sensor data and test an optimized baseline. Try the mission and find the conditions where entanglement earns its place.” |

Si se muestra un resultado local, decir “local simulator”. Usar “IonQ simulator” únicamente al mostrar una corrida real identificada así. No llenar el video con terminales. Grabar 1440×900, zoom legible, cursor quieto durante cada resultado.

## Respuestas al jurado

**¿Reemplaza GPS?** No. WMM aporta contexto físico; el corredor ilustra propagación de incertidumbre angular. No hay localizador magnético, filtro de navegación ni validación de vuelo.

**¿El baseline es fuerte?** Compara sensores separables óptimos en cuadratura al mismo N×M y tiempo fijo. Para un caso industrial falta optimizar tiempos y sumar costo de preparación, calibración y ruido medido.

**¿La ventaja sobrevive al ruido?** En ciertos parámetros del modelo sí; el cruce es visible. No afirmamos escalamiento Heisenberg robusto a ruido markoviano con tiempo optimizado.

**¿El pájaro es un sensor GHZ?** No. Son dos mecanismos físicos diferentes en dos experimentos separados. El radical-pair es un modelo mínimo, no una réplica de una especie.

**¿Qué es nuevo?** La experiencia de decisión con recursos explícitos, ablation molecular, procedencia y evidencia exportable. No un nuevo límite de metrología.

## Hipótesis comercial, después del evento

Primer comprador a investigar: un laboratorio o integrador que evalúe sensores antes de conseguir hardware. Primer producto vendible: un estudio comparativo reproducible de una misión y un conjunto de datos de ruido. Entregable: condiciones de operación donde un sensor mejora una métrica, y condiciones donde no.

Propuesta de conversación: “Con tus registros y tu baseline, podemos construir una comparación reproducible para decidir qué experimento físico vale la pena financiar.” No vender una precisión que todavía no medimos.

Piloto acotado: un dataset, una misión, dos baselines, revisión por el equipo de sensado. Criterio de continuidad: el informe cambia una decisión de integración o evita un experimento inútil. Criterio de abandono: no consiguen datos o el cliente solo quiere una visualización educativa sin presupuesto para validación. El rango de precio debe surgir de esas entrevistas; aún no hay evidencia de disposición a pagar.

Riesgo de competencia: ya existe investigación sobre simuladores de sensores cuánticos para navegación, por ejemplo [Southampton](https://www.southampton.ac.uk/study/postgraduate-research/projects/quantum-technologies-for-gnss-denied-navigation-a-quantum). Una interfaz bonita no es una barrera de entrada. Datos de calibración, validación y reproducibilidad sí pueden convertirse en activos si el piloto funciona.
