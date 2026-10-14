"""Build static content pages for pepminder.app from Markdown in _src/pages/.

GitHub Pages (Jekyll) does not publish folders that start with "_", so this source
folder stays private to the repo while the generated .html files are served.

Usage (from the repo root):
    pip install markdown==3.7
    python _src/build.py

Each page file starts with "key: value" header lines, then a line with "---",
then Markdown. Keys:
    title, description, path (output path, e.g. compare/pepminder-vs-regimen.html),
    date, modified (ISO dates), type (article | page), og_image (optional),
    cta (yes | no, default yes), faq (repeatable: "Question ||| Answer")
Edit the .md files, re-run the script, and commit both the .md and the .html.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
PAGES = Path(__file__).resolve().parent / "pages"
SITE = "https://pepminder.app"
PLAY = "https://play.google.com/store/apps/details?id=com.pepminder.pep_minder"

NAV = f"""<nav>
  <div class="container">
    <a href="/" class="nav-brand">
      <img src="/images/PepMinder_logo.svg" alt="PepMinder logo" width="36" height="36">
      PepMinder
    </a>
    <div class="nav-links">
      <a href="/#features">Features</a>
      <a href="/compare/">Compare</a>
      <a href="/blog/">Blog</a>
      <a href="{PLAY}" class="nav-cta" target="_blank" rel="noopener">Get the App</a>
    </div>
  </div>
</nav>"""

CTA = f"""<div class="cta-box">
  <h3>Try PepMinder free on Android</h3>
  <p>Reconstitution calculator, dose reminders, and an injection log in one private app. No account, works offline.</p>
  <a href="{PLAY}" class="cta-button" target="_blank" rel="noopener">Get it on Google Play</a>
</div>"""

LEGAL = """<p class="legal">PepMinder is a personal tracking and calculation tool. It does not provide medical
advice, diagnosis, dosing recommendations, or protocols, and it does not sell or link to any products.
Always consult a licensed healthcare provider about your treatment.</p>"""

FOOTER = f"""<footer>
  <div class="footer-links">
    <a href="/">Home</a>
    <a href="/compare/">Compare apps</a>
    <a href="/blog/">Blog</a>
    <a href="/no-account-peptide-tracker.html">Privacy-first tracking</a>
    <a href="/privacy.html">Privacy Policy</a>
    <a href="/terms.html">Terms</a>
    <a href="{PLAY}" target="_blank" rel="noopener">Google Play</a>
    <a href="https://alternativeto.net/software/pepminder/about/" target="_blank" rel="noopener">AlternativeTo</a>
  </div>
  <p>&copy; 2026 PepMinder. All rights reserved. Google Play and the Google Play logo are trademarks of Google LLC.
  Other app names are trademarks of their respective owners and are used only to identify them.</p>
</footer>"""


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    header, body = text.split("\n---\n", 1)
    meta = {"faq": []}
    for line in header.strip().splitlines():
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key == "faq":
            q, a = value.split("|||")
            meta["faq"].append((q.strip(), a.strip()))
        else:
            meta[key] = value
    return meta, body


def render(meta, body):
    url = f"{SITE}/{meta['path']}".replace("/index.html", "/")
    content = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    # Wrap tables so they scroll in their own box on narrow screens.
    content = re.sub(r"<table>", '<div class="table-wrap"><table>', content)
    content = content.replace("</table>", "</table></div>")
    content = content.replace("<p>[[CTA]]</p>", CTA)
    if meta.get("cta", "yes") == "yes" and CTA not in content:
        content += "\n" + CTA

    ld = [{
        "@context": "https://schema.org",
        "@type": "Article" if meta.get("type", "article") == "article" else "WebPage",
        "headline": meta["title"],
        "description": meta["description"],
        "author": {"@type": "Organization", "name": "PepMinder", "url": SITE},
        "publisher": {"@type": "Organization", "name": "PepMinder", "url": SITE},
        "datePublished": meta["date"],
        "dateModified": meta.get("modified", meta["date"]),
        "mainEntityOfPage": url,
    }]
    if meta["faq"]:
        ld.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in meta["faq"]
            ],
        })
    ld_html = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(item, indent=2, ensure_ascii=False)}\n</script>'
        for item in ld
    )
    og_image = meta.get("og_image", f"{SITE}/images/calculator_result.jpg")
    t, d = html.escape(meta["title"]), html.escape(meta["description"])
    d_iso = date.fromisoformat(meta.get("modified", meta["date"]))
    date_line = f"{d_iso:%B} {d_iso.day}, {d_iso.year}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t}</title>
  <meta name="description" content="{d}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:type" content="{'article' if meta.get('type', 'article') == 'article' else 'website'}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/images/PepMinder_logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/site.css">
{ld_html}
</head>
<body>

{NAV}

<article class="page">
  <p class="meta">Updated {date_line}</p>
{content}
{LEGAL}
</article>

{FOOTER}

</body>
</html>
"""


def main():
    built = []
    for src in sorted(PAGES.glob("*.md")):
        meta, body = parse(src)
        out = ROOT / meta["path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(meta, body), encoding="utf-8", newline="\n")
        built.append(meta["path"])
    print("\n".join(f"built {p}" for p in built))


if __name__ == "__main__":
    main()
