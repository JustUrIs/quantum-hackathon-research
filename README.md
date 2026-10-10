# Quantum experiments you can question

Four projects for the Qollab × IonQ hackathon. Each experience makes a quantum idea tangible and exposes the assumptions behind its result.

**This effort is supported by Qollab & IonQ.**

**[Try the three interactive browser previews](https://justuris.github.io/quantum-hackathon-research/)** — no account or installation required. These use analytical browser calculations and precomputed Qiskit references; they do not run Python or submit quantum jobs. Download the full Qollab projects below to execute their circuits.

| Project | The experiment | Source / project page | Upload package |
|---|---|---|---|
| IMPOSTOR | Try to reproduce constrained quantum-game correlations | [Existing project](impostor-qollab/README.md) | `impostor-qollab/` |
| LOST SIGNAL | Compare sensor precision, then let noise choose the winner | [Project and physics](lost-signal-qollab/README.md) | [ZIP](releases/lost-signal-qollab.zip) |
| Q-DAY CLOCK | Tell genuine order finding from an imitation given the answer | [Project and algorithm](qday-clock-qollab/README.md) | [ZIP](releases/qday-clock-qollab.zip) |
| ORDER | Swap questions, inspect QQ, and audit your own AB/BA counts | [Project and evidence](order-qollab/README.md) | [ZIP](releases/order-qollab.zip) |

## Run the three new projects locally

Requires Python 3.11+ with Qiskit 2.5.2. Tested here with Python 3.13.

```sh
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python tools/serve.py
```

Open [the local launcher](http://127.0.0.1:8766/). Each Qollab project is self-contained; the local server bridges JavaScript to Python for development. On Qollab, upload one project's files with `index.html` and `main.js` at the root. Do not open those files directly from disk.

```sh
python -m unittest discover -s tests -v
python tools/ui_test.py
python tools/benchmark_projects.py
python tools/package_projects.py
```

## What has been verified

Local checks cover physical identities, reversible arithmetic, independent probability calculations, explicit classical baselines, count decoding, input validation and browser interactions at desktop and mobile widths. [Exact benchmarks](artifacts/benchmarks.json), [browser results](artifacts/ui-results.json), and local backend evidence in `artifacts/` preserve the source of each result. [Validation report](research/07_VALIDATION.md).

**Qollab/Pyodide and remote IonQ execution are not yet verified.** The projects follow Qollab's documented bridge and one-job model. Local execution and a GitHub push do not replace publication, the public video or the captain's final submission.

## See the interfaces

[LOST SIGNAL demo](https://justuris.github.io/quantum-hackathon-research/lost-signal/) · [Q-DAY CLOCK demo](https://justuris.github.io/quantum-hackathon-research/qday-clock/) · [ORDER demo](https://justuris.github.io/quantum-hackathon-research/order/).

The public previews pass 100 numerical reference comparisons, mobile layout checks and export provenance checks. Rebuild with `python tools/build_previews.py` and verify with `python tools/test_previews.py`. After a UI-only change, `--ui-only` reuses the existing reference data; regenerate fully after changing any scientific model. GitHub Pages serves `main:/docs`.

[LOST SIGNAL](artifacts/lost-signal-desktop.png) · [Q-DAY CLOCK](artifacts/qday-clock-desktop.png) · [ORDER](artifacts/order-desktop.png). Mobile screenshots are alongside them. Every export distinguishes local calculations from a captured backend snapshot.

## Delivery and story

- [Entrega: pasos y pendientes](launch/00_ENTREGA.md).
- [LOST SIGNAL: guion de 2:30, objeciones y piloto comercial](launch/01_LOST_SIGNAL_PITCH.md).
- [Q-DAY CLOCK: guion de 2:30, objeciones y piloto comercial](launch/02_QDAY_PITCH.md).
- [ORDER: guion de 2:30, objeciones y piloto comercial](launch/03_ORDER_PITCH.md).
- [Contexto reconstruido y correcciones al brief](research/06_BUILD_DECISIONS.md).

The original idea research remains under `research/`. Treat its unverified forecasts and novelty claims as historical proposals; the project READMEs document the implemented scope. Quantum metrology, order finding and quantum cognition all have substantial prior work. These projects offer educational experiments and audit tools, not new scientific theorems or demonstrated commercial quantum advantage.

MIT-licensed project code. Existing IMPOSTOR work supplied the bridge pattern; the three new engines, interfaces and launch materials extend the repository during the hackathon, with AI assistance. External sources and data provenance are credited in each project.
