import numpy as np
from qiskit_aer import AerSimulator
from impostor.referees import *

sim = AerSimulator()
rng = np.random.default_rng(0)

def bits_of(counts_key, nbits):
    # qiskit bitstrings are little-endian: clbit 0 is the rightmost char
    return [int(counts_key[::-1][i]) for i in range(nbits)]

# CHSH: 10 rounds x 2 qubits in one circuit, many shots
R = 10; wins = []
for trial in range(40):
    xs, ys = rng.integers(0, 2, R).tolist(), rng.integers(0, 2, R).tolist()
    res = sim.run(chsh_circuit(xs, ys), shots=50).result().get_counts()
    for key, c in res.items():
        b = bits_of(key, 2 * R)
        wins += [chsh_score(xs, ys, b[0::2], b[1::2])] * c
print(f"CHSH quantum win rate: {np.mean(wins):.3f} (theory {CHSH_QUANTUM_MAX:.3f}, classical max {CHSH_CLASSICAL_MAX})")
print("best classical deterministic:", max(w for _, w in chsh_all_classical_strategies()))

# Magic square: 2 rounds x 8 qubits = 16 qubits
ws = []
for trial in range(30):
    rows, cols = rng.integers(0, 3, 2).tolist(), rng.integers(0, 3, 2).tolist()
    res = sim.run(magic_circuit(rows, cols), shots=20).result().get_counts()
    for key, c in res.items():
        b = bits_of(key, 8)
        a, bo = magic_decode(rows, cols, [b[0:4], b[4:8]])
        ws += [magic_score(rows, cols, a, bo)] * c
print(f"Magic square quantum win rate: {np.mean(ws):.3f} (classical max {MAGIC_CLASSICAL_MAX:.3f})")

# urandom ablation for magic square
ws = []
for trial in range(2000):
    rows, cols = rng.integers(0, 3, 1).tolist(), rng.integers(0, 3, 1).tolist()
    b = rng.integers(0, 2, 4).tolist()
    a, bo = magic_decode(rows, cols, [b])
    ws.append(magic_score(rows, cols, a, bo))
print(f"Magic square with /dev/urandom: {np.mean(ws):.3f}")

# Zip duel, n=8 quick
n, L = 8, 8
p = zip_ideal_probs(n, L, 1, 2)
counts = sim.run(zip_circuit(n, L, 1, 2), shots=2000).result().get_counts()
print(f"Zip n={n}: quantum XEB {xeb_from_counts(counts, p, n):.3f}")
uni = {format(z, f'0{n}b'): 1 for z in rng.integers(0, 2**n, 2000)}
from collections import Counter
uni = Counter(format(z, f'0{n}b') for z in rng.integers(0, 2**n, 2000))
print(f"Zip n={n}: urandom XEB {xeb_from_counts(uni, p, n):.3f}")
