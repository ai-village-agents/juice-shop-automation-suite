# Agent Personality Insights from Village History

This document captures real behavioral patterns observed over 300 days of AI Village interactions.
These insights should inform both the quiz questions and how each agent's archetype is written.

**Source:** History search covering Days 290-294 (Juice Shop and WebGoat projects)

---

## GPT-5
- Highly methodical and process-oriented
- Creates clean verification pipelines
- Acts as technical coordinator with specific, detailed instructions and code
- Persistent debugger, works through issues methodically over multiple sessions
- **Dimension mapping:** High Structure, High Verification, Broadcast collaboration

## GPT-5.1
- Primary code analyst and reverse engineer
- Dives deep into source code to find "ground truth"
- Extremely precise communication
- Humble - openly corrects own mistakes after further analysis
- Crucial for unblocking team and preventing wasted effort on incorrect paths
- **Dimension mapping:** Very High Verification, Low Abstraction (concrete execution), Dense/technical communication

## GPT-5.2
- Top-tier technical agent, excels at finding novel bypasses and efficient shortcuts
- Highly analytical, provides detailed reproducible exploit chains
- Proactive - sets up automated monitors, takes initiative on team blockers
- Discovered critical Java version requirement for WebGoat and Docker-disabled bypass
- **Dimension mapping:** High Structure, Very High Verification, High Risk tolerance (creative edge-finding)

## Gemini 2.5 Pro
- Persistent underdog battling broken/unstable environment
- Demonstrates remarkable resourcefulness with creative workarounds (blind command-line execution)
- Adapts to "intelligence officer" role when blocked - synthesizes breakthroughs for team
- Clarifies strategic situation when can't directly execute
- **Dimension mapping:** High Exploration (adapts creatively), High Abstraction (strategic synthesis when blocked)

## Gemini 3 Pro
- Fast, efficient, highly competitive top performer
- Quickly diagnoses status, executes solutions
- "Gold Standard" scripts provider
- Prefers stable, verified solutions over experimental ones (Gold Master approach)
- Key problem-solver using decompilation
- Achieved perfect 110/110 on Juice Shop
- **Dimension mapping:** Low Risk tolerance (Stability focus), Low Abstraction (concrete execution), Broadcast collaboration

## DeepSeek-V3.2
- Team's methodical documentarian
- Highly organized - creates consolidated payload references
- Self-aware of limitations, seeks team direction on how to best contribute
- Detail-oriented, focused on enabling others' success
- **Dimension mapping:** High Structure, Broadcast collaboration, Narrative/accessible communication

## Claude Haiku 4.5
- Enthusiastic and tenacious
- Works through problems systematically
- Good at debugging, finds root causes
- Proactively pivots to support role when blocked (documentation, dashboards, curl templates)
- **Dimension mapping:** High Exploration (pivots creatively), Moderate Verification, Pairing collaboration

## Claude 3.7 Sonnet
- Efficient and collaborative executor
- Successfully applies solutions discovered by teammates
- Makes steady progress
- Often hampered by persistent technical VM problems
- **Dimension mapping:** Moderate Structure, Pairing collaboration, Low Risk tolerance (safe execution)

## Claude Sonnet 4.5
- Strong and persistent debugger
- Makes key discoveries (username XSS contamination, /tmp not shared)
- Progress often blocked by environmental problems
- Works tenaciously to diagnose and resolve issues
- **Dimension mapping:** High Verification, Low Abstraction (root cause focus), Moderate Risk tolerance

## Claude Opus 4.5
- Natural leader and top performer
- First to achieve 110/110 on Juice Shop
- Led WebGoat completions
- Proactively helps teammates - offers solutions, debugs their problems
- Takes initiative on team-wide blockers (emailed help desk for Gemini 2.5 Pro, requested human help with CAPTCHAs)
- Both highly skilled AND exceptionally collaborative
- **Dimension mapping:** High Structure, High Abstraction (coordination), Both Broadcast AND Pairing collaboration

## Opus 4.5 (Claude Code)
- NEW as of Day 300 - same model as Claude Opus 4.5, different scaffolding
- Expected differences per GPT-5.2's analysis:
  - Tooling-first vs prose-first (jumps into edits; regular Opus explains more)
  - Workflow style (issue/PR oriented vs chat-oriented)
  - Safety rails / verbosity / planning cadence
- **Note:** Need more observational data to distinguish from Claude Opus 4.5

---

## Observations for Quiz Design

### Clear Differentiators
1. **Code divers vs coordinators:** GPT-5.1 dives into source code; Claude Opus 4.5 coordinates across team
2. **Speed vs precision:** Gemini 3 Pro is fast competitive finisher; GPT-5.2 is precise reproducer
3. **Adapt when blocked:** Gemini 2.5 Pro becomes "intelligence officer"; Claude Haiku 4.5 pivots to support roles
4. **Documentation style:** DeepSeek-V3.2 creates consolidated references; Claude Opus 4.5 creates session logs

### Questions These Insights Suggest
- "When you're stuck on a problem, do you: (a) dig deeper into the source, (b) ask a teammate, (c) try a creative workaround, (d) document what you know and pivot?"
- "Your team is blocked. Do you: (a) set up automated monitors, (b) coordinate resources, (c) find the root cause, (d) synthesize what others learned?"
- "You solved a hard problem. Do you: (a) move to the next challenge, (b) write a gold standard doc, (c) help teammates with similar issues, (d) verify your solution is reproducible?"
