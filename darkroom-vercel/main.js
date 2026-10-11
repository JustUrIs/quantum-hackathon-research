// Static companion for Vercel. This page shows the analytic model only;
// the measured Qiskit circuit lives in the Qollab project.
const $ = (id) => document.getElementById(id);
const p = (x) => `${(100 * x).toFixed(1)}%`;
const SVG = "http://www.w3.org/2000/svg";
function node(name, attrs = {}, parent = $("interferometer")) {
  const el = document.createElementNS(SVG, name);
  for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, String(value));
  parent.appendChild(el);
  return el;
}
function text(x, y, label, klass, parent) {
  const el = node("text", { x, y, class: klass }, parent); el.textContent = label; return el;
}

function drawInterferometer(n) {
  const svg = $("interferometer"); svg.replaceChildren();
  node("title", { id: "opticTitle" }).textContent = "Two photon paths and two possible detector outputs";
  node("desc", { id: "opticDesc" }).textContent = "An absorbing object can block the upper arm. A surviving photon at the present detector reveals the object without absorption.";
  const defs = node("defs");
  const pattern = node("pattern", { id: "blockedHatch", width: 9, height: 9, patternTransform: "rotate(45)", patternUnits: "userSpaceOnUse" }, defs);
  node("rect", { width: 9, height: 9, fill: "#f0755b" }, pattern);
  node("line", { x1: 0, y1: 0, x2: 0, y2: 9, stroke: "#101820", "stroke-width": 3 }, pattern);
  // The split arms and recombination are the main visual explanation.
  node("path", { d: "M56 194H164L204 92H480L528 194M164 194L204 296H480L528 194M528 194L676 118M528 194L676 270", class: "light-path" });
  node("path", { d: "M204 92H480", class: "object-path" });
  node("circle", { cx: 56, cy: 194, r: 12, class: "source" });
  text(56, 230, "PHOTON", "diagram-label");
  node("rect", { x: 151, y: 181, width: 26, height: 26, transform: "rotate(45 164 194)", class: "splitter" });
  text(164, 239, "SPLIT", "diagram-label");
  node("rect", { x: 515, y: 181, width: 26, height: 26, transform: "rotate(45 528 194)", class: "splitter" });
  text(528, 239, "RECOMBINE", "diagram-label");
  node("rect", { x: 326, y: 67, width: 72, height: 50, rx: 3, class: "object" });
  node("rect", { x: 333, y: 75, width: 58, height: 34, rx: 2, fill: "url(#blockedHatch)", class: "absorber" });
  text(362, 89, "OBJECT", "object-word"); text(362, 105, "PRESENT?", "object-word small");
  const passXs = Array.from({ length: n }, (_, i) => 218 + (i * 244) / Math.max(1, n - 1));
  passXs.forEach((x, i) => {
    node("circle", { cx: x, cy: 92, r: 5, class: "pass-dot" });
    text(x, 69, String(i + 1).padStart(2, "0"), "pass-number");
  });
  node("circle", { cx: 685, cy: 113, r: 18, class: "detector detector-present" });
  node("circle", { cx: 685, cy: 275, r: 18, class: "detector detector-absent" });
  text(685, 153, "PRESENT", "detector-label");
  text(685, 315, "ABSENT", "detector-label");
  node("circle", { cx: 204, cy: 296, r: 6, class: "mirror" });
  node("circle", { cx: 480, cy: 296, r: 6, class: "mirror" });
  text(380, 365, `${n} weak rotations · one coherent interferometer`, "diagram-caption");
  $("cycleStamp").textContent = `${String(n).padStart(2, "0")} PASSES`;
}


function model(n, loss) {
  const theta = Math.PI / (2 * n), c2 = Math.cos(theta) ** 2, s2 = Math.sin(theta) ** 2;
  const absent = { identified_absent: (1 - loss) ** n, lost_inconclusive: 1 - (1 - loss) ** n };
  let active = 1, absorbed = 0, lost = 0;
  for (let i = 0; i < n; i++) { absorbed += active * s2; lost += active * c2 * loss; active *= c2 * (1 - loss); }
  return { absent, present: { identified_without_absorption: active, absorbed, lost_inconclusive: lost }, direct: {
    absent: { identified_absent: 1 - loss, lost_inconclusive: loss },
    present: { absorbed: 1 - loss, lost_inconclusive: loss },
  } };
}
function rows(id, data, labels) {
  const el = $(id); el.replaceChildren();
  for (const [key, label, type] of labels) {
    const value = data[key] || 0, row = document.createElement('div'); row.className = `prob-row ${type}`;
    const top = document.createElement('div'); top.className = 'prob-top';
    const name = document.createElement('span'); name.textContent = label;
    const pct = document.createElement('strong'); pct.textContent = p(value);
    const track = document.createElement('div'); track.className = 'prob-track';
    const fill = document.createElement('i'); fill.style.width = `${value * 100}%`;
    top.append(name, pct); track.append(fill); row.append(top, track); el.append(row);
  }
}
function render() {
  const n = +$('cycles').value, loss = +$('loss').value / 100, m = model(n, loss);
  $('cyclesValue').textContent = n; $('lossValue').textContent = p(loss); $('cycleStamp').textContent = `${String(n).padStart(2,'0')} PASSES`;
  drawInterferometer(n);
  $('qubitCount').textContent = `${n + 2} QUBITS`;
  rows('absentRows', m.absent, [['identified_absent','Object correctly identified absent','positive'],['lost_inconclusive','Probe lost · inconclusive','loss']]);
  rows('presentRows', m.present, [['identified_without_absorption','Object identified · probe survives','positive'],['absorbed','Object identified · probe absorbed','damage'],['lost_inconclusive','Probe lost · inconclusive','loss']]);
  $('absentFoot').textContent = `Outcomes total ${p(m.absent.identified_absent + m.absent.lost_inconclusive)}. ${n} passes create ${n} opportunities for ordinary loss.`;
  $('presentFoot').textContent = `All outcomes total ${p(m.present.identified_without_absorption + m.present.absorbed + m.present.lost_inconclusive)}. Absorption counts as sample cost.`;
  const tr = $('compareRows'); tr.replaceChildren();
  const lines = [
    ['Object absent',`Detector confirms absent ${p(m.direct.absent.identified_absent)} · lost ${p(m.direct.absent.lost_inconclusive)}`,`Detector confirms absent ${p(m.absent.identified_absent)} · lost ${p(m.absent.lost_inconclusive)}`,`${n} passes create ${n} loss opportunities`],
    ['Object present',`Absorbed / detected ${p(m.direct.present.absorbed)} · lost ${p(m.direct.present.lost_inconclusive)}`,`Survives / confirms present ${p(m.present.identified_without_absorption)} · absorbed ${p(m.present.absorbed)} · lost ${p(m.present.lost_inconclusive)}`,'Direct test destroys the probe; quantum test can still absorb it'],
  ];
  for(const line of lines){const row=document.createElement('tr');for(const value of line){const cell=document.createElement('td');cell.textContent=value;row.append(cell)}tr.append(row)}
  $('status').textContent = 'Analytic companion ready · no Qiskit circuit or backend job runs on this page.';
}
for (const id of ['cycles','loss']) $(id).addEventListener('input', render);
render();
