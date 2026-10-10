# Front B — Real pain of quantum practitioners & learners

Scout: Front B agent. Collected 2026-10-10. Sources: GitHub API via `gh`, the StackExchange API (live counts), HN Algolia API (live), arXiv abstracts, and web search.

**Upfront finding (contrarian):** Pain in quantum software does **not** show up as GitHub reactions. The most-reacted open issue in Qiskit/qiskit has **6 reactions** (#6740), and qiskit-ibm-runtime tops out at **2**. People don't vote on quantum pain in issue trackers. It shows up in three other places: Q&A sites (QCSE has 2,619 `qiskit`-tagged questions), HN fights about whether a result is real, and education papers. Don't build a pitch on "Qiskit issue #N has many upvotes", because no such issue exists.

Method notes: QCSE full-text search counts (marked ~) are fuzzy keyword matches, so read them as an order of magnitude only. Tag totals and unanswered counts are exact API numbers.

---

### S-B-1: "Did the quantum computer actually do anything?" Output vs. noise is unverifiable (the /dev/urandom scandal)
- What: In April 2026 Project Eleven paid **1 BTC** for "the largest quantum attack on ECC to date", a 17-bit ECC key recovered on IBM Quantum hardware. Yuval Adam then swapped the IBM backend for `/dev/urandom` and **still recovered the key**. The submission's own README admits the output was "indistinguishable from uniform random sampling at the bitstring level" and that "only the true d passes EC verification." The classical post-processing filter did all the work.
- Source: HN "Replace IBM Quantum back end with /dev/urandom", **383 pts / 50 comments**, 2026-04-25 https://news.ycombinator.com/item?id=47897647 · repo https://github.com/yuvadm/quantumslop · Gutmann on the cryptography list https://www.metzdowd.com/pipermail/cryptography/2026-April/039486.html
- Rarity: 3. Crypto and quantum Twitter know it; most hackathon teams won't.
- Evidence: Craig Gidney (HN user Strilanc) commented: *"for small numbers, Shor's algorithm succeeds quickly when fed random samples. And when your circuit is too long (given the error rate of the quantum computer), the quantum computer imitates a random number generator. So it's trivial to 'do the right thing' and succeed for the wrong reason."* Another commenter: *"The article itself is maddeningly vague on exactly what happened here… I'm not able to parse the particulars."* Related: Gutmann & Neuhaus, "Replication of Quantum Factorisation Records with an 8-bit Home Computer, an Abacus, and a Dog" (IACR ePrint 2025/1237), argues that *all* publicised quantum factorisations used trickery.
- Quantum hook: ESSENTIAL. The tool would run the same circuit three ways: ideal, noisy, and a random or classical control. It would then measure how much quantum signal survives (heavy-output probability, cross-entropy/XEB, or distance to uniform) and how much the classical verifier is "cheating."
- Buildability: HIGH. Shor/ECDLP-lite or period finding on ≤ 12 qubits; Aer noise models with increasing depth; compare against a uniform sampler. One circuit per run is fine, since each mode is its own run.
- Theme fit: Unlocked (teach "how to tell real quantum from noise") plus Impact (a validation tool for prize and paper claims).
- Prior art: XEB and heavy-output tests are standard in research. IBM's Quantum Advantage Tracker (2025) collects advantage claims for classical challenge. Metriq does benchmarking. None of them is an interactive "slop detector" for a single circuit plus post-processing pipeline. Not verified exhaustively.
- Collision hint: plagiarism and AI-slop detectors, scientific fraud forensics, the "placebo arm" in clinical trials.

### S-B-2: "Why haven't quantum computers factored 21 yet?" Resource cost is invisible, so claims can't be judged
- What: Gidney's 2025 post shows that factoring 21 needs about **115× the cost** of the famous factor-15 circuit (or ~500× realistically), because 15 has special structure. The public can't see why. People ask "same computers that will break ECC? Now I'm very confused."
- Source: HN **340 pts / 197 comments**, 2025-08-31 https://news.ycombinator.com/item?id=45082587 · https://algassert.com/post/2500 · HN "A cryptography engineer's perspective on quantum computing timelines" **551 pts / 248 comments**, 2026-04-06 https://news.ycombinator.com/item?id=47662234
- Rarity: 3.
- Evidence: Comments include *"And these are the same quantum computers that will eventually break ecliptic curve cryptography? Now I'm very confused."*; *"So how many gates are we talking to factor some 'cryptographically useful' number?"*; and *"what they did was not factorization, but 'print 3' with extra steps."* A commenter on the timelines thread: *"What surprises me is how non-linear this argument is…"* The Unitary Foundation 2025 survey (1,400+ respondents) got 102 free-text answers on what people use resource estimation for, and "resource estimation & planning" was the top category (33).
- Quantum hook: ESSENTIAL if the user can *build* the modular-multiplication circuit for N = 15, 21, 35… and watch gate count, depth, and simulated success under noise blow up, with no hand-waving.
- Buildability: MED-HIGH. Small Shor instances fit in ≤ 15 qubits. Scaling curves come from transpile counts, which is cheap. Extrapolating to RSA-2048 needs published formulas (Gidney 2025 "<1M qubits").
- Theme fit: Unlocked (strong) / Impact.
- Prior art: Gidney's blog; Azure Quantum Resource Estimator; Qualtran (Google). These are expert tools, not a hands-on "feel the wall" experience.
- Collision hint: Moore's-law charts, the doomsday clock, a "cost to break" ticker.

### S-B-3: Measurement is the #1 conceptual wall
- What: Learners can run the math but can't reconcile unitary gates with irreversible measurement, measuring "in a basis", and how measuring one qubit affects the others.
- Source: QCSE `measurement` tag: **780 questions, 126 unanswered (16%)**. Top questions: "If all quantum gates must be unitary, what about measurement?" (41 votes, 7.8k views) https://quantumcomputing.stackexchange.com/questions/136 · "How to measure in another basis" (18.2k views) https://quantumcomputing.stackexchange.com/questions/13605 · "What does 'measurement in a certain basis' mean?" (8.7k views) · "How does measurement of one qubit affect the others?" (5.5k views). A recent r/QuantumComputing thread (mirror, date unverified) asks about the gap between unitary evolution and "one definite observed outcome." QCCS (validated concept survey v2.2, Spring 2025) treats measurement as a core item: https://www.physport.org/assessments/assessment.cfm?A=QCCS
- Rarity: 1. Everyone knows measurement is confusing.
- Evidence: see above. A ~347-hit keyword match on "why measurement" (fuzzy).
- Quantum hook: ESSENTIAL by definition. Mid-circuit measurement and basis choice change outcomes.
- Buildability: HIGH.
- Theme fit: Unlocked / Playground.
- Prior art: VERY crowded (Quirk, IBM Composer, countless Bloch-sphere apps). Only worth doing with a radically new framing.
- Collision hint: detective games where looking at evidence destroys it; photography (shutter = measurement).

### S-B-4: Phase (relative vs. global) and interference never click, and everything downstream depends on them
- What: Students don't recognize that relative phases have measurable effects. That blocks interference, phase kickback, Grover, QPE, and QFT.
- Source: Wan, Emigh & Shaffer (UW), PER study on relative phase (via PER Central / par.nsf.gov). QCSE: "What is the difference between a relative phase and a global phase?" (34 votes, **24.4k views**) https://quantumcomputing.stackexchange.com/questions/5125 · "Why does the 'Phase Kickback' mechanism work in QPE?" (29 votes, 7.8k views) https://quantumcomputing.stackexchange.com/questions/2565 · "Is there a layman's explanation for why Grover's algorithm works?" (16.5k views) · "If quantum speed-up is due to the wave-like nature… why not just use regular waves?" (39 votes).
- Rarity: 2.
- Evidence: the PER finding is that many students "do not recognize that relative phases have measurable effects." Global phase gets ~131 fuzzy QCSE hits and phase kickback ~50.
- Quantum hook: ESSENTIAL. Interference is the only real source of advantage.
- Buildability: HIGH (2–5 qubits).
- Theme fit: Unlocked / Playground (phase as sound or color is a natural fit for music).
- Prior art: crowded (Quirk shows amplitudes and phases; "Quantum Odyssey"; many audio-phase demos). The gap is making phase *audible or physical* in a game where you lose if you ignore it. Not verified unique.
- Collision hint: noise-cancelling headphones (destructive interference), music harmonics, rowing in sync.

### S-B-5: Error correction / surface code / magic states: huge demand, thin intuition, 41% blame training
- What: QEC is now the industry's main storyline (Willow below threshold, IBM Starling 2029 with 200 logical qubits, bivariate-bicycle codes, magic state cultivation). Intuition for syndromes, decoders, thresholds and magic states is scarce even among professionals.
- Source: QCSE `error-correction` tag: **1,253 questions, 216 unanswered (17%)**. "What is the surface code?" (49 votes, **25.5k views**) https://quantumcomputing.stackexchange.com/questions/2106 · "What are magic states?" (38 votes, **18.2k views**) https://quantumcomputing.stackexchange.com/questions/13629 · "Intuition about Knill-Laflamme QEC conditions" (8.5k views). From 2025–26 the questions turn expert-level and some go unanswered, e.g. "How should I think about Single Shot decoding?" (0 answers) and "logical T gates in the recent BB architecture paper" (0 answers). The `stim` tag has 423 questions (QEC tooling demand). Riverlane QEC Survey 2025 (300+ professionals): **41% cite limited training as the top barrier**, 96% expect to rely on external support, and only 4% plan to build in-house https://thequantuminsider.com/2025/08/11/survey-wide-gap-between-qec-awareness-and-qec-capabilities/ . Unitary 2024 survey: 51.6% called error correction the most promising area.
- Rarity: 2 for the topic, 4 for the "41% training gap" stat.
- Quantum hook: ESSENTIAL. A repetition or small surface code with real syndrome measurement, all in one circuit. That fits IonQ's one-job rule because syndromes and data are measured together at the end, or with mid-circuit measurement if supported (verify on Qollab).
- Buildability: MED-HIGH. A distance-3 repetition code is ~5 qubits. A d=3 rotated surface code is 17 qubits (one round), which fits ≤ 25. Decoding is classical (lookup or MWPM via a small greedy algorithm, which suits an ICPC captain).
- Theme fit: Unlocked (the explicitly named topic).
- Prior art: Decodoku (2017 mobile puzzle, decoding as a game); Gidney's Crumble (browser Stim circuit editor, expert-facing); QEC-Playground (Rust, research); the Error Correction Zoo. No widely known *Qiskit-native, run-the-real-circuit* QEC game was found in 2025–26 (unverified beyond search).
- Collision hint: Minesweeper and Sudoku (syndrome = clues); immune system (detect without looking); RAID / ECC RAM.

### S-B-6: Debugging quantum programs is "print statements and prayer"
- What: The 2025 William & Mary practitioner survey (26 developers plus interviews) found everyone tests. Only **31%** use quantum-specific testing tools, and debugging means print statements, circuit drawings and simulators, *"which respondents noted do not scale well."* Core issues they report: probabilistic execution, limited observability, shallow abstractions.
- Source: Zappin, Stalnaker, Chaparro, Poshyvanyk, arXiv:2506.17306 (v1 Jun 2025, v2 Jan 2026) https://arxiv.org/abs/2506.17306 . I couldn't extract quotes from the full PDF. Numbers are from the abstract: unit testing 88%, bug sources library updates 81%, developer errors 69%, compatibility 62%. Interview quote (via search snippet, unverified in full text): *"You need to do a lot of thinking about how to translate bit logic to the so-called qubit logic."* LSU repo mining (qsw25) of 21k+ issues and commits: **34% of issues quantum-specific**, corrective commits only 18.54% https://csc.lsu.edu/~ufarooq/assets/pdf/qsw25.pdf . The quantum-software-engineering roadmap paper notes testers "may be unable to reliably determine whether a test case failed… or was due to noise" https://arxiv.org/pdf/2404.06825
- Rarity: 3.
- Quantum hook: ESSENTIAL (you can't inspect a state without destroying it, which is the debugging pain itself). But a debugger is a dev tool, a weaker demo story.
- Buildability: MED. Statevector diff "breakpoints" on a simulator are easy. Statistical assertions are medium.
- Theme fit: Impact (dev tooling) / Unlocked.
- Prior art: Qiskit has no debugger. Academic: Quito, QuSBT, statistical assertions (Huang & Martonosi 2019), Bugs4Q dataset. HN "Observability for quantum SDK workflows" (2026-04, 2 pts) got no traction https://news.ycombinator.com/item?id=47766236
- Collision hint: Chrome DevTools, flight recorders, medical imaging that can't open the patient.

### S-B-7: Qubit ordering / endianness: the eternal paper cut
- What: Qiskit is little-endian (q0 is the rightmost bit), while textbooks are big-endian. Learners' results look "reversed."
- Source: QCSE "Big Endian vs. Little Endian in Qiskit" (7.1k views) https://quantumcomputing.stackexchange.com/questions/8244 ; "Qubit ordering in qiskit" (3.3k views). Qiskit issue #1148 "qiskit ordering convention" (19 comments, 2018), #7628 "Support alternative tensor product ordering" (12 comments). ~108 fuzzy QCSE hits for "bit order", ~103 GitHub issues across the Qiskit org.
- Rarity: 1 among Qiskit users.
- Quantum hook: decorative (a convention, not physics).
- Buildability: HIGH, but low value.
- Theme fit: none (a docs footnote at most). **Don't build this.** Make sure your own demo never trips on it, since judges will notice.
- Prior art: Qiskit docs already explain it.

### S-B-8: SDK churn breaks every tutorial (Qiskit 1.0 → 2.0)
- What: `execute()` was removed (deprecated in 0.x, removed in 1.0, from my knowledge), and 2.0 removed `c_if`, `BackendV1`, `qiskit.pulse` and V1 primitives. Old tutorials and Stack Overflow answers fail. Downstream libraries break (e.g. aer-gpu 0.15.1 vs Qiskit 2.0, issue #2336, which with **6 reactions is the most-reacted open Aer issue**).
- Source: https://quantum.cloud.ibm.com/docs/en/api/qiskit/release-notes/2.0 · SO "cannot import name 'execute' from 'qiskit'" (2.7k views) https://stackoverflow.com/questions/78657935 · QCSE "Getting error when importing qiskit_algorithms in Qiskit 2.1.0" (960 views, Jul 2025) · https://github.com/Qiskit/qiskit-aer/issues/2336 · Aer issue #2134 "Documentation has not been updated since Qiskit 0.22." Unitary 2024 survey: **50.8% of people who don't use a tool they want cite "poorly documented."** The practitioner survey says 81% name library updates as a bug source.
- Rarity: 1.
- Quantum hook: none (a classical software problem).
- Buildability: n/a.
- Theme fit: none / Best Documentation. Practical takeaway: pin Qiskit versions and document them well, which costs little and wins the documentation award.

### S-B-9: Noise and decoherence feel like a black box, and noise questions go unanswered most often
- What: The `noise` tag has the **highest unanswered rate measured: 70 of 247 (28%)**, against 16–17% for measurement and QEC. `transpile` is at 18/76 (24%). Learners can't predict how depth, gate choice and qubit mapping turn into errors, or why simulator results differ from hardware.
- Source: StackExchange API counts (2026-10-10). "How to selectively apply noise in Qiskit simulations?" (2.5k views) · "Transpiling qiskit quantum circuits on IonQ Native Gates" (1.7k views) https://quantumcomputing.stackexchange.com/questions/30294 · The multivocal literature review arXiv:2609.00354 says the most reported challenges are "scalability, hardware noise, measurement limitations, probabilistic outputs, debugging limitations, and tool limitations."
- Rarity: 3 for the unanswered-rate stat.
- Quantum hook: ESSENTIAL. A noise budget depends on circuit structure, and IonQ's all-to-all connectivity (no SWAPs) against heavy-hex is a real, demonstrable difference.
- Buildability: HIGH (Aer noise models; IonQ simulator has a noise option, verify on Qollab).
- Theme fit: Unlocked / Impact.
- Prior art: IBM learning modules on noise; Mitiq (used by 9%). No intuitive "noise budget" visual found.
- Collision hint: an audio signal chain (each gate adds hiss); the telephone game; a battery draining.

### S-B-10: Entanglement: "how do I know it's entangled?"
- What: One of the most-viewed practical questions on QCSE.
- Source: "How do I show that a two-qubit state is an entangled state?" (55 votes, **42.1k views**) https://quantumcomputing.stackexchange.com/questions/2263 · "Can the Bloch sphere be generalized to two qubits?" (9.6k views) · `entanglement` tag has 945 questions.
- Rarity: 1.
- Quantum hook: ESSENTIAL.
- Buildability: HIGH (CHSH game with one circuit and 4 settings measured together, or randomized settings).
- Theme fit: Playground / Unlocked.
- Prior art: VERY crowded (CHSH games, Bell test demos, the HN "Bell's Inequalities with Qiskit" post from 2025).

### S-B-11: "It tries all answers in parallel": the speedup myth
- What: The most persistent lay misconception, and the HN default.
- Source: HN comment 2024-11-20: *"Been trying for the longest time, I still don't understand how quantum computing work. It's always something-something tries all possible combinations and viola, your answer."* https://news.ycombinator.com/item?id=42198056 · QCSE "Is quantum computing just pie in the sky?" (183 votes, **44.5k views**, the #1 voted question on the site) https://quantumcomputing.stackexchange.com/questions/2499 · "Effects of quantum computing on parallel universes" (15.2k views).
- Rarity: 1.
- Quantum hook: ESSENTIAL. Show that naive superposition plus measurement gives a random answer, and that only interference (Grover/Deutsch-Jozsa) beats it.
- Buildability: HIGH.
- Theme fit: Unlocked / Playground.
- Prior art: Scott Aaronson's SMBC comic "The Talk" (2015); many explainers. A crowded *message*, but rarely made *interactive and falsifiable*.

### S-B-12: Instructors: no standard curriculum, a math wall, few validated materials
- What: Instructors report diverse student backgrounds, linear algebra as a blocker, and too few curricular materials. Each course "tells a different story." Students struggle with matrix representation, **rotation gates**, and analyzing teleportation circuits. They prefer Dirac notation over matrices and the Bloch sphere. A mini-tutorial that forced all three representations improved Bloch-sphere understanding.
- Source: Meyer, Passante, Pollock, Wilcox, PRPER 18, 010150 (2022) https://link.aps.org/doi/10.1103/PhysRevPhysEducRes.18.010150 · arXiv:2507.09656 (2025) https://arxiv.org/abs/2507.09656 · Seifollahi & Singh instructor interviews, arXiv:2510.00150 (Sep 2025) · concept inventory with expert interviews arXiv:2512.20836 (Dec 2025) ("substantial conceptual content… students can learn before studying the mathematics") · Resource Letter QIE-1, arXiv:2606.06445 (Jun 2026). Unitary 2025 survey: "Learning, Mentorship & Training" was the #1 open-ended need (25 of 88).
- Rarity: 3.
- Quantum hook: depends on the build.
- Buildability: n/a (context card).
- Theme fit: Unlocked. Takeaway: a **math-free-first, multi-representation** tool (Dirac, matrix and Bloch linked live) is what education research says works.
- Prior art: QuILTs (Singh group), IBM Learning, Quantum Odyssey, Quirk.

### S-B-13: Benchmarking and claims can't be compared across platforms
- What: Native gate sets, connectivity, compiler choices, non-uniform provider metadata and queue variability make cross-device results irreproducible. IBM launched a community **Quantum Advantage Tracker** (QDC Nov 2025) and placed its July 2026 advantage claims (3 preprints, Heron R3 with error mitigation) there for classical challenge.
- Source: Metriq paper arXiv:2603.08680 (Mar 2026) https://arxiv.org/abs/2603.08680 · https://www.ibm.com/quantum/blog/qdc-2025 · https://www.livescience.com/technology/quantum/ibm-scientists-claim-theyve-achieved-quantum-advantage-and-theyve-dared-others-to-prove-them-wrong
- Rarity: 4 (the tracker exists; few outsiders know how claims are adjudicated).
- Quantum hook: ESSENTIAL but heavy. Real cross-platform benchmarking needs real hardware, while Qollab offers simulators only.
- Buildability: LOW-MED within Qollab limits (simulators only, so you can't benchmark real devices). A teaching version ("be the referee of an advantage claim") is feasible.
- Theme fit: Unlocked / Impact.
- Prior art: Metriq, QED-C benchmarks, the Advantage Tracker. Building infrastructure here is a losing race. Popularizing the *adjudication logic* is open.
- Collision hint: sports VAR replay; a peer-review court.

---

## Concepts that are hardest to make click (ranked by evidence)

| # | Concept | Evidence strength | Key numbers |
|---|---|---|---|
| 1 | **Measurement** (unitary vs. collapse, basis choice, effect on other qubits) | Strongest: QCSE + PER + QCCS + Reddit | 780 Qs tag, 16% unanswered; "measure in another basis" 18.2k views; "unitary… what about measurement?" 41 votes |
| 2 | **Phase and interference** (relative vs. global, kickback, why Grover works) | Strong: PER study + QCSE views | relative/global phase 24.4k views; Grover layman 16.5k; kickback 7.8k; students "do not recognize relative phases have measurable effects" |
| 3 | **Error correction intuition** (syndromes, surface code, decoders, magic states) | Strong and rising (2025–26 news cycle) | 1,253 Qs, 17% unanswered; surface code 25.5k views; magic states 18.2k; 41% of professionals cite a training gap (Riverlane) |
| 4 | **Noise / decoherence / telling signal from noise** | Strong, and the most *timely* (2026 /dev/urandom scandal) | `noise` tag has the highest unanswered rate (28%); HN 383 pts; Gidney: "succeed for the wrong reason" |
| 5 | **Where speedup comes from** ("tries all answers" myth, resource scaling) | Strong among the public | "pie in the sky" 44.5k views (#1 QCSE); factor-21 HN 340 pts / 197 comments |
| 6 | **Entanglement verification** | Medium (high views, crowded) | 42.1k views on "how do I show a state is entangled" |
| 7 | **Rotation gates / Bloch vs. matrix vs. Dirac** | Medium (education papers) | arXiv 2507.09656 flags rotation gates and matrix representation |
| 8 | Qubit ordering (endianness) | High frequency, zero depth | a convention bug, not a concept |

**Pattern across the ranking:** #1, #3 and #4 are the same underlying idea: *you can't look at a quantum state, so how do you know what happened?* Measurement destroys the state, QEC learns about errors without looking at the data, and noise makes output indistinguishable from random. A project that unifies these three ("learning without looking") hits the top three pain points at once.

---

## Top 3 from this front

1. **S-B-1 "Quantum or /dev/urandom?" verifiability.** It is fresh (April 2026, 383-pt HN thread plus a 1 BTC prize scandal), honest, and judge-proof: IonQ engineers will love a tool that *catches* pseudo-quantum, which is exactly what they guard against. It is buildable on the simulator with noise models, and it connects to the Unlocked and Impact themes.
2. **S-B-5 Error-correction intuition (QEC as "learning without looking").** It is the explicitly named Unlocked topic, backed by the 41% training-gap stat. A d=3 code fits in ≤ 17 qubits in one circuit, and decoding is a classical graph puzzle (the captain's ICPC strength). The prior art is either expert tools (Crumble/Stim) or a 2017 non-Qiskit game.
3. **S-B-2 "Why can't it factor 21?": making resource scaling tangible.** It hits the public's #1 confusion (a 340 + 551 pt HN debate). Users build real small Shor circuits and watch cost and noise explode, which gives an honest answer to "when does Q-Day come?" It combines naturally with #1 (show where the "success" really came from).
