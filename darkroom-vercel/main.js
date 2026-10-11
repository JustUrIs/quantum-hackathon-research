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
  node("title", { id: "opticTitle" }).textContent = "Repeated mixing of two photon paths and a final readout";
  node("desc", { id: "opticDesc" }).textContent = "Start in clear path 0. Each cycle mixes path amplitudes. A present object can absorb path 1 after each cycle. Only the final detectors are measured.";
  node("path", { d: "M100 120H680M56 270H680", class: "light-path" });
  node("path", { d: "M120 120H610", class: "object-path" });
  node("circle", { cx: 56, cy: 270, r: 11, class: "source" });
  text(56, 308, "1 PHOTON", "diagram-label");
  text(358, 60, "PATH 1 / THE OBJECT CAN ABSORB HERE", "diagram-label");
  text(356, 315, "PATH 0 / CLEAR", "diagram-label");
  for (let i = 0; i < n; i++) {
    const x = 150 + (i * 410) / Math.max(1, n - 1);
    node("rect", { x: x - 10, y: 104, width: 20, height: 182, rx: 4, class: "splitter" });
    node("path", { d: `M${x-6} 254L${x+6} 134M${x-6} 134L${x+6} 254`, fill: "none", stroke: "#63d6c5", "stroke-width": 1.4 });
    node("circle", { cx: x, cy: 90, r: 4, class: "pass-dot" });
    text(x, 76, String(i + 1).padStart(2, "0"), "pass-number");
    node("rect", { x: x + 15, y: 112, width: 16, height: 16, rx: 2, class: "object" });
  }
  node("circle", { cx: 687, cy: 120, r: 17, class: "detector detector-absent" });
  node("circle", { cx: 687, cy: 270, r: 17, class: "detector detector-present" });
  text(687, 163, "D1: ABSENT", "detector-label");
  text(687, 313, "D0: PRESENT", "detector-label");
  text(380, 365, `${n} mixing cycles, then one final detector measurement`, "diagram-caption");
  $("cycleStamp").textContent = `${String(n).padStart(2, "0")} CYCLES`;
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
