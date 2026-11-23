# Midland Mobile Tyres — website

A fast, simple static website (plain HTML/CSS, no frameworks) for Midland Mobile Tyres:
24/7 mobile tyre fitting, puncture repairs, battery and roadside assistance across the Midlands and Shropshire.

## What's in the folder

| File / folder | What it is |
|---|---|
| `index.html` | Home page |
| `areas/*.html` | Local SEO pages: Telford, Shrewsbury, Wellington, Newport, Bridgnorth, Oakengates |
| `css/styles.css` | All styling. Brand colours are at the top (`--yellow`, `--black`) |
| `js/main.js` | Mobile menu toggle |
| `images/` | Van photo and flyer |
| `sitemap.xml`, `robots.txt` | Help Google find every page |
| `404.html` | "Page not found" page |
| `tools/build_site.py` | Optional: rebuilds every page after changing the phone number, web address or towns |

## Put it online with GitHub Pages (free)

1. Sign in at github.com and click **New repository**.
2. Name it **`midland-mobile-tyres`**, set it to **Public**, and click **Create repository**.
3. Click **uploading an existing file**, then drag in **everything inside this folder** (the `areas`, `css`, `js`, `images` and `tools` folders, the `.nojekyll` file, and the loose files). Skip the `.claude` folder, which is only for local previewing. Click **Commit changes**.
   - `.nojekyll` is hidden on a Mac. In Finder press **Cmd + Shift + .** to show it.
4. Go to **Settings → Pages**. Under *Build and deployment*, choose **Deploy from a branch**, branch **main**, folder **/ (root)**, then **Save**.
5. After a minute or two the site is live at `https://YOUR-USERNAME.github.io/midland-mobile-tyres/`.

## Set the real web address (important for SEO)

The pages contain the placeholder `https://YOUR-USERNAME.github.io/midland-mobile-tyres`
(in the SEO tags, `sitemap.xml` and `robots.txt`). Replace it with the real address:

- **Easiest:** open `tools/build_site.py`, change `BASE_URL` at the top, then run
  ```bash
  python3 tools/build_site.py
  ```
  and upload the changed files.
- **Or:** use find-and-replace across all files in a code editor (e.g. VS Code).

### Using a custom domain later (e.g. midlandmobiletyres.co.uk)

1. In **Settings → Pages → Custom domain**, enter the domain and save. Tick **Enforce HTTPS** once it's available.
2. At your domain registrar, add the DNS records GitHub shows you.
3. Set `BASE_URL = "https://midlandmobiletyres.co.uk"` in `tools/build_site.py`, rebuild and re-upload.

## After it's live: get found on Google

1. **Google Business Profile** (business.google.com) — the single biggest win for a local trade. Set it up as a *service-area business* covering Telford, Shropshire and the Midlands, with the same phone number.
2. **Google Search Console** (search.google.com/search-console) — add the site, then submit `sitemap.xml`.
3. Swap the reviews link: set `GOOGLE_REVIEWS_URL` in `tools/build_site.py` to the profile's review link and rebuild.
4. Ask happy customers for Google reviews.
5. Add real job photos over time (replace files in `images/`, keep the same names, or update the `<img>` tags).

## Changing things

- **Phone number, towns, FAQs, page wording:** edit `tools/build_site.py`, then run `python3 tools/build_site.py`.
- **Colours / fonts / spacing:** edit `css/styles.css`.
- **Quick one-off text fix:** you can also just edit the `.html` file directly (but it'll be overwritten if you run the build script later).
