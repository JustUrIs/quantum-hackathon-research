/* Ideal reference simulator for browser practice. Qollab uses Qiskit instead. */
(function () {
  const V = 'qcp-1.0';
  function metrics(ir, n, problem) {
    const queries = ir.ops.filter(o => o[0] === 'oracle').length;
    const cap = problem === 'grover' ? Math.floor(Math.PI / 4 * Math.sqrt(2 ** n)) : 1;
    const layers = Array(ir.width).fill(0);
    let two = 0;
    for (const [name, qs] of ir.ops) {
      const layer = 1 + Math.max(...qs.map(q => layers[q]));
      qs.forEach(q => { layers[q] = layer; });
      if (name !== 'oracle' && qs.length === 2) two++;
    }
    if (queries > cap) throw {status: 'QRE', message: `n=${n}: ${queries} oracle calls; limit ${cap}.`};
    if (Math.max(...layers) > 256) throw {status: 'DLE', message: `n=${n}: logical depth ${Math.max(...layers)}; limit 256.`};
    return {qubits: ir.width, queries, query_limit: cap, logical_depth: Math.max(...layers), logical_instructions: ir.ops.length, explicit_two_qubit_gates: two};
  }
  function simulate(ir, fixture) {
    const size = 2 ** ir.width, r = new Float64Array(size), im = new Float64Array(size);
    r[0] = 1;
    function phase(i, angle) {
      const a = r[i], b = im[i], c = Math.cos(angle), s = Math.sin(angle);
      r[i] = a*c - b*s; im[i] = a*s + b*c;
    }
    function single(q, m) {
      const bit = 1 << q;
      for (let a = 0; a < size; a++) if (!(a & bit)) {
        const b = a | bit, ar = r[a], ai = im[a], br = r[b], bi = im[b];
        r[a] = m[0]*ar - m[1]*ai + m[2]*br - m[3]*bi;
        im[a] = m[0]*ai + m[1]*ar + m[2]*bi + m[3]*br;
        r[b] = m[4]*ar - m[5]*ai + m[6]*br - m[7]*bi;
        im[b] = m[4]*ai + m[5]*ar + m[6]*bi + m[7]*br;
      }
    }
    for (const [name, qs, params] of ir.ops) {
      const q = qs[0], a = params[0], h = Math.SQRT1_2;
      if (name === 'oracle') {
        const bit = 1 << fixture.n, mask = bit - 1;
        for (let i = 0; i < size; i++) if (!(i & bit)) {
          const x = i & mask;
          let f;
          if (fixture.kind === 'bv') {
            let p = x & fixture.secret; f = 0;
            while (p) { f ^= 1; p &= p-1; }
          } else f = fixture.kind === 'grover' ? Number(x === fixture.secret) : fixture.table[x];
          if (f) { const j = i | bit; [r[i],r[j]] = [r[j],r[i]]; [im[i],im[j]] = [im[j],im[i]]; }
        }
      } else if (name === 'h') single(q, [h,0,h,0,h,0,-h,0]);
      else if (name === 'x') single(q, [0,0,1,0,1,0,0,0]);
      else if (name === 'y') single(q, [0,0,0,-1,0,1,0,0]);
      else if (name === 'rx') single(q, [Math.cos(a/2),0,0,-Math.sin(a/2),0,-Math.sin(a/2),Math.cos(a/2),0]);
      else if (name === 'ry') single(q, [Math.cos(a/2),0,-Math.sin(a/2),0,Math.sin(a/2),0,Math.cos(a/2),0]);
      else if (name === 'rz') {
        for (let i = 0; i < size; i++) phase(i, (i & (1<<q)) ? a/2 : -a/2);
      } else if (['z','s','sdg','t','tdg','p'].includes(name)) {
        const angles = {z: Math.PI, s: Math.PI/2, sdg: -Math.PI/2, t: Math.PI/4, tdg: -Math.PI/4, p: a};
        for (let i = 0; i < size; i++) if (i & (1<<q)) phase(i, angles[name]);
      } else if (['cx','ccx','mcx'].includes(name)) {
        const target = 1 << qs[qs.length - 1];
        const mask = qs.slice(0,-1).reduce((x,y)=>x|(1<<y), 0);
        for (let i = 0; i < size; i++) if (!(i & target) && (i & mask) === mask) {
          const j = i | target; [r[i],r[j]]=[r[j],r[i]]; [im[i],im[j]]=[im[j],im[i]];
        }
      } else if (['cz','mcp'].includes(name)) {
        const mask = qs.reduce((x,y)=>x|(1<<y), 0);
        for (let i = 0; i < size; i++) if ((i & mask) === mask) phase(i, name === 'cz' ? Math.PI : a);
      } else if (name === 'swap') {
        const b1 = 1<<qs[0], b2 = 1<<qs[1];
        for (let i = 0; i < size; i++) if (!(i & b1) && (i & b2)) {
          const j = i ^ b1 ^ b2; [r[i],r[j]]=[r[j],r[i]]; [im[i],im[j]]=[im[j],im[i]];
        }
      } else throw {status:'UGE', message:`Unsupported gate ${name}`};
    }
    const probs = Array(2 ** fixture.n).fill(0);
    for (let i = 0; i < size; i++) probs[i & (probs.length-1)] += r[i]*r[i] + im[i]*im[i];
    return probs;
  }
  function judge(problem, circuits, allCases, mode) {
    const start = performance.now();
    try {
      const cases = mode === 'run' ? allCases.filter(c => c.sample) : allCases;
      const checked = {}, rows = [];
      let worst = 1, failed = null, sample = null;
      for (let i = 0; i < cases.length; i++) {
        const c = cases[i], ir = circuits[c.n];
        if (!checked[c.n]) checked[c.n] = metrics(ir, c.n, problem);
        const probs = simulate(ir, c);
        const constant = c.kind === 'dj' && c.table.every(x => x === c.table[0]);
        const success = c.kind === 'dj' ? (constant ? probs[0] : 1-probs[0]) : probs[c.secret];
        const passed = success >= (problem === 'grover' ? 0.9 : 1-1e-9) - 1e-12;
        const row = {case:i+1, n:c.n, success, passed};
        rows.push(row); worst = Math.min(worst, success);
        if (!passed && !failed) failed = {...row, fixture:c, probabilities:probs};
        if (!sample) sample = {fixture:c, probabilities:probs};
      }
      return {status:failed?'WA':'AC', problem, mode, version:V, source:'Python subset + browser ideal simulator',
        total:cases.length, passed:rows.filter(r=>r.passed).length, worst_success:worst, failed, sample,
        rows, metrics:checked, elapsed_ms:Math.round(performance.now()-start), circuits};
    } catch (e) { return {status:e.status||'RE', message:e.message, source:'Browser practice judge', version:V}; }
  }
  globalThis.QCPSim = {simulate, judge, metrics};
})();
