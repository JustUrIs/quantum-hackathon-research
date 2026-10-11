# Guardia Grid

**Move the plan before the call.** Guardia Grid is a Qiskit/QAOA experiment for scenario planning: compare eight hypothetical emergency-standby locations against historical CABA injury-crash signals, hold fleet size fixed, and account for one selected location becoming unavailable.

This is a planning demonstrator, not an ambulance dispatch product. It has not been reviewed by SAME or a public agency. Its bundled records describe road-injury events, not every 107 call, ambulance trip, patient, or response time. Candidate positions are census-radio representatives, not verified depots, lots, or legal staging locations. Straight-line catchments are not street routes. No patient or health records are included.

## Run on Qollab

Upload the contents of this folder to a new Qollab project. Keep `index.html` and `main.js` at its root and preserve `ambulancia/` and `data/`. Use the free local simulator. The app performs its ideal reference calculations in Qiskit's local statevector simulator.

To measure the same optimized circuit on the simulator selected in Qollab, press **Run QAOA on the selected Qollab simulator**. The app makes one backend call per project run. IonQ simulation uses 100 shots; the local backend uses 256. A failed job stays labeled as a failure. It is not replaced with local counts. IonQ results are a hardware-compatibility check, not a judging advantage.

The page lets you vary the historical time slice, number of units, distance catchment and how much the score should value the average loss from one unavailable site. It compares sequential greedy placement, greedy followed by one-site swaps, exact enumeration, and the most likely ideal QAOA basis state. The exact comparator evaluates all `choose(8,K)` subsets for the selected objective. A tiny problem is deliberate: this product measures sampler behavior and robustness rather than claiming a classical runtime victory.

## What QAOA optimizes

The score is a weighted combination of historical signal covered during normal service and the average score after removing each selected location in turn:

```text
score(S) = (1−ρ) coverage(S) + ρ mean[coverage(S without j) for j in S]
```

`ρ` is the user's one-location-outage weight. Every subset keeps exactly `K` locations: the circuit starts in a Dicke state of Hamming weight `K` and alternates the full diagonal cost unitary with an XY ring mixer. No penalty qubits distort the fleet size. The cost phase uses a diagonal lookup of the complete scored function for this eight-site instance, including the outage term. It does not truncate coverage to pairwise interactions. The offline classical optimizer minimizes the negative exact statevector expectation.

The displayed QAOA candidate is an ideal, local statevector prediction. The backend panel reports the measured counts from a separate, single Qollab job. Both go through the same decoder and objective, and both can lose to the classical methods. `P(optimum)` is measured per ideal QAOA circuit shot against the best classical score; it is not a speedup. Uniform random is included as `number of optima / number of feasible subsets`.

## Data and limits

`data/caba_signals.json` aggregates 61,784 unique injury-crash events, point-in-polygon filtered against the published census-radio polygons for CABA. The event table spans 2019–2025 and was updated by Buenos Aires City on July 14, 2026. Duplicate victim rows for one incident are collapsed by the incident identifier. The 2010 census-radio layer defines the historical geographic boundary mask and representative candidate points. Its population figures do not determine the demand score.

The 8×8 signal grid contains event count, severe/fatal count, nighttime count, and 2025 count. Default event index is `events + 2×severe + 5×fatal`. The night and recent modes use recorded subset counts; the severe mode uses `severe + 3×fatal`. These are transparent model weights. They are not fitted ambulance-call probabilities or patient counts. Source names, links, dates and distinct data licenses appear in [data/README.md](data/README.md).

At 40 km/h, a 3 km radius would imply roughly 4.5 minutes on an empty straight path. The app does not turn that calculation into a response-time claim: traffic, road geometry, one-way streets, dispatch, handover, availability and facility access are absent. It shows distance only. Census points are synthetic scenario locations. Input coordinates stay bundled; the app makes no network requests and needs no API key.

For a real pilot, request de-identified 107/SAME call coordinates, timestamps, dispatch/arrival timestamps, unit availability and approved staging sites from the relevant emergency-response authority; these operational records are not included here. Public starting points for facility and road-network layers are the [Buenos Aires City hospital catalog](https://data.buenosaires.gob.ar/es_AR/dataset/hospitales), the [Buenos Aires Province public-health establishments catalog](https://catalogo.datos.gba.gob.ar/dataset/establecimientos-salud), and a local [Geofabrik Argentina OpenStreetMap extract](https://download.geofabrik.de/south-america/argentina.html). Facility locations do not establish ambulance availability, and OSM-derived data requires ODbL attribution. Add time-dependent traffic only from a source whose permission and historical coverage have been verified.

## Reproduce the fixture and local checks

The development-time acquisition script uses only Python's standard library. It downloads the public source files into `tmp/ambulance-source/` and writes the small fixture to `data/`. Qollab never runs the downloader.

```sh
python ../../tools/build_ambulance_data.py
```

The standalone repository's development harness serves this project at `http://127.0.0.1:8766/ambulancias/` using local Qiskit BasicSimulator counts. Those counts must be labeled **BasicSimulator · local harness**; they do not verify Pyodide or IonQ. For a clean install, use the repository's `requirements-dev.txt`; this folder's `requirements.txt` lists the two project-specific packages.

## MIT and attribution

Project code is MIT; see [LICENSE](LICENSE). Historical event data is CC BY, and the source geography is CC-BY-2.5-AR. Each license remains attached to its own material; the source data is not relicensed as MIT. **This effort is supported by Qollab & IonQ.** Built during the hackathon with AI assistance, disclosed to the judges. City and Qollab/IonQ endorse neither the model nor any deployment recommendation.
