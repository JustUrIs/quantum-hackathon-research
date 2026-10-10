# Front D: Saturation map (what's already done, what judges reward)

Scanned 2026-10-10 ~00:30 ART. Sources: the Qollab CMS API (`api.cms.qollab.xyz/items/articles`, which is public and the richest source), Qollab sitemaps, IonQ newsroom/blog, iQuHACK coverage, itch.io jams, and GitHub search (repo counts from 2026-10-10; the counts are noisy proxies, see the caveats). Live competitor repos from this hackathon were found on GitHub.

---

## Signal cards

### S-D-1: Qollab already has 13 funded "creative quantum" projects, and they cover most obvious ideas
- What: The Spring 2026 Creative Challenge cohort (13 teams, real IonQ hardware) plus the Winter 2025 winners. Each is listed with the territory it already occupies:
  - **Quantum Garden**: generative plants, "entangled" plants, real measurement outcomes.
  - **QAVE**: gate-by-gate state/density-matrix visualizer. It is preinstalled as a library on Qollab.
  - **Qatalyst Game**: race IonQ at vehicle routing with QAOA.
  - **qOrbital**: VQE molecular orbitals, Copenhagen cloud vs Bohmian trajectories, "hardware noise as the exhibit".
  - **Superposition Sequencer**: circuit as an instrument, MIDI.
  - **Quantum Butterfly Field**: scrambling and the no-butterfly effect as art.
  - **GraFT**: 3D graph of fault-tolerant compilation, magic-state distillation and syndrome extraction.
  - **QuantumRegimeRadar**: quantum kernels vs GARCH for market regimes.
  - **Musiq**: quantum-walk melody plus entangled voices.
  - **Quantum Patterns**: PQCA live-coding music. PQCA is preinstalled on Qollab.
  - **Quantum Market Game**: quantum prisoner's dilemma as a trading game.
  - **QuantumCanvas**: drag-and-drop circuit sandbox.
  - **QCFlows**: circuit as a dynamic correlation graph, basis-dependent views.
  - **Entangled Body**: point-cloud body with "non-local" touch.
  - **Quantum Systemic Oracle**: QAOA risk score published on-chain.
  - Explore pages also feature **Quantum Courier** ("races classical vs quantum solvers across five logistics problems, shows honestly which wins") and **Quantum Advantage Lab** (four algorithms beside their classical counterparts, streamed step by step).
  - The Qollab example **Quantum Hackathon Soundtrack** is a music piece.
  - Also on Qollab: QuantumBlur (images), Quantum Audio package, Quantum Error Choir (QEC as an audience choir), Bloch Sphere Visualizer, Teleportation Disk, Space Moths (QML Roblox levels), MWPF decoder demo.
- Source: https://api.cms.qollab.xyz/items/articles?filter[slug][_eq]=spring-2026-cohort (dated 2026-05-01, updated 2026-05-08); https://qollab.xyz/explore/* meta descriptions; https://qollab.xyz/sitemap.xml
- Rarity: 4. Few participants will check this before building.
- Evidence of real pain: the judges' own platform is the prior art. A project that duplicates a featured Qollab project will look derivative to judges who curate that gallery.
- Quantum hook: n/a (map of what's taken).
- Buildability: n/a.
- Theme fit: all.
- Prior art: this card is the prior art.
- Collision hint: we must be orthogonal to all of these. Note the gaps: no sensing, no networking/QKD game, no Bell/nonlocal game, no "trapped-ion hardware-native" piece, and no honest Impact entry outside finance and logistics.

### S-D-2: Qollab's editors write down their own scoring taste: honest over hype, essential over decorative
- What: The cohort write-up praises these, verbatim:
  - "grounded in empirical backtesting rather than the usual quantum-finance hype"
  - "shows where quantum kernels help and where they do not"
  - "shows honestly which wins and why" (Quantum Courier)
  - "Quantum-conceptual framing here is honest rather than hyped, which is rarer than it should be"
  - "PQCA outputs are genuinely quantum rather than mapped randomness, which differentiates this from the noise-as-music genre"
  - "Instead of an algorithm with random numbers, it is a real quantum computation"
  - "the case for why a simulator falls short here is clear"

  The Creative Challenge rubric also gives "Quirky and playful work earns bonus points" and asks to "Encourage others to learn from or remix the work".
- Source: spring-2026-cohort article (above); https://qollab.xyz/creativechallenge (fetched 2026-10-10)
- Rarity: 4.
- Evidence: explicit editorial language from the organizers who also run this hackathon.
- Quantum hook: this is the judging filter. Randomness-as-content scores low. A stated negative result ("quantum doesn't win here, and here's why") is rewarded, not punished.
- Buildability: n/a.
- Theme fit: all, and especially Impact. An honest baseline comparison is the expected genre.
- Prior art: n/a.
- Collision hint: build the "honest benchmark" into the core UX. Show the regime where quantum loses as well as where it wins.

### S-D-3: The hackathon terms include a "novelty floor": tutorial-level work can score 0
- What: Per the terms, a project must go beyond a reference or tutorial implementation with at least one of:
  - a novel application context
  - a technical extension (noise mitigation, parameter optimisation, comparative benchmarking)
  - an original analytical or educational contribution

  If it doesn't, panels may score 0 on novelty and technical execution. Other terms:
  - Judges run every project on the free local simulator, and IonQ simulator results "neither add nor subtract points". The project must still fit one IonQ job per run.
  - UI accessibility best practices are required.
  - "This effort is supported by Qollab & IonQ" is mandatory.
  - Prior code must be disclosed.
- Source: https://qollab.xyz/programs/hackathon/terms, summarized second-hand in competitor notes at https://github.com/udsy19/Qollab-Hackathon (vault/Research/qollab-platform-and-submission.md, read 2026-10-09). I could not fetch the SPA directly. **Partly unverified.**
- Rarity: 3.
- Evidence: the explicit rule text (quoted second-hand).
- Quantum hook: Teleportation, BB84, Grover and Bell-pair demos fail by default unless reframed.
- Buildability: n/a.
- Theme fit: all.
- Prior art: Qollab's own "Quantum Teleportation" example is cited as failing the floor.
- Collision hint: state which novelty category we claim, in a heading on the project page.

### S-D-4: Live competitors right now. Networking and repeaters are already being built by at least 2 teams
- What: GitHub repos created 2026-10-07 to 10-10 for this hackathon:
  - **Entangle the Andes** (AGONIXX15): build Colombia's quantum internet. Bell pairs, Werner states, DEJMPS purification, swapping, CHSH, E91/BBM92, three.js.
  - **Cartheon** (SagarPatange): EnergyGridOptimization, FreightDecisionIntelligence, QuantumRepeaters_QKD.
  - **Collapse** (Pizzylee001): noir detective game; clues are qubits, choose an X/Y/Z basis, six measurements.
  - **Quantum Music** (DianaDancea): Mach-Zehnder overtone synth with a quantum-eraser crossfader.
  - **Almond**: Grover vs classical benchmark explorer, which openly says it's a model and not empirical.
  - **grigorovich-sergey**: quantum road-closure map with OSM network, critical sets and geojson. Likely Impact / graph optimization.
  - **Quack** (JhoanMoscoso): a videogame.
  - **udsy19**: three entries, one per track, with a sophisticated docs process.

  That is about 8 visible out of likely hundreds (21 nodes in 10 countries).
- Source: `gh search repos qollab`, 2026-10-10; READMEs.
- Rarity: 5. Nobody else is looking at this.
- Evidence: actual repos.
- Quantum hook: n/a.
- Buildability: n/a.
- Theme fit: shows Unlocked plus networking is getting crowded, Playground has detective and music entries, and Impact has logistics, energy and roads.
- Prior art: the repos above.
- Collision hint: if we do networking, it must differ sharply from "build a repeater chain + purify + QKD". That combination is now the default "IonQ-flattering" idea.

### S-D-5: IonQ's own hackathon challenge in 2026 was entanglement distillation on a network graph
- What: At iQuHACK 2026 (Jan 30 to Feb 1), IonQ's challenge was a "gamified entanglement distillation challenge set across a quantum network graph": maximize utility qubits under a limited budget of entanglement links.
  - 1st place: UAM Madrid with BBPSSW + DEJMPS.
  - 2nd place: iQuackers (MIT) with adaptive real-time protocol selection.
  - In 2025, IonQ's challenge was combinatorial optimization: beat IonQ's own MaxCut benchmarks, with a three-tier problem whose final tier was an open IonQ research question.
  - 2022 winner: Opti-Maze.
- Source: https://thetech.com/2026/02/19/iquhack-2026 ; https://qbraid.com/blog-posts/qbraid-iquhack-2026 ; https://www.uam.es/eps/escuela/noticias/estudiantes-eps-ganan-iquhack2026 ; https://www.a-star.edu.sg/qinc/_features/features/a-star-q.inc-wins-at-mit-iquhack-2025 ; https://www.ionq.com/blog/february-09-2022-iquhack-winners-opti-maze
- Rarity: 3.
- Evidence: IonQ engineers chose this topic themselves, so it is a strong preference signal.
- Quantum hook: purification only works through genuinely quantum operations (bilateral CNOTs plus post-selection).
- Buildability: high. Each purification round uses 4 qubits and fits easily.
- Theme fit: Unlocked (networking), Playground (game).
- Prior art: iQuHACK 2026 winners, plus Entangle the Andes and Cartheon in this hackathon. Saturating fast.
- Collision hint: IonQ judges value it, so a twist on "the budget of entanglement" could still win, but it needs a meaning change (see Gaps).

### S-D-6: IonQ's 2025–26 strategy has five legs, and only compute is represented in hackathon culture
- What: IonQ is assembling a full-stack "quantum platform":
  - **Compute**: Forte/Tempo, #AQ 64 (Sep 2025), 99.99% two-qubit fidelity via Oxford Ionics' Electronic Qubit Control; targets of 256 qubits in 2026 and 2M physical / 80k logical by 2030.
  - **Networking**: Lightsynq (photonic interconnect plus quantum memory). Apr 2026: first photonic interconnect of two commercial trapped-ion systems (AFRL); also the DARPA HARQ program.
  - **Security**: ID Quantique controlling stake (QKD, QRNG, single-photon detectors).
  - **Space**: Capella SAR satellites for space QKD and Earth observation; Skyloom optical comms; $39M SDA HALO contract.
  - **Sensing**: Vector Atomic (PNT: clocks, gravimeters, >$200M in government contracts).
  - **Manufacturing**: SkyWater foundry, $1.8B, announced Jan 2026.
- Source: https://quantumcomputingreport.com/ionq-announces-regulatory-approval-for-oxford-ionics-acquisition-and-provides-a-roadmap-update-at-its-2025-analyst-day-meeting/ ; https://ionq.com/blog/ionq-hits-aq-64-milestone-ahead-of-schedule-and-sets-its-sights-even-higher ; https://ionq.com/news/ionq-achieves-key-photonic-interconnect-milestone-demonstrating-networked-quantum-systems-using-entanglement ; https://www.verdict.co.uk/ionq-acquisition-skywater-technology/ ; https://convergedigest.com/ionq-to-demo-quantum-secure-orbital-communications-adds-quantum-sensing/
- Rarity: 2 for the acquisitions, 4 for the implication that **sensing / PNT / clocks is IonQ's newest business line and has zero creative hackathon projects**.
- Evidence: billions in M&A.
- Quantum hook: GHZ-state phase estimation, Heisenberg-limited sensing and entangled clocks are all circuit-expressible in Qiskit on ≤20 qubits.
- Buildability: high for GHZ metrology toy demos.
- Theme fit: Impact (navigation without GPS: spoofing and jamming are a real 2024–26 pain), Unlocked (why entanglement beats √N), Playground.
- Prior art: GitHub has "GHZ metrology" 0, "quantum sensing game" 0, "quantum sensing qiskit" 10 repos.
- Collision hint: GPS jamming over conflict zones crossed with entangled sensors. Or space plus sensing (the Capella story).

### S-D-7: The trapped-ion hardware story (all-to-all connectivity) is IonQ's main differentiator, and almost nobody visualizes it
- What: IonQ's marketing repeatedly cites "single ion chain with all-to-all connectivity" as the reason for #AQ 64 and for benchmark wins vs IBM (+35% QAOA, +74% QFT, +182% FAA, IonQ's own numbers). Superconducting devices need SWAP routing. QAVE's author explicitly wished for "a visual explorer comparing how the same logical circuit is realized on superconducting, trapped-ion, and neutral-atom platforms" and listed it as an open idea for others.
- Source: https://ionq.com/blog/ionq-hits-aq-64-milestone-ahead-of-schedule-and-sets-its-sights-even-higher ; https://api.cms.qollab.xyz/items/articles?filter[slug][_eq]=project-showcase-qave
- Rarity: 4.
- Evidence: an explicit wish from a Qollab winner. Qollab offers 8 IBM noise-model fake backends (heavy-hex) and IonQ noise sims in the same dialog, so a same-circuit comparison is directly buildable.
- Quantum hook: transpile the same circuit to IBM coupling maps vs IonQ all-to-all, then measure the SWAP count, depth and fidelity on the noise models. That is real and measurable.
- Buildability: high (Qiskit transpiler plus fake backends are in-browser).
- Theme fit: Unlocked (strong), Impact (weak).
- Prior art: GitHub has "qubit routing visualization" 1 and "all-to-all connectivity" 2. IonQ benchmark pages exist.
- Collision hint: risk of looking like an IonQ ad. Frame it as "why connectivity is destiny" or a routing puzzle game (ICPC-flavoured: you are the transpiler).

### S-D-8: Quantum music and sound is the most saturated Playground sub-genre on Qollab specifically
- What: Qollab hosts Superposition Sequencer, Musiq, Quantum Patterns, Quantum Hackathon Soundtrack (the official example), Quantum Sound, Quantum Audio and Quantum Error Choir. That is 7 music/sound items, with at least 1 more competitor in this hackathon (Mach-Zehnder synth). Editors already call out the "noise-as-music genre" as a negative. GitHub "quantum music" has 190 repos. Academic ICCMR (Miranda) has done this for 10 years.
- Source: S-D-1 sources; GitHub search 2026-10-10.
- Rarity: 1.
- Evidence: n/a.
- Quantum hook: rarely essential.
- Buildability: high, which is exactly why it's crowded.
- Theme fit: Playground.
- Prior art: overwhelming.
- Collision hint: avoid, unless sound is only the output channel of something else (e.g. the sonified syndrome of a decoder).

### S-D-9: Visualizers (Bloch sphere, state evolution, circuit graph) are fully taken on Qollab
- What: These already exist on the judges' platform: Bloch Sphere Visualizer (Qollab project), QAVE (state/density matrix, preinstalled), QCFlows (correlation graph, basis views), GraFT (FT compilation), QuantumCanvas (drag-and-drop sandbox), Quantum Advantage Lab (algorithm vs classical, step by step) and the Teleportation Disk. GitHub has "bloch sphere visualizer" 232.
- Source: sitemap and CMS above.
- Rarity: 1.
- Evidence: n/a.
- Quantum hook: decorative unless tied to a task.
- Buildability: high.
- Theme fit: Unlocked.
- Prior art: as listed.
- Collision hint: Unlocked must teach one specific, timely concept via a task the user performs, not a generic viewer.

### S-D-10: Game jams show what "quantum game" means to the crowd: measurement-collapse puzzles, mazes, Schrödinger's cat
- What:
  - The Global Quantum Game Jam 2025 had 17 entries: "Echo" titles ×5, Quantum Maze, Laser Maze, Moth Effect (Decodoku, a QEC game by James Wootton's group), Recoherence Realm.
  - The Quantum Arcade Jam 2025 (grades 6–12, 22 entries) had Quantum Snake, Tetris, Ninja, Schrödinger's Cat ×3, Mine game.
  - GitHub counts: quantum tic-tac-toe 244, chess 226, maze 122, dice 139, coin flip 92, sudoku 81, battleship 61, minesweeper 38, pong 39, card game 24, poker 21, rock-paper-scissors 17, blackjack 15, wordle 15.
- Source: https://itch.io/jam/quantum-game-jam-2025/entries ; https://itch.io/jam/quantum-arcade-game-jam ; GitHub search 2026-10-10.
- Rarity: 1.
- Evidence: n/a.
- Quantum hook: mostly "superposition = random choice", which fails Playground's rule that random output alone does not qualify.
- Buildability: high.
- Theme fit: Playground.
- Prior art: overwhelming. In this hackathon, Collapse (basis-measurement detective) already takes the "choose your measurement basis" mechanic.
- Collision hint: the game rules must be impossible to win classically, as in nonlocal games (see Gaps).

### S-D-11: Impact-track finance and logistics are saturated, even on Qollab
- What:
  - GitHub counts: quantum portfolio optimization 404, QAOA portfolio 141, fraud detection 235, image classification 255, MaxCut QAOA 169, supply chain 94, TSP 71, VRP 70, energy grid 37.
  - On Qollab: Qatalyst (VRP), Quantum Courier (5 logistics problems), RegimeRadar (finance kernels), Systemic Oracle (QAOA risk), Market Game.
  - In this hackathon: Cartheon (energy grid, freight) and the road-closure map.
  - Qollab says its "Fall RFP cycle shifts toward applied domains in optimization and logistics", so expect a flood.
- Source: as above.
- Rarity: 1.
- Evidence: n/a.
- Quantum hook: at ≤25 qubits QAOA almost never beats a strong classical baseline. Honest teams will show "classical wins", which is acceptable per S-D-2 but not distinctive.
- Buildability: high.
- Theme fit: Impact.
- Prior art: as listed.
- Collision hint: for Impact, pick a domain where the quantum subroutine is native, not a QUBO wrapper. That means sensing/metrology, quantum data (certifying a QRNG or a quantum channel), or simulation of a small physical system where the classical baseline is exact and comparable.

### S-D-12: QEC as a human-scale experience exists as art, but nobody has made an interactive QEC game that runs real syndrome circuits
- What:
  - Quantum Error Choir (Stewart Smith, Yale; QEC as a smartphone lattice) and Beneath the Green (Yale QEC installation) are art installations, not playable code.
  - Decodoku / Moth Effect are puzzle games with classical decoding, no circuits.
  - GraFT visualizes FT compilation overhead.
  - MWPF has a decoder demo.
  - GitHub: "quantum error correction game" 9, "qec decoder game" 0, "surface code game" 54 (many are simulators).
  - QuEra's iQuHACK 2026 challenge was QEC, so judges see QEC as timely.
- Source: CMS articles quantum-error-choir and beneath-the-green-the-quantum; https://thetech.com/2026/02/19/iquhack-2026 ; GitHub 2026-10-10.
- Rarity: 3.
- Evidence: the Unlocked theme names error correction first.
- Quantum hook: syndrome extraction must be a real circuit (ancillas, mid-circuit logic). A repetition code or a [[4,2,2]] / [[5,1,3]] / Steane code is ≤ about 20 qubits.
- Buildability: medium-high. One IonQ job is a constraint, so pack the shots in one circuit.
- Theme fit: Unlocked (strong), Playground.
- Prior art: expect several Unlocked entries doing "repetition code explainer". It's the default Unlocked idea, so a distinctive mechanic is needed.
- Collision hint: the player is the decoder, racing the noise. Sound or choir is the output channel. Or cross QEC with trapped-ion 99.99% fidelity ("why IonQ needs fewer physical qubits per logical").

### S-D-13: Nonlocal games (CHSH, Mermin–Peres magic square, GHZ pseudo-telepathy) are a near-empty Playground niche where quantum is mathematically essential
- What:
  - Win probability caps are provable: CHSH is 75% classical vs about 85.4% quantum, and the Mermin–Peres magic square and GHZ game are winnable 100% with entanglement vs ≤ 8/9 or 3/4 classically.
  - This is the cleanest possible proof that "quantum is essential, not randomness", which is exactly the Playground rule.
  - GitHub: "CHSH game" 46 (mostly textbook notebooks), "nonlocal game qiskit" 2, "quantum pseudo telepathy" 3. "magic square game" 195 is mostly classical magic-square puzzles, so it's noise.
  - Not in the Qollab gallery. Quantum Market Game uses a prisoner's dilemma (EWL), which is a different and contested construction.
- Source: GitHub search 2026-10-10; Qollab gallery.
- Rarity: 3 (known to every QI student, rarely turned into a real game).
- Evidence: n/a.
- Quantum hook: essential by theorem. Players provably cannot reach the score without entanglement.
- Buildability: high. 2–3 qubits per round, all rounds packed side by side in one IonQ job.
- Theme fit: Playground (strong), Unlocked (Bell tests and device-independent security link to IonQ / ID Quantique QKD).
- Prior art: textbook notebooks, the Kahoot-style "CHSH game" in IBM tutorials, and "Quantum Odyssey" style puzzles. **Unverified**: whether any polished multiplayer nonlocal game exists. I found none.
- Collision hint: two players who cannot communicate (the IonQ networking story: two linked ion traps), or a social party game where the cheating detector is Bell's inequality.

### S-D-14: Sensing, clocks, PNT and quantum position verification are almost completely empty, and IonQ just bought into them
- What: GitHub counts:
  - GHZ metrology 0
  - quantum sensing game 0
  - entanglement-assisted clock 0
  - quantum clock synchronization 3
  - quantum position verification 3
  - blind quantum computing 10
  - quantum communication complexity 5
  - quantum anonymous voting 0
  - entanglement swapping game 0
  - quantum internet game 3
  - quantum cellular automata music 1

  None of these appear on Qollab. IonQ bought Vector Atomic (PNT: atomic clocks, inertial sensing) and Capella (space).
- Source: GitHub search 2026-10-10; S-D-6 sources.
- Rarity: 5.
- Evidence: real PNT pain. GPS jamming and spoofing became routine in 2024–26 conflict zones and civil aviation; this is from background knowledge and not re-verified in this scan.
- Quantum hook: the GHZ phase-sensitivity N-fold (Heisenberg) vs √N (standard quantum limit) is visible in a ≤12-qubit simulation, and a noise model shows where entanglement stops helping. That makes an honest crossover plot, which is exactly what S-D-2 rewards.
- Buildability: high for the core (GHZ plus a phase plus parity measurement). Medium for a compelling "navigation" framing.
- Theme fit: Unlocked (strong: "why entangled sensors beat N independent ones, until noise kills them"), Impact (a real public dataset is harder; maybe GPS interference maps from gpsjam.org, **unverified CORS**), Playground.
- Prior art: academic only. No hackathon projects found.
- Collision hint: entangled atomic clocks plus a navigation game in a GPS-denied world, or the Capella satellite story.

### S-D-15: Pattern in winners: a narrow, honest, technically specific contribution beats broad "app with quantum inside"
- What: Winners I could find:
  - iQuHACK 2026 IonQ: specific distillation protocols (BBPSSW and DEJMPS), with adaptive selection for 2nd.
  - QuEra 2026: a measured negative result ("no correlation between magic and fidelity").
  - QHack 2024 champion: Modified Singular Value Thresholding for tomography.
  - Qollab Winter 2025: Quantum Garden (meaning change: quantum as slow time / gardening, from non-physicists) and QAVE (rigorous synced visualization from a researcher).
  - Qollab Spring: picked for "honest", "hardware story", "not mapped randomness".
  - QCHack 2021 1st (Microsoft): Mastermind game.
- Source: cards above; https://pennylane.ai/blog/2024/03/qhack-2024-highlights/ ; https://devblogs.microsoft.com/qsharp/?p=1130
- Rarity: 3.
- Evidence: see the cards. **Caveat**: full winner lists for QHack 2025, Fall Fest 2025, Womanium 2025 and Quantum Coalition FLIQ 2025 were not findable.
- Quantum hook: n/a.
- Buildability: n/a.
- Theme fit: all.
- Prior art: n/a.
- Collision hint: Uriel's "meaning change" (Verganti) is what Quantum Garden did. Pair one meaning-change concept with one rigorous measured claim.

---

## AVOID list (counts are GitHub repo search totals, 2026-10-10; noisy but indicative)

| Cliché | GitHub count | Already on Qollab / in this hackathon | Why it loses |
|---|---|---|---|
| BB84 / QKD demo | 1389 / 1020 | Cartheon, Entangle the Andes | Textbook; fails the novelty floor |
| QRNG / quantum dice / coin flip | 484 / 139 / 92 | Quantum Garden uses randomness | "Random output alone does not qualify" |
| Quantum portfolio optimization | 404 (QAOA-portfolio 141) | RegimeRadar, Systemic Oracle | Classical wins; hype-coded |
| Image classification / QML / fraud | 255 / 235 | Space Moths, RegimeRadar | No advantage at ≤25 qubits |
| Quantum tic-tac-toe | 244 | — | Most-cloned quantum game |
| Bloch sphere visualizer | 232 | Qollab project exists | Literally on the platform |
| Quantum chess | 226 | — | Famous prior art (Cantwell) |
| Quantum music from bits/circuits | 190 | 7 items + DianaDancea | Editors call out the "noise-as-music genre" |
| MaxCut QAOA | 169 | iQuHACK 2025 IonQ | Done to death |
| Quantum maze | 122 | Game-jam entries | Superposition = random |
| VQE molecule | 121 | qOrbital | Taken on Qollab |
| Supply chain / TSP / VRP / logistics | 94 / 71 / 70 | Qatalyst, Courier, Cartheon, roads | Qollab's fall RFP is pushing it too |
| Sudoku / Grover search toy | 81 / 47 | Almond (Grover benchmark) | Oracle hides the cost |
| Battleship / pong / minesweeper / poker | 61 / 39 / 38 / 21 | — | Randomness skins |
| Teleportation explainer | 50 | Qollab example (cited as failing the floor) | Textbook |
| Quantum prisoner's dilemma | — | Quantum Market Game | Taken |
| Generic algorithm step-through | — | QAVE, Advantage Lab, QCFlows | Taken |
| Repeater chain + purification + QKD | 25 (repeaters), 35 (distillation) | iQuHACK 2026, 2 live competitors | Converging default "IonQ-pleaser" |
| Measurement-basis detective / collapse game | — | Collapse (live competitor) | Taken this weekend |
| Schrödinger's cat anything | many | arcade jam ×3 | Cliché |

## Gaps list (few or no prior entries, and IonQ-relevant)

1. **Quantum sensing / metrology / clocks / PNT**: GHZ metrology 0, sensing game 0, clock sync 3 repos. IonQ's newest business line (Vector Atomic). The Heisenberg vs SQL crossover under noise is measurable and honest.
2. **Nonlocal games (CHSH, magic square, GHZ pseudo-telepathy) as real multiplayer games**: quantum is provably essential, and it ties to IonQ networking and device-independent QKD. "Nonlocal game qiskit" has 2 repos.
3. **Hardware-native connectivity (all-to-all trapped ion vs heavy-hex SWAP routing)**: an explicit wish from a Qollab winner (Inho Choi). 1–2 repos. Directly IonQ's differentiator, and buildable with Qollab's own fake backends.
4. **QEC where the human is the decoder, running real syndrome circuits**: art installations exist but nothing playable. "qec decoder game" has 0 repos. Expect generic repetition-code explainers from others, so the mechanic must differ.
5. **Position verification / blind computing / proof of quantumness / certified randomness as an experience**: 3 / 10 repos for the first two. Contrarian framing: "how do you know the quantum computer actually did it?" Verification is a live 2025–26 debate (Google's withheld ECDSA circuit and forged ZK proof are on Qollab's own explore page).
6. **Space plus quantum (Capella SAR, satellite QKD, entanglement distribution from orbit)**: "satellite scheduling" 3 repos, and none creative.
7. **Communication complexity / quantum fingerprinting**: 5 repos. Exponential classical-vs-quantum separations that small circuits can demonstrate.

## What wins (pattern)

1. **One sharp, honest, measured claim.** Winners show where quantum helps and where it doesn't (RegimeRadar vs GARCH, Courier "honestly which wins", the QuEra negative result). Hype is penalized by these specific organizers.
2. **Quantum is essential by construction.** Editors reward "not mapped randomness". Strongest of all is a theorem-level necessity (Bell or nonlocal games, Heisenberg scaling), not "we used a circuit to pick a color".
3. **A meaning change by non-physicists still wins** (Quantum Garden: quantum as time/germination, with latency turned into a feature). Uriel's storytelling edge fits here, but it needs a technical anchor (S-D-15).
4. **Topics that align with IonQ.** IonQ's own 2025–26 challenges were optimization benchmarks and then entanglement distillation on networks. Its strategy is networking, sensing, space and trapped-ion fidelity. Projects that show why trapped ions or networking matter get attention, but must not read as an ad.
5. **Docs and remixability are scored**, with a Best Documentation prize. Copy the Soundtrack page skeleton: hook, video, how to run, concept → circuit → effect table, novelty category, fork recipes, disclosure, attribution.
6. **Platform hygiene is a hidden filter.** Judges run on the built-in simulator, the IonQ path needs one job per run, and Safari can't run projects.

## Top 3 from this front

1. **Nonlocal-game party game, possibly framed as two linked ion traps (S-D-13 + S-D-5/6).** Quantum advantage is a theorem, not a claim. It's empty on Qollab and GitHub, fits one IonQ job, and lands in Playground with a strong Unlocked/networking echo that differs from the crowded repeater+QKD builds.
2. **Entangled sensing / clock / GPS-denied navigation with an honest Heisenberg-vs-noise crossover (S-D-6 + S-D-14).** It's the emptiest category anywhere (0 repos), mirrors IonQ's newest acquisition, and can be an Unlocked or Impact entry with a real measurable curve.
3. **"You are the transpiler": a connectivity/routing puzzle comparing trapped-ion all-to-all with heavy-hex SWAP overhead on Qollab's own fake backends (S-D-7).** It answers a public wish from a Qollab winner, is ICPC-flavoured for Uriel, and is measurable (SWAPs, depth, fidelity). Risk: it can read as IonQ marketing unless framed as a universal lesson.
