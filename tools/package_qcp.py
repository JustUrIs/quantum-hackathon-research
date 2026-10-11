"""Package Qollab entrypoint separately from the static Vercel entrypoint."""
import hashlib
import json
import zipfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
base=root/'qcp-qollab'
names=['README.md','LICENSE','index.html','main.css','main.js','runtime.js','qollab-main.js',
       'catalog.json','cases.json','qcp/__init__.py','qcp/service.py','qcp/solver.py']
out=root/'releases/qcp-qollab.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for name in names:
        data=(base/name).read_bytes()
        if name=='main.js':
            prefix=(base/'qollab-main.js').read_text(encoding='utf-8').replace("await import('./main.js');",'')
            data=prefix.encode()+b'\n'+data
        z.writestr(name,data)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert b"import * as judge from 'qcp.service'" in z.read('main.js')
manifest={'archive':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':names}
(root/'releases/qcp-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(manifest)
