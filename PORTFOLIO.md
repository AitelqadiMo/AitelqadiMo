# Mohammed Ait El Qadi — Cinematic Portfolio

Personal portfolio, live at **https://aitelqadimo.github.io/AitelqadiMo/**

An award-style "3D scroll" single-page site: a cinematic 360° orbit of me is scrubbed
frame-by-frame as you scroll, with kinetic typography, scroll-pinned sections, and
scroll-driven video scenes.

## How it works

- **Hero orbit**: an 8s cinematic clip converted to a 120-frame WebP sprite-sheet
  sequence (`assets/sheet_*.webp`), painted to a full-viewport `<canvas>` and scrubbed
  by scroll position (GSAP ScrollTrigger + Lenis smooth scroll).
- **Scene sections**: pinned sections play muted background clips (`assets/builder.mp4`,
  `assets/closer.mp4`); the finale plays once and holds its last frame.
- **Type**: Anton display + Space Grotesk + JetBrains Mono, letter-by-letter name
  reveal tied to scrub progress, count-up stats, marquee, film-grain overlay.
- **Fallbacks**: `prefers-reduced-motion` gets a static, fully readable page.

## Stack

Vanilla HTML/CSS/JS · GSAP 3 ScrollTrigger · Lenis · Canvas 2D · WebP sprite sheets

Cinematic clips generated with Seedance 2.0 (identity-referenced), frames extracted
and packed by `tools/build_sprites.py` (ffmpeg + Pillow).

## Local development

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Structure

```
index.html              the whole site
assets/                 sprite sheets, poster, background clips
tools/build_sprites.py  video -> sprite-sheet pipeline
```

© 2026 Mohammed Ait El Qadi. Code is free to reference; all media and personal
content are all rights reserved.
