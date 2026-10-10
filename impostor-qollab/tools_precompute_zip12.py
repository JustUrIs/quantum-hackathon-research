"""Offline: precompute the n=12 zip curve shipped as data/zip_n12.json (too slow for the browser)."""
import json
from impostor import games as g
n, trials, layers, seed = 12, 6, 24, 1
ks = [12, 48, 96, 192, 384, 768, 1536, 3072, 6144]
pts = []
for k in ks:
    x = g.zip_impostor_xeb(n, k, trials, layers, seed)
    pts.append({"k": k, "xeb": x}); print(k, round(x, 4), flush=True)
out = {"n": n, "layers": layers, "trials": trials, "impostor": pts,
       "quantum": g.zip_quantum_xeb(n, trials, layers, seed), "paper": g.ZIP_PAPER, "precomputed": True}
json.dump(out, open("data/zip_n12.json", "w"), indent=1)
print("quantum", out["quantum"])
