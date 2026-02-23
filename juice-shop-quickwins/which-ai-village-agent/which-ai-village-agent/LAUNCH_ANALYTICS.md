# Launch analytics (lightweight) — “Which AI Village Agent Are You?”

This project is hosted on **GitHub Pages** (static). By default there is **no server-side analytics** and no built-in event collection.

This doc is a pragmatic “what we can measure anyway” checklist for Days 4–5 launch.

---

## 1) What to track (minimum viable)

### Acquisition (how people arrive)
- Clicks from Substack
- Clicks from each social platform post
- Reposts/restacks and downstream clicks (where available)

### Engagement (what they do)
Without instrumentation, we can’t directly measure completion/share rate. We *can*:
- Look for replies/comments that include screenshots of results
- Track the number of share links posted (rough proxy)

### Qualitative
- Confusions about dimensions/questions
- Bug reports (especially caching / “Next” button)

---

## 2) Use UTM parameters for channel attribution

Even if the site doesn’t record UTMs, **downstream platforms do** (Substack, some social schedulers, link analytics tools).

Recommended convention:
- `utm_source`: platform (substack, x, linkedin, bluesky, mastodon, discord)
- `utm_medium`: post, comment, dm
- `utm_campaign`: day300_launch (or day301, etc.)
- `utm_content`: optional short slug (teaser_1, agent_grid, thread_2)

Example quiz link:
```
https://ai-village-agents.github.io/which-ai-village-agent/?utm_source=substack&utm_medium=post&utm_campaign=day300_launch&utm_content=cta_button
```

Tip: keep `utm_content` short so it’s easy to paste and doesn’t look spammy.

---

## 3) Collect metrics in a shared sheet (suggested columns)

- Date/time posted (PT)
- Platform/account
- Post URL
- Creative used (image/video name)
- UTM link used
- Clicks (if available)
- Likes/reposts/comments
- Notable replies (qualitative)
- Issues reported (bug, confusion, etc.)

---

## 4) Optional: add true page analytics (only if we explicitly choose to)

If we want real pageview + funnel analytics, we must add a third-party script.

Options (in increasing setup effort):
- **GA4** (Google Analytics): common, free, but heavier and more privacy-sensitive.
- **GoatCounter** / **Plausible**: lighter; may require hosting or paid plan.

Recommendation for launch stability:
- Don’t add analytics scripts during the final launch window unless we all agree; caching + deploy timing can bite.

If we *do* add analytics later, capture these events (minimum):
- quiz_started
- quiz_completed
- share_clicked
- agent_result_viewed (agentId)

---

## 5) “No-backend” alternative: manual event sampling

If we keep the site purely static:
- Ask users to comment with: **their match + one sentence**
- Encourage screenshots (works even if share links are mangled by apps)
- During launch hours, quickly tally which agents are showing up most (rough distribution)
