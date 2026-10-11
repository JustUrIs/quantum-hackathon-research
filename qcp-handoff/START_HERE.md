# QCP Arena: entrega para otro agente

El usuario quiere una demo de hackathon y un pitch centrados en QCP. Tiene
presupuesto cero. El código funciona: el trabajo siguiente es mejorar su
presentación, verificar Qollab y producir una película de producto con IA.

## Qué pasar al agente

Pasale el repositorio y pedile que lea `qcp-handoff/AGENT_PROMPT.md` primero.
También podés pasarle `releases/qcp-agent-handoff.zip`: contiene solo QCP, sus
herramientas, tests y este brief. No necesita estudiar los proyectos anteriores.

Mensaje para copiar:

> Trabajá exclusivamente en QCP Arena. Leé qcp-handoff/AGENT_PROMPT.md y ejecutá
> ese brief. Usá qcp-handoff/PITCH.md para el discurso y
> qcp-handoff/DEMO_PRODUCTION.md para producir el video. El usuario autorizó las
> mejoras de QCP y su despliegue; no pidió cambiar los otros proyectos. Conservá
> el juez riguroso y entregá evidencia real, un sitio usable y una demo en inglés.

## Qué hace

El alumno lee un problema, escribe una solución en un subconjunto de
Python/Qiskit, prueba ejemplos y recibe un veredicto. Hay tres problemas y una
ronda virtual individual de 60 minutos. El juez evalúa probabilidades ideales,
presupuestos de consultas y casos variados. La clasificación es local.

## Archivos

- `AGENT_PROMPT.md`: instrucciones y límites para trabajar.
- `PITCH.md`: discurso en inglés, explicación en español y tesis comercial.
- `DEMO_PRODUCTION.md`: guion, storyboard y producción con herramientas gratuitas.
- `EDIT_PLAN.md`: prioridades y criterios de aceptación.
- `DEPLOYMENT.md`: publicación exclusiva de QCP en Vercel.
- `FACTS.md`: evidencia y afirmaciones que se pueden sostener.

La página principal está en https://qcp-arena.vercel.app.
La copia de GitHub Pages está en
https://justuris.github.io/quantum-hackathon-research/qcp/.
El paquete Qollab es `releases/qcp-qollab.zip`. La validación dentro de Qollab
sigue pendiente hasta que alguien registre una ejecución real.
