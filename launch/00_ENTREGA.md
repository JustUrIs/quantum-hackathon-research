# Tres proyectos: de demo local a entrega

Los tres viven en el mismo repositorio que IMPOSTOR y se suben a Qollab como proyectos independientes. No necesitan servicios pagos ni claves. Cada carpeta contiene código, licencia MIT, datos y un README que sirve como ficha.

| Proyecto | Carpeta | Momento de la demo | Tema recomendado |
|---|---|---|---|
| LOST SIGNAL | `lost-signal-qollab/` | apagar GPS, subir ruido, perder la mejora GHZ | Unlocked; Impact solo con validación adicional |
| Q-DAY CLOCK: the evidence room | `qday-clock-qollab/` | dos histogramas iguales, uno con la respuesta filtrada | Unlocked |
| ORDER | `order-qollab/` | intercambiar preguntas, romper QQ, dejar ganar al clásico | Playground / Unlocked |

## Abrir todo localmente

Desde la raíz, ejecutar `python tools/serve.py` y abrir http://127.0.0.1:8766/. En esta máquina puede usarse `.venv/Scripts/python.exe`. Instalación desde cero: `python -m pip install -r requirements-dev.txt` y `python -m playwright install chromium`.

No abrir `index.html` con doble clic: los imports Python necesitan el runtime Qollab o el servidor local. El servidor escucha solo en localhost. El repositorio incluye capturas y evidencia real de BasicSimulator en `artifacts/`; esas corridas NO son de IonQ.

## Subir y verificar en Qollab

1. Elegir una carpeta de proyecto, o extraer el ZIP correspondiente en `releases/`. Subir su contenido conservando las carpetas Python y `data/`. `index.html` y `main.js` deben quedar en la raíz.
2. Abrirlo con el simulador gratuito integrado. Esperar el estado «Local model ready». Ejecutar el recorrido de un minuto del README. Verificar que cambien gráficos y números.
3. Presionar el botón de backend una sola vez. Debe terminar con counts, nombre del backend y parámetros. Exportar el JSON. Mover controles después no debe modificar la evidencia capturada.
4. Detener y reiniciar el proyecto, eligiendo un simulador gratuito IonQ. Probar el backend una vez más. Q-DAY debe empezar con N=15 y a=2. El envío usa 100 shots y puede tardar varios minutos. No seleccionar hardware pago por error.
5. Guardar el resultado identificado como IonQ solamente si la corrida real terminó. Si falla, guardar el error exacto; nunca reemplazarlo por un resultado ideal con la etiqueta remota.
6. Grabar el recorrido de 2:30 con los guiones de este directorio. Subir el video a un enlace público sin login, incorporar ese enlace a la ficha y comprobar que se reproduce.
7. Publicar cada proyecto en Qollab y entregar desde la cuenta del capitán. Revisar titular, tema, licencia, atribución y divulgación de trabajo previo.

Las notas del evento indican cierre el domingo 11 de octubre de 2026 a las 19:00 ET, equivalente a 20:00 ART. Usar 19:00 ART como límite interno y confirmar el horario en la página oficial antes de entregar. El resultado local y el push a GitHub no sustituyen la publicación ni la entrega en Qollab.

## Evidencia mínima antes de marcar «listo para competir»

- Enlace público del proyecto que un tercero pueda ejecutar.
- Recorrido completo en Qollab y una corrida en el simulador IonQ, con JSON o error revisado.
- Video público de 2–3 minutos, revisado por alguien que no conoce el proyecto.
- Revisión del compañero de cuántica: metrología a tiempo fijo; síntesis modular y recuperación; QQ y alcance del modelo clásico.
- Entrega visible en la página del equipo del capitán.

La sesión de construcción no dispone de un navegador conectado a Qollab. Es una limitación de acceso concreta: no se registra una publicación ni una corrida remota que no haya ocurrido. Los paquetes y las fichas se preparan para que ese tramo sea corto y verificable.

## Elegir dónde invertir la última hora

Si quedan 60 minutos, invertirlos en una corrida de Qollab, una objeción física y un video comprensible. Una animación adicional tiene menor ROI. Si falta la prueba de Impact para LOST SIGNAL, presentarlo en Unlocked con precisión científica, sin convertir el corredor ilustrativo en una afirmación de navegación.

El informe `research/06_BUILD_DECISIONS.md` reemplaza las promesas excesivas del brief inicial. La propuesta original se conserva como antecedente, no como especificación de resultados logrados.
