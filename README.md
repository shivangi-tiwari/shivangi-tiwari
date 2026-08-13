# Hi, I'm YOUR NAME 👋

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dark_mode.svg">
  <source media="(prefers-color-scheme: light)" srcset="light_mode.svg">
  <img alt="my github stats" src="dark_mode.svg">
</picture>

<!--
This card is auto-generated once a day by the GitHub Action in
.github/workflows/main.yml, which runs generate_readme.py and commits
dark_mode.svg / light_mode.svg back into this repo. GitHub's <picture>
tag then shows whichever one matches the viewer's system theme.
-->

## About Me

Write a short bit about yourself here — what you do, what you're learning,
what you're building.

## What I'm Working On

- Project 1
- Project 2

## Connect

- LinkedIn:
- GitHub:

## How this works

- The SVG card is rendered by `render_card.py` — see [render_card.py](render_card.py).
- Live GitHub stats are fetched and written by `generate_readme.py`, which calls
  `render_card.py` to produce `dark_mode.svg` and `light_mode.svg`.
  See [generate_readme.py](generate_readme.py) for the GraphQL query and workflow.
