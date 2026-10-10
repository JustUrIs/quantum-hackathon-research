import json
import math
from functools import lru_cache
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate, StatePreparation
from qiskit.quantum_info import Statevector


def encode(obj):
    return json.dumps(obj, allow_nan=False)


def _validate(n, a, bits):
    if (
        n not in (15, 21, 33, 35)
        or not 2 <= a < n
        or math.gcd(n, a) != 1
        or bits not in (5, 6, 7, 8)
    ):
        raise ValueError("Use N in 15,21,33,35, a coprime base, and 5–8 phase bits")


def _swap_basis(qc, x, y, work, control):
    """Swap two basis states by a Gray path, with an external control.

    Each adjacent transposition is one multi-controlled X. Reverse all but
    the last edge so intermediate states are restored.
    """
    path = [x]
    for b in range(len(work)):
        if (x ^ y) >> b & 1:
            path.append(path[-1] ^ (1 << b))
    edges = list(zip(path, path[1:]))
    for u, v in edges + edges[-2::-1]:
        target = (u ^ v).bit_length() - 1
        other = [j for j in range(len(work)) if j != target]
        zero = [work[j] for j in other if not (u >> j & 1)]
        if zero:
            qc.x(zero)
        qc.mcx([control] + [work[j] for j in other], work[target])
        if zero:
            qc.x(zero)


def modular_multiply(qc, multiplier, n, work, control):
    """Permutation y -> multiplier*y mod N for y<N; identity outside N.

    Inputs: public N and multiplier only. No factor or period input. This
    truth-table synthesis is exponential in bit width and is a SMALL-N tool.
    """
    # Public algebraic structure: modulo 2**w-1, multiplication by 2 is a
    # cyclic bit rotation. This optimization neither computes nor receives r.
    if (
        n == (1 << len(work)) - 1
        and multiplier > 0
        and multiplier & (multiplier - 1) == 0
    ):
        for _ in range(multiplier.bit_length() - 1):
            for j in range(1, len(work)):
                qc.cswap(control, work[0], work[j])
        return
    seen = set()
    for start in range(n):
        if start in seen:
            continue
        cycle, y = [], start
        while y not in seen:
            seen.add(y)
            cycle.append(y)
            y = multiplier * y % n
        # Applying (c0,c1), then (c0,c2), ... realizes the forward cycle.
        for y in cycle[1:]:
            _swap_basis(qc, cycle[0], y, work, control)


@lru_cache(maxsize=16)
def genuine(n=15, a=2, bits=6):
    _validate(n, a, bits)
    width = (n - 1).bit_length()
    qc = QuantumCircuit(bits + width, name=f"order_{a}_mod_{n}")
    qc.h(range(bits))
    qc.x(bits)
    work = list(range(bits, bits + width))
    for j in range(bits):
        modular_multiply(qc, pow(a, 1 << j, n), n, work, j)
    qc.append(QFTGate(bits).inverse(), range(bits))
    return qc


def convergent_denominators(num, den):
    old_p, p, old_q, q = 0, 1, 1, 0
    while den:
        d, rem = divmod(num, den)
        old_p, p = p, d * p + old_p
        old_q, q = q, d * q + old_q
        yield q
        num, den = den, rem


def recover(y, bits, a, n):
    # No trial order search, multiples sweep, or factor oracle in this path.
    if y == 0:
        return None
    for r in convergent_denominators(y, 1 << bits):
        if r > n:
            break
        if r < 2 or r % 2 or pow(a, r, n) != 1:
            continue
        root = pow(a, r // 2, n)
        for f in (math.gcd(root - 1, n), math.gcd(root + 1, n)):
            if 1 < f < n:
                return {"period_candidate": r, "factors": sorted([f, n // f])}
    return None


def classical_period(a, n):
    # Intentionally isolated: used ONLY by the confessed pre-solved imitation.
    r, x = 0, 1
    while True:
        x = x * a % n
        r += 1
        if x == 1:
            return r


def period_distribution(r, bits):
    size = 1 << bits
    # Mixture of uniform cosets, analytically Fourier transformed.
    result = np.zeros(size)
    for residue in range(r):
        vec = np.zeros(size, complex)
        vec[residue::r] = 1 / math.sqrt(size)
        result += np.abs(np.fft.fft(vec, norm="ortho")) ** 2
    return result


@lru_cache(maxsize=16)
def compiled(n, a, bits):
    return transpile(
        genuine(n, a, bits),
        basis_gates=["rx", "ry", "rz", "cx"],
        optimization_level=1,
        seed_transpiler=7,
    )


@lru_cache(maxsize=16)
def experiment(n, a, bits):
    qc = compiled(n, a, bits)
    prob = Statevector.from_instruction(qc).probabilities(qargs=list(range(bits)))
    r = classical_period(a, n)
    fake = QuantumCircuit(bits)
    fake.append(StatePreparation(np.sqrt(period_distribution(r, bits))), range(bits))
    fake = transpile(
        fake,
        basis_gates=["rx", "ry", "rz", "cx"],
        optimization_level=1,
        seed_transpiler=7,
    )
    wins = [recover(y, bits, a, n) is not None for y in range(1 << bits)]
    gcd_wins = sum(1 < math.gcd(k, n) < n for k in range(2, n))
    divisors_tried = []
    for k in range(2, math.isqrt(n) + 1):
        divisors_tried.append(k)
        if n % k == 0:
            break
    return {
        "n": n,
        "a": a,
        "bits": bits,
        "probabilities": prob.tolist(),
        "genuine_success": float(sum(p for p, w in zip(prob, wins) if w)),
        "random_phase_success": sum(wins) / len(wins),
        "random_gcd_success": gcd_wins / (n - 2),
        "trial_division_checks": len(divisors_tried),
        "trial_division_factors": [divisors_tried[-1], n // divisors_tried[-1]],
        "genuine": {
            "qubits": qc.num_qubits,
            "cx": int(qc.count_ops().get("cx", 0)),
            "depth": qc.depth(),
        },
        "presolved": {
            "qubits": fake.num_qubits,
            "cx": int(fake.count_ops().get("cx", 0)),
            "depth": fake.depth(),
            "period_supplied": r,
        },
        "histogram_distance": float(
            np.max(np.abs(prob - period_distribution(r, bits)))
        ),
        "winning_bins": [y for y, w in enumerate(wins) if w],
    }


def evaluate(params="{}"):
    p = json.loads(params)
    n, a, bits = (int(p.get(k, d)) for k, d in (("n", 15), ("a", 2), ("bits", 6)))
    _validate(n, a, bits)
    result = dict(experiment(n, a, bits))
    mix = float(p.get("mix", 0))
    if not 0 <= mix <= 1:
        raise ValueError("Readout mixture must be 0–1")
    dist = [(1 - mix) * v + mix / (1 << bits) for v in result["probabilities"]]
    result.update(
        {
            "params": {"n": n, "a": a, "bits": bits, "mix": mix},
            "display_probabilities": dist,
            "display_success": sum(dist[i] for i in result["winning_bins"]),
            "origin": "Exact Qiskit statevector; optional uniform output mixture is an illustrative readout ablation, not IonQ noise",
        }
    )
    return encode(result)


def audit_circuit(params="{}"):
    p = json.loads(params)
    n, a, bits = (int(p.get(k, d)) for k, d in (("n", 15), ("a", 2), ("bits", 6)))
    # Do NOT call experiment(): genuine circuit has no dependency on period oracle.
    qc = compiled(n, a, bits).copy()
    from qiskit import ClassicalRegister

    qc.add_register(ClassicalRegister(bits, "phase"))
    qc.measure(range(bits), range(bits))
    return qc


def ingest_audit(raw, params="{}"):
    p = json.loads(params)
    n, a, bits = (int(p.get(k, d)) for k, d in (("n", 15), ("a", 2), ("bits", 6)))
    counts = json.loads(raw)
    total = sum(counts.values())
    if total <= 0:
        raise ValueError("Backend returned no shots")
    success = 0
    evidence = []
    for key, c in counts.items():
        y = int(key.replace(" ", ""), 2)
        found = recover(y, bits, a, n)
        if found:
            success += c
            evidence.append({"y": y, "count": c, **found})
    return encode(
        {
            "shots": total,
            "successes": success,
            "rate": success / total,
            "evidence": evidence,
            "counts": counts,
            "params": p,
            "scope": "Small-N order finding; no cryptographic key attack or resource extrapolation",
        }
    )
