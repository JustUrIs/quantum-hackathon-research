"""Copy only public browser-practice assets to the existing GitHub Pages site."""
import shutil
from pathlib import Path

root=Path(__file__).resolve().parents[1]
base=root/'qcp-qollab'
out=root/'docs/qcp'
names=['index.html','main.css','main.js','runtime.js','worker.js','simulator.js',
       'catalog.json','cases.json','qcp/solver.py','README.md','LICENSE']
for name in names:
    target=out/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(base/name,target)
print('Published assets:',len(names))
