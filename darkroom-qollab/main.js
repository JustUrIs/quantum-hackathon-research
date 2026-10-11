import * as svc from "darkroom.engine";

const $ = (id) => document.getElementById(id);
const SVG = "http://www.w3.org/2000/svg";
let result = null;
let pending = null;
let busy = false;
let spent = false;
const hasBackend = () => { try { return typeof backend !== "undefined" && backend !== null; } catch { return false; } };
const py = async (name, ...args) => await svc[name].callPromising(...args);
const p = (v) => `${(100 * v).toFixed(1)}%`;
const activeConfig = () => ({ cycles: Number($("cycles").value), loss_per_pass: Number($("loss").value) / 100 });

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
  const defs = node("defs");
  const pattern = node("pattern", { id: "blockedHatch", width: 9, height: 9, patternTransform: "rotate(45)", patternUnits: "userSpaceOnUse" }, defs);
  node("rect", { width: 9, height: 9, fill: "#f0755b" }, pattern);
  node("line", { x1: 0, y1: 0, x2: 0, y2: 9, stroke: "#101820", "stroke-width": 3 }, pattern);
  // The split arms and recombination are the main visual explanation.
  node("path", { d: "M56 194H164L204 92H480L528 194M204 296H480L528 194M528 194L676 118M528 194L676 270", class: "light-path" });
  node("path", { d: "M204 92H480", class: "object-path" });
  node("circle", { cx: 56, cy: 194, r: 12, class: "source" });
  text(56, 230, "PROBE", "diagram-label");
  node("rect", { x: 151, y: 181, width: 26, height: 26, transform: "rotate(45 164 194)", class: "splitter" });
  text(164, 239, "SPLIT", "diagram-label");
  node("rect", { x: 515, y: 181, width: 26, height: 26, transform: "rotate(45 528 194)", class: "splitter" });
  text(528, 239, "RECOMBINE", "diagram-label");
  node("rect", { x: 326, y: 67, width: 72, height: 50, rx: 3, class: "object" });
  text(362, 89, "OBJECT", "object-word"); text(362, 105, "PRESENT?", "object-word small");
  const passXs = Array.from({ length: n }, (_, i) => 218 + (i * 244) / Math.max(1, n - 1));
  passXs.forEach((x, i) => {
    node("circle", { cx: x, cy: 92, r: 5, class: "pass-dot" });
    text(x, 69, String(i + 1).padStart(2, "0"), "pass-number");
  });
  // A small, quiet absorber marker makes the dangerous arm legible.
  node("rect", { x: 333, y: 75, width: 58, height: 34, rx: 2, fill: "url(#blockedHatch)", class: "absorber" });
  node("circle", { cx: 685, cy: 113, r: 18, class: "detector detector-present" });
  node("circle", { cx: 685, cy: 275, r: 18, class: "detector detector-absent" });
  text(685, 153, "PRESENT", "detector-label");
  text(685, 315, "ABSENT", "detector-label");
  node("circle", { cx: 204, cy: 296, r: 6, class: "mirror" });
  node("circle", { cx: 480, cy: 296, r: 6, class: "mirror" });
  text(380, 365, `${n} weak rotations · one coherent interferometer`, "diagram-caption");
  $("cycleStamp").textContent = `${String(n).padStart(2, "0")} PASSES`;
}

function outcomeRows(target, data, labels) {
  const el = $(target); el.replaceChildren();
  for (const [key, label, type] of labels) {
    const value = data[key] || 0;
    const row = document.createElement("div"); row.className = `prob-row ${type}`;
    const top = document.createElement("div"); top.className = "prob-top";
    const name = document.createElement("span"); name.textContent = label;
    const percent = document.createElement("strong"); percent.textContent = p(value);
    const track = document.createElement("div"); track.className = "prob-track";
    const fill = document.createElement("i"); fill.style.width = `${Math.max(0, Math.min(100, value * 100))}%`;
    track.appendChild(fill); top.append(name, percent); row.append(top, track); el.appendChild(row);
  }
}
function render(d) {
  result = d;
  const m = d.model, q = m.quantum_interrogation, direct = m.direct;
  drawInterferometer(d.config.cycles);
  $("cyclesValue").textContent = d.config.cycles;
  $("lossValue").textContent = `${(100 * d.config.loss_per_pass).toFixed(1)}%`;
  $("qubitCount").textContent = `${d.qubits} QUBITS`;
  const rowsAbsent = [
    ["identified_absent", "Object correctly identified absent", "positive"],
    ["lost_inconclusive", "Probe lost · inconclusive", "loss"],
  ];
  const rowsPresent = [
    ["identified_without_absorption", "Object identified · probe survives", "positive"],
    ["absorbed", "Object identified · probe absorbed", "damage"],
    ["lost_inconclusive", "Probe lost · inconclusive", "loss"],
  ];
  outcomeRows("absentRows", q.absent, rowsAbsent);
  outcomeRows("presentRows", q.present, rowsPresent);
  $("absentFoot").textContent = `All outcomes total ${p(m.checks.quantum_absent_total)}. Loss model: ${p(direct.absent.lost_inconclusive)} per direct pass; ${p(q.absent.lost_inconclusive)} across ${d.config.cycles} quantum passes.`;
  $("presentFoot").textContent = `All outcomes total ${p(m.checks.quantum_present_total)}. Damage is counted as a real sample cost, not a successful free probe.`;
  const rows = $("compareRows"); rows.replaceChildren();
  const tableRows = [
    ["Object absent", `Detector confirms absent ${p(direct.absent.identified_absent)} · lost ${p(direct.absent.lost_inconclusive)}`, `Detector confirms absent ${p(q.absent.identified_absent)} · lost ${p(q.absent.lost_inconclusive)}`, `${d.config.cycles} passes create ${d.config.cycles} loss opportunities`],
    ["Object present", `Absorbed / detected ${p(direct.present.absorbed)} · lost ${p(direct.present.lost_inconclusive)}`, `Survives / confirms present ${p(q.present.identified_without_absorption)} · absorbed ${p(q.present.absorbed)} · lost ${p(q.present.lost_inconclusive)}`, "Direct test destroys the probe; quantum test can still absorb it"],
  ];
  for (const row of tableRows) { const tr = document.createElement("tr"); for (const cell of row) { const td = document.createElement("td"); td.textContent = cell; tr.appendChild(td); } rows.appendChild(tr); }
  const mismatch = d.circuit.analytic_max_error;
  $("status").textContent = mismatch < 1e-9 ? `Model checked · formula and Qiskit statevector agree within ${mismatch.toExponential(1)}` : `Model check failed · formula differs from statevector by ${mismatch}`;
  $("liveDot").dataset.error = mismatch >= 1e-9 ? "true" : "false";
  // The circuit probability is a no-loss reference; keep it explicitly separate.
  const idealSafe = d.circuit.ideal_statevector_outcomes.present.identified_without_absorption;
  $("auditStatus").textContent = `No-loss Qiskit reference: ${p(idealSafe)} present detections without absorption. Analytic loss model is separate.`;
}

async function refresh() {
  pending = activeConfig(); if (busy) return; busy = true;
  try {
    while (pending) {
      const config = pending; pending = null;
      $("status").textContent = "Propagating every branch; absorbed and lost probes remain visible…";
      const raw = await py("evaluate", JSON.stringify(config));
      if (!pending) render(JSON.parse(String(raw)));
    }
  } catch (error) { $("status").textContent = `Model could not run: ${error.message || error}`; $("liveDot").dataset.error = "true"; }
  finally { busy = false; if (pending) refresh(); }
}
for (const id of ["cycles", "loss"]) $(id).addEventListener("input", refresh);

$("runBackend").addEventListener("click", async () => {
  const button = $("runBackend"), status = $("auditStatus");
  if (spent) { status.textContent = "This project run already used its one backend job. Restart it in Qollab to capture a new measurement."; return; }
  if (busy || !result) { status.textContent = "Wait for the probability model to finish."; return; }
  if (!hasBackend()) { status.textContent = "No Qollab backend is connected. The ideal Qiskit reference is still available."; return; }
  const snapshot = { ...result.config }; button.disabled = true; status.textContent = "Building the measured path-and-absorber circuit…";
  try {
    const circuit = await svc.audit_circuit.callPromising(JSON.stringify(snapshot));
    const name = String(backend.name || backend.backend_name || "selected backend");
    const shots = /ionq/i.test(name) ? 100 : 1024;
    spent = true;
    status.textContent = `Submitting one ${circuit.num_qubits}-qubit experiment · ${shots} shots · ${name}.`;
    const job = await backend.run(circuit, { shots });
    const response = await job.result();
    const raw = response.get_counts(); const v = raw && raw.toJs ? raw.toJs() : raw;
    const counts = v instanceof Map ? Object.fromEntries(v) : v;
    const report = JSON.parse(String(await svc.ingest_audit.callPromising(JSON.stringify(counts), JSON.stringify(snapshot), name)));
    $("auditOutput").textContent = JSON.stringify(report, null, 2); $("auditDetails").open = true;
    const a = report.by_object_hypothesis.absent.rates.identified_absent;
    const s = report.by_object_hypothesis.present.rates.identified_without_absorption;
    status.textContent = `${report.shots} measured shots on ${report.backend}. Correct absent-port rate: ${p(a)}; present detections without absorption: ${p(s)}. Inspect every count below.`;
    button.textContent = "Job used · restart Qollab to measure again";
  } catch (error) { status.textContent = `Backend job failed: ${error.message || error}. The local formula remains separate.`; if (!spent) button.disabled = false; }
});

refresh();
