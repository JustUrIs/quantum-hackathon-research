# Ideas — Qollab × IonQ Hackathon

Síntesis de 5 frentes de scanning (A papers, B dolor de devs, C industria, D saturación, E social y otros dominios). Son ~80 fichas de señales en total. Sábado 10/10, ~01:30 ART. La entrega cierra el **domingo 11 a las 20:00 ART**.

> Límite honesto del scanning: X, Reddit y LinkedIn **no** se escanearon porque la extensión de Chrome no conectó. Lo social sale de Hacker News (API pública) y de blogs de insiders. Además, ninguna idea fue "testeada con personas": la evidencia de dolor real son quejas públicas medibles. La validación de verdad es la sección 5 (mentores y Slack).

---

## 1. Lo que vi cruzando las señales

### La señal que apareció en 4 frentes independientes

**"¿Cómo sabés que lo hizo la computadora cuántica?"**

- **Quantumslop (abril 2026, 383 pts en HN).** Project Eleven pagó **1 BTC** por "romper" una clave ECC de 17 bits en hardware de IBM. Alguien reemplazó la computadora cuántica por `/dev/urandom` y **la clave salió igual**: todo el trabajo lo hacía el filtro clásico. Gidney lo resumió así: *"succeed for the wrong reason"*.
- **Gidney, "¿Por qué no factorizaron 21?" (340 pts).** Factorizar 21 cuesta ~115× más que factorizar 15. La mayoría de los "récords" traen la respuesta escondida adentro del circuito.
- **Pregunta #1 de Quantum StackExchange:** *"Is quantum computing just pie in the sky?"* (44.5k vistas).
- **Aaronson criticó públicamente a IonQ** (dic 2025) por claims engañosos ante gobiernos. **Nuestros jueces son ingenieros de IonQ.**
- **Scholes (Quanta, 23 sep 2026, rareza 5).** Construyó redes clásicas de osciladores que **imitan la matemática de qubits**, y pregunta: *"¿Importa si no podés distinguir la diferencia?"*
- **Ola de "decuantización" 2025–26.** Ventajas cuánticas que se cayeron porque un algoritmo clásico alcanzó al cuántico: circuitos "peaked" simulados en 68 min en una GPU, DQI sin ventaja para MaxCut, QML imitable clásicamente.
- **Los editores de Qollab escriben su propio gusto:** *"honest rather than hyped"*, *"shows honestly which wins and why"*, *"not mapped randomness"*.

### La verdad contrariana que sale de cruzarlas

> **Todo el mundo vende la computación cuántica como velocidad. Pero la velocidad es justo la ventaja que hoy nadie puede verificar, y en un simulador directamente no existe. Las ventajas que SÍ se pueden demostrar hoy, con lápiz y papel, no son de velocidad: son de *correlación*, de *memoria* y de *precisión*.**

| Ventaja | Teorema | Tamaño | ¿Se puede mostrar honestamente en un simulador? |
|---|---|---|---|
| Correlación (juegos no-locales) | CHSH: 75% clásico vs 85.4% cuántico. Cuadrado mágico de Mermin–Peres: ≤8/9 clásico vs **100%** cuántico | 2–3 qubits | Sí. Es un techo matemático, no un tiempo de ejecución |
| Memoria (supremacía de información) | 12 qubits necesitan **62–382 bits clásicos** para imitarlos (Kretschmer/Aaronson 2025, incondicional) | 12 qubits | Sí. Se cuentan bits, no segundos |
| Precisión (metrología) | GHZ: error ∝ 1/N (límite de Heisenberg) vs 1/√N clásico | ≤12 qubits | Sí, con modelo de ruido y la curva donde la ventaja muere |

Esto es un **cambio de significado** (Verganti), no de tecnología. Una computadora cuántica deja de ser "una computadora más rápida" y pasa a ser **"algo que no se puede falsificar"**. Es justo el cambio que el mercado, los jueces y los foros están pidiendo sin decirlo.

### El cruce con IonQ

IonQ compró Vector Atomic (sensado y relojes), Lightsynq (redes), ID Quantique (seguridad) y Capella (espacio). **Sensado tiene 0 proyectos de hackathon** en GitHub y en Qollab. Las redes con repetidores y QKD ya están saturadas: la challenge de IonQ en iQuHACK 2026 fue de eso, y hay 2 competidores en vivo en esta misma hackathon.

---

## 2. Las ideas

Escala 1–10. "Cuántica esencial" significa que si reemplazás el backend por random o por algo clásico, el proyecto se rompe (lo llamo el "test urandom").

### ⭐ IDEA 1 — **IMPOSTOR** · "¿Podés fingir ser una computadora cuántica?"

**Qué es.** Un juego donde **vos sos el estafador**. Te dan recursos clásicos (azar compartido, k bits de memoria, una red de osciladores à la Scholes) y tenés que hacerte pasar por un dispositivo cuántico. Un **árbitro** corre pruebas en Qiskit y te desenmascara con un teorema.

- **Nivel 1, Telepatía:** dos jugadores que no pueden hablar juegan CHSH. El techo clásico es 75% y el par entrelazado llega a 85%. Ningún humano, ninguna estrategia y ningún bot superan el 75% a la larga, y el gráfico lo muestra en vivo.
- **Nivel 2, Cuadrado mágico:** el cuántico gana **100%** y vos como mucho 8/9. Un fallo garantizado, y se ve en qué casilla.
- **Nivel 3, Duelo de memoria:** tenés k bits para imitar 12 qubits. El marcador es XEB (el puntaje de Kretschmer/Aaronson). Ves cuántos bits necesitás y cómo explota.
- **Botón "quantumslop":** reemplaza el backend cuántico por `/dev/urandom` y vés en vivo cómo el resultado se cae. El proyecto **prueba su propia cuanticidad** en vez de pedirle al juez que confíe.

**Por qué gana.**
- **Novedad:** 0 repos en GitHub con "quantum impostor", "quantum turing test" o "chsh game multiplayer". Juegos no-locales con Qiskit: 2 repos, y son notebooks de libro.
- **Cuántica esencial por teorema:** es la forma más fuerte posible de cumplir la regla del tema Playground ("más que generar azar").
- **Encaje con los jueces:** les da la herramienta con la que ellos mismos cazan humo, con tono anti-hype. Conecta con la historia de redes de IonQ (dos trampas de iones conectadas = dos jugadores separados) sin repetir el combo repetidor+QKD.
- **Demo en 15 segundos:** "Tratá de ganarle a esta computadora sin entrelazamiento. No vas a poder, y acá está el teorema."
- **Es la tesis de Uriel hecha juego:** la magia de El gran truco, con el público intentando descubrir el truco y el truco siendo un teorema.

**Riesgos.**
- CHSH es conocido por cualquier estudiante de información cuántica. La novedad está en el marco (impostor + test urandom + Scholes) y en el nivel 3, no en el circuito.
- El nivel 3 (port del código de Kretschmer de pytket a Qiskit) es el más difícil: ~6–8 h de la estudiante de cuántica. **Es opcional** y el proyecto se sostiene sin él.
- Hay que confirmar si Qollab permite UI interactiva. Plan B: el frontend vive afuera (está permitido) y llama a los resultados del circuito.

**Tema:** Playground (principal), con eco en Unlocked. Apunta a **Most novel** y a Playground.

| Contrarian | Baja competencia | Cuántica esencial | Construible en 20 h | Demo | Encaje con IonQ | **Total** |
|---|---|---|---|---|---|---|
| 9 | 9 | 10 | 8 | 9 | 8 | **53/60** |

---

### IDEA 2 — **BRÚJULA** · "Navegar como un pájaro cuando se cae el GPS"

**Qué es.** Los pájaros migratorios navegan con un **par radical**: dos spins de electrón en la retina (paper JACS de nov 2025). El rendimiento singlete según el ángulo del campo magnético terrestre **es** la aguja. Lo simulamos en Qiskit con 3–5 qubits y lo comparamos con un sensor GHZ de N qubits entrelazados (escala de Heisenberg). La curva muestra **dónde el ruido mata la ventaja**.

- **Juego:** guiás un dron o un pájaro sobre un mapa con GPS "jameado" (Ucrania y el Báltico son noticia diaria). Un campo de radiofrecuencia de MHz rompe la brújula, que es justo lo que se observa en aves reales.
- **Señal contrariana:** el sensado cuántico es útil HOY y la computación cuántica todavía no (pilotos de magnetómetros NV-diamante para navegación sin GPS, DARPA).

**Por qué gana.** Cero prior art: "radical pair compass qiskit" da 0, "GHZ metrology" da 0, "quantum sensing game" da 0. Es la nueva línea de negocio de IonQ (Vector Atomic). Tiene una curva medible y honesta de 1/N vs 1/√N con ruido. Y la historia emociona: biología + guerra + espacio.

**Riesgos.** El Hamiltoniano del par radical con Trotter más el ruido requiere física real: es trabajo de la estudiante. El encuadre "Impact" es débil porque no hay dataset público real. Se podría usar gpsjam.org, pero el CORS no está verificado.

**Tema:** Unlocked o Playground. Apunta a **Most novel**.

| Contrarian | Baja competencia | Cuántica esencial | Construible | Demo | Encaje con IonQ | **Total** |
|---|---|---|---|---|---|---|
| 8 | 10 | 9 | 6 | 8 | 9 | **50/60** |

---

### IDEA 3 — **DECODER** · "Sos el decodificador" (corrección de errores para ICPCers)

**Qué es.** Un código de distancia 3 (repetición, después superficie) corre como **circuito real de síndrome** en Qiskit, todo empaquetado en 1 job. Ves solo el síndrome, nunca el estado, y tenés que adivinar el error antes de que el ruido acumule demasiado. Competís contra MWPM y Union-Find. Es la idea "aprender sin mirar", que une los 3 conceptos más difíciles según la evidencia (medición, ruido y QEC).

**Por qué.** Corrección de errores es el tema #1 nombrado en Unlocked. En QCSE tiene 1,253 preguntas, 17% sin respuesta. El 41% de los profesionales dice que la falta de formación es la barrera principal (Riverlane 2025). "qec decoder game" da 0 repos. Decodificar es matching en grafos: **el terreno de Uriel en ICPC**.

**Riesgo.** Es la idea "por defecto" de Unlocked: va a haber varios explicadores de repetition code. La mecánica tiene que ser claramente distinta.

**Tema:** Unlocked.

| Contrarian | Baja competencia | Cuántica esencial | Construible | Demo | Encaje con IonQ | **Total** |
|---|---|---|---|---|---|---|
| 5 | 6 | 9 | 8 | 7 | 7 | **42/60** |

---

### IDEA 4 — **PARETO DE UN DISPARO** (Impact honesto)

**Qué es.** Configuración de red eléctrica real (IEEE 33-bus, MATPOWER `case33bw`) o una red de agua (EPANET). Un QAOA multi-objetivo genera **en un solo job** un *conjunto diverso* de soluciones casi-óptimas: un frente de Pareto entre pérdidas, voltaje y costo. Se compara contra NSGA-II, MILP y fuerza bruta exacta. Que la instancia sea chica es una **ventaja**: se conoce el óptimo exacto y la cobertura exacta.

**Contrarian.** El valor de la cuántica no es "la mejor solución", que siempre gana Gurobi a este tamaño, sino **la diversidad por disparo**. Hay respaldo publicado: IBM/ZIB/LANL (arXiv 2503.22797) y Google (time-to-diversity). El proyecto incluye su propio "auditor de ventaja" que dice dónde gana lo clásico.

**Riesgo.** Impact está saturado (energía y logística ya tienen competidores en vivo). Lo más probable es que la conclusión sea "lo clásico gana": eso es aceptable para estos editores, pero menos distintivo.

**Tema:** Impact.

| Contrarian | Baja competencia | Cuántica esencial | Construible | Demo | Encaje con IonQ | **Total** |
|---|---|---|---|---|---|---|
| 7 | 5 | 6 | 7 | 5 | 7 | **37/60** |

---

### IDEA 5 — **INTERROGATORIO** · "El orden de las preguntas cambia la verdad"

**Qué es.** Wang & Busemeyer (PNAS 2014) analizaron 73 encuestas de Pew y Gallup: el orden de las preguntas cambia las respuestas, y una predicción de probabilidad cuántica **sin parámetros** (la igualdad QQ) se cumple en casi todas. El juego es de detective: el sospechoso es un estado y cada pregunta es una medición en otra base que no conmuta. **El orden en que interrogás define qué termina siendo verdad.** Todo el cuestionario entra en 1 job.

**Por qué.** Rareza 4–5, ningún juego así encontrado. Conecta con encuestas, elecciones y la cultura argentina. Tiene un ángulo de diseño fuerte.

**Riesgo.** Un juez puede decir *"eso es álgebra lineal, no hace falta una computadora cuántica"*. Hay que encuadrarlo como "matemática cuántica, personas clásicas" y ser honesto. Además, ya hay un competidor (*Collapse*, detective con elección de base de medición) que toma una mecánica parecida.

**Tema:** Playground.

| Contrarian | Baja competencia | Cuántica esencial | Construible | Demo | Encaje con IonQ | **Total** |
|---|---|---|---|---|---|---|
| 8 | 6 | 5 | 9 | 8 | 4 | **40/60** |

---

### IDEA 6 — **HYPE-O-METER** · "¿Por qué no factorizaron 21?"

**Qué es.** Compilás Shor **honesto** y Shor **"con trampa"** (la respuesta embebida) para N = 15, 21, 35… y ves explotar el contador de compuertas, la profundidad y la fidelidad bajo ruido. Se suma el test urandom sobre un ECDLP de juguete: *¿la señal le gana al azar?* Y el reloj de Q-Day: las estimaciones de recursos pasaron de Gidney 2025 a Oratomic 2026, con 2029 según Cloudflare y Google.

**Por qué.** Es el debate cuántico más votado en HN en 2025–26 (migración post-cuántica, Bitcoin y las monedas de Satoshi). No hay versión interactiva.

**Riesgo.** Shor honesto para 21 requiere ~2,400 compuertas de entrelazamiento: se puede **compilar y contar**, pero no simular con ruido de forma fiel.

**Tema:** Unlocked.

| Contrarian | Baja competencia | Cuántica esencial | Construible | Demo | Encaje con IonQ | **Total** |
|---|---|---|---|---|---|---|
| 7 | 7 | 7 | 7 | 7 | 5 | **40/60** |

---

### IDEA 7 (el sueño de Uriel) — **MEMOIZACIÓN SIN COPIAR**

**Qué es.** Quantum Dynamic Programming (PRL, mayo 2025). Como no se puede copiar un estado cuántico (no-cloning), la "memoria" de una recursión se **consume**. Se reduce la profundidad exponencialmente a cambio de muchas copias.

**Veredicto honesto.** La historia es preciosa para un ICPCer ("DP cuando no podés copiar la tabla"). Pero con ≤25 qubits solo entran 1–2 niveles de recursión, el único código está en Qibo y no hay ninguna demo en hardware. **No es para este fin de semana.** Es para después: post-hackathon, mentoría de IonQ, una posible tesis.

| Contrarian | Baja competencia | Cuántica esencial | Construible | Demo | Encaje con IonQ | **Total** |
|---|---|---|---|---|---|---|
| 9 | 10 | 10 | 3 | 4 | 5 | **41/60** |

---

## 3. Descartadas por evidencia (no gastar tiempo)

- **Música, Bloch, visualizadores, tic-tac-toe, QRNG, portfolio, VRP, VQE de moléculas, teleportación, BB84:** saturado. Además el reglamento tiene un **piso de novedad**: un proyecto nivel tutorial puede sacar 0 en novedad y en ejecución técnica.
- **Repetidor + purificación + QKD:** es la idea por defecto para "agradarle a IonQ". Hay 2 competidores en vivo y fue la challenge de iQuHACK 2026.
- **QML de cualquier tipo:** el consenso 2025–26 es que se puede imitar clásicamente.
- **Aleatoriedad certificada en simulador:** pseudo-cuántica por construcción.
- **Nobel 2025 como tema:** la parte cuántica quedaría decorativa.
- **"IA que descubre algoritmos cuánticos"** (la idea de la conversación anterior): AlphaTensor-Quantum y AlphaEvolve ya existen, y en 20 h quedaría como un AlphaEvolve simplificado sin contribución propia.

---

## 4. Recomendación

**Proyecto principal: IMPOSTOR.** Es la única idea que junta las tres cosas a la vez: la señal convergente más fuerte (verificabilidad), una ventaja cuántica **demostrable por teorema** a escala chica, y un cambio de significado que es la tesis de Uriel (magia, El gran truco). Además es la que mejor resiste al juez escéptico, porque el escepticismo **es** el juego.

**Segundo proyecto, si sobra gente: BRÚJULA.** No comparte código con IMPOSTOR, pero sí la tesis ("las ventajas verificables no son de velocidad: precisión"). Tiene la categoría más vacía y es la apuesta nueva de IonQ. Si sale, juntas son una narrativa de equipo: **"Correlación, memoria, precisión: las tres ventajas cuánticas que podés verificar hoy."**

**Reparto sugerido para IMPOSTOR:**
| Quién | Qué |
|---|---|
| Estudiante de cuántica | Circuitos de los árbitros (CHSH, cuadrado mágico, GHZ) empaquetados en 1 job IonQ. Después, nivel 3 (port de Kretschmer) si da el tiempo |
| Hackathonero | Frontend del juego, integración con Qollab, test urandom |
| Perfil desconocido | Docs y página de proyecto (el premio Best documentation es aparte), accesibilidad, QA |
| Uriel | Narrativa, diseño de la experiencia, guion y video, mentores. Si quiere tocar código: el bot impostor clásico (busca la mejor estrategia clásica, es terreno ICPC) |

**Hitos (hora ART):**
- **Sábado 10:00:** idea confirmada y validada con un mentor.
- **Sábado 14:00:** CHSH con impostor humano corriendo en Qollab y en el simulador IonQ (1 job).
- **Sábado 22:00:** niveles 1 y 2 más el botón urandom completos.
- **Domingo 12:00:** nivel 3 o pulido, docs.
- **Domingo 16:00:** código congelado, se graba el video.
- **Domingo 19:00:** entregado con 1 h de margen.

---

## 5. Validación (lo que yo no puedo hacer, y es lo más valioso)

Hacerlo **antes de las 10:00**. Hay borradores en `03_MENSAJES_MENTORES.md`.

1. **Mentor de IonQ (técnico):** ¿la ventaja por teorema en simulador se lee como honesta o como "ya lo vimos"?
2. **Slack del nodo:** ¿alguien está haciendo juegos no-locales o sensado? Es un chequeo de competencia en vivo.
3. **3 personas sin formación cuántica, 5 minutos cada una:** les mostrás el pitch de 15 segundos de IMPOSTOR y de BRÚJULA y les preguntás *"¿qué entendiste? ¿lo querrías jugar?"*. Mirá la cara, no la respuesta.
4. **La estudiante de cuántica:** es el veto técnico de cualquier idea, en 10 minutos.

## 6. Cosas sin verificar que pueden cambiar la decisión

- Si Qollab soporta UI interactiva dentro del Run o si el frontend tiene que vivir afuera.
- Si el simulador IonQ soporta medición a mitad de circuito (no hace falta para IMPOSTOR ni para BRÚJULA).
- El texto exacto del reglamento: el "piso de novedad" se leyó de segunda mano, en notas de otro equipo.
- El repo de quantumslop (devolvió 503). La historia se apoya en resúmenes secundarios más el hilo de HN.
