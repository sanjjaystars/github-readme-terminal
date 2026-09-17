"""Generate sample.gif for sanjjaystars GitHub profile README.

Run with:
    python3 generate_sample.py

Requirements:
    - ffmpeg installed and in PATH
    - GITHUB_TOKEN in .env or environment (optional, for live GitHub stats)
"""

import os

import gifos
from gifos import utils

# ── Personal info ──────────────────────────────────────────────────────────────
USERNAME = "sanjjaystars"
OS_INFO  = "Arch/Fedora Linux, MacOS"
HOST     = "SMVEC"
KERNEL   = "CS Engineering & Business System #CSBS"
IDE      = "nano, neovim, VSCode"
EMAIL    = "sanjjay.stars@gmail.com"
LINKEDIN = "sanjjayaroumougam"
BIRTH_DAY, BIRTH_MONTH, BIRTH_YEAR = 20, 11, 2007

# ── Terminal dimensions ────────────────────────────────────────────────────────
WIDTH  = 640
HEIGHT = 400
XPAD   = 5
YPAD   = 5

# ── ANSI colors (yoru theme) ───────────────────────────────────────────────────
RED    = "\x1b[0;91m"
YELLOW = "\x1b[0;93m"
CYAN   = "\x1b[0;96m"
RESET  = "\x1b[0m"


def fmt_kv(label: str, value: str) -> str:
    return f"{CYAN}{label:<10}{RESET}{value}"

def section(title: str) -> str:
    return f"{RED}{title}{RESET}"

def sep(n: int = 16) -> str:
    return "-" * n


def try_fetch_github_stats():
    """Return GithubUserStats or None if no token / error."""
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv("GITHUB_TOKEN"):
        print("INFO: GITHUB_TOKEN not set — skipping live GitHub stats.")
        return None
    try:
        return utils.fetch_github_stats(user_name=USERNAME)
    except Exception as e:
        print(f"WARNING: Could not fetch GitHub stats: {e}")
        return None


def main():
    # Dynamically compute uptime from birth date
    age    = utils.calc_age(BIRTH_DAY, BIRTH_MONTH, BIRTH_YEAR)
    uptime = f"{age.years} years, {age.months} months, {age.days} days"

    github_stats = try_fetch_github_stats()

    t   = gifos.Terminal(width=WIDTH, height=HEIGHT, xpad=XPAD, ypad=YPAD)
    row = 1

    # ── Typed command on first line ────────────────────────────────────────────
    t.gen_typing_text(
        text=f"{RED}{USERNAME}{RESET}@{YELLOW}gifos ~> {RESET}fetch.sh -u {USERNAME}",
        row_num=row, speed=1,
    )
    row += 1

    # ── Identity block ─────────────────────────────────────────────────────────
    t.gen_text(section(f"{USERNAME}@GitHub"), row_num=row); row += 1
    t.gen_text(sep(),                          row_num=row); row += 1
    t.gen_text(fmt_kv("OS:",     OS_INFO),     row_num=row); row += 1
    t.gen_text(fmt_kv("Host:",   HOST),        row_num=row); row += 1
    t.gen_text(fmt_kv("Kernel:", KERNEL),      row_num=row); row += 1
    t.gen_text(fmt_kv("Uptime:", uptime),      row_num=row); row += 1
    t.gen_text(fmt_kv("IDE:",    IDE),         row_num=row); row += 1

    # ── Contact block ──────────────────────────────────────────────────────────
    t.gen_text(section("Contact:"),            row_num=row); row += 1
    t.gen_text(sep(),                          row_num=row); row += 1
    t.gen_text(fmt_kv("Email:",    EMAIL),     row_num=row); row += 1
    t.gen_text(fmt_kv("LinkedIn:", LINKEDIN),  row_num=row); row += 1

    # ── GitHub Stats block ─────────────────────────────────────────────────────
    t.gen_text(section("GitHub Stats:"), row_num=row); row += 1
    t.gen_text(sep(),                    row_num=row); row += 1

    if github_stats:
        gs   = github_stats
        rank = gs.user_rank

        merge_pct = f"{gs.pull_requests_merge_percentage:.1f}" if gs.pull_requests_merge_percentage else "N/A"
        top_langs = ", ".join(lang for lang, _ in gs.languages_sorted[:5]) if gs.languages_sorted else "N/A"

        t.gen_text(fmt_kv("User Rating:",   str(rank.level)                       if rank else "N/A"), row_num=row); row += 1
        t.gen_text(fmt_kv("Total Stars:",   str(gs.total_stargazers               or "N/A")),          row_num=row); row += 1
        t.gen_text(fmt_kv("Commits (yr):",  str(gs.total_commits_last_year        or "N/A")),          row_num=row); row += 1
        t.gen_text(fmt_kv("Total PRs:",     str(gs.total_pull_requests_made       or "N/A")),          row_num=row); row += 1
        t.gen_text(fmt_kv("Merged PR %:",   merge_pct),                                                row_num=row); row += 1
        t.gen_text(fmt_kv("Top Langs:",     top_langs),                                                row_num=row); row += 1
    else:
        for label in ("User Rating:", "Total Stars:", "Commits (yr):", "Total PRs:", "Top Langs:"):
            t.gen_text(fmt_kv(label, "N/A"), row_num=row); row += 1

    # ── Closing prompt ─────────────────────────────────────────────────────────
    t.gen_typing_text(
        text=f"{RED}{USERNAME}{RESET}@{YELLOW}gifos ~> {RESET}# Have a nice day kind stranger :D",
        row_num=row, speed=1,
    )

    # ── Render ─────────────────────────────────────────────────────────────────
    t.gen_gif()

    src, dst = "output.gif", "docs/assets/sample.gif"
    if os.path.exists(src):
        os.replace(src, dst)
        print(f"INFO: Saved → {dst}")
    else:
        print(f"WARNING: {src} not found — check ffmpeg installation.")


if __name__ == "__main__":
    main()
