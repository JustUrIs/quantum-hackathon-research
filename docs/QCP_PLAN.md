# QCP: plan de producto y desarrollo

Estado: alcance confirmado por el usuario; implementación de la demo en curso.
Fecha: 2026-10-11.

## Alcance confirmado

Demo para la hackathon, inglés, individual, presupuesto cero. Usuarios iniciales:
estudiantes de Python/Qiskit; luego programadores sin experiencia cuántica.
Prioridad: juez > catálogo de máximo tres problemas > una ronda virtual.
Sin login, funciones sociales ni base de datos. Supabase no es necesario ahora.

Catálogo definitivo: Bernstein–Vazirani (recuperación exacta), Deutsch–Jozsa
(decisión exacta bajo promesa, con comparación clásica aleatoria explícita) y
Grover (búsqueda con alta probabilidad). Los seis ejercicios del borrador inferior
son alternativas descartadas, no entregables pendientes.

Ejecución: Qollab usa Qiskit Statevector. La web pública usa un constructor Python
acotado en Pyodide y un simulador ideal JavaScript independiente, identificado.
La clasificación es una ronda local de 60 minutos con penalizaciones, no un juez
global confiable. La web puede publicarse en Vercel sin servicios pagos.

La documentación vigente de la implementación está en `qcp-qollab/README.md`.

## Producto

Una plataforma de programación competitiva cuántica: leer un problema, escribir
una solución general en Python/Qiskit, probar ejemplos, enviar, recibir un
veredicto y estudiar el editorial. La captura de Codeforces es una referencia
de estructura y legibilidad; no se reutilizan su marca ni sus enunciados.

Nombre provisional: QCP Arena. El nombre no bloquea el desarrollo.

La diferenciación propuesta es el puente desde programación competitiva clásica:
enunciados orientados a tareas, explicación del modelo de entrada, juez
reproducible, comparación de recursos con supuestos explícitos y progresión hacia
rondas universitarias. La hipótesis de adopción se validará con usuarios; no se
afirma que no existan competidores.

## Decisiones del borrador, ya resueltas arriba

1. Primera entrega: hackathon, beta pública o ambas en dos etapas.
2. Público inicial: competidores clásicos, usuarios de Qiskit o dos rutas.
3. Prioridad: resolución/veredictos, rondas/equipos o aprendizaje guiado.
4. Clasificación: práctica local o competencia global con juez confiable.
5. Idiomas y equipos: propuesta EN/ES; individual primero, equipos después.
6. Infraestructura disponible y presupuesto: GitHub, Vercel, servidor y datos.

## Correcciones al documento de ideas

- QCoder ya tiene concursos, Qiskit, simulación y veredictos. La oportunidad no
  consiste en afirmar que nadie construyó un juez cuántico.
- Grover necesita O(sqrt(M)) consultas para buscar un elemento entre M candidatos
  en el modelo de búsqueda sin estructura; no una consulta general.
- Bernstein–Vazirani permite recuperar una cadena con una consulta a un oráculo
  de paridad específico. No utiliza el oráculo de igualdad de Grover.
- Ejecutar una simulación clásica no demuestra aceleración cuántica práctica.
- Una lista explícita de entrada tiene costos de lectura/carga. No se supone
  acceso cuántico gratuito a esos datos ni a QRAM.
- Un simulador de tensores no elimina el costo exponencial de cualquier circuito.
- Profundidad, puertas y qubits son métricas de un circuito concreto; no prueban
  por sí solas la complejidad asintótica de un algoritmo.
- Un análisis del DAG no demuestra automáticamente corrección ni ausencia de
  clonación. Compilation Error significa un error de compilación, no un detector
  genérico de leyes físicas.
- Los tests distribuidos al navegador no son secretos. Un resultado local no
  puede respaldar una clasificación global resistente a manipulación.

## Experiencia de usuario

1. Abrir un problema sin instalar nada ni crear una cuenta para leerlo.
2. Leer historia breve, tarea, entradas, resultado, límites y ejemplos.
3. Encontrar explícitamente el tipo de tarea: transformación, consulta a un
   oráculo o optimización de recursos.
4. Editar una función Python/Qiskit con firma y registros definidos.
5. Run ejecuta ejemplos; Submit ejecuta la batería de evaluación disponible.
6. Ver AC/WA/error y métricas, con el alcance del veredicto identificado.
7. En práctica, abrir explicación y un contraejemplo pedagógico cuando corresponda.
8. Descargar la solución para usarla en VS Code y continuar con el mismo juez.

Interfaz: catálogo con filtros; página de problema; editor; resultados de envíos;
handbook; ronda y standings cuando el alcance seleccionado lo permita. En la
página del problema predomina el texto legible, como en la captura. El circuito y
las probabilidades son herramientas opcionales, no reemplazos del enunciado.

Guardar borradores y progreso local. Una clasificación local se identifica como
local. No inventar competidores, historial de concursos ni ratings.

## Contratos de problemas

Cada problema incluye identificador/versionado, idiomas, enunciado, ejemplos,
firma de solve, interpretación de bits y registros, gates permitidas, ancillas,
limites, tolerancia, checker, generador de casos, editorial y referencias.

Tres contratos distintos:

- Transformación: construir un circuito que actúa correctamente sobre las
  entradas definidas, incluso cuando el enunciado exige coherencia.
- Consulta: el juez proporciona un oráculo simbólico. La solución trabaja con
  ese acceso y el juez evalúa el resultado y cuenta consultas.
- Optimización: conservar la tarea anterior y reducir recursos medidos bajo una
  base de puertas, conectividad y configuración de compilación publicadas.

El oráculo no revela el secreto a la solución mediante parámetros, nombres o
descomposición. La implementación del juez se inserta después de construir la
solución. En práctica local esto es una regla del modelo, no una garantía de
secreto frente a un usuario que controla su navegador. El juez de concurso debe
separar el proceso del participante y el evaluador que contiene los secretos.

Los ejemplos pueden mostrar entradas/salidas clásicas. Si la tarea es interactiva
o recibe un oráculo, se declara; no se disfraza como stdin/stdout convencional.

## Catálogo inicial propuesto

| Problema | Tarea | Evaluación principal |
| --- | --- | --- |
| Paquetes sellados | Aplicar XOR con una máscara conocida, coherentemente | Transformación correcta, orden de bits, recursos |
| Alarma de paridad | Escribir la paridad de un registro en un bit de salida sin borrar el registro | Todos los casos pequeños, superposiciones, ancillas |
| Suma circular | Construir una suma modular con una constante | Bordes, acarreo, coherencia, limpieza de ancillas |
| Mensajes enlazados | Preparar estados de Bell solicitados por dos bits de entrada | Estado conjunto y fase relativa |
| Contraseña de paridad | Recuperar la cadena del oráculo Bernstein–Vazirani | Secreto variable, probabilidad correcta, consultas |
| La ficha marcada | Buscar el elemento marcado de un oráculo de igualdad con Grover | Probabilidad de éxito y presupuesto de consultas |

Extensiones, después del núcleo: fase/frecuencia escondida, transformación de
Fourier y optimización sobre conectividad limitada. No anunciar un catálogo de
50 problemas sin checkers y editoriales revisados.

Ronda inicial propuesta: cuatro problemas que mezclen tareas reversibles y
consultas. La duración y penalización se fijan antes de comenzar. La corrección
determina Accepted; la eficiencia adicional se publica como métrica separada.
Así se puede conservar una clasificación familiar a ICPC sin un score opaco.

## Juez

Primera versión: circuitos pequeños, idealmente hasta 8–10 qubits, con límites
concretos por problema. Preferir evaluación ideal determinista para que shots
aleatorios no cambien injustamente el veredicto.

Evaluación:

1. Construcción y validación estructural del circuito.
2. Comprobación de ancho, instrucciones y límites de recursos.
3. Checker semántico específico de la tarea.
4. Informe de resultado, versión del problema y versión del evaluador.

Para estados se ignora la fase global, pero no fases relativas. Para
transformaciones pequeñas puede verificarse el operador/isometría completo.
Probar solamente entradas de la base y comparar sus probabilidades no alcanza
para certificar una transformación coherente: se incluyen entradas de
superposición sensibles a fases. Los tests muestreados se identifican como tales;
no se presentan como prueba formal universal.

Si se permiten ancillas deben terminar limpias cuando lo exige el contrato. Las
probabilidades se comparan con umbrales publicados; el modo de shots muestra
incertidumbre y queda separado del checker ideal.

Métricas separadas: consultas al oráculo, qubits/ancillas, profundidad y puertas de
dos qubits bajo compilación fijada, costo del oráculo descompuesto y tiempo de
simulación. No vender el tiempo de CPU como tiempo de QPU.

Veredictos iniciales: AC, WA, CE, RE, TLE, QLE, DLE e instrucción no permitida.
100 casos no es una meta aislada: cada batería debe distinguir soluciones
incorrectas concretas, incluyendo errores de fase y soluciones hardcodeadas.

## Arquitectura y ejecución

Núcleo Python: modelos de problemas, generadores, checker y métricas Qiskit.
Dos superficies consumen el mismo núcleo:

- Qollab: catálogo pequeño, edición de soluciones y evaluación end-to-end con
  Qiskit y simuladores gratuitos. No requiere API externa ni credenciales.
- Vercel: interfaz pública. La ejecución local de Python/Qiskit en un worker del
  navegador depende de una prueba temprana de Pyodide y wheels compatibles.
  Vercel aloja la web; no es una QPU ni resuelve por sí solo la ejecución de Qiskit.

Si esa ejecución en navegador no es viable, mostrar el problema y ofrecer una
ruta explícita a Qollab/CLI. No mostrar un simulador JavaScript como si ejecutara
el Python del participante. El alcance elegido determinará si hace falta un
servidor Python público para la primera entrega.

CLI inicial: ejecutar ejemplos y evaluar localmente una solución descargada.
Submit remoto aparece solo cuando existe una API real de concurso.

Para concurso global: API de envíos, cola, ejecutores aislados con límites de
CPU/memoria/tiempo y sin red, base de datos y autenticación. El proceso que ejecuta
Python no recibe secretos del checker. Los resultados y el reloj del concurso
se calculan en servidor. Una allowlist de imports o exec con pocos builtins no
se presenta como sandbox seguro para código Python hostil.

No ejecutar Python arbitrario de visitantes dentro de la función web de Vercel.
En práctica de navegador, usar un worker cancelable y considerar el aislamiento
del origen que recibe código. La solución concreta requiere una prueba de
viabilidad, no solo un diagrama.

## Handbook

Una ruta corta: bits y registros; amplitudes/fases; interferencia; reversibilidad
y ancillas; entrelazamiento; modelos de oráculos; BV; Grover; métricas y costos.
Cada capítulo contiene una tarea, un template, una explicación y un ejercicio.
No promete transformar cualquier programa clásico en uno cuántico mejor.

## Orden de desarrollo y criterios de salida

1. Viabilidad: una solución correcta y una incorrecta reciben veredictos distintos
   en Qollab; comprobar cómo correr la misma solución desde la web pública.
2. Juez: probar los checkers contra implementaciones con fallos intencionales y
   casos independientes. Fijar contratos, límites y dependencias.
3. Producto: catálogo, enunciado, editor, Run/Submit, resultados y guardado.
4. Contenido: seis problemas originales, editoriales, templates y handbook corto.
5. Competencia: ronda local o juez global según las respuestas pendientes.
6. Entrega: revisión móvil, accesibilidad, MIT, README inglés, ZIP Qollab,
   configuración Vercel y demo pública de 2–3 minutos.

La prueba de producto debe permitir a una persona leer, editar, equivocarse,
entender el error y conseguir Accepted. Verificar que funciona en Qollab, no solo
en Python local. Los envíos deben sobrevivir a recarga donde el modo lo promete.
Un timeout no debe dejar la página bloqueada ni alterar los siguientes envíos.

La demo muestra una solución fallida, una aceptada y una mejora de recursos con
el mismo comportamiento. Cada ejecución identifica su origen. Publicación y
video no se declaran terminados antes de que sus enlaces sean accesibles.

## Después de la primera entrega

Piloto con un club de programación y un curso universitario: medir cuánto tarda
un principiante en obtener su primer Accepted, retorno a otra sesión y problemas
terminados. Clubes/equipos y rondas periódicas necesitan organizadores y writers,
además del software.

Primeras hipótesis comerciales: juez y contenido para cursos; herramientas para
organizar concursos de universidades/laboratorios; retos patrocinados. Un rating
solo adquiere valor de reclutamiento después de evaluar habilidades relevantes,
tener población suficiente y controlar el proceso competitivo.

## Fuentes consultadas

- QCoder Q&A: https://www.qcoder.jp/en/qa
- Ejemplo QCoder: https://www.qcoder.jp/ja/contests/QPC004/problems/B2
- Quantum Lings: https://quantumlings.com/
- IBM, quantum query algorithms: https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/quantum-query-algorithms
- IBM, Grover y modelo de oráculos: https://quantum.cloud.ibm.com/learning/en/modules/computer-science/grovers
