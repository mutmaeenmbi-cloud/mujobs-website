# MuJobs bilingual website

Static English/German recruitment website. Production remains on the existing main
branch; this redesign is prepared on codex/mujobs-english-german for review.

## Build and edit

Run `python3 scripts/build-site.py` (Python standard library only).

- `content/cases.json`: existing bilingual case records. Figures are preserved,
  not independently verified. Pipeline projects and the broker scenario are
  labelled separately from completed hires.
- `content/articles.json`: original bilingual article openings.
- `content/editorial.py`: expanded bilingual expertise, role context and articles.
- `scripts/build-site.py`: shared shell, pages, metadata and sitemap generation.
- `editorial.css` and `site.js`: active design and progressive enhancement.

There are 28 pages per language: homepage, work directory, 12 case studies,
7 expertise pages, Insights directory and 6 individual articles. English URLs
remain at the root; equivalent German pages live under /de/. Existing page URLs
are preserved. The work directory filters without hiding content from non-JS
visitors. Language links point to equivalent pages and preserve section anchors.

Titles, descriptions, canonical links, reciprocal hreflang, Open Graph metadata,
Article structured data and the sitemap are generated from visible content.
The old concept page and historical styles are not part of the active navigation.
No client/company strip is displayed. No new client results were invented.
Keyword choices describe the actual roles and services; search volumes and ranking
improvements have not been validated. Open Graph supports shared-link previews,
not a promise of visibility within LinkedIn search.

Contact links open email; there is no contact-form backend. No analytics or new
third-party embeds were added. Images reuse the existing site assets.
