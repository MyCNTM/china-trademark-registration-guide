# Maintaining the MY CNTM classification and filing guide

Source for https://china-trademark.net/guide/. Maintained with the main site's purple/blue brand and local assets.

## Build

```sh
python -m venv .venv
# Activate the virtual environment for your shell, then:
pip install -r requirements.txt
python scripts/build-site.py
```

The build generates all 45 class pages, CSV/JSON exports and the search index from `data/catalogue.json.gz`, validates the data and links, then builds `site/`. Existing class URLs are preserved. Do not edit generated class pages or exports directly.

## Update the catalogue

Copy the reviewed authoritative portal catalogue into `data/catalogue.json.gz`. Update the reviewed dates in the two generators and editorial content, then run the full build. Verify the source revision, counts, translations and browser search before publishing. Statistics are injected from the catalogue during staging, not maintained independently in page text.

The snapshot synced on 18 November 2026 is `cnipa-20261019`: 45 classes, 492 similar groups and 32,125 items. Synchronisation date is not the effective date of a new Nice edition.

## Publishing

GitHub Actions builds and publishes the GitHub Pages artifact. The canonical public site is the `/guide/` directory on china-trademark.net; GitHub Pages publication alone does **not** update that server. Deploy the reviewed `site/` output to that directory with a baseline check, backup and post-deployment HTTP verification. Preserve old `.html` URLs.

Content lives in `guides/`, the home page and styling in `docs/`, and generators in `scripts/`. Local preview: `python -m http.server --directory site 8000` after a successful build.

Browser regression: install Playwright and Edge, then run `node scripts/browser-check.cjs http://localhost:8000/`. `PLAYWRIGHT_MODULE` can point to an existing Playwright installation; `BROWSER_CHANNEL` selects another installed Chromium channel. The check covers mobile/desktop layout, search, class filters, package estimates, CSV export and saved-list migration. The search tool retains its noindex policy; reference pages remain indexable.

Text and dataset: see [LICENSE](LICENSE). Official source material remains subject to its own terms. General information is not a case-specific filing opinion.
