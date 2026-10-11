/* Python parsing/building is in a worker; the student's source is never exec'd. */
importScripts('./simulator.js');
let boot;
async function initialize() {
  postMessage({stage:'Loading Python runtime (first run only)…'});
  importScripts('https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js');
  const py = await loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.28.3/full/'});
  const response = await fetch('./qcp/solver.py');
  if (!response.ok) throw Error('Could not load the circuit-building interpreter.');
  py.FS.writeFile('/solver.py', await response.text());
  py.runPython('import sys; sys.path.insert(0, "/"); from solver import compile_batch; import json');
  const cases = await (await fetch('./cases.json')).json();
  return {py,cases};
}
onmessage = async event => {
  try {
    boot ||= initialize().catch(e => { boot = null; throw e; });
    const {py,cases} = await boot;
    postMessage({stage:'Building circuits and checking oracle budgets…'});
    py.globals.set('student_source', event.data.source);
    const selected = event.data.mode === 'run' ? cases[event.data.problem].filter(c=>c.sample) : cases[event.data.problem];
    py.globals.set('build_sizes', JSON.stringify([...new Set(selected.map(c=>c.n))]));
    const compiled = JSON.parse(py.runPython('compile_batch(student_source, json.loads(build_sizes))'));
    py.globals.delete('student_source');
    if (compiled.status) { postMessage({result:compiled}); return; }
    postMessage({stage:'Checking the public test suite…'});
    postMessage({result:QCPSim.judge(event.data.problem, compiled.circuits, cases[event.data.problem], event.data.mode)});
  } catch (e) { postMessage({result:{status:'JE',message:`Runtime unavailable: ${e.message}. Retry or use the Qollab package / local CLI. This attempt has no contest penalty.`,source:'Browser runtime'}}); }
};
