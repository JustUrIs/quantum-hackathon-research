"""Offline serialization check. No account, network job or credits are used.

Optional dependency: qiskit-ionq==1.0.2. Does not validate cloud gate limits,
native compilation, runtime bridge, queueing, noise, or provider acceptance.
"""

import importlib.metadata
import json
from pathlib import Path
import sys
from qiskit_ionq.helpers import qiskit_circ_to_ionq_circ

ROOT = Path(__file__).resolve().parents[1]
for folder in ("lost-signal-qollab", "qday-clock-qollab", "order-qollab"):
    sys.path.insert(0, str(ROOT / folder))
from lostsignal import service as lost
from qday import service as qday
from orderlab import service as order

checks = []
for name, service in [("lost-signal", lost), ("qday-clock", qday), ("order", order)]:
    qc = service.audit_circuit()
    instructions, measurements, mapping = qiskit_circ_to_ionq_circ(qc, gateset="qis")
    assert instructions and qc.num_qubits <= 25
    assert measurements == qc.num_clbits
    checks.append(
        {
            "project": name,
            "qubits": qc.num_qubits,
            "serialized_instructions": len(instructions),
            "measurements": measurements,
            "measurement_map": mapping,
            "status": "offline serialization passed",
        }
    )
out = {
    "provider_version": importlib.metadata.version("qiskit-ionq"),
    "scope": "OFFLINE ONLY; no remote job sent",
    "checks": checks,
}
(ROOT / "artifacts/ionq-format-check.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(out, indent=2))
