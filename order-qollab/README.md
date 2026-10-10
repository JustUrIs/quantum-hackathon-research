# ORDER

**You can change the answer without changing a word.**

Swap two questions and watch a synthetic belief model change its response. Explore the QQ symmetry, break one of its assumptions, compare published survey proportions, and invite a classical model to match the result. Then audit aggregate counts from your own randomized AB/BA experiment.

**This effort is supported by Qollab & IonQ.**

## Try it in one minute

1. Run the JS project on Qollab's free built-in simulator.
2. Press **Swap the question order**. At the initial settings, yes-to-A changes from about 91.0% to 64.0% in the synthetic model.
3. The **QQ difference stays zero** even though the marginal response changes.
4. Insert new information between the measurements. The simple QQ prediction can fail.
5. Inspect the published **Rose / Jackson** example, where inserted information matters.
6. Press **Let a classical model match it**. It succeeds. QQ is a useful model constraint, not proof of a quantum brain.
7. Run the six-qubit backend check once and export its counts. Or paste your own aggregate AB/BA counts into the questionnaire auditor.

The guided experiment walks through the central story. Real survey data, synthetic model outputs and backend samples remain separately labeled throughout.

## Mathematics and circuits

A real-valued qubit state `RY(θ)|0⟩` represents a synthetic initial belief. Question A uses basis angle 0; B uses angle β. Each question applies a basis rotation, a CNOT to a fresh answer register, and the inverse rotation. Keeping those records preserves the sequential projective-measurement probabilities. We measure only at the end.

For one order, three qubits represent one state and two answer records. **Two orders occupy six qubits and four classical output bits in one job.** Answer 0 means yes. All displayed joint cells use the same canonical order: AyBy, AyBn, AnBy, AnBn, including when the questions occur BA. This prevents accidental transposition errors.

```
q = P(AyBn | AB) + P(AnBy | AB)
  − P(AyBn | BA) − P(AnBy | BA)
```

The simple projective model with the same initial state and no inserted transformation predicts q = 0. An intervening rotation can violate that prediction. Compatible measurements provide a zero-order-effect control. Tests compare deferred circuits with direct projector formulas over multiple states and bases.

## A classical model that can win

The challenger explicitly constructs a context-sensitive stochastic machine. It stores whether A or B was asked first and uses six conditional probabilities: the first-question marginals and the two transitions after each possible first answer. It reproduces the displayed synthetic distributions, including QQ when present.

This is a saturated in-sample fit, not out-of-sample predictive evidence. Its role is to refute a claim of uniquely quantum explanation. Classical probability with contextual state changes can model order effects. Neither QQ nor an order effect demonstrates that brains physically implement quantum computation. A credible future comparison must evaluate held-out observations and model complexity.

## Published observations

`data/polls.json` transcribes the **Clinton/Gore** and **Rose/Jackson** aggregate tables from Wang et al. (2014), Table 1. It retains the original four-decimal proportions, including rounding totals such as 0.9999, rather than inventing exact counts or sample sizes.

| Dataset | q from rounded cells | Published QQ-test p | Interpretation |
|---|---:|---:|---|
| Clinton / Gore | −0.0032 | 0.91 | Near QQ symmetry despite an order effect |
| Rose / Jackson | 0.1514 | <0.001 | Inserted information violates a premise of the simple prediction |

The paper's main study includes 70 national surveys and two laboratory experiments; this app reproduces two illustrative aggregate tables, not all participants or studies. The comparison involves separate groups, not tracked individuals changing their opinions. The p-values above come from the paper and are not recalculated from rounded proportions.

## Use the questionnaire auditor

Randomly assign independent respondents to the two orders. Paste two rows of four **integer counts**, using AyBy, AyBn, AnBy, AnBn in both rows. The first row is AB, the second BA. The prefilled example is synthetic.

The auditor reports the change in yes-to-A, QQ difference, approximate 95% normal intervals and a two-sided pooled two-proportion QQ test. It flags expected binary counts below five. These calculations assume independent groups with unweighted observations; repeated respondents, clustering and survey weights require a different analysis. Failure to reject QQ is not evidence of a unique quantum mechanism. Only aggregate counts are needed, and Qollab computes them in its local Python runtime. The result joins the evidence export.

## Execution and reproducibility

Upload this folder's contents, preserving `orderlab/` and `data/`, with `index.html` and `main.js` at the root. `runtime.js` handles the shared bridge. There are no API keys, network data fetches or custom backend instances.

The check uses 100 shots for IonQ-named backends and 1,024 locally, in a single circuit. It stores the parameter snapshot and all counts. Its approximate QQ interval uses the per-shot difference of the two discordance indicators, retaining covariance between packed registers. Sparse or extreme counts can invalidate the normal approximation; the raw evidence is exported for reanalysis. These are circuit samples, not new survey data.

**Validation status:** local Qiskit and BasicSimulator tests pass; browser tests exercise interactions, count export and mobile layout. Live Qollab/Pyodide and remote IonQ execution still need verification. We do not claim a remote or hardware run.

From the full repository:

```
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python tools/serve.py
python -m unittest discover -s tests -v
python tools/ui_test.py
```

Open `http://127.0.0.1:8766/order/`. The local HTTP bridge does not ship in the Qollab package.

## Novelty, prior work and use

Suggested theme: **Quantum Playground**, also relevant to Unlocked. The contribution is a playable, falsifiable comparison: synthetic circuits, historical aggregate observations, a premise-breaking intervention, an explicit classical counterexample and a tool for your own randomized study.

Interactive order-effect demos already exist, including [Projections and Order Effects in Quantum Cognition](https://www.puttypeg.net/science/projectiondemo/). Quantum circuit representations of cognition also predate this project: [Quantum Circuit Components for Cognitive Decision-Making](https://arxiv.org/abs/2302.03012). We claim neither discovery of quantum cognition nor a first interactive visualization.

The next practical experiment is questionnaire quality assurance: preregister an AB/BA study, compare held-out predictions from constrained projective and classical contextual models, and measure whether the audit prevents a wrong conclusion. There is no validated political persuasion product, election forecast or customer traction here.

We reused the repository's IMPOSTOR bridge pattern and built this engine, interface and auditor during the hackathon with AI assistance. The cited theories, datasets and Qiskit predate the event. MIT license; source attribution accompanies aggregate data. Keyboard operation, named inputs, numerical alternatives to color and widths down to 390 px are covered. A public demo video and Qollab submission remain release steps.

## Sources

- [Wang et al. (2014), primary paper and Table 1](https://jbusemey.pages.iu.edu/quantum/PNAS2014.pdf).
- [Quantum circuit components for cognitive decision-making](https://arxiv.org/abs/2302.03012).
- [Qollab JS/Python bridge](https://qollab.xyz/learn/docs/js-qiskit-projects), [one-job runtime](https://qollab.xyz/learn/docs/runtime-environment).
