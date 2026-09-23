# Demo photos (live preview only)

Put real product photos here to show them on the live demo. They are never
included in the ThemeForest download: `npm run zip` rebuilds the pages with
the original SVG placeholders and leaves this folder out.

Use the same file name as the placeholder, with .jpg, .webp or .png:

| Folder       | File names                                                                 | Size        |
|--------------|----------------------------------------------------------------------------|-------------|
| products/    | headphones, headphones-side, headphones-case, headphones-detail, earbuds,  | 1000 x 1000 |
|              | phone, laptop, watch, speaker, controller, tablet, camera, keyboard,       |             |
|              | powerbank, monitor                                                         |             |
| categories/  | audio, phones, laptops, wearables, gaming, cameras                         | 800 x 800   |
| hero/        | hero-headphones (Home 1, dark panel), laptop-on-dark (Home 2, dark panel), | 1200 x 900  |
|              | headphones-on-color (Home 3, lime panel)                                   | 800 x 800   |
| blog/        | blog-1 ... blog-6                                                          | 1200 x 750  |

Tips for a clean, consistent look:
- Products on a plain white or very light grey background. White blends into
  the card automatically, so the product looks cut out.
- Hero photos: transparent PNG works best. On the dark panels a photo with a
  dark background also works.
- Then run `bash tools/build.sh` (or `python3 tools/pages.py`) and commit.
- Only use photos you have the right to use (Unsplash, Pexels or your own).
