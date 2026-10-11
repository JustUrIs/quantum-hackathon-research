# Quantum experiments you can question

**Five independent Qollab projects, led by Guardia Grid.** Each makes a quantum idea tangible and exposes the assumptions behind its result.

**This effort is supported by Qollab & IonQ.**

[Try the interactive browser previews](https://justuris.github.io/quantum-hackathon-research/) — no account or installation required. The previews do not run Python or submit quantum jobs. Download a full project package to run its Qiskit circuit on Qollab.

| Project | The experiment | Project page | Qollab upload package |
|---|---|---|---|
| **GUARDIA GRID · CABA** | Robust emergency-capacity planning with public injury-crash signals; QAOA, classical baselines and single-site outages | [Main project](ambulancias-qollab/README.md) | [ZIP](releases/ambulancias-qollab.zip) |
| IMPOSTOR | Reproduce constrained quantum-game correlations | [Project](impostor-qollab/README.md) | [ZIP](releases/impostor-qollab.zip) |
| LOST SIGNAL | Compare sensor precision, then let noise choose the winner | [Project and physics](lost-signal-qollab/README.md) | [ZIP](releases/lost-signal-qollab.zip) |
| Q-DAY CLOCK | Tell genuine order finding from an imitation given the answer | [Project and algorithm](qday-clock-qollab/README.md) | [ZIP](releases/qday-clock-qollab.zip) |
| ORDER | Swap questions, inspect QQ, and audit AB/BA counts | [Project and evidence](order-qollab/README.md) | [ZIP](releases/order-qollab.zip) |

## Run locally

Requires Python 3.11+ with Qiskit 2.5.2.

```sh
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python tools/serve.py
```

Open [the local launcher](http://127.0.0.1:8766/). The local harness bridges JavaScript to Python and uses BasicSimulator. It is a development check, not Qollab or IonQ evidence. On Qollab, upload one project's files with `index.html` and `main.js` at the root. Keep its Python package and data folder.

```sh
python -m unittest discover -s tests -v
python tools/ui_test.py
python tools/benchmark_projects.py
python tools/package_projects.py
```

## Guardia Grid

Guardia Grid is the lead submission: a concrete capacity-planning question, built from public Buenos Aires City data, with explicit uncertainty and a quantum circuit judges can run. It is a scenario-planning demonstrator, not a dispatch recommendation or evidence of quantum advantage. Its [README](ambulancias-qollab/README.md) explains the method, data provenance, limitations, Qollab run steps, and the next operational datasets needed for a credible pilot.

The other four projects remain independent submissions with distinct questions and demos.

## Evidence and delivery

The repository's saved browser screenshots and local backend artifacts are labeled with their source. **Qollab/Pyodide and remote IonQ execution must be verified on Qollab before claiming those results.** A local calculation, ZIP, or GitHub push does not replace the project publication, public 2?3 minute video, or the captain's final team submission.

- [Delivery checklist](launch/00_ENTREGA.md)
- [Guardia Grid judge demo script](launch/06_GUARDIA_GRID_PITCH.md)
- [Project pitches and demos](launch/)
- [Validation report](research/07_VALIDATION.md)

All project code is MIT-licensed. Dataset licenses and attribution remain separate and are listed per project. Work was prepared with AI assistance.
