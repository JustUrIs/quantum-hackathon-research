# Front C — Quantum Impact: real problems, public data, honest benchmarks

Scout date: 2026-10-10. Sources come from web search (arXiv, journals, dataset portals). I did not open every full text. Claims I could not check are marked **[unverified]**.

## Read this first: what the evidence says (applies to every card)
1. **No quantum optimization advantage has been demonstrated on a real problem at ≤25 qubits.** At that size, brute force, CP-SAT/Gurobi or simulated annealing (SA) reaches the exact optimum in milliseconds. A team that claims "QAOA beat Gurobi" will be caught right away by IonQ judges. The only honest way to frame Impact is one of these:
   (a) a quality-per-circuit-depth or scaling study against a fair baseline;
   (b) a different value metric, such as diversity, Pareto fronts or robustness;
   (c) a pipeline that is ready for quantum when bigger machines arrive, with an honest "classical wins today" chart.
2. **Recent advantage claims are being knocked down.** Kipu/IBM BF-DCQO claimed runtime advantage (arXiv 2505.08663, May 2025). Two rebuttals followed: arXiv 2510.06337 ("Recent quantum runtime (dis)advantages", Oct 2025) and arXiv 2509.14358, which shows most of the iterations ran on a classical simulator. Judges know about this fight, so being honest earns points.
3. **The IonQ simulator allows one job per run, and this decides the method.** Classic variational QAOA/VQE needs hundreds of jobs. Two ways around it: optimize the parameters on the local statevector, then send one final sampling circuit to IonQ; or use **fixed or transferred parameters** with no training loop. The JPMorgan LABS paper used fixed-parameter QAOA ([Sci. Adv. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11135426/)). That fits the one-job rule exactly and is a point you can say out loud in the pitch.
4. **A strong Impact submission has three parts:** a real dataset, a strong baseline (CP-SAT/HiGHS/SA plus exact brute force at small n), and a metric where the quantum piece can be measured. Diversity, Pareto coverage and approximation ratio against depth are honest metrics. Wall-clock speed is not.

---

### S-C-1: Power-grid feeder reconfiguration: k diverse switching plans, not one optimum
- **What:** Distribution operators open or close tie switches to cut losses and restore service after a fault. IEEE 33-bus has 37 lines and 5 tie switches. Radial configurations can be enumerated, and the loop structure maps to about 15 binary variables. The proposal is to give the operator a portfolio of near-optimal, structurally different plans, because the best plan may be unavailable when a switch is stuck or a crew is far away.
- **Source:** Hybrid QAOA on the 33-bus case with an AC-feasible loss QUBO, from UPS Ecuador ([pure.ups.edu.ec](https://pure.ups.edu.ec/en/publications/optimal-distribution-network-reconfiguration-with-renewable-gener/)). It reports a 15-parameter QUBO, 32 configurations and a 9.98% gap to the global optimum. Dynamic 33-bus QAOA with real load profiles, Çukurova Univ. 2025 ([pdf](https://cukurovaumfd.cu.edu.tr/storage/40-1/7.pdf)).
- **Dataset:** MATPOWER `case33bw` (Baran–Wu) and `case69`, at github.com/MATPOWER/matpower. pandapower ships `case33bw()` built in.
- **Classical baseline:** exhaustive enumeration of radial topologies (feasible at 33-bus), plus the Merlin–Back branch exchange heuristic, plus MILP via HiGHS/OR-Tools.
- **≤25 qubits without becoming a toy:** yes. 33-bus with ~15–20 binaries is the real IEEE test case, not a scaled-down one. 69-bus fits after loop-based encoding (5 loops) **[unverified qubit count]**.
- **Rarity:** 3. Grid people know the problem, but very few combine it with "diverse sample sets".
- **Real pain:** Distribution losses run at 10–15% in LatAm. Argentine distributors are known for high technical and non-technical losses **[general knowledge, no citation pulled]**. Reconfiguration is standard practice for utilities.
- **Quantum hook:** It is honest only under the diversity framing. Classical enumeration solves 33-bus exactly. The QAOA output distribution gives several good plans per shot set, which you compare against SA restarts on time-to-diversity (TTD).
- **Buildability:** high. pandapower runs in Pyodide **[check that the wheel exists]**, otherwise precompute the losses into a QUBO JSON.
- **Theme fit:** Impact.
- **Prior art:** two QAOA-on-33-bus papers already exist (above), and the 2025 LatAm Quantum Hackathon winner MIQRO did "power distribution networks" ([CERN OQI](https://open-quantum-institute.web.cern.ch/quantum-hackathon-latam-explores-quantum-computing-for-the-sdgs/)). Plain QAOA reconfiguration is not new. The diversity, operator-portfolio framing is.
- **Collision hint:** feeder reconfiguration × resilience after storms (Buenos Aires AMBA blackouts) × the "time-to-diversity" metric from Google (S-C-13).

### S-C-2: Unit commitment on IEEE 57-bus / RTS-GMLC with fixed-parameter QAOA
- **What:** Decide which generators are on in each hour (binary) and dispatch them, which is a continuous subproblem. A 2025 paper reports that 16-layer QAOA matches or beats a strong classical baseline at ≤14 qubits under high load.
- **Source:** arXiv [2505.16444](https://arxiv.org/abs/2505.16444) (2025). Note that v1 and later versions frame the results differently, so cite the latest. Original QAOA-UC: arXiv [2110.12624](https://arxiv.org/pdf/2110.12624). That paper says classical solvers are fine below about 400 units.
- **Dataset:** RTS-GMLC (github.com/GridMod/RTS-GMLC, 73 generators with real hourly profiles) and MATPOWER `case57`. For Argentina, CAMMESA hourly demand and supply is available through Alphacast ([link](https://www.alphacast.io/datasets/activity-production-argentina-cammesa-hourly-electricity-demand-42733), free signup). Official per-unit dispatch data on cammesaweb **[not verified]**.
- **Classical baseline:** MILP UC in HiGHS/PuLP (the industry standard, solves in seconds), plus SA on the same QUBO.
- **≤25 qubits:** 10–20 units × 1 hour, or 5 units × 4 hours. That is honest as a single-period commitment but a toy for real multi-period UC.
- **Rarity:** 2. Well trodden.
- **Real pain:** real (a billion-dollar dispatch market), but MILP already handles it well in practice.
- **Quantum hook:** weak. The arXiv paper itself says advantage would need hundreds of units.
- **Buildability:** high.
- **Theme fit:** Impact.
- **Prior art:** heavy (the two papers above, plus IonQ/ORNL QITE naming unit commitment as a target ([IonQ](https://ionq.com/news/ionq-and-oak-ridge-national-laboratory-unveil-novel-approach-to-scalable))).
- **Collision hint:** fixed-parameter transfer from the LABS work (S-C-12) means UC with zero training jobs on IonQ.

### S-C-3: Earth-observation satellite image acquisition (SPOT5 / CNES)
- **What:** Choose which photo requests a satellite takes in one orbit pass, subject to conflicts (slew time, memory) and with weighted priorities. The structure is a max-weight independent set or knapsack.
- **Source:** QUBO on 20 instances (14 SPOT5) across 3 D-Wave annealers plus hybrid, by Makarov/Osaba/TECNALIA 2023 ([inspire](https://inspirehep.net/literature/2682427)). PoliTo 2025 QUBO for EO formation rescheduling ([Springer SN CS 2025](https://link.springer.com/article/10.1007/s42979-025-04252-2)). ESA EO4Society UC1 ([pdf](https://eo4society.esa.int/wp-content/uploads/2024/01/Summary-of-UC1-Mission-Planning-for-Earth-Observation-Acquisitions.pdf)).
- **Dataset:** SPOT5 daily photograph instances from CNES ([Mendeley 2kbzg9nw3b](https://data.mendeley.com/datasets/2kbzg9nw3b/1)). SIASP benchmark plus generator ([Mendeley dzwvt4bz4j](https://data.mendeley.com/datasets/dzwvt4bz4j)). EOS-Bench 2026 with 13,900 instances (github.com/Ethan19YQ/EOS-Bench). AEOS VTW plus downlink windows ([IEEE DataPort](https://ieee-dataport.org/documents/aeos-scheduling-dataset-vtws-and-illumination-conditions)).
- **Classical baseline:** CP-SAT, or the known optimal SPOT5 values (published). Tabu search.
- **≤25 qubits:** the small SPOT5 instances (8, 54, 29…) have 8–100s of photos. Take connected components or one orbit window of ~20 requests. That is a real CNES instance slice, not a toy.
- **Rarity:** 3.
- **Real pain:** real. Agencies are oversubscribed (more requests than capacity). CONAE's SAOCOM satellites are an Argentine angle.
- **Quantum hook:** MIS/QUBO maps natively to QAOA. Diversity also matters, because plans get re-planned when weather changes and cloud cover kills photos.
- **Buildability:** high. The data is small text files.
- **Theme fit:** Impact (space).
- **Prior art:** annealing done several times (TECNALIA, PoliTo). Gate-based QAOA plus IonQ plus a cloud-robust portfolio looks less covered **[not exhaustively checked]**.
- **Collision hint:** cloud forecast uncertainty (open meteo API, CORS GET OK) × a diverse plan portfolio means picking the plan robust to clouds.

### S-C-4: Protein side-chain packing (rotamer selection)
- **What:** Fix the backbone and choose one rotamer per residue to minimize energy. One-hot encoding gives residues × rotamers qubits. IBM published a 2025 head-to-head of QAOA against classical methods.
- **Source:** arXiv [2507.19383](https://arxiv.org/pdf/2507.19383) (IBM, Jul 2025, statevector and MPS QAOA). QPacker on D-Wave ([bioRxiv 752485](https://www.biorxiv.org/content/10.1101/752485v2)).
- **Dataset:** PDB structures plus the Dunbrack rotamer library. PyRosetta needs a license, but OpenMM or a precomputed pairwise energy table avoids it.
- **Classical baseline:** dead-end elimination plus exact ILP. SCWRL4, Rosetta packer.
- **≤25 qubits:** about 5 residues × 4 rotamers = 20 qubits, which is a toy for packing. Real interest lies in the 100s of residues. A small interface hotspot is defensible.
- **Rarity:** 3.
- **Real pain:** real for protein design, but classical packers are excellent.
- **Quantum hook:** weak at this size. DEE prunes most of the space.
- **Buildability:** med. Building the energy table is the hard part.
- **Theme fit:** Impact.
- **Prior art:** IBM 2025 is direct prior art. Low novelty.
- **Collision hint:** docking (S-C-5).

### S-C-5: Molecular docking as max-weight clique (QAOA)
- **What:** The docking pose comes from the maximum weighted clique in a binding-interaction graph (ligand pharmacophore × receptor pharmacophore pairs).
- **Source:** Xanadu GBS docking 2019 ([PMC7274809](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7274809/)). DC-QAOA docking with 14–17 nodes, Mar 2025 ([arXiv 2503.04239](https://arxiv.org/abs/2503.04239)). 2026 MAC-QAOA penalty calibration ([bioRxiv](https://www.biorxiv.org/content/10.64898/2026.01.27.699805.full.pdf)). Q-Score 2026 reports exact solutions on 8/11 targets at 10 qubits **[unverified, secondary source]**.
- **Dataset:** PDBbind (signup needed) and the TACE complex from the Xanadu paper. Use RDKit for pharmacophores.
- **Classical baseline:** NetworkX exact max-weight clique (instant at 20 nodes), plus AutoDock Vina for actual pose quality.
- **≤25 qubits:** 14–20 node graphs, the same scale as the papers.
- **Rarity:** 3.
- **Real pain:** docking is real, but the clique reduction is a simplified model.
- **Quantum hook:** clique maps to QUBO naturally. No advantage at this size.
- **Buildability:** med-high.
- **Theme fit:** Impact.
- **Prior art:** heavy since 2019. A good tutorial domain with low novelty.
- **Collision hint:** Argentine neglected diseases (Chagas cruzain protease, which has PDB structures) give a meaning change toward "quantum for neglected diseases" **[impact framing; the science gain is nil]**.

### S-C-6: Haplotype assembly / phasing as MEC to Max-Cut
- **What:** Given sequencing reads that cover heterozygous SNPs, split the reads into two haplotypes so that minimum error correction (MEC) is as small as possible. For a diploid genome this is **natively a weighted Max-Cut** on a read-conflict graph, which is QAOA's home problem with no penalty terms and no one-hot overhead.
- **Source:** VRP Assembler (Cell Rep. Methods 2024; [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.10.19.563028.full.pdf)). Quantum-inspired QHap phasing, Mar 2026 ([arXiv 2603.25762](https://arxiv.org/abs/2603.25762v1), **[content unverified]**). Haplotype inference via QUBO (Nghiem et al.). Genome assembly QUBO (Boev, Sci. Rep. 2021, [PMC8222255](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8222255/)).
- **Dataset:** GIAB NA12878 / HG002 reads, plus WhatsHap/HapCUT2 test data. Small phasing blocks come from public 1000 Genomes BAM slices. The CORS GET from the browser **[must be checked]**, otherwise precompute and ship JSON.
- **Classical baseline:** WhatsHap (exact for bounded coverage, the standard tool), HapCUT2, Goemans–Williamson SDP.
- **≤25 qubits:** one phasing block of ~20 reads gives 20 qubits. That is real (blocks are local), but trivially exact classically.
- **Rarity:** 4. Very few people know MEC equals Max-Cut, and it's a neat "aha".
- **Real pain:** phasing errors matter clinically (compound heterozygosity for recessive disease).
- **Quantum hook:** a clean Max-Cut mapping, and a **sample distribution maps to phasing uncertainty**. Several near-optimal cuts give alternative phasings, so you get a confidence per SNP from the sample frequencies. That is a meaningful use of sampling.
- **Buildability:** high if precomputed.
- **Theme fit:** Impact (health).
- **Prior art:** QUBO assembly is well covered. A Max-Cut/QAOA phasing uncertainty readout looks uncovered **[not exhaustively checked]**.
- **Collision hint:** clinical genetics × "quantum gives calibrated uncertainty, not just an answer."

### S-C-7: Water network sensor / isolation-valve placement
- **What:** Place a few pressure sensors (or isolation valves) on a real water distribution network to cover pipe segments so leaks or contamination are detected, or so the population affected when a segment is isolated stays small.
- **Source:** Sensor placement QUBO on a real network, D-Wave plus SA ([arXiv 2108.04075](https://arxiv.org/pdf/2108.04075)). Quantum WDN simulation 2025 ([arXiv 2507.06862](https://arxiv.org/pdf/2507.06862)). Classical valve placement at Univ. Ferrara ([link](https://docente.unife.it/marco.gavanelli/software/valve-placement-in-hydraulic-networks)). **I found no valve-placement QUBO.**
- **Dataset:** EPANET benchmark networks (Net1, Net3, Anytown, L-Town from BattLeDIM 2020, KY networks from the Univ. of Kentucky). They are open and read with WNTR/EPyT.
- **Classical baseline:** greedy submodular coverage (with a (1−1/e) guarantee), plus ILP.
- **≤25 qubits:** Net1/Net3 or a district metered area (DMA) of L-Town gives ~20 candidate locations. That is realistic, because utilities place sensors per DMA.
- **Rarity:** 4.
- **Real pain:** high. Leakage reaches about 30% in many LatAm utilities, and AySA in Buenos Aires runs a leak-reduction programme **[figure from general knowledge, cite before use]**. The BattLeDIM competition exists because of this pain.
- **Quantum hook:** a coverage QUBO. No advantage. The Pareto front (sensor count against coverage) is the honest angle (S-C-11).
- **Buildability:** high (EPANET inp files are small).
- **Theme fit:** Impact (water/SDG).
- **Prior art:** sensor QUBO from 2021, and the 2026 LatAm Quantum Water Hackathon on Falcón dam releases ([QZ](https://quantumzeitgeist.com/mexico-latam-quantum-hackathon-seventy-five/)). Valve placement as a QUBO is a gap.
- **Collision hint:** valve isolation × social vulnerability maps (schools and hospitals weighted higher).

### S-C-8: Wildfire fuelbreak placement as graph partitioning
- **What:** Split a landscape graph into fire-isolated compartments of near-equal size while keeping cleared acreage low. The US Army ERDC did this on D-Wave hybrid. It was published in Jan 2026 in a Nature-family journal.
- **Source:** Dent et al. 2026 ([PMC12910063](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12910063/)). It reports a 2.9% better separation equality with 76 fewer acres cleared, and D-Wave hybrid ran faster than SCIP but slower than CPLEX. Army news ([scquantum](https://www.scquantum.org/news/army-researchers-tap-quantum-computing-optimize-wildfire-prevention)).
- **Dataset:** LANDFIRE (US fuels) or a Cell2Fire / Chilean/Canadian fire simulator grid. For Patagonia (Andean-Patagonian forest fires 2025–26), use INTA/MapBiomas Argentina land cover **[access not checked]**.
- **Classical baseline:** METIS graph partitioning, CPLEX/HiGHS MIP, stochastic programming ([optimization-online](https://optimization-online.org/2023/11/a-two-stage-stochastic-programming-approach-incorporating-spatially-explicit-fire-scenarios-for-optimal-firebreak-placement/)).
- **≤25 qubits:** a 5×5 cell grid is a toy. A coarse watershed graph of ~20 nodes is defensible as a strategic-level plan.
- **Rarity:** 4.
- **Real pain:** high and timely. The Patagonian fires of early 2025 and 2026 burned tens of thousands of hectares **[check figures]**.
- **Quantum hook:** a balanced partitioning QUBO. No advantage.
- **Buildability:** med.
- **Theme fit:** Impact.
- **Prior art:** ERDC 2026 (annealing). Gate-model QAOA plus a Patagonia dataset is new.
- **Collision hint:** fuelbreaks × diversity (several ways to cut that land managers choose between under local constraints).

### S-C-9: Nurse / hospital rostering with constraint-preserving mixers
- **What:** Assign nurses to shifts under coverage, rest and preference rules. A 2026 paper builds QAOA mixers that keep coverage satisfied, so the circuit never samples infeasible rosters.
- **Source:** Ikeda/Nakamura/Humble NSP on D-Wave ([arXiv 1904.12139](https://arxiv.org/pdf/1904.12139)). Constraint-preserving QAOA for rostering, Jul 2026 ([arXiv 2607.09145](https://arxiv.org/pdf/2607.09145)). NSP via PyQUBO ([arXiv 2302.09459](https://arxiv.org/abs/2302.09459v2)).
- **Dataset:** NSPLib ([MaRDI](https://portal.mardi4nfdi.de/wiki/NSPLib)), INRC-II (Second International Nurse Rostering Competition), Curtois/Qu shift-scheduling benchmarks (schedulingbenchmarks.org).
- **Classical baseline:** CP-SAT, which dominates rostering in practice.
- **≤25 qubits:** 3 nurses × 7 days × 1 shift = 21 qubits, a toy. Real hospitals are 30–100 nurses × 28 days.
- **Rarity:** 3.
- **Real pain:** very high (nurse burnout). The quantum fit is weak.
- **Quantum hook:** the XY mixer that preserves constraints is good quantum engineering, a real technical-execution point.
- **Buildability:** high.
- **Theme fit:** Impact (also Unlocked as a "why mixers matter" teaching demo).
- **Prior art:** fresh 2026 paper. Copying it would be low novelty.
- **Collision hint:** fairness. Sample many rosters and pick by equity, which is the diversity angle again.

### S-C-10: QOBLIB "Intractable Decathlon": submit to the official leaderboard
- **What:** In 2025 the IBM-led Quantum Optimization Working Group (with ZIB and others) released 10 hard problem classes with model-independent benchmarking and a public submission log: Market Split, LABS, Birkhoff, Steiner tree packing, sports scheduling, multi-period portfolio, MIS, network design, CVRP, topology design. It holds ~1,260 instances **[secondary figure]**.
- **Source:** [arXiv 2504.03832](https://arxiv.org/html/2504.03832v1). Repo github.com/ZIB-AOPT/QOBLIB. [IBM blog](https://ibm.com/quantum/blog/quantum-optimization-benchmarking). Possibly published in Nature Comp. Sci. **[unverified]**.
- **Dataset:** the repo itself, with instances and best-known solutions. Some instances have ~20 variables.
- **Classical baseline:** given inside QOBLIB (Gurobi/CPLEX/SA results logged).
- **≤25 qubits:** the smallest MIS and Market Split instances fit. Sports scheduling starts at 408 variables, so it does not fit.
- **Rarity:** 4. Known to the optimization working group, unknown to hackathon teams.
- **Real pain:** this is the community's own yardstick, made because simplified toy problems mislead.
- **Quantum hook:** judges from IonQ/IBM-adjacent circles will recognize it at once. Running honest small-instance QAOA plus a classical baseline under the QOBLIB protocol earns rigor credibility.
- **Buildability:** high.
- **Theme fit:** Impact (tech execution). Not an "industry story" by itself, so combine it with a real-world problem framing.
- **Prior art:** the library exists to collect submissions, so contributing to it is the point, not a collision.
- **Collision hint:** Market Split is linked to real "fair division" / budget allocation. Wrap it as "splitting a provincial budget exactly" (e.g., coparticipación in Argentina) **[framing idea]**.

### S-C-11: Multi-objective QAOA: Pareto fronts as the honest quantum value
- **What:** IBM, ZIB and LANL (Mar 2025) used shallow QAOA to approximate **Pareto fronts** of multi-objective weighted Max-Cut. They argue classical solvers struggle on multi-objective problems even when each single objective is easy, and they ran it on IBM hardware.
- **Source:** Kotil et al., [arXiv 2503.22797](https://arxiv.org/abs/2503.22797). Reported as Nature Comp. Sci. **[unverified]**.
- **Dataset:** any of S-C-1/3/7 with two objectives (losses vs. switch operations; sensors vs. coverage; photo value vs. energy).
- **Classical baseline:** epsilon-constraint MILP sweeps, NSGA-II, weighted-sum SA, with hypervolume as the metric.
- **≤25 qubits:** yes. Pareto structure is non-trivial even at 15–20 variables.
- **Rarity:** 5. A very fresh direction that few practitioners know.
- **Real pain:** real decisions are multi-objective (cost vs. reliability vs. equity). Single-number optimization is the cliché.
- **Quantum hook:** **the strongest honest hook here.** One parametrized circuit, sampled once, returns a whole distribution, and the bitstrings that are non-dominated across the objectives form an approximate front. Measuring hypervolume per shot against classical per evaluation is a fair comparison. It also fits the one-job IonQ constraint.
- **Buildability:** high (just a weighted-objective QAOA plus a post-processing filter).
- **Theme fit:** Impact + Novelty.
- **Prior art:** the IBM paper did it on synthetic Max-Cut. On a real infrastructure dataset it looks **unclaimed [not exhaustively checked]**.
- **Collision hint:** this card plus S-C-1 or S-C-7 is the candidate core project.

### S-C-12: LABS / radar pulse codes with fixed-parameter QAOA
- **What:** Find binary sequences with low autocorrelation (used for radar and sonar pulses). JPMorgan, Argonne and Quantinuum showed fixed-parameter QAOA scales better than branch-and-bound in noiseless simulation up to 40 qubits.
- **Source:** [Sci. Adv. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11135426/), [arXiv 2308.02342](https://arxiv.org/abs/2308.02342v2). LABS is also in QOBLIB.
- **Dataset:** the problem is defined by N alone. Optimal values are known for N ≤ 66, and the published parameters are reusable.
- **Classical baseline:** memetic tabu search (the state of the art) and branch-and-bound.
- **≤25 qubits:** N = 20–25, close to the paper's regime, but the objective has 4-body terms, so the circuits are deep.
- **Rarity:** 4.
- **Real pain:** niche. The radar framing is real but abstract.
- **Quantum hook:** the strongest published scaling evidence for QAOA. Fixed parameters mean one job and no training, a perfect fit for IonQ's one-job rule.
- **Buildability:** med (4-body terms mean deep circuits, but the simulator handles them).
- **Theme fit:** Impact (weak industry story), Unlocked (teach "what scaling advantage means").
- **Prior art:** heavy (the reproduction would be the project).
- **Collision hint:** use the **fixed-parameter transfer trick** in any other card to dodge the variational loop.

### S-C-13: "Time-to-diversity": a benchmark metric where sampling, not optimizing, is the value
- **What:** Google proposed TTD (time-to-diversity), the time to collect k independent near-optimal solutions, as a generalization of time-to-solution. Inhomogeneous annealing improved diversity by up to 40% in simulation. Standard transverse-field QA samples degenerate optima **unfairly** (a known caveat that applies to QAOA too).
- **Source:** [arXiv 2110.10196](https://arxiv.org/pdf/2110.10196) (diversity metric), [arXiv 2110.10560](https://arxiv.org/pdf/2110.10560) (diverse sampling). Node-centrality bias, Jan 2026 ([arXiv 2601.01920](https://arxiv.org/pdf/2601.01920)). Classical cluster post-processing fixes this ([arXiv 1801.07681](https://arxiv.org/pdf/1801.07681)).
- **Dataset:** apply it to S-C-1, 3, 6, 7.
- **Classical baseline:** SA with restarts, parallel tempering + ICM (good at fair sampling), and a cluster-update post-processor.
- **≤25 qubits:** yes. With brute force you know **all** near-optimal solutions, so you can measure exact coverage. This is the unique advantage of small instances: you hold the ground truth.
- **Rarity:** 5.
- **Real pain:** operators need alternatives (switch out of service, crew unavailable, a photo clouded over).
- **Quantum hook:** honest. The question is whether QAOA at depth p samples the near-optimal set more uniformly than SA at the same evaluation budget. The answer may be **no**, and reporting that is itself a credible result.
- **Buildability:** high.
- **Theme fit:** Impact + Novelty.
- **Prior art:** metric papers exist, mostly on spin glasses and annealing. A gate-model QAOA TTD on real infrastructure data looks unclaimed **[not exhaustively checked]**.
- **Collision hint:** S-C-11 (Pareto) is a sibling. Combine "diversity + Pareto" into one evaluation framework.

### S-C-14: An "advantage auditor": an honest negative result as the impact
- **What:** A reproducible harness that takes a quantum-optimization claim, re-runs it with strong baselines and fair runtime accounting, and outputs a verdict. Example: QAOA on a real instance versus CP-SAT, SA, PT and brute force, with a scorecard covering quality, diversity, Pareto hypervolume and qubit/shot cost.
- **Source:** the BF-DCQO dispute, with the [claim](https://thequantuminsider.com/2025/05/17/quantum-algorithm-outpaces-classical-solvers-in-optimization-tasks-study-indicates/) and the rebuttals [2510.06337](https://arxiv.org/html/2510.06337v3) and [2509.14358](https://arxiv.org/html/2509.14358v1). The benchmarking literature review ([arXiv 2509.03078](https://arxiv.org/pdf/2509.03078)) warns of "pseudo-dequantizations". QOBLIB's model-independent protocol.
- **Dataset:** QOBLIB plus one real infrastructure dataset.
- **Classical baseline:** that is the whole point. Use every strong one.
- **≤25 qubits:** yes.
- **Rarity:** 4. A contrarian truth: "the most valuable quantum product today is an honest referee."
- **Real pain:** companies spend money on quantum pilots with no good way to judge vendor claims.
- **Quantum hook:** the quantum is essential because it is the thing being audited, though the build is quantum-adjacent. Risk: judges may want the quantum to *do* something, so pair it with a strong positive component (S-C-11).
- **Buildability:** high.
- **Theme fit:** Impact / Best documentation.
- **Prior art:** academic rebuttals exist, but no interactive tool **[not verified]**.
- **Collision hint:** pair it with the Pareto or diversity project as the built-in self-audit. That is very strong for the documentation judges.

### S-C-15: Small-molecule ground states for batteries / electrolytes (VQE / SQD)
- **What:** Ground-state energies of LiH, Li2O fragments, or electrolyte fragments (EC, LiPF6 pieces) via VQE, or IBM's Sample-based Quantum Diagonalization (SQD), which is sampling-based and fits the one-job model.
- **Source:** IonQ × Hyundai lithium oxide VQE, 2022 ([IonQ](https://ionq.com/resources/improving-battery-chemistry-with-quantum-computing)). The IBM SQD tutorial (N2) ([docs](https://quantum.cloud.ibm.com/docs/tutorials/sample-based-quantum-diagonalization)). A 2026 review says classical methods generally beat quantum samplers on standard molecules **[unverified, secondary]**.
- **Dataset:** PubChem geometries and the QM9 / OE62 electrolyte sets. Reference energies from FCI/CCSD(T) via PySCF (PySCF in the browser is **unlikely**, so precompute the Hamiltonians to files).
- **Classical baseline:** FCI / CCSD(T) (exact at this size).
- **≤25 qubits:** LiH (12 spin orbitals) and small active spaces (6–10 orbitals) fit, but they are toys chemically. Classical methods are exact.
- **Rarity:** 1. Everyone does VQE-H2/LiH.
- **Real pain:** real (batteries), but this scale cannot show it.
- **Quantum hook:** genuine (chemistry is the natural quantum problem), but there is no measurable difference at ≤25 qubits.
- **Buildability:** med (the one-job constraint hurts VQE, while SQD fits better).
- **Theme fit:** Impact, weak. Judges have seen this 1,000 times.
- **Prior art:** saturated, and IonQ's own case study covers it. **Avoid unless there is a twist.**
- **Collision hint:** Argentine lithium triangle (Jujuy/Catamarca brines). The story is strong, but the quantum adds nothing measurable here.

### S-C-16: Buenos Aires bus network: depot / stop consolidation from GTFS
- **What:** Use the official Buenos Aires bus GTFS (~1,052 routes) to pick which stops to consolidate, or which lines get electric buses, under coverage constraints. This is a facility-location or stop-selection QUBO on a corridor.
- **Source:** GTFS on data.buenosaires.gob.ar ("colectivos-gtfs"), mirrored at [Mobility Database mdb-1220](https://mobilitydatabase.org/feeds/gtfs/mdb-1220) and [TUMI hub](https://hub.tumidata.org/dataset/buses_gtfs_buenos_aires). The latest version on file covers 2023–24.
- **Classical baseline:** greedy set cover, plus ILP (OR-Tools).
- **≤25 qubits:** ~20 candidate stops on one corridor. Real but local.
- **Rarity:** 3.
- **Real pain:** real (AMBA bus subsidies and fleet electrification are live topics) **[no specific citation pulled]**.
- **Quantum hook:** none beyond generic QUBO. Mostly decorative unless combined with Pareto (S-C-11).
- **Buildability:** high (GTFS is CSV, and the CORS GET from the city CDN **[unverified]**, otherwise ship files).
- **Theme fit:** Impact (local).
- **Prior art:** many quantum hackathons did routing. Stop consolidation on BA data looks new, but it is low in quantum essentiality.
- **Collision hint:** a Pareto front of riders' walking time against operating cost.

### S-C-17: Crop rotation / agro land allocation (Argentina pampas)
- **What:** Assign crops to plots over seasons with family-separation (pest) and soil-nitrogen rules. A D-Wave DQM repo exists. A QAOA "precision agriculture" paper reports 72.5% faster convergence for adaptive QAOA **[low-quality journal, unverified]**.
- **Source:** GitHub Farm-Optimization-QC ([mirror](https://ithub.global.ssl.fastly.net/MohanKrishnaGR/Farm-Optimization---QC)). A-QAOA ([GMR](https://geneticsmr.com/index.php/gmr/article/view/4099)).
- **Dataset:** Argentina's Ministerio de Agricultura "Estimaciones Agrícolas" (datosestimaciones.magyp.gob.ar), with crop × department × season series **[portal not opened this session]**. INTA soil maps.
- **Classical baseline:** CP-SAT / MILP (trivial at this size).
- **≤25 qubits:** 3 plots × 3 seasons × 2–3 crops is about 18–27 qubits, a toy.
- **Rarity:** 3.
- **Real pain:** real (soybean monoculture and soil degradation in the pampas), but farmers do not need optimizers for 3 plots.
- **Quantum hook:** decorative.
- **Buildability:** high.
- **Theme fit:** Impact (local story).
- **Prior art:** thin academic coverage, mostly repos.
- **Collision hint:** diversity of rotations as agronomic risk hedging. That stretches the idea.

### S-C-18: Quantum kernels on real industrial data: say no
- **What:** Quantum kernel SVMs on grid-fault, fraud or medical datasets are a common hackathon move. 2025 dequantization results show random Fourier features or exact classical evaluation match many quantum kernels.
- **Source:** [arXiv 2505.15902](https://arxiv.org/abs/2505.15902v1) (RFF dequantization, v3 Dec 2025). [arXiv 2503.23931](https://arxiv.org/html/2503.23931v1). Review [arXiv 2604.07896](https://arxiv.org/pdf/2604.07896).
- **Dataset / baseline:** any. An RBF SVM or a gradient-boosted model will win.
- **≤25 qubits:** fits, but it's a toy and dequantizable.
- **Rarity:** 1 for doing it, 4 for knowing it's dequantized.
- **Quantum hook:** none / decorative for classical data. IonQ judges will see through it.
- **Buildability:** high.
- **Theme fit:** Impact, poor. Unlocked only as a "why QML hype fails" lesson.
- **Prior art:** saturated.
- **Collision hint:** this is a good **negative control** inside the auditor (S-C-14).

---

## Cross-cutting notes for the build
- **One-job IonQ pattern:** train or transfer parameters locally, then send a single final circuit to the IonQ simulator for N shots. All metrics (best cost, diversity, Pareto hypervolume) are computed from those shots. Say this explicitly in the docs. It turns a platform limit into an honest "a sampler is the product" story.
- **The ground-truth advantage of small instances:** at ≤25 qubits, brute force over 2^n (33M states, feasible in numpy/WebAssembly with some care, easy at n ≤ 20) gives the exact full landscape. So you can report *exact* approximation ratios and *exact* coverage of the near-optimal set. Most papers cannot do this. Turn the limitation into rigor.
- **Classical baselines that are always required:** brute force (exact), simulated annealing with matched evaluations, CP-SAT/HiGHS, plus a problem-specific heuristic (greedy, Merlin-Back, WhatsHap…).

## Top 3 from this front
1. **S-C-11 + S-C-1 (or S-C-7): "Pareto from one shot." Multi-objective QAOA on a real IEEE 33-bus feeder (or EPANET water DMA)**, benchmarked by hypervolume per shot against NSGA-II/epsilon-MILP, with exact brute-force ground truth. It is the freshest honest quantum value (IBM 2025, unclaimed on real infrastructure), fits the one-job IonQ model natively, and the data is real and small.
2. **S-C-13 + S-C-6: "Calibrated uncertainty from a quantum sampler." Haplotype phasing as native Max-Cut**, where the QAOA sample distribution gives per-SNP phasing confidence, compared on time-to-diversity and calibration against WhatsHap plus SA restarts. It has a rare (level 4–5) mapping with no penalty terms, a clinical stake, and the metric is about sampling, so it does not pretend to win on speed.
3. **S-C-14 as the built-in self-audit for #1 or #2: an "advantage auditor"** scorecard that shows where classical wins (speed, plain optimum) and where the quantum sampler does or does not add value (diversity, Pareto coverage), with BF-DCQO-style pitfalls documented. Brutal honesty is exactly what IonQ judges reward, and it carries the Documentation award.
