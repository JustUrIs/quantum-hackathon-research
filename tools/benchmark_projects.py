"""Persist exact model benchmarks without labeling them as remote runs."""

import contextlib
import json
import os
from pathlib import Path
import sys
import platform
import qiskit

ROOT = Path(__file__).resolve().parents[1]
for folder in ("lost-signal-qollab", "qday-clock-qollab", "order-qollab"):
    sys.path.insert(0, str(ROOT / folder))
from lostsignal import service as lost
from qday import service as qday
from orderlab import service as order


@contextlib.contextmanager
def at(folder):
    old = Path.cwd()
    os.chdir(ROOT / folder)
    try:
        yield
    finally:
        os.chdir(old)


output = {
    "source": "Local analytical models and exact Qiskit statevector; NOT remote IonQ or hardware",
    "versions": {"python": platform.python_version(), "qiskit": qiskit.__version__},
}
with at("lost-signal-qollab"):
    d = json.loads(lost.evaluate())
    output["lost_signal"] = {
        k: d[k]
        for k in (
            "params",
            "sql_rad",
            "ghz_rad",
            "gain",
            "crossing",
            "resource_interactions",
        )
    }
    output["lost_signal"]["radical_contrast"] = json.loads(
        lost.radical('{"field_ut":26}')
    )["contrast"]
    output["lost_signal"]["isotropic_contrast"] = json.loads(
        lost.radical('{"field_ut":26,"anisotropy":0}')
    )["contrast"]
output["qday_clock"] = []
for n, a in ((15, 2), (21, 2), (33, 2), (33, 5), (35, 2)):
    d = json.loads(qday.evaluate(json.dumps({"n": n, "a": a})))
    output["qday_clock"].append(
        {
            k: d[k]
            for k in (
                "n",
                "a",
                "bits",
                "genuine_success",
                "random_phase_success",
                "random_gcd_success",
                "genuine",
                "presolved",
                "histogram_distance",
                "trial_division_checks",
            )
        }
    )
with at("order-qollab"):
    d = json.loads(order.evaluate())
    output["order"] = {
        k: d[k]
        for k in ("params", "a_first", "a_second", "qq", "ab", "ba", "classical")
    }
    output["order"]["intervening_qq"] = json.loads(order.evaluate('{"info":65}'))["qq"]
out = ROOT / "artifacts/benchmarks.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps(output, indent=2))
