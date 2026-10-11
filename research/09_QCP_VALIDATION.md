# QCP Arena validation

Date: October 11, 2026. Local evidence, not live Qollab/IonQ evidence.

## Implemented scope

Three problems and one individual, 60-minute virtual round. English, no login,
database, paid API or external QPU credentials. Original problem cards, bounded
Python builder, Qiskit local checker and independent browser ideal simulator.

## Verified locally

- `python -m unittest discover -s tests -p test_qcp.py -v`: 9 checks passed,
  44.117 seconds in the recorded run. The three reference solutions pass all
  382 cases: BV 124, DJ 134, Grover 124.
- Incorrect starters fail. Missing phase kickback fails. A BV circuit does not
  solve the equality-oracle problem. Exceeding query limits is rejected.
- Syntax/module/introspection/decorator/while examples do not execute as user
  Python. Width, gate, instruction and interpreter step limits produce errors.
- `python tools/ui_test_qcp.py`: passed on localhost Qiskit and actual Pyodide
  browser execution. Verified all three reference submissions, all-test display,
  report download, saved drafts, timer reload, editorial locking and round scoring.
- CE and example runs did not add penalties; WA before AC added 20 minutes.
- 40 seeded circuits containing every supported gate family were checked
  against Qiskit. Maximum probability difference: 9.43689570931383e-16.
- Mobile viewport 390×844 had no document-level horizontal overflow. Desktop
  and mobile screenshots were inspected.
- Browser Python uses pinned Pyodide 0.28.3; the runtime was actually downloaded
  and used in Chromium. The browser does not install Qiskit.
- Public GitHub Pages deployment at `/quantum-hackathon-research/qcp/` returned
  HTTP 200. A real browser/Pyodide submission of A's reference passed 124/124
  cases from that HTTPS origin after commit efb2002.
- A focused runtime-download failure test returned JE and left the virtual-round
  penalty at zero. Infrastructure failures are separate from student errors.

The Python/Qiskit reference checks and JS comparisons use local ideal simulation.
They do not establish performance or correctness on noisy hardware.

## Remaining external actions

- Upload the ZIP to Qollab and confirm the Python bridge, examples and submissions
  in the real platform. Its `main.js` is packaged with a direct Python service
  import; the catalog is loaded through that service rather than browser fetch.
- Record the public demo video and submit the public MIT Qollab project.

## Vercel production verification

Production https://qcp-arena.vercel.app, project `qcp-arena`, root `qcp-qollab`.
GitHub connection succeeded. A clean unauthenticated browser reached HTTP 200,
submitted A's reference and obtained AC / 124 of 124. Removing the target
preparation returned WA. A legacy project URL returned 404. The CLI dry run
included only the 15 QCP source files; local environment and other project files
were excluded. Account metadata is ignored and absent from public handoff ZIPs.

## Claims deliberately bounded

Tests are public. The virtual contest is local and honor based. The browser's
result storage, timer and code can be changed by its owner. No trusted global
rating, inaccessible test set, universal Python sandbox or proof for untested
inputs is claimed. Query comparisons assume coherent black-box access; data
loading and oracle construction are separate costs. DJ's exponential comparison
is against exact deterministic classical algorithms, not randomized methods.
