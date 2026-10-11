# DARKROOM: Quantum Interrogation Lab

**Can a probe reveal an object without being absorbed by it?** DARKROOM lets a learner change the number of weak interferometer rotations and ordinary per-pass optical loss, then inspect every outcome for an object-present and object-absent hypothesis.

## What it does

Start with **Learn step by step**. The six-step English/Spanish lesson distinguishes path amplitudes from split photon energy, explains mixers and final detectors, and walks through the empty and object-present two-cycle cases. A final four-question check covers whole-photon detection, the impossible empty-apparatus D0 outcome, the purpose of the measurement, and inconclusive optical loss. The guided lesson uses analytic probabilities at two cycles and zero ordinary loss; the independent experiment controls below can explore more cycles.

A direct probe can reveal a perfectly absorbing object, but the probe is absorbed. In interaction-free measurement, a sequence of weak path rotations can sometimes reveal that the object is present because it changes the interference pattern, even though the successful probe did not enter the blocked arm. This is probabilistic. Increasing the number of ideal cycles reduces absorption, while real loss creates more opportunities for an inconclusive result.

DARKROOM puts those tradeoffs side by side. It reports correct absent-port detections, safe present detections, absorbed probes, and lost/inconclusive probes separately. It never turns them into one success score.

This is an educational simulation of established physics. It is not a photon experiment, camera, human-presence detector, medical tool, or claim of quantum advantage. The low-dose sensing connection is a discussion prompt, not a demonstrated product.

## What runs on Qollab

The Python module constructs and simulates a Qiskit circuit with 4–8 qubits. Qubit 0 labels the object hypothesis, qubit 1 is the probe path, and one fresh environment qubit per cycle records absorption. An absorbed branch is frozen so later rotations cannot change it. The ideal statevector outcome probabilities are compared against a separately written analytic formula.

The loss slider is an independent analytic channel model. It is intentionally not represented as hardware noise or included in the Qiskit circuit.

**Measure locally with Qiskit** runs the measured circuit using Qiskit's Python `BasicSimulator` in the current runtime, without a remote provider request. It uses 1,024 shots and seed 91 for reproducibility. Reports identify the simulator, settings, seed, and simulation source. This is circuit simulation, not hardware evidence.

**Try the selected Qollab backend** separately attempts one job on the backend selected in the portal. If its network connection fails, the app shows a concise explanation and preserves technical details. A failed attempt is never reported as an IonQ result; the local measurement remains available. The app does not retry a potentially submitted remote job automatically. Both circuit runs model the ideal absorber and exclude the slider's optical loss.

The object-label qubit compares two known test conditions; the app does not infer a real object's presence from a sensor feed. One path qubit represents one photon's two path alternatives. The extra qubits record possible absorption branches. Six qubits therefore do not mean six photons.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Create a Qollab project from these files, keeping `darkroom/`, `lesson.js`, and `lesson.css`. Press **Run**, use **Learn step by step**, and then press **Measure locally with Qiskit**. The default two-cycle setup matches the lesson. The local path needs no API keys or provider connection. Browser execution speed depends on the runtime.

## Model

For `N` cycles, each path rotation is `theta = pi/(2N)`. With an ideal object-present absorber, per-pass absorption probability for the active branch is `sin²(theta)`; the safe branch survives each cycle with probability `cos²(theta)`. For absent object and per-pass loss `lambda`, correct output probability is `(1-lambda)^N`. Present-object loss is accumulated only from the unabsorbed active branch. All mutually exclusive outcomes sum to one.

The direct comparison uses one probe: if the object is present, it is absorbed unless ordinary loss removes it first. If absent, the detector reports the absent port unless the probe is lost.

## References

- P. G. Kwiat et al., “Interaction-Free Measurement,” *Physical Review Letters* 74, 4763 (1995), https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.74.4763
- P. G. Kwiat et al., “High-efficiency quantum interrogation measurements via the quantum Zeno effect,” *Physical Review Letters* 83, 4725 (1999), https://doi.org/10.1103/PhysRevLett.83.4725

## Hackathon category and next validation

Recommended category: **Quantum Unlocked**. The central contribution is making a subtle quantum measurement idea inspectable and runnable. Before claiming classroom value, test the explanation with quantum-computing learners and measure whether they can predict the outcome tradeoff before and after using it. A future classroom product could add guided exercises and instructor-built experiments; it should earn that scope through user testing.

MIT licensed. See `LICENSE`.
