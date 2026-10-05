# mujobs website

Static recruitment website deployed through the existing GitHub → Vercel integration.

## Design system

All 21 HTML entry points share `site.css`, `site.js`, accessible navigation and a common footer. The design uses white and charcoal surfaces, restrained orange accents, responsive editorial typography, native expandable content and locally hosted imagery.

- Homepage: approach, selected work, six markets and contact links.
- Twelve case studies: existing source metrics and narratives, section navigation and related work.
- Six market pages: role experience, search approach and relevant cases.
- Insights: expandable articles with readable text.
- `concept.html`: retained as a compatible alternate entry point.

Historical CSS files remain in the repository for reference but are not loaded by the redesigned pages. Contact actions open email; no contact submission backend is introduced.

## Assets

The three photographs in `assets/` were downloaded from Unsplash URLs already used by the previous website. They are illustrative workplace/architecture imagery, not client premises or photographs of the mujobs team.

## Verification

Check all local page links and anchor targets, image loading, desktop/mobile layouts, menu keyboard behavior, case navigation and expandable insights before deployment.
