"""Wrap the project's HTML fragment as a self-contained local browser preview."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
fragment=(ROOT/'preview'/'rover-chassis-concept.html').read_text(encoding='utf-8')
css='''
:root{color-scheme:dark;--background:#181b21;--foreground:#e7edf3;--muted-foreground:#99a6b8;--secondary-foreground:#d0d6df;--blue:#3ca6c0;--orange:#e8a254;--yellow:#d3b85c;--green:#57a77a;--purple:#9a85c2;--border:#363d48;--ring:#f2d59b;font:15px/1.5 system-ui,sans-serif}
body{margin:0;background:var(--background);color:var(--foreground)}main{max-width:1000px;margin:24px auto;padding:0 18px}h3{font-size:18px;font-weight:500;margin:0 0 8px}.viz-row,.viz-controls{display:flex;align-items:center;flex-wrap:wrap;gap:12px;margin:8px 0}.btn{font:inherit;color:var(--foreground);background:#272d36;border:1px solid var(--border);border-radius:7px;padding:7px 12px;cursor:pointer}.btn[aria-pressed=true]{background:#3ca6c0;color:#111820}.form-check{display:flex;align-items:center;gap:6px}.form-label{display:block;width:100%}.form-range{width:100%;accent-color:var(--blue)}.text-small{font-size:12px}.viz-badge{font-size:12px;color:#e8a254}.tabular-nums{font-variant-numeric:tabular-nums}a{color:var(--blue)}.cursor-interaction{cursor:grab}
'''
# srcdoc keeps the component isolated and reproduces its normal preview context.
document='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FNK0053 Modular Rover — Concept A</title><style>'+css+'</style></head><body><main>'+fragment+'</main></body></html>'
dest=ROOT/'docs'/'index.html'
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(document,encoding='utf-8')
print(dest)
