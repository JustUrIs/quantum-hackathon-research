# Research brief — Qollab × IonQ Quantum Hackathon (Oct 9–11, 2026)

## Hard constraints
- Deadline: Sun Oct 11 2026, 19:00 ET. Now: Sat Oct 10 ~00:30 ART. ~20h of real build time after ideation.
- Must be a **Qiskit** project, runnable on Qollab's free simulators incl. **IonQ simulator** (IonQ backend = ONE job per run → everything measured goes in one circuit). Browser runtime (WebAssembly). Network: only GET to CORS-enabled servers. No persistence between runs (ship state as files). MIT license. 2–3 min demo video.
- Judging (same 4 traits, local then global): **Novelty & creativity, Technical execution, Impact potential, Documentation quality**.
- Themes (specialty awards, $500 + $5k compute each; global 1st = $10k + $20k compute + IonQ mentorship/interview fast-track):
  - **Quantum Impact**: real industry problem (logistics, manufacturing, space, finance, energy…), public dataset, STRONG classical baseline, show where quantum subroutine makes measurable difference.
  - **Quantum Playground**: game/music/art/interactive — superposition/interference/entanglement/measurement must be ESSENTIAL, not just randomness.
  - **Quantum Unlocked**: teach a hard timely topic (error correction, fault tolerance, networking, algorithms) via interactive demo/viz/GUI that makes it click.
  - Also: Most novel/creative, Most impact, Best documentation.
- Up to 5 submissions per team, judged independently.
- Judges = IonQ engineers + local panel. They detect pseudo-quantum instantly. Quantum must be essential & honest.

## Team (4)
- Uriel (captain): idea, storytelling, design, pitch; ICPC/algorithms lover; no quantum background.
- Hackathon grinder (builds fast, generalist).
- Student of quantum mechanics / quantum computing (the technical credibility).
- Unknown profile.

## Method (Uriel's design course — "How to Future", Scott Smith)
- **Weak signal** = small early clue of change, almost nobody pays attention. Uriel's filter: "only ~100 people in the world know it".
- **Contrarian truth** (Thiel): important truth few agree with.
- Value is NOT the signal alone but the **connection between signals** ("si pasa X, entonces pasa Y"; "¿qué pasaría si combinamos A y B?").
- Thiel 0→1: if it already exists, it's worth less. So always check prior art / competition.
- Norman & Verganti: radical innovation via technology change OR **meaning change** (Wii).
- Schön: "there is a problem in finding the problem" — find real problems, not tech looking for use.
- Uriel's taste: wants MAGIC (Clarke), change-the-world bar, extreme bold concept, not generic middle ground. Hates fluff.

## Output format for every scanning agent
Write findings to your assigned file in this folder as **signal cards**:

```
### S-<front>-<n>: <short title>
- What: 1–3 sentences, concrete.
- Source: URL(s) + date.
- Rarity: how many people likely know this (1 = everyone, 5 = ~100 people).
- Evidence of real pain / real need (quotes, issue counts, stars, citations) — or "none".
- Quantum hook: why quantum is ESSENTIAL here (or "none / decorative").
- Buildability in ~20h with Qiskit on simulator (≤ ~25 qubits ideally): high/med/low + why.
- Theme fit: Impact / Playground / Unlocked / none.
- Prior art / competition: who already did it (links). Be honest.
- Collision hint: what other domain this could be crossed with.
```

Aim for 10–20 cards, quality > quantity. Prefer 2025–2026 sources. Mark anything you could not verify. End your file with a "Top 3 from this front" section with 1-line reasoning each. Be brutally honest; no hype.
