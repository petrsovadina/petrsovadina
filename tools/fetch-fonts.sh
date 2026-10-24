#!/usr/bin/env bash
# Downloads OFL fonts from google/fonts and creates the static instances gen.py expects.
set -euo pipefail
cd "$(dirname "$0")" && mkdir -p fonts && cd fonts
G=https://raw.githubusercontent.com/google/fonts/main/ofl
curl -fsSL -o Inter-var.ttf          "$G/inter/Inter%5Bopsz%2Cwght%5D.ttf"
curl -fsSL -o SpaceMono-Regular.ttf  "$G/spacemono/SpaceMono-Regular.ttf"
curl -fsSL -o SpaceMono-Bold.ttf     "$G/spacemono/SpaceMono-Bold.ttf"
python3 - <<'PY'
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
for w in (400, 500, 600, 700):
    for o in (14, 32):
        instancer.instantiateVariableFont(TTFont("Inter-var.ttf"), {"wght": w, "opsz": o}).save(f"Inter-{w}-o{o}.ttf")
PY
echo "fonts ready"
