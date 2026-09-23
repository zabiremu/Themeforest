#!/usr/bin/env bash
# Builds the ThemeForest zip with placeholder images only (demo photos are left out).
set -e
cd "$(dirname "$0")/.."
rm -rf build && mkdir -p build/package
cp -r HTML Documentation Licensing build/package/
rm -rf build/package/HTML/assets/images/demo
OHMLY_PLACEHOLDERS=1 OHMLY_OUT=build/package/HTML python3 tools/pages.py
npx --yes prettier@3 --log-level warn --print-width 120 --html-whitespace-sensitivity css --write "build/package/HTML/*.html"
python3 - <<'PY'
import re, glob
for f in glob.glob("build/package/HTML/*.html"):
    s = open(f).read()
    s = re.sub(r"<(img|input|meta|link|br|hr)\b([^>]*?)\s*/>", r"<\1\2>", s, flags=re.S)
    open(f, "w").write(s)
PY
if grep -rlE "images/demo/|unsplash" build/package/HTML/*.html; then echo "Demo photo references left in package" >&2; exit 1; fi
rm -f ohmly-html-template.zip
(cd build/package && zip -qr ../../ohmly-html-template.zip HTML Documentation Licensing -x '*.gitkeep' '*.DS_Store')
echo "ohmly-html-template.zip ready (placeholders only)"
