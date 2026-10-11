"""IMPOSTOR game engine: the quantum player, the classical impostor and the referee.

Every quantum answer comes from a real Qiskit circuit. During play the circuit is
sampled exactly from its statevector (the circuit a perfect device would run);
the one-job audit in service.py sends the same circuits to the selected backend.
"""
from __future__ import annotations

import itertools
import math
import random

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, Pauli, Statevector, random_clifford


def sample_bits(qc: QuantumCircuit, rng: random.Random) -> list[int]:
    """One shot from the exact statevector of an unmeasured circuit. bits[i] = qubit i."""
    probs = Statevector(qc).probabilities()
    z = rng.choices(range(len(probs)), weights=probs)[0]
    return [(z >> i) & 1 for i in range(qc.num_qubits)]


# =============================================================== level 1: CHSH
# Referee sends bit x to Alice and bit y to Bob. They win if a XOR b == x AND y.

CHSH_CLASSICAL_MAX = 0.75
CHSH_QUANTUM_MAX = math.cos(math.pi / 8) ** 2
CHSH_ALICE_ANGLE = (0.0, math.pi / 2)
CHSH_BOB_ANGLE = (math.pi / 4, -math.pi / 4)


def chsh_pair(x: int, y: int) -> QuantumCircuit:
    """Shared Bell pair; each player rotates by their own setting, then measures Z."""
    qc = QuantumCircuit(2, name=f"chsh_{x}{y}")
    qc.h(0)
    qc.cx(0, 1)
    qc.ry(-CHSH_ALICE_ANGLE[x], 0)
    qc.ry(-CHSH_BOB_ANGLE[y], 1)
    return qc


def chsh_win(x: int, y: int, a: int, b: int) -> bool:
    return (a ^ b) == (x & y)


def chsh_strategy_value(strategy: list[int]) -> float:
    """strategy = [a(x=0), a(x=1), b(y=0), b(y=1)]: exact win probability over the 4 questions."""
    a0, a1, b0, b1 = strategy
    return sum(chsh_win(x, y, (a0, a1)[x], (b0, b1)[y]) for x in (0, 1) for y in (0, 1)) / 4


def chsh_bruteforce() -> dict:
    values = [(s, chsh_strategy_value(list(s))) for s in itertools.product((0, 1), repeat=4)]
    best = max(v for _, v in values)
    return {"tried": len(values), "best": best, "at_best": sum(v == best for _, v in values)}


# ======================================================= level 2: magic square
# Alice gets a row and must answer 3 signs with product +1; Bob gets a column and
# must answer 3 signs with product -1. They win if they agree on the shared cell.

MAGIC_CLASSICAL_MAX = 8 / 9

# Two-qubit observables. Character i acts on qubit i of the player's pair.
# Rows multiply to +I and columns to -I, which is impossible for numbers.
MAGIC_SQUARE = [
    [(+1, "XI"), (+1, "IX"), (+1, "XX")],
    [(-1, "XZ"), (-1, "ZX"), (+1, "YY")],
    [(+1, "IZ"), (+1, "ZI"), (+1, "ZZ")],
]

_CANDIDATE_BASES = {
    "none": [],
    "h0 h1": [("h", 0), ("h", 1)],
    "h1 cx01 h0": [("h", 1), ("cx", 0, 1), ("h", 0)],
    "h0 cx01": [("h", 0), ("cx", 0, 1)],
    "h1 cx10": [("h", 1), ("cx", 1, 0)],
    "cx01 h0": [("cx", 0, 1), ("h", 0)],
}


def _gates_circuit(gates) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    for g in gates:
        getattr(qc, g[0])(*g[1:])
    return qc


def _as_z_string(label: str, basis: QuantumCircuit):
    """If the basis change maps the observable to +-Z..Z, return (sign, qubits) else None."""
    p = Pauli(label[::-1]).evolve(Clifford(basis), frame="s")  # qiskit labels are little-endian
    if p.x.any() or p.phase % 2:
        return None
    return (-1 if p.phase % 4 == 2 else 1), [i for i in range(2) if p.z[i]]


def _line_basis(observables: list[str]):
    """Find a 2-qubit Clifford that diagonalizes the first two observables of a line."""
    for name, gates in _CANDIDATE_BASES.items():
        basis = _gates_circuit(gates)
        maps = [_as_z_string(o, basis) for o in observables[:2]]
        if all(maps):
            return {"name": name, "gates": gates, "maps": maps}
    raise ValueError(f"no basis for {observables}")


def _transpose_sign(label: str) -> int:
    # For |Phi+>, Bob measuring P on his half equals Alice measuring P^T; Y^T = -Y.
    return -1 if label.count("Y") % 2 else 1


ROW_BASIS = [_line_basis([MAGIC_SQUARE[r][j][1] for j in range(3)]) for r in range(3)]
COL_BASIS = [_line_basis([MAGIC_SQUARE[j][c][1] for j in range(3)]) for c in range(3)]


def magic_round_circuit(r: int, c: int) -> QuantumCircuit:
    """4 qubits: Alice (0,1) and Bob (2,3) share two Bell pairs, then each rotates
    into the joint eigenbasis of their line and measures Z. No ancillas needed."""
    qc = QuantumCircuit(4, name=f"magic_{r}{c}")
    for a, b in ((0, 2), (1, 3)):
        qc.h(a)
        qc.cx(a, b)
    qc.compose(_gates_circuit(ROW_BASIS[r]["gates"]), qubits=[0, 1], inplace=True)
    qc.compose(_gates_circuit(COL_BASIS[c]["gates"]), qubits=[2, 3], inplace=True)
    return qc


def _value(bits: list[int], mapping) -> int:
    sign, support = mapping
    v = sign
    for q in support:
        v *= 1 - 2 * bits[q]
    return v


def magic_decode(r: int, c: int, bits: list[int]) -> tuple[list[int], list[int]]:
    """bits: 4 measured bits of magic_round_circuit. Returns (alice row signs, bob column signs)."""
    alice = []
    for j in range(2):
        sign, label = MAGIC_SQUARE[r][j]
        alice.append(sign * _value(bits[0:2], ROW_BASIS[r]["maps"][j]))
    alice.append(alice[0] * alice[1])  # row product must be +1
    bob = []
    for j in range(2):
        sign, label = MAGIC_SQUARE[j][c]
        bob.append(sign * _transpose_sign(label) * _value(bits[2:4], COL_BASIS[c]["maps"][j]))
    bob.append(-bob[0] * bob[1])  # column product must be -1
    return alice, bob


def magic_win(r: int, c: int, alice: list[int], bob: list[int]) -> bool:
    return alice[c] == bob[r]


def magic_classical_answers(grid: list[list[int]], r: int, c: int) -> tuple[list[int], list[int]]:
    """The impostor plays from one grid. Alice reads her row and forces the last cell so the
    row multiplies to +1; Bob reads his column and forces the last cell to make -1.
    The player edits 8 cells; cell (2,2) is where the two forced rules collide."""
    row = [grid[r][0], grid[r][1]]
    row.append(row[0] * row[1])
    col = [grid[0][c], grid[1][c]]
    col.append(-col[0] * col[1])
    return row, col


def magic_grid_value(grid: list[list[int]]) -> dict:
    wins = []
    for r in range(3):
        for c in range(3):
            a, b = magic_classical_answers(grid, r, c)
            wins.append(magic_win(r, c, a, b))
    return {"value": sum(wins) / 9, "cells": wins}


def magic_bruteforce(settings=None) -> dict:
    """All deterministic strategies: 4 legal row triples ^3 for Alice x 4 column triples ^3 for Bob."""
    settings = list(itertools.product(range(3), repeat=2)) if settings is None else list(settings)
    if not settings or any(r not in range(3) or c not in range(3) for r, c in settings):
        raise ValueError("Expected nonempty magic-square settings in range(3).")
    plus = [t for t in itertools.product((1, -1), repeat=3) if math.prod(t) == 1]
    minus = [t for t in itertools.product((1, -1), repeat=3) if math.prod(t) == -1]
    best, at_best, tried = 0.0, 0, 0
    for A in itertools.product(plus, repeat=3):
        for B in itertools.product(minus, repeat=3):
            tried += 1
            v = sum(A[r][c] == B[c][r] for r, c in settings) / len(settings)
            if v > best + 1e-12:
                best, at_best = v, 1
            elif abs(v - best) < 1e-12:
                at_best += 1
    return {"tried": tried, "best": best, "at_best": at_best}


# ============================================================ level 3: zip duel
# Distributed XEB from Kretschmer, Grewal, ..., Aaronson, arXiv:2509.07255 (2025).
# Alice must send Bob something that lets him pass a test on a measurement Alice
# never sees. Quantum: send n qubits. Impostor: send k classical bits.

ZIP_PAPER = {
    "n": 12,
    "hardware_xeb": 0.427,
    "lower_bound_bits": 78,      # any classical protocol reaching 0.427 at n=12
    "lower_bound_bits_5sigma": 62,
    "best_known_bits": 330,      # their classical protocol for 0.427
}


def brickwork_state(n: int, layers: int, seed: int) -> QuantumCircuit:
    """Random brickwork with a periodic boundary. The wrap-around gate (n-1, 0) is native on
    all-to-all trapped ions; on a nearest-neighbour chip it costs SWAPs."""
    rng = np.random.default_rng(seed)
    qc = QuantumCircuit(n, name="alice_state")
    for layer in range(layers):
        for q in range(n):
            qc.u(*rng.uniform(0, 2 * np.pi, 3), q)
        for q in range(layer % 2, n, 2):
            qc.rzz(rng.uniform(0, 2 * np.pi), q, (q + 1) % n)
    return qc


def zip_round(n: int, layers: int, state_seed: int, clifford_seed: int) -> dict:
    alice = brickwork_state(n, layers, state_seed)
    bob = random_clifford(n, seed=clifford_seed).to_circuit()
    psi = Statevector(alice)
    p = psi.evolve(bob).probabilities()
    return {"psi": psi.data, "bob": bob, "p": p}


def xeb_of_distribution(q: np.ndarray, p: np.ndarray) -> float:
    """Expected XEB when Bob samples from q and the referee scores with the true p."""
    return float(len(p) * np.dot(q, p) - 1)


def xeb_of_samples(samples: list[int], p: np.ndarray) -> float:
    return float(len(p) * np.mean([p[z] for z in samples]) - 1)


def impostor_state(psi: np.ndarray, k_bits: int, seed: int) -> np.ndarray:
    """Classical impostor: Alice sends k bits = signs of projections of her state onto
    random vectors both players agreed on beforehand. Bob rebuilds a best guess.
    One natural strategy; the theorem bounds every strategy."""
    rng = np.random.default_rng(seed)
    m = max(1, k_bits // 2)
    R = (rng.normal(size=(m, psi.size)) + 1j * rng.normal(size=(m, psi.size))) / np.sqrt(2)
    proj = R.conj() @ psi
    guess = R.T @ (np.sign(proj.real) + 1j * np.sign(proj.imag))
    return guess / np.linalg.norm(guess)


def zip_impostor_xeb(n: int, k_bits: int, trials: int, layers: int, seed: int) -> float:
    scores = []
    for t in range(trials):
        rd = zip_round(n, layers, seed + t, seed + 1000 + t)
        guess = Statevector(impostor_state(rd["psi"], k_bits, seed + 2000 + t)).evolve(rd["bob"])
        scores.append(xeb_of_distribution(guess.probabilities(), rd["p"]))
    return float(np.mean(scores))


def zip_quantum_xeb(n: int, trials: int, layers: int, seed: int, noise: float = 0.0) -> float:
    """Quantum message: Bob measures the real state. `noise` mixes in uniform outcomes
    (a depolarized device), which pulls XEB toward 0 linearly."""
    scores = []
    for t in range(trials):
        rd = zip_round(n, layers, seed + t, seed + 1000 + t)
        ideal = xeb_of_distribution(rd["p"], rd["p"])
        scores.append((1 - noise) * ideal)
    return float(np.mean(scores))


# ======================================================== /dev/urandom ablation
def urandom_bits(n: int, rng: random.Random) -> list[int]:
    return [rng.getrandbits(1) for _ in range(n)]
