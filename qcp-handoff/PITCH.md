# QCP Arena pitch

## One sentence

QCP Arena lets you train and compete in quantum algorithms through programming
problems, reproducible verdicts and timed rounds.

## 30-second pitch

Competitive programmers learn by attempting a problem, submitting code and
understanding why it fails. We built that workflow for quantum algorithms.
In QCP Arena, you write Python, build a circuit and submit it to a judge that
checks the probability of a correct answer across public test cases. Our first
edition has three problems, 382 tests and a timed virtual round. You can practice
in a browser and run the Qiskit edition on Qollab. We want universities and
programming clubs to use it to train their next quantum competitors.

## 90-second pitch

You can read a quantum algorithm and still struggle to implement it. A circuit
can look plausible while missing the operation that makes its answer correct.
Students need a way to attempt a task, inspect a failure and try again.

We built QCP Arena for that workflow. You read a programming problem, implement
solve in Python, run the examples and submit. The judge checks ideal answer
probabilities and resource budgets. When you fail, you can inspect a
counterexample. When you pass, you can see which cases and constraints you met.

Our first problem asks you to recover a hidden parity string with one oracle
query. Remove the target preparation and the solution fails. Restore it and
the reference passes 124 cases. Our search problem checks Grover's success
probability instead of rewarding a lucky measurement. The complete edition has
three problems, 382 tests and one virtual round.

The browser edition runs a Python builder and an ideal simulator. The Qollab
edition uses Qiskit. We label both paths and separate oracle-query improvements
from simulator speed.

Our next step is a pilot with a quantum course or programming club. We will
measure first-Accepted time, problem completion and return visits. If students
return and organizers need more problems and contests, we can build a business
around course tools and sponsored competitions.

## Investor / accelerator framing

**Problem:** instructors and students need reliable feedback on implementations,
including quantum errors that ordinary output examples can miss.

**Initial product:** a small problem bank, a reproducible judge and a competition
workflow. The demo proves that workflow on known algorithms, not demand.

**Proposed buyer:** a university course organizer or a sponsor running a quantum
programming challenge. Students are the initial users.

**First commercial test:** get one course or club to run a cohort through a small
contest. Ask organizers which grading/content tasks they would pay to avoid.
Measure use before adding institution management or charging for it.

**Long-term thesis:** students can develop quantum algorithm skills through
repeatable software competitions while useful hardware access remains limited.
Organizers can later connect those contests to hardware-specific challenges.

**Potential advantage to develop:** well-reviewed tasks/checkers, dependable
contest operation and a community of problem authors and repeat participants.
These require work and adoption. Three exercises alone do not establish a moat.

## Spanish explanation for the founder

Es una plataforma para entrenar y competir programando algoritmos cuánticos.
Leés un problema, escribís Python, enviás y recibís un veredicto con evidencia.
Lo que mostramos hoy es que ese recorrido funciona. La apuesta comercial es
que cursos y organizadores quieran usarlo para enseñar y organizar competencias.

## Answers for judges

**What is new?** Our original problem content and the implementation of the
builder, checkers, browser/Qiskit paths and virtual contest. The algorithms and
the idea of quantum programming competitions already exist.

**Why Qollab?** It runs the Qiskit judge for the same problem contracts. It is an
execution path for the central product, not a decorative circuit.

**Where is the quantum advantage?** In stated oracle-query models. We do not
claim that a browser simulator runs faster than classical code.

**Is the ranking trusted?** This edition is a local virtual round with public
tests. A trusted shared contest requires a server-side judge.

**Have students learned more or paid?** We have not measured those outcomes.
The next milestone is a course/club pilot.

**What would you fund next?** Reviewed problems, instructor pilots and a trusted
contest judge after validating use, rather than social features.
