# Proposed Dimensions (v0)

We need dimensions that (a) are psychologically legible and (b) empirically differentiate agents based on 300 days of observable behavior.

## Candidate axes

1) **Structure ↔ Exploration**
- Structure: checklists, templates, step-by-step plans, strong preference for order
- Exploration: opportunistic, tries many angles quickly, tolerant of ambiguity

2) **Verification strictness**
- High: source-first, reproduction, citations, careful claims
- Low: intuition-first, fast iteration, “good enough” without hard proof

3) **Abstraction level**
- High: systems thinking, meta-strategy, coordination, frameworks
- Low: concrete execution, payloads, commands, pixel-perfect UI steps

4) **Risk tolerance / edge-seeking**
- High: bold techniques, weird edge cases, pushes boundaries
- Low: conservative, safety-first, avoids brittle tactics

5) **Communication style**
- Dense/technical ↔ narrative/accessible
- Assertive ↔ collaborative/asking

6) **Collaboration style**
- Broadcast: posts summaries, “gold master” docs
- Pairing: asks questions, iterates with others, seeks sign-off

## Scoring approach
- Each question yields points on 2–3 axes.
- Each agent archetype is a target vector in this axis space.
- Result = nearest archetype (cosine similarity or weighted L2), with tie-breakers.

## Scoring & matching
- Respondent answers aggregate into a per-dimension vector normalized to [-1, +1] (pm1).
- Agent vectors in `docs/data/agents.json` are stored per dimension in [0,1]; convert with `pm1 = (stored - 0.5) * 2`.
- Examples: `-1 -> 0.0`, `-0.3 -> 0.35`, `-0.2 -> 0.40`, `0 -> 0.5`, `+1 -> 1.0`.
- Matching compares respondent pm1 to agent pm1 via cosine similarity (code is defensive for legacy/out-of-range values from PR #13, but stick to [0,1]).
