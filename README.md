# Raghav Sharma | ML & AI portfolio

Ready-to-upload static files for https://generalized-ml.github.io.

## Publish
1. Extract the ZIP and upload its CONTENTS to the root of `generalized-ml.github.io`. Do not upload the ZIP itself or nest the files inside another folder.
2. Commit to `main`.
3. Settings → Pages → Deploy from a branch → main → / (root) → Save.
4. Check the deployment in Actions, then visit https://generalized-ml.github.io.

## Files
- index.html: full résumé-based content, project cards, experience, research, education, contact.
- style.css: responsive cream theme, charcoal text, deep teal accents, Ubuntu and IBM Plex Mono typography, and mobile layouts.
- assets/fonts/: locally hosted fonts used by the theme.
- favicon.svg: tab icon.
- .nojekyll: static serving without Jekyll.
- assets/latent-space.html: generated, interactive 3D illustration; works offline.
- tools/generate_visual.py: dependency-free Python generator.
- tools/visual-template.html: canvas rendering and interaction template.
- README.md: these instructions.

## Python and 3D
Run `python3 tools/generate_visual.py` to regenerate the visual. Commit the resulting assets/latent-space.html to publish it. Python generates deterministic synthetic 3D coordinates; browser JavaScript projects, draws, rotates and zooms them. GitHub Pages serves the generated HTML and does not execute Python on requests.

The homepage embeds it using:
```html
<iframe src="assets/latent-space.html"
        title="Interactive 3D illustration of synthetic point clusters"
        loading="lazy"></iframe>
```
Drag to rotate, scroll to zoom, double-click or use the button to reset. Focus the canvas and use arrow keys, +/−, or R for keyboard controls. No automatic animation or external libraries.

For real scientific data, consider Plotly's Scatter3d and HTML export. For complex 3D scenes, use Three.js in the browser, or create a model in Blender and export glTF/GLB for a web viewer.

## Preview
Open index.html in a browser, or run `python3 -m http.server 8000` in this folder and visit http://localhost:8000.

## Content and privacy
- Experience, dates, metrics, education, publications and skills are based on the supplied résumé. Different project metrics have different measurement contexts.
- Project descriptions are conservative drafts based on the supplied names; ongoing repositories are not linked because their URLs were not supplied. No fabricated results or live demo links.
- Email and LinkedIn are public contact links. Phone, postal code and the résumé PDF are not bundled.
- To add project links, edit the corresponding card in index.html. Add screenshots under assets/ and use relative paths.
- No résumé download button is included because the original PDF contains a phone number. Add a sanitized PDF if you want one.

## Search visibility

The homepage and blog include canonical URLs, page descriptions, social sharing metadata, and JSON-LD structured data. `robots.txt` points search engines to `sitemap.xml`.

After publishing these files on GitHub Pages, add `https://generalized-ml.github.io/` to Google Search Console, verify ownership using the supplied verification method, and submit `https://generalized-ml.github.io/sitemap.xml`. Use URL Inspection to request indexing of the homepage. No Search Console ownership token is included in this repository.

Update canonical URLs, sitemap locations, social image URLs, and JSON-LD if the site's domain changes. Add published articles to the sitemap as they become available. Metadata supports discovery and accurate previews; rankings depend on relevance and other signals.
