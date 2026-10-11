"""Check the judge against wrong algorithms, syntax abuse, and complete fixtures."""
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'qcp-qollab'))
from qcp.solver import compile_solution, VerdictError
from qcp.service import judge

CATALOG = json.loads((ROOT/'qcp-qollab/catalog.json').read_text(encoding='utf-8'))
CASES = json.loads((ROOT/'qcp-qollab/cases.json').read_text(encoding='utf-8'))


class QCPTests(unittest.TestCase):
    def test_complete_reference_suites(self):
        for p in CATALOG['problems']:
            with self.subTest(problem=p['id']):
                result = json.loads(judge(p['id'],p['solution']))
                self.assertEqual(result['status'],'AC',result)
                self.assertEqual(result['total'],p['test_count'])
                self.assertEqual(result['passed'],result['total'])
                self.assertGreaterEqual(result['worst_success'],.9)

    def test_fixture_contracts(self):
        self.assertEqual([len(CASES[k]) for k in ('bv','dj','grover')],[124,134,124])
        for key in ('bv','grover'):
            for n in range(2,7):
                self.assertEqual({c['secret'] for c in CASES[key] if c['n']==n},set(range(1<<n)))
        for c in CASES['dj']:
            self.assertIn(sum(c['table']),(0,1<<(c['n']-1),1<<c['n']))
        self.assertEqual(sum(c['n']==3 and sum(c['table'])==4 for c in CASES['dj']),70)

    def test_starters_fail(self):
        for p in CATALOG['problems']:
            result=json.loads(judge(p['id'],p['template'],'run'))
            self.assertEqual(result['status'],'WA')

    def test_missing_phase_kickback_fails(self):
        p=CATALOG['problems'][0]
        result=json.loads(judge('bv',p['solution'].replace('    qc.x(n)\n',''),'run'))
        self.assertEqual(result['status'],'WA')

    def test_bv_does_not_solve_equality_search(self):
        result=json.loads(judge('grover',CATALOG['problems'][0]['solution'],'run'))
        self.assertEqual(result['status'],'WA')

    def test_query_budget(self):
        source=CATALOG['problems'][0]['solution'].replace('    qc.h(range(n))','    oracle(qc, range(n), n)\n    qc.h(range(n))')
        self.assertEqual(json.loads(judge('bv',source,'run'))['status'],'QRE')

    def test_grover_reference_probability(self):
        result=json.loads(judge('grover',CATALOG['problems'][2]['solution'],'run'))
        self.assertAlmostEqual(result['worst_success'],.9453125,places=10)

    def test_no_arbitrary_user_execution(self):
        sources=["import os\ndef solve(n, oracle):\n    return QuantumCircuit(n+1)",
                 "def solve(n, oracle):\n    return __import__(1)",
                 "def solve(n, oracle):\n    return oracle.__class__",
                 "@oracle\ndef solve(n, oracle):\n    return QuantumCircuit(n+1)",
                 "def solve(n, oracle):\n    while True:\n        pass"]
        for source in sources:
            with self.assertRaises(VerdictError):compile_solution(source,3)

    def test_budget_and_gates(self):
        fixtures=[('QLE','qc = QuantumCircuit(n+2)\n    return qc'),
                  ('UGE','qc = QuantumCircuit(n+1)\n    qc.measure(0,0)\n    return qc'),
                  ('DLE','qc = QuantumCircuit(n+1)\n    for i in range(256):\n        qc.h(0)\n        qc.h(0)\n        qc.h(0)\n    return qc'),
                  ('TLE','qc = QuantumCircuit(n+1)\n    for i in range(256):\n        for j in range(256):\n            pass\n    return qc'),
                  ('RE','qc = QuantumCircuit(n+1)\n    qc.cx(0,0)\n    return qc')]
        for expected,body in fixtures:
            with self.subTest(status=expected):
                result=json.loads(judge('bv','def solve(n, oracle):\n    '+body,'run'))
                self.assertEqual(result['status'],expected,result)


if __name__=='__main__':unittest.main()
