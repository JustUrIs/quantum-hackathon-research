# DARKROOM execution and teaching evidence

The user confirmed on 2026-10-11 that the project loaded and its ideal calculation ran in Qollab. Their selected-provider attempt failed in `qiskit_ionq` while `requests.post` used Pyodide/urllib3's browser fetch bridge: `TypeError: Failed to fetch`. This is evidence of a failed provider connection, not evidence that six-qubit circuit simulation failed. The trace does not identify whether CORS, connectivity, provider access, or another browser/network condition caused it.

The revised project adds an explicit Qiskit BasicSimulator measurement in the Python runtime, with no remote-provider call. Source labels distinguish this from the selected backend. Both the local measured path and a simulated selected-provider failure have been verified in the local development harness. The new local path still needs a user run in Qollab/Pyodide before that environment is marked verified.

Five Python checks cover all analytic/statevector outcomes for 2–6 cycles, outcome normalization, invalid inputs, count classification, and local measured distributions/source labeling. The browser integration check runs both lesson languages, the two-cycle empty/present traces, four correct concept answers, mobile sizing, source/settings snapshots, a selected-backend network failure, and subsequent local measurement.

The four-question quiz checks specific concepts. There is no completed learner study, adoption evidence, or demonstrated improvement in learning outcomes. A user's quiz answers and own-word explanation can help identify remaining teaching problems; they are not a controlled efficacy result.
