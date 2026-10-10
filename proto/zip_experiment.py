"""Quick experiment: classical k-bit messages vs quantum n-qubit message on DXHOG (XEB) task."""
import numpy as np
from qiskit.quantum_info import random_clifford, Statevector

rng = np.random.default_rng(1)

def haar(n):
    v = rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
    return v / np.linalg.norm(v)

def xeb(p_true, q_bob, n):
    # expected score when Bob samples z~q and is scored with true p
    return 2**n * float(np.dot(q_bob, p_true)) - 1

def sketch_strategy(psi, k, shared):
    # Alice sends k bits: signs of Re and Im of projections onto shared random complex vectors
    m = k // 2
    R = shared[:m]
    proj = R.conj() @ psi
    bits_re, bits_im = np.sign(proj.real), np.sign(proj.imag)
    coef = bits_re + 1j * bits_im
    est = R.T @ coef  # Bob reconstruction
    return est / np.linalg.norm(est)

def topk_strategy(psi, k, n):
    # send index (n bits) of the largest-|amp| basis states, as many as fit
    m = max(1, k // n)
    idx = np.argsort(-np.abs(psi))[:m]
    est = np.zeros_like(psi); est[idx] = 1.0
    return est / np.linalg.norm(est)

for n in [6, 8, 10, 12]:
    N = 2**n
    trials = 10
    print(f"\n n={n} qubits (state has {N} complex amplitudes)")
    for k in [n, 4*n, 16*n, 64*n, 256*n]:
        s_sk, s_tk = [], []
        for _ in range(trials):
            psi = haar(n)
            shared = (rng.normal(size=(k, N)) + 1j * rng.normal(size=(k, N))) / np.sqrt(2)
            C = random_clifford(n, seed=int(rng.integers(1e9))).to_circuit()
            ev = lambda v: np.abs(Statevector(v).evolve(C).data) ** 2
            p = ev(psi)
            for strat, acc in ((sketch_strategy(psi, k, shared), s_sk), (topk_strategy(psi, k, n), s_tk)):
                q = ev(strat)
                acc.append(xeb(p, q, n))
        print(flush=True, end="");print(f"  k={k:5d} bits | sketch XEB={np.mean(s_sk):.3f} | top-k XEB={np.mean(s_tk):.3f}")
    print(f"  quantum ({n} qubits, ideal) XEB ~ {2**n*2/(2**n+1)-1:.3f}")
