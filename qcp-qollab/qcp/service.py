"""Authoritative local Qiskit judge. All cases are public practice cases."""
import json
import math
import time
from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from .solver import compile_solution, VerdictError, VERSION

ROOT = Path(__file__).resolve().parents[1]


def catalog():
    return (ROOT / "catalog.json").read_text(encoding="utf-8")


def build(ir, case):
    n = case["n"]
    qc = QuantumCircuit(n + 1)
    for name, qubits, params in ir["ops"]:
        if name == "oracle":
            if case["kind"] == "bv":
                for q in range(n):
                    if case["secret"] & (1 << q): qc.cx(q, n)
            else:
                marked = [case["secret"]] if case["kind"] == "grover" else [x for x, y in enumerate(case["table"]) if y]
                if len(marked) == (1 << n): qc.x(n)
                else:
                    for x in marked:
                        zeros = [q for q in range(n) if not x & (1 << q)]
                        if zeros: qc.x(zeros)
                        qc.mcx(list(range(n)), n)
                        if zeros: qc.x(zeros)
        elif name == "mcx": qc.mcx(qubits[:-1], qubits[-1])
        elif name == "mcp": qc.mcp(params[0], qubits[:-1], qubits[-1])
        else: getattr(qc, name)(*params, *qubits)
    return qc


def inspect(ir, n, problem):
    queries = sum(op[0] == "oracle" for op in ir["ops"])
    cap = int(math.pi / 4 * math.sqrt(1 << n)) if problem == "grover" else 1
    depths = [0] * ir["width"]
    two = 0
    for name, qs, _ in ir["ops"]:
        layer = 1 + max(depths[q] for q in qs)
        for q in qs: depths[q] = layer
        if name != "oracle" and len(qs) == 2: two += 1
    if queries > cap:
        raise VerdictError("QRE", f"n={n}: {queries} oracle calls; limit {cap}.")
    if max(depths) > 256:
        raise VerdictError("DLE", f"n={n}: logical depth {max(depths)}; limit 256.")
    return {"qubits": ir["width"], "queries": queries, "query_limit": cap,
            "logical_depth": max(depths), "logical_instructions": len(ir["ops"]),
            "explicit_two_qubit_gates": two}


def judge(problem, source, mode="submit"):
    start = time.perf_counter()
    try:
        if mode not in ("run", "submit"): raise VerdictError("CE", "Unknown judge mode.")
        cases = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))[problem]
        if mode == "run": cases = [c for c in cases if c.get("sample")]
        circuits = {}
        metrics = {}
        for n in sorted({c["n"] for c in cases}):
            circuits[n] = compile_solution(source, n)
            metrics[str(n)] = inspect(circuits[n], n, problem)
        rows, worst, failed = [], 1.0, None
        for i, case in enumerate(cases):
            qc = build(circuits[case["n"]], case)
            probabilities = Statevector.from_instruction(qc).probabilities(list(range(case["n"])))
            if problem == "dj":
                constant = len(set(case["table"])) == 1
                success = float(probabilities[0] if constant else 1 - probabilities[0])
            else: success = float(probabilities[case["secret"]])
            threshold = 0.9 if problem == "grover" else 1 - 1e-9
            passed = success >= threshold - 1e-12
            worst = min(worst, success)
            row = {"case": i + 1, "n": case["n"], "success": success, "passed": passed}
            rows.append(row)
            if not passed and failed is None:
                failed = {**row, "fixture": case, "probabilities": probabilities.tolist()}
        # Fixed physical decomposition is diagnostic, never the oracle-query cost.
        sample = cases[0]
        representative = build(circuits[sample["n"]], sample)
        decomposed = transpile(representative, basis_gates=["u", "cx"], optimization_level=0, seed_transpiler=19)
        return json.dumps({"status": "WA" if failed else "AC", "problem": problem, "mode": mode,
                           "version": VERSION, "source": "Qiskit Statevector · local ideal simulation",
                           "total": len(cases), "passed": sum(r["passed"] for r in rows),
                           "worst_success": worst, "failed": failed, "rows": rows, "metrics": metrics,
                           "representative": {"n": sample["n"], "cx": int(decomposed.count_ops().get("cx", 0)), "depth": decomposed.depth(),
                                              "note": "First fixture, u/cx basis, optimization level 0; includes oracle construction."},
                           "elapsed_ms": round((time.perf_counter() - start) * 1000),
                           "circuits": {str(k): v for k, v in circuits.items()}})
    except VerdictError as exc:
        return json.dumps({"status": exc.status, "message": str(exc), "source": "Qiskit judge", "version": VERSION})
    except (KeyError, ValueError) as exc:
        return json.dumps({"status": "RE", "message": str(exc), "source": "Qiskit judge", "version": VERSION})


def evaluate(payload):
    value = json.loads(payload)
    return judge(value["problem"], value["source"], value.get("mode", "submit"))
