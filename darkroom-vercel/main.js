// Static companion for Vercel. This page shows the analytic model only;
// the measured Qiskit circuit lives in the Qollab project.
const $ = (id) => document.getElementById(id);
const p = (x) => `${(100 * x).toFixed(1)}%`;
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
