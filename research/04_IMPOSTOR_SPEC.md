# IMPOSTOR: ¿podés fingir ser una computadora cuántica?

> **Spec del proyecto principal.** Sábado 10/10, madrugada. El núcleo cuántico ya está **construido y verificado en simulador** (ver `proto/`). Si leés solo una cosa, leé la sección 1.

---

## 1. En 30 segundos

En abril de 2026 alguien cobró **1 BTC** por "romper" una clave con una computadora cuántica de IBM. Otra persona reemplazó la computadora cuántica por números aleatorios (`/dev/urandom`) y **la clave salió igual**. Lo cuántico no estaba haciendo nada.

**IMPOSTOR es un juego donde vos sos ese estafador.** Te damos todos los recursos clásicos que quieras: estrategia, azar, memoria, hasta un bot que prueba miles de estrategias por fuerza bruta. Tu misión es hacerte pasar por una computadora cuántica. Un árbitro escrito en Qiskit te desenmascara siempre, y te muestra **el teorema** que dice por qué.

**La tesis (verdad contrariana):**
> Todo el mundo vende la cuántica como velocidad. Pero la velocidad es la ventaja que nadie puede verificar hoy, y en un simulador no existe. Las ventajas que sí se demuestran con un teorema son **correlación, memoria y precisión**. Una computadora cuántica no es "una computadora más rápida": es **algo que no se puede falsificar**.

---

## 2. La experiencia, con la estructura de un truco de magia (El gran truco)

| Acto | Qué pasa | Qué siente el jugador |
|---|---|---|
| **La promesa** | Un juego simple de cooperación: dos jugadores que no se pueden hablar responden preguntas. "Fácil, armamos una estrategia." | Confianza |
| **El giro** | El par cuántico gana más seguido que vos. Siempre. Probás otra estrategia y otra. El bot prueba **las 4.096 posibles**. Nada alcanza. | "¿Cómo lo hace?" |
| **El prestigio** | Botón **quantumslop**: cambiamos el backend cuántico por `/dev/urandom` y el récord se derrumba en vivo. Aparece el teorema: no es un truco de software, es un techo matemático. | Magia que **no se arruina al entenderla** (la pregunta abierta del ensayo de Uriel) |

---

## 3. Niveles (los 3 ya funcionan en simulador)

### Nivel 1: TELEPATÍA (juego CHSH)
- **Reglas:** el árbitro manda un bit x a Alice y un bit y a Bob. Ganan si `a XOR b == x AND y`. No pueden comunicarse.
- **Techo clásico: 75%.** Hay solo 16 estrategias deterministas y el bot las prueba todas. El azar compartido es una mezcla de esas 16, así que tampoco sirve.
- **Cuántico: cos²(π/8) ≈ 85,4%.** Medido en nuestro simulador: **85,6%**.
- **Circuito:** un par de Bell por ronda, 2 qubits. 10 rondas son 20 qubits en **un solo job**.

### Nivel 2: CUADRADO MÁGICO (Mermin–Peres)
- **Reglas:** grilla de 3×3. Alice recibe una fila y escribe 3 signos con producto +1. Bob recibe una columna y escribe 3 signos con producto −1. Ganan si coinciden en la casilla donde se cruzan.
- **Es imposible llenar la grilla clásicamente:** las filas exigen producto total +1 y las columnas −1. **Fuerza bruta propia: 4.096 estrategias, máximo 8/9 (144 empatan en ese techo).**
- **Cuántico: 100%.** Medido: **100,0%**. Con `/dev/urandom` cae a **51%**.
- **Circuito:** dos pares de Bell más mediciones de paridad de Pauli con ancillas. Son 8 qubits por ronda; 2 rondas entran en 16 qubits, un job.
- Es el nivel "wow": **la estrategia cuántica no falla nunca, y la clásica falla siempre en al menos una casilla.**

### Nivel 3: ZIP (supremacía de información, Kretschmer/Aaronson 2025)
- **Reglas:** Alice tiene que mandarle a Bob un "mensaje" que le permita pasar un test (XEB) sobre una medición aleatoria que Alice no conoce. El cuántico manda **12 qubits**. Vos mandás **bits**.
- **Teorema (arXiv:2509.07255):** para empatar el puntaje que logró el hardware (0,427), cualquier estrategia clásica necesita **≥78 bits**. La mejor conocida usa **~330**. El experimento original se hizo en iones atrapados: el mismo tipo de hardware que IonQ.
- **Nuestra medición:** el impostor ingenuo (sketch aleatorio) necesita **~3.000 bits para llegar a XEB 0,19** a n=12. Los 12 qubits ideales dan ~1,0. A n=8 el circuito cuántico simulado da 0,80 y `/dev/urandom` da 0,03.
- **Interacción:** un slider de "bits que le das al impostor" y una curva en vivo, más la línea del teorema y la línea cuántica.
- **Circuito:** brickwork aleatorio con borde periódico más un Clifford aleatorio. 12 qubits, un job.
- **Gancho IonQ:** la compuerta que "da la vuelta" (qubit 11 ↔ qubit 0) es nativa en conectividad all-to-all. En hardware tipo grilla cuesta SWAPs.

### (Opcional) Nivel 4: PRECISIÓN (sensado con GHZ)
- **Idea:** N sensores independientes tienen error ∝ 1/√N; N qubits en estado GHZ, ∝ 1/N (límite de Heisenberg). Con modelo de ruido se ve **dónde muere la ventaja**.
- **Gancho:** es la línea de negocio nueva de IonQ (Vector Atomic, sensado y relojes), y hay 0 proyectos en hackathons. Construir solo si los niveles 1 a 3 están pulidos.

---

## 4. El botón quantumslop (`/dev/urandom`)

En **cada nivel** hay un interruptor que reemplaza al backend cuántico por bits aleatorios. Le damos al juez el test con el que él mismo caza humo. Que el proyecto **pruebe su propia cuanticidad** no lo hace ningún otro proyecto encontrado.

| Nivel | Cuántico (medido) | Mejor clásico (teorema / fuerza bruta) | `/dev/urandom` (medido) |
|---|---|---|---|
| Telepatía | 85,6% | 75% | ~50% |
| Cuadrado mágico | 100% | 88,9% | 51% |
| Zip (n=8, XEB) | 0,80 | (necesita cientos o miles de bits) | 0,03 |

---

## 5. Cómo pega en cada criterio del jurado

| Criterio | Argumento |
|---|---|
| **Novedad y creatividad** | Cambio de significado (cuántica = no falsificable, no "rápida"). Invierte el rol: el jugador es el estafador. 0 repos con "quantum impostor", "quantum turing test" o "chsh game multiplayer". El nivel 3 es un resultado de 2025 sin port a Qiskit ni versión interactiva. |
| **Ejecución técnica** | Tres teoremas, cada uno con su verificación: simulación, fuerza bruta exhaustiva y ablación con `/dev/urandom`. Todo en un job IonQ por nivel. Qiskit 2.x. |
| **Potencial de impacto** | **Verificación de computación cuántica** (ver sección 6), un problema real y reciente: quantumslop, récords falsos de factorización, el tracker de ventaja cuántica de IBM. |
| **Documentación** | Por cada nivel, una tabla "concepto → circuito → número medido → teorema". Cita de papers. Sección "qué NO afirmamos". |

**Temas:** Playground (principal: "superposición, interferencia y entrelazamiento son esenciales, no azar". Acá son esenciales por teorema). También califica para Most novel.

---

## 6. Potencial grande (la historia de startup, para el pitch y para después)

- **El problema real:** la computación cuántica se vende como servicio en la nube. **¿Cómo sabe el cliente que recibió cómputo cuántico y no un simulador o ruido?** El caso quantumslop lo mostró con plata real de por medio. Los récords de factorización inflados y la polémica de Majorana muestran lo mismo.
- **La dirección:** auditoría de cuanticidad, con tests independientes del dispositivo, supremacía de información y pruebas de cuanticidad. **IMPOSTOR es la versión juego de una auditoría cuántica.**
- **Encaja con la estrategia de IonQ:** redes (dos trampas de iones conectadas son exactamente "dos jugadores que no se pueden hablar"), seguridad (QKD independiente del dispositivo se basa en CHSH) y sensado (nivel 4).

---

## 7. Qué NO afirmamos (honestidad = puntos con estos jueces)

- Que un simulador demuestre ventaja física. El simulador **calcula** las correlaciones; la ventaja es un **teorema** sobre jugadores separados o sobre la cantidad de bits. Lo decimos en pantalla.
- Que nuestro impostor del nivel 3 sea el mejor posible. El teorema acota **todas** las estrategias; la nuestra es una de muchas, y la mejor conocida (~330 bits) es del paper.
- Que CHSH o Mermin–Peres sean nuevos. Son de 1969 y 1990. Lo nuevo es el formato (impostor más ablación), el nivel 3 y la tesis que une los tres niveles.
- Que hayamos cerrado el loophole de independencia de configuración del paper. En el original, Bob elige su medición antes de que Alice prepare el estado; lo mencionamos.

---

## 8. Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| "CHSH otra vez" | Abrir el video con quantumslop y el cuadrado mágico (100% vs 8/9), no con CHSH. El nivel 3 es el diferencial técnico. |
| Qollab no soporta UI interactiva | Pendiente de verificar (agente investigando). Plan B: frontend estático afuera (permitido) con resultados precomputados más Run en vivo en Qollab. |
| Que el nivel 3 sea pesado en el simulador del navegador | n=8 y n=10 como modo rápido, n=12 como modo "paper". |
| Que haya muchos qubits por job | CHSH 20q, mágico 16q, zip 12q. Todo dentro de ~25. |

---

## 9. Reparto y horas (ART)

| Bloque | Estudiante de cuántica | Hackathonero | Perfil desconocido | Uriel |
|---|---|---|---|---|
| 09–12 | Revisar los circuitos de `proto/` y validar la física de los 3 niveles | Esqueleto Qollab y prueba del IonQ sim (1 job) | Leer la spec y armar el esqueleto de la página del proyecto | Mentor, narrativa, guion del video |
| 12–20 | Nivel 3 a n=12 (y nivel 4 si da el tiempo) | Frontend del juego (niveles 1 y 2) | Docs y tablas, accesibilidad | Diseño de la experiencia: promesa, giro y prestigio |
| 20–02 | Pulir y revisar números | Integración del nivel 3 | QA en Chrome y Edge | Copy, slides del video |
| Dom 09–16 | Revisión técnica final | Bugfix, congelar código | Docs finales | Grabar el video |
| Dom 16–19 | — | **Entrega con 1 h de margen** | — | — |

---

## 10. Guion del video (2:30)

1. **0:00–0:20.** "En abril alguien cobró 1 BTC por romper una clave con una computadora cuántica. Después la reemplazaron por números aleatorios. Funcionó igual." (Captura del hilo de HN.)
2. **0:20–0:40.** "¿Entonces cómo sabés que algo es cuántico? Hicimos un juego: vos sos el impostor."
3. **0:40–1:20.** Cuadrado mágico en vivo: el humano pierde una casilla, el bot prueba 4.096 estrategias y queda en 8/9, el par cuántico gana 100%.
4. **1:20–1:45.** Botón quantumslop: todo se derrumba.
5. **1:45–2:15.** Zip: "12 qubits contra miles de bits". La curva, el teorema y el link al paper.
6. **2:15–2:30.** La tesis: "las ventajas cuánticas que podés verificar hoy no son de velocidad". Cierre y créditos: *This effort is supported by Qollab & IonQ*.
