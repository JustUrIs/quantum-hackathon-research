# LOST SIGNAL

**When the satellites go quiet, what can you still measure?**

Choose a sensor for a simulated Buenos Aires–Ushuaia mission. Compare independent probes with an entangled GHZ state at the same resource budget, add noise, and find where entanglement stops helping. Then remove the anisotropy from a three-spin radical-pair model and watch its directional response disappear.

**This effort is supported by Qollab & IonQ.**

## Try it in one minute

1. Run this JS project on Qollab's free built-in simulator, in a supported desktop browser.
2. Press **Cut the GPS signal**. The map displays two illustrative uncertainty corridors.
3. Leave four probes, 256 readings and η = 0.08: the local precision gain is about **1.57×**.
4. Press **Find the point where it stops helping**. Independent probes win at higher dephasing.
5. In the molecular experiment, remove the directional coupling. The angular response becomes flat.
6. Press **Run the backend check** once to sample a real Qiskit circuit on the selected backend. Export the snapshot, counts and confidence intervals.

The mission button guides the same sequence. No API keys or external data downloads are needed during a run.

## What the experiment measures

For N probes, M repeated preparations and single-probe coherence v = exp(−η), independent phase-flip noise gives these *local* Cramér–Rao bounds at the respective optimal quadratures:

```
independent σφ = 1 / sqrt(M N v²)
GHZ         σφ = 1 / sqrt(M N² v^(2N))
gain          = sqrt(N) exp[−(N−1)η]
crossover η   = log(N) / [2(N−1)], for N > 1
```

Both protocols spend N×M probe interactions at a fixed interrogation time. The independent baseline is a separable quantum Ramsey sensor, often called the standard quantum limit baseline; it is not a measured commercial magnetometer. The experiment does not optimize interrogation time, include entangling-gate cost in the analytic model, or solve the global phase ambiguity. Huelga et al. show why the frequency-estimation conclusion changes when time is optimized under Markovian dephasing. At N = 1 the preparations coincide.

The fringes are `P(0)=(1+v cos φ)/2` and `P(even)=(1+v^N cos Nφ)/2`. Uniform random outputs have zero phase Fisher information. Tests independently apply Kraus phase-flip channels to Qiskit density matrices and reproduce the analytical result.

## Geography and the molecule

`data/route.json` contains 41 spherical great-circle route samples evaluated with **WMM2025**, through `pygeomag==1.1.0`, at 10 km altitude and decimal year 2026.775. These are model outputs, not flight measurements. The map coastline is schematic; exported samples retain their coordinates. WMM represents the large-scale field, not a magnetic-anomaly map sufficient to localize an aircraft. US-government WMM material is public domain; attribution and DOI are in the file.

The corridor converts a fixed phase uncertainty into heading uncertainty with an explicit illustrative gain of 1 rad/rad. It is not a navigation filter, GPS replacement, calibration, safety margin or field performance claim. The display caps very large angular errors at 0.45 rad and labels the cap.

The molecular panel uses a separate **three-spin toy model**: two electrons initially in a singlet, one maximally mixed spin-½ nucleus, static field and anisotropic hyperfine interaction. In angular units rad/μs:

```
H = ω/2 [sin θ (X₀+X₁) + cos θ (Z₀+Z₁)]
  + 2π/4 [0.2 X₀X₂ + 0.2 Y₀Y₂ + (0.2+a) Z₀Z₂]
ω = 2π × 0.028024951 × field_μT
ΦS = ∫₀∞ k exp(−kt) Tr[PS U(t)ρ U†(t)] dt, k = 1/μs
```

The code evaluates the integral exactly in the Hamiltonian eigenbasis. Its UI uses 26 μT and switches a between 1 and 0. An isotropic coupling makes the yield direction-independent. This is not a biological fit, a north/south polarity detector, an NV-diamond sensor or an RF disruption simulation. Those are distinct physical systems.

## One backend job

`lostsignal/service.py` packs an N-qubit GHZ Ramsey experiment and N independent probes into **2N qubits, at most 12**. Both see φ = 0.23 rad. The counts decode GHZ parity and one independent-probe marginal, with Wilson 95% intervals. This checks a transfer response, not a measured sensitivity bound. The local noise slider is not injected into the selected provider.

The button sends 100 shots to IonQ-named backends and 1,024 to the local simulator. It can submit only once per Qollab run. Later control changes do not change the recorded snapshot. Failures surface explicitly without relabeling a fallback simulation as a provider result.

**Validation status:** mathematical and local-browser tests run in this repository; local BasicSimulator counts are saved under `artifacts/`. A live Qollab/Pyodide and remote IonQ run still requires verification. No hardware or remote-IonQ results are claimed.

## Reproduce and extend

Upload this folder's contents, with `index.html` and `main.js` at the project root. `main.css`, `runtime.js`, `requirements.txt`, `lostsignal/` and `data/` must accompany them. Python returns JSON through Qollab's `.callPromising` bridge. No custom backend is created in production.

From the full GitHub repository:

```
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python tools/serve.py
python -m unittest discover -s tests -v
python tools/ui_test.py
```

Open `http://127.0.0.1:8766/lost-signal/`. Reproduce the field fixture with `python tools/generate_route.py`. The HTTP Python bridge is local development infrastructure and is not part of the Qollab upload.

## Contribution, scope and next experiment

Suggested theme: **Quantum Unlocked**. The navigation setting creates an Impact direction, but this submission does not yet demonstrate an industrial navigation improvement. Its contribution is an interactive comparison with matched resources, a visible noise crossover, traceable geomagnetic context, an anisotropy ablation and exportable circuit evidence. GHZ metrology and radical-pair compasses are established science.

Next useful validation: obtain recorded sensor noise from a navigation research group; compare against an optimized separable baseline, include preparation overhead and fit a measurement model before connecting anything to a navigation filter. There is no proprietary sensor, field trial or customer traction in this submission.

We extended the existing IMPOSTOR repository's JS/Python bridge pattern during the hackathon; this project has its own engine, interface and data. Qiskit, NumPy, the cited models and WMM predate the event. AI assisted implementation and drafting. MIT applies to our code; external data provenance remains explicit.

Keyboard controls, descriptive labels, numerical alternatives to color, mobile layouts and reduced-motion support are included. Local browser tests cover widths 390, 768 and 1,440 px. A 2–3 minute public video and final Qollab submission are release requirements, not completed artifacts.

## Sources

- [Huelga et al., decoherence and frequency standards (1997)](https://arxiv.org/abs/quant-ph/9707014).
- [NOAA/BGS World Magnetic Model](https://www.ncei.noaa.gov/products/world-magnetic-model), [WMM2025 dataset DOI](https://doi.org/10.25921/aqfd-sd83).
- [Radical-pair mechanism and the avian chemical compass, review](https://arxiv.org/abs/1502.00671). Our parameters are illustrative, not a reproduction of a biological dataset.
- [Qollab JS projects](https://qollab.xyz/learn/docs/js-qiskit-projects), [runtime rules](https://qollab.xyz/learn/docs/runtime-environment).
