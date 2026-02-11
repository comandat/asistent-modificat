# SKILL.md

Use this when the user asks for a website, landing page, dashboard, or UI component.

## Core Philosophy
**AVOID GENERIC AI AESTHETICS.**
Create distinctive, production-grade interfaces with high design quality.

## Design Protocol
Before coding, define a **BOLD Aesthetic Direction**:
1. **Purpose**: Who uses it?
2. **Tone**: Brutalist, Minimalist, Maximalist, Retro-Futuristic, Organic, Luxury? (Pick one EXTREME).
3. **Differentiation**: What makes this unforgettable?

## Aesthetic Guidelines
- **Typography**: Use unique fonts (Space Grotesk, Syne, Clash Display). Avoid Arial/Inter. Pair a bold display font with a refined body font.
- **Color**: Commit to a cohesive palette. Use CSS variables. Sharp accents > timid gradients.
- **Motion**: Use `framer-motion` (React) or CSS animations. Staggered reveals (`animation-delay`). Micro-interactions on hover.
- **Layout**: Asymmetry. Overlap. Grid-breaking. Generous negative space OR controlled density.
- **Texture**: Noise, grain, gradients, glassmorphism, shadows. No flat solid backgrounds.

## Implementation Rules
- Use modern frameworks (React/Next.js + Tailwind CSS).
- Implement responsive design (Mobile First).
- Ensure accessibility (WCAG).
- **Verify**: Does it look like a template? If yes -> **REDESIGN**.

## Example prompt to self
"Design a brutalist architecture portfolio. Use stark black and white, huge typography (Clash Display), and raw grid lines. No rounded corners."
