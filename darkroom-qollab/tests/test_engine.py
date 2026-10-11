import json
import math
import unittest

from darkroom.engine import _analytic, _ideal_circuit_outcomes, evaluate, ingest_audit


class QuantumInterrogationTests(unittest.TestCase):
    def test_ideal_circuit_matches_all_analytic_outcomes(self):
        for cycles in range(2, 7):
            with self.subTest(cycles=cycles):
                ideal = _ideal_circuit_outcomes(cycles)
                exact = _analytic(cycles, 0.0)["quantum_interrogation"]
                for state in ("absent", "present"):
                    for outcome in ("identified_absent", "absorbed", "identified_without_absorption"):
                        self.assertAlmostEqual(ideal[state][outcome], exact[state][outcome], places=12)
                    self.assertAlmostEqual(sum(ideal[state].values()), 1.0, places=12)
                self.assertLess(ideal["absent"]["unexpected"], 1e-12)
                self.assertLess(ideal["present"]["unexpected"], 1e-12)

    def test_loss_accounting_normalizes_for_both_hypotheses(self):
        for cycles in range(2, 7):
            for loss in (0, 0.025, 0.1):
                model = _analytic(cycles, loss)
                for hypothesis in ("absent", "present"):
                    self.assertAlmostEqual(sum(model["quantum_interrogation"][hypothesis].values()), 1.0, places=12)
                    self.assertAlmostEqual(sum(model["direct"][hypothesis].values()), 1.0, places=12)

    def test_measured_counts_keep_absorption_and_noise_visible(self):
        report = json.loads(ingest_audit(json.dumps({"000000": 50, "000101": 25, "000011": 25}), '{"cycles":2,"loss_per_pass":0}'))
        self.assertEqual(report["shots"], 100)
        self.assertEqual(report["by_object_hypothesis"]["absent"]["shots"], 50)
        self.assertEqual(report["by_object_hypothesis"]["present"]["shots"], 50)
        self.assertEqual(sum(report["by_object_hypothesis"]["present"]["outcomes"].values()), 50)

    def test_rejects_out_of_scope_cycles_and_loss(self):
        for config in ({"cycles": 1}, {"cycles": 7}, {"cycles": 3, "loss_per_pass": 0.2}):
            with self.subTest(config=config), self.assertRaises(ValueError):
                evaluate(json.dumps(config))


if __name__ == "__main__":
    unittest.main()
