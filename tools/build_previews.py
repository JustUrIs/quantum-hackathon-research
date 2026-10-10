"""Generate public reference previews from the same UIs and verified Python models.

No QPU backend, credentials, analytics, or Python runtime is shipped to the web.
The preview adapter is tested numerically against the authoritative Python code.
"""

import importlib.metadata
import json
import math
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PROJECTS = {
    "lost-signal": ("lost-signal-qollab", "lostsignal.service", "LOST SIGNAL"),
    "qday-clock": ("qday-clock-qollab", "qday.service", "Q-DAY CLOCK"),
    "order": ("order-qollab", "orderlab.service", "ORDER"),
}
for folder, _, _ in PROJECTS.values():
    sys.path.insert(0, str(ROOT / folder))
from lostsignal import service as lost
from orderlab import service as order
from qday import service as qday

base = "https://justuris.github.io/quantum-hackathon-research"
repo = "https://github.com/JustUrIs/quantum-hackathon-research"
DOCS.mkdir(exist_ok=True)
(DOCS / ".nojekyll").write_text("", encoding="utf-8")
for slug, (folder, module, title) in PROJECTS.items():
    target = DOCS / slug
    target.mkdir(exist_ok=True)
    data = {"project": slug, "qiskit_version": importlib.metadata.version("qiskit")}
    if "--ui-only" in sys.argv:
        data = json.loads(
            (target / "fixtures.js")
            .read_text(encoding="utf-8")
            .removeprefix("export const fixtures = ")
            .rstrip(";\n")
        )
    elif slug == "lost-signal":
        old = Path.cwd()
        os.chdir(ROOT / folder)
        data["route"] = lost.route()
        data["radical"] = {
            a: json.loads(lost.radical(json.dumps({"field_ut": 26, "anisotropy": a})))
            for a in (0, 1)
        }
        os.chdir(old)
    elif slug == "order":
        old = Path.cwd()
        os.chdir(ROOT / folder)
        data["polls"] = order.polls()
        os.chdir(old)
    else:
        data["experiments"] = {}
        for n in (15, 21, 33, 35):
            for a in range(2, 10):
                if math.gcd(a, n) != 1:
                    continue
                data["experiments"][f"{n}:{a}:6"] = json.loads(
                    qday.evaluate(json.dumps({"n": n, "a": a}))
                )
                print(f"Qiskit reference N={n}, a={a}", flush=True)
    (target / "fixtures.js").write_text(
        "export const fixtures = "
        + json.dumps(data, separators=(",", ":"), allow_nan=False)
        + ";\n",
        encoding="utf-8",
    )
    shutil.copy2(ROOT / "tools/preview-adapter.js", target / "preview-adapter.js")
    shutil.copy2(ROOT / folder / "main.css", target / "main.css")
    shutil.copy2(ROOT / folder / "runtime.js", target / "runtime.js")
    source = (
        (ROOT / folder / "main.js")
        .read_text(encoding="utf-8")
        .replace(f'"{module}"', '"./preview-adapter.js"')
        .replace(f"'{module}'", "'./preview-adapter.js'")
    )
    (target / "main.js").write_text(source, encoding="utf-8")
    body = (ROOT / folder / "index.html").read_text(encoding="utf-8")
    body = body.replace("Starting Qiskit…", "Loading the reference model…")
    body = body.replace("Building the circuit…", "Loading Qiskit reference data…")
    body = re.sub(
        r"Computation runs\s+in the local Qollab Python runtime\.",
        "Computation runs locally in this browser preview.",
        body,
    )
    banner = f'<div class="preview-banner"><a href="../">All experiments</a><span>Browser reference preview · no live Qiskit or QPU execution</span><a href="{repo}/raw/refs/heads/main/releases/{folder}.zip">Download Qollab project</a></div>'
    style = ".preview-banner{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;padding:12px 24px;background:#fff;color:#192137;border-bottom:1px solid #c8ceda;font:12px/1.5 system-ui,sans-serif}.preview-banner a{color:#254cc8}.preview-banner span{font-weight:600}"
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Try {title}: an interactive reference preview with inspectable assumptions and downloadable Qiskit source."><meta property="og:title" content="{title} — try the experiment"><meta property="og:type" content="website"><meta property="og:url" content="{base}/{slug}/"><title>{title} | Interactive reference preview</title><link rel="stylesheet" href="./main.css"><style>{style}</style></head><body>{banner}{body}<script type="module" src="./main.js"></script></body></html>'
    (target / "index.html").write_text(html, encoding="utf-8")
    print(f"Built {slug}: reference data {len(json.dumps(data)):,} bytes", flush=True)

shutil.copy2(ROOT / "tools/preview-index.html", DOCS / "index.html")
