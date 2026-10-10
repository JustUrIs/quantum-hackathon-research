import * as svc from "qday.service";
import { $, percent, escapeHTML, connect } from "./runtime.js";
const api = connect(svc, typeof backend === "undefined" ? null : backend);
const params = () => ({
  n: Number($("modulus").value),
  a: Number($("base").value),
  bits: 6,
  mix: Number($("mixture").value),
});
function clock() {
  const h = Number($("horizon").value),
    l = Number($("lifetime").value),
    m = Number($("migration").value),
    slack = h - l - m;
  for (const [id, v] of [
    ["horizon", h],
    ["lifetime", l],
    ["migration", m],
  ])
    $(id + "Value").textContent = v + " year" + (v === 1 ? "" : "s");
  const color = slack < 0 ? "#b9314f" : "#5841ba";
  let ticks = "";
  for (let j = 0; j < 60; j++) {
    const a = (j * Math.PI) / 30;
    const r = j % 5 ? 181 : 173;
    ticks += `<line x1="${220 + Math.sin(a) * r}" y1="${220 - Math.cos(a) * r}" x2="${220 + Math.sin(a) * 190}" y2="${220 - Math.cos(a) * 190}" stroke="#b5bdcd" stroke-width="${j % 5 ? 1 : 2}"/>`;
  }
  const frac = Math.min(1, (l + m) / h),
    circ = 2 * Math.PI * 157;
  $("clock").innerHTML =
    `<circle cx="220" cy="220" r="204" fill="white"/>${ticks}<circle cx="220" cy="220" r="157" fill="none" stroke="#eceef3" stroke-width="14"/><circle cx="220" cy="220" r="157" fill="none" stroke="${color}" stroke-width="14" stroke-dasharray="${frac * circ} ${circ}" transform="rotate(-90 220 220)"/><text x="220" y="167" text-anchor="middle" font-size="14">Migration headroom</text><text x="220" y="251" text-anchor="middle" style="font:86px Georgia,serif;fill:${color}">${slack > 0 ? "+" : ""}${slack}</text><text x="220" y="285" text-anchor="middle" font-size="18">years in your scenario</text><text x="220" y="317" text-anchor="middle" font-size="12">${h} − ${l} − ${m} = ${slack}</text>`;
  $("clockVerdict").textContent =
    slack < 0
      ? "Your scenario leaves a confidentiality gap."
      : slack === 0
        ? "Your scenario leaves no migration buffer."
        : "Your scenario leaves room to migrate.";
  api.setExtraEvidence("planning_scenario", {
    assumed_attack_horizon_years: h,
    confidentiality_years: l,
    migration_years: m,
    headroom_years: slack,
    forecast: false,
  });
}
for (const id of ["horizon", "lifetime", "migration"]) $(id).oninput = clock;
$("scenarioPreset").onclick = () => {
  $("horizon").value = 10;
  $("lifetime").value = 25;
  $("migration").value = 4;
  clock();
};
function render(d) {
  for (const [prefix, data] of [
    ["genuine", d.genuine],
    ["fake", d.presolved],
  ]) {
    $(prefix + "Q").textContent = data.qubits;
    $(prefix + "CX").textContent = data.cx.toLocaleString();
    $(prefix + "Depth").textContent = data.depth.toLocaleString();
  }
  $("periodLeak").textContent =
    `Period supplied: r = ${d.presolved.period_supplied}. Already solved classically.`;
  $("mixtureValue").textContent = percent(d.params.mix);
  $("randomize").textContent =
    d.params.mix === 1
      ? "Restore the ideal circuit outputs"
      : "Replace all outputs with random bits";
  const prob = d.display_probabilities,
    max = Math.max(...prob) * 1.13,
    W = 720,
    H = 280,
    L = 42,
    B = 38,
    T = 22,
    R = 14,
    bw = (W - L - R) / prob.length;
  let s = "";
  for (let j = 0; j <= 4; j++) {
    const p = (max * j) / 4,
      y = H - B - ((H - B - T) * j) / 4;
    s += `<line x1="${L}" x2="${W - R}" y1="${y}" y2="${y}" stroke="#d4d8e2"/><text x="${L - 7}" y="${y + 4}" text-anchor="end" font-size="10">${percent(p)}</text>`;
  }
  prob.forEach((p, i) => {
    const h = (p / max) * (H - B - T);
    s += `<rect x="${L + i * bw + 1}" y="${H - B - h}" width="${Math.max(1, bw - 2)}" height="${h}" fill="${d.winning_bins.includes(i) ? "#5841ba" : "#aeb6c7"}"><title>Phase ${i}/64: ${percent(p)}${d.winning_bins.includes(i) ? ", factor recovered" : ""}</title></rect>`;
  });
  for (let i = 0; i <= 56; i += 8)
    s += `<text x="${L + i * bw}" y="${H - 15}" font-size="11">${i}/64</text>`;
  $("histogram").innerHTML = s;
  $("histogramNote").textContent =
    `Purple bins yield checked nontrivial factors. Genuine vs pre-solved ideal histogram difference: ${d.histogram_distance.toExponential(1)}. The imitation can match the output without running order finding. ${d.genuine_success < 1e-10 ? "This base yields no useful factor: a legitimate algorithmic failure. Try another coprime base." : ""}`;
  const rows = [
    ["Current output + recovery", d.display_success, "#5841ba"],
    ["Uniform phase bits + same recovery", d.random_phase_success, "#b9314f"],
    ["Random integer + GCD", d.random_gcd_success, "#74809a"],
  ];
  $("baselineBars").innerHTML = rows
    .map(
      ([name, v, color]) =>
        `<div class="barrow"><span>${escapeHTML(name)}</span><div class="bartrack"><div class="barfill" style="width:${v * 100}%;background:${color}"></div></div><b>${percent(v)}</b></div>`,
    )
    .join("");
  $("trialDivision").textContent =
    `Classical trial division finds ${d.trial_division_factors.join(" × ")} in ${d.trial_division_checks} divisor checks. On this tiny instance, you should use it.`;
}
const refresh = () => api.update(params(), render);
const gcd = (a, b) => (b ? gcd(b, a % b) : a);
$("modulus").onchange = () => {
  const n = Number($("modulus").value);
  $("base").innerHTML = Array.from({ length: 8 }, (_, i) => i + 2)
    .filter((a) => gcd(a, n) === 1)
    .map((a) => `<option value="${a}">${a}</option>`)
    .join("");
  refresh();
};
$("base").onchange = refresh;
$("mixture").oninput = refresh;
$("randomize").onclick = () => {
  $("mixture").value = Number($("mixture").value) === 1 ? 0 : 1;
  $("randomize").textContent =
    Number($("mixture").value) === 1
      ? "Restore the ideal circuit outputs"
      : "Replace all outputs with random bits";
  refresh();
};
api.wireAudit(params);
clock();
refresh();
