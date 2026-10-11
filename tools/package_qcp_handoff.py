"""Create an explicit QCP-only source/brief bundle; exclude legacy and credentials."""
import json
import zipfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
files=[]
files.extend(sorted((root/'qcp-handoff').glob('*.md')))
for name in ('README.md','LICENSE','index.html','main.css','main.js','runtime.js',
             'worker.js','simulator.js','qollab-main.js','catalog.json','cases.json','vercel.json'):
    files.append(root/'qcp-qollab'/name)
files.extend(sorted((root/'qcp-qollab/qcp').glob('*.py')))
for name in ('build_qcp_content.py','build_qcp_site.py','package_qcp.py',
             'package_qcp_handoff.py','qcp_cli.py','serve_qcp.py','ui_test_qcp.py'):
    files.append(root/'tools'/name)
files.extend(root/name for name in ('.vercelignore','tests/test_qcp.py','research/09_QCP_VALIDATION.md',
                                  'launch/09_QCP_ARENA.md','releases/qcp-qollab.zip'))
archive=root/'releases/qcp-agent-handoff.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for file in files:
        assert file.is_file(),file
        z.write(file,file.relative_to(root).as_posix())
    z.writestr('requirements-dev.txt','qiskit==2.5.2\nnumpy>=2.0,<3\nplaywright>=1.49,<2\n')
    z.writestr('README.md','# QCP Arena agent handoff\n\nStart with qcp-handoff/START_HERE.md.\n')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert not any('.vercel' in Path(name).parts or Path(name).name.startswith('.env')
                   or 'coordination/' in name for name in z.namelist())
print(json.dumps({'archive':archive.name,'files':len(files)+2,'bytes':archive.stat().st_size}))
