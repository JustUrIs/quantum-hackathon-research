# Q-DAY CLOCK: guion y estrategia

## Abrir con el experimento, no con una profecía

Mostrar dos distribuciones idénticas. Preguntar cuál realizó el trabajo. Revelar que una ya recibió el período. El reloj aparece después para conectar la auditoría con una decisión concreta.

## Video de 2:30, narración en inglés

| Tiempo | Pantalla | Voz |
|---|---|---|
| 0:00–0:15 | Dos circuitos, un histograma | “These two quantum demos produce the same peaks. One builds modular multiplication. The other is given the answer. Could you tell from the result alone?” |
| 0:15–0:40 | N15 a2, gate counts y leaked period | “This circuit receives only the public number and base. Its phase register drives reversible arithmetic. This imitation computes the period classically and prepares the expected output. We show the leaked input.” |
| 0:40–1:00 | Botón random, 21.875% | “Replace the phase outputs with random bits. The same recovery code still finds factors in about 22 percent of attempts. On tiny examples, success alone is weak evidence.” |
| 1:00–1:20 | Trial division y N33 a2 | “Classical trial division wins easily here. And the genuine quantum algorithm can fail: this base for 33 gives a useless square root. Change the base, and useful factors return.” |
| 1:20–1:40 | Backend con N15 | “One backend job produces counts and explicit factor witnesses. The record keeps the settings and source. These small circuits teach the algorithm; their synthesis cost does not extrapolate to RSA.” |
| 1:40–2:05 | Reloj y lifetime | “The real planning question is how long your data must stay private. Choose an assumed attack horizon, a confidentiality lifetime and a migration duration. The clock makes those assumptions visible.” |
| 2:05–2:30 | Papers, exportar | “Published resource estimates explain what future machines would require under specific assumptions. They do not give us a delivery date. Q-DAY CLOCK's evidence room helps you question the demo and document the decision.” |

No decir que atacamos RSA-2048 ni que 2029 es una fecha probada. El slider es un supuesto elegido por el usuario. Distinguir “resultados de un circuito pequeño”, “estimaciones publicadas” y “supuestos de planificación”.

## Respuestas al jurado

**¿La factorización es genuina?** El builder produce la permutación multiplicativa desde N y a; no recibe r ni factores. Tests bloquean la función que calcula r para la imitación y comprueban que el builder sigue funcionando.

**¿Es escalable?** No. La síntesis general por tabla es exponencial. La especialización para módulos 2^w−1 usa una identidad algebraica de rotación, no el período. Una implementación de Shor escalable necesitaría aritmética reversible diferente.

**¿Dónde está la ventaja cuántica?** No demostramos aceleración en un simulador. Mostramos estructura algorítmica, trazabilidad y trampas de evaluación.

**¿Por qué no cae a cero con azar?** Porque el postprocesamiento de números pequeños también puede acertar con fases aleatorias. Ese dato es parte del resultado.

**¿Ya existe un Q-Day Clock?** Sí. Hay coincidencia de nombre y concepto. Nuestro aporte es la auditoría interactiva del experimento. Para una empresa usaríamos otra marca tras verificarla.

## Hipótesis comercial

Empezar con formación técnica y talleres de evaluación para equipos de seguridad o consultoras que deban explicar PQC a clientes. Vendemos claridad de supuestos, no alarmismo. Un primer taller puede usar el producto actual; un producto empresarial de inventario criptográfico todavía no existe aquí.

Siguiente entrega a validar: inventario proporcionado por el cliente, plazos de confidencialidad, dependencias de migración y fuentes de cada supuesto. Un analista puede exportar qué decisiones cambian cuando cambia el horizonte. Trabajar con especialistas en criptografía para cualquier recomendación de implementación.

Criterio de éxito: el equipo toma una decisión de inventario, priorización o capacitación que puede justificar por escrito. Criterio de abandono: solo pide una fecha espectacular o cree que ya ofrecemos descubrimiento automático de criptografía. No inventar clientes, cifras de mercado, tasas de conversión ni ROI monetario.

Antecedentes que hay que reconocer: [Q-Day Clock](https://q-dayclock.com/), [Quantum Day Countdown](https://qdayclock.net/), [programa PQC de NIST](https://csrc.nist.gov/projects/post-quantum-cryptography). El espacio existe y tiene competidores. La defensa comercial debe venir de evidencia integrada en un flujo de trabajo, no del nombre.
