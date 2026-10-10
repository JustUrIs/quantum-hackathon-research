# Borradores de mensajes (en inglés para los mentores de IonQ; el de Slack del nodo, en el idioma del canal)

## 1. Mentor IonQ — validación de IMPOSTOR (prioridad)

> Hi! We're [team], building for the Playground track. Quick sanity check before we commit:
>
> Idea: "IMPOSTOR" — a game where the player tries to *fake* being a quantum device using classical resources (shared randomness, k bits of memory), and Qiskit referees unmask them with theorem-level bounds: CHSH (75% vs ~85%), Mermin–Peres magic square (8/9 vs 1), and, stretch goal, the 12-qubit information-supremacy test from Kretschmer/Aaronson 2025 (k classical bits vs 12 qubits). Plus a "/dev/urandom" toggle that swaps the quantum backend for randomness so you watch the result collapse (inspired by the quantumslop episode).
>
> Thesis: the quantum advantages you can verify today aren't speed — they're correlation, memory and precision.
>
> Two questions:
> 1. Would an IonQ engineer read this as honest and novel, or as "seen it, CHSH again"?
> 2. Is porting the information-supremacy experiment to Qiskit (12 qubits, one circuit) something you'd find technically credible / interesting?
>
> Thanks!

## 2. Mentor IonQ — validación de BRÚJULA

> We're also considering a second entry: simulate the avian radical-pair compass (2 electron spins + nuclear spin, 3–5 qubits) in Qiskit and contrast it with a GHZ sensor showing Heisenberg vs shot-noise scaling, with a noise model that shows where entanglement stops helping — framed as GPS-denied navigation. Does a sensing project fit what IonQ cares about (given Vector Atomic), and is there a pitfall we should know about simulating the radical-pair Hamiltonian?

## 3. Slack del nodo — chequeo de competencia en vivo

> ¿Alguien está trabajando en juegos no-locales (CHSH / magic square) o en sensado cuántico? No queremos pisarnos — si hay overlap, coordinemos.

(Opcional: no mandarlo si preferimos no revelar la idea. Trade-off: info de competencia vs. exponer la idea. Recomiendo NO mandarlo; usar en cambio la búsqueda en GitHub de repos con tag/keyword "qollab".)

## 4. Test con 3 personas sin formación cuántica (en persona / WhatsApp audio)

Pitch de 15 s, IMPOSTOR:
> "Hay una computadora cuántica. Vos tenés que hacerte pasar por ella sin serlo. Podés usar lo que quieras: estrategia, azar, memoria. Un árbitro te va a desenmascarar siempre — y te muestra el teorema que dice por qué. ¿Lo jugarías?"

Pitch de 15 s, BRÚJULA:
> "Los pájaros navegan con un efecto cuántico dentro del ojo. Cuando se cae el GPS, los drones militares quedan ciegos. Simulamos la brújula del pájaro en una computadora cuántica y te dejamos volar con ella."

Preguntas: ¿qué entendiste? (en sus palabras) · ¿qué te dio curiosidad? · del 1 al 10, ¿lo abrirías?
