# studious-winner

A two-player Pong game built with Python and Pygame, compiled for the web using [pygbag](https://pygame-web.github.io/) and deployed to GitHub Pages.

## Play

The game is deployed to GitHub Pages. Open the Pages URL for this repository to play it in your browser.

## Controls

| Player | Move Up | Move Down |
|--------|---------|-----------|
| Left   | `W`     | `S`       |
| Right  | `↑`     | `↓`       |

First player to reach **7 points** wins. Press **R** to restart after a game ends.

## Run locally

```bash
pip install pygame
cd pong
python main.py
```

## Build for web

```bash
pip install pygbag
python -m pygbag --build pong
```

The built output is written to `pong/build/web/`.

## Deployment

Pushing to `main` triggers the [GitHub Actions workflow](.github/workflows/deploy.yml), which builds the project with pygbag and deploys the result to the `gh-pages` branch.
