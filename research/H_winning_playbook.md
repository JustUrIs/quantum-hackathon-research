# H. Winning playbook: how hackathon winners build and pitch, applied to IMPOSTOR

> Scanned Sat 2026-10-10. Deadline: **Sun Oct 11, 19:00 ET (20:00 ART)**. The rubric is **Novelty & creativity, Technical execution, Impact potential, Documentation quality**, with no published weights. Judges "open the project page, read the description and the code, and press Run on a free simulator" (see `F_qollab_platform.md`).
>
> **Evidence tags.** **[V]** means the source states it. **[INF]** is my inference from the source, since most winner write-ups don't give the judges' reasons. **[UNV]** means unverified: a single self-reported or social source, or one I couldn't open.
>
> **Gaps, stated honestly.** I could not find official winner lists for **HackITBA** (any year), **Platanus Hack 25 overall** or **Platanus BA (May 2026)**, the **Cal Hacks 2025 / HackMIT 2025 / PennApps 2025 grand prizes**, or **Apart Research sprint rubrics**. I also found no description of the Qollab 2025 winners (**Quantum Garden** and **QAVE**). Before recording, open them on qollab.xyz/projects (5 minutes). They are the closest thing to "what this jury liked".

---

## 1. Case cards (15)

### 1. CrossBeam: 1st place, Anthropic "Built with Opus 4.6" (Feb 2026)
- **What:** Sub-agents read California permit blueprints and correction letters and return an action plan in about 20 minutes. Built by a personal-injury lawyer with no software background. [V]
- **Why it won [INF]:** It opens on hard numbers about a real pain: a **90%+ first-submission rejection rate, a 6-month delay, and $30k per home**. Buena Park needs 8,900 units by 2029 but permitted about 120 in 2024 [V]. A domain expert owns the problem.
- **Pitch trick:** A reframe in one line: "a permit crisis, not a housing crisis." [V]
- Link: https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon

### 2. Elisa: 2nd place, same event
- **What:** A block-based visual IDE for kids where AI writes the code. [V]
- **Why [INF]:** It shows proof of effort as numbers (**30 h, 76 commits, 39k LOC, 1,500+ tests**) [V] and has a real user: it is named after the builder's 12-year-old daughter, who used it for a science fair [V].
- **Pitch trick:** A human anchor ("my daughter used it") plus a wall of verification numbers.
- Link: same as card 1.

### 3. TARA: "Keep Thinking" prize, same event
- **What:** Turns dashcam road footage into an investment appraisal (NPV, sensitivity analysis) and generates a PDF in one click. [V]
- **Why [INF]:** The before/after contrast is brutal: **$1–4M and 9–14 months versus about 5 hours** [V]. The demo ran on real footage of a real road (Kira–Matugga, Uganda) [V].
- **Pitch trick:** One click produces one artifact. The judge watches the output appear.

### 4. Conductr: "Creative Exploration" prize, same event
- **What:** A browser MIDI instrument that generates the band live. A prompt like "make it funky" changes the arrangement mid-performance. [V]
- **Why [INF]:** The demo is a **performance**, not a tour of features. It backs the claim with one technical number (a note every **15 ms** from a C→WASM engine) [V].
- **Pitch trick:** Let the audience feel it before you explain it.

### 5. Opti-Maze: 1st place, MIT iQuHACK 2022 (IonQ × Microsoft challenge)
- **What:** **A game where you compete against a quantum computer**, flipping binary variables to beat the QAOA result, with a co-op mode on a CO2-emissions problem. Ran on IonQ hardware through Azure. [V]
- **Why:** No judge reasoning was published [UNV]. It is IonQ's own blog that showcased it [V].
- **Relevance:** This is **the closest precedent to IMPOSTOR** (human vs QC, run on IonQ). It shows that IonQ judges reward the "player vs quantum computer" format. **Our difference:** in Opti-Maze the human can win, and with us **a theorem says you can't**. Say that out loud.
- Link: https://www.ionq.com/blog/february-09-2022-iquhack-winners-opti-maze

### 6. Piqasso: 1st place, iQuHACK 2026 (QuEra challenge)
- **What:** Compared circuit fidelity against "magicness". [V]
- **Why [INF]:** Their headline result was **negative and stated plainly**: they "found no correlation" [V]. Quantum judges reward honest measurement over hype.
- **Lesson:** Our "What we do NOT claim" section is an asset, not filler.
- Link: https://thetech.com/2026/02/19/iquhack-2026

### 7. QHack 2024 open hackathon (Xanadu/PennyLane)
- **Winners:** Quolumbia (in-person champion, singular value thresholding for tomography), plus Kharkiv_team and others. [V]
- **What the judges say they want [V]:** Build on **recent papers**. "Clearly and honestly show the results". A simpler result with critical thinking beats a flashier one. **"Please don't make us do code archaeology"**. "Include a readme… tell us which file does what… leave us a guide that will let us retrace your steps". Don't drift from the challenge.
- **Relevance:** Level 3 (Kretschmer/Aaronson, arXiv 2509.07255, 2025) hits "recent paper" squarely.
- Links: https://pennylane.ai/blog/2024/02/how-to-do-a-great-hackathon-project · https://pennylane.ai/blog/2024/03/qhack-2024-highlights/

### 8. QuantumJam 2025 (IEEE CS ITBA + IBM Quantum, Buenos Aires): UdeSA team
- **What:** An end-to-end QKD platform covering BB84 and E91, noise models, **simulated man-in-the-middle attacks**, error correction, privacy amplification, and QBER visualizations in Qiskit Aer. [V] Three of the four had competed in **HackITBA** before. [V]
- **Why:** They say it was "comprehensive and realistic," and that "the visualizations made it easy to understand and evaluate". [V]
- **Relevance:** This is the **local quantum jury culture** (the ITBA ecosystem). Simulating the attacker won there. **IMPOSTOR is the attacker as a game.**
- Link: https://www.udesa.edu.ar/noticias/quienes-son-los-jovenes-argentinos-que-ganaron-la-primera-competencia-de-computacion-cuantica-del

### 9. Little Dragons: 1st place overall, Platanus Hack 2024 (Santiago)
- **What:** Kids aged 8–10 learn to save by raising a virtual dragon, with mini-games and rewards. [V]
- **Why [INF]:** A **named mental model** (the 4-stage habit loop: cue, craving, response, reward [V]) plus a playful, concrete user. **Theory as game mechanics** is the same move as "theorem as the boss of the level".
- **Format [V]:** 36 h, 3–5 person teams, **3-minute final pitch** on Sunday morning, a five-person founder/VC jury, and the motto "de cero a producto en 36 horas" (from zero to product in 36 hours).
- Links: https://www.ing.uc.cl/noticias/estudiantes-de-ingenieria-uc-destacan-con-increibles-proyectos-en-platanus-hack-2024/ · https://www.df.cl/df-mas/punto-de-partida/36-horas-de-programacion-nonstop-asi-fue-la-primera-platanus-hack

### 10. Kairos: Finance track, Platanus Hack 2024
- **What:** Explains a credit card statement "in human language" from the bank PDF. [V]
- **Why [INF]:** Three of the members had banking/fintech experience, so domain credibility drove the track choice [V]. The **team had a world-class designer** [V], so polish was not left to chance.
- **Pitch trick:** The pitch was given by the person who cared most (he stutters and pitched anyway [V]). Conviction beats smoothness.
- Link: https://huss.substack.com/p/ganamos-la-hackaton-de-platanus

### 11. Anómala: Tech track, Platanus Hack 2024
- **What:** Detects website hacking attempts from anomalous browser behavior, blocks them, and **replays incident recordings**. Integrates with **one line of code**. [V]
- **Why [INF]:** A security product that **shows the attacker getting caught** on replay. Adoption is trivially cheap.
- **Relevance:** "Watch the impostor get caught, with a replay" is a proven demo beat.

### 12. Shepherd: Grand prize, TreeHacks 2026 (Stanford)
- **What:** A motorized smart cane that sees obstacles and steers its user. [V]
- **Why [INF]:** The rubric was creativity, technical complexity and social impact [V]. The demo has one physical moment you can't misread.
- Link: https://stanforddaily.com/2026/02/15/12th-annual-treehacks/

### 13. Baymax: Moonshot Grand Prize, TreeHacks 2024
- **What:** A CV robotic arm that feeds people with paralysis or Parkinson's. [V]
- **Pitch trick [V]:** Moral framing: the lack of affordable care is "unacceptable given the capabilities of today's technology". Judges read it as "innovation + empathy".
- Link: https://stanforddaily.com/2024/02/27/treehacks-2024/

### 14. DeFake: Grand prize, PennApps XX (2019)
- **What:** A browser extension that estimates whether a video was manipulated. [V]
- **Why [INF]:** **Authenticity verification during a hype/fear moment** (deepfakes, 2019). This is structurally identical to our pitch: "how do you know a 'quantum' result is real?" in the quantumslop moment.
- Link: https://penntoday.upenn.edu/news/deepfake-detector-wins-pennapps-xx

### 15. Soshi / Suparova: Supabase AI Hackathon at YC (Dec 2024)
- **What:** Soshi (overall) is a Twitter reply assistant. Suparova ("Most Novel Use") is a talking, dancing rover. [V]
- **Format [V]:** Semi-finals, then the top 10 on stage before YC partners (Jared Friedman and others).
- **Why [INF]:** The overall winner was a **narrow, obviously useful** tool. "Most novel" went to the most **surprising embodiment** of the sponsor's tech, not the most complex one.
- Link: https://supabase.com/blog/ai-hackathon-at-y-combinator

**Other LatAm notes.** NASA Space Apps: Lemon Py's "Pollen Alert" (Argentina) won **Best Use of Data** globally, per a congressional report; the year is unclear [UNV]. Platanus 2026 CDMX: a team claims 1st place with "Dominikito", personalized kids' stories, on LinkedIn [UNV]. **Platanus runs a "Cómo hacer un buen demo" (How to make a good demo) workshop at 20:00 on Saturday** [V]. Like YC, the accelerator treats the demo as the product.

**Qollab Creative Challenge.** The criteria are "creativity, storytelling, interactivity, and technical rigor" and "what quantum computing can uniquely do" [V]. IonQ judges [V]. *"Uniquely do"* is literally our thesis. Quote it.

---

## 2. Patterns that win (ranked by how often they show up × how well they fit our rubric)

1. **One "oh, this is possible" moment, shown within 90 s.** Bonnie Xu (OpenAI): one clear moment beats a feature tour. Jono Bacon: show a working solution within about 90 s of stating the problem. Colin Lowenberg: "one flow" [V, JetBrains]. **For us, that moment is the magic square: 100% vs 8/9, then the quantumslop button.**
2. **A number-driven problem in the first 15 s.** Every Opus 4.6 winner led with a hard contrast (90% rejection, $1–4M vs 5 h) [V]. **For us: 1 BTC paid, `/dev/urandom` got the same key, and 4,096 strategies all fail.**
3. **A reframe sentence.** "A permit crisis, not a housing crisis." **For us: "A quantum computer isn't a faster computer. It's something you can't fake."** Say it twice: at 0:25 and at the close.
4. **Honest rigor that quantum judges can check.** QHack asks for honest results and no code archaeology. Piqasso won with a null result [V]. **A "What we do NOT claim" section plus a table that runs from concept to theorem.**
5. **A recent paper, made tangible.** QHack: "build on recent publications" [V]. **Level 3 (2025) is the differentiator. Name the paper on screen.**
6. **Game or performance format with the judge as player.** Opti-Maze (IonQ!), Little Dragons, Conductr [V]. Kelvin Boateng (Google): "I play it to see if it solves the problem" [V]. **Judges press Run, so the Run must be the game.**
7. **Fit the sponsor's business.** "If I reward this, will my company look good?" [V, sustained.substack]. **IonQ: all-to-all connectivity (the level 3 wrap gate), networking (two traps = two players who can't talk), DI-QKD, and sensing.** One slide, one sentence each.
8. **Proof-of-work numbers.** Elisa's commits and tests [V]. **For us: "4,096 strategies brute-forced, N rounds simulated, 3 theorems, 1 IonQ job per level."**
9. **Moral or real-world stakes, kept brief.** Baymax, DeFake [V]. **For us: cloud QC is sold by the hour, and the customer cannot verify it today.**
10. **Text and video complement each other.** Richard Moot: a great video with a thin description is a red flag. Karen Bajza-Terlouw: "Ambiguity is a red flag" [V].

**What makes "Most novel" winners [INF from Suparova, Conductr, Opti-Maze, the Qollab criteria]:** an **inversion of roles or medium** (you are the fraud, not the user), a **surprising embodiment** of known science, and an angle that other teams won't take. Nathan, a 22-time winner, says: "anticipate what others will build, take a different angle" [V]. Expected crowd here: QRNG, Bell-pair "is it entangled" checks, Bell's Bluff-style card games (F front). **Pre-empt it: "This isn't another Bell demo. You play the forger."**

---

## 3a. Video script template: 2:30, adapted to IMPOSTOR (English narration, Spanish subtitles optional)

Rules: the **hook is in the first 10 s** (judges binge). The product is visible before 0:30. Show **no code editor or terminal** except the 3-second "swap backend" proof. Spend about 40% on demo and 60% on explanation [V, Nathan]. Use the best microphone. Burn captions in. Upload to **YouTube, public or unlisted** (it is the only host that embeds on Qollab).

| Time | Beat | Screen | VO (draft) |
|---|---|---|---|
| 0:00–0:10 | **HOOK** | The HN headline "1 BTC… quantum" → hard cut to a terminal: `/dev/urandom` → same key | "Someone got paid one bitcoin for breaking a key with a quantum computer. Then someone swapped the quantum computer for random noise. Same result." |
| 0:10–0:25 | **Question + reframe** | Black screen, white text: *How do you know it's quantum?* | "Speed can't be verified today. But some quantum advantages can be **proven**. So we built a game where **you** are the impostor." |
| 0:25–1:05 | **The trick (magic square)** | The game UI on Qollab. A human fills the grid and loses one cell. The bot counter runs to 4,096 and stalls at 8/9. The quantum pair wins 100% in green | "Fill a 3×3 grid of signs. Rows multiply to +1, columns to −1. Impossible, and the bot tries all 4,096 strategies: 8 out of 9, never 9. The entangled pair? 100%. Every time." |
| 1:05–1:25 | **The prestige: the quantumslop button** | Click → `/dev/urandom` → the score collapses to 51% live | "Here's the test we give the judge: swap the quantum backend for random bits. It collapses. The advantage isn't in the software. It's a theorem." (show the inequality for 2 s) |
| 1:25–1:55 | **Level 3, the novel part** | Slider for "bits given to the impostor". The curve rises slowly. A dashed line marks the theorem bound (≥78 bits), a line marks the paper's best (~330), and a quantum dot sits at 12 qubits | "Level three is from a 2025 paper, run on trapped ions like IonQ's. Twelve qubits. To fake it you need at least 78 bits, and our impostor needed about 3,000." (arXiv ID on screen) |
| 1:55–2:10 | **Rigor and honesty** | A quick pan over the project page: the results table, and "What we do NOT claim" | "Every level: simulation, exhaustive brute force, and an ablation. And a section on what we don't claim." |
| 2:10–2:25 | **Impact + IonQ** | Three icons: networking (two traps), DI-QKD, sensing | "Cloud quantum is sold by the hour. IMPOSTOR is the playable version of a quantumness audit, and it fits one IonQ job per level." |
| 2:25–2:30 | **Close** | Title card: **IMPOSTOR: you can't fake a quantum computer**, plus the Qollab link and "This effort is supported by Qollab & IonQ" | "Quantum isn't faster. It's unfakeable. Try to fool it." |

Production: record screen captures first, then the VO, then edit. Make a **placeholder upload by Sun 14:00 ART** and replace it later [V, Devpost]. Ask one outsider to watch it once and **explain it back**. If they can't, re-cut [V, Devpost].

## 3b. Project page template (Qollab page / README)

Qollab's minimums [V]: what it does, the problem, how to run, how to replicate/extend, disclosure of pre-existing work, MIT. Everything else is for winning.

```markdown
# IMPOSTOR: Can you fake a quantum computer?
![2-min demo](https://youtu.be/XXXX)          <- embeds on Qollab
> You get every classical trick: strategy, shared randomness, memory, a bot that brute-forces 4,096 strategies.
> A Qiskit referee unmasks you anyway, and shows you the theorem that says why.

## Try it in 60 seconds (for judges)
1. Press **Run** (the free local simulator gives the full experience; Chrome or Edge, not Safari).
2. Play **Magic Square** → lose a cell → press **"Let the bot try"** → press **quantumslop**.
3. Open **Zip** and drag the bits slider past the theorem line.

## Why this exists (the problem)
Cloud quantum is sold by the hour. In April 2026 a "quantum" key break was reproduced with /dev/urandom [link].
Speed claims are unverifiable today; **correlation, memory and precision advantages are provable**.

## Results (measured, this repo)
| Level | Quantum (measured) | Best classical (theorem / brute force) | /dev/urandom | Theorem / paper |
|---|---|---|---|---|
| Telepathy (CHSH) | 85.6% | 75% (16/16 strategies) | ~50% | Tsirelson; CHSH 1969 |
| Magic square | 100.0% | 88.9% (4,096 strategies, 144 tie) | 51% | Mermin–Peres 1990 |
| Zip (n=8 / 12) | XEB 0.80 | ≥78 bits needed (paper); ours ~3,000 | 0.03 | Kretschmer et al., arXiv:2509.07255 |
(Reproduce: `python proto/test_referees.py` and `python proto/zip_experiment.py` → print these numbers.)

## How it works (concept → circuit → number → theorem)
One short subsection per level + circuit image + qubit count + "1 IonQ job".

## Why IonQ / trapped ions
All-to-all connectivity: the wrap-around gate (q11↔q0) is native. Two traps = two players that can't talk.

## What we do NOT claim
(copy §7 of the spec verbatim: the simulator ≠ physical advantage; our Zip impostor ≠ optimal; CHSH/MP are not new; loophole note)

## Run / replicate / extend
Files: `main.js` UI · `referee/` circuits · `data/*.json` recorded IonQ-sim runs · `proto/` verification scripts (`test_referees.py`, `zip_experiment.py`).
Extend: add a level = 1 circuit + 1 classical bound + 1 ablation.

## Built during the hackathon vs before
Pre-existing: ___ (credit). AI assistance: ___ (disclosed). License: MIT.

## Team
4 names + roles, one line each.
```

---

## 4. The 36h workflow (ART; deadline Sun 20:00 ART = 19:00 ET)

**Principles [V]:** work backward from the winning demo (Lowenberg). Freeze early. Leave at least 15% of the time for polish (Nathan: about 5 h of 36). Mock and pre-fill anything that can stall (Lowenberg). Check every few hours that you're still on the brief (QHack).

- [ ] **Sat, now:** Pick the **single demo flow** (Magic Square → bot → quantumslop → Zip slider). Anything not in that flow is optional. Write the **page text first**: it doubles as the video script [V, Devpost].
- [ ] **Sat, now:** Open Quantum Garden and QAVE on Qollab (5 min). Note what the jury already rewarded and copy their page structure.
- [ ] **Sat by 14:00:** Hello-world on Qollab: `main.js` + **one** `backend.run` on the IonQ sim, under 25 qubits. Confirm the page renders and Run works in Chrome. *This is the riskiest unknown. Kill it first.*
- [ ] **Sat by 20:00:** Level 2 (the magic square) playable end to end on the local sim, including the quantumslop toggle. **This is the MVP. If everything else dies, this ships.**
- [ ] **Sat by 20:00:** Commit recorded IonQ-sim results to `data/*.json` with a recorded / ideal / this-run selector.
- [ ] **Sat 20:00–02:00:** Level 3 slider (precomputed curve is fine), then Level 1. Level 4 only if 1–3 are polished (per the spec).
- [ ] **Sat 23:00:** Make a rough screen recording of the flow. Watch it as a team. Cut anything over 2:30 [V, Lowenberg: "cut features rather than rushing"].
- [ ] **Sun 09:00: FEATURE FREEZE.** After this, only bugfixes, copy and visuals.
- [ ] **Sun 09:00–13:00:** Record the VO and screen captures, then edit. In parallel, finish the docs and table (rerun `proto/test_referees.py` + `zip_experiment.py` and paste real numbers).
- [ ] **Sun 14:00:** Upload the placeholder video to YouTube and confirm it **embeds and plays logged out**. Submit a complete draft (the captain can edit until the deadline [V]).
- [ ] **Sun 15:00:** Fresh-eyes QA: someone outside the team opens the page in Chrome or Edge, follows the "60 seconds for judges" steps, and explains it back.
- [ ] **Sun 17:00:** Final video swap, final page, MIT license, disclosures.
- [ ] **Sun 19:00 ART: SUBMITTED** (1 h margin). Then run the IonQ sim one last time to confirm it doesn't crash.

**Roles (one owner each):** Physics/verification (student) · Build/integration and code freeze (hackathonero) · Page, docs and QA (unknown profile) · Narrative, video and final call on cuts (Uriel). *One person can veto scope after 09:00 Sunday.* That person is the hackathonero.

---

## 5. Anti-patterns (don't)

1. **A feature tour instead of one flow.** It's the most common failure judges name [V, JetBrains].
2. **Opening with CHSH or a definition of entanglement.** Judges have seen Bell demos. Open with the fraud [spec §8 + INF].
3. **Describing features that don't exist, or being vague about limits.** Judges read that as weakness [V, Avi Press]. Say "precomputed" where it is.
4. **Code archaeology:** no file map, no reproduce command [V, QHack].
5. **A polished front end with thin code, or a template with the colors changed** [V, Bajza-Terlouw, Boateng].
6. **A great video with a thin description, or the reverse** [V, Moot].
7. **Overclaiming quantum advantage from a simulator.** This jury will catch it. Our honesty section is our moat [V, QHack; INF].
8. **A second `backend.run` on IonQ,** over 25 qubits, Safari demos, a private or unembeddable video [F front].
9. **Uploading in the last hour** [V, Devpost]. **Undisclosed pre-existing code or AI help** means disqualification [V, Qollab terms].
10. **A script that sounds LLM-generic.** Devpost warns about exactly this [V]. Keep our voice: "you're the fraud."
11. **Reading the script flat.** Visible enthusiasm is persuasive [V, JetBrains]. Record the VO standing up, take 3.

---

### Sources
- Anthropic Opus 4.6 winners: https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon
- JetBrains, judging-table notes: https://blog.jetbrains.com/ai/2026/06/how-to-win-a-hackathon-notes-from-the-judging-table/
- Devpost: https://info.devpost.com/blog/6-tips-for-making-a-hackathon-demo-video · https://info.devpost.com/blog/hackathon-judging-tips · https://info.devpost.com/blog/user-story-nathan
- PennyLane/QHack: https://pennylane.ai/blog/2024/02/how-to-do-a-great-hackathon-project · https://pennylane.ai/blog/2024/03/qhack-2024-highlights/ · https://pennylane.ai/blog/2023/04/qhack-2023-highlights
- iQuHACK: https://www.iquise.mit.edu/iquhack/2024-02-02 · https://www.iquise.mit.edu/iquhack/2023-01-27 · https://thetech.com/2026/02/19/iquhack-2026 · https://www.ionq.com/blog/february-09-2022-iquhack-winners-opti-maze
- Qollab × IonQ: https://www.ionq.com/news/ionq-partners-with-qollabs-creative-challenge-advancing-creative-quantum-innovation
- Platanus: https://www.df.cl/df-mas/punto-de-partida/36-horas-de-programacion-nonstop-asi-fue-la-primera-platanus-hack · https://huss.substack.com/p/ganamos-la-hackaton-de-platanus · https://www.ing.uc.cl/noticias/estudiantes-de-ingenieria-uc-destacan-con-increibles-proyectos-en-platanus-hack-2024/ · https://hack.platan.us/26-ar
- ITBA/QuantumJam: https://www.udesa.edu.ar/noticias/quienes-son-los-jovenes-argentinos-que-ganaron-la-primera-competencia-de-computacion-cuantica-del · HackITBA 2026: https://www.lanacion.com.ar/tecnologia/llega-hackitba-la-hackathon-mas-grande-de-buenos-aires-que-lleva-a-estudiantes-universitarios-a-nid17032026/
- TreeHacks: https://stanforddaily.com/2026/02/15/12th-annual-treehacks/ · https://stanforddaily.com/2024/02/27/treehacks-2024/
- PennApps: https://penntoday.upenn.edu/news/deepfake-detector-wins-pennapps-xx
- YC/Supabase: https://supabase.com/blog/ai-hackathon-at-y-combinator
- Sponsor psychology: https://sustained.substack.com/p/lessons-from-winning-five-hackathons
