# QCP Arena: 2–3 minute demo

Suggested theme: Quantum Unlocked, because the central contribution is a
reproducible learning and competition workflow. Quantum Playground is an
alternative if organizers classify competitive programming there. Theme
placement is a proposal, not an organizer-confirmed decision.

## Pitch

Competitive programmers learn by solving problems and getting precise feedback.
Quantum students should have that same loop. QCP Arena supplies three complete
oracle problems, a circuit-building editor, 382 public tests and a virtual round.
The judge checks the probability of a correct answer rather than rewarding a
lucky measurement. Every comparison states which classical baseline applies.

## Show, in this order

1. Open A and read the task: recover all switch positions with one oracle query.
   Explain that the hidden string is not provided to the submitted function.
2. Run the unmodified starter. Show Wrong Answer and the public counterexample.
3. Write/load the solution from the editorial. Submit it and show 124/124 checks.
   Open resource metrics: one oracle call for every tested input size.
4. Remove the target's X preparation. Submit again: missing phase kickback fails.
5. Open C, run its reference and show 94.53125% success on the n=3 sample.
   Explain that the success threshold is checked exactly, not through a lucky shot.
6. Start a virtual round and show solved count/penalties. Identify it as local
   virtual participation, not a live global league.
7. Show the Qollab edition evaluating a solution with Qiskit. Only show this step
   after confirming that the project actually runs on Qollab.

End: The next test is a course or programming club using this workflow. We are
testing whether rigorous problems and fast feedback help students return and
learn; we have not validated those outcomes yet.

## Publication handoff

- Upload `releases/qcp-qollab.zip`, publish MIT and confirm Run/examples/Submit.
- Vercel root is `qcp-qollab`, Other preset, no build command, output `.`.
- Record a public 2–3 minute video viewable without login.
- Captain submits the public Qollab project from the team page.
- Vercel is deployed at https://qcp-arena.vercel.app and connected to GitHub.
  A real public submission passed 124/124 cases; the missing-preparation variant
  returned WA. A Qollab authenticated session is still needed for platform checks.
- Full pitch, next-agent prompt and film-production brief: `qcp-handoff/`.
