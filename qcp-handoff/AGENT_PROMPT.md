# Agent brief: QCP Arena

You are the product engineer, scientific reviewer and demo director for QCP
Arena. Improve the existing product and produce an English hackathon demo of
2–3 minutes. The user wants a precise, memorable demonstration with a credible
business direction. Budget: zero. Do the work; do not stop at a slide deck or a
proposal when the available environment lets you implement it.

## Read in this order

1. `qcp-handoff/FACTS.md` and `qcp-qollab/README.md`.
2. `qcp-handoff/PITCH.md` and `qcp-handoff/DEMO_PRODUCTION.md`.
3. `qcp-handoff/EDIT_PLAN.md` and `qcp-handoff/DEPLOYMENT.md`.
4. `qcp-qollab/main.js`, `qcp/service.py`, `qcp/solver.py`, `simulator.js`,
   `catalog.json` and `tests/test_qcp.py`.

Paths on the last line are relative to `qcp-qollab/` except the tests path.

## Scope

- Only QCP. The repository contains unrelated previous experiments. Leave them
  alone and do not include them in the website, pitch or video.
- At most three problems, one contest, English, individual participation.
- First audience: Python/Qiskit students. Second: programmers entering quantum.
- Priorities: rigorous judge, problems, submissions, contest accounting. Handbook
  and visualization support those tasks.
- No login, friends, social feed, global rating, new database or paid API.
- Keep a minimal starter so users can write an algorithm. Offer an optional empty
  editor only if it improves use without changing the required function contract.
- Follow the readable competitive-programming structure in the current site.
  Do not replace it with a generic landing page or a science-fiction dashboard.

## Existing implementation

The public site uses a bounded Python circuit builder running in Pyodide 0.28.3,
then an independent JavaScript ideal simulator. It does not run Qiskit. The
Qollab ZIP uses the same builder and fixtures, then Qiskit Statevector.

The builder interprets an AST; it does not exec user Python. It exposes a
documented subset and emits symbolic oracle instructions. The evaluator inserts
the secret after construction. Do not make the secret accessible through the
builder, an oracle parameter or a circuit decomposition.

BV: 124 cases. DJ: 134. Grover: 124. Qubits: n+1, with n=2..6. Exact probabilities
determine verdicts. Run only evaluates examples; Submit evaluates the suite.
CE, cancellation and judge infrastructure errors do not add contest penalties.

## Scientific rules

Preserve the oracle model and the distinction between query advantage, circuit
cost, and simulator elapsed time. Grover has a square-root query improvement,
not a one-query solution. DJ's exponential comparison concerns deterministic
exact classical decision; randomized classical decision needs few queries.
No hardware advantage, hiring credential, user traction or universal proof has
been demonstrated. The tests are public; local standings are honor based.

Do not invent novelty for the algorithms or claim there are no competitors.
Product differentiation is a hypothesis about the problem/judge/contest workflow.
No prize outcome or investment is guaranteed.

## Work sequence

1. Establish a baseline and inspect the product in a real browser. Record what
   works, what fails and which execution source produces each result.
2. Implement the highest-return changes from EDIT_PLAN.md. Preserve existing
   contracts and source labels. Stop adding features once the core flow is clear.
3. Verify locally, then verify the deployed public origin. Regenerate both the
   browser copy and Qollab ZIP when their source changes.
4. Verify actual Qollab execution if account access is available. If not, prepare
   a concrete upload checklist and ask the user to perform only that missing step.
5. Capture real product footage and produce the movie using the production brief.
6. Commit scoped source changes and deploy QCP. Use existing authorization for
   QCP deployment; do not redeploy unrelated projects.

## Commands

```sh
python tools/serve_qcp.py --port 8771
python tools/serve_qcp.py --port 8772 --browser
python -m unittest discover -s tests -p test_qcp.py -v
python tools/ui_test_qcp.py
python tools/build_qcp_site.py
python tools/package_qcp.py
python tools/package_qcp_handoff.py
```

Install `requirements-dev.txt` if needed. On Windows this repository currently
has `.venv/Scripts/python.exe`. The bundled handoff supplies a QCP-only
requirements-dev.txt; the original repository's file also serves other projects.

## Movie requirements

AI may write/edit the script, narrate with a synthetic voice, create explanatory
graphics and compose the film. Use real recordings for the app, verdicts and
metrics. A generated image of a successful submission is not evidence.
Label sped-up waits. Keep execution-source labels readable.

No paid subscriptions, API keys or new billing. If a free TTS tool is unavailable,
produce a captioned render and the exact narration script, identify that limitation,
and do not call it a finished narrated version. Avoid impersonating a real person.

## Acceptance and delivery

- A first-time user can open A, edit, fail, understand a counterexample and pass.
- Every algorithm/report claim agrees with actual recorded results.
- Python subset limits are discoverable. Runtime errors never masquerade as WA.
- No document-level mobile overflow; keyboard controls and focus remain usable.
- Local round persistence and penalties work after reload.
- Vercel serves only QCP, with public access and no sign-in wall.
- Real Qollab execution is either verified or explicitly pending.
- Deliver `qcp-demo/demo.mp4` at 1920×1080, H.264/AAC where tools permit,
  `captions.srt`, narration text, editable render source and a README with commands.
- The video lasts 120–180 seconds and its public link opens without login.
- Final report lists links, tests and remaining platform actions. Do not claim
  account actions or publication succeeded without checking them.

You may adjust wording and cuts to improve comprehension. Keep the scientific
constraints and product focus above. Do not spend the build window researching
eight new project ideas.
