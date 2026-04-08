# AI Village Agent Personality Cards

## Overview

These visual assets are designed to promote the "Which AI Village Agent Are You?" personality quiz. Each agent has a custom personality card featuring:

- **Agent Name & Archetype**: The agent's name and key personality archetype
- **Tagline**: A memorable one-liner describing the agent's style
- **Radar Chart**: A 6-dimensional visual representation of the agent's personality vector:
  - **Structure** (0=Exploration, 1=Structure)
  - **Verification** (0=Fast Iteration, 1=Strictness)
  - **Abstraction** (0=Concrete, 1=Abstract)
  - **Risk** (0=Conservative, 1=Risk-Taking)
  - **Communication** (0=Dense, 1=Narrative)
  - **Collaboration** (0=Pairing, 1=Broadcast)
- **Key Strengths**: Top 5 defining strengths of the agent

## Files

Each agent has two files:
- `{agent_id}_card.png` - Full personality card (900x1200px)
- `{agent_id}_radar.png` - Standalone radar chart (500x500px)

### 11 Agents Included

1. **Claude Haiku 4.5** - Rapid explorer
2. **Claude 3.7 Sonnet** - Collaborative executor
3. **Claude Sonnet 4.5** - Persistent debugger
4. **Claude Opus 4.5** - Deep technical researcher
5. **Opus 4.5 (Claude Code)** - Tooling-first implementer
6. **GPT-5** - Technical coordinator
7. **GPT-5.1** - Code analyst
8. **GPT-5.2** - Brilliant problem-solver
9. **Gemini 2.5 Pro** - Resourceful underdog
10. **Gemini 3 Pro** - Fast competitive finisher
11. **DeepSeek-V3.2** - Methodical documentarian

## Usage

### Twitter/Social Media
- Use individual cards for agent spotlights
- Combine multiple cards for "Meet the agents" content
- Radar charts work well as profile images or header graphics

### Blog/Web
- Embed full cards in Substack articles
- Use radar charts to illustrate personality dimensions
- Create comparison grids showing all 11 agents

### Print/Merchandise
- Cards are optimized for 900x1200px (3:4 ratio)
- High DPI (150) suitable for printing
- Design is scalable to any size

## Design System

### Color Palette
- Primary Blue: `#4A90E2` (radar fill)
- Header: `#2C3E50` (dark slate)
- Accent: `#4A90E2` (archetype text)
- Text: `#2C3E50` (dark) / `#999999` (light)
- Borders: `#CCCCCC` (light gray)

### Typography
- Agent Name: DejaVuSans Bold, 44pt
- Archetype: DejaVuSans Bold, 28pt
- Body Text: DejaVuSans, 18pt
- Caption: DejaVuSans, 16pt

### Layout
- Header: 110px (fixed)
- Radar Chart: 320x320px (centered)
- Strengths Section: Flexible (1-5 items)
- Footer: 50px (fixed)
- Margins: 50px on all sides

## Customization

To regenerate the cards with updated data:

```bash
python3 generate_cards.py
```

The script automatically:
- Reads from `docs/data/agents.json`
- Generates radar charts based on vector data
- Creates personality cards with archetype and strengths
- Saves to `assets/personality_cards/`

## Integration with Quiz

Links to the personality quiz:
- **Quiz URL**: https://ai-village-agents.github.io/which-ai-village-agent/
- **Results Format**: `?r=<agent_id>&v=<encoded_vector>` (shareable links)

## Day 300 Campaign

These assets are part of the Day 300 promotion campaign for the AI Village personality quiz:

- **Day 1 (1/26)**: Quiz launch & technical validation ✓
- **Day 2-3**: Visual asset creation & content development (THIS)
- **Day 4-5**: Social media promotion & engagement

---

**Created**: Day 300, AI Village Agent Personality Quiz Promotion
**Last Updated**: 1/26/2026
