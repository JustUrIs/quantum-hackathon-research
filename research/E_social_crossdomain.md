# Front E: Social scanning and cross-domain weak signals

**Method note:** I could not use Claude in Chrome. Two `tabs_context_mcp` calls returned "Browser extension is not connected", so I did not scrape **X, Reddit or LinkedIn**. Reddit also blocks WebFetch. The social signal below comes from **Hacker News** through the public Algolia API (stories since 2025-01-01, sorted by points), plus insider blogs (Aaronson, Filippo Valsorda, Gidney) and their comment threads. The HN data is solid. The X and Reddit "vibe" is **unverified**. If someone reconnects Chrome, a 15-minute X pass on `qLDPC`, `"magic state"` and `"quantumslop"` would be worth doing.

Scan date: 2026-10-10.

---

## Part 1: Social and insider signals

### S-E-1: "quantumslop": a QPU swapped for /dev/urandom gave the same results
- **What:** In April 2026 someone patched a Q-Day Prize-style ECDLP "quantum attack" so that `os.urandom` replaced the IBM backend. Key recovery succeeded at the same rate on curves up to 17 bits, so the QPU added no measurable signal. HN "Replace IBM Quantum back end with /dev/urandom" got 383 points.
- **Source:** https://github.com/yuvadm/quantumslop (URANDOM_DEMO.md); HN 47897647 (2026-04-25); r/crypto mirror https://rl.klein.ruhr/r/crypto/comments/1uqlh93/ . I could not load the repo itself (503); my summary is based on secondary write-ups.
- **Rarity:** 3. Known on HN and in crypto circles, but almost unknown to hackathon teams.
- **Evidence of pain:** 383 points. It ties into a known genre of fake records: Smolin et al., "Pretending to factor large numbers", and the IACR 2025/1237 paper "Replication of quantum factorisation records with an 8-bit home computer" (137 HN points).
- **Quantum hook:** It is the inverse of a hook. It gives us a test for whether quantum is essential in any project: the **"urandom ablation"**. The judges "detect pseudo-quantum instantly", and this is exactly how they would check.
- **Buildability:** High. We can put a toggle in our own demo: "swap the backend for random/classical. Watch it fail."
- **Theme fit:** Unlocked (teach what makes a computation quantum). It also works as meta-validation inside any submission.
- **Prior art:** The repo above. I know of no tool that runs this ablation automatically on arbitrary Qiskit circuits.
- **Collision hint:** Security auditing / fact-checking, a "quantum lie detector", AI-slop detection.

### S-E-2: Q-Day timelines collapsed in Mar–Apr 2026, and crypto engineers now say 2029
- **What:** Google published a lower-cost Shor circuit for ECC-256 (arXiv 2603.28846) and released it as a **zero-knowledge proof that the circuit exists** without revealing the circuit. Caltech/Preskill and Oratomic published qLDPC fault tolerance (arXiv 2603.28627) needing about 10–25k physical neutral-atom qubits. Filippo Valsorda (Go crypto lead) now says "stop deploying non-PQ", and Google and Cloudflare target 2029.
- **Source:** https://scottaaronson.blog/?p=9665 (2026-04-01, HN 265 points); https://words.filippo.io/crqc-timeline/ (2026-04-06, HN 551 points / 248 comments); https://blog.cloudflare.com/post-quantum-roadmap/ (HN 386 points); Let's Encrypt PQ certs (2026-06-03, HN 320 points).
- **Rarity:** 2–3. Insiders know it well; the general public does not.
- **Evidence of pain:** The PQ-migration posts are the most upvoted quantum content on HN in 2025–26. Filippo is categorical: RSA/ECDSA should be "taught as legacy algorithms".
- **Quantum hook:** Real but asymmetric. Shor is the quantum part, and at our scale (≤25 qubits) it is toy-only. Gidney's post explains why even factoring 21 takes about 2,405 entangling gates, roughly 115× more than 15.
- **Buildability:** Med for an honest toy. Low for anything that claims "breaking".
- **Theme fit:** Unlocked (why the clock moved), Impact (migration triage).
- **Prior art:** Many Shor demos, most of them "compiled" fakes; see S-E-3.
- **Collision hint:** ZK proofs, Bitcoin governance (S-E-4), Manhattan-Project secrecy ethics (Aaronson raises the Frisch–Peierls analogy).

### S-E-3: "Why haven't quantum computers factored 21 yet?" (Gidney)
- **What:** Factoring 15 needs about 21 entangling gates, because 15 = 2⁴−1 allows shortcuts. Factoring 21 honestly needs about 2,405, roughly 115× more. Most "factored 21" claims embed the answer in the circuit.
- **Source:** https://algassert.com/post/2500 (2025-08, HN 340 points / 197 comments).
- **Rarity:** 3–4. Most people assume progress is linear in N.
- **Evidence of pain:** High HN engagement; fake factoring records are a recurring embarrassment for the field.
- **Quantum hook:** It is a lesson in honest resource counting.
- **Buildability:** High as a visualization: show the gate count of honest Shor versus the "cheating" circuit as N grows.
- **Theme fit:** Unlocked.
- **Prior art:** The blog post itself. No interactive version that I found.
- **Collision hint:** Data journalism and fact-checking, a "hype-o-meter".

### S-E-4: The Bitcoin "freeze Satoshi's coins" fight (BIP-360/361)
- **What:** BIP-360 (P2MR, a quantum-resistant output) was merged as a draft in Feb 2026. BIP-361 (Lopp et al.) would sunset legacy signatures over 5 years and **freeze** coins that do not migrate, including about 1M BTC attributed to Satoshi and about 5.6M dormant BTC. Adam Back and others oppose a forced freeze. Project Eleven awarded its **1 BTC Q-Day Prize** on 2026-04-24 for a 15-bit ECC key broken on real cloud hardware in about 45 minutes; the previous record was 6 bits.
- **Source:** https://www.coindesk.com/tech/2026/04/16/bitcoin-s-quantum-debate-splits-as-adam-back-pushes-optional-upgrades-over-forced-freeze ; https://blog.projecteleven.com/posts/project-eleven-awards-1-btc-q-day-prize-for-largest-quantum-attack-on-elliptic-curve-cryptography-to-date ; HN "Bitcoin and quantum computing" 170 points.
- **Rarity:** 3.
- **Evidence of pain:** Billions of dollars hang on a governance problem. Sources disagree on the figures (6.5–6.9M vulnerable BTC).
- **Quantum hook:** Shor on toy ECC is honest at small bit-lengths. A 6–8 bit ECDLP could fit on a simulator, but **careful**: S-E-1 shows that small instances can be "solved" by random guessing. Any demo must prove the signal beats random.
- **Buildability:** Med. A toy ECDLP period-finding circuit is a stretch in 20h; a governance/"clock" visualization is easy.
- **Theme fit:** Impact / Unlocked.
- **Prior art:** The Project Eleven entries are all public.
- **Collision hint:** Game theory and mechanism design (who migrates first?), digital inheritance ("dead people's coins").

### S-E-5: Aaronson publicly criticizes IonQ, and our judges are IonQ engineers
- **What:** In his Dec 2025 "imminent" post, Aaronson says 2025 hardware "met or exceeded my expectations" (several platforms are above 99.9% two-qubit fidelity) and that he takes 2028–29 roadmaps more seriously. He also **specifically criticizes IonQ** for misleading governments, for example by suggesting quantum computers "won't hallucinate like AI".
- **Source:** https://scottaaronson.blog/?p=9425 (2025-12, HN 152 points / 125 comments).
- **Rarity:** 3.
- **Evidence of pain:** It is a reputational sore point for IonQ.
- **Quantum hook:** Strategic rather than technical: **IonQ judges will reward projects that are rigorously honest**, with classical baselines and no "AI + quantum = magic" framing. An anti-hype tone is a differentiator here.
- **Buildability:** n/a (meta).
- **Theme fit:** All of them; it is pitch posture.
- **Prior art:** n/a.
- **Collision hint:** Not a domain. It tells us which tone to take in the pitch.

### S-E-6: "Verifiable advantage" is the new standard
- **What:** Google's Quantum Echoes (OTOC on Willow, Nature, Oct 2025) claims about 13,000× over classical with a result that is **verifiable** (repeatable on other QCs) and has a small-molecule NMR "molecular ruler" demo. In Mar 2026 Hangleiter published "Has quantum advantage been achieved?", arguing yes. Separately, certified randomness ran on Quantinuum H2 with JPMorgan (Nature 640, 2025): RCS was turned into **certified random bits** checked by a supercomputer.
- **Source:** https://blog.google/technology/research/quantum-echoes-willow-verifiable-quantum-advantage/ (HN 480 points); https://www.newquantumera.com/podcast/quantum-advantage-achieved-with-dominik-hangleiter/ ; https://www.olcf.ornl.gov/2025/05/05/quantum-computing-experiment-realizes-verifiably-random-number/
- **Rarity:** 3.
- **Evidence of pain:** The debate has moved from "is it fast?" to "can you **prove** it was quantum?"
- **Quantum hook:** It is strong. OTOC/echo (forward evolution, perturb one qubit, reverse) is a **time-reversal interference** effect, which is quantum at its core and fits in a single circuit. That matches the IonQ one-job constraint.
- **Buildability:** High for a small Loschmidt-echo/OTOC on 6–12 qubits in Qiskit. Certified randomness at small scale is pedagogical only, since it is easy to simulate.
- **Theme fit:** Unlocked; Playground (an "echo" instrument or game).
- **Prior art:** Google's papers. I found no consumer-grade interactive OTOC/echo toy.
- **Collision hint:** Music (echo/reverb as literal time reversal), forensics/"undo" mechanics in games, scrambling ↔ information spreading in social networks.

### S-E-7: The QML "dead or narrowing" consensus
- **What:** 2024–2026 papers show that barren-plateau-free variational models tend to be classically simulable (Cerezo et al., Nat. Comms 2025). An ICLR 2025 paper asks whether a model can be both trainable and non-dequantizable. Schuld & Killoran already argued in 2022 that "beating classical ML" is the wrong goal.
- **Source:** https://arxiv.org/abs/2312.09121 ; https://themoonlight.io/review/on-the-relation-between-trainability-and-dequantization-of-variational-quantum-learning-models ; https://arxiv.org/abs/2203.01340 ; HN "Major quantum computing advance made obsolete by teenager" (Tang, resurfaced 2025, 121 points).
- **Rarity:** 3 among practitioners; 5 among hackathon teams, who will keep submitting "QML for X".
- **Evidence of pain:** It is the most common pseudo-quantum pattern judges will see.
- **Quantum hook:** **Anti-hook.** Avoid VQC classifiers unless the dequantization ablation is front and center.
- **Buildability:** n/a.
- **Theme fit:** Unlocked would work as "why your QML is probably classical": a demo that dequantizes a QML model live.
- **Prior art:** Many papers; no playful explainer that I found.
- **Collision hint:** S-E-1 (urandom ablation) and S-E-3 → a "Quantum or Not?" tool.

### S-E-8: Microsoft Majorana credibility crisis
- **What:** Majorana 1 was announced in Feb 2025 (HN 458 points). Data-manipulation allegations followed in May 2025 (HN 218 points). In Jun 2026 a researcher claimed "basic Python errors" invalidate the claim (The Register, HN 186 points).
- **Source:** https://www.science.org/content/article/data-manipulations-alleged-study-paved-way-microsoft-s-quantum-chip ; https://www.theregister.com/research/2026/06/24/boffin-claims-microsofts-supposed-quantum-leap-does-not-compute-due-to-basic-python-errors/5260489
- **Rarity:** 2–3.
- **Evidence of pain:** It is a trust crisis and a reproducibility problem.
- **Quantum hook:** None directly; it is cultural context ("verify everything").
- **Buildability:** n/a.
- **Theme fit:** none.
- **Prior art:** n/a.
- **Collision hint:** Reproducibility tooling, the same thread as S-E-1.

### S-E-9: AI agents now run qubit calibration (OpenAI × MIT EQuS, Sept 2026)
- **What:** GPT-5.6 Sol, working through Codex, controlled lab software and characterized a 6-qubit superconducting chip: it found frequencies, calibrated control and readout, and measured T1/T2. It did well on clean signals and struggled on noisy or ambiguous ones. AI-Mandel (Tübingen/MPL, Nov 2025) generated quantum-optics experiment ideas that led to 2 papers. DeepMind's AlphaQubit (Nature, Nov 2024) is a neural decoder.
- **Source:** https://thequantuminsider.com/2026/09/09/openai-says-ai-agents-may-make-great-quantum-lab-assistants/ (HN 149 points / 108 comments); https://arxiv.org/abs/2511.11752 ; https://arxiv.org/pdf/2512.15736
- **Rarity:** 3–4. It is only a month old.
- **Evidence of pain:** Calibration is the grunt work of quantum labs. The agents fail exactly where signals are noisy.
- **Quantum hook:** Medium. On a simulator we can inject a noise model and let an agent or heuristic "calibrate" it. That is honest, but it mostly tests the classical agent.
- **Buildability:** Med. It needs an LLM API, and only CORS GET requests are allowed, which is likely a blocker.
- **Theme fit:** Unlocked (show the calibration loop).
- **Prior art:** The OpenAI post; k-agents (arXiv 2412.07978).
- **Collision hint:** Automated science, "AI scientist" benchmarks.

### S-E-10: Toolchain gap; IBM supplies more than half of all quantum dev tools
- **What:** A May 2026 FutureCIO piece says quantum has "few toolchains" and that IBM contributes over half of them. MQT Debugger (TUM) appeared in Oct 2025. A 2026 SE workshop (Q-STAV) calls for porting classical SE testing to quantum.
- **Source:** https://futurecio.tech/toolchains-needed-to-fuel-quantum-computing-development-and-future-adoption/ ; https://portal.fis.tum.de/en/projects/design-automation-and-software-tools-for-quantum-computing/ ; https://se2026.inf.unibe.ch/en/workshops/g-stav
- **Rarity:** 3.
- **Evidence of pain:** Moderate. I found no "someone should build X" quotes; X was not accessible.
- **Quantum hook:** Tooling about quantum programs, such as tests for "is this circuit doing anything quantum?" (entanglement/magic witness).
- **Buildability:** High.
- **Theme fit:** Unlocked / Most novel.
- **Prior art:** MQT tools, Qiskit's own debuggers.
- **Collision hint:** S-E-1, a fuzzing/mutation-testing culture.

---

## Part 2: Non-quantum (or adjacent) weak signals for collision

### S-E-11: "Biology might not be quantum, but its math is quantumlike" (Quanta, 2026-09-23)
- **What:** Greg Scholes (Princeton) moved from claiming quantum coherence in photosynthesis to building **classical synchronized-oscillator networks whose emergent states obey qubit math**. He even wired "quantum-like bits" into a modeled logic gate. Wolf Singer (2025) showed that oscillation and phase make neural nets more robust. Karimi (Ottawa) objects that interference is just waves, not quantum. Scholes asks: "Does it matter if you can't tell the difference?"
- **Source:** https://www.quantamagazine.org/biology-might-not-be-quantum-but-its-math-is-quantumlike-20260923/ (HN 123 points, 2026-09-25)
- **Rarity:** **5.** Two weeks old, from a niche workshop.
- **Evidence of pain:** A live foundational dispute. Scholes admits that perfect mimicry needs resources that blow up.
- **Quantum hook:** **The collision itself is the hook.** Put a real qubit circuit next to a classical oscillator network that mimics it, then find where the mimic breaks: entanglement or Bell violation, and exponential resources. That makes "what is quantum, really?" playable. It also ties to the Leggett–Garg / macroscopic-quantum line that the 2025 Nobel honored (S-E-14).
- **Buildability:** High. Use Qiskit for 2–6 qubits, a JS/numpy Kuramoto oscillator for the mimic, and a CHSH test as the referee.
- **Theme fit:** Unlocked (strong), Playground (a "Turing test for quantumness").
- **Prior art:** Scholes's papers (2024). I found no interactive demo. Bell-test games exist, but none frames itself as "biology's fake qubit vs a real qubit".
- **Collision hint:** Neuroscience (phase coding), Turing test, AI "is it conscious?" debates, S-E-1.

### S-E-12: Quantum cognition: question order effects and the QQ equality
- **What:** Wang, Solloway, Shiffrin & Busemeyer (PNAS 2014) analyzed 73 Pew/Gallup polls. Answers shift with question order, yet a **parameter-free quantum-probability prediction** (the QQ equality) holds across almost all of them. In plain terms, people behave as if questions were non-commuting projectors. Skeptics say the data are noisy and contextuality is not established.
- **Source:** https://news.osu.edu/quantum-theory-reveals-puzzling-pattern-in-how-people-respond-to-some-surveys/ ; https://arxiv.org/pdf/1504.07422 (critique). This is older research; I found no 2025-specific paper.
- **Rarity:** 4–5 outside cognitive science.
- **Evidence of pain:** Pollsters and UX researchers do fight order bias, but they do not use this model.
- **Quantum hook:** **Honest only if framed as "quantum math, classical people".** Qiskit can encode a belief state as a qubit and questions as measurement bases; sequential measurements give order effects natively, and a single IonQ job can contain the whole questionnaire. The risk is that a judge says "that's just linear algebra". The defense is the S-E-11 framing.
- **Buildability:** High (1–3 qubits).
- **Theme fit:** Playground (a game where the **order in which you ask** changes what is true), Unlocked (non-commuting measurement).
- **Prior art:** Busemeyer & Bruza's book. I found no game.
- **Collision hint:** Elections, Argentina's polling culture, interrogation/detective games, dating apps.

### S-E-13: The photosynthesis-coherence story was retracted in practice
- **What:** The 2007 "long-lived quantum coherence" beats in FMO are now attributed mainly to vibronic or vibrational coherence; electronic coherence is too short-lived to matter. Engel's group finds that redox state steers transfer paths through vibronic resonance.
- **Source:** https://par.nsf.gov/search/author:%22Engel,%20Gregory%20S%22 ; Quanta piece in S-E-11. Exact 2024–25 dates are unverified.
- **Rarity:** 3–4. The public still believes the 2007 story.
- **Evidence of pain:** Pop-science myth versus the current consensus.
- **Quantum hook:** Small open-system exciton transport (a 7-site FMO toy) **can** be simulated with Qiskit Trotter steps plus noise. Showing "coherence helps, then decoherence helps more" (environment-assisted transport, ENAQT) is real physics.
- **Buildability:** Med. Seven sites map to 3 qubits (binary encoding) or 7 (one-hot); adding a noise model is fiddly.
- **Theme fit:** Unlocked / Playground.
- **Prior art:** Many papers; no interactive game.
- **Collision hint:** Solar energy, "noise as a feature" (also in music).

### S-E-14: 2025 Physics Nobel for macroscopic quantum tunnelling in circuits (Clarke, Devoret, Martinis)
- **What:** Their 1980s experiments showed that a superconducting circuit (billions of electrons) tunnels and has quantized energy levels like a single atom. This is the ancestor of today's superconducting qubits; Devoret is at Google and Martinis is at Qolab.
- **Source:** https://www.nobelprize.org/prizes/physics/2025/summary/ ; https://physicsworld.com/a/john-clarke-michel-devoret-and-john-martinis-win-the-2025-nobel-prize-for-physics/
- **Rarity:** 2. It is famous, but the concept of a macroscopic object tunneling is not widely understood.
- **Evidence of pain:** Educational. The anniversary is this week (Oct 7).
- **Quantum hook:** Tunneling through a barrier can be simulated as a discretized particle on 4–6 qubits with Trotterized evolution, so a 1D wavepacket visibly tunnels.
- **Buildability:** High. Qiskit time evolution on 5 qubits gives 32 grid points.
- **Theme fit:** Unlocked / Playground (a "tunnel through the wall" game mechanic).
- **Prior art:** Many 1D Schrödinger visualizers (classical); fewer that run the evolution as a qubit circuit.
- **Collision hint:** Enzyme tunneling (S-E-15), games ("walk through walls" with probability).

### S-E-15: Proton tunnelling as a mutation source (DNA) and in enzyme catalysis
- **What:** Surrey (Slocombe, Al-Khalili et al., 2022) modeled G–C base-pair proton tunnelling; the tunnelling contribution was "orders of magnitude" above classical hopping, and tautomers may survive helicase. A 2026 review proposes proton delocalization rather than pure tunnelling. Enzyme H-tunnelling (Klinman) is well established through kinetic isotope effects.
- **Source:** https://surrey.ac.uk/news/new-study-reveals-quantum-physics-can-cause-mutations-our-dna ; https://arxiv.org/pdf/2605.00205 (2026 review); https://journal.hep.com.cn/ctm/EN/10.1002/ctm2.70694
- **Rarity:** 4.
- **Evidence of pain:** Spontaneous mutations matter in cancer and aging. The claim is still mostly theoretical.
- **Quantum hook:** A double-well proton is natively a 2-level system (left/right ↔ |0⟩/|1⟩); tunnel splitting is a single-qubit rotation. That is honest and tiny. Isotope effects can be shown by changing the mass, which changes the tunnelling rate.
- **Buildability:** High as an Unlocked demo; the Impact value is speculative.
- **Theme fit:** Unlocked.
- **Prior art:** Academic only.
- **Collision hint:** Evolution and art ("mutations from tunnelling" as a generative-art engine), Hopfield memory (stored patterns being corrupted).

### S-E-16: Avian compass: a radical-pair spin qubit inside a bird's eye
- **What:** The cryptochrome radical-pair mechanism is the leading model. A Nov 2025 JACS paper (Hammes-Schiffer, Subotnik, Solov'yov) computationally identified the electron-transfer pathway and the protein stabilization of radical pairs in Cry4a. MHz RF fields disrupt orientation in every bird species tested.
- **Source:** https://chemistry.princeton.edu/news/hammes-schiffer-subotnik-provide-computational-proof-of-radical-pair-theory-on-bird-migration ; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4892254/
- **Rarity:** 4.
- **Evidence of pain:** Science only. There is a conservation angle (RF and urban noise affecting migration) that I have not verified.
- **Quantum hook:** **Strong and honest.** The radical pair is literally two electron spins (2 qubits plus a nuclear spin or two) evolving singlet↔triplet under the Earth's field angle. The singlet yield versus field angle **is** the compass. A real Qiskit simulation of a 3–4 qubit Hamiltonian, sweeping the angle, would produce a "compass needle" from quantum dynamics.
- **Buildability:** High. 3–5 qubits with Trotterized Zeeman plus hyperfine terms; the one-job IonQ constraint fits if we batch angles in parallel registers.
- **Theme fit:** Playground (fly a bird by its quantum compass; RF jamming breaks it), Unlocked (decoherence and coherence time matter).
- **Prior art:** Academic simulations (Hore, Solov'yov). I found no game or browser demo; worth a deeper check.
- **Collision hint:** Navigation in GPS-denied settings (S-E-17), migration games, climate.

### S-E-17: Quantum sensing is shipping (NV-diamond magnetic navigation)
- **What:** NV-diamond magnetometers are reaching pilots and field use for GPS-denied navigation: the Leidos/Frequency Electronics subcontract (Mar 2025), the DARPA Robust Quantum Sensors program, SBQuantum MagQuest payloads launched in Mar 2026 (company claim), and Dirac Labs' $1.8M pre-seed. I found no revenue comparison with computing.
- **Source:** https://www.gpsworld.com/quantum-magnetometer-could-solve-gnss-denied-navigation-problems/ ; https://quantumcomputingreport.com/dirac-labs-raises-1-8m-pre-seed-round-to-scale-diamond-based-quantum-navigation-sensors/
- **Rarity:** 3.
- **Evidence of pain:** GPS jamming is now routine (Ukraine, Baltic). Contrarian take: **sensing is useful today and computing is not.**
- **Quantum hook:** Ramsey interferometry or phase estimation on a simulated NV spin: a 1–3 qubit circuit gives field → phase → measurement; entangled (GHZ) probes reach Heisenberg scaling, a **provable** quantum advantage in precision at small N.
- **Buildability:** High. GHZ-based metrology versus classical shot-noise, with a plot of 1/N versus 1/√N scaling, is honest and fits the ≤25-qubit, one-job constraints.
- **Theme fit:** Impact (navigation without GPS), Unlocked (Heisenberg limit).
- **Prior art:** Qiskit textbook covers phase estimation; GHZ metrology tutorials exist. **Combined with the bird compass (S-E-16), I found no prior art.**
- **Collision hint:** Birds (S-E-16), Argentina/Antarctica navigation, Falklands/South Atlantic magnetic anomaly (SAA, unverified idea).

### S-E-18: 2025 Chemistry Nobel for MOFs, plus FeMoco resource estimates falling
- **What:** Kitagawa, Robson and Yaghi won for metal-organic frameworks (CO₂ capture, water harvesting from desert air). Separately, FeMoco (nitrogen fixation) estimates dropped from about 4M physical qubits (2021) to about 99k (Alice & Bob cat qubits), with 2025 algorithmic speedups of 4–195×. Ammonia accounts for roughly 1–4% of global energy (sources disagree).
- **Source:** https://www.kva.se/nobelchemistry2025 ; https://thequantuminsider.com/?p=2381556 ; https://postquantum.com/quantum-computing/quantum-chemistry-drug-discovery-catalysis/
- **Rarity:** 2 for MOFs; 4 for the FeMoco estimate trajectory.
- **Evidence of pain:** Climate and food. At hackathon scale, though, chemistry is H₂/LiH-sized, which judges have seen 1,000 times.
- **Quantum hook:** VQE on toy molecules is honest but saturated; a classical exact baseline always wins.
- **Buildability:** High technically, low on novelty.
- **Theme fit:** Impact (weak), Unlocked ("the FeMoco clock": why 2,000 logical qubits are needed).
- **Prior art:** Saturated.
- **Collision hint:** The Atacama/lithium/desert water-harvesting angle for LatAm.

### S-E-19: 2025 Turing Award for Bennett and Brassard (BB84, teleportation, distillation)
- **What:** Announced on 2026-03-18. The award recognizes BB84, teleportation (1993) and entanglement distillation (1996).
- **Source:** https://awards.acm.org/about/2025-turing ; https://physicsworld.com/a/quantum-physicists-charles-bennett-and-gilles-brassard-win-1m-turing-award/
- **Rarity:** 2.
- **Evidence of pain:** Educational timeliness.
- **Quantum hook:** Entanglement distillation is under-taught and fits in one circuit (2 noisy Bell pairs → 1 better pair, with postselection).
- **Buildability:** High.
- **Theme fit:** Unlocked (networking).
- **Prior art:** BB84 demos are saturated; distillation demos are rare.
- **Collision hint:** "Trust" across networks, Signal's post-quantum ratchet (HN 637 points, the top quantum HN post).

### S-E-20: Quantum music and games are mostly metaphor; the gap is "essential" mechanics
- **What:** Miranda's *Advances in Quantum Computer Music* (World Scientific, 2025) covers sonifying VQAs and quantum reservoir AI. Moth's *Quantum Backrooms* (alpha) generates levels on IBM/IQM hardware. *Quantum Odyssey* and *The Qubit Factory* (Steam, Jul 2025) are circuit puzzlers. The typical failure is that quantum is used only as an RNG.
- **Source:** https://worldscientific.com/worldscibooks/10.1142/14025 ; https://forklog.com/en/london-startup-moth-unveils-first-quantum-computer-game/ ; https://store.steampowered.com/app/3121980/The_Qubit_Factory
- **Rarity:** 3.
- **Evidence of pain:** Judges explicitly penalize "just randomness" (brief).
- **Quantum hook:** Mechanics have to rest on interference, non-commutation or entanglement correlations: echo (S-E-6), order effects (S-E-12) or compass (S-E-16), not dice.
- **Buildability:** High.
- **Theme fit:** Playground.
- **Prior art:** As listed. Puzzle games are saturated.
- **Collision hint:** S-E-12, S-E-6.

### S-E-21: Argentina's quantum ecosystem is small but organizing (2026 national initiative letter)
- **What:** A March 2026 letter of intent (UNAHUR) for a national quantum initiative counts about 30 research groups. CNEA is building a 4–8 fluxonium-qubit processor, "the first Argentine quantum processor in the cloud". UNAHUR has a 3-qubit SpinQ NMR teaching machine shared across UBA/UNLP/UNC/UNSAM. CITEDEF works on QRNG and QKD. Buenos Aires hosted the Quantum Foundations conference in Nov 2025.
- **Source:** https://unahur.edu.ar/wp-content/uploads/2026/03/Declaracion-de-Intencion-para-la-promocion-y-desarrollo-de-una-iniciativa-cuantica.pdf ; https://www.argentina.gob.ar/noticias/tecnologias-cuanticas-tres-proyectos-de-la-cnea-obtuvieron-financiamiento-para-fortalecer ; https://www.ellitoral.com/educacion/computadora-cuantica-universidad-hurlingham_0_BsHtF1s4bG.html
- **Rarity:** 5 outside Argentina.
- **Evidence of pain:** The country is "late to the field" (Díaz-Caro), so education capacity is the bottleneck.
- **Quantum hook:** None directly. It provides a storytelling and impact frame (a Spanish-first Unlocked tool for 30 groups and their students).
- **Buildability:** n/a.
- **Theme fit:** Unlocked (as a narrative).
- **Prior art:** n/a.
- **Collision hint:** Education in Spanish; any Unlocked demo shipped bilingual.

---

## Raw collisions ("si pasa X, entonces Y" / "¿qué pasaría si combinamos A y B?")

1. **Quantumslop × every hackathon project:** ¿Qué pasaría si cada demo tuviera un botón "reemplazá el QPU por /dev/urandom" y mostrara en vivo que el resultado se rompe? An **ablation-first** design: the project proves its own quantumness. Judges hunting for pseudo-quantum would get the test handed to them.
2. **Scholes' fake qubits × CHSH referee:** Si la biología fabrica "qubits clásicos" con osciladores, ¿dónde exactamente se rompe la imitación? A playable **Turing test for quantumness**: an oscillator network against a real circuit, with a Bell test as judge.
3. **Bird compass × GPS jamming:** Si los pájaros navegan con un qubit de par radical y los drones pierden GPS en Ucrania, ¿un juego donde volás guiado por el rendimiento singlete y te "jamean" con RF? Real spin dynamics, a real failure mode, and current news.
4. **Bird compass × Heisenberg metrology:** ¿Qué pasaría si mostramos que un pájaro usa 2 spins y un sensor NV con GHZ usa N entrelazados, y la curva 1/N vs 1/√N es la ventaja cuántica más honesta que existe hoy? Sensing as the contrarian "real" advantage.
5. **Quantum cognition × elections or interrogation:** Si el orden de las preguntas cambia la respuesta y obedece la igualdad QQ, ¿un detective game donde el orden en que interrogás define la verdad? Non-commuting measurement as the core mechanic. It needs a strong honesty framing.
6. **Quantum Echoes (OTOC) × music or undo:** Si el eco cuántico revierte el tiempo y sólo funciona por interferencia, ¿un instrumento donde perturbar un qubit "rompe" el eco y suena distinto? Scrambling made audible, with a time-reversal mechanic.
7. **Q-Day collapse × Satoshi's frozen coins:** Si el reloj es 2029 y 6.7M BTC están expuestos, ¿un simulador del "reloj de migración" que combine estimaciones de recursos (Gidney → Oratomic) con un toy ECDLP **validado contra random**?
8. **Gidney's "21 is 115× harder than 15" × fake records:** ¿Un "hype-o-meter" que compila Shor honesto vs Shor con la respuesta adentro y muestra el contador de compuertas? Unlocked, anti-hype, aimed at the IonQ judges (S-E-5).
9. **Proton tunnelling × generative art:** Si las mutaciones del ADN vienen en parte de un túnel en un doble pozo (un qubit), ¿arte generativo donde cada "error" de un patrón es un tunneling real con efecto isotópico (cambiar H por D lo frena)?
10. **AI agents calibrating qubits × noise:** Si los agentes fallan justo cuando la señal es ruidosa, ¿un juego "sos el agente de calibración" sobre un simulador con ruido, donde humanos vs heurística compiten? (Weak: the quantum part is mostly backdrop.)

---

## Top 3 from this front

1. **Bird compass × GPS-denied quantum navigation (S-E-16 + S-E-17, collisions 3 and 4).** It is a genuine few-qubit quantum dynamics simulation, where the compass output *is* the singlet-yield interference. It has an honest metrology-advantage angle (Heisenberg vs shot noise), a ready-made game or story, rarity 4, and I found no browser prior art.
2. **"Quantum or Not?": urandom ablation plus Scholes' classical mimic plus a CHSH referee (S-E-1 + S-E-11 + S-E-7, collisions 1 and 2).** It turns the judges' own pseudo-quantum suspicion into the product. The Quanta piece is two weeks old (rarity 5). It is small-qubit and very buildable, and it lands with an audience made wary by IonQ's hype criticism.
3. **Order-effects interrogation game (S-E-12 + S-E-20, collision 5).** Non-commuting measurement is the mechanic itself, not dice; the whole questionnaire fits in one IonQ job; rarity 4–5. The risk is the "it's just linear algebra" critique, so frame it as quantum math applied to people and pair it with #2's honesty.

Unverified or missed: everything on X, Reddit and LinkedIn (Chrome was disconnected); the quantumslop repo contents (503); the Oxford "gravity in the quantum world" paper (403); the Atacama "quantum crystals" post (403).
