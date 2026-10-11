// Bilingual teaching walkthrough. The lesson uses exact two-cycle, zero-loss
// analytic probabilities; actual Qiskit measurements are a separate experiment.
(() => {
  const root = document.getElementById('lesson');
  if (!root) return;
  let lang = navigator.language.startsWith('es') ? 'es' : 'en';
  let step = 0, pass = 0, graded = false;
  const answers = {};
  const copy = {
    es: {
      eyebrow: 'Aprendelo antes de correrlo', title: 'Un fotón. Dos caminos. Una pregunta.',
      intro: 'Queremos saber si hay un objeto que absorbe luz. ¿Podemos averiguarlo en algunos intentos sin que el objeto absorba nuestro fotón?',
      next: 'Siguiente', previous: 'Anterior', step: 'Paso', advance: 'Avanzar un ciclo', reset: 'Volver al inicio',
      safe: 'Camino 0 · libre', blocked: 'Camino 1 · donde puede estar el objeto', mixer: 'Mezclador', object: 'Absorbe',
      detector0: 'D0: revela presencia', detector1: 'D1: revela ausencia',
      remaining: 'Fotones que siguen disponibles', absorbed: 'Intentos absorbidos por el objeto',
      traceNote: 'Los porcentajes describen muchas repeticiones. Cada intento envía UN fotón entero. La lección supone dos ciclos y pérdida ordinaria cero.',
      scope: 'Este recorrido usa probabilidades analíticas. El proyecto de Qollab también permite medir un circuito Qiskit. La app modela un experimento: no recibe luz de una cámara.',
      titles: ['El fotón no se parte por la mitad.', 'Qué hace cada pieza.', 'Primero: la caja está vacía.', 'Ahora: un objeto bloquea el camino 1.', 'Por qué una detección revela el objeto.', 'Comprobá qué aprendiste.'],
      texts: [
        ['Un fotón es una unidad de luz. Un divisor de haz prepara dos alternativas cuánticas de camino. No fabrica dos medios fotones: una medición ideal registra un fotón completo en un solo detector.', 'Las dos alternativas tienen amplitudes que pueden reforzarse o cancelarse cuando se vuelven a mezclar. No es lo mismo que tirar una moneda para elegir un camino secreto.'],
        ['Un mezclador de caminos puede implementarse con un divisor de haz. Mezcla las amplitudes de los dos caminos. Los espejos, en un montaje óptico, solamente redirigen la luz.', 'El bloque rojo representa un objeto que absorbe la luz del camino 1. D0 y D1 son detectores: un clic es la lectura final. “Sobrevivir” significa evitar la absorción por el objeto; la detección final termina la prueba. Este dibujo muestra ciclos lógicos, no el plano de un dispositivo.'],
        ['Empezamos en el camino 0. Sin objeto, después del primer ciclo una medición tendría 50% de probabilidad en cada camino. En el segundo mezclador, las contribuciones de ambos caminos se cancelan para D0 y se suman para D1: el fotón termina en D1 con 100% de probabilidad.', 'Las amplitudes son números que usamos para predecir las probabilidades; no son mitades de energía. No medimos entre ciclos: hacerlo destruiría esta interferencia. Avanzá los dos ciclos para ver la cancelación.'],
        ['Después de cada mezcla, el objeto absorbe la alternativa del camino 1. El fotón se absorbe por completo en esos intentos. Los intentos que sobreviven quedan en el camino 0 y pasan al siguiente ciclo.', 'Tras el primer ciclo, sobrevive la mitad de los intentos. Tras el segundo, sobrevive la mitad de esa mitad: 25% del total. Esos fotones llegan enteros a D0. El otro 75% de los intentos fue absorbido.'],
        ['Compará las dos cajas: vacía → D0 nunca hace clic; con objeto → D0 puede hacer clic. Por eso, en este modelo ideal, un clic en D0 revela el objeto. Ese fotón sobrevivió: no lo absorbió el objeto.', 'No basta con decir “llegó menos luz”. La información está en QUÉ detector responde. Tampoco conservamos el estado inicial del fotón: la lectura final es una medición. El objetivo es aprender sobre el objeto evitando su absorción en algunos intentos.'],
        ['Respondé sin mirar los pasos anteriores. Después vas a ver las explicaciones.', 'Utilidad: enseñar interferencia, medición y el costo de sondear un objeto. Este principio motiva investigar mediciones con poca absorción; nuestra simulación por sí sola no demuestra un sensor práctico.'],
      ],
      check: 'Comprobar mis respuestas', incomplete: 'Respondé las cuatro preguntas primero.', score: 'Conceptos correctos',
      questions: [
        ['¿Qué llega a un detector al medir un solo fotón?', ['Dos mitades de energía en dos detectores.', 'Un fotón entero en un solo detector.', 'Dos fotones enteros.'], 1, 'El divisor de haz mezcla amplitudes de camino, no divide un fotón en dos fotones más pequeños.'],
        ['¿Por qué D0 puede revelar el objeto en el aparato ideal?', ['Porque la luz es más tenue.', 'Porque D0 nunca responde con la caja vacía.', 'Porque el fotón informa cuál camino secreto eligió.'], 1, 'Comparamos resultados posibles: D0 es imposible con la caja vacía al terminar los dos ciclos.'],
        ['¿Cuál es el objetivo de la prueba?', ['Mantener intacto el estado original del fotón para siempre.', 'Conocer la presencia del objeto sin que absorba algunos de los fotones usados.', 'Producir energía extra.'], 1, 'La lectura final mide el fotón; preservar su estado inicial no es el objetivo.'],
        ['Si hay pérdidas comunes y ningún detector hace clic, ¿qué concluimos?', ['Seguro hay un objeto.', 'Seguro no hay un objeto.', 'El intento es inconcluso: también pudo perderse el fotón.'], 2, 'Sin un clic, la pérdida ordinaria puede confundirse con absorción. No debemos contarla como detección.'],
      ],
      emptyState: 'Caja vacía', presentState: 'Objeto presente', both: 'Mismo aparato; dos condiciones distintas',
      zeroResult: 'Inicio: un fotón disponible en el camino 0.', emptyResult: 'Final: D1 = 100%; D0 = 0%.', presentResult: 'Final: D0 = 25%; absorbidos = 75%.',
      pathProb: 'Probabilidad de cada camino si midiéramos ahora', cycle: 'Ciclo', treeTitle: 'Promedio de 100 intentos independientes',
      tree1: '100 fotones, uno por intento', tree2: 'Primer ciclo: 50 absorbidos; 50 siguen', tree3: 'Segundo ciclo: 25 más absorbidos; 25 llegan a D0',
      emptyFinal: 'Caja vacía: 0 de 100 en D0', presentFinal: 'Con objeto: 25 de 100 en D0, sin absorción',
    },
    en: {
      eyebrow: 'Learn before you run', title: 'One photon. Two paths. One question.',
      intro: 'We want to know whether a light-absorbing object is present. Can some attempts reveal it without that object absorbing our photon?',
      next: 'Next', previous: 'Previous', step: 'Step', advance: 'Advance one cycle', reset: 'Restart the trace',
      safe: 'Path 0 · clear', blocked: 'Path 1 · possible object', mixer: 'Mixer', object: 'Absorber',
      detector0: 'D0: reveals presence', detector1: 'D1: reveals absence',
      remaining: 'Photons still available', absorbed: 'Attempts absorbed by the object',
      traceNote: 'Percentages describe many repetitions. Each attempt sends ONE whole photon. This lesson assumes two cycles and zero ordinary loss.',
      scope: 'This walkthrough uses analytic probabilities. The Qollab project also measures a Qiskit circuit. The app models an experiment; it does not receive light from a camera.',
      titles: ['The photon is not split in half.', 'What each component does.', 'First: the apparatus is empty.', 'Now: an object blocks path 1.', 'Why a detection reveals the object.', 'Check what you learned.'],
      texts: [
        ['A photon is one unit of light. A beam splitter prepares two quantum path alternatives. It does not make two half-photons: an ideal measurement registers one whole photon at one detector.', 'The two alternatives have amplitudes that can reinforce or cancel when mixed again. This is different from flipping a coin to choose a hidden path.'],
        ['A path mixer can be implemented with a beam splitter. It mixes the amplitudes of the two paths. Mirrors in an optical setup merely redirect the light.', 'The red block represents an object absorbing light in path 1. D0 and D1 are detectors: a click is the final readout. Surviving means avoiding absorption by the object; final detection ends the trial. This drawing shows logical cycles, not an optical construction plan.'],
        ['Start in path 0. After the first cycle, a measurement would have 50% probability in each path. In the second mixer, contributions from both paths cancel at D0 and add at D1: the photon ends at D1 with 100% probability.', 'Amplitudes are numbers used to predict probabilities, rather than halves of the energy. We do not measure between cycles: that would destroy this interference. Advance both cycles to see the cancellation.'],
        ['After each mixing step, the object absorbs the path-1 alternative. The whole photon is absorbed in those attempts. Surviving attempts remain in path 0 and continue to the next cycle.', 'Half the attempts survive the first cycle. Half of that half survive the second: 25% of all attempts. Those whole photons reach D0. The other 75% were absorbed.'],
        ['Compare the two conditions: empty → D0 never clicks; object present → D0 can click. So, in this ideal model, a D0 click reveals the object. That photon survived: the object did not absorb it.', 'The information is WHICH detector responds, rather than simply reduced brightness. The final readout measures the photon. The goal is learning about the object while avoiding its absorption in some attempts.'],
        ['Answer without checking earlier steps, then read the explanations.', 'Use: teaching interference, measurement and the cost of probing an object. This principle motivates research into low-absorption measurements; our simulation alone does not demonstrate a practical sensor.'],
      ],
      check: 'Check my answers', incomplete: 'Answer all four questions first.', score: 'Correct concepts',
      questions: [
        ['What reaches a detector when measuring a single photon?', ['Two half-energy clicks at two detectors.', 'One whole photon at one detector.', 'Two whole photons.'], 1, 'The beam splitter mixes path amplitudes, rather than splitting a photon into smaller photons.'],
        ['Why can D0 reveal the object in the ideal apparatus?', ['Because the light is dimmer.', 'Because D0 never clicks when the apparatus is empty.', 'Because the photon reveals which hidden path it chose.'], 1, 'Compare possible outcomes: D0 is impossible in the empty apparatus at the end of the two cycles.'],
        ['What is the goal of this test?', ['Keep the original photon state intact forever.', 'Learn the object is present without its absorbing some of our probes.', 'Generate extra energy.'], 1, 'The final readout measures the photon; preserving its initial state is not the goal.'],
        ['With ordinary loss and no detector click, what can we conclude?', ['An object is certainly present.', 'An object is certainly absent.', 'The attempt is inconclusive: the photon may have been lost.'], 2, 'Ordinary loss can be confused with absorption when there is no click. It must not count as detection.'],
      ],
      emptyState: 'Empty apparatus', presentState: 'Object present', both: 'Same apparatus; two different conditions',
      zeroResult: 'Start: one photon available in path 0.', emptyResult: 'Final: D1 = 100%; D0 = 0%.', presentResult: 'Final: D0 = 25%; absorbed = 75%.',
      pathProb: 'Path probabilities if measured now', cycle: 'Cycle', treeTitle: 'Expected values over 100 independent attempts',
      tree1: '100 photons, one per attempt', tree2: 'First cycle: 50 absorbed; 50 continue', tree3: 'Second cycle: 25 more absorbed; 25 reach D0',
      emptyFinal: 'Empty: 0 out of 100 at D0', presentFinal: 'Present: 25 out of 100 at D0 without absorption',
    },
  };
  function diagram(c, present, progress=0) {
    return `<svg class="lesson-svg" viewBox="0 0 650 290" role="img" aria-label="${present ? c.presentState : c.emptyState}">
      <path d="M90 100H545M90 200H545" fill="none" stroke="#718996" stroke-width="2"/>
      <text x="90" y="75">${c.blocked}</text><text x="90" y="240">${c.safe}</text>
      <circle cx="90" cy="200" r="10" fill="#63d6c5"/>
      ${[210,380].map((x,i)=>`<rect x="${x-18}" y="86" width="36" height="130" rx="5" fill="${i<progress?'#37586a':'#243b53'}" stroke="#63d6c5" stroke-width="${i<progress?3:1}"/><path d="M${x-12} 193L${x+12} 107M${x-12} 107L${x+12} 193" stroke="#63d6c5"/><text x="${x}" y="265" text-anchor="middle">${c.mixer} ${i+1}</text>${present ? `<rect x="${x+35}" y="87" width="61" height="26" rx="3" fill="#f0755b"/><text x="${x+65}" y="104" text-anchor="middle" style="fill:#101820">${c.object}</text>` : ''}`).join('')}
      <circle cx="550" cy="100" r="14" fill="${progress===2&&!present?'#e8c87a':'#e8c87a22'}" stroke="#e8c87a"/><circle cx="550" cy="200" r="14" fill="${progress===2&&present?'#63d6c5':'#63d6c522'}" stroke="#63d6c5"/>
      <text x="560" y="72" text-anchor="end">${c.detector1}</text><text x="560" y="242" text-anchor="end">${c.detector0}</text>
    </svg><div class="lesson-detector-key"><span>${c.detector0}</span><span>${c.detector1}</span></div>`;
  }
  function bar(label, probability, kind='safe') {
    return `<div class="lesson-prob ${kind}"><span>${label}</span><strong>${(probability*100).toFixed(0)}%</strong><div><i style="width:${probability*100}%"></i></div></div>`;
  }
  function trace(c, present) {
    const safe = present ? Math.pow(0.5,pass) : Math.cos(pass*Math.PI/4)**2;
    const other = present ? 1-safe : Math.sin(pass*Math.PI/4)**2;
    const interference = !present && pass===2 ? `<div class="lesson-interference"><p>${lang==='es'?'Contribuciones de amplitud en la segunda mezcla':'Amplitude contributions at the second mixer'}</p><div><span>D0</span><strong>½ − ½ = 0</strong><small>0%</small></div><div><span>D1</span><strong>½ + ½ = 1</strong><small>100%</small></div><p>${lang==='es'?'Se cancela la posibilidad de D0; no se pierde la energía del fotón.':'The D0 possibility cancels; the photon energy is not lost.'}</p></div>` : '';
    return `<div class="lesson-visual"><p class="lesson-visual-title">${present ? c.presentState : c.emptyState} · ${c.cycle} ${pass}/2</p>${diagram(c,present,pass)}
      <p>${present ? c.remaining : c.pathProb}</p>
      ${bar(present ? c.remaining : c.safe,safe)}${bar(present ? c.absorbed : c.blocked,other,present?'absorbed':'other')}
      <p class="lesson-trace-result" role="status">${pass===0 ? c.zeroResult : pass===2 ? (present?c.presentResult:c.emptyResult) : '50% / 50%'}</p>
      ${interference}
      <div class="lesson-trace-controls"><button id="lessonAdvance" ${pass===2?'disabled':''}>${c.advance}</button><button id="lessonReset" class="lesson-secondary">${c.reset}</button></div>
      <small>${c.traceNote}</small></div>`;
  }
  function quiz(c) {
    const questions = c.questions.map((q,i)=>`<fieldset><legend>${i+1}. ${q[0]}</legend>${q[1].map((choice,j)=>`<label><input type="radio" name="lesson-q${i}" value="${j}" ${answers[i]===j?'checked':''}/><span>${choice}</span></label>`).join('')}${graded?`<p class="lesson-feedback ${answers[i]===q[2]?'correct':'incorrect'}">${answers[i]===q[2]?'✓':'↻'} ${q[3]}</p>`:''}</fieldset>`).join('');
    return `<div class="lesson-quiz">${questions}<button id="lessonGrade">${c.check}</button><p id="lessonScore" role="status">${graded?`${c.score}: ${c.questions.filter((q,i)=>answers[i]===q[2]).length}/4`:''}</p></div>`;
  }
  function render() {
    const c=copy[lang];
    const visual = step===2 || step===3 ? trace(c,step===3) : step===4
      ? `<div class="lesson-visual lesson-tree"><p class="lesson-visual-title">${c.treeTitle}</p>${[c.tree1,c.tree2,c.tree3].map((x,i)=>`<div>${i?'↓<br/>':''}${x}</div>`).join('')}<p class="lesson-proof">${c.emptyFinal}<br/><strong>${c.presentFinal}</strong></p><small>${c.traceNote}</small></div>`
      : step===5 ? quiz(c) : `<div class="lesson-visual"><p class="lesson-visual-title">${c.both}</p>${diagram(c,step===1)}<p class="lesson-single-photon">${lang==='es'?'1 fotón → 1 clic de detector':'1 photon → 1 detector click'} <span> ${lang==='es'?'o absorción':'or absorption'}</span></p></div>`;
    root.innerHTML=`<div class="lesson-heading"><div><p class="eyebrow">${c.eyebrow}</p><h2>${c.title}</h2></div><div class="lesson-languages" aria-label="Language"><button data-lang="es" aria-pressed="${lang==='es'}">Español</button><button data-lang="en" aria-pressed="${lang==='en'}">English</button></div></div>
      <p class="lesson-intro">${c.intro}</p><div class="lesson-progress">${copy[lang].titles.map((_,i)=>`<span class="${i<=step?'reached':''}"></span>`).join('')}</div>
      <div class="lesson-layout"><div class="lesson-copy"><p class="lesson-step">${c.step} ${step+1}/6</p><h3>${c.titles[step]}</h3>${c.texts[step].map(x=>`<p>${x}</p>`).join('')}<div class="lesson-nav"><button id="lessonPrevious" class="lesson-secondary" ${step===0?'disabled':''}>← ${c.previous}</button><button id="lessonNext" ${step===5?'disabled':''}>${c.next} →</button></div></div>${visual}</div><p class="lesson-scope">${c.scope}</p>`;
    root.querySelectorAll('[data-lang]').forEach(button=>button.addEventListener('click',()=>{lang=button.dataset.lang;render()}));
    document.getElementById('lessonPrevious').addEventListener('click',()=>{step--;pass=0;render()});
    document.getElementById('lessonNext').addEventListener('click',()=>{step++;pass=0;render()});
    if(step===2||step===3){document.getElementById('lessonAdvance').addEventListener('click',()=>{pass++;render()});document.getElementById('lessonReset').addEventListener('click',()=>{pass=0;render()})}
    if(step===5){
      root.querySelectorAll('input[type=radio]').forEach(input=>input.addEventListener('change',()=>{answers[Number(input.name.replace('lesson-q',''))]=Number(input.value);graded=false;render()}));
      document.getElementById('lessonGrade').addEventListener('click',()=>{
        if(Object.keys(answers).length!==4){document.getElementById('lessonScore').textContent=c.incomplete;return}
        graded=true;render();
      });
    }
  }
  render();
})();
