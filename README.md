# studious-winner

A two-player Pong game built with Python and Pygame, compiled for the web using [pygbag](https://pygame-web.github.io/) and deployed to GitHub Pages.

## Play

**https://evaluating-cli.github.io/studious-winner/**

## Deployment

Every push to the `main` branch uses an **auto-deploy** GitHub Actions workflow: [Deploy Pong to GitHub Pages](.github/workflows/deploy.yml). There is **no manual build** or deploy step needed.

The workflow runs the following steps:

1. **Checkout** – checks out the repository code.
2. **Set up Python** – installs Python 3.11.
3. **Install pygbag** – runs `pip install pygbag` to install the web-build tool.
4. **Build with pygbag** – compiles the Pygame app to WebAssembly via `python -m pygbag --build --ume_block 0 pong`. The game uses a responsive canvas that fills the browser window. The output is written to `pong/build/web/`.
5. **Add .nojekyll** – adds a `.nojekyll` file so GitHub Pages serves the files as-is.
6. **Upload artifact** – packages the `pong/build/web/` directory as a Pages artifact.
7. **Deploy** – publishes the artifact to GitHub Pages, making the game available at https://evaluating-cli.github.io/studious-winner/.
