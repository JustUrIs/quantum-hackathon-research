"""Run: python -m tests.test_impostor  (from the project root). Uses only qiskit + numpy,
plus BasicSimulator as a stand-in for the backend Qollab injects."""
import json
import random
import time

from qiskit.providers.basic_provider import BasicSimulator

from impostor import games as g, service as s


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    assert cond, name


ov = json.loads(s.overview())
check("chsh bruteforce = 0.75 over 16", ov["chsh"]["bruteforce"] == {"tried": 16, "best": 0.75, "at_best": 8})
check("magic bruteforce = 8/9 over 4096", ov["magic"]["bruteforce"]["tried"] == 4096
      and abs(ov["magic"]["bruteforce"]["best"] - 8 / 9) < 1e-9)

# exact play
res = json.loads(s.play_chsh(4000, json.dumps([0, 0, 0, 0]), "exact", 1))
q = sum(r["q"][2] for r in res["rounds"]) / 4000
y = sum(r["you"][2] for r in res["rounds"]) / 4000
check("chsh quantum ~0.854", abs(q - g.CHSH_QUANTUM_MAX) < 0.02, f"{q:.3f}")
check("chsh best classical ~0.75", abs(y - 0.75) < 0.03, f"{y:.3f}")
u = json.loads(s.play_chsh(4000, "[0,0,0,0]", "urandom", 2))
check("chsh urandom ~0.5", abs(sum(r["q"][2] for r in u["rounds"]) / 4000 - 0.5) < 0.03)

grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
res = json.loads(s.play_magic(900, json.dumps(grid), "exact", 3))
qm = sum(r["q"][2] for r in res["rounds"]) / 900
check("magic quantum = 1.0", qm == 1.0, f"{qm:.3f}")
best_grid = max((json.loads(json.dumps([[a, b, c], [d, e, f], [h, i, 1]])) for a, b, c, d, e, f, h, i in
                 __import__("itertools").product((1, -1), repeat=8)), key=lambda G: g.magic_grid_value(G)["value"])
check("magic best editable grid = 8/9", abs(g.magic_grid_value(best_grid)["value"] - 8 / 9) < 1e-9)
u = json.loads(s.play_magic(3000, json.dumps(grid), "urandom", 4))
check("magic urandom ~0.5", abs(sum(r["q"][2] for r in u["rounds"]) / 3000 - 0.5) < 0.04)

# the one job
qc = s.audit_circuit()
check("audit fits IonQ Aria (<=25 qubits)", qc.num_qubits <= 25, f"{qc.num_qubits} qubits, ops {dict(qc.count_ops())}")
t = time.time()
counts = BasicSimulator().run(qc, shots=300).result().get_counts()
rep = json.loads(s.ingest_audit(json.dumps(counts), "basic_simulator"))
check("audit chsh ~0.85", abs(rep["chsh_total"] - 0.854) < 0.05, f"{rep['chsh_total']:.3f} in {time.time()-t:.1f}s")
check("audit magic = 1", rep["magic_total"] == 1.0, json.dumps(rep["magic"]))
a = json.loads(s.play_chsh(50, "[0,0,0,0]", "audit", 5))
check("audit-sourced rounds use backend shots", all(r["src"] == "audit" for r in a["rounds"]))

# zip
z = json.loads(s.zip_curve(8, "[8, 128, 2048]", 4, 1))
check("zip quantum >> impostor at 8 bits", z["quantum"] > 0.8 and z["impostor"][0]["xeb"] < 0.2,
      f"q={z['quantum']:.2f} " + " ".join(f"k{p['k']}={p['xeb']:.2f}" for p in z["impostor"]))
zu = json.loads(s.zip_urandom(8, 4, 1))
check("zip urandom ~0", abs(zu["xeb"]) < 0.15, f"{zu['xeb']:.3f}")
print("all good")
