"""Physical invariants, adversarial baselines and end-to-end counts decoding.

Run from repo root: python -m unittest discover -s tests -v
"""

import contextlib
import json
import math
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, Kraus, Operator
from qiskit.providers.basic_provider import BasicSimulator

ROOT = Path(__file__).resolve().parents[1]
for name in ("lost-signal-qollab", "qday-clock-qollab", "order-qollab"):
    sys.path.insert(0, str(ROOT / name))
from lostsignal import service as lost
from orderlab import service as order
from qday import service as qday


@contextlib.contextmanager
def directory(name):
    before = Path.cwd()
    os.chdir(ROOT / name)
    try:
        yield
    finally:
        os.chdir(before)


class SensingTests(unittest.TestCase):
    def test_noiseless_scaling_and_equal_budget(self):
        for n in range(1, 7):
            a, b = lost.precision(n, 0, 256)
            self.assertAlmostEqual(a / b, math.sqrt(n))
            self.assertAlmostEqual(b, 1 / (n * 16))

    def test_noise_crossover(self):
        for n in range(2, 7):
            eta = math.log(n) / (2 * (n - 1))
            a, b = lost.precision(n, eta)
            self.assertAlmostEqual(a, b)
            a, b = lost.precision(n, eta + 0.1)
            self.assertLess(a, b)

    def test_dephasing_formula_against_density_matrix(self):
        for n in (1, 2, 4):
            for eta in (0, 0.2, 0.6):
                phase = 0.31
                qc = QuantumCircuit(n)
                qc.h(0)
                for j in range(1, n):
                    qc.cx(0, j)
                for j in range(n):
                    qc.rz(phase, j)
                rho = DensityMatrix.from_instruction(qc)
                v = math.exp(-eta)
                channel = Kraus(
                    [
                        math.sqrt((1 + v) / 2) * np.eye(2),
                        math.sqrt((1 - v) / 2) * np.diag([1, -1]),
                    ]
                )
                for j in range(n):
                    rho = rho.evolve(channel, qargs=[j])
                read = QuantumCircuit(n)
                read.h(range(n))
                rho = rho.evolve(read)
                even = sum(
                    p
                    for i, p in enumerate(rho.probabilities())
                    if i.bit_count() % 2 == 0
                )
                self.assertAlmostEqual(
                    even, (1 + math.exp(-n * eta) * math.cos(n * phase)) / 2, places=11
                )

    def test_ideal_qiskit_transfer(self):
        for n in (1, 3, 6):
            for phase in (0.1, 0.6, 1.2):
                p = Statevector.from_instruction(lost.ramsey(n, phase)).probabilities()
                even = sum(x for i, x in enumerate(p) if i.bit_count() % 2 == 0)
                self.assertAlmostEqual(even, (1 + math.cos(n * phase)) / 2)

    def test_radical_direction_requires_anisotropy(self):
        flat = lost.radical_curve(26, 0)
        directional = lost.radical_curve(26, 1)
        self.assertLess(np.ptp([p["yield"] for p in flat]), 1e-12)
        self.assertGreater(np.ptp([p["yield"] for p in directional]), 0.001)
        self.assertTrue(all(0 <= p["yield"] <= 1 for p in directional))

    def test_counts_bit_order(self):
        qc = lost.audit_circuit('{"n":4}')
        c = BasicSimulator().run(qc, shots=4096, seed_simulator=8).result().get_counts()
        rep = json.loads(lost.ingest_audit(json.dumps(c), '{"n":4}'))
        self.assertLess(abs(rep["ghz_even"] - rep["ghz_expected"]), 0.035)
        self.assertLess(
            abs(rep["independent_zero"] - rep["independent_expected"]), 0.025
        )

    def test_route_provenance_and_bounds(self):
        with directory("lost-signal-qollab"):
            r = lost.route()
        self.assertEqual(r["model"], "WMM2025")
        self.assertEqual(len(r["points"]), 41)
        self.assertTrue(all(15 < p["field_ut"] < 65 for p in r["points"]))
        self.assertGreater(r["points"][-1]["distance_km"], 2000)


class OrderTests(unittest.TestCase):
    def test_deferred_measurement_against_projectors(self):
        for theta, first, second in ((0.2, 0, 0.6), (1.3, 0.4, 0.9), (0.8, 1.2, 0.1)):
            p = order.canonical_probs(order.sequence(theta, first, second))
            a = math.cos((theta - first) / 2) ** 2
            c = math.cos((first - second) / 2) ** 2
            np.testing.assert_allclose(
                p, [a * c, a * (1 - c), (1 - a) * (1 - c), (1 - a) * c], atol=1e-12
            )

    def test_qq_invariant_for_varied_states(self):
        for theta in np.linspace(0, math.pi, 7):
            for angle in np.linspace(0, math.pi, 9):
                ab = order.canonical_probs(order.sequence(theta, 0, angle))
                ba = order.canonical_probs(order.sequence(theta, angle, 0), True)
                self.assertAlmostEqual(order.qq(ab, ba), 0, places=12)

    def test_commuting_limit(self):
        for angle in (0, math.pi):
            ab = order.canonical_probs(order.sequence(0.7, 0, angle))
            ba = order.canonical_probs(order.sequence(0.7, angle, 0), True)
            np.testing.assert_allclose(ab, ba, atol=1e-12)

    def test_intervening_information_can_break_qq(self):
        ab = order.canonical_probs(order.sequence(0.6, 0, 1.2, 1.1))
        ba = order.canonical_probs(order.sequence(0.6, 1.2, 0, 1.1), True)
        self.assertGreater(abs(order.qq(ab, ba)), 0.1)

    def test_classical_contextual_counterexample(self):
        for ab, ba in (
            ([0.4, 0.1, 0.2, 0.3], [0.2, 0.3, 0.1, 0.4]),
            ([1, 0, 0, 0], [0, 0, 0, 1]),
        ):
            c = order.contextual(ab, ba)
            self.assertLess(c["max_error"], 1e-12)

    def test_empirical_transcription_and_failure_case(self):
        with directory("order-qollab"):
            d = order.polls()["datasets"]
        self.assertAlmostEqual(order.qq(d[0]["ab"], d[0]["ba"]), -0.0032)
        self.assertAlmostEqual(order.qq(d[1]["ab"], d[1]["ba"]), 0.1514)
        self.assertAlmostEqual(sum(d[0]["ab"]), 0.9999)

    def test_packed_counts_match_each_order(self):
        qc = order.audit_circuit()
        counts = (
            BasicSimulator()
            .run(qc, shots=8192, seed_simulator=19)
            .result()
            .get_counts()
        )
        rep = json.loads(order.ingest_audit(json.dumps(counts)))
        with directory("order-qollab"):
            exact = json.loads(order.evaluate())
        np.testing.assert_allclose(rep["ab"], exact["ab"], atol=0.025)
        np.testing.assert_allclose(rep["ba"], exact["ba"], atol=0.025)
        self.assertGreater(rep["qq_se"], 0)

    def test_questionnaire_audit_intervals_and_validation(self):
        d = json.loads(
            order.audit_counts('{"ab":[250,50,100,100],"ba":[280,30,120,70]}')
        )
        self.assertAlmostEqual(d["qq"], 0)
        self.assertAlmostEqual(d["qq_p_normal"], 1)
        self.assertAlmostEqual(d["a_order_effect"], 0.02)
        self.assertLess(d["qq_ci95_normal"][0], 0)
        self.assertGreater(d["qq_ci95_normal"][1], 0)
        d = json.loads(order.audit_counts('{"ab":[400,30,30,40],"ba":[50,210,210,30]}'))
        self.assertLess(d["qq_p_normal"], 0.00001)
        with self.assertRaises(ValueError):
            order.audit_counts('{"ab":[-1,2,3,4],"ba":[1,2,3,4]}')
        with self.assertRaises(ValueError):
            order.audit_counts('{"ab":[1.5,2,3,4],"ba":[1,2,3,4]}')
        with self.assertRaises(ValueError):
            order.audit_counts('{"ab":[0,0,0,0],"ba":[1,2,3,4]}')


class FactoringTests(unittest.TestCase):
    def test_controlled_modular_multiplication_entire_basis(self):
        for n, multiplier in ((15, 2), (15, 4), (21, 2), (21, 4), (33, 2), (35, 4)):
            w = (n - 1).bit_length()
            qc = QuantumCircuit(w + 1)
            qday.modular_multiply(qc, multiplier, n, list(range(1, w + 1)), 0)
            u = Operator(qc).data
            for control in (0, 1):
                for x in range(1 << w):
                    y = x * multiplier % n if control and x < n else x
                    self.assertAlmostEqual(
                        abs(u[(y << 1) | control, (x << 1) | control]), 1, places=10
                    )

    def test_order_histograms_against_independent_cosets(self):
        for n in (15, 21, 33, 35):
            r = qday.experiment(n, 2, 6)
            self.assertLess(r["histogram_distance"], 1e-9)
            self.assertAlmostEqual(sum(r["probabilities"]), 1, places=9)
            if n == 33:
                # a=2 has order 10 but 2**5 == -1 mod 33: an honest Shor failure.
                self.assertEqual(r["genuine_success"], 0)
                self.assertEqual(r["random_phase_success"], 0)
            else:
                self.assertGreater(r["genuine_success"], 0)
                self.assertGreater(r["random_phase_success"], 0)
        self.assertGreater(qday.experiment(33, 5, 6)["genuine_success"], 0)

    def test_builder_never_calls_period_oracle(self):
        qday.genuine.cache_clear()
        qday.compiled.cache_clear()
        with patch.object(
            qday, "classical_period", side_effect=AssertionError("oracle used")
        ):
            qc = qday.audit_circuit('{"n":15,"a":2,"bits":6}')
        self.assertEqual(qc.num_qubits, 10)

    def test_recovered_factors_are_real(self):
        for n in (15, 21, 33, 35):
            self.assertIsNone(qday.recover(0, 6, 2, n))
            for y in range(64):
                r = qday.recover(y, 6, 2, n)
                if r:
                    f, g = r["factors"]
                    self.assertEqual(f * g, n)
                    self.assertGreater(min(f, g), 1)

    def test_output_ablation_does_not_hide_classical_success(self):
        d = json.loads(qday.evaluate('{"mix":1}'))
        self.assertAlmostEqual(d["display_success"], d["random_phase_success"])
        self.assertAlmostEqual(d["random_gcd_success"], 6 / 13)
        self.assertEqual(d["trial_division_checks"], 2)

    def test_backend_counts_and_postprocessing(self):
        qc = qday.audit_circuit()
        counts = (
            BasicSimulator().run(qc, shots=2048, seed_simulator=8).result().get_counts()
        )
        d = json.loads(qday.ingest_audit(json.dumps(counts)))
        self.assertAlmostEqual(d["rate"], 0.5, delta=0.04)
        self.assertTrue(d["evidence"])

    def test_invalid_inputs_fail_explicitly(self):
        with self.assertRaises(ValueError):
            qday.evaluate('{"n":21,"a":3}')
        with self.assertRaises(ValueError):
            lost.evaluate('{"n":25}')
        with self.assertRaises(ValueError):
            order.evaluate('{"theta":999}')


if __name__ == "__main__":
    unittest.main()
