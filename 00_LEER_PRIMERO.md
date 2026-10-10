# LEER PRIMERO (sábado a la mañana)

## Qué hay

**Idea elegida: IMPOSTOR.** "¿Podés fingir ser una computadora cuántica?"

Vos sos el estafador y un árbitro escrito en Qiskit te desenmascara con un teorema. La tesis es: *una computadora cuántica no es una computadora más rápida, es lo que no se puede falsificar.* El razonamiento completo está en `research/02_IDEAS.md` y la spec en `research/04_IMPOSTOR_SPEC.md`.

**El proyecto ya funciona:** `impostor-qollab/` es un proyecto JS de Qollab listo para subir.
- **Nivel 01 Telepatía (CHSH):** el par cuántico gana 85,6%. El techo clásico es 75%, y el bot prueba las 16 estrategias posibles.
- **Nivel 02 Cuadrado mágico:** el cuántico gana 100%. El techo clásico es 8/9, y el bot prueba las 4.096 estrategias.
- **Nivel 03 Zip:** es el paper de Aaronson de 2025. 12 qubits sacan XEB 0,99; el impostor saca 0,32 aun mandando 6.144 bits.
- **Botón `/dev/urandom` (quantumslop):** cambia el lado cuántico por bits aleatorios y todo cae a ~50%.
- **"El único job":** un circuito empaquetado de 20 qubits que va al backend elegido. Entra en IonQ Aria (25 qubits) y Forte (29).
- **Sobrevive al ruido:** con 5% de error en compuertas de 2 qubits, CHSH da 0,825 y el cuadrado mágico 0,916. Los dos siguen por encima del techo clásico.
- **Tests:** los 14 del motor y el test de UI con navegador automático (Playwright) pasan, sin errores en la página. Las capturas están en `shots/`.
- **README:** ya escrito como página del proyecto (es la ficha que Qollab muestra al subir), siguiendo el playbook de ganadores.

## Lo que SOLO ustedes pueden hacer (en este orden)

1. **[Hackathonero, 30 min, CRÍTICO] Subir `impostor-qollab/` a Qollab** con la cuenta del capitán o de un miembro. Usar *Upload your files*: todo el contenido de la carpeta, con `index.html` y `main.js` en la raíz. Si se sube como proyecto nuevo, el README se convierte en la ficha.
2. **Presionar Run con el simulador local.** Ver que carga, jugar los 3 niveles y mirar la consola por errores. **Yo no pude probarlo en Qollab real**: lo probé en un entorno que imita su puente entre JS y Python. Lo que más riesgo tiene:
   - las llamadas `svc.fn.callPromising(...)` con argumentos;
   - leer `circuit.num_qubits` sobre el objeto que devuelve Python;
   - `backend.run(circuit, {shots})`.
   Todo sigue el patrón de su proyecto oficial "Soundtrack".
3. **Presionar Run en el IonQ Aria 1 simulator.** Tarda: usa 100 shots y el simulador es lento por shot. Confirmar que "The one job" muestra resultados. **Guardar esos números**: con ruido real de IonQ, CHSH debería quedar entre 75% y 85%. Pasármelos y los agrego a la ficha.
4. **[Estudiante de cuántica, 1 h] Revisar la física:** `impostor-qollab/impostor/games.py` y el README. Sobre todo, el decode del cuadrado mágico (transpuesta, signo de Y) y el resumen del paper de Zip.
5. **[Uriel] Mentor de IonQ:** el mensaje está en `research/03_MENSAJES_MENTORES.md`. Preguntar si se lee como honesto y novedoso.
6. **[Uriel] Video de 2:30:** el guion segundo a segundo está en `research/H_winning_playbook.md`, sección 3a. **Abrir con el fraude del 1 BTC, nunca con CHSH.** El orden es: cuadrado mágico, bot, quantumslop, Zip. Subirlo a **YouTube** (es el único sitio que se embebe en Qollab).
7. **Fijar un horario de freeze:** domingo 09:00. **Entregar el domingo a las 19:00 ART** (1 h de margen). Lo entrega el capitán.

## Ángulos nuevos para el pitch

- **Conexión con IA (de los chats de BAISH, `research/G_baish_signals.md`):** los evaluadores de IA detectan trampa con "tareas imposibles", pero esas tareas tenían bugs. IMPOSTOR ofrece **tareas imposibles con prueba matemática**. Frase posible: *"ImpossibleBench con prueba de imposibilidad."* También sirve como visión de startup: verificación que no se puede hackear.
- **Antecedente directo de IonQ:** Opti-Maze ganó la challenge de IonQ en iQuHACK 2022 jugando *contra* una computadora cuántica. Contraste para el pitch: *"ahí el humano podía ganar; acá un teorema dice que no podés."*
- **Competencia en Qollab:** nadie publicó CHSH, cuadrado mágico, supremacía de información ni sensado. Lo más parecido es *Bell's Bluff* (póker con cartas entrelazadas, que no es un test de Bell). Hay un equipo argentino con *Truco Cuántico*, probablemente del mismo nodo.

## Si sobra tiempo (en orden)

1. Nivel 04 Precisión (sensado GHZ). El código base ya está en `proto/impostor/referees.py`.
2. Grabar una corrida real del simulador IonQ en `data/` y agregar un selector "IonQ take".
3. Textos en español: Argentina tiene su iniciativa cuántica nacional desde 2026.

## Mapa de archivos

- `research/`: todo el análisis.
  - `00_BRIEF.md`: restricciones y criterios.
  - `A_` a `F_`: los informes de scanning.
  - `02_IDEAS.md`: las 7 ideas.
  - `04_IMPOSTOR_SPEC.md`: la spec del proyecto elegido.
  - `F_qollab_platform.md`: cómo funciona Qollab por dentro.
  - `G_baish_signals.md`: lo que salió de los chats de BAISH.
  - `H_winning_playbook.md`: cómo ganan y pitchean otros equipos.
- `impostor-qollab/`: **el proyecto que se sube.**
- `proto/`: los primeros experimentos.
- `shots/`: capturas de la UI.
