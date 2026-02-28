# studious-winner

A two-player Pong game built with Python and Pygame, compiled for the web using [pygbag](https://pygame-web.github.io/) and deployed to GitHub Pages.

## Play

The game has a **live demo** on GitHub Pages — play it here: **https://evaluating-cli.github.io/studious-winner/**

## Controls

| Player | Move Up | Move Down |
|--------|---------|-----------|
| Left   | `W`     | `S`       |
| Right  | `↑`     | `↓`       |

First player to reach **7 points** wins. Press **R** to restart after a game ends.

In **Options**, press **ENTER** to toggle aspect mode between Retro 4:3 and Widescreen, and press **F** to toggle fullscreen canvas mode.

## Deployment

Every push to the `main` branch uses an **auto-deploy** GitHub Actions workflow: [Deploy Pong to GitHub Pages](.github/workflows/deploy.yml). There is **no manual build** or deploy step needed.

The workflow runs the following steps:

1. **Checkout** – checks out the repository code.
2. **Set up Python** – installs Python 3.11.
3. **Install pygbag** – runs `pip install pygbag` to install the web-build tool.
4. **Build with pygbag** – compiles the Pygame app to WebAssembly via `python -m pygbag --build --ume_block 0 --width 640 --height 480 pong` so the deployed build matches the game's 640x480 canvas and avoids `ume_block` issues. The output is written to `pong/build/web/`.
5. **Add .nojekyll** – adds a `.nojekyll` file so GitHub Pages serves the files as-is.
6. **Upload artifact** – packages the `pong/build/web/` directory as a Pages artifact.
7. **Deploy** – publishes the artifact to GitHub Pages, making the game available at https://evaluating-cli.github.io/studious-winner/.


## Display Mode Regression Checklist

Manual QA path for web builds (pygbag output):

1. Launch the web build and start from normal mode (640x480).
2. Open **Options** and toggle aspect mode (Retro 4:3/Widescreen) repeatedly with `ENTER`.
3. Toggle fullscreen mode repeatedly with `F` (independent from aspect mode), then toggle aspect again while fullscreen is either on or off.
4. Confirm the canvas and visible viewport resize on every toggle path.
5. Start gameplay in each mode and verify:
   - paddles and ball stay within visible bounds,
   - scoring still triggers at left/right edges,
   - center line, scores, menu/options labels, and win banner remain centered.
