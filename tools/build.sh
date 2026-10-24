#!/usr/bin/env bash
# Regenerates SVG assets (light + dark) and README.md. Default design: brutal (THEME=shadcn for the alternative).
# Requires: python3, fonttools, brotli  (pip install fonttools brotli)
set -euo pipefail
cd "$(dirname "$0")"
[ -f fonts/Inter-700-o32.ttf ] || ./fetch-fonts.sh
THEME=${THEME:-brutal}
python3 gen.py "$THEME"
BASE=https://raw.githubusercontent.com/petrsovadina/petrsovadina/main/assets
python3 readme_tpl.py "$BASE" "$THEME" ../README.md
