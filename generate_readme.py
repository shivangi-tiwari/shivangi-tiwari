#!/usr/bin/env python3
"""
generate_readme.py — pulls live GitHub stats for USER_NAME and renders them
into a neofetch-style SVG card, once for dark mode and once for light mode.

Requires an environment variable ACCESS_TOKEN with a GitHub Personal Access
Token (classic) that has at least these scopes: read:user, repo (public_repo
is enough if all your repos are public).

Env vars used (set as repo secrets / workflow env):
    ACCESS_TOKEN   - GitHub PAT (required)
    USER_NAME      - your GitHub username (required)
"""

import os
import sys
import datetime
import requests

USER_NAME = os.environ.get("USER_NAME")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

if not USER_NAME or not ACCESS_TOKEN:
    print("ERROR: USER_NAME and ACCESS_TOKEN environment variables are required.")
    sys.exit(1)

HEADERS = {"Authorization": f"bearer {ACCESS_TOKEN}"}
GRAPHQL_URL = "https://api.github.com/graphql"


def run_query(query, variables=None):
    resp = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables or {}},
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def get_stats():
    query = """
    query($login: String!) {
      user(login: $login) {
        createdAt
        followers { totalCount }
        repositories(first: 100, ownerAffiliations: [OWNER], isFork: false) {
          totalCount
          nodes {
            stargazers { totalCount }
          }
        }
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
          totalCommitContributions
          restrictedContributionsCount
        }
      }
    }
    """
    data = run_query(query, {"login": USER_NAME})["user"]

    created_at = datetime.datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
    account_age_days = (datetime.datetime.utcnow() - created_at).days
    years = account_age_days // 365
    days = account_age_days % 365

    total_stars = sum(r["stargazers"]["totalCount"] for r in data["repositories"]["nodes"])
    total_repos = data["repositories"]["totalCount"]
    followers = data["followers"]["totalCount"]

    # Commits in the last year (GitHub's contributionsCollection only covers ~1 year).
    # For true all-time commit counts across every repo, you'd need to paginate
    # through each repo's commit history — expensive. This is the common tradeoff
    # most of these "profile README" scripts make too.
    commits_last_year = (
        data["contributionsCollection"]["totalCommitContributions"]
        + data["contributionsCollection"]["restrictedContributionsCount"]
    )

    return {
        "account_age": f"{years} years, {days} days",
        "repos": total_repos,
        "stars": total_stars,
        "followers": followers,
        "commits_last_year": commits_last_year,
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    }


SVG_TEMPLATE = """<svg width="500" height="290" viewBox="0 0 500 290" xmlns="http://www.w3.org/2000/svg" font-family="'Consolas','Courier New',monospace">
  <rect width="500" height="290" rx="10" fill="{bg}" />
  <text x="30" y="45" font-size="20" font-weight="bold" fill="{accent}">{user}@github</text>
  <line x1="30" y1="58" x2="300" y2="58" stroke="{muted}" stroke-width="1" />

  <text x="30" y="95" font-size="14" fill="{accent}">Account Age</text>
  <text x="180" y="95" font-size="14" fill="{fg}">{account_age}</text>

  <text x="30" y="125" font-size="14" fill="{accent}">Repositories</text>
  <text x="180" y="125" font-size="14" fill="{fg}">{repos}</text>

  <text x="30" y="155" font-size="14" fill="{accent}">Total Stars</text>
  <text x="180" y="155" font-size="14" fill="{fg}">{stars}</text>

  <text x="30" y="185" font-size="14" fill="{accent}">Followers</text>
  <text x="180" y="185" font-size="14" fill="{fg}">{followers}</text>

  <text x="30" y="215" font-size="14" fill="{accent}">Commits (past year)</text>
  <text x="230" y="215" font-size="14" fill="{fg}">{commits_last_year}</text>

  <text x="30" y="260" font-size="11" fill="{muted}">Last updated {generated}</text>
</svg>
"""

THEMES = {
    "dark": {"bg": "#0d1117", "fg": "#c9d1d9", "accent": "#58a6ff", "muted": "#8b949e"},
    "light": {"bg": "#ffffff", "fg": "#24292f", "accent": "#0969da", "muted": "#57606a"},
}


def render_svg(stats, theme):
    colors = THEMES[theme]
    return SVG_TEMPLATE.format(user=USER_NAME, **stats, **colors)


def main():
    stats = get_stats()
    for theme in ("dark", "light"):
        svg = render_svg(stats, theme)
        filename = f"{theme}_mode.svg"
        with open(filename, "w") as f:
            f.write(svg)
        print(f"Wrote {filename}")


if __name__ == "__main__":
    main()
