# Deekshith06.github.io

A deployment-ready, one-screen portfolio for `https://deekshith06.github.io/`.

## Design

- Uses a fixed `100dvh` application shell with no body or page scrolling.
- Keeps all portfolio sections on one HTML page.
- Uses accessible tabs for Overview, Projects, Skills, and Education.
- Includes responsive layouts for desktop, tablet, and mobile.
- Uses an optimized WebP ASCII portrait with a PNG fallback.
- Has no frameworks, package installation, or external runtime dependencies.

## Deploy the real GitHub Pages address

1. Create a **public** GitHub repository named exactly `Deekshith06.github.io`.
2. Upload the contents of this folder to the repository root.
3. Use `main` as the default branch.
4. Open **Settings → Pages** and set **Source** to **GitHub Actions**.
5. Confirm the included `Deploy GitHub Pages` workflow succeeds.
6. Open `https://deekshith06.github.io/`.

The separate `Deekshith06` repository must remain named `Deekshith06`; it controls the profile README shown on the GitHub account page.

## Local preview

Run this command from the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.


## Portrait animation

The portrait uses an animated WebP with an animated GIF fallback. Visitors who prefer reduced motion receive the clear static PNG.
