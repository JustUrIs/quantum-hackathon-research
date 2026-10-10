"""All numerical results originate here; JS only renders them.

Fixed interrogation time, independent phase-flip noise with coherence exp(-eta).
No claim of navigation capability or optimal frequency estimation under noise.
"""

import json
import math
from functools import lru_cache
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, SparsePauliOp


def encode(obj):
    return json.dumps(obj, allow_nan=False)


@lru_cache(maxsize=1)
def route():
    with open("data/route.json", encoding="utf-8") as f:
        return json.load(f)


def ramsey(n, phase, ghz=True):
    qc = QuantumCircuit(n)
    if ghz:
        qc.h(0)
        for i in range(1, n):
            qc.cx(0, i)
    else:
        qc.h(range(n))
    for i in range(n):
        qc.rz(phase, i)
    qc.h(range(n))
    return qc


def precision(n, eta, shots=256):
    """Local Cramer-Rao bounds at each protocol's own quadrature."""
    v = math.exp(-eta)
    independent = 1 / math.sqrt(shots * n * v * v)
    entangled = 1 / math.sqrt(shots * n * n * v ** (2 * n))
    return independent, entangled


def evaluate(params="{}"):
    p = json.loads(params)
    n = int(p.get("n", 4))
    eta = float(p.get("eta", 0.08))
    shots = int(p.get("shots", 256))
    if n not in range(1, 7) or not 0 <= eta <= 1 or not 16 <= shots <= 4096:
        raise ValueError("Use 1–6 probes, noise 0–1, and 16–4096 repetitions")
    sql, ghz = precision(n, eta, shots)
    points = []
    for x in np.linspace(-math.pi, math.pi, 121):
        points.append(
            {
                "phase": float(x),
                "independent": (1 + math.exp(-eta) * math.cos(x)) / 2,
                "ghz": (1 + math.exp(-n * eta) * math.cos(n * x)) / 2,
            }
        )
    crossing = math.log(n) / (2 * (n - 1)) if n > 1 else None
    curves = [
        {"eta": float(e), "gain": precision(n, e, shots)[0] / precision(n, e, shots)[1]}
        for e in np.linspace(0, 1, 81)
    ]
    # Phase-to-heading gain of one is an explicit teaching assumption, not calibration.
    return encode(
        {
            "params": {"n": n, "eta": eta, "shots": shots},
            "sql_rad": sql,
            "ghz_rad": ghz,
            "gain": sql / ghz,
            "crossing": crossing,
            "phase_curve": points,
            "noise_curve": curves,
            "random_fisher": 0,
            "resource_interactions": n * shots,
            "route": route(),
            "origin": "Analytical dephasing model; Qiskit circuit checked independently",
        }
    )


def _pauli(label):
    return SparsePauliOp.from_list([(label, 1)]).to_matrix()


@lru_cache(maxsize=32)
def radical_curve(field_ut=35.0, anisotropy=1.0):
    """3-spin toy radical pair, static field, one spin-1/2 nucleus, equal decay rates.

    Angular units rad/us. Initial electron singlet and maximally mixed nucleus.
    Exact exponential lifetime integration in Hamiltonian eigenbasis.
    """
    omega = 2 * np.pi * 0.028024951 * field_ut
    k = 1.0  # inverse microsecond, illustrative lifetime
    initial = []
    for nuclear in (0, 1):
        qc = QuantumCircuit(3)
        qc.x(1)
        qc.h(0)
        qc.cx(0, 1)
        qc.z(0)
        if nuclear:
            qc.x(2)
        initial.append(Statevector.from_instruction(qc).data)
    rho = sum(np.outer(s, s.conj()) for s in initial) / 2
    singlet = 2 * rho
    results = []
    for angle in range(0, 181, 5):
        t = math.radians(angle)
        h = (
            omega
            / 2
            * (
                math.sin(t) * (_pauli("IIX") + _pauli("IXI"))
                + math.cos(t) * (_pauli("IIZ") + _pauli("IZI"))
            )
        )
        h += (
            2
            * np.pi
            * (
                0.2 * _pauli("XIX")
                + 0.2 * _pauli("YIY")
                + (0.2 + anisotropy) * _pauli("ZIZ")
            )
            / 4
        )
        e, u = np.linalg.eigh(h)
        rh = u.conj().T @ rho @ u
        pr = u.conj().T @ singlet @ u
        integral = k / (k + 1j * (e[:, None] - e[None, :]))
        val = float(np.real(np.sum(pr.T * rh * integral)))
        results.append({"angle": angle, "yield": val})
    return results


def radical(params="{}"):
    p = json.loads(params)
    field = float(p.get("field_ut", 35))
    anisotropy = float(p.get("anisotropy", 1))
    if not 10 <= field <= 70 or not 0 <= anisotropy <= 2:
        raise ValueError("Field or anisotropy outside toy model range")
    curve = radical_curve(round(field, 2), round(anisotropy, 2))
    return encode(
        {
            "curve": curve,
            "contrast": max(x["yield"] for x in curve) - min(x["yield"] for x in curve),
            "larmor_mhz": 0.028024951 * field,
            "origin": "Exact 3-spin toy Hamiltonian, 1 us lifetime, mixed nucleus; no RF or biological validation",
        }
    )


def audit_circuit(params="{}"):
    # Ideal sensor transfer functions; UI noise slider is NOT provider calibration.
    p = json.loads(params)
    n = int(p.get("n", 4))
    if n not in range(1, 7):
        raise ValueError("Audit supports 1–6 probes")
    phase = 0.23
    qc = QuantumCircuit(2 * n, 2 * n)
    qc.compose(ramsey(n, phase, True), range(n), inplace=True)
    qc.compose(ramsey(n, phase, False), range(n, 2 * n), inplace=True)
    qc.measure(range(2 * n), range(2 * n))
    return transpile(qc, basis_gates=["rx", "ry", "rz", "cx"], optimization_level=1)


def _wilson(k, total):
    z = 1.95996398454
    v = k / total
    den = 1 + z * z / total
    mid = (v + z * z / (2 * total)) / den
    half = z * math.sqrt(v * (1 - v) / total + z * z / (4 * total * total)) / den
    return [mid - half, mid + half]


def ingest_audit(raw, params="{}"):
    counts = json.loads(raw)
    n = int(json.loads(params).get("n", 4))
    total = sum(counts.values())
    if total <= 0:
        raise ValueError("Backend returned no shots")
    even = sum(
        v
        for b, v in counts.items()
        if (int(b.replace(" ", ""), 2) & ((1 << n) - 1)).bit_count() % 2 == 0
    )
    zeros = sum(
        v for b, v in counts.items() if not (int(b.replace(" ", ""), 2) >> n) & 1
    )
    return encode(
        {
            "shots": total,
            "n": n,
            "phase": 0.23,
            "ghz_even": even / total,
            "ghz_expected": (1 + math.cos(n * 0.23)) / 2,
            "ghz_ci95": _wilson(even, total),
            "independent_zero": zeros / total,
            "independent_expected": (1 + math.cos(0.23)) / 2,
            "independent_ci95": _wilson(zeros, total),
            "counts": counts,
            "scope": "Fixed phase transfer check; not a measured sensitivity or navigation benchmark",
        }
    )
