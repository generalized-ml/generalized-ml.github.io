"""Generate an offline interactive 3D visual. Run from any directory with Python 3."""
from pathlib import Path
import random, json
rng = random.Random(42)
points = []
for group, center in enumerate([(-1.1,-0.5,0.2),(1.0,-0.2,0.6),(0.0,1.0,-0.7)]):
    for _ in range(85):
        points.append([*[round(rng.gauss(c,0.32),4) for c in center],group])
template = (Path(__file__).with_name("visual-template.html")).read_text()
out = Path(__file__).resolve().parents[1] / "assets" / "latent-space.html"
out.parent.mkdir(exist_ok=True)
out.write_text(template.replace("__POINTS__",json.dumps(points)))
print(f"Generated {out}")
