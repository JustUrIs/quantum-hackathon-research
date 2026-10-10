const call = async (method, args) => {
  const r = await fetch("/__SLUG__/api/" + method, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ args }),
  });
  const text = await r.text();
  if (!r.ok) throw new Error(JSON.parse(text).error || text);
  return text;
};
const fn = (name) => ({ callPromising: (...args) => call(name, args) });
export const evaluate = fn("evaluate");
export const radical = fn("radical");
export const audit_counts = fn("audit_counts");
export const ingest_audit = fn("ingest_audit");
export const audit_circuit = {
  callPromising: async (...args) =>
    JSON.parse(await call("audit_circuit", args)),
};
globalThis.backend = {
  name: "BasicSimulator · local harness",
  run: async (qc, opts) => {
    const counts = JSON.parse(await call("backend_run", [opts.shots]));
    return { result: async () => ({ get_counts: () => counts }) };
  },
};
