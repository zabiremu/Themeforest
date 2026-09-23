#!/usr/bin/env bash
# Rebuild pages, images and CSS. Authoring tool only (not needed by buyers).
set -e
cd "$(dirname "$0")/.."
python3 tools/images.py
python3 tools/pages.py
npx --yes prettier@3 --log-level warn --print-width 120 --html-whitespace-sensitivity css --write "HTML/*.html"
python3 - <<'PY'
import re, glob
for f in glob.glob("HTML/*.html"):
    s = open(f).read()
    s = re.sub(r"<(img|input|meta|link|br|hr)\b([^>]*?)\s*/>", r"<\1\2>", s, flags=re.S)
    open(f, "w").write(s)
PY
npm run build --silent && npm run build:min --silent
