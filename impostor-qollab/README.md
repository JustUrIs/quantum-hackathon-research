# IMPOSTOR: Can you fake a quantum computer?

<!-- ![2-minute demo](https://youtu.be/XXXXXXXXXXX)  ← replace with the YouTube link; YouTube embeds on Qollab -->

> You get every classical trick: a plan agreed in advance, shared randomness, memory, and a bot that brute-forces every possible strategy.
> A referee written in Qiskit unmasks you anyway, and shows you the theorem that does it.

**This effort is supported by Qollab & IonQ.**

## Try it in 60 seconds (for judges)

1. Upload the project and press **Run** on Qollab's free local simulator. The code targets the selected Qollab backend, including IonQ simulators, with one job per run. **Live Qollab/Pyodide and remote IonQ execution remain unverified as of October 11.** Local Python/browser checks are documented below.
2. Open **02 Magic square**, press **Play 200 rounds**, then **Let the bot try all 4,096 plans**. One cell always clashes. The quantum pair wins every round.
3. Switch **Who plays the quantum side?** to **/dev/urandom** and play again: the "quantum" record falls apart.
4. Open **03 Zip**, choose **12 qubits** and drag the bits slider: thousands of bits still lose to 12 qubits.

## Why this exists

In April 2026 a 1 BTC prize went to a "quantum attack" on a small elliptic-curve key run on cloud quantum hardware. Someone then replaced the quantum backend with `/dev/urandom` and the key still came out: the classical post-processing was doing all the work ([HN discussion, 383 points](https://news.ycombinator.com/item?id=47897647)). Craig Gidney's line on that episode: such runs "succeed for the wrong reason".

Quantum computing is sold, funded and audited as **speed**. Speed is the advantage nobody can check today, and a simulator doesn't have it at all. Some quantum advantages, though, can be **proven on paper**, at a size that fits in a browser:

| Advantage | What can't be faked | Proof |
|---|---|---|
| **Correlation** | Two players who cannot talk win more often than any plan allows | Bell / CHSH (1964/69); Mermin–Peres (1990) |
| **Memory** | 12 qubits do a job that provably needs at least 78 classical bits | Kretschmer, Grewal, …, Aaronson, [arXiv:2509.07255](https://arxiv.org/abs/2509.07255) (2025) |

IMPOSTOR turns those proofs into a game where **you are the forger**. The thesis it argues: *a quantum computer is not a faster computer; it is the thing you can't fake.*

## Results (measured with this repo)

| Level | Quantum | Best classical | `/dev/urandom` | Where the bound comes from |
|---|---|---|---|---|
| 01 Telepathy (CHSH) | **85.6%** exact sampling, 84.6–86.3% in the packed job | **75%**: all 16 deterministic plans checked; shared randomness only mixes them | ~51% | CHSH inequality; Tsirelson cos²(π/8) = 85.36% |
| 02 Magic square | **100.0%** | **88.9%**: all **4,096** deterministic plans checked, 144 tie at 8/9 | ~51% | Mermin–Peres: rows multiply to +I, columns to −I |
| 03 Zip, n = 8 | XEB **1.03** | our impostor: 0.41 with 512 bits, 0.76 with 2,048 bits | ~0.00 | linear XEB, ideal ≈ 1 |
| 03 Zip, n = 12 | XEB **0.99** | our impostor: 0.06 with 768 bits, **0.32 with 6,144 bits**; the paper proves ≥78 bits are needed for 0.427, and its best known protocol uses ~330 | ~0.00 | arXiv:2509.07255, Theorem 1 |

**Does it survive noise?** Historical offline results for the 20-qubit audit circuit with depolarizing plus readout noise (Qiskit Aer): at 0.5% two-qubit error CHSH scores 0.845 and the three-cell magic check 0.978; at 5% they score 0.825 and 0.916. CHSH remains above the full-game 0.75 ceiling in these samples. The three-cell magic check has a classical ceiling of 1, so those scores do not establish a violation. These results have not been rerun in the October 11 review.

Reproduce: `python -m tests.test_impostor` (16 checks) from the project root. All 16 passed in the October 11 local review, including the corrected subset bound. A focused Chromium check also verified the displayed subset bound and mixed-source label without page errors; this does not certify live Qollab execution.

## How it works

### The one job
IonQ backends accept **one job per run** and return counts only. So on load, `impostor/service.py` packs the referees side by side into **one 20-qubit circuit**, which fits IonQ Aria (25) and Forte (29):
- the four CHSH settings, 2 qubits each
- three magic-square cells that together touch every row and column, 4 qubits each

The page sends it to whatever backend you chose in *Select QPU* and shows the scores as **"The one job"**. Choosing **This run's backend** reuses the collected shots for covered settings; the six missing magic-square settings use exact simulation, explicitly labeled as a mixed source. Replayed shots are not new independent measurements. **Qiskit, exact** samples each round's own circuit from its exact statevector.

**The three-cell backend check has a classical ceiling of 100%.** The 8/9 bound applies to the full game with all nine uniformly sampled settings. The packed magic-square circuit checks implementation behavior; its score cannot demonstrate violation of the full-game bound. Likewise, its reported offline noise scores must not be compared to 8/9 as a nonlocality test. All these circuits run in one simulator/device; this is an educational model of separated players, not a loophole-free Bell experiment or hardware certification.

### 01 Telepathy (CHSH)
- **Concept:** you get a bit x, your partner a bit y. You win if a ⊕ b = x·y.
- **Circuit:** `H(0) · CX(0,1) · RY(−θx)(0) · RY(−θy)(1)`, with θx ∈ {0, π/2} and θy ∈ {π/4, −π/4}.
- **Number:** 85.4% in theory, 85.6% measured.
- **Theorem:** no plan beats 75%.

### 02 Magic square (Mermin–Peres)
- **Concept:** you answer a row of 3 signs with product +1; your partner answers a column with product −1. You must agree on the cell where they cross.
- **Circuit:** two Bell pairs, 4 qubits, **no ancillas**. For each row and column, the code finds a 2-qubit Clifford that rotates the line's commuting observables onto Z. It searches automatically with `Pauli.evolve`, so the decoding signs are derived, not hand-typed. Your partner's answers use the transpose identity of |Φ+⟩ (Yᵀ = −Y).
- **Number:** 100%.
- **Theorem:** no grid of numbers satisfies all six parity rules, so the best plan wins 8/9.

### 03 Zip (quantum information supremacy)
- **Concept:** you send a message; your partner then runs a random Clifford measurement you never see and outputs strings scored by linear XEB.
- **Quantum message:** an n-qubit random brickwork state (U + RZZ, **periodic boundary**).
- **Classical message:** k sign bits of the state's projections onto shared random vectors, which your partner turns into a guess.
- **Theorem (from the paper):** bits needed ≥ min{Ω(ε²2ⁿ), ε·2^(n−O(√n))}.
- **n = 12:** the curve is precomputed offline (`data/zip_n12.json`) because 4,096-amplitude sketches are slow in the browser. **n = 8** is computed live.

### Why trapped ions
- In Zip, the wrap-around gate between the last and first qubits is native on all-to-all ion chains; a nearest-neighbour chip pays SWAPs for it.
- "Two players who can't talk" is the networking picture: two linked ion traps.
- CHSH-type tests are the basis of device-independent QKD.

## What we do NOT claim

- **A simulator proves no physical advantage.** It *computes* the correlations. The advantages here are theorems about separated players and about bits, so they hold however fast the computer running the simulation is.
- **CHSH and the magic square are not new.** They date from 1969 and 1990. What is new is the format:
  - you play the impostor
  - a `/dev/urandom` ablation is built into every level
  - an exhaustive bot is built into every level
  - an ancilla-free packed audit circuit
  - an interactive version of a 2025 result that, as far as we found, has no Qiskit port
- **Our Zip impostor is one natural strategy, not the best one.** The 78-bit bound and the ~330-bit protocol are the paper's. As the authors note, their experiment chose Bob's measurement before Alice's state was prepared.
- **Short runs are noisy.** The page shows each plan's exact value next to its sampled score.

## Files

| Path | What |
|---|---|
| `index.html`, `main.css`, `main.js` | UI. The only `backend.run` call is in `runAudit()` |
| `impostor/games.py` | circuits, the classical impostors, referees, brute force |
| `impostor/service.py` | JSON functions called from JS, plus the packed audit circuit |
| `data/zip_n12.json` | precomputed 12-qubit Zip curve |
| `tests/test_impostor.py` | 16 checks (theory values, brute force, ablations, audit and subset bound) |
| `dev/` | local harness only (HTTP bridge + Playwright UI test); not used on Qollab |
| `tools_*.py` | offline scripts that produced `zip_n12.json` and the noise table |

**To extend:** add a level as one circuit, one classical bound and one ablation, e.g. GHZ phase sensing, where N entangled qubits reach 1/N and N independent ones 1/√N, until noise erases the gap.

## Built during the hackathon

Everything here was written during the build window (Oct 9–11, 2026). No pre-existing project code. We used Qiskit 2.x and its examples. The Zip protocol and bounds come from Kretschmer et al. (2025), credited above; we did not reuse their code. The single packed job follows the pattern of Qollab's *Quantum Hackathon Soundtrack*. AI assistance (Claude, Codex) was used for research, code and copy, and all results were checked by the tests above.

## Accessibility

- Every control is a real button or input.
- Tabs follow the ARIA tab pattern, with arrow-key navigation.
- Results are announced through `aria-live` regions.
- The magic square cells have spoken labels.
- Colour is never the only signal: verdicts are written out, and Y/P values are printed in each cell.
- Animation respects `prefers-reduced-motion`.

## License

MIT. See `LICENSE`.
