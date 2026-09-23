# Ohmly | Electronics eCommerce HTML Template

A static HTML5 / SCSS / vanilla JavaScript template for electronics stores, built for ThemeForest.

Live preview: connect this repo to Netlify with publish directory `HTML`.

## Pages (24)
Home 1 (annotated hero), Home 2 (editorial), Home 3 (category mosaic), Shop grid, Shop list, Shop full width,
Product details, Cart, Checkout, Order complete, Wishlist, Compare, Login, Register, Forgot password,
My account, Order tracking, About, Contact, FAQ, Blog, Blog details, 404, Coming soon.

## Structure
- `HTML/` - template pages, assets and SCSS source (this is what buyers upload)
- `Documentation/` - buyer documentation
- `Licensing/` - third-party asset licenses
- `tools/` - authoring scripts (page and image generators). Not included in the ThemeForest zip.

## Develop
```bash
npm install
npm run watch     # compile SCSS while editing
npm run build     # compile style.css
npm run build:min # compile style.min.css
bash tools/build.sh  # regenerate all pages + images from tools/pages.py and tools/images.py, then CSS
npm run zip       # package HTML, Documentation and Licensing for upload
```

Note: `tools/build.sh` overwrites every file in `HTML/*.html`. Edit `tools/pages.py` for changes you want to keep
across rebuilds, or stop using the generator and edit the HTML directly.

## Quality checks
- All 24 pages and style.css pass the W3C Nu HTML Checker with no errors or warnings.
- No jQuery and no third-party JavaScript.
