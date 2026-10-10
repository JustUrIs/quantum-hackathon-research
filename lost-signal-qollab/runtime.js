// Copied into each upload: no dependency outside the project folder.
export const $ = (id) => document.getElementById(id);
export const percent = (x) => (100 * x).toFixed(1) + "%";
export const number = (x, d = 2) => Number(x).toFixed(d);
export const escapeHTML = (text) =>
  String(text).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
export function chart(
  svg,
  series,
  { xmin = 0, xmax = 1, ymin = 0, ymax = 1, xlabel = "", ylabel = "" } = {},
) {
  const w = 640,
    h = 240,
    l = 54,
    r = 18,
    t = 18,
    b = 42;
  const x = (v) => l + ((v - xmin) / (xmax - xmin)) * (w - l - r),
    y = (v) => h - b - ((v - ymin) / (ymax - ymin)) * (h - t - b);
  let s = "";
  for (let j = 0; j <= 4; j++) {
    const v = ymin + ((ymax - ymin) * j) / 4;
    s += `<line class="grid" x1="${l}" x2="${w - r}" y1="${y(v)}" y2="${y(v)}"/><text x="${l - 8}" y="${y(v) + 4}" text-anchor="end">${v.toFixed(ymax > 10 ? 0 : 2)}</text>`;
  }
  for (let j = 0; j <= 4; j++) {
    const v = xmin + ((xmax - xmin) * j) / 4;
    s += `<text x="${x(v)}" y="${h - b + 19}" text-anchor="middle">${v.toFixed(xmax > 10 ? 0 : 1)}</text>`;
  }
  series.forEach((a) => {
    s += `<polyline fill="none" stroke="${a.color}" stroke-width="3" ${a.dash ? 'stroke-dasharray="6 5"' : ""} points="${a.values.map((v) => `${x(v[0])},${y(v[1])}`).join(" ")}"/>`;
  });
  s += `<text x="${l}" y="12">${escapeHTML(ylabel)}</text><text x="${w - r}" y="${h - 2}" text-anchor="end">${escapeHTML(xlabel)}</text>`;
  svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
  svg.innerHTML = s;
}
export function connect(svc, selectedBackend) {
  let spent = false,
    evidence = null,
    latest = null,
    busy = false,
    pending = null;
  const extra = {};
  const py = async (name, ...args) =>
    JSON.parse(String(await svc[name].callPromising(...args)));
  const fail = (e) => {
    $("status").textContent =
      "Could not finish: " + (e.message || e) + ". Adjust a control to retry.";
    $("status").dataset.error = "true";
  };
  async function update(params, render) {
    pending = { params, render };
    if (busy) return;
    busy = true;
    while (pending) {
      const next = pending;
      pending = null;
      $("status").textContent = "Calculating experiment…";
      delete $("status").dataset.error;
      try {
        const data = await py("evaluate", JSON.stringify(next.params));
        if (!pending) {
          latest = data;
          next.render(data);
          $("status").textContent =
            "Local model ready. Backend evidence is a separate experiment.";
        }
      } catch (e) {
        fail(e);
      }
    }
    busy = false;
  }
  function wireAudit(params) {
    $("runBackend").onclick = async () => {
      if (spent) return;
      const snapshot = JSON.parse(JSON.stringify(params()));
      const button = $("runBackend");
      button.disabled = true;
      $("auditStatus").textContent = "Building the circuit for this snapshot…";
      try {
        if (!selectedBackend) throw new Error("No Qollab backend is connected");
        const circuit = await svc.audit_circuit.callPromising(
          JSON.stringify(snapshot),
        );
        const name = String(selectedBackend.name || "selected backend");
        const shots = /ionq/i.test(name) ? 100 : 1024;
        spent = true;
        $("auditStatus").textContent =
          `Running ${circuit.num_qubits} qubits × ${shots} shots on ${name}. Remote simulators can take several minutes.`;
        const job = await selectedBackend.run(circuit, { shots });
        const result = await job.result();
        const raw = result.get_counts();
        const values = raw?.toJs ? raw.toJs() : raw;
        const counts =
          values instanceof Map ? Object.fromEntries(values) : values;
        const report = await py(
          "ingest_audit",
          JSON.stringify(counts),
          JSON.stringify(snapshot),
        );
        evidence = {
          backend: name,
          recorded_at: new Date().toISOString(),
          params: snapshot,
          report,
        };
        $("auditStatus").textContent =
          `Completed ${report.shots} shots on ${name}. Evidence belongs to the snapshot below; moving controls does not rerun it.`;
        $("auditOutput").textContent = JSON.stringify(evidence, null, 2);
        $("auditDetails").open = true;
        button.textContent = "Backend job used. Restart Qollab to run again.";
      } catch (e) {
        $("auditStatus").textContent =
          "Backend check failed: " +
          (e.message || e) +
          ". Local model remains available. " +
          (spent ? "Restart Qollab for a fresh job." : "You can retry.");
        button.disabled = spent;
      }
    };
    $("export").onclick = () => {
      $("exportOutput").value = JSON.stringify(
        {
          schema: "quantum-hackathon/1",
          created_at: new Date().toISOString(),
          local_model: latest,
          backend_evidence: evidence,
          additional_experiments: extra,
        },
        null,
        2,
      );
      $("exportDetails").open = true;
      $("exportOutput").focus();
      $("exportOutput").select();
    };
  }
  return {
    py,
    update,
    wireAudit,
    fail,
    setExtraEvidence: (key, value) => {
      extra[key] = value;
    },
  };
}
