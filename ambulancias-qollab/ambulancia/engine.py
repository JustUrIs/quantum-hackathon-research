"""Small, exact scenario model plus a fixed-cardinality QAOA experiment."""
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import DiagonalGate, StatePreparation
from qiskit.quantum_info import Statevector

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "caba_signals.json"
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))
N = len(DATA["sites"])
SITES = DATA["sites"]
CELLS = DATA["demand_grid"]["cells"]
BOUNDS = DATA["boundary"]
CELL_POINTS = []
for row in range(8):
    for col in range(8):
        CELL_POINTS.append((
            BOUNDS["west"]+(col+.5)*(BOUNDS["east"]-BOUNDS["west"])/8,
            BOUNDS["north"]-(row+.5)*(BOUNDS["north"]-BOUNDS["south"])/8,
        ))


def _config(config_json):
    c=json.loads(config_json) if isinstance(config_json,str) else dict(config_json)
    k=int(c.get("units",3)); radius=float(c.get("radius_km",3.0))
    failure=float(c.get("outage_weight",.3)); scenario=c.get("scenario","history")
    if not 1<=k<=N or not 1.0<=radius<=6.0 or not 0<=failure<=1:
        raise ValueError("Choose 1-8 units, a 1-6 km radius and a 0-100% outage weight.")
    if scenario not in {"history","night","recent","severe"}:
        raise ValueError("Unknown demand scenario.")
    return {"units":k,"radius_km":radius,"outage_weight":failure,"scenario":scenario}


def _weights(scenario):
    out=[]
    for row in CELLS:
        for cell in row:
            if scenario=="night": w=cell["night"]
            elif scenario=="recent": w=cell["recent"]
            elif scenario=="severe": w=cell["serious"]+3*cell["fatal"]
            else: w=cell["events"]+2*cell["serious"]+5*cell["fatal"]
            out.append(float(w))
    return out


def _distance_km(a,b):
    lat1,lat2=math.radians(a[1]),math.radians(b[1])
    dlat=lat2-lat1;dlon=math.radians(b[0]-a[0])
    q=math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371*2*math.asin(min(1,math.sqrt(q)))


def _problem(c):
    weights=_weights(c["scenario"])
    reachable=[]
    for lon,lat in CELL_POINTS:
        reachable.append(sum((1<<i) for i,s in enumerate(SITES)
                             if _distance_km((lon,lat),(s["lon"],s["lat"]))<=c["radius_km"]))
    def coverage(mask):
        return sum(w for w,site_mask in zip(weights,reachable) if mask&site_mask)
    def objective(mask):
        k=mask.bit_count()
        normal=coverage(mask)
        if k<1:return normal
        outage=sum(coverage(mask^(1<<j)) for j in range(N) if mask>>j&1)/k
        a=c["outage_weight"]
        return (1-a)*normal+a*outage
    return weights,reachable,coverage,objective


def _mask(combo):
    return sum(1<<j for j in combo)


def _solve_classical(k,objective):
    combos=list(itertools.combinations(range(N),k))
    values={_mask(q):float(objective(_mask(q))) for q in combos}
    optimum=max(values.values())
    winners=[m for m,v in values.items() if abs(v-optimum)<1e-9]
    current=0
    while current.bit_count()<k:
        current=max((current|(1<<j) for j in range(N) if not current>>j&1),key=objective)
    greedy=current
    improved=True
    while improved:
        improved=False;best=current;bestv=objective(current)
        for i in range(N):
            if not current>>i&1:continue
            for j in range(N):
                if current>>j&1:continue
                candidate=(current^(1<<i))|(1<<j);v=objective(candidate)
                if v>bestv+1e-9:best,bestv=candidate,v
        if best!=current:current=best;improved=True
    return values,winners,greedy,current,float(optimum)


def _dicke(n,k):
    v=np.zeros(1<<n,dtype=float)
    for q in itertools.combinations(range(n),k):v[_mask(q)]=1
    return v/np.linalg.norm(v)


def _circuit(params,k,utilities,measure=False):
    layers=len(params)//2
    qc=QuantumCircuit(N,N if measure else 0,name="guardia_grid_qaoa")
    qc.append(StatePreparation(_dicke(N,k)),range(N))
    maxabs=max(float(np.max(np.abs(utilities))),1.0)
    phase=np.exp(-1j*np.asarray(utilities,dtype=float)/maxabs)
    for layer in range(layers):
        gamma,beta=float(params[2*layer]),float(params[2*layer+1])
        # Exact lookup phase for the true robust coverage objective; invalid
        # Hamming-weight sectors are unreachable from the Dicke state.
        qc.append(DiagonalGate(phase**gamma),range(N))
        for parity in (0,1):
            for i in range(parity,N,2):
                j=(i+1)%N
                qc.rxx(2*beta,i,j);qc.ryy(2*beta,i,j)
    if measure:qc.measure(range(N),range(N))
    return qc


def _probabilities(params,k,utilities):
    qc=_circuit(params,k,utilities)
    return Statevector.from_instruction(qc).probabilities()


@lru_cache(maxsize=12)
def solve(config_key):
    c=_config(json.loads(config_key));weights,reachable,coverage,objective=_problem(c)
    values,winners,greedy,classical,optimum=_solve_classical(c["units"],objective)
    utility=np.zeros(1<<N,dtype=float)
    for mask,value in values.items():utility[mask]=value
    def energy(x):
        p=_probabilities(x,c["units"],utility)
        return -float(p@utility)
    # Fixed seed and several deterministic starts make browser runs reproducible.
    best=None
    starts=([.55,.8,.9,.35],[1.15,.48,.4,1.0])
    for x0 in starts:
        fit=minimize(energy,x0,method="COBYLA",options={"maxiter":14,"rhobeg":.45,"tol":.035})
        if best is None or fit.fun<best.fun:best=fit
    probs=_probabilities(best.x,c["units"],utility)
    expected=float(probs@utility)
    qaoa_best=max((m for m in values),key=lambda m:(probs[m],values[m]))
    p_opt=float(sum(probs[m] for m in winners))
    uniform=len(winners)/len(values)
    rows=[]
    for key,mask in (("greedy",greedy),("local_swap",classical),("exact",winners[0])):
        rows.append({"method":key,"sites":[i for i in range(N) if mask>>i&1],
                     "score":float(objective(mask)),"normal_score":float(coverage(mask)),
                     "one_site_out_score":float(sum(coverage(mask^(1<<j)) for j in range(N) if mask>>j&1)/max(1,mask.bit_count()))})
    qaoa_normal=float(coverage(qaoa_best))
    qaoa_outage=float(sum(coverage(qaoa_best^(1<<j)) for j in range(N) if qaoa_best>>j&1)/c["units"])
    best_outage=min((coverage(qaoa_best^(1<<j)) for j in range(N) if qaoa_best>>j&1),default=0.0)
    total=float(sum(weights))
    return {"config":c,"event_index_total":total,"unweighted_events":sum(cel["events"] for row in CELLS for cel in row),
            "coverable_index":float(max(coverage(_mask(q)) for q in itertools.combinations(range(N),c["units"]))),
            "methods":rows,"optimal_sites":[[i for i in range(N) if m>>i&1] for m in winners],
            "classical_combinations":len(values),"qaoa":{"expected_score":expected,"best_sample_score":float(objective(qaoa_best)),
             "best_sample_sites":[i for i in range(N) if qaoa_best>>i&1],"normal_score":qaoa_normal,
             "one_site_out_score":qaoa_outage,"probability_optimum":p_opt,
             "uniform_probability_optimum":uniform,"probability_fixed_cardinality":float(sum(probs[m] for m in values)),
             "worst_single_outage_score":float(best_outage),"parameters":[float(x) for x in best.x],
             "layers":2,"shots":"live backend run only"},
            "map":{"boundary":BOUNDS,"grid_rows":CELLS,"sites":SITES,"reach_masks":reachable,
                   "qaoa_sites":[i for i in range(N) if qaoa_best>>i&1],"optimal_sites":rows[2]["sites"]},
            "interpretation":{"proxy":"historical injury-crash event index; not all emergency calls or people served",
             "distance":"straight-line km, not drive time","site":"representative census-radio point, not verified parcel",
             "qaoa":"ideal local statevector prediction; not a measured quantum speedup"}}


def evaluate(config_json):
    key=json.dumps(_config(config_json),sort_keys=True,separators=(",",":"))
    return json.dumps(solve(key),allow_nan=False)


def audit_circuit(config_json):
    c=_config(config_json);key=json.dumps(c,sort_keys=True,separators=(",",":"))
    result=solve(key);_,_,_,objective=_problem(c)
    utility=np.zeros(1<<N,dtype=float)
    for q in itertools.combinations(range(N),c["units"]):utility[_mask(q)]=objective(_mask(q))
    circuit=_circuit(result["qaoa"]["parameters"],c["units"],utility,measure=True)
    # QIS basis is accepted by Qiskit/IonQ backends; decompose StatePreparation,
    # XY gates and the exact diagonal lookup before crossing the Qollab bridge.
    return transpile(circuit,basis_gates=["h","x","y","z","s","sdg","t","tdg","rx","ry","rz","cx"],optimization_level=1)


def ingest_audit(counts_json,config_json,backend_name="selected backend"):
    c=_config(config_json);_,_,_,objective=_problem(c)
    counts=json.loads(counts_json);shots=sum(int(v) for v in counts.values())
    if not shots:raise ValueError("Backend returned no measurement shots.")
    records=[]
    for key,count in counts.items():
        bitstring=str(key).replace(" ","")
        mask=int(bitstring,16) if bitstring.startswith("0x") else int(bitstring,2)
        score=float(objective(mask)) if mask.bit_count()==c["units"] else 0.0
        records.append({"bits":format(mask,f"0{N}b"),"shots":int(count),"units":mask.bit_count(),"score":score})
    fixed=sum(r["shots"] for r in records if r["units"]==c["units"])
    mean=sum(r["shots"]*r["score"] for r in records)/shots
    return json.dumps({"backend":str(backend_name),"shots":shots,"fixed_cardinality_rate":fixed/shots,
                       "mean_score":mean,"best_score":max((r["score"] for r in records),default=0),
                       "counts":records,"config":c},allow_nan=False)
