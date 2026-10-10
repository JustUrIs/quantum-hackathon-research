# Q-DAY CLOCK: the evidence room

**Two circuits show the same peaks. Only one tried to find the period.**

Inspect a genuine miniature order-finding circuit beside an imitation that receives the answer in advance. Give random outputs the same post-processing. Then explore how a hypothetical quantum-attack horizon interacts with the lifetime of your data and the time needed to migrate.

**This effort is supported by Qollab & IonQ.**

## Try it in one minute

1. Run on Qollab's free built-in simulator. Scroll to **The evidence room**.
2. Choose N = 15, a = 2. The genuine and pre-solved circuits have matching ideal histograms but different work and inputs.
3. Replace all outputs with random bits. The factor-recovery rate falls from **50% to 21.875%**, not to zero. That surviving success matters.
4. Choose N = 33, a = 2. Even the ideal circuit finds no useful factor. Change a to 5 to see why a legitimate algorithm sometimes needs another attempt.
5. Return to N = 15, a = 2 and run **one backend check**. Export counts and explicit factor witnesses.
6. Set a confidentiality lifetime longer than your assumed attack horizon. The clock shows the planning gap. It does not predict when such a machine will exist.

## What runs

The genuine builder receives public N, base a and phase-register width. It prepares a work register in |1⟩, applies controlled multiplication by `a^(2^j) mod N`, then an inverse QFT. No factor or period enters that builder. It extends multiplication as identity on unused basis states y ≥ N, preserving reversibility.

The implementation synthesizes finite permutations with Gray-path transpositions. For public moduli of the form 2^w−1 and power-of-two multipliers, cyclic bit rotation gives an algebraic optimization. That optimization does not compute the period. General truth-table synthesis is **exponential**, so this is a small-N teaching implementation, not scalable RSA arithmetic. Gate counts use RX/RY/RZ/CX and are not predictions of IonQ's native compiler or fault-tolerant cost.

The imitation computes the period **classically** and prepares a state with the resulting distribution. The period is displayed as a leaked input. Matching output statistics therefore cannot establish that a circuit performed the intended computation.

Recovery uses continued-fraction convergents of y/2^t. Each even period candidate must pass `a^r mod N == 1`, followed by a nontrivial GCD check. We count failed outputs. We do not sweep all possible periods or inject known factors into the recovery function.

For N = 33, a = 2, the order is 10 and `2^5 mod 33 = −1`; that base yields trivial GCDs even with an ideal period. The failure is intentional evidence, not hidden behind a favorable input choice.

## Baselines and interpretation

| Comparison | Exact meaning |
|---|---|
| Genuine circuit | Ideal Qiskit statevector distribution followed by the described recovery |
| Uniform phase bits | Uniform 6-bit output through the identical recovery function |
| Random integer + GCD | Uniform integer from 2 to N−1; success if GCD is nontrivial |
| Trial division | Deterministic divisor checks through the first divisor; the practical winner for these instances |

For N = 15, a = 2, uniform phase recovery succeeds on 14/64 outputs and random-GCD on 6/13 integers. Trial division needs two checks. These are different attempts with different costs, not a quantum speedup claim. The noise control mixes ideal output probabilities with a uniform distribution. It is an output ablation, not an IonQ noise model or simulated gate-level decoherence.

## The clock's assumptions

```
planning headroom = assumed attack horizon
                 − required confidentiality lifetime
                 − migration duration
```

All three numbers are user assumptions. The export includes them. A negative number flags a gap under those assumptions, not a measured probability of compromise. The interface does not invent hardware arrival dates, equate physical with logical qubits or extrapolate tiny circuit counts to RSA-2048.

The two source cards summarize published RSA-2048 resource estimates: Gidney–Ekerå's roughly 20 million physical qubits / 8 hours and Gidney's 2025 estimate below one million / below one week. Both assume a 0.1% physical gate error rate, 1 μs surface-code cycle, 10 μs reaction time and specified connectivity. Their space/time tradeoffs differ. They are not directly interchangeable hardware specifications.

## Run and verify

Upload this folder's contents as a Qollab JS project. The backend check sends one measured genuine circuit, 100 shots on IonQ-named backends or 1,024 locally. The default uses **10 qubits**. Larger inputs can exceed practical remote gate/time limits despite fitting the qubit count. Use the local lab for those explorations; begin remote testing with N = 15, a = 2. Backend failure is shown and never disguised as a successful remote result.

**Validation status:** tests verify the complete controlled-multiplication basis mapping, independent Fourier-coset distributions, no-period-oracle construction, recovery witnesses and real local BasicSimulator counts. Browser controls, export, one-job behavior and responsive layouts have local coverage. Qollab/Pyodide and remote IonQ execution still need verification; this repository does not claim either occurred.

From the full repository:

```
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python tools/serve.py
python -m unittest discover -s tests -v
python tools/ui_test.py
```

Open `http://127.0.0.1:8766/qday-clock/`. Qollab loads `qday/service.py` through `.callPromising`; the local server is only a development bridge. The upload includes no API key and creates no custom provider.

## Contribution and prior art

Suggested theme: **Quantum Unlocked**. Our educational contribution combines a real miniature algorithm, a confessed pre-solved imitation, matched post-processing ablations, visible algorithmic failures and a scenario clock with exportable assumptions. It is not a new factoring algorithm.

The name and concept “Q-Day Clock” already appear at [q-dayclock.com](https://q-dayclock.com/) and [qdayclock.net](https://qdayclock.net/). We are not affiliated and do not claim to have invented a quantum countdown. **The evidence room** is this project's distinguishing experience; a commercial release needs a separate naming review.

The bridge pattern derives from IMPOSTOR in this repository. This engine and interface were built during the hackathon with AI assistance; Qiskit, Shor's algorithm and the cited analyses predate it. MIT license. No real key attack, security certification, customer validation or new resource record is claimed.

Controls support keyboard input and widths down to 390 px. Probability bars have numerical labels. A public 2–3 minute video and final Qollab submission remain release steps; scripts are in the repository's `launch/` folder.

## Sources

- [Gidney–Ekerå, RSA resource estimate](https://arxiv.org/abs/1905.09749).
- [Gidney, revised resource estimate (2025)](https://arxiv.org/abs/2505.15917).
- [NIST: post-quantum cryptography and harvest-now/decrypt-later](https://www.nist.gov/cybersecurity-and-privacy/what-post-quantum-cryptography).
- [Qollab JS projects](https://qollab.xyz/learn/docs/js-qiskit-projects), [compiler caveats](https://qollab.xyz/learn/docs/how-your-circuit-is-compiled).
