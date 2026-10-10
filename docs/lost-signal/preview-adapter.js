// Public, network-free reference preview. Never impersonates a live Qiskit/QPU run.
import { fixtures } from "./fixtures.js";
const origin =
  "Browser reference preview: analytical JavaScript or precomputed Qiskit data. No Python/QPU runs in this page.";
const wrap = (f) => ({
  callPromising: async (raw) =>
    JSON.stringify(await f(JSON.parse(raw || "{}"))),
});
const precision = (n, eta, m) => [
  1 / Math.sqrt(m * n * Math.exp(-2 * eta)),
  1 / Math.sqrt(m * n * n * Math.exp(-2 * n * eta)),
];
function sensing(p) {
  const n = Number(p.n ?? 4),
    eta = Number(p.eta ?? 0.08),
    shots = Number(p.shots ?? 256);
  const [sql, ghz] = precision(n, eta, shots);
  return {
    params: { n, eta, shots },
    sql_rad: sql,
    ghz_rad: ghz,
    gain: sql / ghz,
    crossing: n > 1 ? Math.log(n) / (2 * (n - 1)) : null,
    resource_interactions: n * shots,
    route: fixtures.route,
    random_fisher: 0,
    origin,
    phase_curve: Array.from({ length: 121 }, (_, j) => {
      const phase = -Math.PI + (2 * Math.PI * j) / 120;
      return {
        phase,
        independent: (1 + Math.exp(-eta) * Math.cos(phase)) / 2,
        ghz: (1 + Math.exp(-n * eta) * Math.cos(n * phase)) / 2,
      };
    }),
    noise_curve: Array.from({ length: 81 }, (_, j) => {
      const eta = j / 80,
        [a, b] = precision(n, eta, shots);
      return { eta, gain: a / b };
    }),
  };
}
function sequence(theta, first, second, info, reverse = false) {
  const r = Math.PI / 180,
    a = Math.cos(((theta - first) * r) / 2) ** 2,
    c = Math.cos(((first + info - second) * r) / 2) ** 2;
  const row = [a * c, a * (1 - c), (1 - a) * (1 - c), (1 - a) * c];
  return reverse ? [row[0], row[2], row[1], row[3]] : row;
}
const qq = (ab, ba) => ab[1] + ab[2] - ba[1] - ba[2];
function classical(ab, ba) {
  const pa = ab[0] + ab[1],
    pb = ba[0] + ba[2],
    safe = (x, y) => (y ? x / y : 0.5);
  const parameters = {
    A_first_yes: pa,
    B_after_Ayes: safe(ab[0], pa),
    B_after_Ano: safe(ab[2], 1 - pa),
    B_first_yes: pb,
    A_after_Byes: safe(ba[0], pb),
    A_after_Bno: safe(ba[1], 1 - pb),
  };
  const c = parameters,
    ab2 = [
      pa * c.B_after_Ayes,
      pa * (1 - c.B_after_Ayes),
      (1 - pa) * c.B_after_Ano,
      (1 - pa) * (1 - c.B_after_Ano),
    ];
  const ba2 = [
    pb * c.A_after_Byes,
    (1 - pb) * c.A_after_Bno,
    pb * (1 - c.A_after_Byes),
    (1 - pb) * (1 - c.A_after_Bno),
  ];
  return {
    parameters,
    ab: ab2,
    ba: ba2,
    qq: qq(ab2, ba2),
    max_error: Math.max(
      ...ab.concat(ba).map((v, i) => Math.abs(v - ab2.concat(ba2)[i])),
    ),
  };
}
function ordering(p) {
  const theta = Number(p.theta ?? 35),
    angle = Number(p.angle ?? 70),
    info = Number(p.info ?? 0);
  const ab = sequence(theta, 0, angle, info),
    ba = sequence(theta, angle, 0, info, true);
  return {
    params: { theta, angle, info },
    ab,
    ba,
    qq: qq(ab, ba),
    a_first: ab[0] + ab[1],
    a_second: ba[0] + ba[1],
    b_first: ba[0] + ba[2],
    b_second: ab[0] + ab[2],
    commutator_norm: Math.abs(Math.sin((angle * Math.PI) / 180)) / 2,
    classical: classical(ab, ba),
    polls: fixtures.polls,
    origin,
  };
}
function factoring(p) {
  const n = Number(p.n ?? 15),
    a = Number(p.a ?? 2),
    bits = Number(p.bits ?? 6),
    mix = Number(p.mix ?? 0);
  const base = fixtures.experiments[`${n}:${a}:${bits}`];
  if (!base)
    throw new Error(
      "This configuration has no verified reference fixture. Run it in the Python/Qollab project.",
    );
  const d = structuredClone(base),
    dist = d.probabilities.map((v) => (1 - mix) * v + mix / 2 ** bits);
  return {
    ...d,
    params: { n, a, bits, mix },
    display_probabilities: dist,
    display_success: d.winning_bins.reduce((s, i) => s + dist[i], 0),
    origin,
    fixture_qiskit_version: fixtures.qiskit_version,
  };
}
export const evaluate = wrap((p) =>
  fixtures.project === "lost-signal"
    ? sensing(p)
    : fixtures.project === "order"
      ? ordering(p)
      : factoring(p),
);
export const radical = wrap((p) => {
  if (p.field_ut !== 26 || ![0, 1].includes(p.anisotropy))
    throw new Error(
      "Only the displayed 26 μT reference experiment is included.",
    );
  return { ...fixtures.radical[p.anisotropy], origin };
});
// Abramowitz-Stegun approximation. Absolute erfc error <~1.5e-7.
function erfc(x) {
  const t = 1 / (1 + 0.3275911 * x);
  return Math.min(
    1,
    ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) *
      t +
      0.254829592) *
      t *
      Math.exp(-x * x),
  );
}
export const audit_counts = wrap((d) => {
  for (const row of [d.ab, d.ba])
    if (
      !Array.isArray(row) ||
      row.length !== 4 ||
      !row.every((v) => Number.isInteger(v) && v >= 0 && v <= 1e7) ||
      row.reduce((a, b) => a + b, 0) < 2
    )
      throw new Error(
        "Supply four nonnegative integer counts per order; at least two responses per group.",
      );
  const na = d.ab.reduce((a, b) => a + b, 0),
    nb = d.ba.reduce((a, b) => a + b, 0),
    pa = d.ab.map((x) => x / na),
    pb = d.ba.map((x) => x / nb),
    qa = pa[1] + pa[2],
    qb = pb[1] + pb[2],
    q = qa - qb;
  const se = Math.sqrt((qa * (1 - qa)) / na + (qb * (1 - qb)) / nb),
    pooled = (d.ab[1] + d.ab[2] + d.ba[1] + d.ba[2]) / (na + nb),
    ns = Math.sqrt(pooled * (1 - pooled) * (1 / na + 1 / nb));
  const aa = pa[0] + pa[1],
    bb = pb[0] + pb[1],
    delta = bb - aa,
    dse = Math.sqrt((aa * (1 - aa)) / na + (bb * (1 - bb)) / nb);
  const ci = (v, s) => [Math.max(-1, v - 1.96 * s), Math.min(1, v + 1.96 * s)];
  return {
    counts: d,
    ab: pa,
    ba: pb,
    n_ab: na,
    n_ba: nb,
    qq: q,
    qq_se: se,
    qq_ci95_normal: ci(q, se),
    qq_p_normal: ns ? erfc(Math.abs(q / ns) / Math.SQRT2) : 1,
    a_order_effect: delta,
    a_effect_ci95_normal: ci(delta, dse),
    normal_approximation_adequate:
      Math.min(
        na * pooled,
        na * (1 - pooled),
        nb * pooled,
        nb * (1 - pooled),
      ) >= 5,
    assumptions:
      "Independent randomized groups; unweighted counts; no clustering or repeated respondents. Approximate intervals. Failure to reject QQ is not proof of a quantum mechanism.",
    origin,
  };
});
export const audit_circuit = {
  callPromising: async () => {
    throw new Error(
      "Live backend execution is available in the downloadable Qollab project.",
    );
  },
};
export const ingest_audit = audit_circuit;

const button = document.getElementById("runBackend");
button.disabled = true;
button.textContent = "Live backend runs in the Qollab version";
document.getElementById("auditStatus").textContent =
  "This is the public reference preview. No backend job is sent. Download the Qollab package to execute the circuit.";
