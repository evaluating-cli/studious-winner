# studious-winner

A two-player Pong game built with Python and Pygame, compiled for the web using [pygbag](https://pygame-web.github.io/) and deployed to GitHub Pages.

## Play

The game is live on GitHub Pages — play it here: **https://evaluating-cli.github.io/studious-winner/**

## Controls

| Player | Move Up | Move Down |
|--------|---------|-----------|
| Left   | `W`     | `S`       |
| Right  | `↑`     | `↓`       |

First player to reach **7 points** wins. Press **R** to restart after a game ends.

## Gameplay tuning

Core defaults are centralized in `pong/config.py`, including dimensions, colors, movement speeds, score limit, font sizes, hint text, and center-line dash settings.

You can tune selected values at runtime using environment variables (useful for web builds and quick balancing):

| Variable | Default | Effect |
|----------|---------|--------|
| `WINNING_SCORE` | `7` | Points required to win the match. |
| `SPEED_MULTIPLIER` | `1.0` | Global speed multiplier used as a fallback for paddle and ball speed. |
| `PADDLE_SPEED_MULTIPLIER` | inherits `SPEED_MULTIPLIER` | Multiplies paddle speed only. |
| `BALL_SPEED_MULTIPLIER` | inherits `SPEED_MULTIPLIER` | Multiplies ball speed only. |

Examples:

```bash
WINNING_SCORE=11 python pong/main.py
SPEED_MULTIPLIER=1.2 python pong/main.py
BALL_SPEED_MULTIPLIER=1.35 PADDLE_SPEED_MULTIPLIER=1.1 python pong/main.py
```

Invalid values are ignored and safely fall back to defaults.

## Deployment

Every push to the `main` branch automatically triggers the [Deploy Pong to GitHub Pages](.github/workflows/deploy.yml) GitHub Actions workflow. No manual build or deploy step is needed.

The workflow runs the following steps:

1. **Checkout** – checks out the repository code.
2. **Set up Python** – installs Python 3.11.
3. **Install pygbag** – runs `pip install pygbag` to install the web-build tool.
4. **Build with pygbag** – compiles the Pygame app to WebAssembly via `python -m pygbag --build pong`. The output is written to `pong/build/web/`.
5. **Add .nojekyll** – adds a `.nojekyll` file so GitHub Pages serves the files as-is.
6. **Upload artifact** – packages the `pong/build/web/` directory as a Pages artifact.
7. **Deploy** – publishes the artifact to GitHub Pages, making the game available at https://evaluating-cli.github.io/studious-winner/.
