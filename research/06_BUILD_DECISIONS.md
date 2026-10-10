# Continuidad y decisiones de construcción

Fecha: 10 de octubre de 2026. Continuación del trabajo iniciado con Claude.

## Contexto reconstruido

Uriel quiere experiencias que produzcan asombro al entender una tecnología, problemas reales y una dirección comercial que sobreviva al hackathon. El criterio científico importa: simulación, azar y ventaja física deben distinguirse. La referencia conceptual viene de su trabajo de diseño, Argos, How to Future y su interés en algoritmos/ICPC. No se publican las conversaciones personales ni el ensayo privado.

IMPOSTOR ya tiene implementación, pruebas y capturas. Las otras tres ideas existían solamente en `05_TRES_PROYECTOS_MAS.md`; no hay resultados de los agentes anteriores en este checkout. Se conserva IMPOSTOR y se crean tres carpetas autocontenidas, con la misma interfaz JS/Python de Qollab.

## Correcciones que cambian el producto

- LOST SIGNAL compara sensores independientes con GHZ con el mismo número de interacciones y repeticiones, a tiempo de interrogación fijo. La decoherencia puede eliminar la mejora; optimizar el tiempo en ruido markoviano cambia la comparación (Huelga et al., 1997). WMM describe el campo terrestre a gran escala, no un mapa suficiente para geolocalizar un avión. El mapa ilustra incertidumbre angular, no navegación validada. El modelo de par radical es un modelo didáctico separado, no un magnetómetro NV ni una réplica biológica.
- Q-DAY CLOCK no predice una fecha de ruptura. Compara experimentos pequeños con recursos publicados y permite elegir un horizonte hipotético. La construcción modular no recibe los factores ni el período. Su síntesis por permutaciones es exponencial, apta para números pequeños, y no debe extrapolarse a RSA. Se compara con azar y división clásica.
- ORDER no prueba cerebros cuánticos ni exclusividad cuántica de QQ. Un modelo clásico contextual puede reproducir las distribuciones y también cumplir QQ. Se incluye ese competidor. Wang et al. (2014) estudian 70 encuestas nacionales y dos experimentos, no 73 encuestas. El ejemplo Rose/Jackson muestra una violación bajo información intercalada. Se conservan proporciones publicadas y su precisión original.
- La fecha 19:00 ET del 11 de octubre corresponde a 20:00 ART; 19:00 ART es un objetivo interno con una hora de margen, no el cierre oficial. Verificar en la página del evento antes de entregar.

## Diseño antes de implementar

| Proyecto | Paleta | Tipografía local | Composición y gesto memorable |
|---|---|---|---|
| LOST SIGNAL | océano #071F32, instrumento #0D3249, hielo #E6F4F3, sonar #64D8CD, ámbar #FFCA70 | Bahnschrift / sans; Consolas para lectura instrumental | mapa amplio a izquierda, controles a derecha; apagar GPS y observar cómo se abre el corredor de incertidumbre |
| Q-DAY CLOCK | papel técnico #ECEEF3, tinta #192137, ultravioleta #5841BA, alerta #B9314F, blanco #FFFFFF | Georgia para el reloj, Segoe UI para el dossier | reloj circular y presupuesto de migración; debajo, banco de pruebas de factorización con procedencia de cada resultado |
| ORDER | papeleta #FFFFFF, tinta #202F65, cobalto #254CC8, frambuesa #B72E62, papel #EBF0FF | Georgia para titulares; Trebuchet MS para controles | dos papeletas grandes e intercambio de orden; titular cambiante, tabla empírica y contraejemplo clásico |

Se evita copiar el aspecto de IMPOSTOR. Sin dependencia de fuentes remotas, sin servicios pagos, sin claves en los proyectos. Contraste, teclado, tamaños móviles y movimiento reducido se verifican en navegador.

## Entregables

Motores Qiskit, interfaces, datos con procedencia, tests físicos y de interacción, servidor local compartido, exportaciones JSON y paquetes de subida. README por proyecto con fuentes, límites, reproducción, novedad y atribución. Guiones de 2:30, respuestas al jurado y una estrategia comercial con hipótesis de cliente y criterios para abandonar una mala apuesta. GitHub recibe código y material público; no se envían mensajes a terceros.

## Fuentes primarias de las correcciones

- https://arxiv.org/abs/quant-ph/9707014
- https://www.ncei.noaa.gov/products/world-magnetic-model
- https://arxiv.org/abs/1905.09749
- https://arxiv.org/abs/2505.15917
- https://jbusemey.pages.iu.edu/quantum/PNAS2014.pdf

La ejecución local no certifica el puente Pyodide ni una corrida remota IonQ. Esos resultados se registran solamente cuando se observan.
