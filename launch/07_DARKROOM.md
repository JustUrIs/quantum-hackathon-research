# DARKROOM — pitch and project card

## One sentence

DARKROOM is an interactive Qiskit lab that lets students test a counterintuitive quantum question: can a probe reveal a perfectly absorbing object without being absorbed?

## Project card (English)

Can a probe reveal that an object is present without touching it? DARKROOM makes interaction-free measurement inspectable. Learners vary the number of weak path rotations and optical loss, then compare a direct probe with a quantum interrogation protocol. The experiment reports every outcome separately: correct absent detections, safe present detections, absorbed probes, and inconclusive losses. Its Qiskit circuit uses a path qubit and a fresh environment flag on each pass to model absorption; an independent analytic calculation checks the ideal statevector probabilities. The loss slider is explicitly a separate analytic channel, not a Qiskit noise result. DARKROOM is an educational simulation of established physics—not a photon experiment, imaging device, or claim of quantum advantage. It belongs in Quantum Unlocked because its purpose is to make a subtle quantum measurement idea runnable and understandable.

## 90-second spoken pitch

“Here is a strange question: can you learn that an object is there without your probe being absorbed by it? A normal test sends a probe into the sample. If the sample blocks the path, that probe is destroyed. Quantum interference gives us another route: make several tiny rotations between two paths. If one path is blocked, the interference changes. Sometimes the surviving probe reveals that the object was there without entering it.

“DARKROOM lets you change the number of rotations and ordinary loss, then see every result. We show safe detections, absorbed probes and inconclusive losses separately. There is no success score hiding the cost. More gentle cycles can protect the sample in the ideal model, but real loss accumulates across passes.

“The Qollab project builds the experiment as a Qiskit circuit. A fresh environment qubit records absorption on each pass, and absorbed branches stop evolving. We verify its statevector against an independent probability calculation. The web companion is only an analytic explainer; the circuit runs in Qollab.

“This is known physics, not a new detector. Our contribution is a transparent learning lab for a concept that is usually hard to picture. The next test is to measure whether students can predict the tradeoff better after using it.”

## Category and claims

Submit under **Quantum Unlocked**. The core result is an accessible, runnable explanation. Do not submit it as Quantum Impact: no real sample, medical use, or practical sensing performance has been demonstrated. The product hypothesis is an interactive lab for quantum/optics courses; validate that with instructors and learner outcome tests before claiming adoption or a business.

## Demo path

1. Open **Learn step by step** and demonstrate the empty versus object-present two-cycle traces. Point out the final D0 cancellation in the empty setup and the whole-photon outcomes.
2. Move to 6 cycles: in the ideal model, safe detections rise and absorption falls.
3. Set loss to 5% per pass: lost/inconclusive outcomes grow. Emphasize that this loss model is analytic and not in the circuit.
4. Use **Measure locally with Qiskit** on Qollab. Show its BasicSimulator source, counts and formula/statevector agreement; distinguish finite-shot variation from exact probabilities. A selected-provider run is optional and separately labeled.
5. Close with the caveat: simulated absorber, established physics, no claim of practical imaging.
