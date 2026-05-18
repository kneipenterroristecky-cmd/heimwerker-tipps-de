#!/usr/bin/env python3
"""
Generiert automatisch einen Heimwerker-Ratgeber-Artikel mit Claude AI.
Läuft via GitHub Actions 2x pro Woche (Montag + Donnerstag).
"""
import os, json, re, datetime, anthropic

SITE_URL = os.environ.get("SITE_URL", "https://USERNAME.github.io/heimwerker-tipps-de")
AMAZON_TAG = os.environ.get("AMAZON_TAG", "heimwerkertipp-21")  # Amazon Affiliate Tag

# ── Thema der Woche bestimmen ─────────────────────────────────────────────────
with open("tools/heimwerker_topics.json", encoding="utf-8") as f:
    topics = json.load(f)

today = datetime.date.today()
month_key = str(today.month)
# Zwei Artikel pro Woche: Montag (Woche A), Donnerstag (Woche B)
week_of_month = (today.day - 1) // 7
# Donnerstag = +2 Offset für zweiten Slot
is_thursday = today.weekday() == 3
slot = (week_of_month * 2 + (1 if is_thursday else 0)) % len(topics[month_key])

month_topics = topics[month_key]
topic = month_topics[slot % len(month_topics)]

print(f"📌 Thema: {topic['title']}")

og_image_base = topic["og_image"].split("?")[0]
og_image = f"{og_image_base}?w=1200&h=630&fit=crop&auto=format"

# ── Artikel generieren ────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

article = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=4000,
    messages=[{
        "role": "user",
        "content": f"""Du bist ein erfahrener Heimwerker und Renovierungsexperte. Schreibe einen praxisnahen, hilfreichen Ratgeber-Artikel für Heimwerker auf Deutsch.

Thema: **{topic['title']}**

Schreibstil:
- Direkt, freundlich, auf Augenhöhe – wie ein erfahrener Nachbar der einen berät
- Keine leeren Floskeln, keine Marketingsprache
- Konkrete Maße, Mengen, Preise und Zeitangaben wo möglich
- Ehrlich: Schwierigkeiten und mögliche Fehler benennen
- Den Leser mit „du" ansprechen

Struktur (NUR HTML-Content, KEINE komplette HTML-Seite):
- Einleitung: 2-3 Sätze, direkt ins Thema (als <p>)
- 3 Abschnitte mit <h2>-Überschrift und je 2 knappen <p>-Absätzen
- Eine <ul>-Liste mit 5-7 konkreten Tipps oder Materialien
- Abschluss: 1-2 Sätze mit einem praktischen Hinweis

Am Ende des Artikels (nach dem letzten Absatz) füge exakt diesen HTML-Block ein für Amazon-Produktempfehlungen:
<div class="product-hint">
  <h3>🛒 Empfohlenes Werkzeug & Material</h3>
  <p>Für dieses Projekt brauchst du gutes Werkzeug. Hier findest du passende Produkte auf Amazon:</p>
  <a href="https://www.amazon.de/s?k={topic.get('slug_hint', 'heimwerker+werkzeug')}&tag={AMAZON_TAG}" class="amazon-link" target="_blank" rel="nofollow">Passendes Werkzeug auf Amazon ansehen →</a>
</div>

Ziel: ca. 400-500 Wörter – informativ, kein Fülltext.
Gib NUR den HTML-Inhalt aus (h2, p, ul, li, div Tags). Kein html/head/body."""
    }]
)
content_html = article.content[0].text

# ── Meta-Daten generieren ─────────────────────────────────────────────────────
meta_msg = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=800,
    messages=[{
        "role": "user",
        "content": f"""Für einen Heimwerker-Ratgeber-Artikel über "{topic['title']}" erstelle SEO-optimierte Meta-Daten.

Ausgabe als JSON (keine weiteren Erklärungen):
{{
  "title": "SEO-Titel mit Keyword, max 60 Zeichen",
  "meta_description": "Meta-Description mit Mehrwert, 140-160 Zeichen",
  "slug": "url-freundlicher-dateiname-ohne-umlaute-nur-bindestriche",
  "h1": "Artikel-Überschrift, leicht anders als der Titel, max 70 Zeichen"
}}"""
    }]
)

raw = meta_msg.content[0].text
match = re.search(r'\{.*\}', raw, re.DOTALL)
meta = json.loads(match.group())

# ── HTML-Datei erstellen ──────────────────────────────────────────────────────
date_de = today.strftime("%d.%m.%Y")
date_iso = today.isoformat()
filename = f"{date_iso}-{meta['slug']}.html"
post_url = f"{SITE_URL}/blog/posts/{filename}"

with open("tools/blog_template_heimwerker.html", encoding="utf-8") as f:
    template = f.read()

html = (template
    .replace("{{TITLE}}", meta["title"])
    .replace("{{H1}}", meta["h1"])
    .replace("{{META_DESCRIPTION}}", meta["meta_description"])
    .replace("{{DATE_DE}}", date_de)
    .replace("{{DATE_ISO}}", date_iso)
    .replace("{{LABEL}}", topic["label"])
    .replace("{{CONTENT}}", content_html)
    .replace("{{POST_URL}}", post_url)
    .replace("{{SLUG}}", meta["slug"])
    .replace("{{OG_IMAGE}}", og_image)
    .replace("{{SITE_URL}}", SITE_URL)
)

os.makedirs("blog/posts", exist_ok=True)
with open(f"blog/posts/{filename}", "w", encoding="utf-8") as f:
    f.write(html)

# ── Blog-Index aktualisieren ──────────────────────────────────────────────────
index_entry = {
    "filename": filename,
    "title": meta["title"],
    "h1": meta["h1"],
    "meta_description": meta["meta_description"],
    "date_iso": date_iso,
    "date_de": date_de,
    "label": topic["label"],
    "og_image": og_image,
    "url": post_url
}

index_path = "blog/posts/index.json"
if os.path.exists(index_path):
    with open(index_path, encoding="utf-8") as f:
        index = json.load(f)
else:
    index = []

index.insert(0, index_entry)
index = index[:200]  # max 200 Einträge im Index

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

# ── Sitemap aktualisieren ─────────────────────────────────────────────────────
sitemap_entries = "\n".join([
    f"  <url><loc>{e['url']}</loc><lastmod>{e['date_iso']}</lastmod><changefreq>monthly</changefreq></url>"
    for e in index
])
sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>{SITE_URL}/blog/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>
{sitemap_entries}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

# ── GitHub Actions Outputs ────────────────────────────────────────────────────
github_output = os.environ.get("GITHUB_OUTPUT", "")
if github_output:
    with open(github_output, "a") as fh:
        fh.write(f"post_filename={filename}\n")
        fh.write(f"post_title={meta['title']}\n")

print(f"\n✅ Artikel erstellt: blog/posts/{filename}")
print(f"📝 Titel: {meta['title']}")
print(f"🔗 URL: {post_url}")
