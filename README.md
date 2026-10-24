# Raghav Sharma — GitHub Pages portfolio

A responsive, dependency-free portfolio for https://generalized-ml.github.io.

## Publish

1. Create a public repository named `generalized-ml.github.io`.
2. Upload the contents of this folder directly to the repository root. Do not upload the ZIP or put everything in another nested folder.
3. Commit the files to `main`.
4. Open Settings → Pages → Deploy from a branch → main → / (root) → Save.
5. Open https://generalized-ml.github.io after deployment finishes.

## Included files

- `index.html`: page content and project cards.
- `style.css`: responsive layout and colors.
- `favicon.svg`: browser tab icon.
- `.nojekyll`: serves the files without Jekyll processing; keep this empty file.
- `README.md`: setup and editing instructions; not displayed on the homepage.

## Personalize before publishing

The project copy is a starter draft based on the supplied project names, not a verified description of their capabilities. Review all public-facing copy.

- Confirm your preferred name, headline, and About section in `index.html`.
- Replace the brief Pandas-Agent description with its actual problem, approach, and capabilities.
- Update the NEET, image-search, and ncert_rag descriptions and add their real repository links. They currently have no fabricated links or results.
- Add LinkedIn or a public contact email if desired.
- Add screenshots later by creating `assets/` and referencing images with relative paths.
- Change colors using the variables at the top of `style.css`.

## Preview locally

Open `index.html` directly in a browser, or from this directory run:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000.

No build step, JavaScript, package installation, API keys, or external fonts are required. This static website links to projects; it does not run Python agents or model inference.
