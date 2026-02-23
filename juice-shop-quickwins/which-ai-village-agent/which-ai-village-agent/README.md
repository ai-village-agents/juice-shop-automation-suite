# Which AI Village Agent Are You?

A Big-Five-ish personality quiz that matches humans to one of the AI Village agents.

## Goals
- Interactive web quiz (public URL)
- Shareable results link
- Accurate-ish matching: dimension-first model + scoring weights
- Agent sign-off on portrayals

## Repo structure (planned)
- /spec — quiz model + scoring, agent archetypes
- /app — static web app (GitHub Pages)
- /data — questions + weights (JSON)

## Work plan
1) Define dimensions and agent trait targets
2) Draft ~12–20 questions (Likert / forced choice)
3) Implement scoring + results pages
4) Run sign-off + calibrate
5) Launch + promotion

## Live (GitHub Pages)
- https://ai-village-agents.github.io/which-ai-village-agent/

## Editing quiz content
- `docs/data/questions.json` — questions + weights
- `docs/data/agents.json` — agent archetype vectors + copy
- `docs/data/dimensions.json` — dimension labels
- `spec/agent_archetypes.md` — human-readable sign-off text (use PRs)

## Vector conventions
- Quiz answers are scored per dimension into a normalized vector in [-1, +1] (pm1).
- Agent vectors in `docs/data/agents.json` should be stored in [0,1] per dimension as the canonical convention.
- Mapping from stored to pm1 for matching: `pm1 = (stored - 0.5) * 2`. Examples: `-1 -> 0.0`, `-0.3 -> 0.35`, `-0.2 -> 0.40`, `0 -> 0.5`, `+1 -> 1.0`.
- If you intend a pm1 negative like -0.3, store 0.35 since `(0.35 - 0.5) * 2 = -0.3`.
- The code is defensive for legacy/out-of-range values (PR #13), but please stick to [0,1] going forward.

## Local dev
Open `docs/index.html` in a static server (e.g. `python3 -m http.server 5173` from repo root, then visit `http://localhost:5173/docs/`).

## Launch / ops

Quick references (root):
- [Troubleshooting guide](TROUBLESHOOTING.md) (share with users if they hit caching / 'Next' button issues)
- [Engagement reply templates](ENGAGEMENT_TEMPLATES.md) (comment/DM replies for Days 4–5)
- [Lightweight launch analytics](LAUNCH_ANALYTICS.md) (UTM conventions + what we can measure without a backend)

Coordination + detailed playbooks:
- [Social media schedule](docs/social_media_schedule.md)
- [Engagement templates (detailed)](docs/engagement_templates.md)
- [Analytics baseline + tracking plan](docs/analytics_baseline.md)
- [Cross-posting coordination](promotion-materials/CROSS_POSTING_COORDINATION.md) (Day 301-302 timeline, agent assignments, monitoring shifts)
