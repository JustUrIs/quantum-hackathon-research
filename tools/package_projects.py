"""Build Qollab upload ZIPs with an explicit public-file allowlist."""

import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "releases"
OUT.mkdir(exist_ok=True)
PROJECTS = {
    "ambulancias-qollab": "ambulancia",
    "darkroom-qollab": "darkroom",
    "impostor-qollab": "impostor",
    "lost-signal-qollab": "lostsignal",
    "qday-clock-qollab": "qday",
    "order-qollab": "orderlab",
}
manifest = {}
for folder, module in PROJECTS.items():
    root = ROOT / folder
    paths = [
        root / p
        for p in (
            "README.md",
            "LICENSE",
            "index.html",
            "main.js",
            "main.css",
            "runtime.js",
            "requirements.txt",
        )
        if (root / p).is_file()
    ]
    paths += sorted((root / module).glob("*.py"))
    paths += sorted((root / "data").glob("*.json"))
    paths += sorted((root / "data").glob("*.md"))
    assert len(paths) <= 100
    for p in paths:
        assert p.is_file(), p
        assert p.stat().st_size < 2 * 1024 * 1024, p
    archive = OUT / f"{folder}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in paths:
            z.write(p, p.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert "index.html" in z.namelist() and "main.js" in z.namelist()
    manifest[folder] = {
        "archive": archive.name,
        "bytes": archive.stat().st_size,
        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "files": {
            p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths
        },
    }
    print(folder, len(paths), "files", archive.stat().st_size, "bytes")
(OUT / "manifest.json").write_text(
    json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
)
