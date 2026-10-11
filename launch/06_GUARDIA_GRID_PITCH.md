# GUARDIA GRID · CABA — 2:30 judge demo

## Spoken script

**[0:00 · show the map]**

Emergency-response planners have to place limited standby capacity before calls arrive. Historic hotspots help, but a plan can look strong and still depend on one location staying available. Guardia Grid turns that planning question into an inspectable Qiskit experiment: with a fixed number of hypothetical staging points, how much past injury-crash signal is covered, and how does coverage change when one selected point goes offline?

**[0:20 · change demand slice and fleet size]**

This is Buenos Aires City. The bundled signal contains 61,784 unique injury-crash events from the city's published 2019–2025 records, filtered against its census-radio geography. They are not all 107 calls, ambulance trips, or response times. The eight candidate points are representative census-radio locations, not verified depots or approved lots. The map uses straight-line distance, not road travel time.

**[0:48 · adjust outage weight; point to scorecards]**

The objective blends weighted historic signal coverage with the average coverage after removing each selected location in turn. You can change the fleet size, radius, time slice, severity weighting, and outage emphasis. Every method receives the same inputs: sequential greedy, greedy plus one-site swaps, exact search, and QAOA. With three units, exact search checks all 56 valid combinations.

**[1:15 · point to QAOA card; open circuit details]**

The circuit uses eight qubits. It starts in a fixed-Hamming-weight Dicke state, applies a two-layer XY mixer, and phases the complete robust objective. This keeps exactly the requested number of locations without penalty qubits. The local ideal statevector is an optimizer reference, not a hardware measurement. In this default scenario, the best exact plan scores 36.0% of the weighted signal and the most-likely ideal QAOA state scores 34.2%. We show the gap rather than hiding it.

**[1:48 · select the free Qollab simulator; run once]**

On Qollab, this button submits the same measured circuit to the selected simulator and reports backend counts separately. The local development run is labeled BasicSimulator; it is not evidence from IonQ hardware. There is no claim of quantum speedup, and the eight-site instance is intentionally small enough for exact audit.

**[2:10 · show pilot hypothesis]**

The product hypothesis is a planning workbench that lets an operations team stress-test candidate coverage and failure scenarios. A credible pilot needs de-identified 107/SAME calls, dispatch and arrival timestamps, actual available units, approved base locations, and a road-time model. We would compare against current positioning and integer optimization on held-out dates, measuring missed demand and worst-area travel time before anyone considered operational use.

Guardia Grid makes the assumptions visible, keeps the classical answer in the room, and gives quantum optimization a concrete question it has to earn its place on.

## Capture checklist

- Use a clean Qollab run with the bundled default fixture and the free simulator.
- Show the four scorecards, then vary the fleet size and outage weight.
- If you capture a backend job, show its backend name and shot count; do not call a local BasicSimulator run an IonQ result.
- Keep the demo public without a sign-in wall and between two and three minutes.
- Disclose AI assistance and describe the current result as a prototype. Do not imply SAME validation, dispatch deployment, saved response times, or quantum advantage.

## Mentor questions

1. For robust maximum coverage with a fixed fleet and a single-site outage term, is the XY ring mixer a defensible starting point, and what small-instance diagnostic would you use before increasing the candidate count?
2. Which operational objective would make a pilot most useful to dispatch planners: expected missed calls, worst-neighborhood travel time, or a distribution over unit outages?
3. What minimum de-identified fields and validation protocol would you require before comparing candidate staging plans against current practice?
