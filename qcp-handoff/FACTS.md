# Facts the next agent must preserve

## Shipped and tested

- Three original problem cards; five tested input sizes: n=2,3,4,5,6.
- BV: 124 secrets across those sizes, exhaustive.
- DJ: 134 tables; exhaustive n=2,3, sampled balanced tables for n=4,5,6.
- Grover: 124 marked addresses, exhaustive at those sizes.
- Total: 382 cases. Ideal probability thresholds: 1−10⁻⁹ for A/B, 0.90 for C.
- Grover's n=3 example: two iterations, 0.9453125 success probability.
- Python/Qiskit reference solutions pass the three suites locally.
- Nine local QCP tests passed. Browser/editor/contest checks passed.
- Forty gate-family comparisons differed from Qiskit by at most
  9.43689570931383e-16 in the recorded run.
- A browser submission from the public GitHub Pages origin passed 124/124 cases.
- Blocking the runtime download produced JE and zero contest penalty.
- Vercel production https://qcp-arena.vercel.app is public. Its real browser
  submission passed A's 124 cases; removing target preparation produced WA.
  The deployment serves the QCP root and is connected to GitHub.

## Execution paths

Browser: Python subset in Pyodide + independent ideal JavaScript simulation.
Qollab ZIP: same bounded builder/fixtures + Qiskit Statevector judge.
Local Qiskit harness: a development server, not a live Qollab session.

Qollab platform validation remains pending unless new evidence records an actual
upload and execution. Vercel status is in DEPLOYMENT.md and must be checked live.

## Comparisons

BV: exact recovery costs n classical oracle queries versus one quantum query.
DJ: the exponential gap is against exact deterministic classical decision;
randomized classical decision can use few queries with bounded error.
Grover: square-root query improvement for unstructured search at fixed high
success probability. Oracle construction/data loading are separate costs.

The CPU simulator has no claimed quantum wall-clock advantage. These algorithms
are established; competitive quantum programming platforms already exist.

## Not yet demonstrated

Student learning gains, retention, customers, revenue, global contest fairness,
noise resilience, hardware speedup or accelerator interest. Each is a future
validation task, not a number to put in the pitch.

The primary local record is `research/09_QCP_VALIDATION.md`. Source baseline:
implementation commit efb2002; public-check documentation commit 6927617.
