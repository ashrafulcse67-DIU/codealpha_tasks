# HisabCulator

A static multi-page calculation website: plain HTML, CSS and JavaScript. No framework, no build step for visitors, no dependencies.

## Run it
Open `site/index.html` in a browser, or upload the contents of `site/` to any static host.
(The optional "Fetch latest rates" button on the currency page needs the site to be served over http/https. It is blocked when opened from a file.)

## Before you publish (edit `tools/build.py`, top of file, then run `python3 tools/build.py`)
- `CONTACT_EMAIL` is a placeholder (`hello@hisabculator.example`). The contact form and contact page use it.
- `CONTACT_PHONE` and `SOCIAL` are empty and hidden until you fill them in.
- `SITE_URL` (e.g. `https://yourdomain.com`) switches on canonical URLs, og:url and `sitemap.xml`.

## Structure
```
site/                 the website (generated + hand-written assets)
  index.html about.html contact.html
  calculators/ converters/ education/ fitness/ date-time/
  assets/css/style.css          one design system
  assets/js/core.js             theme, Bangla toggle, nav, helpers
  assets/js/mathparse.js        safe expression parser (no eval / new Function)
  assets/js/grading.js          SSC/HSC and university grading rules (4th subject logic)
  assets/js/<tool>.js           one small script per tool
tools/build.py        generates every page so navbar, footer and SEO tags stay identical
```

## Add a tool
1. Add an entry to `TOOLS` in `tools/build.py` (name, Bangla name, description, SEO text, how-to, example, FAQ, related).
2. Add a UI function and register it in `UI` with the script(s) it needs.
3. Add `site/assets/js/<name>.js`, then run `python3 tools/build.py`. It appears in the navbar, home page and sitemap automatically.

## Notes
- Bangla mode translates navigation, headings, labels, results and tool names. The longer "How to use", example and FAQ text is English only.
- Currency rates built in are approximate reference values, not live.
- Preferences (theme, language, calculator history, edited rates) are stored in the visitor's own browser only.
