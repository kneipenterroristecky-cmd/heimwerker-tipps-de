# Einrichtungsanleitung – Heimwerker-Tipps Website

**Einmaliger Aufwand: ca. 45–60 Minuten**  
Danach läuft alles vollautomatisch.

---

## Schritt 1: GitHub-Repo erstellen

1. Gehe auf [github.com](https://github.com) und logge dich ein
2. Klicke oben rechts auf **"New repository"**
3. Name: `heimwerker-tipps-de`
4. Sichtbarkeit: **Public** (wichtig für GitHub Pages!)
5. Klicke auf **"Create repository"**

---

## Schritt 2: Code hochladen

Öffne PowerShell und führe diese Befehle aus:

```powershell
cd "C:\Users\D.Eck\Desktop\heimwerker-tipps-de"
git init
git add .
git commit -m "Initiales Setup"
git branch -M main
git remote add origin https://github.com/DEIN-GITHUB-USERNAME/heimwerker-tipps-de.git
git push -u origin main
```

**DEIN-GITHUB-USERNAME** ersetzen mit deinem echten GitHub-Benutzernamen.

---

## Schritt 3: GitHub Pages aktivieren

1. Gehe in deinem neuen Repo auf **Settings** → **Pages**
2. Branch: **main**, Ordner: **/ (root)**
3. Klicke auf **Save**
4. Deine Website ist nun erreichbar unter:  
   `https://DEIN-USERNAME.github.io/heimwerker-tipps-de/`

---

## Schritt 4: Secrets hinterlegen (einmalig)

Im Repo: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Name | Wert |
|---|---|
| `ANTHROPIC_API_KEY` | Dein Anthropic API Key (gleicher wie für die Versicherungsseite) |
| `SITE_URL` | `https://DEIN-USERNAME.github.io/heimwerker-tipps-de` |
| `AMAZON_TAG` | Dein Amazon Affiliate Tag (kommt nach Schritt 6) |

---

## Schritt 5: URL in Dateien anpassen

Ersetze in diesen Dateien `USERNAME` mit deinem echten GitHub-Benutzernamen:
- `index.html` (2x)
- `blog/index.html` (1x)
- `robots.txt` (1x)

Danach committen und pushen:
```powershell
git add .
git commit -m "URL angepasst"
git push
```

---

## Schritt 6: Amazon Affiliate Programm beitreten

1. Gehe auf [affiliate-program.amazon.de](https://affiliate-program.amazon.de)
2. Mit deinem Amazon-Konto einloggen
3. Website `https://DEIN-USERNAME.github.io/heimwerker-tipps-de/` eintragen
4. Thema: "Heimwerken & Do-it-yourself"
5. Nach Genehmigung (meist sofort): Deinen **Tracking-ID / Tag** notieren (z.B. `heimwerkertipp-21`)
6. Diesen Tag als GitHub Secret `AMAZON_TAG` hinterlegen (Schritt 4)

---

## Schritt 7: Impressum & Datenschutz ausfüllen

Öffne `impressum.html` und ersetze:
- `[DEIN NAME]` → z.B. Daniel Eck
- `[STRASSE HAUSNUMMER]` → deine Privatadresse (NICHT die Geschäftsadresse!)
- `[PLZ ORT]` → z.B. 98574 Schmalkalden
- `[DEINE-EMAIL@DOMAIN.DE]` → z.B. eine neue, separate E-Mail-Adresse

Dasselbe in `datenschutz.html`.

---

## Schritt 8: Google AdSense beantragen

**Erst wenn mindestens 20–30 Artikel online sind (nach ca. 2–3 Monaten):**

1. Gehe auf [adsense.google.com](https://adsense.google.com)
2. Mit einem Google-Konto (am besten neu anlegen) registrieren
3. Website-URL eintragen
4. AdSense bestätigt die Website (dauert 2–4 Wochen)
5. Nach Genehmigung: In `tools/blog_template_heimwerker.html` und `index.html` die AdSense-Kommentare durch echten Code ersetzen:

```html
<!-- ALT (auskommentiert): -->
<!-- <script async src="...?client=ca-pub-XXXXXXXXXXXXXXXX"... -->

<!-- NEU (aktiviert, mit deiner echten Publisher-ID): -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-DEINE-ID" crossorigin="anonymous"></script>
```

---

## Schritt 9: Google Search Console

1. [search.google.com/search-console](https://search.google.com/search-console) → "Property hinzufügen"
2. URL-Präfix: `https://DEIN-USERNAME.github.io/heimwerker-tipps-de/`
3. Sitemap einreichen: `sitemap.xml`

Das hilft Google, die Artikel schneller zu finden.

---

## Vollautomatischer Betrieb ab sofort

Nach dem Setup generiert GitHub Actions **jeden Montag und Donnerstag um 10 Uhr** automatisch:
- Einen neuen Heimwerker-Ratgeber-Artikel
- Aktualisierte `sitemap.xml`
- Aktualisierten Blog-Index

**Dein Aufwand: 0 Minuten pro Woche.**

---

## Erwarteter Einkommensverlauf

| Zeitraum | Artikel | Besucher/Monat | Einnahmen |
|---|---|---|---|
| Monat 1–3 | 25–35 | 100–300 | €5–20 |
| Monat 4–6 | 50–70 | 500–1.500 | €30–100 |
| Monat 7–12 | 80–120 | 1.500–4.000 | €80–280 |
| Jahr 2+ | 200+ | 5.000–15.000 | €200–600 |

SEO braucht Zeit – die ersten 3 Monate sind ruhig, danach wächst Traffic organisch.

---

## Support

Bei Fragen einfach Claude Code öffnen und fragen – alle Dateien sind kommentiert.
