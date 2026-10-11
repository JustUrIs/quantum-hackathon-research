"""python tools/qcp_cli.py bv solution.py --examples"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'qcp-qollab'))
from qcp.service import judge

ap=argparse.ArgumentParser(description='Evaluate a QCP Arena solution locally with Qiskit.')
ap.add_argument('problem',choices=['bv','dj','grover'])
ap.add_argument('source',type=Path)
ap.add_argument('--examples',action='store_true')
ap.add_argument('--report',type=Path)
opts=ap.parse_args()
result=judge(opts.problem,opts.source.read_text(encoding='utf-8'),'run' if opts.examples else 'submit')
if opts.report:opts.report.write_text(result+'\n',encoding='utf-8')
value=json.loads(result)
print(value['status'],f"{value.get('passed',0)}/{value.get('total',0)} cases",value.get('message',''))
print(value['source'])
sys.exit(0 if value['status']=='AC' else 1)
