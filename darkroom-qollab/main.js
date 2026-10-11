import * as svc from "darkroom.engine";
import "./lesson.js";

const $ = (id) => document.getElementById(id);
const SVG = "http://www.w3.org/2000/svg";
let result = null;
let pending = null;
let busy = false;
let spent = false;
let auditBusy = false;
let lastReport = null;
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
  if (!lastReport && !auditBusy && !spent) $("auditStatus").textContent = `Start with local Qiskit measurement. Ideal prediction: ${p(idealSafe)} safe detections for a present object. The loss slider is excluded from both circuit runs.`;
}

function showReport(report) {
  lastReport = report;
  $("auditOutput").textContent = JSON.stringify(report, null, 2);
  const present = report.by_object_hypothesis.present;
  const absent = report.by_object_hypothesis.absent;
  $("measuredSummary").textContent = `${report.backend} · ${report.config.cycles} cycles · ${report.shots} simulated/recorded shots. Of ${present.shots} present-object trials: ${present.outcomes.identified_without_absorption} detected without absorption, ${present.outcomes.absorbed} absorbed, ${present.outcomes.unexpected_or_noise} unexpected. Of ${absent.shots} absent-object trials: ${absent.outcomes.identified_absent} correctly reached ABSENT. Ordinary optical loss is excluded.`;
  $("auditStatus").textContent = `Result received: ${p(present.rates.identified_without_absorption)} safe detections among present-object trials. Source: ${report.backend}. These counts belong to ${report.config.cycles} cycles, independently of later slider changes.`;
}

$("runLocal").addEventListener("click", async () => {
  if (busy || auditBusy || !result) return;
  const snapshot = { ...result.config };
  const button = $("runLocal"); button.disabled = true; auditBusy = true;
  $("auditStatus").textContent = "Measuring the Qiskit circuit locally: 1,024 simulated trials, no remote provider request…";
  try {
    showReport(JSON.parse(String(await py("local_audit", JSON.stringify(snapshot)))));
  } catch (error) {
    $("auditStatus").textContent = "Local Qiskit measurement failed. Open the technical error details below.";
    $("backendError").textContent = String(error.message || error);
    $("errorDetails").hidden = false;
  } finally { button.disabled = false; auditBusy = false; }
});

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
  if (busy || auditBusy || !result) { status.textContent = "Wait for the current calculation to finish."; return; }
  if (!hasBackend()) { status.textContent = "No Qollab backend is connected. The ideal Qiskit reference is still available."; return; }
  const snapshot = { ...result.config }; button.disabled = true; auditBusy = true; status.textContent = "Building the measured path-and-absorber circuit…";
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
    showReport(report);
    button.textContent = "Job used · restart Qollab to measure again";
  } catch (error) {
    const message = String(error.message || error);
    status.textContent = /failed to fetch|networkerror|connection aborted/i.test(message)
      ? "The selected backend could not be reached from this browser. No result was received. Use Measure locally with Qiskit; it needs no provider connection."
      : "The selected-backend attempt failed. Use the local Qiskit measurement or inspect the technical error below.";
    $("backendError").textContent = message; $("errorDetails").hidden = false;
    if (!spent) button.disabled = false;
    else button.textContent = "Attempt used · restart Qollab to try again";
  } finally { auditBusy = false; }
});

refresh();
