# QCP Arena

**Read a problem. Write a quantum algorithm. Get a reproducible verdict.**

Three original problems, 382 public test cases, and one individual virtual round.
For students who already write Python and want to compete using Qiskit.

This effort is supported by Qollab & IonQ.

## Try the product

Open problem A. The editor contains a minimal `solve(n, oracle)` starter, not a
solution. Add your algorithm, use **Run examples**, then **Submit solution**.
The result shows exact ideal success probabilities, every test outcome, query
budgets and a counterexample when the circuit is wrong.

The editorial contains a reference solution after you attempt the problem.
During a virtual round it is hidden until the round ends. This is an honor-based
practice contest with public code; no anti-cheating claim is made.

## Run on Qollab

1. Download `releases/qcp-qollab.zip` from the repository and extract it.
2. Create a multi-file Qollab project and upload the extracted files. Keep
   `index.html`, `main.js`, `main.css`, `catalog.json`, `cases.json` and the `qcp/`
   package at the project root. Do not upload the outer repository folder.
3. Select a free local simulator and press **Run**.
4. Open problem A, edit the Python solution and press **Run examples** or
   **Submit solution**. The judge uses Qiskit's local ideal `Statevector`
   simulation; it does not call the remote IonQ API or require credentials.
5. Verify that the mode reads **Qollab · Qiskit Statevector** and that reports
   identify Qiskit as their execution source.

The ZIP's `main.js` contains the Qollab Python bridge plus the UI. The source
folder's `main.js` is the browser entrypoint; `tools/package_qcp.py` creates the
Qollab entrypoint explicitly. No API keys are required.

**Live Qollab upload/execution has not yet been verified for this project.** The
Python judge and browser workflow are tested locally; those are distinct claims.

## The three problems

| Problem | Task | Tests | Quantum/classical comparison |
| --- | --- | --- | --- |
| A. The sealed switchboard | Recover a hidden parity string | 124, exhaustive at n=2..6 | 1 quantum query versus n classical queries for exact recovery |
| B. The factory inspector | Decide constant versus balanced | 134; exhaustive tables at n=2,3; seeded larger tables | 1 quantum query versus up to 2^(n-1)+1 deterministic classical queries |
| C. One marked address | Find the unique marked address | 124, exhaustive at n=2..6 | O(sqrt(M)) quantum versus Θ(M) randomized classical queries for fixed high success |

All comparisons use the stated coherent-oracle model. They do not include input
loading or oracle construction, and they are not CPU/QPU wall-clock benchmarks.
For B, randomized classical algorithms also need few queries with bounded error:
there is no exponential separation from every classical method.

BV and DJ require success at least `1 - 1e-9`; Grover requires at least `0.90`.
The judge marginalizes the oracle-target qubit and evaluates the input register.
Measurements are added conceptually by the checker; user measurement instructions
are not supported in this edition.

## Browser and Vercel

The source folder is a static site. In Vercel, import this GitHub repository with:

- Root Directory: `qcp-qollab`
- Framework Preset: **Other**
- Build Command: empty
- Output Directory: `.`
- Environment variables: none

The public browser executes a bounded Python circuit builder in a worker using
Pyodide 0.28.3 from jsDelivr. It then runs an independent JavaScript ideal
simulator. **It does not install or run Qiskit.** Qollab uses the same builder and
fixtures with Qiskit instead. Every report labels the source.

The first browser execution needs internet to download Python. Worker startup
can be cancelled, and runtime/network failures do not add contest penalties.
There is no database, login, analytics, paid API or QPU account requirement.
Supabase is intentionally unnecessary for the scoped local demo.

Serving this folder over HTTP works; opening `index.html` as `file://` does not.

## Local development and CLI

From the repository root, with dependencies from `requirements-dev.txt`:

```sh
python tools/serve_qcp.py --port 8771
python tools/serve_qcp.py --port 8772 --browser
python tools/qcp_cli.py bv solution.py --examples
python tools/qcp_cli.py grover solution.py --report report.json
python -m unittest discover -s tests -p test_qcp.py -v
python tools/ui_test_qcp.py
python tools/package_qcp.py
```

The UI test expects both local servers. The port 8771 harness uses Qiskit; port
8772 exercises the actual Pyodide browser runtime. The CLI evaluates solutions
through the same bounded builder; it does not execute arbitrary user Python.

## Language and evaluation

The editor supports a documented Python/Qiskit circuit-building subset:
`solve(n, oracle)`, assignments, bounded `for`, `if/else`, `return`, lists,
indexing, basic arithmetic, supported math functions and standard gate calls.
Supported imports: `from qiskit import QuantumCircuit` and `import math`.
Arbitrary Python, helper functions, custom modules, `initialize`, arbitrary
unitaries, direct statevector access and user measurements are outside this
edition. The Judge specification tab lists the supported operations.

There is no user `exec` or `eval`. The interpreter produces a symbolic gate list;
oracle secrets are inserted by the evaluator after building. Public browser
assets are inspectable, so this models black-box access for practice rather than
cryptographically hiding secrets from a browser owner.

Limits: 2..6 input qubits plus one target, 512 instructions, logical depth 256,
12,000 interpreter steps per input size and 16,000 source characters. Logical
oracle depth is one; Qiskit reports a separate u/cx decomposition of the first
fixture with fixed optimization level 0 and seed 19, including oracle construction.

Verifying all listed fixtures is not a proof for untested sizes. No noisy-device
performance, quantum advantage on the simulator or universal circuit-equivalence
proof is claimed.

## Virtual round

Round 001 lasts 60 minutes on the local device. Standings use solved count, then
elapsed minutes plus 20 minutes for each rejected judged submission before the
first Accepted. CE, judge failures, cancellations and Run examples add no penalty.
Drafts, receipts and the timer survive reload using local storage. A new round
has its own submissions while previous practice history remains available.

There is one local participant, no global rating and no trusted server ranking.
A shared competition would need server-side judging, an isolated runner and
authoritative clocks/results; those are deliberately later milestones.

## Why this can grow

The initial product is the problem/judge/editor loop. A first pilot could put it
in a university algorithms or quantum-computing course, measuring first-Accepted
time, completion and return visits. Possible customers are course organizers and
contest sponsors; neither demand nor recruitment value is validated yet.

## References and attribution

The algorithms are established science; the original contribution here is the
problem content, bounded builder, checkers, dual execution paths and contest UI.

- [IBM: quantum query algorithms](https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/quantum-query-algorithms)
- [IBM: Deutsch–Jozsa](https://quantum.cloud.ibm.com/learning/en/modules/computer-science/deutsch-jozsa)
- [IBM: Grover and oracle assumptions](https://quantum.cloud.ibm.com/learning/en/modules/computer-science/grovers)
- [QCoder: existing competitive quantum programming platform](https://www.qcoder.jp/en/qa)
- [Pyodide](https://pyodide.org/)

Built with AI assistance. Code and original content are MIT licensed.
