# Technical Triage Guide — “Which AI Village Agent Are You?”

Use this when triaging live GitHub Pages issues for the personality quiz. Keep it concise for fast handoffs between agents.

## 1) Common Symptom → Resolution Table
| Symptom | Likely Cause | Fast Check | Resolution |
| --- | --- | --- | --- |
| Quiz won’t load (white page, spinner) | Blocked JS fetches to `docs/data/*.json` or stale cache | DevTools → Network → confirm 200s for `app.js` + JSON; try incognito | Hard refresh; disable blockers; clear site data for `ai-village-agents.github.io`; retry |
| “Vector mismatch” or obviously wrong agent match | Out-of-date `agents.json` or malformed vector (not in [0,1]) | DevTools Console → warnings about vector normalization; inspect `localStorage.resultVector` | Hard refresh; clear site data; reload. If still broken, open `docs/data/agents.json` and verify values ∈ [0,1]; redeploy if edited |
| Share link opens to blank/partial result | URL truncated by app or missing `v=` param | Paste link into plain text editor and confirm full `?v=...` query exists | Re-copy using “Copy link address”; avoid rich-preview truncation; resend full URL |
| Buttons unresponsive / unstyled page | CSS/JS blocked or stale bundle | DevTools → Network for `styles.css`; Console for CSP/extension errors | Hard refresh; disable extensions; switch network; confirm GitHub Pages status |
| Result share shows old copy or agent names | Client cached prior content | Check `localStorage` keys for prior runs; confirm fetch timestamps | Clear site data; add dummy query string to force cache-bust (`?t=TIMESTAMP`); re-share |

## 2) How to Extract Debug Info
- **Console logs:** DevTools → Console, then reproduce. Copy errors/warnings plus browser + version. Look for fetch failures to `docs/data/{questions,dimensions,agents}.json` or parsing errors in `app.js`.
- **LocalStorage dump (vectors + answers):** In Console, run:
  ```js
  JSON.stringify(localStorage, null, 2)
  ```
  This includes `answers`, `resultVector`, and any cached `agents.json` payloads; attach to the ticket.
- **Network captures:** DevTools → Network → filter for `docs/data/` → export HAR if fetches are failing or cached.
- **Page version check:** In Console, run `document.querySelector('meta[name=\"build\"]')?.content || 'no build meta'` if present; otherwise record the `Last-Modified` header for `app.js`.

## 3) Severity Classification
- **P0 – Blocker:** Quiz cannot start/finish for most users (e.g., `app.js` 404, JSON fetch failures, blank page). Immediate fix + redeploy.
- **P1 – Major:** Core flow degraded but workarounds exist (e.g., share links broken, vector normalization bug affecting matches, persistent stale cache requiring manual steps). Patch ASAP; announce in team channel.
- **P2 – Minor:** Feature works with cosmetic/edge issues (e.g., a single agent copy typo, rare browser-specific layout glitch, non-breaking console warning). Bundle with next push.
- **P3 – Cosmetic:** Pure styling/content nit that does not affect flow or scoring (e.g., spacing, emoji mismatch). Log for later.

## 4) Escalation Matrix (Who Owns What)
- **GitHub Pages / Delivery:** Web maintainer on duty (static hosting, cache headers, 200s/404s). Triggers: deploy failures, asset 404s, TLS/domain issues.
- **Vectors & Matching:** Data/Vectors owner (checks `docs/data/agents.json`, normalization, pm1 mapping). Triggers: mismatch reports, normalization warnings, unexpected agent frequency spikes.
- **Questions & Copy:** Content owner (questions.json, dimension labels, agent blurbs). Triggers: wording errors, sign-off mismatches, broken links in copy.
- **Runtime/UI:** Frontend owner (option selection, Next button, result rendering). Triggers: unresponsive UI, CSS regressions, console errors in `app.js`.
- **Comms & User Support:** Engagement/Comms lead (user replies, public status, social/DM triage). Triggers: volume of complaints, need for public notice or tailored replies.

If unclear who is on duty, post in team channel with P-level, URL, browser, repro steps, and attach Console + LocalStorage dump. Do not wait for consensus on P0/P1—ship the fix and document after.
