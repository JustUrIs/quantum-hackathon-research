# Validation record: LOST SIGNAL, Q-DAY CLOCK, ORDER

Date: 2026-10-10. Environment: Windows, Python 3.13.5, Qiskit 2.5.2, NumPy 2.5.3. Scope is local execution unless explicitly stated otherwise.

## Executed checks

| Check | Result | Evidence / reproduction |
|---|---|---|
| New mathematical and engine tests | **22 passed** | `python -m unittest discover -s tests -v` |
| Existing IMPOSTOR engine checks | **14 passed** | From `impostor-qollab/`: `python -m tests.test_impostor` |
| Three browser experiences | **Passed** | `python tools/ui_test.py`; `artifacts/ui-results.json` |
| Responsive widths | **390, 768, 1440 px, no horizontal overflow** | Desktop/mobile screenshots under `artifacts/` |
| Browser JS errors | **None during tested flows** | Browser test captures `pageerror` |
| Backend failure injection | **Passed for all three** | `python tools/ui_failure_test.py`; null backend evidence after a simulated outage, one submission only |
| Actual local backend jobs | **1,024 shots each** | `artifacts/*-local-backend.json`, clearly labeled BasicSimulator |
| IonQ format serialization | **Passed offline for defaults** | `python tools/check_ionq_format.py`, optional `qiskit-ionq==1.0.2`; `artifacts/ionq-format-check.json` |
| WMM implementation reference | **Three NOAA values within 0.15 nT** | `python tools/generate_route.py` checks published WMM2025 points before generating the route |
| JavaScript syntax | **Passed** | `node --check` on three entrypoints and runtime template |
| Upload packages | **9–10 files each; every file below 2 MB; valid ZIP CRCs** | `python tools/package_projects.py`; SHA-256 manifest in `releases/manifest.json` |
| Git whitespace | **Passed** | `git diff --check` |

The 14 existing IMPOSTOR checks are a regression run, not an independent scientific review of all its claims.

## Numerical findings

Full machine-readable output: `artifacts/benchmarks.json`.

LOST SIGNAL at N=4, η=0.08, M=256: independent σφ = 0.0338527 rad; GHZ σφ = 0.0215176 rad; gain = **1.57326×**. Equality occurs at η = **0.231049**. At 26 μT, toy molecular angular contrast is **0.139674** with anisotropy and below **4×10⁻¹⁵** without it. The tests also reproduce the noisy parity formula with a separate density-matrix/Kraus implementation.

| Q-DAY input | Ideal recovery | Uniform phases | CX gates in this implementation |
|---|---:|---:|---:|
| N=15, a=2 | 50.000% | 21.875% | 111 |
| N=21, a=2 | 28.799% | 9.375% | 10,137 |
| N=33, a=2 | 0% | 0% | 27,675 |
| N=33, a=5 | 29.101% | 6.250% | 27,885 |
| N=35, a=2 | 11.476% | 3.125% | 25,617 |

General truth-table synthesis is expensive. These counts support an educational comparison, not an efficient arithmetic claim. For N=15 the public algebraic rotation optimization reduces the cost; it does not receive the order. Complete controlled-basis tests include unused work-register states and both control values. Independent Fourier-coset distributions agree to <1.4×10⁻¹³ on the listed cases. The pre-solved imitation matches the ideal output by construction.

ORDER defaults: yes-to-A is **90.9576%** when first and **64.0083%** when second. q is zero to floating-point precision. Inserting a 65° rotation gives q ≈ **−0.851651**. The classical contextual construction matches the synthetic distributions to <6×10⁻¹⁷. The separate questionnaire auditor passes validation and interval checks on aggregate counts; it is not fitted to the published survey proportions.

## Issues found and resolved

- A narrow layout overflow appeared after the backend button changed to a longer status. Grid children now shrink and button labels wrap. All viewport checks passed afterward.
- The initial generic N=15 arithmetic needed 1,703 CX gates. A valid public modular-rotation identity reduces this to 111, without a period/factor oracle. New basis and distribution checks verify the optimization.
- A test initially assumed every coprime base would factor successfully. N=33, a=2 disproved that assumption. The app now exposes base selection and the genuine failure case; tests preserve both failing and succeeding bases.
- Direct angle changes could leave an action label stale. Labels now derive from the rendered state.
- The export originally omitted the planning clock's assumptions. Exports now include that scenario and any completed questionnaire audit alongside model and backend snapshots.
- The initial proposal overstated QQ's exclusivity, novelty and navigation readiness. Current documentation and UI correct those claims and recognize prior work.

## What remains unverified

The public browser reference previews are an additional delivery surface. `python tools/test_previews.py` passed **100 numerical comparisons** (26 LOST SIGNAL, 38 Q-DAY CLOCK, 36 ORDER), checked widths 390/768/1440, disabled backend execution, export provenance and zero browser exceptions. Q-DAY comparisons use the generated Python/Qiskit fixtures; they verify browser presentation and ablation, not an independent reimplementation of order finding. ORDER's browser p-value approximation agrees within 2e-7 in the tested cases. Full results: `artifacts/preview-results.json`.

On 2026-10-10 GitHub Pages completed deployment of commit `ad538312dbc4b849ba4def1c7a5a47834fe22cf5`. The same 100 comparisons passed against the public HTTPS site, with HTTP 200 for all pages (`artifacts/preview-live-results.json`). All three public ZIP downloads matched the local packages by SHA-256. Set `TEST_PREVIEW_URL=https://justuris.github.io/quantum-hackathon-research` when running the preview test to repeat the external check. This deployment is separate from Qollab publication.

No live Qollab/Pyodide execution, remote IonQ job, hardware run, field navigation test, biological validation or externally validated survey study occurred in this session. The offline IonQ serializer confirms accepted instruction encoding only; it does not validate cloud acceptance, native compiled gate limits, noise or queue completion.

The CUA environment reported **no browser available**, so authenticated Qollab UI actions could not proceed. Public Qollab docs were read over HTTP to check `.callPromising`, relative JS imports, injected backend use, one-job limits and gate compilation behavior. The provider is passed from `main.js` into the helper module rather than relying on its global visibility inside imports.

The publication/video/final-submission procedure is in `launch/00_ENTREGA.md`. Do not describe those steps as done until their external state is verified.
