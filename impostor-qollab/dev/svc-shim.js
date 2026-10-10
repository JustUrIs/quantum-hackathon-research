// Dev-only stand-in for Qollab's Pyodide bridge: `svc.fn.callPromising(...)` -> HTTP -> Python.
const call = async (name, args) => {
  const r = await fetch(`/api/${name}`, { method: 'POST', body: JSON.stringify({ args }) });
  const t = await r.text();
  if (!r.ok) throw new Error(t);
  return t;
};
const fn = (name) => ({ callPromising: (...args) => call(name, args) });
export const overview = fn('overview');
export const play_chsh = fn('play_chsh');
export const play_magic = fn('play_magic');
export const zip_curve = fn('zip_curve');
export const zip_urandom = fn('zip_urandom');
export const ingest_audit = fn('ingest_audit');
export const audit_circuit = { callPromising: async () => JSON.parse(await call('audit_circuit', [])) };
globalThis.backend = { name: 'basic_simulator (dev harness)' };
// backend_run needs shots in the body
globalThis.backend.run = async (qc, opts) => {
  const r = await fetch('/api/backend_run', { method: 'POST', body: JSON.stringify({ shots: opts.shots }) });
  const counts = await r.json();
  return { result: async () => ({ get_counts: () => counts }) };
};
