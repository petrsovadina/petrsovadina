# Umístit do repa petrsovadina/petrsovadina jako .github/workflows/snake.yml
name: Generate contribution snake

on:
  schedule:
    - cron: "0 3 * * *" # denně 03:00 UTC
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  snake:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Generate snake SVGs (brand magenta)
        uses: Platane/snk/svg-only@d8f6715049803e982ee5ff501b6b9b7d5deeb09b # v3.5.0
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-snake.svg?color_snake=#1a1b27&color_dots=#ebedf0,#f5c6e3,#eb94c8,#e06db5,#d84ba4
            dist/github-snake-dark.svg?palette=github-dark&color_snake=#ffffff&color_dots=#161b22,#4a1c3a,#7a2a5e,#a93a82,#d84ba4

      - name: Push SVGs to the output branch
        uses: crazy-max/ghaction-github-pages@1d6ee9b181a81033a16bd707a1401afa978daab4 # v5.0.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
