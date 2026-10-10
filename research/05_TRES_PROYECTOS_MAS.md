# Tres proyectos más (se pueden presentar hasta 5)

> Propuesta histórica de Claude. La implementación posterior corrige afirmaciones de exclusividad, navegación, predicción de Q-Day y número de encuestas. Consultar `06_BUILD_DECISIONS.md` y los README de cada proyecto para el alcance verificable; no usar este brief como ficha final.

Criterio de selección: cada uno en un **dominio**, un **tema del jurado**, un **tipo de ventaja cuántica** y una **estética** distintos de IMPOSTOR y entre sí. Todos tienen que pasar el test urandom: si reemplazás la parte cuántica por azar, el proyecto se rompe. Y todos son honestos sobre qué demuestra un simulador y qué no.

| | IMPOSTOR (ya hecho) | LOST SIGNAL | Q-DAY CLOCK | ORDER |
|---|---|---|---|---|
| Dominio | fundamentos / verificación | biología + navegación + defensa | criptografía + dinero | democracia + cognición humana |
| Tema Qollab | Playground | **Impact** | **Unlocked** | Playground / Most novel |
| Lo cuántico | correlación y memoria | **precisión** (sensado) | **algoritmos** (Shor) y costo real | **medición que no conmuta** |
| Cambio en el mundo | "lo cuántico no se puede falsificar" | "el sensado cuántico funciona HOY, cuando el GPS muere" | "cuándo se rompe toda la criptografía, contado honestamente" | "el orden de las preguntas cambia la verdad: encuestas, elecciones, IA" |

---

## 1. LOST SIGNAL: navegar cuando el GPS muere

**Señales que lo sostienen:**
- El GPS se interfiere y se falsifica a diario (Ucrania, Báltico, aviación civil).
- Los pájaros migratorios navegan con un **par radical**: dos spins de electrón en el criptocromo de la retina (paper JACS de noviembre 2025). Un campo de radiofrecuencia en MHz los desorienta, lo que se observó en todas las especies probadas.
- Los magnetómetros cuánticos (NV-diamante) ya se prueban para navegación sin GPS: DARPA, Mesa Quantum (USD 11,8M en septiembre 2026), Dirac Labs.
- IonQ compró Vector Atomic (posicionamiento y navegación, relojes). **Hay 0 proyectos de sensado** en Qollab y en GitHub de hackathons.

**Verdad contrariana:** la tecnología cuántica que cambia el mundo primero no es la computación, es el **sensado**. Y la naturaleza la usa hace millones de años.

**Experiencia:** un mapa del Atlántico Sur, con un vuelo de Buenos Aires hacia Ushuaia o las Malvinas. "GPS JAMMED". Tenés dos instrumentos cuánticos simulados en Qiskit:
1. **La brújula del pájaro.** Dos electrones más un núcleo (3 qubits) evolucionan bajo el campo terrestre real y el acople hiperfino. El rendimiento singlete según el ángulo es la aguja. Encendés un emisor de radiofrecuencia a la frecuencia de Larmor (~1,4 MHz) y la brújula se rompe, como en los pájaros reales.
2. **El sensor entrelazado (GHZ, N qubits)** contra N sensores independientes. La precisión escala 1/N (límite de Heisenberg) contra 1/√N. Con un slider de ruido se ve **el punto exacto donde el entrelazamiento deja de ayudar**: la curva honesta.

**Dato real:** el campo magnético terrestre sale del World Magnetic Model (NOAA, dominio público). La inclinación y la intensidad a lo largo de la ruta salen de ahí, precomputadas en un archivo de datos.

**Impact (exigencia del tema):** baseline clásico fuerte (brújula clásica: magnetómetro con ruido de disparo), métrica medible (error de heading y deriva de la ruta), dataset público (WMM).

---

## 2. Q-DAY CLOCK: ¿cuándo se rompe la criptografía? Contado honestamente

**Señales que lo sostienen:**
- En marzo–abril 2026, Google publicó un circuito de Shor más barato para romper firmas de curva elíptica (ECC-256), presentado como prueba de conocimiento cero de que el circuito existe. Caltech y Oratomic estimaron que bastan ~10–25k qubits físicos de átomos neutros.
- Ingenieros de criptografía (Valsorda, Cloudflare) hablan ahora de **2029**. En Bitcoin se discute congelar ~6,5–6,9M BTC vulnerables, entre ellos ~1M atribuidos a Satoshi (BIP-360/361).
- Gidney: factorizar **21** cuesta ~**115×** más que factorizar 15. La mayoría de los "récords" esconden la respuesta adentro del circuito.
- Con N chico, **adivinar al azar ya encuentra el factor** muy seguido. Es la lección de quantumslop.

**Verdad contrariana:** la pregunta importante no es "¿cuántos qubits hay?" sino **"¿cuántas compuertas honestas cuesta, y cuánto acierta el azar?"**.

**Experiencia:**
1. **"Factorizá N."** Para N = 15, 21, 33, 35, Qiskit arma dos circuitos: el **honesto** (exponenciación modular genérica) y el **"compilado"** (con el período metido adentro). Se ven explotar el contador de compuertas de dos qubits y la profundidad, y se corren en simulador con ruido.
2. **Botón de azar (urandom):** ¿cuánto acierta elegir `a` al azar y hacer un gcd, sin nada cuántico? Para N = 15, muchísimo.
3. **El reloj:** las estimaciones publicadas de recursos (Gidney–Ekerå 2019: 20M qubits → Gidney 2025: <1M para RSA-2048 → ECC-256 2026 → ~10–25k qubits de átomos neutros) contra las hojas de ruta de hardware. El reloj marca cuántos años faltan según cada supuesto. Y "tus secretos de hoy": guardar ahora y descifrar después.

**Unlocked:** algoritmos y tolerancia a fallos, el tema más candente de 2026, con números que se pueden reproducir.

---

## 3. ORDER: el orden de las preguntas cambia la verdad

**Señales que lo sostienen:**
- Wang, Solloway, Shiffrin y Busemeyer (PNAS 2014) analizaron **73 encuestas nacionales** (Pew/Gallup). Cambiar el orden de dos preguntas cambia las respuestas. Una predicción **sin parámetros libres** de la probabilidad cuántica (la **igualdad QQ**) se cumple en casi todas. Los modelos clásicos de Markov pueden producir efectos de orden, pero **no predicen la igualdad QQ**.
- Los LLM también muestran efectos de orden, y hay un movimiento de "silicon samples" que reemplaza encuestados humanos por IA.
- Rareza 4–5: fuera de la ciencia cognitiva casi nadie lo conoce. No encontramos ningún juego.

**Verdad contrariana:** las personas no tienen opiniones guardadas que una pregunta "lee". **La pregunta construye la respuesta**, y la matemática que mejor lo describe es la de la medición cuántica. No porque el cerebro sea cuántico: porque medir y preguntar tienen la misma estructura.

**Experiencia:**
1. **"Sos el encuestador."** Datos reales (por ejemplo, Clinton/Gore de Gallup 1997, más otros del paper): elegís el orden de las preguntas y el titular cambia.
2. **El circuito:** la creencia es un qubit y cada pregunta es una medición en otra base, que no conmuta con la anterior. La medición secuencial se implementa como **medición diferida** (CNOT a un qubit "registro"), sin medir a mitad del circuito. Los dos órdenes y varias preguntas entran en **un job**.
3. **El test que los separa:** se calcula la igualdad QQ sobre los datos reales. El modelo cuántico la predice; un modelo clásico de Markov ajustado a los mismos datos no.
4. **"Manipulá la elección":** con un presupuesto de preguntas previas, ¿cuánto podés mover la respuesta final?

**Honestidad:** decimos "matemática cuántica, personas clásicas". El circuito es cuántico de verdad: la incompatibilidad de las mediciones es esencial y el modelo clásico falla la igualdad QQ.

---

## Cómo se construyen

Cada uno es un proyecto JS de Qollab con la misma arquitectura que IMPOSTOR: Python con los circuitos y el puntaje, **un solo job empaquetado** para IonQ, tests, harness local con Playwright y README como ficha. Cada uno tiene **su propia identidad visual**:
- **LOST SIGNAL:** cartografía náutica, pantalla de radar.
- **Q-DAY CLOCK:** reloj del juicio final, dossier de inteligencia.
- **ORDER:** boleta electoral, tipografía de diario.
