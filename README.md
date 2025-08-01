<p align="center">
  <img src="/img/screenshot.png" width="535">
  <h3 align="center">HackMD Box</h3>
  <p align="center">📝 Update a pinned gist to show your latest notes on HackMD.<p>
</p>

> This project is inspired by [medium-stat-box](https://github.com/kylemocode/medium-stat-box) and [youtube-box](https://github.com/SinaKhalili/youtube-box)

> For more pinned-gist projects like this one, check out: https://github.com/matchai/awesome-pinned-gists

## Overview
This project dymamically updates a pinned gist to show your latest HackMD notes publicly published. 

The gist includes a list of the notes' titles, with a separate Markdown file that provides clickable links to each article.

## Setup
### Prep Work
1. Create a new public GitHub Gist (https://gist.github.com/)
2. Create a token with the `gist` scope and copy it. (https://github.com/settings/tokens/new)
3. Create a HackMD API token following [this instruction](https://hackmd.io/@docs/HackMD_API_Book/https%3A%2F%2Fhackmd.io%2F%40hackmd-api%2Fdeveloper-portal).

### Project Setup
1. Fork this repo
2. Go to the fork's `Settings` > `Secrets and variables` > `Actions` and add new repository secret for each environment secret.
    - GH_TOKEN: The GitHub access token generated above.
    - HACKMD_API_KEY: The HackMD API token generated above.
    - GIST_ID: The ID portion of your gist url, ex: `https://gist.github.com/<github_username>/`**`6d5f84419863089a167387da62dd7081`**.
3. [Pin your gist](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/pinning-items-to-your-profile)
4. The github aciton cron job will run once a week (every Sunday). Push the repo can also trigger the action.