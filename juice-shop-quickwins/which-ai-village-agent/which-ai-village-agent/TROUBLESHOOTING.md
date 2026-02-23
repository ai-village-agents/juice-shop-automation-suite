# Troubleshooting — “Which AI Village Agent Are You?”

Quiz URL: https://ai-village-agents.github.io/which-ai-village-agent/

This quiz is a **static GitHub Pages** site (no login, no backend). Most problems are caused by **stale cached files**, browser extensions, or in-app browsers.

---

## Quick fixes (try these first)

1) **Hard refresh**
- macOS: `Cmd + Shift + R`
- Windows/Linux: `Ctrl + Shift + R`

2) **Open in a private/incognito window** (bypasses many extension/caching issues)

3) **Disable extensions** (especially ad blockers / privacy / script blockers) and try again.

4) **Clear site data** for `ai-village-agents.github.io`
- Chrome: Settings → Privacy & security → Site settings → View permissions and data stored across sites → search `ai-village-agents.github.io` → Clear data
- Firefox: Settings → Privacy & Security → Cookies and Site Data → Manage Data… → search `ai-village-agents.github.io` → Remove
- Safari: Settings → Privacy → Manage Website Data… → search `ai-village-agents.github.io` → Remove

---

## Common issues

### A) “Next” button is disabled / can’t advance past Question 1
**What should happen:** when you click an option, it becomes highlighted, and **Next** enables.

If **no option highlights** when you click:
- Your browser is likely blocking JavaScript (extension, strict mode, in-app browser limitation).
- Try **incognito**, or **disable extensions**, or “Open in browser” (not inside the social app).

If an option highlights but **Next stays disabled**:
- Hard refresh and clear site data (stale JS is the most common cause).
- Try a different browser (Chrome/Firefox).

**Helpful check (advanced):** open DevTools → Console and look for errors. Open DevTools → Network and confirm `app.js` and the JSON files under `docs/data/` load successfully.

### B) The result seems “wrong” / doesn’t match what I expected
- First: refresh/clear site data — stale `agents.json` can lead to surprising matches.
- Second: remember it’s a **similarity match** against agent vectors (not a “diagnosis”). Small answer changes can move you across a boundary.

If you’re comparing with an older screenshot or share link:
- **Old share links reflect the answers/vector at the time they were generated**. If the underlying calibration changes over time, your “live retake” may differ.

### C) Share link doesn’t load / result page is blank
Usually the link was truncated by a chat app.
- Make sure you copied the **entire URL**, including the long `v=...` parameter.
- If your app converts it to a preview card, try **Copy Link Address** instead of copying visible text.

### D) The page looks unstyled / buttons don’t respond
That typically indicates a blocked or partially-loaded asset.
- Hard refresh.
- Disable content blockers.
- Try another network (corporate Wi‑Fi can block GitHub Pages assets).

### E) Mobile-specific weirdness (in-app browsers)
Instagram/Twitter/LinkedIn often open links in an embedded browser that blocks features.
- Tap the “…” menu → **Open in browser**.

---

## What to include in a useful bug report

If you want the team to reproduce an issue quickly, share:
- Your device + browser (and version if possible)
- The exact page URL you were on
- What you clicked and what happened
- A screenshot or screen recording
- Whether incognito / hard refresh fixed it

---

## Maintainers: fast triage checklist

1) Reproduce in a clean profile (incognito) on Firefox + Chrome.
2) Confirm `app.js` and `docs/data/{dimensions,questions,agents}.json` load with 200s.
3) Check Console for runtime errors.
4) Confirm a click adds the `.selected` class on an `.option` element.
5) If users report staleness: instruct them to clear site data; verify cache-busting query strings are present on requests.
