# 🚀 Cosmic Clash

A 2D spaceship duel built with **Python + Pygame**. Pilot the yellow ship against a red AI opponent that dodges, chases, and fights back — first ship to drain the other's **15 health** wins.

## Gameplay

- You control the **yellow ship**; the **red ship is AI-controlled**.
- The AI **dodges incoming bullets**, matches your altitude to line up shots, and switches between defensive and aggressive behavior when you're low on health.
- Each side can have up to **4 bullets** in flight at once.
- Fire sounds and hit effects are bundled in `assets/sound/`.

## Controls

| Key | Action |
|---|---|
| `W` `A` `S` `D` | Move your yellow ship |
| `Space` | Fire |
| `Esc` | Quit |
| `R` | Restart (after a match ends) |
| `Q` | Quit (after a match ends) |

## Getting started

```bash
git clone https://github.com/ZeroDayDoom/Cosmic-Clash.git
cd Cosmic-Clash
pip install pygame
python __init__.py
```

Requires Python 3 with [pygame](https://www.pygame.org/). All sprites, sounds, and fonts are bundled in `assets/` — run from the repository root so relative paths resolve.

## Project structure

```
Cosmic-Clash/
├── __init__.py        # full game code: rendering, AI, collision physics, main loop
├── setup.py           # packaging metadata
├── assets/
│   ├── images/        # red/yellow ships + space background
│   └── sound/         # firing and hit sounds
└── LICENSE            # MIT
```

## For developers

- The AI opponent lives in `red_ai()` — bullet-danger detection, target chasing, cooldown-based firing, and an aggressive/defensive stance switch.
- Difficulty is tweakable via the `LEVEL` and `DIFFICULTY` constants.
- Ideas to extend: smarter AI, power-ups, a local 2-player mode, or new ships/assets. PRs welcome!

## License

This project is licensed under the [MIT License](./LICENSE).
