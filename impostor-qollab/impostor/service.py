"""Functions main.js calls. Everything crosses the JS boundary as JSON strings.

Quantum sources a round can be played with:
  "exact"   - a shot sampled from the exact statevector of the round's Qiskit circuit
  "urandom" - the /dev/urandom ablation: the quantum player is replaced by random bits
  "audit"   - shots measured on the selected backend in this run's single job
"""
import json
import random

from qiskit import QuantumCircuit, transpile

from . import games as g

ZIP_N12_FILE = "data/zip_n12.json"
BASIS = ["rx", "ry", "rz", "h", "cx"]

# ---------------------------------------------------------------- the one job
# IonQ backends take ONE job per run and return counts only, so every audited
# circuit sits side by side on its own qubits: the 4 CHSH settings (2 qubits each)
# and 3 magic-square cells that together touch every row and column (4 qubits each).
AUDIT_CHSH = [(0, 0), (0, 1), (1, 0), (1, 1)]
AUDIT_MAGIC = [(0, 1), (1, 2), (2, 0)]

_audit = {"backend": None, "chsh": {}, "magic": {}, "cursor": {}}


def _registers():
    regs, offset = [], 0
    for xy in AUDIT_CHSH:
        regs.append(("chsh", xy, offset, 2))
        offset += 2
    for rc in AUDIT_MAGIC:
        regs.append(("magic", rc, offset, 4))
        offset += 4
    return regs, offset


def audit_circuit():
    regs, width = _registers()
    qc = QuantumCircuit(width, name="impostor_audit")
    for kind, what, offset, w in regs:
        sub = g.chsh_pair(*what) if kind == "chsh" else g.magic_round_circuit(*what)
        qc.compose(sub, qubits=list(range(offset, offset + w)), inplace=True)
    qc.measure_all()
    return transpile(qc, basis_gates=BASIS, optimization_level=1)


def _shots_from_counts(counts: dict, seed: int = 11) -> list[int]:
    shots = []
    for key, c in counts.items():
        k = str(key).replace(" ", "")
        shots.extend([int(k, 16) if k.startswith("0x") else int(k, 2)] * int(c))
    random.Random(seed).shuffle(shots)
    return shots


def ingest_audit(counts_json, backend_name="selected backend"):
    """Counts of audit_circuit() -> per-test scores on the backend, and a bank of shots for play."""
    shots = _shots_from_counts(json.loads(counts_json))
    regs, _ = _registers()
    report = {"backend": str(backend_name), "shots": len(shots), "chsh": {}, "magic": {}}
    chsh_wins, magic_wins = [], []
    for kind, what, offset, w in regs:
        values = [[(s >> (offset + i)) & 1 for i in range(w)] for s in shots]
        key = "".join(map(str, what))
        if kind == "chsh":
            x, y = what
            wins = [g.chsh_win(x, y, b[0], b[1]) for b in values]
            chsh_wins += wins
            _audit["chsh"][what] = values
        else:
            r, c = what
            wins = [g.magic_win(r, c, *g.magic_decode(r, c, b)) for b in values]
            magic_wins += wins
            _audit["magic"][what] = values
        report[kind][key] = sum(wins) / max(1, len(wins))
    report["chsh_total"] = sum(chsh_wins) / max(1, len(chsh_wins))
    report["magic_total"] = sum(magic_wins) / max(1, len(magic_wins))
    _audit["backend"] = str(backend_name)
    _audit["cursor"] = {}
    return json.dumps(report)


def _from_audit(kind: str, key: tuple):
    bank = _audit[kind].get(key)
    if not bank:
        return None
    i = _audit["cursor"].get((kind, key), 0)
    _audit["cursor"][(kind, key)] = i + 1
    return bank[i % len(bank)]


# ------------------------------------------------------------------- overview
def overview():
    return json.dumps({
        "chsh": {"classical_max": g.CHSH_CLASSICAL_MAX, "quantum_max": g.CHSH_QUANTUM_MAX,
                 "bruteforce": g.chsh_bruteforce()},
        "magic": {"classical_max": g.MAGIC_CLASSICAL_MAX, "quantum_max": 1.0,
                  "bruteforce": g.magic_bruteforce(),
                  "square": [[f"{'-' if s < 0 else ''}{p}" for s, p in row] for row in g.MAGIC_SQUARE]},
        "zip": g.ZIP_PAPER,
        "audit": {"qubits": _registers()[1], "chsh": ["".join(map(str, k)) for k in AUDIT_CHSH],
                  "magic": ["".join(map(str, k)) for k in AUDIT_MAGIC]},
    })


# ------------------------------------------------------------------ level 1
def play_chsh(rounds, strategy_json, source="exact", seed=0):
    """strategy = [a(x=0), a(x=1), b(y=0), b(y=1)] agreed before the players are separated."""
    rng = random.Random(int(seed))
    strat = json.loads(strategy_json)
    out = []
    for _ in range(int(rounds)):
        x, y = rng.getrandbits(1), rng.getrandbits(1)
        ia, ib = strat[x], strat[2 + y]
        used = source
        if source == "urandom":
            qa, qb = g.urandom_bits(2, rng)
        else:
            bits = _from_audit("chsh", (x, y)) if source == "audit" else None
            if bits is None:
                used = "exact"
                bits = g.sample_bits(g.chsh_pair(x, y), rng)
            qa, qb = bits
        out.append({"x": x, "y": y, "you": [ia, ib, g.chsh_win(x, y, ia, ib)],
                    "q": [qa, qb, g.chsh_win(x, y, qa, qb)], "src": used})
    return json.dumps({"rounds": out, "your_exact": g.chsh_strategy_value(strat)})


# ------------------------------------------------------------------ level 2
def play_magic(rounds, grid_json, source="exact", seed=0):
    rng = random.Random(int(seed))
    grid = json.loads(grid_json)
    out = []
    for _ in range(int(rounds)):
        r, c = rng.randrange(3), rng.randrange(3)
        ya, yb = g.magic_classical_answers(grid, r, c)
        used = source
        if source == "urandom":
            qa, qb = g.magic_decode(r, c, g.urandom_bits(4, rng))
        else:
            bits = _from_audit("magic", (r, c)) if source == "audit" else None
            if bits is None:
                used = "exact"
                bits = g.sample_bits(g.magic_round_circuit(r, c), rng)
            qa, qb = g.magic_decode(r, c, bits)
        out.append({"r": r, "c": c, "you": [ya, yb, g.magic_win(r, c, ya, yb)],
                    "q": [qa, qb, g.magic_win(r, c, qa, qb)], "src": used})
    return json.dumps({"rounds": out, "your_exact": g.magic_grid_value(grid)})


# ------------------------------------------------------------------ level 3
def zip_curve(n=8, ks_json="[]", trials=6, seed=1):
    """Impostor XEB for each bit budget k, and the quantum message's XEB, at n qubits.
    n=12 is precomputed offline (data/zip_n12.json) because 4096-amplitude sketches are slow here."""
    n = int(n)
    if n == 12:
        with open(ZIP_N12_FILE) as f:
            return f.read()
    layers = 2 * n
    ks = json.loads(ks_json) or [n, 4 * n, 16 * n, 64 * n, 256 * n]
    points = [{"k": int(k), "xeb": g.zip_impostor_xeb(n, int(k), int(trials), layers, int(seed))} for k in ks]
    return json.dumps({"n": n, "layers": layers, "trials": int(trials), "impostor": points,
                       "quantum": g.zip_quantum_xeb(n, int(trials), layers, int(seed)),
                       "paper": g.ZIP_PAPER})


def zip_urandom(n=8, trials=6, seed=1):
    """Ablation: Bob outputs uniformly random strings instead of measuring a state."""
    import numpy as np
    n = int(n)
    rng = random.Random(int(seed))
    scores = []
    for t in range(int(trials)):
        rd = g.zip_round(n, 2 * n, int(seed) + t, int(seed) + 1000 + t)
        samples = [rng.randrange(2 ** n) for _ in range(400)]
        scores.append(g.xeb_of_samples(samples, rd["p"]))
    return json.dumps({"n": n, "xeb": float(np.mean(scores))})
