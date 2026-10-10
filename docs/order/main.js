import * as svc from "./preview-adapter.js";
import { $, percent, number, escapeHTML, connect } from "./runtime.js";
const api = connect(svc, typeof backend === "undefined" ? null : backend);
let current = null,
  reversed = false,
  matched = false,
  step = 0;
const params = () => ({
  theta: Number($("belief").value),
  angle: Number($("angle").value),
  info: Number($("information").value),
});
function table(ab, ba) {
  return `<table><thead><tr><th scope="col">Answers to A / B</th><th scope="col">Ask A then B</th><th scope="col">Ask B then A</th></tr></thead><tbody>${["Yes / Yes", "Yes / No", "No / Yes", "No / No"].map((v, i) => `<tr><th scope="row">${v}</th><td>${percent(ab[i])}</td><td>${percent(ba[i])}</td></tr>`).join("")}</tbody></table>`;
}
function headline() {
  if (!current) return;
  const p = reversed ? current.a_second : current.a_first;
  $("headline").textContent = percent(p) + " say yes to A.";
  $("headlineContext").textContent = reversed
    ? "A asked second, after B"
    : "A asked first, before B";
  $("headlineDelta").textContent =
    `${number(Math.abs(current.a_second - current.a_first) * 100)} percentage-point difference between orders in this model.`;
  $("ballots").classList.toggle("reversed", reversed);
  $("aNumber").textContent = reversed ? "Asked second" : "Asked first";
  $("bNumber").textContent = reversed ? "Asked first" : "Asked second";
}
function bloch(d) {
  let s =
    '<circle cx="140" cy="98" r="73" fill="#ebf0ff" stroke="#cbd4ed"/><line x1="45" y1="98" x2="235" y2="98" stroke="#cbd4ed"/><line x1="140" y1="12" x2="140" y2="178" stroke="#cbd4ed"/>';
  for (const [deg, color, label] of [
    [0, "#254cc8", "A"],
    [d.params.angle, "#b72e62", "B"],
    [d.params.theta, "#202f65", "state"],
  ]) {
    const a = (deg * Math.PI) / 180,
      x = 140 + Math.sin(a) * 72,
      y = 98 - Math.cos(a) * 72;
    s += `<line x1="140" y1="98" x2="${x}" y2="${y}" stroke="${color}" stroke-width="${label === "state" ? 2 : 4}"/><circle cx="${x}" cy="${y}" r="4" fill="${color}"/><text x="${x + 8}" y="${y - 5}" fill="${color}" font-size="12">${label}</text>`;
  }
  $("bloch").innerHTML = s;
}
function render(d) {
  current = d;
  for (const [id, v] of [
    ["belief", d.params.theta],
    ["angle", d.params.angle],
    ["information", d.params.info],
  ])
    $(id + "Value").textContent = v + "°";
  $("breakQQ").textContent = d.params.info
    ? "Remove the extra information"
    : "Insert new information";
  $("qq").textContent = Math.abs(d.qq) < 1e-10 ? "0.0000" : number(d.qq, 4);
  $("qqVerdict").textContent =
    Math.abs(d.qq) < 1e-10
      ? "QQ holds in this model. That alone does not identify a uniquely quantum explanation."
      : "The intervening rotation breaks the simple QQ prediction for these settings.";
  $("jointTable").innerHTML = table(d.ab, d.ba);
  headline();
  bloch(d);
  poll();
  if (matched) classical();
}
function poll() {
  if (!current) return;
  const d = current.polls.datasets.find((p) => p.id === $("poll").value);
  $("pollTitle").textContent = d.title;
  $("pollQuestions").textContent = "A: " + d.a + " B: " + d.b;
  const a1 = d.ab[0] + d.ab[1],
    a2 = d.ba[0] + d.ba[1];
  $("pollChart").innerHTML = [
    ["A asked first", a1, "#254cc8"],
    ["A asked after B", a2, "#b72e62"],
  ]
    .map(
      ([name, v, c]) =>
        `<div class="pollbar"><span>${name}: yes to A</span><div class="track"><div class="fill" style="width:${v * 100}%;background:${c}">${percent(v)}</div></div></div>`,
    )
    .join("");
  $("pollQQ").textContent = number(d.ab[1] + d.ab[2] - d.ba[1] - d.ba[2], 4);
  $("pollP").textContent = "Published QQ test p-value: " + d.published_qq_p;
  $("pollCondition").textContent = d.condition;
}
function classical() {
  if (!current) return;
  matched = true;
  const c = current.classical;
  $("classicalResult").innerHTML =
    `<strong>The classical model matches.</strong><p>Largest probability error: ${c.max_error.toExponential(1)}. Its QQ value is ${number(c.qq, 4)}. Remembering context is sufficient to reproduce the displayed distributions.</p><code>${Object.entries(
      c.parameters,
    )
      .map(([k, v]) => escapeHTML(k) + ": " + number(v, 4))
      .join(
        "<br>",
      )}</code><p>Six fitted conditional probabilities. This is a constructive classical baseline, not a prediction fitted on separate data.</p>`;
}
const refresh = () => api.update(params(), render);
for (const id of ["belief", "angle", "information"]) $(id).oninput = refresh;
$("swap").onclick = () => {
  reversed = !reversed;
  headline();
};
$("poll").onchange = poll;
$("classical").onclick = classical;
$("auditStudy").onclick = async () => {
  try {
    const rows = $("studyCounts")
      .value.trim()
      .split(/\n/)
      .map((row) =>
        row
          .trim()
          .split(/[\s,;]+/)
          .map((x) => {
            if (!/^\d+$/.test(x))
              throw new Error("Use nonnegative integer counts only");
            return Number(x);
          }),
      );
    if (rows.length !== 2) throw new Error("Enter exactly two rows");
    const report = await api.py(
      "audit_counts",
      JSON.stringify({ ab: rows[0], ba: rows[1] }),
    );
    api.setExtraEvidence("questionnaire_audit", report);
    $("studyResult").innerHTML =
      `<strong>Questionnaire audit</strong><p>${report.n_ab} AB responses; ${report.n_ba} BA responses.</p><p>A order effect: ${number(report.a_order_effect * 100, 2)} percentage points.<br>Approximate 95% CI: [${report.a_effect_ci95_normal.map((x) => number(x * 100, 2)).join(", ")}] points.</p><p>QQ difference: ${number(report.qq, 4)}.<br>Approximate 95% CI: [${report.qq_ci95_normal.map((x) => number(x, 4)).join(", ")}].<br>Two-sided normal-test p = ${number(report.qq_p_normal, 4)}.</p><p>${report.normal_approximation_adequate ? "Expected binary counts meet the ≥5 rule of thumb." : "Small expected counts: the normal approximation may be unreliable."}</p><p>${escapeHTML(report.assumptions)}</p>`;
  } catch (e) {
    $("studyResult").textContent = "Could not audit: " + e.message;
  }
};
$("breakQQ").onclick = () => {
  $("information").value = Number($("information").value) === 0 ? 65 : 0;
  $("breakQQ").textContent = Number($("information").value)
    ? "Remove the extra information"
    : "Insert new information";
  refresh();
};
const tour = [
  "Ask A first, then swap. You changed the sequence without editing either question. These are synthetic model responses.",
  "Look at QQ: the full joint distribution changes, yet a symmetry remains. Now insert a rotation between the questions.",
  "Try the Rose / Jackson dataset. The simple prediction fails when the experiment violates a premise. A useful model must have a way to lose.",
  "Invite the classical challenger. It matches the distributions too. The practical question is which model predicts new data with fewer assumptions.",
];
$("tour").onclick = () => {
  $("tourText").hidden = false;
  $("tourText").textContent = tour[step];
  if (step === 0) $("swap").click();
  if (step === 1) {
    $("information").value = 65;
    refresh();
    $("qq").scrollIntoView({ block: "center" });
  }
  if (step === 2) {
    $("poll").value = "rose-jackson";
    poll();
    $("poll").scrollIntoView({ block: "center" });
  }
  if (step === 3) {
    classical();
    $("classicalResult").scrollIntoView({ block: "center" });
  }
  step = (step + 1) % tour.length;
  $("tour").textContent = step
    ? "Next experiment step"
    : "Replay the experiment";
};
api.wireAudit(params);
refresh();
