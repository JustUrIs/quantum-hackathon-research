# Probar DARKROOM y comprobar si enseña

1. Reemplazá los archivos del proyecto Qollab por el ZIP actualizado; incluí `lesson.js`, `lesson.css` y `darkroom/engine.py`. Volvé a presionar Run en Qollab.
2. Entrá a **Learn step by step / Aprendelo paso a paso** y elegí **Español**.
3. Recorré los seis pasos. En los pasos 3 y 4, presioná **Avanzar un ciclo** dos veces para comparar la caja vacía con el objeto presente.
4. En la caja vacía, observá cómo las contribuciones se cancelan para D0 y se suman para D1. Con objeto, observá los intentos absorbidos: 50% en el primer ciclo y otro 25% en el segundo; el 25% restante llega a D0.
5. Respondé las cuatro preguntas del paso 6 antes de consultar los anteriores. Guardá el puntaje y decí, con tus propias palabras, por qué un clic en D0 revela el objeto en el aparato ideal.
6. En la sección de medición, presioná **Measure locally with Qiskit**. La configuración inicial es de dos ciclos; el informe debe identificar **Qiskit BasicSimulator**, 1.024 tiros y simulación local. Los porcentajes de muestra pueden diferir de los valores exactos.

La ejecución del backend elegido es una prueba separada y opcional. Si IonQ devuelve `Failed to fetch`, no hubo un resultado recibido de ese proveedor. El botón local mide un circuito Qiskit en el runtime Python sin llamar a IonQ. La nueva ruta local está verificada en el entorno de desarrollo; su prueba en Qollab/Pyodide queda pendiente hasta correr esta versión ahí.

No confundas el número de qubits con fotones: el modelo representa dos caminos de un fotón y utiliza otros qubits para etiquetar condiciones y registrar absorciones. El objetivo no es conservar intacto el estado inicial del fotón: la lectura final es una medición.

Esto prueba comprensión de cuatro conceptos concretos; no constituye un estudio controlado de eficacia educativa.
