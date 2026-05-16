# Eventinkerer - Brand Identity

## Essence
Eventinkerer is a modern, vibrant platform for discovering and buying tickets to concerts, conferences, talks, and festivals. The brand conveys **energy, warmth, and trust**, evoking the anticipation people feel before a live event.

## Visual Principles
- **Soft curves**: large radii (1.25rem base, up to 2xl/3xl on cards and buttons) create a friendly, contemporary feel.
- **Subtle gradients**: violet to cyan serves as the visual signature across the logo, CTAs, and event covers.
- **Clear hierarchy**: bold typography for titles and muted styling for metadata.
- **Generous spacing**: comfortable breathing room between cards and sections.

## Palette (oklch)
| Token | Value | Usage |
|---|---|---|
| Primary | `oklch(0.58 0.22 295)` - Vibrant violet | CTAs, logo, primary accents |
| Accent | `oklch(0.78 0.17 200)` - Electric cyan | Highlights, notifications, gradients |
| Background | `oklch(0.985 0.005 280)` - White with a subtle lilac tint | Main background |
| Foreground | `oklch(0.18 0.04 280)` - Near-black with a violet cast | Primary text |
| Muted | `oklch(0.96 0.015 285)` | Secondary backgrounds |
| Secondary | `oklch(0.95 0.03 290)` | Chips, badges |

The signature gradient is built with `from-primary to-accent` (violet to cyan).

## Typography
Default operating-system sans-serif stack. Weights: 400 for body text, 600 for subtitles, and 700 for headings.

## Key Components
- **Navbar**: sticky header with translucent blur, gradient logo tile, gradient wordmark, and a brand-ringed avatar.
- **Filters**: sticky panel with rounded chips, checkboxes, and a price slider.
- **Event card**: cover with a unique gradient and emoji, floating category badge, icon-led metadata, and gradient CTA.

## Tone
Friendly, enthusiastic, and clear. Neutral English. CTAs use direct action verbs, such as "Buy tickets" and "Apply filters".

## Home Layout
- Top navbar with the logo on the left and the logged-in user on the right.
- Main body in a 1/3 + 2/3 grid: filters on the left and the event list on the right.
- Responsive behavior: on mobile, filters move above the event list.
