import json
import math
from functools import lru_cache
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector


def encode(obj):
    return json.dumps(obj, allow_nan=False)


@lru_cache(maxsize=1)
def polls():
    with open("data/polls.json", encoding="utf-8") as f:
        return json.load(f)


def sequence(theta, first, second, intervening=0):
    """q0 belief; q1 first answer; q2 second answer. 0 means yes.

    Record outcomes coherently; do not erase records. Final measurement gives
    exactly the sequential projective probabilities after tracing the system.
    """
    qc = QuantumCircuit(3)
    qc.ry(theta, 0)
    qc.ry(-first, 0)
    qc.cx(0, 1)
    qc.ry(first, 0)
    qc.ry(intervening, 0)
    qc.ry(-second, 0)
    qc.cx(0, 2)
    qc.ry(second, 0)
    return qc


def canonical_probs(qc, reverse=False):
    out = [0.0] * 4  # AyBy, AyBn, AnBy, AnBn
    for i, v in enumerate(Statevector.from_instruction(qc).probabilities()):
        first, second = (i >> 1) & 1, (i >> 2) & 1
        a, b = (second, first) if reverse else (first, second)
        out[2 * a + b] += float(v)
    return out


def qq(ab, ba):
    return ab[1] + ab[2] - ba[1] - ba[2]


def audit_counts(raw):
    """Independent randomized AB/BA respondent groups, canonical A/B cells.

    Delta-method normal intervals and pooled two-proportion QQ test. These
    do not handle survey weights, repeated respondents or cluster sampling.
    """
    d = json.loads(raw)
    ab, ba = d.get("ab"), d.get("ba")
    for row in (ab, ba):
        if (
            not isinstance(row, list)
            or len(row) != 4
            or not all(type(x) is int and 0 <= x <= 10000000 for x in row)
        ):
            raise ValueError(
                "Supply four nonnegative integer counts per order, at most 10 million per cell"
            )
        if sum(row) < 2:
            raise ValueError("Each order needs at least two responses")
    na, nb = sum(ab), sum(ba)
    pa, pb = [x / na for x in ab], [x / nb for x in ba]
    qa, qb = pa[1] + pa[2], pb[1] + pb[2]
    q = qa - qb
    se = math.sqrt(qa * (1 - qa) / na + qb * (1 - qb) / nb)
    pooled = (ab[1] + ab[2] + ba[1] + ba[2]) / (na + nb)
    null_se = math.sqrt(pooled * (1 - pooled) * (1 / na + 1 / nb))
    pv = math.erfc(abs(q / null_se) / math.sqrt(2)) if null_se else 1.0
    aa, bb = pa[0] + pa[1], pb[0] + pb[1]
    delta = bb - aa
    dse = math.sqrt(aa * (1 - aa) / na + bb * (1 - bb) / nb)
    expected = [na * pooled, na * (1 - pooled), nb * pooled, nb * (1 - pooled)]
    return encode(
        {
            "counts": d,
            "ab": pa,
            "ba": pb,
            "n_ab": na,
            "n_ba": nb,
            "qq": q,
            "qq_se": se,
            "qq_ci95_normal": [max(-1, q - 1.96 * se), min(1, q + 1.96 * se)],
            "qq_p_normal": pv,
            "a_order_effect": delta,
            "a_effect_ci95_normal": [
                max(-1, delta - 1.96 * dse),
                min(1, delta + 1.96 * dse),
            ],
            "normal_approximation_adequate": min(expected) >= 5,
            "assumptions": "Independent randomized groups; unweighted counts; no clustering or repeated respondents. Approximate intervals. Failure to reject QQ is not proof of a quantum mechanism.",
        }
    )


def contextual(ab, ba):
    """Classical model with an order bit and stochastic answer transitions.

    A constructive counterexample to 'QQ proves uniquely quantum cognition'.
    It fits the displayed distributions; this is not out-of-sample prediction.
    """
    pa = ab[0] + ab[1]
    pb = ba[0] + ba[2]
    safe = lambda num, den: num / den if den else 0.5
    transitions = {
        "A_first_yes": pa,
        "B_after_Ayes": safe(ab[0], pa),
        "B_after_Ano": safe(ab[2], 1 - pa),
        "B_first_yes": pb,
        "A_after_Byes": safe(ba[0], pb),
        "A_after_Bno": safe(ba[1], 1 - pb),
    }
    p = transitions
    ab2 = [
        pa * p["B_after_Ayes"],
        pa * (1 - p["B_after_Ayes"]),
        (1 - pa) * p["B_after_Ano"],
        (1 - pa) * (1 - p["B_after_Ano"]),
    ]
    ba2 = [
        pb * p["A_after_Byes"],
        (1 - pb) * p["A_after_Bno"],
        pb * (1 - p["A_after_Byes"]),
        (1 - pb) * (1 - p["A_after_Bno"]),
    ]
    return {
        "parameters": transitions,
        "ab": ab2,
        "ba": ba2,
        "qq": qq(ab2, ba2),
        "max_error": max(abs(x - y) for x, y in zip(ab + ba, ab2 + ba2)),
    }


def evaluate(params="{}"):
    p = json.loads(params)
    theta, angle, info = (
        float(p.get(k, d)) for k, d in (("theta", 35), ("angle", 70), ("info", 0))
    )
    if not all(0 <= v <= 180 for v in (theta, angle, info)):
        raise ValueError("Angles must be 0–180 degrees")
    t, a, i = map(math.radians, (theta, angle, info))
    ab = canonical_probs(sequence(t, 0, a, i))
    ba = canonical_probs(sequence(t, a, 0, i), True)
    return encode(
        {
            "params": {"theta": theta, "angle": angle, "info": info},
            "ab": ab,
            "ba": ba,
            "a_first": ab[0] + ab[1],
            "a_second": ba[0] + ba[1],
            "b_first": ba[0] + ba[2],
            "b_second": ab[0] + ab[2],
            "qq": qq(ab, ba),
            "commutator_norm": abs(math.sin(a)) / 2,
            "classical": contextual(ab, ba),
            "polls": polls(),
            "origin": "Exact Qiskit statevectors of deferred projective measurements; synthetic model",
        }
    )


def audit_circuit(params="{}"):
    p = json.loads(params)
    t, a, i = map(
        math.radians,
        (float(p.get("theta", 35)), float(p.get("angle", 70)), float(p.get("info", 0))),
    )
    qc = QuantumCircuit(6, 4)
    qc.compose(sequence(t, 0, a, i), [0, 1, 2], inplace=True)
    qc.compose(sequence(t, a, 0, i), [3, 4, 5], inplace=True)
    qc.measure([1, 2, 4, 5], [0, 1, 2, 3])
    return transpile(qc, basis_gates=["rx", "ry", "rz", "cx"], optimization_level=1)


def ingest_audit(raw, params="{}"):
    counts = json.loads(raw)
    total = sum(counts.values())
    if total <= 0:
        raise ValueError("Backend returned no shots")
    ab, ba = [0.0] * 4, [0.0] * 4
    paired = []
    for key, count in counts.items():
        b = int(key.replace(" ", ""), 2)
        a1, b2, b1, a2 = ((b >> k) & 1 for k in range(4))
        ab[2 * a1 + b2] += count / total
        ba[2 * a2 + b1] += count / total
        paired.append((int(a1 != b2) - int(a2 != b1), count))
    q = qq(ab, ba)
    # Retain within-shot covariance across packed registers, even under provider noise.
    variance = sum(c * (v - q) ** 2 for v, c in paired) / max(1, total - 1)
    se = math.sqrt(variance / total)
    return encode(
        {
            "shots": total,
            "ab": ab,
            "ba": ba,
            "qq": q,
            "qq_se": se,
            "qq_ci95_normal": [max(-1, q - 1.96 * se), min(1, q + 1.96 * se)],
            "counts": counts,
            "scope": "Circuit sampling, not human responses; normal CI is approximate",
        }
    )
