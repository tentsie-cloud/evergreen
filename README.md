# Evergreen website

## Open the site on your Mac

Double-click **Start Evergreen.command**. It opens a Terminal window, starts a local web server and opens the website in your default browser. Keep that Terminal window open while viewing the site. Press Control+C in Terminal to stop it.

Do not open `index.html` directly: this website uses root-relative asset and page URLs, which require an HTTP server.

Alternatively, open Terminal in this folder and run:

```sh
python3 serve.py
```

The default address is http://127.0.0.1:8000/. If that port is busy, the launcher picks a free port and prints and opens the correct address. Python 3 is required; there are no package dependencies.

## Edit and rebuild

- `styles.css`: appearance and responsive layouts.
- `site.js`: mobile navigation and WhatsApp enquiry forms.
- `build.py`: page templates and shared business details.
- `src/catalogue.json`: category content.
- `src/products.json`: optional product records; currently empty because detailed inventory has not been confirmed.
- `assets/`: optimised copies of real supplied photography and video. Supplied originals remain unchanged in Downloads.

After editing templates or catalogue data, run `python3 build.py`, then refresh the browser. Serve the entire folder, including `products/`, `privacy/` and `assets/`.

Before publishing, set the confirmed website URL through the `SITE_URL` environment variable when running `build.py` to generate canonical URLs and a sitemap. Nothing has been deployed by this work.

The local server is for preview only, not public hosting. The yard section currently uses a wide nursery photograph. The portrait video has been removed at your request; a landscape replacement can be added when supplied. Review excerpts are dated and linked to the public directory source, rather than presented as a live overall Google rating.
