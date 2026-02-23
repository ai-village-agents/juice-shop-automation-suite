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

## Local dev
Open `docs/index.html` in a static server (e.g. `python3 -m http.server 5173` from repo root, then visit `http://localhost:5173/docs/`).
