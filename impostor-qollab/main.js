// IMPOSTOR: you try to fake a quantum computer; Qiskit referees catch you.
// Python (impostor/) owns every circuit, the referee and the scoring. This file owns
// the UI and the single call to the backend selected in Qollab's Select QPU dialog.
import * as svc from 'impostor.service';

const $ = (id) => document.getElementById(id);
const log = (...a) => console.log('[impostor]', ...a);
const pct = (x) => (x == null || Number.isNaN(x) ? '–' : `${(100 * x).toFixed(1)}%`);
const sgn = (v) => (v > 0 ? '+' : '−');

async function py(fn, ...args) {
  const out = await svc[fn].callPromising(...args);
  return JSON.parse(String(out));
}

const state = {
  ov: null,
  source: 'exact',
  seed: 1,
  chsh: { strategy: [0, 0, 0, 0], you: [], q: [] },
  magic: { grid: [[1, 1, 1], [1, 1, 1], [1, 1, 1]], you: [], q: [], ask: null },
  zip: { n: 8, data: {}, urandom: {} },
  auditDone: false,
};

const backendName = () => {
  try { return String(backend.name ?? backend.backend_name ?? 'selected backend'); } catch { return 'no backend'; }
};

// ------------------------------------------------------------------ the one job
// IonQ backends accept ONE job per run and return counts only, so Python packs the
// 4 CHSH settings and 3 magic-square cells side by side in one 20-qubit circuit.
async function runAudit() {
  const status = $('auditStatus');
  try {
    if (typeof backend === 'undefined') throw new Error('no backend selected');
    const name = backendName();
    const shots = /ionq/i.test(name) ? 100 : 500;
    const circuit = await svc.audit_circuit.callPromising();
    status.textContent = `Sending one ${circuit.num_qubits}-qubit circuit × ${shots} shots to ${name}… (IonQ simulators take a while)`;
    log(`audit: ${circuit.num_qubits} qubits, ${shots} shots on ${name}`);
    const job = await backend.run(circuit, { shots });
    const res = await job.result();
    const raw = res.get_counts();
    const m = raw && raw.toJs ? raw.toJs() : raw;
    const counts = m instanceof Map ? Object.fromEntries(m) : m;
    const rep = await py('ingest_audit', JSON.stringify(counts), name);
    renderAudit(rep);
    state.auditDone = true;
    const btn = document.querySelector('#source [data-source="audit"]');
    btn.disabled = false;
    btn.textContent = `This run: ${name}`;
  } catch (err) {
    status.textContent = `Audit job did not run (${err.message || err}). The game still works with exact Qiskit sampling.`;
    log('audit failed', err);
  }
}

function renderAudit(rep) {
  $('auditStatus').textContent = `${rep.backend} measured ${rep.shots} shots of the packed circuit. Same circuits, real backend:`;
  const cells = [
    ['Telepathy (CHSH), all 4 settings', rep.chsh_total, state.ov.chsh.classical_max, '75% max for any faker'],
    ['Magic square, 3 cells', rep.magic_total, state.ov.magic.classical_max, '88.9% max for any faker'],
  ];
  $('auditTable').innerHTML = cells.map(([name, v, cap, capTxt]) =>
    `<div class="audit-cell ${v > cap ? '' : 'fail'}"><span>${name}</span><b>${pct(v)}</b><span>${v > cap ? 'beats' : 'does not beat'} the classical ceiling · ${capTxt}</span></div>`).join('');
  $('auditTable').hidden = false;
}

// ------------------------------------------------------------------ source
const SOURCE_NOTES = {
  exact: 'Each answer is one shot sampled from the exact statevector of the round\'s Qiskit circuit: what a perfect device would return.',
  audit: () => `Answers are real shots from this run's single job on ${backendName()}, including its noise. Settings the job did not cover fall back to exact sampling.`,
  urandom: 'quantumslop mode: the quantum player is replaced by /dev/urandom, as in the April 2026 1 BTC episode. Watch the "quantum" record collapse.',
};

function setSource(src) {
  state.source = src;
  document.querySelectorAll('#source button').forEach((b) => b.setAttribute('aria-checked', String(b.dataset.source === src)));
  const n = SOURCE_NOTES[src];
  $('sourceNote').textContent = typeof n === 'function' ? n() : n;
  const label = src === 'urandom' ? '/dev/urandom' : src === 'audit' ? `Quantum pair (${backendName()})` : 'Quantum pair';
  for (const id of ['chshQLabel', 'magicQLabel']) $(id).textContent = label;
  document.querySelectorAll('.meter.q').forEach((el) => el.classList.toggle('slop', src === 'urandom'));
  resetChsh(); resetMagic();
  if (state.zip.n) drawZip();
}

// ------------------------------------------------------------------ charts
function lineChart(svg, series, ceiling, qmax, ceilingLabel) {
  const W = 600, H = 220, L = 40, R = 12, T = 12, B = 26;
  const n = Math.max(1, ...series.map((s) => s.values.length));
  const x = (i) => L + (W - L - R) * (n <= 1 ? 0 : i / (n - 1));
  const y = (v) => T + (H - T - B) * (1 - v);
  let g = '';
  for (const v of [0, 0.25, 0.5, 0.75, 1]) g += `<line class="grid" x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}"/><text x="4" y="${y(v) + 4}">${v * 100}%</text>`;
  g += `<line class="ceiling" x1="${L}" x2="${W - R}" y1="${y(ceiling)}" y2="${y(ceiling)}"/><text x="${W - R - 4}" y="${y(ceiling) - 6}" text-anchor="end" style="fill:var(--caught)">${ceilingLabel}</text>`;
  g += `<line class="qline" x1="${L}" x2="${W - R}" y1="${y(qmax)}" y2="${y(qmax)}"/>`;
  for (const s of series) {
    if (!s.values.length) continue;
    let acc = 0;
    const pts = s.values.map((w, i) => { acc += w ? 1 : 0; return `${x(i).toFixed(1)},${y(acc / (i + 1)).toFixed(1)}`; });
    g += `<polyline class="${s.cls}" points="${pts.join(' ')}"/>`;
  }
  g += `<text x="${L}" y="${H - 6}">rounds played: ${n}</text>`;
  svg.innerHTML = g;
}

const rate = (arr) => (arr.length ? arr.reduce((a, b) => a + (b ? 1 : 0), 0) / arr.length : null);

function verdict(el, you, q, ceiling, rounds, exact) {
  if (rounds < 20) { el.innerHTML = rounds ? 'Keep playing. Short runs are noisy; the referee is patient.' : ''; return; }
  if (state.source === 'urandom') {
    el.innerHTML = `<span class="stamp">FAKE</span> /dev/urandom wins ${pct(q)} and falls below the classical ceiling. The referee catches it too.`;
  } else if (q > ceiling) {
    el.innerHTML = `<span class="stamp">CAUGHT</span> The quantum pair: ${pct(q)}, above what any classical plan can reach. Your plan is worth ${pct(exact)} however long you play${you > exact ? '; your current lead is luck' : ''}.`;
  } else {
    el.innerHTML = `<span class="stamp ok">NOISY</span> Quantum at ${pct(q)} this time. Play more rounds: with fewer than ~200, luck still matters.`;
  }
}

// ------------------------------------------------------------------ level 1
function renderChshStrategy() {
  document.querySelectorAll('#chshStrategy .bit').forEach((el) => {
    const i = Number(el.dataset.i);
    el.innerHTML = [0, 1].map((v) => `<button aria-pressed="${state.chsh.strategy[i] === v}" data-v="${v}">${v}</button>`).join('');
    el.querySelectorAll('button').forEach((b) => b.onclick = () => { state.chsh.strategy[i] = Number(b.dataset.v); renderChshStrategy(); });
  });
}

async function playChsh(n) {
  state.seed += 1;
  const res = await py('play_chsh', n, JSON.stringify(state.chsh.strategy), state.source, state.seed);
  for (const r of res.rounds) { state.chsh.you.push(r.you[2]); state.chsh.q.push(r.q[2]); }
  state.chsh.exact = res.your_exact;
  $('chshExact').textContent = `your plan's exact value: ${pct(res.your_exact)}`;
  const r = res.rounds[res.rounds.length - 1];
  const w = (ok) => (ok ? '<span class="w">WIN</span>' : '<span class="l">LOSE</span>');
  $('chshLast').innerHTML = `Referee asks x=${r.x}, y=${r.y}. Target a⊕b = ${r.x & r.y}.\n` +
    `You:     a=${r.you[0]} b=${r.you[1]}  ${w(r.you[2])}\n` +
    `Quantum: a=${r.q[0]} b=${r.q[1]}  ${w(r.q[2])}   (${r.src})`;
  updateChsh();
}

function updateChsh() {
  const you = rate(state.chsh.you), q = rate(state.chsh.q);
  $('chshYou').textContent = pct(you);
  $('chshQ').textContent = pct(q);
  lineChart($('chshChart'), [{ values: state.chsh.you, cls: 'you' }, { values: state.chsh.q, cls: 'qp' }], 0.75, state.ov.chsh.quantum_max, 'classical ceiling 75%');
  verdict($('chshVerdict'), you, q, 0.75, state.chsh.you.length, state.chsh.exact);
}

function resetChsh() { state.chsh.you = []; state.chsh.q = []; $('chshExact').textContent = ''; $('chshLast').textContent = 'No rounds yet.'; updateChsh(); }

function chshBot() {
  const b = state.ov.chsh.bruteforce;
  $('chshVerdict').innerHTML = `<span class="stamp">CEILING</span> The bot tried all ${b.tried} plans. Best: ${pct(b.best)} (${b.at_best} plans tie). Shared randomness only mixes these, so nothing classical beats 75%.`;
}

// ------------------------------------------------------------------ level 2
function magicAnswers(g, r, c) {
  const row = [g[r][0], g[r][1]]; row.push(row[0] * row[1]);
  const col = [g[0][c], g[1][c]]; col.push(-col[0] * col[1]);
  return { y: row[c], p: col[r] };
}

function renderMagic() {
  const g = state.magic.grid;
  let html = '', clashes = 0;
  for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
    const { y, p } = magicAnswers(g, r, c);
    const clash = y !== p; clashes += clash;
    const editable = !(r === 2 && c === 2);
    const ask = state.magic.ask && state.magic.ask[0] === r && state.magic.ask[1] === c;
    const big = editable ? sgn(g[r][c]) : '?';
    const desc = `Row ${r + 1} column ${c + 1}: you answer ${y > 0 ? 'plus' : 'minus'}, partner answers ${p > 0 ? 'plus' : 'minus'}${clash ? ', clash' : ''}`;
    html += `<div class="cell ${clash ? 'clash' : ''} ${ask ? 'ask' : ''}" role="gridcell">
      <button class="main" data-r="${r}" data-c="${c}" ${editable ? '' : 'disabled'} aria-label="${desc}${editable ? '. Press to flip.' : '. Forced by both rules.'}">${big}</button>
      <span class="ab" aria-hidden="true"><span>Y ${sgn(y)}</span><span>P ${sgn(p)}</span></span></div>`;
  }
  $('magicGrid').innerHTML = html;
  $('magicGrid').querySelectorAll('button.main:not(:disabled)').forEach((b) => b.onclick = () => {
    const r = Number(b.dataset.r), c = Number(b.dataset.c);
    state.magic.grid[r][c] *= -1; renderMagic();
  });
  $('magicConflicts').textContent = `${clashes} cell${clashes === 1 ? '' : 's'} clash → your plan wins ${9 - clashes}/9 = ${pct((9 - clashes) / 9)} of rounds. Try to make it 0.`;
}

async function playMagic(n) {
  state.seed += 1;
  const res = await py('play_magic', n, JSON.stringify(state.magic.grid), state.source, state.seed);
  for (const r of res.rounds) { state.magic.you.push(r.you[2]); state.magic.q.push(r.q[2]); }
  state.magic.exact = res.your_exact.value;
  $('magicExact').textContent = `your plan's exact value: ${pct(res.your_exact.value)}`;
  const r = res.rounds[res.rounds.length - 1];
  state.magic.ask = [r.r, r.c];
  const s3 = (a) => a.map(sgn).join(' ');
  const w = (ok) => (ok ? '<span class="w">WIN</span>' : '<span class="l">LOSE</span>');
  $('magicLast').innerHTML = `Referee asks row ${r.r + 1}, column ${r.c + 1}.\n` +
    `You:     row [${s3(r.you[0])}]  partner col [${s3(r.you[1])}]  ${w(r.you[2])}\n` +
    `Quantum: row [${s3(r.q[0])}]  partner col [${s3(r.q[1])}]  ${w(r.q[2])}   (${r.src})`;
  renderMagic(); updateMagic();
}

function updateMagic() {
  const you = rate(state.magic.you), q = rate(state.magic.q);
  $('magicYou').textContent = pct(you);
  $('magicQ').textContent = pct(q);
  lineChart($('magicChart'), [{ values: state.magic.you, cls: 'you' }, { values: state.magic.q, cls: 'qp' }], 8 / 9, 1, 'classical ceiling 8/9');
  verdict($('magicVerdict'), you, q, 8 / 9, state.magic.you.length, state.magic.exact);
}

function resetMagic() { state.magic.you = []; state.magic.q = []; state.magic.ask = null; $('magicExact').textContent = ''; $('magicLast').textContent = 'No rounds yet.'; renderMagic(); updateMagic(); }

function magicBot() {
  // Search the 256 grids this UI allows, then show the full-strategy result from Python.
  let best = null, bestClash = 10;
  for (let m = 0; m < 256; m++) {
    const b = (i) => ((m >> i) & 1 ? -1 : 1);
    const g = [[b(0), b(1), b(2)], [b(3), b(4), b(5)], [b(6), b(7), 1]];
    let cl = 0;
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) { const { y, p } = magicAnswers(g, r, c); cl += y !== p; }
    if (cl < bestClash) { bestClash = cl; best = g; }
  }
  state.magic.grid = best; resetMagic();
  const bf = state.ov.magic.bruteforce;
  $('magicVerdict').innerHTML = `<span class="stamp">CEILING</span> The bot tried all ${bf.tried.toLocaleString()} plans. Best: ${pct(bf.best)} (${bf.at_best} plans tie). It loaded one of them into your grid. One cell always clashes.`;
}

// ------------------------------------------------------------------ level 3
const ZIP_MULT = [1, 4, 8, 16, 32, 64, 128, 256, 512];
const zipKs = (n) => ZIP_MULT.map((m) => m * n);

async function loadZip(n) {
  state.zip.n = n;
  if (!state.zip.data[n]) {
    $('zipVerdict').textContent = n === 12 ? 'Loading the precomputed 12-qubit curve…' : 'Computing the live curve with Qiskit statevectors (a few seconds)…';
    state.zip.data[n] = await py('zip_curve', n, JSON.stringify(zipKs(n)), 4, 1);
    state.zip.urandom[n] = (await py('zip_urandom', n, 4, 1)).xeb;
  }
  $('zipQLabel').textContent = `Quantum: ${n} qubits`;
  drawZip();
}

function zipPoint() {
  const d = state.zip.data[state.zip.n];
  if (!d) return null;
  return d.impostor[Number($('zipK').value)];
}

function drawZip() {
  const d = state.zip.data[state.zip.n];
  const k = zipKs(state.zip.n)[Number($('zipK').value)];
  $('zipKVal').textContent = k.toLocaleString();
  $('zipKLabel').textContent = k.toLocaleString();
  if (!d) return;
  const W = 600, H = 260, L = 40, R = 14, T = 14, B = 34;
  const ks = d.impostor.map((p) => p.k);
  const lx = (v) => Math.log2(v);
  const x0 = lx(Math.min(...ks, 60)), x1 = lx(Math.max(...ks));
  const x = (v) => L + (W - L - R) * (lx(v) - x0) / (x1 - x0);
  const y = (v) => T + (H - T - B) * (1 - Math.max(-0.05, Math.min(1.1, v)) / 1.1);
  const qx = state.source === 'urandom' ? state.zip.urandom[state.zip.n] : d.quantum;
  let g = '';
  for (const v of [0, 0.25, 0.5, 0.75, 1]) g += `<line class="grid" x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}"/><text x="4" y="${y(v) + 4}">${v}</text>`;
  for (const kk of ks) g += `<text x="${x(kk)}" y="${H - 18}" text-anchor="middle">${kk >= 1000 ? (kk / 1000).toFixed(kk % 1000 ? 1 : 0) + 'k' : kk}</text>`;
  g += `<text x="${W - R}" y="${H - 4}" text-anchor="end">bits the impostor sends (log scale)</text>`;
  g += `<line class="qline" x1="${L}" x2="${W - R}" y1="${y(qx)}" y2="${y(qx)}" style="opacity:1;${state.source === 'urandom' ? 'stroke:var(--caught)' : ''}"/>`;
  g += `<text x="${L + 6}" y="${y(qx) - 6}" style="fill:${state.source === 'urandom' ? 'var(--caught)' : 'var(--quantum)'}">${state.source === 'urandom' ? '/dev/urandom' : `${d.n} qubits`}: XEB ${qx.toFixed(2)}</text>`;
  g += `<polyline class="you" points="${d.impostor.map((p) => `${x(p.k)},${y(p.xeb)}`).join(' ')}"/>`;
  for (const p of d.impostor) g += `<circle class="dot-you" cx="${x(p.k)}" cy="${y(p.xeb)}" r="${p.k === k ? 6 : 3}"/>`;
  if (d.n === 12) {
    const pp = d.paper;
    g += `<circle class="dot-paper" cx="${x(pp.lower_bound_bits)}" cy="${y(pp.hardware_xeb)}" r="6"/><text x="${x(pp.lower_bound_bits) + 9}" y="${y(pp.hardware_xeb) - 8}" style="fill:var(--caught)">theorem: ≥${pp.lower_bound_bits} bits for ${pp.hardware_xeb}</text>`;
    g += `<circle class="dot-paper" cx="${x(pp.best_known_bits)}" cy="${y(pp.hardware_xeb)}" r="6"/><text x="${x(pp.best_known_bits) + 9}" y="${y(pp.hardware_xeb) + 16}" style="fill:var(--caught)">best known classical: ${pp.best_known_bits} bits</text>`;
  }
  $('zipChart').innerHTML = g;
}

function zipSend() {
  const p = zipPoint(), d = state.zip.data[state.zip.n];
  if (!p) return;
  const qx = state.source === 'urandom' ? state.zip.urandom[state.zip.n] : d.quantum;
  $('zipYou').textContent = p.xeb.toFixed(3);
  $('zipQ').textContent = qx.toFixed(3);
  const ratio = (p.k / d.n).toFixed(0);
  $('zipVerdict').innerHTML = state.source === 'urandom'
    ? `<span class="stamp">FAKE</span> Random strings score ${qx.toFixed(3)}: zero. The test can't be passed by noise.`
    : p.xeb >= qx * 0.95
      ? `<span class="stamp ok">MATCHED</span> With ${p.k} bits you reached the quantum score. That's ${ratio}× more bits than qubits.`
      : `<span class="stamp">CAUGHT</span> ${p.k.toLocaleString()} bits (${ratio}× the qubit count) score ${p.xeb.toFixed(3)}. ${d.n} qubits score ${qx.toFixed(3)}.`;
  drawZip();
}

// ------------------------------------------------------------------ tabs & init
function selectTab(id) {
  document.querySelectorAll('.tabs [role="tab"]').forEach((t) => {
    const on = t.id === id;
    t.setAttribute('aria-selected', String(on));
    t.tabIndex = on ? 0 : -1;
    $(t.getAttribute('aria-controls')).hidden = !on;
  });
  if (id === 'tab-zip' && !state.zip.data[state.zip.n]) loadZip(state.zip.n);
}

function wire() {
  document.querySelectorAll('#source button').forEach((b) => b.onclick = () => setSource(b.dataset.source));
  const tabs = [...document.querySelectorAll('.tabs [role="tab"]')];
  tabs.forEach((t, i) => {
    t.onclick = () => selectTab(t.id);
    t.onkeydown = (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        const j = (i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length;
        tabs[j].focus(); selectTab(tabs[j].id);
      }
    };
  });
  $('chshOne').onclick = () => playChsh(1);
  $('chshMany').onclick = () => playChsh(200);
  $('chshBot').onclick = chshBot;
  $('chshReset').onclick = resetChsh;
  $('magicOne').onclick = () => playMagic(1);
  $('magicMany').onclick = () => playMagic(200);
  $('magicBot').onclick = magicBot;
  $('magicReset').onclick = resetMagic;
  $('zipN').onchange = (e) => loadZip(Number(e.target.value));
  $('zipK').oninput = drawZip;
  $('zipRun').onclick = zipSend;
}

async function init() {
  state.ov = await py('overview');
  $('obsSquare').innerHTML = state.ov.magic.square.flat().map((o) => `<span>${o}</span>`).join('');
  wire();
  renderChshStrategy();
  resetChsh();
  resetMagic();
  log('ready. Referees:', JSON.stringify({ chsh: state.ov.chsh.bruteforce, magic: state.ov.magic.bruteforce }));
  await runAudit();
}

init();
