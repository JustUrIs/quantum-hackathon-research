"""IMPOSTOR referees: theorem-backed tests that a classical faker cannot pass.

Each level builds ONE QuantumCircuit (IonQ simulator accepts one job per run)
and scores both the quantum device and a classical impostor on the same inputs.
"""
from __future__ import annotations

import itertools
import math

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, random_clifford


# ---------------------------------------------------------------- level 1: CHSH
# Referee sends x to Alice, y to Bob (random bits). They win if a XOR b == x AND y.
# Classical ceiling: 75%. Quantum (shared Bell pair): cos^2(pi/8) ~ 85.4%.

CHSH_CLASSICAL_MAX = 0.75
CHSH_QUANTUM_MAX = math.cos(math.pi / 8) ** 2

_ALICE_ANGLE = {0: 0.0, 1: math.pi / 2}
_BOB_ANGLE = {0: math.pi / 4, 1: -math.pi / 4}


def chsh_circuit(xs: list[int], ys: list[int]) -> QuantumCircuit:
    """One Bell pair per round, measured at the round's angles. 2 qubits per round."""
    rounds = len(xs)
    qc = QuantumCircuit(2 * rounds, 2 * rounds, name="chsh")
    for r, (x, y) in enumerate(zip(xs, ys)):
        a, b = 2 * r, 2 * r + 1
        qc.h(a)
        qc.cx(a, b)
        qc.ry(-_ALICE_ANGLE[x], a)
        qc.ry(-_BOB_ANGLE[y], b)
    qc.measure(range(2 * rounds), range(2 * rounds))
    return qc


def chsh_score(xs, ys, alice_bits, bob_bits) -> float:
    wins = [(a ^ b) == (x & y) for x, y, a, b in zip(xs, ys, alice_bits, bob_bits)]
    return sum(wins) / len(wins)


def chsh_all_classical_strategies():
    """All 16 deterministic strategies (a0,a1,b0,b1). Shared randomness is a mix of these,
    so none can beat the best of them: that is the whole Bell argument."""
    for a0, a1, b0, b1 in itertools.product((0, 1), repeat=4):
        win = sum(((a0, a1)[x] ^ (b0, b1)[y]) == (x & y) for x in (0, 1) for y in (0, 1)) / 4
        yield (a0, a1, b0, b1), win


# ------------------------------------------------------ level 2: magic square
# Mermin-Peres. Alice gets a row r and outputs 3 signs with product +1.
# Bob gets a column c and outputs 3 signs with product -1. Win if they agree on cell (r, c).
# Classical ceiling: 8/9. Quantum (two Bell pairs): 100%.

MAGIC_CLASSICAL_MAX = 8 / 9

# Square of two-qubit Paulis (signs included). Every row multiplies to +I, every column to -I.
MAGIC_SQUARE = [
    [("+", "XI"), ("+", "IX"), ("+", "XX")],
    [("-", "XZ"), ("-", "ZX"), ("+", "YY")],
    [("+", "IZ"), ("+", "ZI"), ("+", "ZZ")],
]


def _measure_pauli(qc: QuantumCircuit, pauli: str, data: list[int], anc: int):
    """Parity measurement of a Pauli string onto an ancilla (pauli[0] acts on data[0])."""
    for p, q in zip(pauli, data):
        if p == "X":
            qc.h(q)
        elif p == "Y":
            qc.sdg(q)
            qc.h(q)
    for p, q in zip(pauli, data):
        if p != "I":
            qc.cx(q, anc)
    for p, q in zip(pauli, data):
        if p == "X":
            qc.h(q)
        elif p == "Y":
            qc.h(q)
            qc.s(q)


def magic_circuit(rows: list[int], cols: list[int]) -> QuantumCircuit:
    """Per round: 4 data qubits (Alice a1 a2, Bob b1 b2) + 2 ancillas each = 8 qubits.
    Each player measures the first two observables of their line; the third is fixed by parity."""
    rounds = len(rows)
    qc = QuantumCircuit(8 * rounds, 4 * rounds, name="magic")
    for k, (r, c) in enumerate(zip(rows, cols)):
        base = 8 * k
        a1, a2, b1, b2 = base, base + 1, base + 2, base + 3
        anc = [base + 4, base + 5, base + 6, base + 7]
        for p, q in ((a1, b1), (a2, b2)):  # two Bell pairs |Phi+>
            qc.h(p)
            qc.cx(p, q)
        for j in range(2):
            _measure_pauli(qc, MAGIC_SQUARE[r][j][1], [a1, a2], anc[j])
        # Bob holds the partner halves. For |Phi+>, measuring P on Bob's side equals P^T on Alice's,
        # so Y picks up a sign: handled in decoding.
        for j in range(2):
            _measure_pauli(qc, MAGIC_SQUARE[j][c][1], [b1, b2], anc[2 + j])
        for j in range(4):
            qc.measure(anc[j], 4 * k + j)
    return qc


def _sign(s: str) -> int:
    return 1 if s == "+" else -1


def magic_decode(rows, cols, bits_per_round) -> tuple[list, list]:
    """bits_per_round: list of 4-bit tuples (alice obs0, alice obs1, bob obs0, bob obs1)."""
    alice, bob = [], []
    for r, c, bits in zip(rows, cols, bits_per_round):
        av = [_sign(MAGIC_SQUARE[r][j][0]) * (1 - 2 * bits[j]) for j in range(2)]
        av.append(av[0] * av[1])  # row product +1
        bv = []
        for j in range(2):
            sign, p = MAGIC_SQUARE[j][c]
            ytwist = (-1) ** p.count("Y")  # transpose of Y is -Y
            bv.append(_sign(sign) * ytwist * (1 - 2 * bits[2 + j]))
        bv.append(-bv[0] * bv[1])  # column product -1
        alice.append(av)
        bob.append(bv)
    return alice, bob


def magic_score(rows, cols, alice, bob) -> float:
    return sum(a[c] == b[r] for r, c, a, b in zip(rows, cols, alice, bob)) / len(rows)


# --------------------------------------------------------- level 3: zip duel
# Distributed XEB (Kretschmer, Grewal, ..., Aaronson 2025, arXiv:2509.07255).
# Alice sends an n-qubit state; Bob applies a random Clifford and measures z.
# Score = 2^n |<z|U|psi>|^2 - 1. Quantum ideal ~1. A classical impostor must send bits instead:
# the paper proves >= 78 bits are needed to reach 0.427 at n=12, best known classical uses ~330.

ZIP_PAPER = {"n": 12, "hardware_xeb": 0.427, "lower_bound_bits": 78, "best_classical_bits": 330}


def brickwork_state_circuit(n: int, layers: int, seed: int) -> QuantumCircuit:
    """Random brickwork with periodic boundary (the wrap-around gate is native on all-to-all ions)."""
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(n, name="alice")
    for layer in range(layers):
        for q in range(n):
            qc.u(*rng.uniform(0, 2 * np.pi, 3), q)
        for q in range(layer % 2, n, 2):
            qc.rzz(rng.uniform(0, 2 * np.pi), q, (q + 1) % n)
    return qc


def zip_circuit(n: int, layers: int, state_seed: int, clifford_seed: int) -> QuantumCircuit:
    qc = QuantumCircuit(n, n, name="zip")
    qc.compose(brickwork_state_circuit(n, layers, state_seed), inplace=True)
    qc.compose(random_clifford(n, seed=clifford_seed).to_circuit(), inplace=True)
    qc.measure(range(n), range(n))
    return qc


def zip_ideal_probs(n: int, layers: int, state_seed: int, clifford_seed: int) -> np.ndarray:
    qc = brickwork_state_circuit(n, layers, state_seed)
    qc.compose(random_clifford(n, seed=clifford_seed).to_circuit(), inplace=True)
    return Statevector(qc).probabilities()


def xeb_from_counts(counts: dict[str, int], probs: np.ndarray, n: int) -> float:
    total = sum(counts.values())
    return sum(2**n * probs[int(z, 2)] * c for z, c in counts.items()) / total - 1


def zip_impostor_state(psi: np.ndarray, k_bits: int, seed: int) -> np.ndarray:
    """Classical impostor: Alice sends k sign bits of projections on shared random vectors;
    Bob rebuilds a guess of the state. (One natural sketch; the theorem bounds ALL strategies.)"""
    rng = np.random.default_rng(seed)
    m = max(1, k_bits // 2)
    R = (rng.normal(size=(m, psi.size)) + 1j * rng.normal(size=(m, psi.size))) / np.sqrt(2)
    proj = R.conj() @ psi
    est = R.T @ (np.sign(proj.real) + 1j * np.sign(proj.imag))
    return est / np.linalg.norm(est)


def magic_all_classical_strategies():
    """Brute force: Alice fixes a +1-product triple per row (4^3), Bob a -1-product triple per column (4^3).
    4,096 deterministic strategies; shared randomness only mixes them. Returns (best_win, count_at_best)."""
    plus = [t for t in itertools.product((1, -1), repeat=3) if t[0] * t[1] * t[2] == 1]
    minus = [t for t in itertools.product((1, -1), repeat=3) if t[0] * t[1] * t[2] == -1]
    best, n_best, total = 0.0, 0, 0
    for A in itertools.product(plus, repeat=3):
        for B in itertools.product(minus, repeat=3):
            total += 1
            w = sum(A[r][c] == B[c][r] for r in range(3) for c in range(3)) / 9
            if w > best + 1e-12:
                best, n_best = w, 1
            elif abs(w - best) < 1e-12:
                n_best += 1
    return best, n_best, total


# ---------------------------------------------------- level 4: precision (GHZ)
# Estimate a tiny phase phi (a field) with N qubits.
# Independent probes: each qubit picks up phi -> error ~ 1/sqrt(N) (standard quantum limit).
# GHZ probe: the N-qubit cat state picks up N*phi -> error ~ 1/N (Heisenberg limit).
# With dephasing, the GHZ coherence decays N times faster: the advantage dies at a crossover.


def ghz_probe_circuit(n: int, phi: float) -> QuantumCircuit:
    qc = QuantumCircuit(n, n, name="ghz")
    qc.h(0)
    for q in range(1, n):
        qc.cx(0, q)
    for q in range(n):
        qc.rz(phi, q)
    for q in range(n - 1, 0, -1):
        qc.cx(0, q)
    qc.h(0)
    qc.measure(range(n), range(n))
    return qc


def independent_probe_circuit(n: int, phi: float) -> QuantumCircuit:
    qc = QuantumCircuit(n, n, name="indep")
    for q in range(n):
        qc.h(q)
        qc.rz(phi, q)
        qc.h(q)
    qc.measure(range(n), range(n))
    return qc


def phase_sensitivity(n: int, dephasing: float = 0.0) -> dict:
    """Analytic slope-based sensitivity (Fisher information per shot) for both strategies,
    with per-qubit dephasing probability `dephasing` (coherence factor (1-2p) per qubit)."""
    c = 1 - 2 * dephasing
    return {
        "independent_fisher": n * c**2,        # n probes, each with visibility c
        "ghz_fisher": (n * c**n) ** 2,         # one probe, phase n*phi, visibility c^n
    }
