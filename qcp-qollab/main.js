import {run, cancel} from './runtime.js';

const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const storageKey = 'qcp-arena-1';
let state;
try { state = JSON.parse(localStorage.getItem(storageKey)) || {}; } catch { state={}; }
state.drafts ||= {}; state.history ||= []; state.contest ||= null;
let catalog, busy=false, current=null, lastReport=null;
const save = () => { try { localStorage.setItem(storageKey,JSON.stringify(state)); } catch { $('roundState').textContent='Storage unavailable; keep this tab open.'; } };
const cards = () => catalog.problems;
const card = id => cards().find(p=>p.id===id);
const contestLive = () => state.contest && Date.now() < state.contest.started + 60*60*1000 && !state.contest.ended;
const pct = x => `${(100*x).toFixed(6)}%`;
const link = p => `<a href="#problem/${p.id}">${p.letter}. ${esc(p.title)}</a>`;
function clock() {
  if (!state.contest) return 'Not started';
  if (!contestLive()) return 'Finished';
  const seconds = Math.max(0,Math.ceil((state.contest.started+3600000-Date.now())/1000));
  return `${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`;
}
function updateChrome() {
  $('problemLinks').innerHTML=cards().map(p=>`<a class="problem-link" href="#problem/${p.id}">${p.letter}. ${esc(p.title)}<span>${state.history.some(h=>h.problem===p.id&&h.mode==='submit'&&h.status==='AC')?'✓':''}</span></a>`).join('');
  $('roundState').textContent=state.contest?`Your round: ${clock()}`:'Virtual participation';
  const el=$('contestClock'); if(el)el.textContent=clock();
  document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a.hash===location.hash||a.hash==='#catalog'&&location.hash.startsWith('#problem/')));
}
function section(title,text) { return `<h2 class="section-title">${title}</h2><p>${esc(text)}</p>`; }
function renderProblem(p) {
  current=p.id;
  const locked = contestLive();
  $('content').innerHTML=`
    <div class="subnav"><a href="#catalog">Problems</a><a href="#submissions">My submissions</a><a href="#contest">Virtual standings</a></div>
    <div class="problem-head"><h1>${p.letter}. ${esc(p.title)}</h1><p>${esc(p.query_limit)}</p><p>Ideal success: ${p.id==='grover'?'at least 90%':'at least 1 − 10⁻⁹'} · ${p.test_count} public test cases</p></div>
    <article class="statement"><p>${esc(p.story)}</p>${section('Task',p.task)}${section('Input',p.input)}${section('Output',p.output)}${section('Interface',p.interface)}${section('Constraints',p.limits)}
    <h2 class="section-title">Example</h2><pre class="sample">${esc(p.sample)}</pre>
    <div class="notice"><strong>What is actually better than classical?</strong><p>${esc(p.comparison)}</p></div>
    <details><summary>Encoding and test coverage</summary><p>${esc(p.encoding)}</p><p>${esc(p.coverage)}</p><p class="small">This public suite checks the listed cases, not correctness for arbitrarily large inputs.</p></details></article>
    <section class="editor-panel" aria-label="Solution editor"><div class="editor-head"><h2>Python / Qiskit circuit builder</h2><button id="resetCode">Restore starter</button></div>
    <div class="editor-wrap"><pre class="gutter" id="gutter" aria-hidden="true"></pre><textarea id="code" aria-label="Python solution" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off"></textarea></div>
    <div class="editor-foot"><div class="actions"><button class="secondary" id="runCode">Run examples</button><button class="primary" id="submitCode">Submit solution</button><button class="text" id="cancelRun" hidden>Cancel</button><a href="#about">Supported Python</a><button class="text" id="downloadCode">Download .py</button></div>
    <p class="progress" id="progress" role="status" aria-live="polite">${locked?'Submissions count toward your virtual round.':'Practice mode. Drafts are saved on this device.'} Ctrl+Enter: Run. Ctrl+Shift+Enter: Submit.</p></div></section>
    <div id="result" aria-live="polite"></div>
    ${locked?'<p class="small">Editorials unlock when your virtual round ends.</p>':`<details class="editorial"><summary>Editorial and reference solution</summary><p>${esc(p.editorial)}</p><pre class="source-code">${esc(p.solution)}</pre><a href="${esc(p.reference)}" target="_blank" rel="noopener">Algorithm reference</a><p class="small">The reference is for studying after you attempt the problem. It is intentionally public in this practice demo.</p></details>`}`;
  $('code').value=state.drafts[p.id] ?? p.template;
  function lines() { $('gutter').textContent=Array.from({length:$('code').value.split('\n').length},(_,i)=>i+1).join('\n'); }
  lines();
  $('code').addEventListener('input',()=>{state.drafts[p.id]=$('code').value;save();lines();});
  $('code').addEventListener('scroll',()=>{$('gutter').scrollTop=$('code').scrollTop;});
  $('code').addEventListener('keydown',e=>{
    if(e.key==='Tab') { e.preventDefault(); const el=e.target,start=el.selectionStart,end=el.selectionEnd; el.setRangeText('    ',start,end,'end'); el.dispatchEvent(new Event('input')); }
    if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)) {e.preventDefault();execute(e.shiftKey?'submit':'run');}
  });
  $('runCode').onclick=()=>execute('run'); $('submitCode').onclick=()=>execute('submit');
  $('cancelRun').onclick=cancel;
  $('resetCode').onclick=()=>{if(confirm('Replace this problem’s saved draft with the starter?')){$('code').value=p.template;$('code').dispatchEvent(new Event('input'));}};
  $('downloadCode').onclick=()=>download(`qcp-${p.id}.py`,$('code').value,'text/x-python');
  syncBusy();
}
function syncBusy() {
  for(const id of ['runCode','submitCode','resetCode']) if($(id))$(id).disabled=busy;
  if($('cancelRun'))$('cancelRun').hidden=!busy||Boolean(globalThis.QCPJudge);
}
function download(name,value,type='application/json') {
  const url=URL.createObjectURL(new Blob([value],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
async function digest(source) {
  if(!crypto.subtle)return 'Unavailable on this origin';
  const bytes=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(source));
  return Array.from(new Uint8Array(bytes),b=>b.toString(16).padStart(2,'0')).join('');
}
async function execute(mode) {
  if(busy||!current)return;
  const problem=current,source=$('code').value,submitted=Date.now(),contest=contestLive()?state.contest.id:null;
  busy=true;syncBusy();$('progress').textContent='Starting judge…';$('result').innerHTML='';
  let result;
  try {result=await run({problem,source,mode},stage=>{if(current===problem&&$('progress'))$('progress').textContent=stage;});}
  catch(e){result={status:'JE',message:e.message,source:'Judge unavailable'};}
  const receipt=await digest(source).catch(()=> 'Unavailable');
  busy=false;syncBusy();
  const item={id:state.history.length+1,problem,mode,status:result.status,submitted,contest,source,result,receipt};
  state.history.push(item);save();lastReport=item;
  if(current===problem&&$('result')) {renderResult(item);$('progress').textContent='Judging complete. Results are local to this device.';}
  else if(location.hash==='#submissions')renderHistory();
  else if(location.hash==='#contest')renderContest();
  updateChrome();
}
function diagram(ir) {
  if(!ir)return '';
  const ops=ir.ops.slice(0,24), width=80+ops.length*42, height=35+ir.width*30;
  let svg=`<svg viewBox="0 0 ${width} ${height}" style="width:${width}px" role="img" aria-label="Circuit instructions, with oracle shown as a black box">`;
  for(let q=0;q<ir.width;q++)svg+=`<text x="3" y="${29+q*30}" font-size="11" fill="#596779">q${q}</text><line x1="28" y1="${25+q*30}" x2="${width-8}" y2="${25+q*30}" stroke="#c5cfdd"/>`;
  ops.forEach(([name,qs],i)=>{
    const x=48+i*42;
    if(name==='oracle')svg+=`<rect x="${x-13}" y="13" width="29" height="${(ir.width-1)*30+25}" fill="#edf2f9" stroke="#24579b"/><text transform="translate(${x+5},${height/2}) rotate(-90)" text-anchor="middle" fill="#24579b" font-size="10">U_f</text>`;
    else {
      if(qs.length>1)svg+=`<line x1="${x}" y1="${25+Math.min(...qs)*30}" x2="${x}" y2="${25+Math.max(...qs)*30}" stroke="#24579b"/>`;
      qs.forEach(q=>{svg+=`<rect x="${x-13}" y="${14+q*30}" width="26" height="22" fill="white" stroke="#24579b"/><text x="${x}" y="${29+q*30}" text-anchor="middle" font-size="9" fill="#24579b">${esc(name)}</text>`;});
    }
  });
  return `<div class="diagram">${svg}</svg></div><p class="small">${ir.ops.length>24?'First 24 instructions shown. ':''}Oracle implementation stays outside the submitted builder. These are logical instructions, not a hardware layout.</p>`;
}
function renderResult(item) {
  const r=item.result,p=card(item.problem),good=r.status==='AC',sampleOnly=item.mode==='run';
  let body=`<section class="result"><h2 class="${good?'accepted':'rejected'}">${esc(r.status)} — ${good?(sampleOnly?'Examples passed':'Accepted'):({'WA':'Wrong answer','CE':'Compilation error','RE':'Runtime error','TLE':'Time limit exceeded','QLE':'Qubit limit exceeded','DLE':'Depth limit exceeded','QRE':'Oracle query limit exceeded','UGE':'Unauthorized gate','JE':'Judge unavailable','CANCELLED':'Cancelled'}[r.status]||'Judge error')}</h2><p class="small">${esc(r.source||'Circuit builder')} · ${esc(r.version||catalog.version)}${sampleOnly?' · Example checks only; not a submission verdict.':''}</p>`;
  if(r.message)body+=`<p>${esc(r.message)}</p>`;
  if(r.total!==undefined) {
    body+=`<div class="metrics"><span><strong>${r.passed}/${r.total}</strong> cases passed</span><span>Worst success <strong>${pct(r.worst_success)}</strong></span><span>${r.elapsed_ms} ms simulation/check time</span></div>`;
    if(r.failed) {
      const f=r.failed;
      body+=`<div class="notice"><strong>First counterexample: case ${f.case}, n = ${f.n}</strong><p>Success probability ${pct(f.success)}. Required: ${p.id==='grover'?'90%':'1 − 10⁻⁹'}.</p><details><summary>Inspect this public fixture</summary><pre class="source-code">${esc(JSON.stringify(f.fixture,null,2))}</pre></details></div>`;
    }
    body+=`<details><summary>Resource report</summary><div class="table-scroll"><table><thead><tr><th>n</th><th>Qubits</th><th>Queries / limit</th><th>Logical depth</th><th>Instructions</th></tr></thead><tbody>${Object.entries(r.metrics).map(([n,m])=>`<tr><td>${n}</td><td>${m.qubits}</td><td>${m.queries} / ${m.query_limit}</td><td>${m.logical_depth}</td><td>${m.logical_instructions}</td></tr>`).join('')}</tbody></table></div><p class="small">Oracle calls count as one logical instruction. Building the oracle is not free in hardware. ${r.representative?`For the first fixture, Qiskit decomposition to u/cx at optimization level 0 gives ${r.representative.cx} CX gates and depth ${r.representative.depth}, including the oracle.`:'Browser metrics describe logical instructions; no physical gate decomposition is claimed.'}</p></details>`;
    body+=`<details><summary>Show every test result (${r.total})</summary><div class="table-scroll"><table><thead><tr><th>Case</th><th>n</th><th>Success probability</th><th>Verdict</th></tr></thead><tbody>${r.rows.map(row=>`<tr><td>${row.case}</td><td>${row.n}</td><td>${pct(row.success)}</td><td class="${row.passed?'accepted':'rejected'}">${row.passed?'PASS':'FAIL'}</td></tr>`).join('')}</tbody></table></div></details>`;
    const ir=r.circuits?.['3']||Object.values(r.circuits||{})[0];
    body+=`<details><summary>Inspect the submitted circuit</summary>${diagram(ir)}</details>`;
  }
  body+=`<p class="receipt">Source SHA-256: ${esc(item.receipt)}</p><button class="secondary" id="exportReceipt">Download judge report</button></section>`;
  $('result').innerHTML=body;
  $('exportReceipt').onclick=()=>download(`qcp-${p.id}-report.json`,JSON.stringify(item,null,2));
}
function renderCatalog() {
  $('content').innerHTML=`<h1>Problemset</h1><p>Three problems about doing more with fewer oracle calls. Each has a complete statement, an ideal checker and a public test suite.</p><div class="table-scroll"><table><thead><tr><th>Problem</th><th>Title</th><th>Task</th><th>Tests</th><th>Progress</th></tr></thead><tbody>${cards().map(p=>`<tr class="catalog-row"><td>${p.letter}</td><td>${link(p)}</td><td>${esc(p.tag)}</td><td>${p.test_count}</td><td>${state.history.some(h=>h.problem===p.id&&h.mode==='submit'&&h.status==='AC')?'Accepted':'Unsolved'}</td></tr>`).join('')}</tbody></table></div><div class="notice"><strong>Start with problem A</strong><p>You write a function that constructs a circuit. The judge supplies the oracle and reads the result. No installation is needed for browser practice; the first run downloads Python.</p></div><a class="button" href="#problem/bv">Open problem A</a>`;
}
function score() {
  if(!state.contest)return {solved:0,penalty:0,cells:[]};
  let solved=0,penalty=0;
  const cells=cards().map(p=>{
    const rows=state.history.filter(h=>h.problem===p.id&&h.contest===state.contest.id&&h.mode==='submit'&&h.submitted<state.contest.started+3600000&&(!state.contest.ended||h.submitted<=state.contest.ended));
    const ac=rows.find(h=>h.status==='AC');
    const rejected=rows.filter(h=>!['AC','CE','CANCELLED','JE'].includes(h.status)&&(!ac||h.submitted<ac.submitted)).length;
    if(ac){solved++;penalty+=Math.floor((ac.submitted-state.contest.started)/60000)+20*rejected;}
    return ac?`+${rejected||''} (${Math.floor((ac.submitted-state.contest.started)/60000)}m)`:rejected?`−${rejected}`:'—';
  });
  return {solved,penalty,cells};
}
function renderContest() {
  const s=score();
  $('content').innerHTML=`<h1>QCP Round 001</h1><p>An individual, 60-minute virtual round. Solve A, B and C. Ranking uses solved count, then lower penalty.</p><div class="notice"><strong>Local virtual participation</strong><p>There is one participant on this device. Public tests and local storage cannot provide trusted global standings. This demo does not create a rating.</p></div><p>${esc(catalog.contest.scoring)}</p><p class="clock" id="contestClock">${clock()}</p>
    ${!state.contest?'<label for="participant">Display name</label><br><input id="participant" type="text" maxlength="32" value="Participant"><button class="primary" id="startContest">Start virtual round</button>':`<p>Participant: <strong>${esc(state.contest.name)}</strong></p>${contestLive()?'<button class="secondary" id="endContest">Finish round early</button>':'<button class="secondary" id="resetContest">Start a new round</button>'}`}
    <h2>Your standings</h2><div class="table-scroll"><table><thead><tr><th>Participant</th><th>Solved</th><th>Penalty</th>${cards().map(p=>`<th>${p.letter}</th>`).join('')}</tr></thead><tbody><tr><td>${esc(state.contest?.name||'Not entered')}</td><td>${s.solved}</td><td>${s.penalty}</td>${s.cells.length?s.cells.map(c=>`<td>${c}</td>`).join(''):'<td>—</td><td>—</td><td>—</td>'}</tr></tbody></table></div><h2>Problems</h2><p>${cards().map(link).join('<br>')}</p><p class="small">Editorials are hidden during an active round. They remain public in the package; this is an honor-based virtual contest.</p>`;
  if($('startContest'))$('startContest').onclick=()=>{state.contest={id:Date.now(),started:Date.now(),name:$('participant').value.trim()||'Participant'};save();renderContest();updateChrome();};
  if($('endContest'))$('endContest').onclick=()=>{state.contest.ended=Date.now();save();renderContest();updateChrome();};
  if($('resetContest'))$('resetContest').onclick=()=>{state.contest=null;save();renderContest();updateChrome();};
}
function renderHistory() {
  $('content').innerHTML=`<h1>My submissions</h1><p class="small">Stored on this device. Run examples is recorded separately and never counts toward contest penalties.</p>${state.history.length?`<div class="table-scroll"><table><thead><tr><th>#</th><th>Problem</th><th>Action</th><th>Verdict</th><th>Checks</th><th>Receipt</th></tr></thead><tbody>${state.history.slice().reverse().map(h=>`<tr><td>${h.id}</td><td>${link(card(h.problem))}</td><td>${h.mode==='run'?'Examples':'Submit'}</td><td class="${h.status==='AC'?'accepted':'rejected'}">${esc(h.status)}</td><td>${h.result.total!==undefined?`${h.result.passed}/${h.result.total}`:'—'}</td><td><button class="text" data-receipt="${h.id}">Open</button></td></tr>`).join('')}</tbody></table></div><div id="result"></div>`:'<div class="empty">No submissions yet. Open problem A, write a solution, and run the examples.</div><p><a href="#problem/bv">Open problem A</a></p>'}`;
  document.querySelectorAll('[data-receipt]').forEach(b=>b.onclick=()=>renderResult(state.history.find(h=>h.id===Number(b.dataset.receipt))));
}
function renderHandbook() {
  $('content').innerHTML=`<h1>A short competitor’s handbook</h1><p>For programmers comfortable with Python who are beginning to use Qiskit.</p><h2>1. You construct a circuit</h2><p>The judge starts the qubits at zero. Your function returns operations, not a printed answer. Qubit 0 is the least significant bit. Readout is added by the judge.</p><h2>2. Superposition is not a list of answers</h2><p>H creates amplitudes for different outcomes. You cannot read them all in one measurement. The useful step is interference: arrange the amplitudes so the answer becomes likely.</p><h2>3. A phase can change a later answer</h2><p>X swaps zero and one. Z changes the sign of the one amplitude. H, then Z, then H maps zero to one: probabilities alone would miss what Z did halfway through.</p><h2>4. The oracle is a contract</h2><p>All three problems provide U_f: |x,y> → |x,y XOR f(x)>. Preparing y in |−> turns a bit flip into a phase. A call counts once in the query model; implementing the oracle still costs hardware operations.</p><h2>5. Compare like with like</h2><p>A recovers a parity string exactly. B has a promise and compares against deterministic classical decision; randomized classical methods are much stronger than that baseline. C compares high-probability unstructured search. None of these browser runs proves quantum wall-clock advantage.</p><h2>6. Train deliberately</h2><p>Attempt A before reading its editorial. In B, explain why any nonzero readout is sufficient. In C, try one iteration too many and inspect the probability. Then test the full suite.</p><a href="#problem/bv" class="button">Start problem A</a>`;
}
function renderAbout() {
  $('content').innerHTML=`<h1>Judge specification</h1><p>Version <code>${catalog.version}</code>. Ideal, deterministic correctness checks. No hardware speedup or formal proof for untested inputs is claimed.</p><h2>Execution sources</h2><p>The public browser runs a bounded Python circuit-building interpreter in Pyodide and an independent JavaScript ideal simulator. It does not install Qiskit. The Qollab package uses the same builder and fixtures, then executes the circuits with Qiskit Statevector. Each report names its source.</p><h2>Supported Python</h2><p>One <code>solve(n, oracle)</code> function; assignments, bounded for loops, if/else, return, arithmetic, lists, ranges and indexing. Imports: <code>from qiskit import QuantumCircuit</code> and <code>import math</code>. Math: pi, e, sqrt, floor, ceil, sin, cos. Helpers: range, list, len, int, float, abs, min, max, round. This is a documented subset, not arbitrary Python execution.</p><h2>Supported circuit instructions</h2><p><code>h x y z s sdg t tdg rx ry rz p cx cz swap ccx mcx mcp barrier</code>. Use positional arguments. Single-qubit H/X/Y/Z/S/T variants accept ranges. No initialize, arbitrary unitary, statevector inspection or user measurement. Use <code>oracle(qc, range(n), n)</code> for the supplied oracle.</p><h2>Verdicts</h2><div class="table-scroll"><table><tbody>${[['AC','All evaluated cases passed. Run only covers examples.'],['WA','A semantic correctness check failed.'],['CE','Syntax or unsupported language feature.'],['RE','Invalid arguments, indexing or return value.'],['QLE','Qubit budget exceeded or wrong register size.'],['DLE','Logical depth or instruction budget exceeded.'],['QRE','Oracle query budget exceeded.'],['UGE','Instruction outside the supported gate set.'],['TLE','Builder budget or browser worker timeout exceeded.']].map(([a,b])=>`<tr><th>${a}</th><td>${b}</td></tr>`).join('')}</tbody></table></div><h2>Fairness and reproducibility</h2><p>Exact probabilities determine verdicts; a lucky shot does not pass a wrong circuit. Global phase does not affect the probability checks. Relative phases can affect interference and are preserved in simulation. Reports include source hash, version, per-case outcomes and resource metrics.</p><p>Fixtures are public. BV and Grover cover all secrets at the tested sizes; larger DJ tables are sampled. The user’s builder cannot access the oracle secret through its supported interface. A person controlling the browser can still modify the application: local results are practice receipts, not a tamper-proof credential.</p><h2>Next product milestone</h2><p>A trusted shared contest needs server-side judging and isolated execution. This edition establishes the problem contracts, checkers and competitor workflow before adding that infrastructure.</p>`;
}
function render() {
  current=null;
  const [view,id]=(location.hash.slice(1)||'problem/bv').split('/');
  if(view==='problem'&&card(id))renderProblem(card(id));
  else if(view==='contest')renderContest();
  else if(view==='submissions')renderHistory();
  else if(view==='handbook')renderHandbook();
  else if(view==='about')renderAbout();
  else renderCatalog();
  updateChrome();
}
try {
  if(globalThis.QCPCatalog)catalog=globalThis.QCPCatalog;
  else {const response=await fetch('./catalog.json');if(!response.ok)throw Error('Problem catalog could not be loaded.');catalog=await response.json();}
  $('mode').textContent=globalThis.QCPMode||'Browser practice';
  if(globalThis.QCPJudge)$('footerSource').textContent='Circuit correctness is evaluated with Qiskit on a local ideal simulator.';
  render();window.addEventListener('hashchange',render);
  setInterval(()=>{const wasLive=$('roundState').textContent.includes('Your round:')&&$('roundState').textContent!=='Your round: Finished';updateChrome();if(wasLive&&!contestLive()&&current)render();},1000);
} catch(e){$('content').innerHTML=`<div class="notice"><h1>Could not open the problemset</h1><p>${esc(e.message)}</p><p>Serve this folder over HTTP, or upload the Qollab ZIP. Opening index.html as file:// cannot load the judge assets.</p></div>`;}
