"""A small unitary model of quantum interrogation with full outcome accounting.

The probe is a path qubit. A fresh environment qubit records absorption on
each pass, and absorbed branches are frozen. Per-pass optical loss is reported
as a separate analytic channel; it is intentionally absent from the circuit.
"""
import json
import math
from functools import lru_cache

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.providers.basic_provider import BasicSimulator


def _config(value):
    c = json.loads(value) if isinstance(value, str) else dict(value)
    cycles = int(c.get("cycles", 2))
    loss = float(c.get("loss_per_pass", 0.0))
    if not 2 <= cycles <= 6:
        raise ValueError("Choose between 2 and 6 interrogation cycles.")
    if not math.isfinite(loss) or not 0 <= loss <= 0.1:
        raise ValueError("Choose a per-pass optical loss between 0% and 10%.")
    return {"cycles": cycles, "loss_per_pass": loss}


def _circuit(cycles, measure=False):
    # q0 labels object absent/present; q1 is the probe path; q2.. record a
    # fresh, orthogonal absorber/environment flag for each interrogation.
    obj, path = 0, 1
    env = list(range(2, 2 + cycles))
    qc = QuantumCircuit(cycles + 2, cycles + 2, name=f"darkroom_{cycles}_passes")
    qc.h(obj)  # both object hypotheses in one measured circuit
    theta = math.pi / (2 * cycles)

    for j, flag in enumerate(env):
        if j == 0:
            # Both hypotheses are active on the first weak beam splitter.
            qc.ry(2 * theta, path)
        else:
            # With no object, the path keeps rotating. With an object, only
            # the branch that has not already been absorbed keeps rotating.
            qc.x(obj)
            qc.cry(2 * theta, obj, path)
            qc.x(obj)
            qc.x(env[:j])
            qc.mcry(2 * theta, [obj, *env[:j]], path, mode="noancilla")
            qc.x(env[:j])

        # A present object absorbs path=1, provided no earlier pass absorbed
        # the probe. The fresh environment flag stores that lost branch.
        if j == 0:
            qc.ccx(obj, path, flag)
        else:
            qc.x(env[:j])
            qc.mcx([obj, path, *env[:j]], flag, mode="noancilla")
            qc.x(env[:j])

    if measure:
        qc.measure(range(cycles + 2), range(cycles + 2))
    return qc


def _analytic(cycles, loss):
    theta = math.pi / (2 * cycles)
    c2, s2 = math.cos(theta) ** 2, math.sin(theta) ** 2

    # A direct one-pass probe: if present, the object absorbs every probe
    # that was not already lost; if absent, a detector reports its absence.
    direct = {
        "absent": {"identified_absent": 1 - loss, "lost_inconclusive": loss,
                   "absorbed": 0.0, "identified_without_absorption": 0.0},
        "present": {"identified_absent": 0.0, "lost_inconclusive": loss,
                    "absorbed": 1 - loss, "identified_without_absorption": 0.0},
    }

    # For an absent object, all N weak rotations add coherently to pi/2.
    absent_survival = (1 - loss) ** cycles
    quantum_absent = {
        "identified_absent": absent_survival,
        "lost_inconclusive": 1 - absent_survival,
        "absorbed": 0.0,
        "identified_without_absorption": 0.0,
    }

    # With an object, each active pass can absorb in the blocked arm, lose the
    # probe, or survive. Sum every mutually exclusive outcome; hide no failures.
    active = 1.0
    absorbed = lost = 0.0
    for _ in range(cycles):
        absorbed += active * s2
        lost += active * c2 * loss
        active *= c2 * (1 - loss)
    quantum_present = {
        "identified_absent": 0.0,
        "lost_inconclusive": lost,
        "absorbed": absorbed,
        "identified_without_absorption": active,
    }
    return {
        "theta_radians": theta,
        "direct": direct,
        "quantum_interrogation": {"absent": quantum_absent, "present": quantum_present},
        "checks": {
            "direct_absent_total": sum(direct["absent"].values()),
            "direct_present_total": sum(direct["present"].values()),
            "quantum_absent_total": sum(quantum_absent.values()),
            "quantum_present_total": sum(quantum_present.values()),
        },
    }


def _ideal_circuit_outcomes(cycles):
    state = Statevector.from_instruction(_circuit(cycles))
    bins = {
        "absent": {"identified_absent": 0.0, "lost_inconclusive": 0.0,
                   "absorbed": 0.0, "identified_without_absorption": 0.0,
                   "unexpected": 0.0},
        "present": {"identified_absent": 0.0, "lost_inconclusive": 0.0,
                    "absorbed": 0.0, "identified_without_absorption": 0.0,
                    "unexpected": 0.0},
    }
    env_mask = (1 << cycles) - 1
    for basis, probability in enumerate(state.probabilities()):
        if probability < 1e-15:
            continue
        present = (basis & 1) == 1
        path = (basis >> 1) & 1
        flags = (basis >> 2) & env_mask
        row = bins["present" if present else "absent"]
        if not present and path == 1 and flags == 0:
            row["identified_absent"] += 2 * float(probability)
        elif present and flags and flags.bit_count() == 1 and path == 1:
            row["absorbed"] += 2 * float(probability)
        elif present and flags == 0 and path == 0:
            row["identified_without_absorption"] += 2 * float(probability)
        else:
            row["unexpected"] += 2 * float(probability)
    return bins


@lru_cache(maxsize=5)
def _evaluate(cycles):
    ideal = _ideal_circuit_outcomes(cycles)
    exact = _analytic(cycles, 0.0)["quantum_interrogation"]
    max_error = max(
        abs(ideal[state][key] - exact[state][key])
        for state in ("absent", "present")
        for key in ("identified_absent", "absorbed", "identified_without_absorption")
    )
    max_error = max(max_error, *(ideal[state]["unexpected"] for state in ("absent", "present")))
    return ideal, max_error


def evaluate(config_json):
    c = _config(config_json)
    ideal, error = _evaluate(c["cycles"])
    analytic = _analytic(c["cycles"], c["loss_per_pass"])
    return json.dumps({
        "config": c,
        "qubits": c["cycles"] + 2,
        "circuit": {
            "cycles": c["cycles"],
            "object_hypothesis": "equal superposition label, measured and conditioned",
            "absorption": "fresh environment flag per pass; absorbed branch frozen",
            "optical_loss": "not in Qiskit circuit; shown as separate analytic channel",
            "ideal_statevector_outcomes": ideal,
            "analytic_max_error": error,
        },
        "model": analytic,
        "interpretation": {
            "scope": "single-photon path-interferometer model; not a real optical experiment",
            "measurement": "presence can be inferred from the safe output without absorption, probabilistically",
            "loss": "lost probes are inconclusive, never counted as detections",
            "caveat": "quantum interrogation is established physics; this app is a teaching and audit tool, not a new sensing result",
        },
    }, allow_nan=False)


def audit_circuit(config_json):
    c = _config(config_json)
    circuit = _circuit(c["cycles"], measure=True)
    return transpile(circuit, basis_gates=["h", "x", "y", "z", "s", "sdg", "t", "tdg", "rx", "ry", "rz", "cx"], optimization_level=1)


def local_audit(config_json):
    """Measure the Qiskit circuit without calling a remote provider."""
    circuit = audit_circuit(config_json)
    counts = BasicSimulator().run(
        circuit, shots=1024, seed_simulator=91
    ).result().get_counts()
    report = json.loads(ingest_audit(
        json.dumps(counts), config_json, "Qiskit BasicSimulator / local Python runtime"
    ))
    report["source"] = {
        "kind": "local_qiskit_simulation", "shots": 1024,
        "seed": 91, "network_used": False, "quantum_hardware": False,
    }
    return json.dumps(report, allow_nan=False)


def _classify(mask, cycles):
    present = bool(mask & 1)
    path = (mask >> 1) & 1
    flags = (mask >> 2) & ((1 << cycles) - 1)
    if not present and path == 1 and flags == 0:
        label = "identified_absent"
    elif present and flags and flags.bit_count() == 1 and path == 1:
        label = "absorbed"
    elif present and flags == 0 and path == 0:
        label = "identified_without_absorption"
    else:
        label = "unexpected_or_noise"
    return ("present" if present else "absent"), label, path, flags


def ingest_audit(counts_json, config_json, backend_name="selected backend"):
    c = _config(config_json)
    counts = json.loads(counts_json)
    shots = sum(int(v) for v in counts.values())
    if shots <= 0:
        raise ValueError("Backend returned no measurement shots.")
    rows = []
    aggregate = {
        state: {"shots": 0, "outcomes": {"identified_absent": 0,
                 "lost_inconclusive": 0, "absorbed": 0,
                 "identified_without_absorption": 0, "unexpected_or_noise": 0}}
        for state in ("absent", "present")
    }
    for bits, number in counts.items():
        cleaned = str(bits).replace(" ", "")
        mask = int(cleaned, 16) if cleaned.startswith("0x") else int(cleaned, 2)
        state, label, path, flags = _classify(mask, c["cycles"])
        number = int(number)
        aggregate[state]["shots"] += number
        aggregate[state]["outcomes"][label] += number
        rows.append({"bits": cleaned, "object": state, "path": path,
                     "absorption_flags": flags, "outcome": label, "shots": number})
    for state in aggregate:
        n = aggregate[state]["shots"]
        aggregate[state]["rates"] = {k: v / n if n else 0.0
                                      for k, v in aggregate[state]["outcomes"].items()}
    return json.dumps({"backend": str(backend_name), "shots": shots,
                       "config": c, "by_object_hypothesis": aggregate,
                       "raw_counts": rows,
                       "note": "backend counts model the ideal absorber only; per-pass optical loss is a separate analytic scenario"},
                      allow_nan=False)
