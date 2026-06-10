#!/usr/bin/env python3
"""
Bulk Domain Collector - 200K Unique Domains
Scrapes Bing search results for large-scale domain collection.
Runs continuously until target is reached or Ctrl+C is pressed.
Automatically resumes from existing CSV file (no data loss).

Usage:
    python3 search.py                         (auto-search 200 casino/gambling keywords, until 200K or Ctrl+C)
    python3 search.py "casino" "poker" -o mydomains.csv
    python3 search.py --once                  (run through keywords once, then stop)
    python3 search.py -p 5 -i 10 -t 50000     (5 pages per keyword, 10s interval, 50K target)
"""

import argparse
import csv
import os
import random
import signal
import sys
import time
import urllib.parse
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# ===== CONFIGURATION =====

# User-Agent rotation to avoid detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
]

# Domains to always filter out
IGNORED_DOMAINS = {
    "google.com", "bing.com", "microsoft.com", "yahoo.com", "wikipedia.org",
    "youtube.com", "blogger.com", "support.google", "facebook.com", "instagram.com",
    "twitter.com", "x.com", "linkedin.com", "reddit.com", "tiktok.com",
    "pinterest.com", "amazon.com", "ebay.com", "walmart.com", "apple.com",
}

# Comprehensive casino & gambling keyword database (240+ keywords, 9 categories)
DEFAULT_KEYWORDS = [
    # 1. High-Volume Broad Keywords (for homepage traffic)
    "casino", "online casino", "gambling", "online gambling", "casino site",
    "online casinos", "casino games", "slots", "live casino", "online slots",

    # 2. Game & Table Keywords (for game pages)
    "online slots", "online slots real money", "blackjack", "online blackjack",
    "roulette", "online roulette", "video poker", "online poker", "baccarat",
    "craps", "live casino games", "online blackjack real money",
    "online roulette real money", "video poker online", "live baccarat",
    "online slots real money", "progressive slots", "table games",
    "card games", "dice games online",

    # 3. Bonus & Registration Keywords (for conversion pages)
    "best online casino", "casino bonus", "free spins", "free spins no deposit",
    "no deposit bonus casino", "casino welcome bonus",
    "online casino welcome bonus", "free spins casino",
    "casino no deposit bonus", "best casino bonuses 2026",
    "claim free spins", "welcome bonus casino", "deposit bonus casino",
    "casino free spins", "no deposit casino", "best casino bonus",
    "online casino bonus", "free spins offer", "casino sign up bonus",
    "no deposit bonus online casino",

    # 4. Casino Brand & Review Keywords (for review/comparison pages)
    "best online casino", "top online casinos", "online casino reviews",
    "best casino sites", "casino sites", "online casino sites",
    "best gambling sites", "gambling sites", "trusted online casino",
    "legit online casino", "casino review", "online casino review",
    "best casino", "casino comparison", "gambling website",
    "online gambling sites", "best casino 2026", "new online casinos",
    "casino bonus comparison", "top casino sites", "online casino comparison",
    "best gambling websites", "casino recommendation",
    "online casino recommendation", "trusted casino sites",

    # 5. Location & Country-Specific Keywords (for targeted landing pages)
    "online casino USA", "best online casino USA", "casino USA",
    "online casino UK", "best online casino UK", "online casino Canada",
    "casino Australia", "online casino Australia", "online casino Germany",
    "casino Germany", "online casino France", "casino France",
    "online casino Sweden", "online casino Norway",
    "best casino in my country", "online casino near me",
    "legal online casino USA", "casino UK", "online casino Canada",
    "online casino Australia", "casino USA real money",
    "best online casino UK 2026", "online casino Germany",
    "casino France", "online casino Sweden",

    # 6. Mobile & Device Keywords (for responsive design pages)
    "mobile casino", "mobile slots", "play casino on mobile",
    "best mobile casino", "online casino mobile", "casino on phone",
    "slots on mobile", "play slots online mobile", "casino mobile games",
    "mobile live casino", "best mobile slots", "casino apps",
    "online casino app", "play casino mobile", "mobile blackjack",
    "slots mobile online", "casino mobile bonus", "mobile casino bonus",
    "play slots on phone", "best mobile casino sites",

    # 7. Bonus & Payment Keywords (for deposit/withdrawal pages)
    "casino free spins", "online casino no deposit bonus",
    "casino deposit bonus", "no deposit casino", "casino welcome bonus",
    "best casino bonus", "free spins casino", "casino no deposit",
    "online casino deposit bonus", "casino bonus code",
    "casino deposit methods", "instant deposit casino",
    "casino payout methods", "fast casino deposits",
    "casino withdrawal bonus", "no deposit free spins",
    "casino bonus code 2026", "online casino bonus code",
    "casino instant deposit", "best casino payment methods",
    "casino bonus 2026", "free casino spins", "casino deposit offer",
    "online casino bonus 2026", "casino welcome offer",

    # 8. Strategy & How-To Keywords (for blog/content pages)
    "how to play blackjack", "how to win at roulette",
    "best casino strategy", "casino winning strategy",
    "how to win online slots", "casino tips", "online casino tips",
    "blackjack strategy", "roulette strategy", "slots strategy",
    "how to play poker", "casino game guide", "online casino guide",
    "gambling strategy", "best casino games", "play blackjack online",
    "roulette strategy", "slots tips", "casino guide",
    "online casino strategy", "blackjack tips", "how to win at slots",
    "casino tutorial", "online gambling strategy", "best casino tips",

    # 9. Long-Tail & Low-Volume High-Intent Keywords (for targeted pages)
    "best online slots real money", "no deposit casino 2026",
    "online casino bonus no deposit", "casino free spins 2026",
    "play online slots real money", "best casino site",
    "online casino real money", "casino sites with no deposit",
    "online casino bonus 2026", "casino bonus code no deposit",
    "best online casino no deposit", "online slots free spins",
    "casino welcome bonus no deposit", "play casino real money",
    "online casino no deposit", "casino bonus without deposit",
    "best casino no deposit", "online casino 2026",
    "casino bonus 2026", "free casino spins no deposit",
    "online blackjack real money", "slots real money online",
    "casino live dealer", "online casino live casino",
    "best casino live dealer", "casino live games",
    "online casino live", "play live casino online",
    "best live casino online", "casino live dealer online",
]

TARGET_DOMAINS = 200000

# Global flag for Ctrl+C handling
running = True
iteration = 1
session_count = 0


def signal_handler(sig, frame):
    """Handles Ctrl+C gracefully."""
    global running
    print(f"\n\n[!] INTERRUPT RECEIVED. Finishing current cycle, then saving...")
    running = False


def get_headers():
    """Return headers with a random User-Agent to avoid detection."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.bing.com/",
    }


def extract_domain(url: str) -> str | None:
    """Extracts the clean domain name from a full URL."""
    try:
        if "google.com" in url:
            parsed_query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            url = parsed_query.get("q", [url])[0]

        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        domain = domain.lower().strip()
        if not domain or domain.replace(".", "").isdigit():
            return None
        return domain
    except Exception:
        return None


def search_bing_page(query: str, first: int = 1) -> set:
    """Scrape one page of Bing search results."""
    domains = set()
    params = {"q": query, "first": first, "count": 10}
    url = f"https://bing.com/search?{urllib.parse.urlencode(params)}"

    try:
        response = requests.get(url, headers=get_headers(), timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for div in soup.find_all("div", class_="b_attribution"):
                cite = div.find("cite")
                if cite:
                    url_text = cite.get_text(strip=True)
                    url_text = url_text.replace(" › ", "/")
                    if not url_text.startswith("http"):
                        url_text = "https://" + url_text
                    domain = extract_domain(url_text)
                    if domain:
                        domains.add(domain)

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("http") and not any(
                    x in href for x in ["bing.com", "microsoft.com"]
                ):
                    domain = extract_domain(href)
                    if domain:
                        domains.add(domain)
        return domains
    except requests.exceptions.Timeout:
        print("    [!] Bing search timed out")
    except requests.exceptions.ConnectionError:
        print("    [!] Bing connection error")
    except Exception as e:
        print(f"    [!] Bing search error: {e}")
    return domains


def search_bing_multi_page(query: str, num_pages: int = 1) -> set:
    """Scrape multiple pages of Bing results for a single query."""
    all_domains = set()
    for page in range(num_pages):
        first = (page * 10) + 1
        page_domains = search_bing_page(query, first)
        all_domains.update(page_domains)
        if page < num_pages - 1:
            time.sleep(random.uniform(2.0, 4.0))
    return all_domains


def collect_niche_domains(niche_keyword: str, num_pages: int = 1) -> list:
    """Collect domains for a keyword from Bing."""
    global session_count
    print(f"\n  Searching: '{niche_keyword}' (pages: {num_pages})...")
    bing_results = search_bing_multi_page(niche_keyword, num_pages)
    session_count += 1
    delay = random.uniform(1.5, 3.5)
    time.sleep(delay)
    final_domains = [d for d in bing_results if d not in IGNORED_DOMAINS]
    if final_domains:
        print(f"    -> Found {len(final_domains)} new candidate domains")
    return final_domains


def load_existing_domains(filename: str) -> set:
    """Load previously collected domains from CSV."""
    domains = set()
    if not filename or not os.path.exists(filename):
        return domains
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    domains.add(row[1].strip().lower())
    except Exception as e:
        print(f"  [!] Could not load existing domains: {e}")
    return domains


def save_results_csv(domains: set, filename: str) -> str:
    """Save all unique domains to CSV (overwrites with complete list)."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["#", "Domain", "Found At"])
        sorted_domains = sorted(domains)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for index, domain in enumerate(sorted_domains, 1):
            writer.writerow([index, domain, now])
    return filename


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Bulk domain collector - collects 200K+ unique domains. Runs continuously until target reached or Ctrl+C.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              (auto-search 200 keywords, runs until 200K)
  %(prog)s -o domains.csv -p 3 -i 10   (3 pages per keyword, 10s interval)
  %(prog)s "casino" "poker" -o results.csv
  %(prog)s --once                       (run through keywords once, then stop)
  python3 search.py -t 50000            (set custom target of 50,000)
        """,
    )

    parser.add_argument(
        "keywords", nargs="*",
        help="Keywords to search for. If omitted, 200 built-in defaults are used.",
    )
    parser.add_argument(
        "-k", "--keyword", action="append", dest="keywords_from_flag",
        help="Keyword to search for (can be used multiple times)",
    )
    parser.add_argument(
        "-p", "--pages", type=int, default=1,
        help="Result pages to scrape per keyword (1-5, default: 1)",
    )
    parser.add_argument(
        "-o", "--output", type=str, default="domains.csv",
        help="Output CSV file (default: domains.csv)",
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="Do not save to file (console only)",
    )
    parser.add_argument(
        "--delay", type=float, default=2.0,
        help="Base delay between requests in seconds (default: 2.0)",
    )
    parser.add_argument(
        "-i", "--interval", type=int, default=15,
        help="Seconds between collection rounds (default: 15)",
    )
    parser.add_argument(
        "-t", "--target", type=int, default=TARGET_DOMAINS,
        help=f"Target unique domains (default: {TARGET_DOMAINS:,})",
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Run once through keywords, then stop (default: continuous loop)",
    )
    parser.add_argument(
        "--fresh", action="store_true",
        help="Start fresh, ignore existing CSV file",
    )

    args = parser.parse_args()

    # Merge keywords
    final_keywords = list(args.keywords) if args.keywords else []
    if args.keywords_from_flag:
        final_keywords.extend(args.keywords_from_flag)
    args.keywords = final_keywords

    args.pages = max(1, min(args.pages, 5))
    return args


def main():
    global running, iteration

    args = parse_arguments()

    # Use default keywords if none provided
    if not args.keywords:
        args.keywords = DEFAULT_KEYWORDS

    signal.signal(signal.SIGINT, signal_handler)

    # Always load existing domains unless --fresh is specified
    all_found_websites: set = set()
    if not args.fresh and not args.no_save:
        existing = load_existing_domains(args.output)
        if existing:
            all_found_websites = existing
            print(f"[i] Loaded {len(existing):,} existing domains from {args.output}")
            print(f"    (use --fresh to start over)")

    keyword_index = 0

    print(f"\n{'='*60}")
    print(f"  BULK DOMAIN COLLECTOR")
    print(f"{'='*60}")
    print(f"  Keywords:          {len(args.keywords)}")
    print(f"  Pages per keyword: {args.pages}")
    print(f"  Interval:          {args.interval}s")
    print(f"  Target:            {args.target:,} unique domains")
    print(f"  Output:            {args.output}")
    print(f"  Starting count:    {len(all_found_websites):,} domains")
    if args.once:
        print(f"  Mode:              Single pass (--once)")
    else:
        print(f"  Mode:              Continuous loop (press Ctrl+C to stop)")
    print(f"{'='*60}")

    # --- MAIN LOOP (continuous by default, single-pass if --once) ---
    while running:
        print(f"\n--- Round {iteration} --- (total: {len(all_found_websites):,} / {args.target:,})")

        # Search 5 keywords per round (or all if --once)
        keywords_this_round = len(args.keywords) if args.once else min(5, len(args.keywords))

        for _ in range(keywords_this_round):
            if not running:
                break

            niche = args.keywords[keyword_index % len(args.keywords)]
            keyword_index += 1

            found = collect_niche_domains(niche, args.pages)
            new_count = 0
            for d in found:
                if d not in all_found_websites:
                    all_found_websites.add(d)
                    new_count += 1

            if new_count > 0:
                print(f"    >> +{new_count} NEW unique domains")

            # Check target
            if len(all_found_websites) >= args.target:
                print(f"\n{'='*60}")
                print(f"  ✅ TARGET REACHED! {len(all_found_websites):,} unique domains collected!")
                print(f"{'='*60}")
                running = False
                break

        # Save progress every round
        if not args.no_save and all_found_websites:
            save_results_csv(all_found_websites, args.output)
            print(f"\n  [{datetime.now().strftime('%H:%M:%S')}] Saved {len(all_found_websites):,} domains to {args.output}")

        # Exit if once mode
        if args.once:
            break

        # Wait between rounds (responsive to Ctrl+C)
        if running:
            print(f"\n  Waiting {args.interval}s (Ctrl+C to stop & save)...")
            for _ in range(args.interval):
                if not running:
                    break
                time.sleep(1)

        iteration += 1

    # --- FINAL SUMMARY ---
    sorted_domains = sorted(all_found_websites)
    total = len(sorted_domains)

    print(f"\n{'='*60}")
    print(f"  FINAL RESULTS")
    print(f"{'='*60}")
    print(f"  Total domains collected: {total:,}")
    print(f"  Rounds completed:        {iteration}")
    print(f"  Searches performed:      {session_count}")
    print(f"{'='*60}")

    # Print first 50 domains
    print(f"\n  First {min(50, total)} domains:")
    for i, domain in enumerate(sorted_domains[:50], 1):
        print(f"    {i}. {domain}")
    if total > 50:
        print(f"    ... and {total - 50} more")

    # Final save
    if not args.no_save:
        save_results_csv(all_found_websites, args.output)
        print(f"\n  All {total:,} domains saved to: {args.output}")

    if total >= args.target:
        print(f"\n✅ Target achieved! ({total:,} / {args.target:,})")
    else:
        print(f"\n📊 Collected {total:,} of {args.target:,} target")
        if not args.once and total < args.target:
            print(f"   Run again and it will auto-resume from {args.output}")

    print(f"\nDone!")