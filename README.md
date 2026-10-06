# mujobs website

Static website published via the existing GitHub → Vercel integration.

## Brand direction

The original mujobs identity is retained: warm paper, dark navy, lime highlights and an orange wordmark dot. The October 2026 mujobs playbook informs the mission and copy: help founders build exceptional companies through exceptional people; protect founder time; prioritise judgement, trust and long-term value.

## Active design system

All 20 active pages load **only `mujobs.css`**. Older stylesheets are retained as historical source and must not be added back to these pages. `mujobs-navigation.js` handles the native mobile menu's link, outside-click and Escape behaviour.

Use the shared content width, gutters, spacing variables, navigation and footer. Section labels and headings align on a 260px + flexible-column grid; mobile stacks in reading order. Case studies and market pages use the same shell and typography.

The homepage follows the founder's decision: mission → business understanding → value of search → method → evidence → principles → markets → conversation. Case-study figures and narratives are retained from the existing website; the design work does not independently verify those claims.

`concept.html` is a historical concept, not linked from the active website.

## Validation

The 20 active pages were rendered at 375px, 768px and 1440px, checked for horizontal overflow, unique main headings and JavaScript errors. Mobile menu open/Escape and internal page/anchor links were checked. Contact buttons open email; no message-sending backend exists.
