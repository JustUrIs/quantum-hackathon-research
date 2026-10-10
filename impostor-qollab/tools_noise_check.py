"""Offline: does the advantage survive trapped-ion-like noise? (depolarizing + readout, Aer)."""
import json
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
from impostor import service as s
qc = s.audit_circuit()
for p2 in (0.004, 0.01, 0.03, 0.06):
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p2 / 10, 1), ["rx", "ry", "rz", "h"])
    nm.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
    nm.add_all_qubit_readout_error(ReadoutError([[0.995, 0.005], [0.005, 0.995]]))
    c = AerSimulator(noise_model=nm, method="density_matrix" if False else "automatic").run(qc, shots=1500).result().get_counts()
    r = json.loads(s.ingest_audit(json.dumps(c), "aer"))
    print(f"2q depol {p2}: CHSH {r['chsh_total']:.3f} (classical max 0.750) | magic {r['magic_total']:.3f} (classical max 0.889)", flush=True)
