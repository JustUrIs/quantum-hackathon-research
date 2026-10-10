import * as svc from "lostsignal.service";
import { $, number, chart, connect } from "./runtime.js";
const api = connect(svc, typeof backend === "undefined" ? null : backend);
let result = null,
  gpsOff = false,
  isotropic = false,
  storyStep = 0;
const params = () => ({
  n: Number($("probes").value),
  eta: Number($("noise").value),
  shots: Number($("shots").value),
});
function drawMap() {
  if (!result) return;
  const route = result.route.points,
    x = (lon) => 90 + ((lon + 75) / 25) * 510,
    y = (lat) => 75 + ((-lat - 30) / 29) * 510;
  const points = route.map((p) => [x(p.lon), y(p.lat)]),
    end = points.at(-1),
    start = points[0];
  let s =
    '<defs><pattern id="mapgrid" width="55" height="55" patternUnits="userSpaceOnUse"><path d="M55 0H0V55" fill="none" stroke="#21465b" stroke-width=".6"/></pattern></defs><rect width="680" height="660" fill="url(#mapgrid)"/>';
  // Deliberately schematic coast; field samples have real lat/lon in evidence.
  s +=
    '<path d="M90 0 L315 0 325 78 398 125 356 175 342 235 298 292 286 360 247 420 251 477 236 525 286 572 245 596 207 568 177 522 163 461 150 398 143 340 121 276 117 214 97 149Z" fill="#153b4b" stroke="#416176"/>';
  s +=
    '<text x="158" y="245" transform="rotate(-78 158 245)" style="letter-spacing:4px;font-size:14px">PATAGONIA</text><text x="390" y="380" style="letter-spacing:3px">SOUTH ATLANTIC</text><text x="490" y="585">55°S</text><text x="490" y="145">35°S</text>';
  const path = points.map((p) => p.join(",")).join(" ");
  if (gpsOff) {
    for (const [sigma, color] of [
      [result.sql_rad, "#ffca70"],
      [result.ghz_rad, "#64d8cd"],
    ]) {
      const capped = Math.min(sigma, 0.45),
        dx = end[0] - start[0],
        dy = end[1] - start[1],
        len = Math.hypot(dx, dy),
        nx = -dy / len,
        ny = dx / len;
      const left = points.map((p, i) => [
        p[0] + (nx * len * Math.tan(capped) * i) / 40,
        p[1] + (ny * len * Math.tan(capped) * i) / 40,
      ]);
      const right = points
        .map((p, i) => [
          p[0] - (nx * len * Math.tan(capped) * i) / 40,
          p[1] - (ny * len * Math.tan(capped) * i) / 40,
        ])
        .reverse();
      s += `<polygon points="${[...left, ...right].map((p) => p.join(",")).join(" ")}" fill="${color}" fill-opacity=".13" stroke="${color}" stroke-width="1.5"/>`;
    }
  }
  s += `<polyline points="${path}" fill="none" stroke="#e6f4f3" stroke-width="2" stroke-dasharray="5 7"/>`;
  for (const [p, name, labelX] of [
    [start, "Buenos Aires", start[0] + 15],
    [end, "Ushuaia", end[0] + 17],
  ])
    s += `<circle cx="${p[0]}" cy="${p[1]}" r="5" fill="#64d8cd"/><text x="${labelX}" y="${p[1] - 12}" style="fill:#e6f4f3;font-size:17px">${name}</text>`;
  const middle = route[20];
  s += `<rect x="370" y="440" width="235" height="82" rx="3" fill="#071f32"/><text x="385" y="465">Earth's field, midpoint</text><text x="385" y="494" style="fill:#64d8cd;font-size:24px">${middle.field_ut.toFixed(2)} μT</text><text x="45" y="636">${gpsOff ? "GPS absent · uncertainty projected" : "GPS present · cut signal to reveal the corridor"}${gpsOff && Math.max(result.sql_rad, result.ghz_rad) > 0.45 ? " · display capped at 0.45 rad" : ""}</text>`;
  $("map").innerHTML = s;
}
function render(d) {
  result = d;
  $("probesValue").textContent = d.params.n;
  $("noiseValue").textContent = d.params.eta.toFixed(2);
  $("gain").textContent = number(d.gain) + "×";
  $("gain").style.color = d.gain >= 1 ? "var(--mint)" : "var(--amber)";
  $("sql").textContent = number(d.sql_rad, 4) + " rad";
  $("ghz").textContent = number(d.ghz_rad, 4) + " rad";
  $("resources").textContent = d.resource_interactions.toLocaleString();
  $("verdict").textContent =
    d.gain > 1.001
      ? "Entanglement buys more local precision at this noise level."
      : d.gain < 0.999
        ? "The independent probes win. Entanglement is too fragile here."
        : "The two preparations offer the same local precision.";
  $("crossing").textContent =
    d.crossing === null
      ? "One probe: the two preparations are identical."
      : `Equal precision at η = ${number(d.crossing, 3)}. Equal resources, independent noise, fixed interrogation time.`;
  chart(
    $("fringes"),
    [
      {
        color: "#ffca70",
        values: d.phase_curve.map((p) => [p.phase, p.independent]),
      },
      { color: "#64d8cd", values: d.phase_curve.map((p) => [p.phase, p.ghz]) },
    ],
    {
      xmin: -Math.PI,
      xmax: Math.PI,
      xlabel: "Phase (rad)",
      ylabel: "Response probability",
    },
  );
  chart(
    $("noisePlot"),
    [
      { color: "#64d8cd", values: d.noise_curve.map((p) => [p.eta, p.gain]) },
      {
        color: "#ffca70",
        values: [
          [0, 1],
          [1, 1],
        ],
        dash: true,
      },
    ],
    {
      ymax: Math.max(1.2, Math.sqrt(d.params.n)),
      xlabel: "Independent dephasing η",
      ylabel: "Precision gain (×)",
    },
  );
  drawMap();
}
const refresh = () => api.update(params(), render);
for (const id of ["probes", "noise", "shots"])
  $(id).addEventListener("input", refresh);
$("gps").onclick = () => {
  gpsOff = !gpsOff;
  $("gps").setAttribute("aria-pressed", gpsOff);
  $("gps").textContent = gpsOff ? "Restore GPS" : "Cut the GPS signal";
  $("gpsLabel").textContent = gpsOff ? "GPS signal lost" : "GPS available";
  $("gpsLabel").classList.toggle("cut", gpsOff);
  drawMap();
};
$("breakSensor").onclick = () => {
  if (Number($("probes").value) === 1) $("probes").value = 4;
  const n = Number($("probes").value);
  $("noise").value = Math.min(0.8, Math.log(n) / (2 * (n - 1)) + 0.15);
  refresh();
};
async function bird() {
  try {
    const d = await api.py(
      "radical",
      JSON.stringify({ field_ut: 26, anisotropy: isotropic ? 0 : 1 }),
    );
    chart(
      $("birdPlot"),
      [{ color: "#64d8cd", values: d.curve.map((p) => [p.angle, p.yield]) }],
      {
        xmin: 0,
        xmax: 180,
        ymin: 0.2,
        ymax: 1,
        xlabel: "Field angle (degrees)",
        ylabel: "Integrated singlet yield",
      },
    );
    $("birdStatus").textContent =
      `26 μT static field · directional contrast ${number(d.contrast, 3)} · Larmor ${number(d.larmor_mhz, 3)} MHz. ${isotropic ? "Isotropic coupling removes the directional signal." : "Anisotropy creates the angular response."}`;
  } catch (e) {
    $("birdStatus").textContent = "Molecular experiment failed: " + e.message;
  }
}
$("isotropic").onclick = () => {
  isotropic = !isotropic;
  $("isotropic").setAttribute("aria-pressed", isotropic);
  $("isotropic").textContent = isotropic
    ? "Restore the directional coupling"
    : "Remove the directional coupling";
  bird();
};
const story = [
  "You are southbound over Patagonia. Cut GPS to reveal the uncertainty hidden by the position fix.",
  "Use four entangled probes. At low noise, their local phase precision beats four independent probes at the same resource budget.",
  "Increase dephasing. The green instrument loses its advantage. A sensor that wins on paper can lose in the field.",
  "Now remove the directional coupling in the molecule below. The compass response goes flat. Two different quantum mechanisms, two falsifiable experiments.",
];
$("story").onclick = () => {
  $("storyText").hidden = false;
  $("storyText").textContent = story[storyStep];
  if (storyStep === 0 && !gpsOff) $("gps").click();
  if (storyStep === 1) {
    $("probes").value = 4;
    $("noise").value = 0.03;
    refresh();
  }
  if (storyStep === 2) $("breakSensor").click();
  if (storyStep === 3) {
    $("birdPlot").scrollIntoView({ block: "center" });
  }
  storyStep = (storyStep + 1) % story.length;
  $("story").textContent = storyStep ? "Next mission step" : "Replay mission";
};
api.wireAudit(params);
refresh();
bird();
