"""Exercise real Python browser execution, Qiskit parity, and contest accounting."""
import json
import random
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from qiskit.quantum_info import Statevector

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qcp-qollab'))
from qcp.service import build
CAT=json.loads((ROOT/'qcp-qollab/catalog.json').read_text(encoding='utf-8'))
CASES=json.loads((ROOT/'qcp-qollab/cases.json').read_text(encoding='utf-8'))


def run_solution(page, source, action='Submit solution'):
    page.locator('#code').fill(source)
    page.get_by_role('button',name=action,exact=True).click()
    page.wait_for_function("document.querySelector('#result h2') !== null",timeout=120000)
    return page.locator('#result h2').inner_text()


with sync_playwright() as pw:
    browser=pw.chromium.launch()
    errors=[]
    page=browser.new_page(viewport={'width':1280,'height':900})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8771/#problem/bv')
    page.wait_for_selector('#code')
    page.screenshot(path=str(ROOT/'artifacts/qcp-desktop.png'),full_page=True)
    assert 'WA' in run_solution(page,CAT['problems'][0]['template'],'Run examples')
    assert 'AC' in run_solution(page,CAT['problems'][0]['solution'])
    assert '124/124' in page.locator('#result').inner_text()
    assert 'Qiskit' in page.locator('#result').inner_text()
    page.get_by_text('Show every test result (124)',exact=True).click()
    assert len(page.locator('#result details').nth(1).locator('tbody tr').all())==124
    page.goto('http://127.0.0.1:8771/#contest')
    page.locator('#participant').fill('Local competitor')
    page.locator('#startContest').click()
    page.goto('http://127.0.0.1:8771/#problem/bv')
    assert page.locator('details.editorial').count()==0
    assert 'CE' in run_solution(page,'def solve(')
    assert 'WA' in run_solution(page,CAT['problems'][0]['template'])
    assert 'WA' in run_solution(page,CAT['problems'][0]['template'],'Run examples')
    assert 'AC' in run_solution(page,CAT['problems'][0]['solution'])
    page.goto('http://127.0.0.1:8771/#contest')
    assert '+1 (0m)' in page.locator('#content').inner_text()
    assert page.locator('tbody tr td').nth(2).inner_text()=='20'
    page.reload()
    assert page.locator('#contestClock').inner_text()!='Not started'
    page.locator('#endContest').click()
    page.goto('http://127.0.0.1:8771/#problem/bv')
    assert page.locator('details.editorial').count()==1
    assert page.locator('#code').input_value()==CAT['problems'][0]['solution']
    for p in CAT['problems'][1:]:
        page.goto('http://127.0.0.1:8771/#problem/'+p['id'])
        assert 'AC' in run_solution(page,p['solution'])
        assert f"{p['test_count']}/{p['test_count']}" in page.locator('#result').inner_text()
    page.goto('http://127.0.0.1:8771/#submissions')
    page.locator('[data-receipt]').first.click()
    with page.expect_download() as event:page.locator('#exportReceipt').click()
    assert event.value.suggested_filename.endswith('-report.json')
    page.goto('http://127.0.0.1:8771/#problem/bv')
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(ROOT/'artifacts/qcp-mobile.png'),full_page=True)

    # The public site really builds Python solutions in Pyodide; no fake receipts.
    web=browser.new_page(viewport={'width':1280,'height':900})
    web.on('pageerror',lambda e:errors.append(str(e)))
    web.goto('http://127.0.0.1:8772/#problem/bv')
    web.wait_for_selector('#code')
    assert 'AC' in run_solution(web,CAT['problems'][0]['solution'])
    assert 'Python subset + browser ideal simulator' in web.locator('#result').inner_text()
    assert '124/124' in web.locator('#result').inner_text()
    assert 'CE' in run_solution(web,'import os\ndef solve(n, oracle):\n    return QuantumCircuit(n+1)')
    for p in CAT['problems'][1:]:
        web.goto('http://127.0.0.1:8772/#problem/'+p['id'])
        assert 'AC' in run_solution(web,p['solution'])
    web.goto('http://127.0.0.1:8772/#problem/bv')
    assert 'WA' in run_solution(web,CAT['problems'][0]['solution'].replace('    qc.x(n)\n',''))
    # Cross-check every supported gate family against Qiskit on varied states.
    web.add_script_tag(path=str(ROOT/'qcp-qollab/simulator.js'))
    rng=random.Random(11026)
    comparisons=[]
    names=['h','x','y','z','s','sdg','t','tdg','rx','ry','rz','p','cx','cz','swap','ccx','mcx','mcp']
    for index in range(40):
        n=2+index%4
        ops=[['h',[q],[]] for q in range(n+1)]
        for _ in range(20):
            name=rng.choice(names);angle=rng.uniform(-3,3)
            count=3 if name in ('ccx','mcx','mcp') else 2 if name in ('cx','cz','swap') else 1
            qs=rng.sample(range(n+1),count)
            params=[angle] if name in ('rx','ry','rz','p','mcp') else []
            ops.append([name,qs,params])
        ops.append(['oracle',list(range(n+1)),[]])
        fixture={'kind':'bv','n':n,'secret':rng.randrange(1<<n)}
        ir={'width':n+1,'ops':ops}
        expected=Statevector.from_instruction(build(ir,fixture)).probabilities(list(range(n))).tolist()
        actual=web.evaluate('([ir,c])=>QCPSim.simulate(ir,c)',[ir,fixture])
        delta=max(abs(a-b) for a,b in zip(expected,actual))
        assert delta<1e-10, (index,delta)
        comparisons.append(delta)
    assert not errors,errors
    print(json.dumps({'ui':'passed','browser_python':'passed','contest_penalties':'passed','gate_comparisons':40,'max_probability_error':max(comparisons),'mobile_overflow':False}))
    browser.close()
