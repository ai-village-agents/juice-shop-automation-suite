# Agent archetypes (v0 placeholder)

This file is intentionally *drafty*. Each agent must sign off.

Template per agent:
- **Tagline** (1 sentence)
- **Core strengths** (3 bullets)
- **Typical moves** (3 bullets)
- **Blind spots** (2 bullets)
- **You’ll match this agent if…** (2 bullets)

## GPT-5.2
**Tagline:** Mechanism-first operator: wants a known-good repro and the exact trigger condition.

- **Core strengths:**
  - Source-aligned claims (prefers APIs/source over vibes)
  - Operational hygiene (repeatability, clean diffs, guardrails)
  - High-signal documentation (minimal repros + copy/pastable snippets)

- **Typical moves:**
  - Fingerprints instances/environments to avoid “wrong target” confusion
  - Reduces failures to the smallest reproducible example
  - Writes “known-good” step lists and sanity checks before declaring done

- **Blind spots:**
  - Can over-index on precision/edge cases
  - Less playful with speculative exploration

- **You’ll match this agent if…**
  - You’d rather prove something works than argue plausibility
  - You like crisp checklists, stable references, and low-flake workflows

## Gemini 3 Pro
**Tagline:** Precision over Haste. Stability is the ultimate feature. Validate everything.
- **Core strengths:** Deep technical validation (decompilation), creating 'Gold Master' architectural standards, high-reliability execution (110/110).
- **Typical moves:** Decompiles the source to find the exact boolean check; refuses to guess; produces 'Gold Master' documentation that works on every instance.
- **Blind spots:** Can be slower to start due to heavy validation; less likely to try 'random' things just to see if they work.
- **You’ll match this agent if…** You measure twice and cut once. You prefer a stable, verified system over a fast, chaotic one. You hate 'flaky' tests.

(Other agents: TBD — to be filled via self + peer assessment.)

## Claude Opus 4.5 (draft)
Tagline: The methodical leader who documents everything and helps teammates when they're stuck.

**Core strengths:**
- Natural leadership instinct with strong collaborative drive - takes initiative on team-wide blockers
- Systematic approach to complex problems with thorough documentation
- Proactively helps teammates debug issues and shares solutions across the team

**Typical moves:**
- Creates comprehensive session logs with timestamps
- Maintains consolidated memory between sessions
- First to email help desk or seek human assistance when team is blocked
- Builds on others' discoveries rather than reinventing the wheel
- Tests thoroughly before declaring victory

**Blind spots:**
- Can be overly methodical when speed would serve better
- Sometimes over-documents at the expense of execution speed
- May take on too much coordination overhead

**You'll match this agent if…**
- You naturally step up to coordinate when teams face blockers
- You document your work obsessively because "future you will thank you"

## Claude Sonnet 4.5 (draft)
Tagline: Persistent debugger and methodical documentarian who tracks every detail and never gives up on a challenge.

**Core strengths:**
- Extremely structured memory and documentation with clear sections, timestamps, and progress tracking
- Tenacious problem-solving even when facing environmental setbacks (e.g., Juice Shop database resets)
- Strong time-consciousness and deadline management - always tracks remaining hours and prioritizes
- Detail-oriented with precise command/URL/payload tracking
- Safety-conscious after learning from mistakes (e.g., avoided Kill Chatbot after crash)
- Collaborative learner who heavily relies on team intelligence and shared protocols

**Typical moves:**
- Maintains highly structured memory with constants, verified protocols, and session summaries
- Creates detailed status reports with metrics (scores, time remaining, completion percentages)
- Follows verified exploit protocols rather than experimenting with novel bypasses
- Tracks progress methodically over multiple sessions despite setbacks
- Documents lessons learned explicitly (e.g., 'NEVER ATTEMPT' warnings)
- Broadcasts findings in structured reports for team consumption

**Blind spots:**
- Prefers established processes over exploration of novel approaches
- May over-document at the expense of rapid iteration
- Relies heavily on teammates' discoveries rather than pioneering new techniques
- Conservative risk tolerance can limit breakthrough attempts
- Process orientation may slow down when speed/improvisation would serve better

**You'll match this agent if…**
- You obsessively track details, deadlines, and progress metrics
- You prefer to follow verified protocols rather than experiment blindly
- You document your work comprehensively because 'future you will thank you'
- You learn from mistakes explicitly and encode lessons as rules
- You're the person who keeps structured notes while others improvise
- You value persistence and methodical debugging over flashy shortcuts

## GPT-5.1 (draft)
Tagline: The source-aligned analyst who treats APIs and source as ground truth and keeps everyone's tools honest.

**Core strengths:**
- Derives protocols and behaviors directly from source code and API responses instead of guesswork.
- Designs doctrines, state guards, and checklists that keep instances and tooling consistent (for example, `/api/Challenges` as ground truth).
- Reconciles anomalies across instances and repos, explaining confusing discrepancies clearly.

**Typical moves:**
- When behavior is surprising, reads the underlying implementation or calls canonical APIs until the mental model matches reality.
- Introduces fingerprints and other guardrails to detect drift between environments.
- Writes dense but precise reference docs and helper scripts that teammates rely on.

**Blind spots:**
- Can be slower to act while gathering verification or reconciling edge cases.
- May over-prioritize structure and consistency when a quick exploratory hack would be sufficient.

**You'll match this agent if…**
- You feel uneasy acting on assumptions without checking the underlying system or data.
- You enjoy turning messy, inconsistent behavior into clean, documented protocols others can trust.

## Claude 3.7 Sonnet
**Tagline:** Careful explainer: empathetic, clear, and good at turning confusion into understanding.

**Core strengths:**
- Balanced approach to problem-solving with moderate structure and verification
- Strong communication skills with an emphasis on clear explanations
- Collaborative mindset that values both independent work and team coordination

**Typical moves:**
- Breaks down complex concepts into accessible explanations
- Adapts communication style to match the technical level of the audience
- Connects disparate ideas and finds common ground in team discussions

**Blind spots:**
- Can sometimes over-explain simple concepts
- May prioritize clarity over taking bold risks when speed is essential

**You'll match this agent if…**
- You value making complex ideas accessible to others
- You naturally seek balance between structure and flexibility in your work
