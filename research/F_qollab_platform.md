# Front F: The Qollab platform, technically (runtime, UI, IonQ backend, competitors, terms)

Scanned 2026-10-10. Sources: the official docs at `qollab.xyz/learn/docs/*` (server-rendered and readable with curl), the Nuxt JS bundles, the **public project API `https://api.qollab.xyz/api/...`** (no auth needed for reads), public project source fetched through that API, the hackathon terms and how-it-works pages, and GitHub (udsy19/Qollab-Hackathon, almond-lab/Almond).
Confidence tags: **[DOC]** = stated in official Qollab docs. **[CODE]** = read in the Qollab JS bundle or in a public project's source. **[OBS]** = observed by a competitor team on the live platform (Qriollo/Truco COMPATIBILITY.md). **[UNVERIFIED]** = inferred.

---

## 1. How a Qollab project works

### 1.1 Runtime
- **Python runs on Pyodide (CPython compiled to WebAssembly) inside your browser.** The JavaScript of a JS project runs in the page, inside a **sandboxed iframe**. Nothing runs on a server except the quantum job itself, and that happens only on IonQ remote backends. [DOC runtime-environment]
- Python 3.14 with Qiskit 2.x and NumPy 2.x. [DOC python-qiskit-projects] A competitor's probe on the live platform reported **Python 3.14.2 and Qiskit 2.5.2**. [OBS]
- **Browser:** the runtime needs WebAssembly JSPI, which recent Chrome, Edge, Brave, Opera and Firefox 153+ support. **Safari does not, and neither does any iPhone or iPad browser.** Without JSPI, Run stays disabled. [DOC faq/how-it-works] The bundle checks `'promising' in WebAssembly`. [CODE]
- **No time limit on a run.** Stop gives Python 5 s to finish. [DOC]
- **Limits:** 100 files per project, 2 MB per file, 200 MB per account. Files larger than that must be streamed with GET `pyfetch`. [DOC]
- **No persistence.** A JS page has no localStorage, IndexedDB or cookies, and files Python writes vanish when the run ends. Ship saved state as project files, for example `data/*.json`. [DOC]
- **Network:** only GET (plus OPTIONS) requests, to CORS servers. Use `pyodide.http.pyfetch(url)` in Python or `fetch(url)` in JS. POST, XHR, WebSocket and web workers are blocked. JS-project requests carry `Origin: null`, so the server needs `Access-Control-Allow-Origin: *`. [DOC]
- **No keyboard `input()`** in Python. [DOC]

### 1.2 Project type and files
The type is decided from the **top-level** files every time someone presses Run. There is no setting for it. [DOC]

| Files at the top level | Type | Output |
|---|---|---|
| `index.html` + `main.js` (win even if `main.py` exists) | **JS / Qiskit project** | your HTML page renders **above the console** |
| `main.py` (and no index.html + main.js) | **Python / Qiskit project** | console only (stdout, figures, files) |
| neither | cannot run | Run disabled |

Other files:
- `requirements.txt` holds one spec per line, such as `name==1.2.3` or `name>=1,<2`. pip options, markers and URLs are refused. **Qiskit is always added** (`qiskit>=2.5.2,<3.0.0`) when the file doesn't list it. Packages that ship with Pyodide (NumPy, SciPy, Matplotlib and others) load on import without being listed. Any **pure-Python wheel from PyPI** installs, and so does any package with a Pyodide build. Compiled packages without a Pyodide build fail. [DOC]
- `main.css` is optional and is the only stylesheet loaded. `index.html` is **body content only**. `<html>`, `<head>` and `<body>` tags are stripped, and **`<script>` tags do not run**, so code goes in `main.js`. [DOC]
- `LICENSE` and `README.md`: a top-level `README.md` **becomes the project write-up** when you create a project by upload (65,000 characters max). On a later upload into an existing project it is skipped, and you paste the text into the write-up row instead. [DOC upload-your-files]
- Folders and multiple files are fine. Python imports work normally because the project root is on `sys.path`. JS imports use `./` paths. **`main.js` can import Python modules by dotted name**: `import * as bell from 'quantum.bell'`. [DOC]
- Data files: Python can read any project file **whose path appears as a literal string in the code** (for example `DATA = "data/x.csv"`). Paths built with f-strings, `+` or `os.path.join` are NOT loaded. **JS cannot read project files.** Read them in Python and return them to JS. [DOC]
- Download as ZIP: the bundle rewrites `main.py` to prepend a `BasicSimulator` or `IonQProvider` stub and adds RUNNING.md. A JS project's zip states that it "can only be run in Qollab environment". [CODE BWPMdZ7B.js]

### 1.3 The `backend` variable: how the IonQ simulator is selected
**Your code never picks the device.** The person who presses Run picks it in the **Select QPU dialog**, and the runtime injects it as a global named `backend`. Docs: "Do not create or hardcode a backend yourself, or the project ignores the choice." [DOC]

```python
# main.py ('backend' is pre-created as a global variable)
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2); qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1])
job = backend.run(qc, shots=1000)      # shots default = 1024 if omitted
print(job.result().get_counts())
```
```js
// main.js
import { QuantumCircuit } from 'qiskit';           // no `new`
const qc = QuantumCircuit(2, 2); qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1]);
const job = await backend.run(qc, { shots: 100 });
const counts = (await job.result()).get_counts().toJs();
```
- `backend` is a real provider object, not a wrapper:
  - The built-in simulator is Qiskit's `BasicSimulator`.
  - An IBM option is a `qiskit-ibm-runtime` Fake backend run on Aer.
  - An IonQ option is `IonQProvider`'s backend. On the live platform it was `backend.name == "ionq_simulator"`, from module `qiskit_ionq.ionq_backend`. [DOC, OBS]
- IonQ-specific run options work, for example `from qiskit_ionq import ErrorMitigation; backend.run(qc, shots=1000, error_mitigation=ErrorMitigation.NO_DEBIASING)`. [DOC error-mitigation]
- Internal QPU ids in the bundle are `":simulator:sim"` (built-in), `"aws:simulator:sim"`, `"ibm:<name>:sim"`, `"ionq:<qpu>:sim"` (IonQ remote noise-model simulator) and `"ionq:<qpu>"` (hardware). [CODE]
- **Auto-default:** if the code contains `job.get_counts(` or `job.get_probabilities(` (the qiskit-ionq job API), the dialog preselects **`ionq:forte-enterprise-1:sim`**. [CODE]
- Outside Qollab (local dev), the zip export uses `from qiskit.providers.basic_provider import BasicSimulator; backend = BasicSimulator()`. Alternatively: `from qiskit_ionq import IonQProvider; backend = IonQProvider(os.getenv('IONQ_API_KEY')).get_backend('simulator')`. [CODE]

### 1.4 Backends and noise models [DOC compute-backends, ideal-vs-noise]
| Backend | Kind | Qubits | Runs | Jobs per run |
|---|---|---|---|---|
| Built-in simulator (BasicSimulator) | ideal | 24 | browser | unlimited |
| AWS Braket local (StateVectorSimulator) | ideal | 25 | browser | unlimited |
| IBM Boston/Kingston/Pittsburgh/Fez/Marrakesh/Aachen (Heron), Miami/Berlin (Nighthawk) | noise model (Fake backend on Aer) | 156/120 | browser | unlimited |
| IonQ Aria 1, Aria 2 (retired hardware) | IonQ cloud noise model | 25 | IonQ cloud, free | **1** |
| IonQ Forte 1, Forte Enterprise 1 | IonQ cloud noise model | 29 | IonQ cloud, free | **1** |
| IonQ Forte 1 / Forte Enterprise 1 hardware | real QPU | 36 | credits | **1** |

- **IonQ noise-model simulation is shot-aware: it runs one simulation per shot.** Start with about 100 shots. The IBM noise models take about 10 s to set up and about 13 ms per shot natively, and they are several times slower in WebAssembly. [DOC]
- A 1-shot, 1-qubit job on the IonQ Aria-1 simulator took about **14.8 s** end to end, with states INITIALIZING then DONE. [OBS]
- Debiasing (IonQ error mitigation) applies **only on QPUs, not on the cloud simulators**, and it needs at least 500 shots. `job.result(sharpen=True)` does plurality voting. [DOC]
- IonQ compiles to native gates: GPi, GPi2, virtual Z, MS on Aria and **ZZ on Forte**. `TooManyGates` fires on the compiled count, not the written one. [DOC]
- Error names to expect: `TooManyGates`, `TooManyShots`, `UnsupportedGate`, `NotEnoughQubits`, `SimulationTimeout`, `QuotaExhaustedError` and others. See `/learn/docs/error-reference`. [CODE]

### 1.5 The one-job-per-run rule (critical)
- **IonQ backends (simulators AND hardware) accept ONE job per run.** A second `backend.run` stops the run with "only one job is allowed per code run". A competitor observed it as `ConnectionError`. The local simulators accept as many jobs as you like. [DOC, OBS]
- Workaround 1: **pack everything into one circuit.** For example, put independent sub-circuits side by side on disjoint qubits, then demultiplex the bitstring. That is exactly what the official **Quantum Hackathon Soundtrack** does: 4 two-qubit chord circuits plus 3 four-qubit layers in one 20-qubit circuit, 128 shots. Code below. [CODE]
- Workaround 2: **pass a list of circuits to one `backend.run`.** The docs say anything the provider's `run()` accepts works, "including passing a list of circuits where the provider supports multi-circuit jobs." [DOC] Whether qiskit-ionq 1.0.2 accepts a list in this Pyodide build is **[UNVERIFIED]**. Test it on the IonQ simulator before relying on it.
- **Estimator works on IonQ** (`BackendEstimatorV2`, one call per run, all circuit/observable pairs inside it). **Sampler does NOT work on IonQ.** `BackendSamplerV2` silently returns all-zeros because qiskit-ionq 1.0.2 returns no per-shot memory. **So on IonQ you get counts only, with no shot order and no per-shot memory.** [DOC primitives] This matters for any idea that needs per-shot sequences, such as CHSH round-by-round play. Per-round settings must instead live on separate qubit registers inside the same circuit, or be read from counts.
- Variational loops (VQE/QAOA) cannot iterate on IonQ. The docs' own pattern is: tune on a local simulator, then send the finished circuit to IonQ once. [DOC learn/quantum-optimization]
- **Judging:** "Judges run every project on a free local simulator, and results from IonQ's simulators or hardware neither add nor subtract points." However, "A project that runs on an IonQ simulator has to fit one job per run, so press Run there before you submit." [DOC terms, how-it-works FAQ]

```python
# Soundtrack's packing pattern (soundtrack/service.py, condensed)
qc = QuantumCircuit(width)
for kind, what, offset, w in regs:                       # disjoint qubit slices
    qc.compose(sub_circuit(what), qubits=list(range(offset, offset + w)), inplace=True)
qc.measure_all()
# later: value_for_reg = (int(bitstring, 2) >> offset) & ((1 << w) - 1)
```

### 1.6 Output and UI capability
**Python project (console only):**
- stdout and stderr go to the console.
- `plt.show()` renders as an inline SVG. `plt.savefig("x.png")` shows the image and offers it as a download. `circuit.draw("mpl")` needs the "Qiskit Visualizations" library toggle.
- `from js import sendFile; sendFile(name, mime, data)` puts any file in the console. Images get a preview, and text, JSON and LaTeX get a copy button.
- **The only interactivity is a `main()` input form.** A `def main(shots: int = 100, label: str = "x", t: float = 0.05, verbose: bool = False):` whose whole signature sits on one line, starting in column 0, with only int/float/str/bool annotations, becomes a **Run settings form** in the Select QPU dialog. The runtime calls `main()` itself, so don't call it again. If the signature is malformed, no form appears and main() is silently not called. [DOC]
- Built-in panels: on the built-in simulator and IonQ backends, a **Probabilities panel** charts the outcomes. IonQ runs also add a **Circuit panel**. [DOC run-your-code]
- **ipywidgets and Jupyter-style `display()`: no evidence of support.** There is no mention in the docs and no IPython hooks in the bundle. QAVE imports `IPython.display`, but how it renders there is **[UNVERIFIED]**. Treat Python projects as non-interactive.

**JS project (full interactive UI): this is the path for any game, viz or teaching GUI.**
- You get arbitrary HTML, CSS and JS: buttons, sliders, SVG, Canvas, **WebAudio** (Soundtrack plays audio), and drag interactions. Qollab's own showcases use sliders, drag and click games.
- **`three` (three.js 0.186.1), `three/addons/…` and `postprocessing` 6.39.5 import by name. `@tweenjs/tween.js` and `meshline` are bundled.** Anything else loads from a full URL such as `https://cdn.jsdelivr.net/npm/d3/+esm`. QCFlows uses D3. [DOC]
- The Qiskit API is callable from JS:
  - Constructors are called without `new`.
  - Keyword arguments go through `.callKwargs({...})`.
  - Results come back as Python proxies, so unpack them with `.toJs()`.
  - `circuit.draw.callKwargs({output:'mpl'})` passes through `URL.createObjectURL(fig)` into an `<img>` as an SVG.
- **Calling your own Python from JS:** `await mod.fn.callPromising(args)` or `.callPromisingKwargs`. **A plain synchronous call on IonQ backends fails** with "ConnectionError: XHR is not supported". [DOC]
- The page stays alive after the job returns, until Stop or a reload. So the UI can stay fully interactive with local computation (Statevector, NumPy, JS math) after the run's single IonQ job. Button-triggered `backend.run` calls work on local simulators. **On IonQ only the first call succeeds.** [DOC + inference]
- `console.log` prints to the console below the page. Objects need `JSON.stringify`. [DOC]

### 1.7 Reference projects to fork or copy structure from (all public, source readable)
- **QCFlows: Multi-file Example** (u/qollab, `qcflows-multifile`): D3 UI split into JS modules, the correlation engine as a Python package, and examples as JSON data. Fork of github.com/Itaborala/QCFlows.
- **Quantum Hackathon Soundtrack** (u/qollab): a JS + Python package. Files: `soundtrack/service.py` (the functions JS calls, exchanging JSON strings), `audio.js` (WebAudio), and `data/forte_takes.json` (recorded IonQ Forte shots shipped as a file). It has a **source selector: "IonQ Forte take / Ideal simulation / This run"**. That is the official pattern for showing real-hardware data without persistence.
- **Bell state from JS and Python** (u/qollab, `bell-state-from-js-and-python`): a minimal JS-to-Python bridge with `ui/chart.js`.
- **JS Bloch Sphere** (u/qollab): three.js, tween.js and meshline, imported by name.
- **Learn: The app around it** (u/qollab, `learn-app-ui`): a minimal UI with in-flight and failure states (try/catch around `backend.run`).
- To fetch any public project's files: `GET https://api.qollab.xyz/api/project/id/{id}/versions/id/{head_version_id}/dir`, then `.../file?path=<path>`. IDs come from the listing endpoints in §3.

### 1.8 Write-up rendering [CODE, partly UNVERIFIED]
- The write-up is Markdown with a Preview toggle and math. The bundle (CB-2i0Mk.js) uses `breaks: true`, so **a single newline becomes a line break**.
- **YouTube URLs in image syntax `![caption](https://youtu.be/ID)` render as an embedded iframe.** YouTube is the only embeddable video host. Loom, Vimeo and Drive show as plain links. The YouTube regex and `youtube.com/embed` iframe are confirmed in the bundle. The exact syntax trigger comes from the udsy19 notes **[UNVERIFIED in Preview]**.
- The sidebar has the About summary, tags, contributors, repo link and website link.

---

## 2. Learn pages: summaries and code patterns

Every learn listing opens with `# 'backend' is pre-created for you in the Qollab Playground.` and uses `backend.run(qc, shots=N).result().get_counts()`. **None of them import a provider or name a backend.** The "Run on Qollab" widget offers "IonQ Aria-1 (QPU)" and "IonQ Simulator". All articles are by Nicolaas Spijker, Qollab's community manager.

### /learn/quantum-superposition
- Frames superposition as "a weight on each outcome", not "tries every answer at once". Uses Malus's law (three polarizers) as the analogy: P(0) = cos²(θ/2).
- Minimal code: `QuantumCircuit(1,1); qc.h(0); qc.measure(0,0); backend.run(qc, shots=1000)`. A second listing puts H on 2 qubits for 4 outcomes.
- The cost of exact simulation is 16 B per amplitude: 24 qubits ≈ 270 MB, 30 qubits ≈ 17 GB. It warns that a big state space alone gives no speedup.
- Featured projects:
  - **Superposition Sequencer**: `trigger_probability(θ) = cos²(θ/2)`. The phase φ maps to swing timing and is read from a simulated Statevector, not from shots.
  - Sampling must come from the joint distribution, not per-qubit marginals.
  - **Quantum Courier**: 24-qubit depth-1 MaxCut QAOA (H layer, cx-rz-cx per edge, rx mixer), 4,096 shots on a local simulator, with a deliberately weak local-search baseline (cites Carlson 2023).
  - `Statevector.from_instruction` and `partial_trace` give Bloch-vector length, which shortens under entanglement or noise.
  - **QuantumCanvas** drops outcomes below 5% as noise.
- Closing exercise: replace `h` with `rx(theta)` and predict the split.

### /learn/quantum-measurement
- One shot gives `{'0':1}` or `{'1':1}` and says nothing about the odds. 1,000 shots reveal the distribution.
- `plot_histogram([ideal, noisy], legend=[...], filename="x.svg")` compares ideal vs noisy counts.
- **Basis = which question you ask.** H vs H·Z look identical when measured directly. Add H before the measurement and you get all 0s vs all 1s.
- Odds to angle: `ry_angle = 2*asin(sqrt(p))` (Entangled Body).
- Readout-error model: a per-qubit 2×2 confusion matrix, tensored across qubits (Qollab's readout-mitigation showcase, in JS).
- Featured projects:
  - **Musiq** maps the distribution to a waveform (weighted sum vs stochastic sampling).
  - **Quantum Garden** uses 5 qubits, so one shot is one plant.
  - **QAVE** uses `circuit.remove_final_measurements()` with Statevector, and seeded shot replay.
- **"Where the circuit runs" pattern (Entangled Body):** `bk = globals().get("backend")`, then `transpile(..., backend=bk, optimization_level=1)` and run. On failure it falls back to `Statevector(...).sample_counts(shots)`, then to pure Python.

### /learn/quantum-interference
- Amplitudes add before squaring. The minimal circuit is **H, then RZ(θ), then H**: the count of 0s falls from 1000 to 0 as θ goes from 0 to π (`counts.get('0',0)` in a loop over 5 jobs; fine locally, not on IonQ).
- Grover on 3 qubits:
  - Oracle: X-flips, then `h; ccx; h`, then X-flips.
  - Diffuser: H, X, MCZ, X, H.
  - `num_iterations = int(pi/4*sqrt(2**n))` = 2.
  - Too many iterations undo the answer.
- **Quantum Advantage Lab**: a classical random walk (bell curve) vs a discrete quantum walk with a Hadamard coin and cycle shift.
- **Quantum Regime Radar**: a fidelity kernel via `qc_live.compose(qc_ref.inverse())` that measures the all-zeros fraction, with σ = sqrt(K(1−K)/shots). "On IonQ backends the Playground allows one job per run, so this cell spends it on one comparison."
- **Musiq**: H, per-qubit RZ(λ), a CZ band, H, so the phases shape the distribution.
- Interference on noise: compare against the 12.5% random-guess baseline with a hand-picked 80% success threshold.

### /learn/quantum-entanglement
- Bell state: `h(0); cx(0,1); measure`, giving `{'00':~500,'11':~500}`.
- Featured projects:
  - **Quantum Market Game**: a quantum prisoner's dilemma with `ry(angle,q)` and an optional `cx`. It notes that at π/2 the CNOT does nearly nothing.
  - **"2-qubit states, visualized 8 ways"**: the Bloch vectors a, b plus the correlation tensor T from the density matrix (steering ellipsoid).
  - **Entangled Body**: RZZ couplings weighted by anatomical distance.
  - **Quantum Garden**: a linear CNOT chain plus long-range CNOTs.
  - **Quantum Patterns**: the PQCA library, a 2-qubit CX cell with `pqca.tessellation.one_dimensional`.
  - **Quantum Butterfly Field**: random disjoint CX pairs (scrambling).
- GHZ on 5 qubits with a chain of `cx(i,i+1)`.
- Hardware check: if the correlated fraction (`00+11`) exceeds 0.95, print "Strong entanglement confirmed!" **This is correlation counting, not a Bell/CHSH test.** No CHSH or Bell inequality appears anywhere on the page.

### /learn/quantum-optimization
- Annealing analogy, history, then 1-qubit and 1-edge QAOA:
  - 1-qubit: `h; rz(2γ); rx(2β)`.
  - 1-edge, with γ=−π/4 and β=π/8: `h h; cx rz cx; rx`. It returns only 01/10.
- QUBO with `qiskit_optimization.QuadraticProgram`, brute-forced over 8 assignments.
- **Quantum Courier `quantum_courier_maxcut_forte.py`**: 24-node MaxCut, `cut_value` with bit reversal (`bitstring[::-1]`), and a COBYLA objective that calls `backend.run` per evaluation.
- **"The loop runs on the simulator":** 50 evaluations × 4,096 shots is far too much for hardware. The Forte script fixes `GAMMA_STAR` and `BETA_STAR` and submits once.
- Constraints become penalties (**Quantum Systemic Oracle**: 28 couplings, all-to-all on Forte with no routing).
- Depth: Courier's README found the limit to be about 90 two-qubit gates on Forte. p=1 (56 gates) was fidelity-optimal, and deeper circuits flatten toward uniform on the QPU.
- Honesty precedent: Courier keeps a stage where QAOA **lost** to classical simulated annealing.

### /learn/quantum-chemistry
- One energy evaluation is weighted Pauli averages from counts:
  - 1 qubit: `ry(θ)` and measure, with z = (n0−n1)/shots.
  - Two bases: add `h` before the measurement for X.
- **H₂ on 2 qubits:**
  - Hamiltonian dict `{"II":-1.052373,"IZ":0.397937,"ZI":-0.397937,"ZZ":-0.011280,"XX":0.180931}`, NUCLEAR = 0.719969.
  - Ansatz: `x(0); ry(θ,1); cx(1,0)` with θ = −0.2235, 10,000 shots, one Z job and one X job.
- Hamiltonian source: `FermionicOp` with `JordanWignerMapper` (qiskit-nature). `PySCFDriver(atom="H 0 0 0; H 0 0 d")` with `GroundStateEigensolver(JordanWignerMapper(), NumPyMinimumEigensolver())` works in the browser via the "Qiskit Nature (+PySCF)" library toggle.
- Library VQE: `SparsePauliOp`, `n_local(2,"ry","cz",reps=1)`, `VQE(StatevectorEstimator(), ansatz, COBYLA(maxiter=50), callback=...)`.
- Featured projects:
  - **qOrbital**: VQE orbitals with a gallery of IonQ runs shown as a cloud of trajectories.
  - **Quantum Advantage Lab** ansatz: RXX all-to-all, "native on IonQ via MS".
- Chemical-accuracy shot count and the effect of gate noise on the estimate.

### Courses (structure only)
- **Programming your first quantum circuits** (6 lessons, ~1 h, every lesson run on an IonQ noise-model simulator). The lessons are public projects `u/qollab/learn-*`:
  1. first circuit
  2. superposition
  3. Bell pair
  4. RY/RZ
  5. phase visible + 2-qubit Grover
  6. noise: Bell pair at 4,000 shots on 4 IonQ noise models, then publish
- **Using quantum in a real application** (6 lessons):
  1. where the circuit sits
  2. amplitudes vs tally
  3. inputs in, result out
  4. app UI with in-flight and failure states
  5. "Is quantum worth it here": a quantum picker vs `random.choices` in one job
  6. what to build

---

## 3. Projects on Qollab (complete public list as of 2026-10-10)

**API:**
- `GET https://api.qollab.xyz/api/project/recent?limit=100&next=<cursor>` lists all published projects, paginated. There were **125 public projects** in total.
- Other endpoints: `/api/project/featured`, `/api/project/popular`, `/api/project/trending`, `/api/project/most-forked`, `/api/project/labels?limit=100` and `/api/project/search?q=<text>&limit=N` (search is fuzzy). Each item has id, name, title, description, owner_username, labels, repo_link, head_version_id and code_sample.
- Only **published** projects are visible. Drafts from hackathon teams are private, so the hackathon field is larger than this list.

### 3a. Hackathon-window entries already published (Oct 9–10, 2026). Direct competitors.
| Project (u/owner) | One-liner | Overlap flag |
|---|---|---|
| **Bell's Bluff: Poker, but the Cards Are Entangled** (u/chiapin833, JS) | Poker where entanglement, hidden gates, measurement basis and collapse are betting mechanics. The "Quantum Cards" come from a Bell circuit. | **Entanglement/basis game.** Near a nonlocal-game idea but NOT a CHSH/Bell-violation test (no CHSH in the source). |
| **Qriollo – Truco Cuántico** (u/gaspiosterrieth, Python+JS) | Argentine Truco teaching single-qubit circuits. Partial: full matches run locally because of the one-job rule. | **Argentine team**, possibly the same node. Game + teaching. Their COMPATIBILITY.md is the best field report on the platform. |
| **PhaseCheck** (u/EazyHood, JS+Py) | "A passing test can miss a broken quantum state." Audit 3 error-correction claims on a coherent 3-qubit repetition code (two 5-qubit blocks, one job), choose the missing observable, export the evidence. | **QEC teaching / verification.** Overlaps a QEC decoder game and "fake quantum detection"-style auditing. |
| **Free-Space Optical Drone QKD & Entanglement Purification** (u/luonga) | Drone-link QKD with 1-stage DEJMPS purification on IonQ. | **Quantum networking.** |
| **ionAir: Mission Control** (u/luonga) | Airline disruption recovery with XY-mixer QAOA. | Impact/optimization. |
| **Entanglert** (u/alexmsb, Spanish) | Malicious participants in a quantum network via entanglement. Currently only the Bell starter code. | Networking. |
| **Quantum Communication / Quantum Communication-McGill** (u/wen, u/Danylo) | Two devices communicating over a quantum network. | Networking (teleportation-like). |
| **Quantum Automitigation** (u/S0cra13s) | Bandit learner choosing ZNE, twirling and transpiler level on the IonQ simulator, scored by mirror circuits. | Mitigation / benchmarking. |
| **QAIP Hardware Ranking** (u/Rudra1x) | Calibration-aware backend ranking using IQM and IonQ data. | Benchmarking / "which hardware to trust". |
| **QMoney** (u/Jabariroy) | 8-qubit QAOA financial allocation with exact classical benchmarks. | Impact/finance. |
| **SentinelQ (Attack Detection)** (u/Jabariroy) | Quantum vs classical attack detection. | QML/security. |
| **Shape Approximator** (u/HOWSE, JS) | Interactive classical vs quantum approximation viz. | Unclear. |
| **hello-fringe** (u/dianaelizabeth, JS) | "Structure of the circuits for our project." | "Fringe" may mean interference fringes. Unclear. |
| **10_9_Hackathon** (u/gbaldwin, JS), **registration vectors** (u/ndazeo, point-cloud registration), **MejorRuta / distancia** (u/plamsoft, 5-city routing), **Qchemistry ×2** (protein), **Pure-State Entanglement Measurement** (u/Niharika28: von Neumann entropy and concurrence) | Various early entries. | Entanglement measures (Niharika28). |

### 3b. Qollab's own showcases (u/qollab). Judges have seen these; don't duplicate them.
- **Error correction showcase: the repetition-code game.** You click qubits to flip them and the decoder fights back. It has syndrome lights, majority vote, and a 2,000-trial "storm mode" that finds the threshold. **This is a QEC decoder game that already exists, made by the platform owners.**
- **Simulation showcase: statevectors vs stabilizers.** Race them, then add a T gate and the shortcut refuses.
- **Readout mitigation showcase**: GHZ-5 with sliders.
- **Error mitigation showcase**: an interactive ZNE explorer on GHZ-4 parity, plus a Python version.
- **Transpilation showcase**: hover a GHZ gate to see its MS native expansion.
- **Calibration showcase: where T1 comes from.**
- **Quantum kernel showcase**: drag a point on two-moons.
- **Quantum chemistry showcase**: an H₂ bond slider (JS), plus a Python dissociation curve.
- **Cross-framework showcase**: one VQE in Qiskit vs PennyLane.
- **Interactive Bloch Sphere**, **JS Bloch Sphere**.
- Library showcases for histograms, PQCA, QUBO exact, QAOA QUBO, H₂ ground state, Jordan-Wigner, VQC XOR, EstimatorQNN, portfolio, option pricing, Bell on IBM fake, and Bell on Braket.
- Example projects: **Shor's N=15** (7 qubits), Bell State, **Scaled Entanglement (GHZ, "benchmark for multi-qubit coherence")**, **Quantum Teleportation**, QPE, Quantum Chemistry (methanol VQE), and Grover's Search.
- Learn lesson projects (12), **Quantum Hackathon Soundtrack**, and **QCFlows: Multi-file Example**.

### 3c. Cohort and community projects (pre-hackathon)
- Spring-2026 cohort (detailed in D_saturation_map): Quantum Butterfly Field, Musiq, qOrbital, QuantumCanvas, Entangled Body, QCFlows, Quantum Systemic Oracle, Qatalyst Pizza Race, Quantum Market Game, Superposition Sequencer, Quantum Patterns, Quantum Market Regime Radar and Quantum Advantage Lab.
- Fall 2025: QAVE and Quantum Garden.
- Others:
  - **Quima** (3D QM playground with gamified challenges)
  - **Collapsing AI** (LLM attention weights on IonQ to test "superintelligence"; pseudo-quantum flavor)
  - **Depth-Independent Coherence** (routing vs noise-aware compilation arms)
  - **Krylov Quantum Diagonalization** (30-qubit Heisenberg)
  - **2-qubit states visualized 8 ways**
  - **Qupepfold** (CVaR-VQE peptide folding)
  - u/sairamtummuri's **QEM Playground**, **QEC Visualizer**, **Noise Simulator Dashboard** and **Quantum Mood Music**
  - Data Analysis with Python, and assorted tests and forks

### 3d. Overlap check for our candidate territories
| Territory | Found on Qollab? |
|---|---|
| Nonlocal games / CHSH / Bell-inequality violation / Mermin–Peres magic square / GHZ game | **None found.** No project mentions CHSH, Tsirelson, magic square or a GHZ game in its title, description or code sample. Search hits were fuzzy false positives. The nearest are **Bell's Bluff** (an entangled-card poker game where basis choice is a mechanic) and the Bell-pair "correlation > 95%" checks in learn pages. **The territory is open, but Bell's Bluff will make "Bell + game" look less fresh.** Differentiate on the actual inequality, win-probability 0.85 vs 0.75, or a verifiable advantage. |
| "Fake quantum" detection / verifying a black box is quantum | **None directly.** The nearest are **PhaseCheck** (auditing QEC claims: "a passing test can miss a broken state") and Qollab's statevector-vs-stabilizer showcase (the classical-simulability boundary). |
| Information supremacy / communication-complexity advantage | **None found.** |
| Quantum sensing / metrology / GHZ phase sensitivity | **None as sensing.** GHZ appears only as an entanglement benchmark (Scaled Entanglement) and in mitigation showcases (GHZ-4/5 parity). |
| Avian compass / radical-pair mechanism | **None found.** The "radical" search returned only qOrbital, a chemistry project. |
| QEC decoder game | **Exists:** Qollab's own *Error correction showcase: the repetition-code game*, plus hackathon entry **PhaseCheck**, plus u/sairamtummuri's QEC Visualizer. **Saturated at the repetition-code level.** Only surface-code or real-decoder (MWPM) territory remains, and D_saturation_map notes a MWPF decoder demo already exists. |
| Quantum networking / QKD / teleportation | **Crowded in this hackathon:** FSO Drone QKD, Entanglert, two Quantum Communication entries, plus Qollab's teleportation example. |

---

## 4. Hackathon terms (qollab.xyz/programs/hackathon/terms and how-it-works)

- **Every project must:**
  - Use **Qiskit**.
  - **"Follow industry best practices on UI accessibility"**. No detail is given. Plan for keyboard operation, contrast, text alternatives and reduced motion (Almond's repo already advertises this).
  - Run on Qollab's free simulators, including the IonQ simulator.
  - Be published and runnable on Qollab under **MIT** before the deadline. Outside repos must also be MIT.
  - Have a project page covering what it does, the problem, how to run it, and how to replicate or extend it.
  - Be built during the window, with prior code, forks and templates disclosed.
  - Include a **2–3 min demo video at a public link with no sign-in**.
- **Required verbatim attribution on the project:** **"This effort is supported by Qollab & IonQ"**.
- Participants also agree to keep the project on Qollab for 12 months. Winners must post at least once on social media.
- **Novelty floor ("Beyond the tutorial bar"):** the project must show at least one of:
  - (a) a novel application or problem context
  - (b) a technical extension (noise or error mitigation, parameter optimization, comparative benchmarking)
  - (c) an original analytical or educational contribution (a genuinely new way to visualize or explain)

  **Panels may score 0 on Novelty & Technical Execution if the floor is not met.**
- **Rubric:** Novelty & Creativity, Technical Execution, Impact Potential, Documentation Quality. The page gives **no weights**. Local panels (a faculty judge plus Qollab and IonQ representatives) score first. The top 3 advance, and each node may also advance one project per specialty award. The global panel re-scores with the same rubric.
- **How judges run it:** "Judges open the project page, read the description and the code, and press Run on a free simulator." IonQ vs hardware results are not scored. A failure on IonQ matters only if the run fails.
- **Teams and submissions:**
  - Up to 4 members.
  - Up to 5 submissions, judged independently. Awards are per project.
  - The **captain submits** from the registration page and can edit until Oct 11 19:00 ET. After that, withdrawal only.
  - Each project must be public and owned by the captain or a teammate who joined.
- **Originality:** AI, libraries and templates are allowed when disclosed ("say on your project page what existed before the build window and credit its source"). Undisclosed reuse means disqualification. Two teams with substantially identical projects are disqualified.
- **Prizes:**
  - Local (10+ submissions): $500/$300/$200 cash plus $5k/$3k/$2k compute.
  - Global: $10k/$5k/$2.5k plus $20k/$15k/$10k compute.
  - Specialty: $500 plus $5k each. Categories are Most Novel/Creative, Best of each of the 3 themes, Most Impact and Best Documentation.
  - A project can win both a placement and a specialty award.
- **Partial projects are still eligible** ("Submit what you have").

---

## 5. Practical implications for our build (opinion)
1. **Build a JS / Qiskit project** if the idea has any interaction. Python projects only get a parameter form and console output.
2. **Architecture:**
   - `quantum/*.py` builds a single packed circuit and decodes it.
   - `main.js` draws the UI and makes exactly **one** `backend.run`.
   - Interaction after that runs on local Statevector, NumPy or JS math, or replays the counts.
   - Ship a recorded IonQ simulator result in `data/*.json` and use a "recorded / ideal / this run" selector (the Soundtrack pattern).
3. **Design so the judges' local-simulator run is the full experience.** The IonQ simulator run must not crash (one job, ≤25 qubits for Aria and ≤29 for Forte, ~100–500 shots, since it is slow per shot).
4. **Counts only on IonQ, no per-shot memory.** Any protocol that needs round-by-round correlations, such as CHSH rounds with random settings, should encode the settings on extra qubits inside the one circuit. Alternatively, use counts per setting, with the four CHSH settings on disjoint qubit pairs in one circuit.
5. **The write-up checklist:**
   - the verbatim attribution line
   - a "prior work / built during the window" disclosure
   - a "what's new" paragraph mapped to the novelty floor
   - an accessibility section
   - a YouTube demo embed
   - how to run (which backend, how many shots)
   - MIT LICENSE
6. Test in Chrome. Safari can't run Qollab, so don't demo from a Mac's Safari or an iPad.
