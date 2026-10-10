# Front A: Frontier papers and algorithms (2025–2026)

Scout notes, written 2026-10-10. Everything below was checked with web search. Anything marked **[unverified]** I could not confirm.

**Read this first.** Many 2025–26 headline results are claims that "this is hard for classical computers" (certified randomness, peaked circuits, Quantum Echoes, information supremacy). Running them on a *classical simulator* (Qollab / IonQ sim) shows how the protocol works, but it cannot show any advantage. IonQ judges will notice right away if we blur that line. The honest framing is: "we rebuilt the protocol, here is exactly what a real QPU would add, and here is the classical attack." That framing is itself a selling point.

Second constraint to check with organizers: **does the IonQ simulator path support mid-circuit measurement and reset?** [unverified]. Cards marked (MCM) depend on it. A fallback is deferred measurement or postselection.

---

### S-A-1: Quantum information supremacy in 12 qubits (Kretschmer, Aaronson et al., 2025)
- What: A 12-qubit trapped-ion run (Quantinuum H1-1) that *provably* needs 62–382 classical bits to match. There is no complexity conjecture behind it, which is why it's called "unconditional". The structure has two steps. Alice prepares a near-Haar-random state. Bob applies a random Clifford measurement chosen from one fixed template with classical control bits. The score is linear XEB, F = 0.427 ± 0.013 over 10k trials.
- Source: arXiv:2509.07255 (Sep 2025); Aaronson blog https://scottaaronson.blog/?p=9138 ; APS March 2026 talk. Code: https://github.com/sabeegrewal/quantum-info-supremacy (MIT, built on Quantinuum tooling, not Qiskit) + `-data` repo.
- Rarity: 4. It got press, but very few people understand the communication-complexity idea behind it.
- Evidence of need: the authors list open problems. (1) Bob's choice should come *after* Alice's preparation, which needs online randomness. (2) "Is the device really 12 qubits?" calls for larger n: n=26 means about 1.1M classical bits. (3) The lower bounds could be tightened. (4) State-prep fidelity is only 0.46.
- Quantum hook: essential. The whole object is the gap between n qubits and the 2^Θ(n) classical bits needed to fake them. On a simulator we can *show* that gap, because the simulator needs 2^12 amplitudes. We cannot claim it.
- Buildability: **high**. 12 qubits, one circuit (state prep + Clifford measurement), and it fits the IonQ one-job rule. The brickwork ansatz uses periodic boundaries, so the wrap-around gate is native to all-to-all hardware. Main work: port to Qiskit and train the variational state (they did this offline, and we can ship the parameters as files).
- Theme fit: Unlocked (main), Playground. A "Memory Duel" where a human or a classical bot gets k bits to beat 12 qubits.
- Prior art: the paper's own code (pytket/Quantinuum). No Qiskit port or interactive explainer found [unverified beyond GitHub search].
- Collision hint: ICPC "interactive problems" and communication-complexity puzzles; a game where the scoreboard is XEB; compression ("can you zip a quantum state?").

### S-A-2: CliNR, Clifford Noise Reduction (IonQ's own technique, 2024–2026)
- What: Split a Clifford circuit into sub-circuits run by gate teleportation. Before using each Bell+Clifford resource state, check it with a few random stabilizer measurements and throw away the bad ones. It costs 3n+1 qubits and 2s+o(s) gates. IonQ ran it on Forte Enterprise (without MCM) and reached break-even. A 2026 preprint adds MCM for Hamiltonian simulation; an IonQ blog reports 54% lower error on Trotter circuits.
- Source: arXiv:2407.06583 (Delfosse & Tham, IonQ); arXiv:2504.13356 (Quantum, Aug 2025); arXiv:2605.06792 (May 2026, MCM); "Mid-Circuit CliNR" was one of IonQ's 9 QCE26 papers (Sep 2026). https://www.ionq.com/blog/a-platform-solution-to-the-deep-trotter-dilemma-improving-quantum-chemistry-simulations
- Rarity: 5. Outside IonQ and a few QEC people, almost nobody knows it.
- Evidence of need: it is IonQ's own near-term error-reduction line, with active papers in 2025 and 2026. The judges are IonQ engineers.
- Quantum hook: essential. Stabilizer verification, teleportation and postselection are core QEC-lite ideas.
- Buildability: **high**. n=4–6 logical qubits gives 13–19 qubits. The no-MCM version is one circuit plus postselection in post-processing, which fits the IonQ one-job rule. The Qiskit noise model is the main effort. The "choose verification stabilizers" optimization step (tabu search) is a natural ICPC-style hook.
- Theme fit: Unlocked ("error correction before error correction"). Impact is possible if framed as tooling, e.g. a Qiskit transpiler pass that "CliNR-wraps" a Clifford block.
- Prior art: IonQ internal code. No public Qiskit implementation found [unverified, GitHub search only].
- Collision hint: software testing, where verifying a resource state = unit tests on a component before it ships; quality control in manufacturing (reject defective parts upstream).

### S-A-3: Decoded Quantum Interferometry (DQI) on toy OPI / max-XORSAT, plus its dequantizations
- What: Google's DQI (Jordan et al., Nature, Oct 2025) uses a QFT to turn optimization into decoding. Its flagship case is Optimal Polynomial Intersection: about 0.718 of constraints satisfied, versus about 0.55 for the best known classical polynomial-time algorithm. Counter-evidence: for MaxCut, DQI-tractable instances are classically solvable exactly (arXiv:2509.19966, TQC 2026), and there is an overlap-gap obstruction for unstructured max-k-XORSAT. Follow-ups: Maslov & Jordan circuits (2510.10967), nearly linear time (2601.15171).
- Source: arXiv:2408.08292; https://research.google/blog/a-new-quantum-toolkit-for-optimization/ ; Quanta (Mar 2025); https://arxiv.org/abs/2504.18334 (circuit design, simulated up to 30 qubits); https://arxiv.org/html/2509.19966v2
- Rarity: 4.
- Evidence of need: active theory debate, and the most prominent candidate for a verifiable optimization advantage. A small, visual, end-to-end example is missing.
- Quantum hook: essential. Interference through the Fourier transform is the whole algorithm.
- Buildability: **medium-low**. Coherent decoding is the hard part. On toy sizes (m≈8 constraints, n≈4 vars, small field or GF(2)) we can use a reversible lookup-table decoder. That gives roughly 15–25 qubits [estimate, unverified]. Expect 10+ hours from the quantum student alone.
- Theme fit: Unlocked; contrarian Impact ("where DQI wins, where it provably doesn't").
- Prior art: Classiq notebook for DQI on max-XORSAT (https://docs.classiq.io/explore/algorithms/search_and_optimization/dqi/dqi_max_xorsat.md), which is Classiq, not Qiskit. yezhuoyang/DQI (only a README, 1 star). OpenQuantumInstitute/2025-team-mohituQ (ocean-trash DQI, a hackathon entry!). magic-state-labs/dqi-screening-code. EgrettaThula/gs-dqi-reproducibility. There is prior art, but no polished Qiskit explainer.
- Collision hint: Reed–Solomon codes in QR codes and CDs ("the algorithm that decodes a scratched CD to solve optimization"); polynomial regression in data science.

### S-A-4: Quantum Echoes / OTOC(2), Google's "verifiable advantage" (Nature, Oct 2025)
- What: Run forward U, apply a butterfly perturbation B, run backward U†, then probe M. Second-order OTOCs show constructive interference at the edge of ergodicity. Google reported 13,000× vs Frontier on Willow. A TNBP (tensor-network belief propagation) attack failed [preprint]; classical hardness is still open.
- Source: https://research.google/blog/a-verifiable-quantum-advantage/ (Oct 2025); Xu & Swingle tutorial, PRX Quantum 5, 010201 (2024); OTOC spectroscopy arXiv:2511.22654.
- Rarity: 3. Press-famous, but few people understand *why* OTOC(2) matters.
- Evidence of need: high public attention, and "verifiable" is a confusing claim worth explaining.
- Quantum hook: essential. Time reversal and many-body interference of Pauli paths.
- Buildability: **high**. 8–20 qubits, one circuit per (t, B, M) point. Trapped-ion all-to-all speeds up scrambling, and the first verified-scrambling experiment was itself on trapped ions (Landsman et al., Nature 2019, 7 qubits).
- Theme fit: Playground ("butterfly echo" sonification: the louder the echo, the less scrambled) and Unlocked.
- Prior art: plenty of OTOC theory tutorials and papers. I found no Qiskit OTOC(2) interactive [unverified]. Generic OTOC notebooks probably exist; the novelty has to come from the experience.
- Collision hint: acoustic echo and reverb in music, Loschmidt "can you un-stir the coffee", rumor spread on social networks.

### S-A-5: Measurement-induced phase transition (MIPT) without postselection, using tree circuits (2025)
- What: Feng, Côté, Kourtis & Skinner (2025, Quantinuum H1-1) use *tree-structured* circuits. Here the MIPT has an exact solution (critical point and scaling) and needs no postselection. The idea is "watching too often freezes entanglement". Earlier trapped-ion observation: Noel et al. 2021 (Monroe/IonQ lineage).
- Source: arXiv:2502.01735 ; arXiv:2106.05881 ; lecture notes arXiv:2307.02986.
- Rarity: 4.
- Evidence of need: a famous phenomenon with no Qiskit tutorial found (searched; IBM has only a related Nishimori tutorial).
- Quantum hook: essential. Measurement backaction against entangling dynamics.
- Buildability: **medium**. Needs mid-circuit measurement (MCM) [check IonQ sim support]. Tree circuits are shallow, and 8–16 qubits is enough for a visible crossover. Exact theory gives a ground-truth curve to plot against.
- Theme fit: Unlocked / Playground ("the observer's slider").
- Prior art: papers only; no interactive demo found [unverified].
- Collision hint: surveillance and privacy ("monitoring kills correlation"), attention economy, a quantum Zeno game.

### S-A-6: Peaked circuits and their 2026 classical break
- What: Aaronson & Zhang (2024) proposed peaked circuits: random-looking circuits with one hidden high-probability bitstring, which makes them verifiable. BlueQubit + Zhang ran 56 qubits / about 2,000 gates on Quantinuum H2 and claimed heuristic advantage (arXiv:2510.25838). In **Apr 2026, Kremer & Dupuis (arXiv:2604.21908) simulated the largest instance in about 68 min on one A100**, half the QPU time. Their attack contracts the mirrored halves into an MPO and greedily "unswaps" the hidden permutations.
- Source: arXiv:2404.14493 ; arXiv:2510.25838 ; https://www.emergentmind.com/papers/2604.21908 ; IBM Quantum Advantage Tracker https://www.ibm.com/quantum/blog/quantum-advantage-tracker
- Rarity: 5 for the break (6 months old, niche).
- Evidence of need: the advantage tracker exists precisely to host this attack-and-defend cycle.
- Quantum hook: essential for the construction (interference concentrates amplitude). Note the contrarian truth: the obfuscation was the weak point.
- Buildability: **medium**. Building small peaked circuits (10–16 qubits) by optimizing the second half to peak is doable. A simplified MPO attack is doable for the student plus the grinder. An "obfuscation vs. attack" game is possible.
- Theme fit: Playground (a hide-the-peak puzzle, CTF style) / Unlocked (how advantage claims die).
- Prior art: the papers above. Kremer–Dupuis code release unknown [unverified].
- Collision hint: CTF crypto challenges, steganography, ICPC "hack" phases (Codeforces hacking).

### S-A-7: Quantum Dynamic Programming (Son, Gluza, Takagi, Ng, PRL 134, 180602, May 2025)
- What: Store intermediate quantum states as "memory" and reuse them, via density-matrix exponentiation, to build the next recursion step's unitary. This gives an exponential *depth* reduction for fixed-point recursions, paid for in *width* (copies). Applications include a Grover variant, double-bracket imaginary-time evolution, and oblivious Schmidt-basis preparation.
- Source: arXiv:2403.09187 ; https://www.cqt.sg/?p=20403 ; code: qiboteam/qibo-qdp (Qibo, 1 star).
- Rarity: 5.
- Evidence of need: no hardware demonstration found and no Qiskit implementation.
- Quantum hook: essential. You cannot copy the state (no-cloning), so you consume copies. This is the quantum twist on memoization.
- Buildability: **low-medium**. Each recursion level multiplies the number of copies needed, so ≤25 qubits gives only 1–2 recursion levels on 1–2 qubit targets. That is honest but small. Hard to make pretty in 20h.
- Theme fit: Unlocked, with a strong *story* for Uriel (an ICPC DP lover: "memoization when you can't copy memory").
- Prior art: qibo-qdp only. Unrelated repos share the name (annealing DP for economics).
- Collision hint: competitive programming DP, caching and CDNs, biology (cells "consuming" templates).

### S-A-8: Magic state cultivation (Gidney, Shutty, Jones 2024) and its 2025 experiment
- What: "Grow" a T state inside a surface-code patch at about the cost of a lattice-surgery CNOT. It reaches about 2·10⁻⁹ logical error at 10⁻³ noise and arguably removes the need for distillation. A 2025 superconducting experiment (Rosenfeld, Gidney et al.) showed about 40× error reduction.
- Source: arXiv:2409.17595 ; APS March 2025 talk (Cody Jones); arXiv:2512.13908 [title not fully checked].
- Rarity: 4.
- Evidence of need: I found no interactive explainer at all (searched). The QEC community treats it as a key resource-estimate driver.
- Quantum hook: essential (non-Clifford resources, QEC).
- Buildability: **medium** as an explainer, **low** as a faithful sim. Real cultivation circuits are stim-scale (tens of qubits, Clifford+T check). A toy version fits: a d=3 color-code T-check, postselected, with ≤~20 qubits [estimate].
- Theme fit: Unlocked ("why T gates are the expensive ones, and how a gardener grows them").
- Prior art: Gidney's stim code / Zenodo data [believed public, unverified]; papers.
- Collision hint: horticulture metaphor, sourdough starters (cultivate, check, discard), quality-gated supply chains.

### S-A-9: Bivariate bicycle / gross codes, and why trapped ions fit them naturally
- What: IBM's qLDPC family. The [[144,12,12]] gross code is built from A=x³+y+y², B=y³+x+x², with H_X=[A|B]. "Tour de gross" (arXiv:2506.03094, 2025) designs a modular computer around it. The checks are *long-range* on a 2D grid; IBM needs special couplers for that. **Trapped ions have all-to-all connectivity natively**, which is a clean IonQ-flavoured connection.
- Source: arXiv:2308.07915 ; arXiv:2506.03094 ; arXiv:2603.19062 (decoder baselines); Riverlane deltakit `BivariateBicycleCode`.
- Rarity: 3 (big QEC topic) to 4 (for the ion angle).
- Evidence of need: there is no interactive Tanner-graph/torus visualizer (searched); the codes are hard to picture.
- Quantum hook: essential for teaching. For a *simulation*, the [[72,12,6]] code means about 144 qubits with ancillas, which only a stabilizer sim can handle. **Qollab browser runtime support for Aer stabilizer is [unverified]**.
- Buildability: **medium** as a visual plus classical decoding sim; **low** as a state-vector Qiskit run. Small cousins could fit 25 qubits, e.g. the [[18,4,4]]-type BB codes [unverified parameters].
- Theme fit: Unlocked.
- Prior art: papers, deltakit, bbqec/bbqudit PyPI packages. No interactive explainer found.
- Collision hint: donut/torus video-game maps (Pac-Man wraparound), network topology design, RAID storage.

### S-A-10: Random unitaries in extremely low depth (Schuster, Haferkamp, Huang, Science, Jul 2025)
- What: Glue small local random patches together and you get unitary designs in **log n depth** on a 1D line. Pseudorandom unitaries appear in polylog depth (1D) and polyloglog depth with all-to-all connectivity. A corollary: classical shadows built from log-depth Cliffords are as powerful as deep ones.
- Source: arXiv:2407.07754 ; Science 10.1126/science.adv8590.
- Rarity: 4.
- Evidence of need: theory only; I found no public demo.
- Quantum hook: essential (unitary designs, indistinguishability).
- Buildability: **medium-high**. 8–16 qubits; compare frame potential / k-th moments of the patchwork against brickwork against Haar. A Playground "can you tell?" game (a Turing test for randomness) is a nice frame. All-to-all depth advantage gives an IonQ hook.
- Theme fit: Playground / Unlocked.
- Prior art: none found as code [unverified].
- Collision hint: shuffling cards (Bayer–Diaconis "7 riffle shuffles"), cryptographic block ciphers (Feistel rounds).

### S-A-11: Generative quantum advantage (Huang et al., Google, arXiv:2509.09033, Sep 2025)
- What: "Instantaneously deep" QNNs. Training is classically efficient through a "sewing" divide-and-conquer method with no barren plateaus, but *sampling* needs a QPU. Demonstrated on 68 superconducting qubits. Also compresses deep circuits into shallow ones.
- Source: https://arxiv.org/abs/2509.09033 ; https://research.google/pubs/generative-quantum-advantage-for-classical-and-quantum-problems/
- Rarity: 4.
- Evidence of need: preprint; I found no public code [unverified].
- Quantum hook: essential, with the honest caveat that the advantage is in sampling, not in usefulness.
- Buildability: **medium**. Reproducing the sewing learner at 10–16 qubits is feasible for a strong student. Explaining "the asymmetry is the point" is the value.
- Theme fit: Unlocked; Impact is weak (no real dataset).
- Prior art: paper only.
- Collision hint: generative AI ("train on a laptop, generate on a QPU"), fonts and music generation.

### S-A-12: Ansatz-free Hamiltonian learning at the Heisenberg limit (PRX Quantum, Oct 2025)
- What: Learn an *unknown sparse* Hamiltonian (structure included) using only black-box time-evolution queries and minimal control, with Heisenberg-limited precision. There is a proven trade-off between evolution time and control. Related: no-short-time-control version (arXiv:2604.27838); 300-ion Hamiltonian learning (Sci. Adv. 2025).
- Source: arXiv:2502.11900 ; arXiv:2604.27838.
- Rarity: 5.
- Evidence of need: numerics only in the paper; there is real need from hardware calibration.
- Quantum hook: essential (learning from quantum dynamics).
- Buildability: **medium**. A "reverse-engineer the hidden physics" interactive game: the player queries U(t) on 4–8 qubits, each query is one IonQ job, and the player infers the couplings. A simplified (non-optimal) learner is fine.
- Theme fit: Playground / Unlocked. Impact angle: calibrating ion-trap couplings.
- Prior art: papers; no interactive found.
- Collision hint: **ICPC interactive problems** (query an oracle, minimize queries); system identification in control engineering; detective games.

### S-A-13: Dequantization wave 2025–26, "advantage court"
- What: Classical algorithms are catching up with quantum speedup claims. Short-path algorithms for MAX-k-CSP: a classical 2^((1-c)n) algorithm kills the super-quadratic claim (arXiv:2604.12131, Apr 2026). Linear classical dynamics with local interactions: dequantized (arXiv:2505.10445). QML via random Fourier features (arXiv:2505.15902). DQI-MaxCut: no advantage (S-A-3). Peaked circuits broken (S-A-6). Quantum RL surrogates (arXiv:2609.16266, Sep 2026).
- Source: as listed.
- Rarity: 4 as a unified picture.
- Evidence of need: the IBM Quantum Advantage Tracker exists because claims keep being challenged.
- Quantum hook: the honest contrast is the hook. Each "case" pairs a tiny quantum run with its classical opponent.
- Buildability: **medium**. Each case is small, but you need 3–4 cases to make the point. The risk is spreading too thin.
- Theme fit: Unlocked; Best documentation.
- Prior art: no interactive aggregator found; the IBM tracker is a table.
- Collision hint: courtroom / sports VAR replay format; fact-checking journalism.

### S-A-14: Certified randomness (JPMorgan + Quantinuum, Nature 640, Mar 2025). Warning card.
- What: Random circuit sampling challenges answered faster than a classical computer could spoof them give 70k+ certified random bits on 56 qubits.
- Source: https://www.jpmorganchase.com/about/technology/news/certified-randomness ; Nature 640, 343 (2025).
- Rarity: 3.
- Quantum hook: essential on a real QPU, but **meaningless on a simulator**: the certification rests on the classical machine being too slow. Any hackathon "certified randomness" demo on Qollab is pseudo-quantum by construction.
- Buildability: high to imitate, low to make honest.
- Theme fit: Unlocked only if framed as "why this can't be certified here". Otherwise avoid.
- Prior art: lots of QRNG hackathon projects (crowded).
- Collision hint: lotteries, provably fair gaming.

### S-A-15: Quantum reservoir computing. Low-signal card.
- What: Use fixed quantum dynamics as a reservoir for time-series prediction. A few-atom QRC outperforms classical reservoirs on Mackey-Glass (PRR, Apr 2025). There is a 2026 6-qubit finance paper (arXiv:2602.13094) and a 2026 review (arXiv:2607.18552).
- Rarity: 2–3.
- Quantum hook: weak. Advantage claims are shaky and classical reservoirs are strong baselines.
- Buildability: high (QuantumReservoirPy exists, JOSS 2025).
- Theme fit: Impact, but judges will push hard on the baseline.
- Prior art: crowded. **Recommend skipping.**
- Collision hint: none compelling.

### S-A-16: Nobel 2025 (macroscopic quantum tunneling). Low-signal card.
- What: Clarke, Devoret and Martinis, for MQT and energy quantization in a Josephson-junction circuit (Berkeley, mid-1980s), which became the foundation of transmon qubits.
- Source: https://physicsworld.com/a/john-clarke-michel-devoret-and-john-martinis-win-the-2025-nobel-prize-for-physics/
- Rarity: 1 (everyone heard about it).
- Quantum hook: mostly decorative for a qubit-circuit hackathon. Simulating a washboard-potential tunneling on discretized qubits is possible but contrived. And it is superconducting hardware, not IonQ's ions.
- Buildability: medium. Theme: Unlocked (history). **Weak; anniversary hook only.**

### S-A-17: IonQ-specific landscape, 2025–26 (context for pitching)
- What: Tempo reached #AQ 64 (Sep 2025). Nine QCE26 papers (Sep 2026), including Mid-Circuit CliNR, DQAOA-GPT, Quantum Parity, and protein folding with Kipu (46–61 qubits). There is a compiled resource estimate for Shor on 256-bit keys. Superion 256 platform.
- Source: https://quantumcomputingreport.com/ionq-demonstrates-hybrid-hpc-and-quantum-ai-workflows-across-nine-peer-reviewed-papers-at-ieee-quantum-week-2026/ ; https://quantumcomputingreport.com/ionq-reaches-aq-64-milestone-on-100-qubit-tempo-system-ahead-of-schedule/
- Takeaway: IonQ cares about **all-to-all connectivity, error mitigation (CliNR), and application benchmarks**. Projects that use all-to-all connectivity *on purpose* (S-A-1 periodic wrap, S-A-2, S-A-9 long-range checks, S-A-10 polyloglog depth) will resonate with them. Company claims are not independently verified.

---

## Top 3 from this front

1. **S-A-1, Quantum information supremacy, interactive ("Memory Duel").** It is the only 2025 "advantage" result that is *provable* and needs only 12 qubits. MIT reference code exists to port, it fits one circuit per run, the authors list open problems, and the "k classical bits vs 12 qubits" game makes it click.
2. **S-A-2, CliNR in Qiskit.** IonQ's own 2025–26 error-reduction technique. It needs 13–19 qubits and one postselected circuit, and I found no public Qiskit version. It lands directly with IonQ-engineer judges, and the stabilizer-selection optimization is a natural algorithmic hook.
3. **S-A-3 + S-A-13, DQI and the "advantage court".** The most interesting live debate: a Nature 2025 claim and its 2025–26 partial dequantizations. A tiny DQI next to its classical opponents is honest and contrarian. It is the riskiest build (the coherent decoder), so it is best paired with S-A-4 Quantum Echoes as an easier fallback case.

Honourable mention: **S-A-6, the peaked-circuit break (Apr 2026)**. It has the rarest signal on this front and is a natural CTF/game format.
