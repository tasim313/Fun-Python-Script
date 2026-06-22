#!/usr/bin/env python3
"""
Bulk Domain Collector - 20K Domains
Scrapes Bing search results for large-scale domain collection.
Runs continuously until target is reached or Ctrl+C is pressed.
Automatically resumes from existing CSV file (no data loss).

Key improvements:
- Concurrent requests with ThreadPoolExecutor (up to 3 parallel searches)
- No domain keyword filter (uses IGNORED_DOMAINS only to block unwanted)
- Faster delays, more keywords per round
- Auto-reshuffle when stuck

Usage:
    python3 search.py                         (auto-search, until 20K or Ctrl+C)
    python3 search.py --once                  (run through keywords once, then stop)
"""

import argparse
import csv
import os
import random
import re
import signal
import sys
import time
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

# ===== CONFIGURATION =====

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
]

# Domains to NEVER store (massive blacklist)
IGNORED_DOMAINS = {
    "google.com", "bing.com", "yahoo.com", "yandex.com", "duckduckgo.com",
    "baidu.com", "ask.com", "aol.com",
    "facebook.com", "instagram.com", "twitter.com", "x.com", "linkedin.com",
    "reddit.com", "tiktok.com", "pinterest.com", "snapchat.com", "tumblr.com",
    "whatsapp.com", "telegram.org", "discord.com", "twitch.tv",
    "microsoft.com", "support.google", "apple.com", "amazon.com", "ebay.com",
    "stackoverflow.com", "github.com", "github.io", "gitlab.com", "bitbucket.org",
    "sourceforge.net", "npmjs.com", "pypi.org", "docker.com",
    "wikipedia.org", "en.wikipedia.org", "wiktionary.org", "wikihow.com",
    "wikidata.org", "wikimedia.org", "britannica.com",
    "dictionary.cambridge.org", "merriam-webster.com", "dictionary.com",
    "collinsdictionary.com", "thesaurus.com", "wordreference.com",
    "youtube.com", "blogger.com", "wordpress.com", "medium.com",
    "cnn.com", "bbc.com", "bbc.co.uk", "nytimes.com", "theguardian.com",
    "reuters.com", "bloomberg.com", "forbes.com", "wsj.com", "washingtonpost.com",
    "npr.org", "foxnews.com", "abc.net.au", "nbcnews.com", "cbsnews.com",
    "usatoday.com", "latimes.com", "ndtv.com", "timesofindia.com",
    "who.int", "cdc.gov", "fda.gov", "usa.gov", "nih.gov",
    "verywellmind.com", "medicalnewstoday.com", "healthline.com",
    "webmd.com", "mayoclinic.org", "nhs.uk", "medscape.com",
    "weather.com", "accuweather.com", "wunderground.com", "yr.no",
    "zhihu.com", "zhuanlan.zhihu.com", "zhidao.baidu.com", "wenku.baidu.com",
    "baike.baidu.com", "sohu.com", "sina.com.cn", "qq.com", "weibo.com",
    "163.com", "douban.com", "taobao.com", "tmall.com", "jd.com",
    "xhamster.com", "pornhub.com", "xvideos.com", "xnxx.com",
    "redtube.com", "youporn.com",
    "adobe.com", "oracle.com", "ibm.com", "sap.com", "salesforce.com",
    "imdb.com", "spotify.com", "soundcloud.com",
    "zillow.com", "realtor.com", "indeed.com", "expedia.com",
    "booking.com", "tripadvisor.com", "yelp.com", "quora.com",
    "answers.com", "archive.org", "change.org", "gofundme.com",
    "khanacademy.org", "coursera.org", "udemy.com",
    "slideshare.net", "scribd.com", "issuu.com",
    "y8.com", "crazygames.com", "poki.com", "coolmathgames.com",
    "win-rar.com", "winzip.com", "7-zip.org",
    "vidio.com", "vimeo.com", "wetv.vip",
    "xtmobile.vn", "xoso.com.vn", "xosominhngoc.net.vn",
    "xosodaiphat.com", "xosothienphu.vn",
    "wiresawcutter.com", "wheresthematch.com",
    "wheelspinner.app", "what-is-gambling.com",
    "zh.wiktionary.org", "apps.apple.com",
    "account.microsoft.com", "support.apple.com",
    "2tmobile.com", "a-z-animals.com", "ai-bot.cn",
    "aitop100.cn", "aliyun.com", "amnh.org",
    "andar-global.com", "andar-sg.com", "andar.co.kr", "andar.com",
    "animals.net", "bbcearth.com", "best-inc.vn",
    "bestbuy.com", "bubble.com",
    "buildbackbetter.gov", "ca.gov",
    "cardgames.io", "ccw.gov.in",
    "cnn.com", "color-ize.com",
    "comicphonics.com", "compare.bet",
    "comparecards.com", "cricket.com",
    "dailymail.co.uk", "dailymotion.com",
    "dictionary.com", "dictionary.cambridge.org",
    "discover.com", "disney.com",
    "dummies.com", "duplichecker.com",
    "ebay.com", "edition.cnn.com",
    "eiu.com", "emojipedia.org",
    "en.wikipedia.org", "eonline.com",
    "espn.com", "etsy.com",
    "europa.eu", "ew.com",
    "finance.yahoo.com", "fiverr.com",
    "flipkart.com", "freegames.com",
    "freeonlinegames.com", "fujitsu.com",
    "funtrivia.com", "games.aarp.org",
    "games.paddypower.com", "gamespot.com",
    "gamesradar.com", "gamestop.com",
    "gaming.amazon.com", "gaming.lego.com",
    "gamingonphone.com", "gizmodo.com",
    "glassdoor.com", "globenewswire.com",
    "gmanetwork.com", "gogoanime.tv",
    "google.co.in", "google.co.uk",
    "google.com", "google.de",
    "google.fr", "grammarly.com",
    "groupon.com", "guardian.com",
    "happycolorz.com", "hasbro.com",
    "hgtv.com", "hindustantimes.com",
    "history.com", "hitc.com",
    "homedepot.com", "hootsuite.com",
    "hotels.com", "houzz.com",
    "howstuffworks.com", "huffpost.com",
    "hulu.com", "i.pinimg.com",
    "ibtimes.com", "iciciprumf.com",
    "ign.com", "igv.com",
    "ikea.com", "iloveds.com",
    "image.tmdb.org", "imgur.com",
    "independent.co.uk", "indiatimes.com",
    "indiegogo.com", "indonesia.travel",
    "info.microsoft.com", "infobae.com",
    "infoseek.co.jp", "inquirer.net",
    "insider.com", "instagram.com",
    "investopedia.com", "ipindia.gov.in",
    "irctc.co.in", "irishtimes.com",
    "islamicreliefcanada.org", "isro.gov.in",
    "itunes.apple.com", "iwanttodeliver.com",
    "jagran.com", "japantimes.co.jp",
    "jdsupra.com", "jio.com",
    "jobs.net", "jpost.com",
    "justdial.com", "kayak.com",
    "kickstarter.com", "klook.com",
    "kompas.com", "koreatimes.co.kr",
    "kreditkarma.com", "ksl.com",
    "kumparan.com", "laptopmag.com",
    "lasvegas.com", "latimes.com",
    "law.com", "law.cornell.edu",
    "lawinsider.com", "lawyers.com",
    "lazada.co.th", "lazada.com.ph",
    "lazada.co.id", "lazada.sg",
    "lazada.vn", "lbb.in",
    "lego.com", "library.spotify.com",
    "lifehacker.com", "lifewire.com",
    "likeable.com", "linkedin.com",
    "linio.com.mx", "liputan6.com",
    "livescience.com", "livestrong.com",
    "lloydsbank.com", "logical.com",
    "looktothestars.org", "lowes.com",
    "ludwig.guru", "lululemon.com",
    "lupa.gov.in", "luther.edu",
    "lyrics.com", "lyst.com",
}

# Casino domain filter - a domain must contain at least one of these
# This is a COMPREHENSIVE list of casino/gambling related keywords
CASINO_DOMAIN_REQUIRED = re.compile(
    r"(?:casino|gambl(?:ing)?|slot|poker|blackjack|roulette|baccarat|craps|"
    r"bet365|betfair|betway|bovada|draftkings|fanduel|"
    r"betting|bookmaker|bookie|sportsbook|sportsbet|"
    r"betsafe|betsson|betonline|betus|betamerica|"
    r"1xbet|sbobet|22bet|bemybet|asiabet|"
    r"bettingtop|bettingrank|bettingodds|bettingbonus|"
    r"bettingexchange|"
    r"vegas|lasvegas|jackpot|keno|lotto|lottery|wagering|"
    r"punt|wager|highroller|megaslot|"
    r"pokerstar|pokersite|pokeronline|pokergame|"
    r"fulltilt|partypoker|pokerstars|"
    r"247poker|247freepoker|"
    r"bingo|bingoblitz|bingoonline|bingogame|bingosites|"
    r"galabingo|meccabingo|"
    r"888casino|888poker|ladbrokes|williamhill|unibet|"
    r"bwin|paddypower|leovegas|mrgreen|comeon|"
    r"netent|microgaming|playtech|evolutiongaming|"
    r"askgamblers|casinomeister|thepogg|"
    r"slotomania|houseoffun|doubledown|"
    r"ignitioncasino|zyngapoker|"
    r"casinosite|casinoreview|casinotop|casinorating|"
    r"casinomentor|casinoencyclopedia|casinobeats|"
    r"gamblingsite|gamblingonline|"
    r"topcasino|top100bookmaker|"
    r"onlinecasino|livecasino|cryptocasino|bitcasino|"
    r"vegasslot|vegasworld|vegascasino|"
    r"freeslots|freepoker|freecasino|freespin|"
    r"247roulette|247blackjack|247slots|"
    r"slotmachine|slotgame|onlineslot|onlineslots|"
    r"wizardofodds|casinowizard)",
    re.IGNORECASE
)

# Default casino/gambling keywords
DEFAULT_KEYWORDS = [
    "online casino", "casino bonus", "free spins", "no deposit bonus",
    "casino welcome bonus", "best online casino", "top online casinos",
    "online casino reviews", "casino games", "online slots",
    "live casino", "blackjack", "roulette", "baccarat", "poker",
    "online poker", "video poker", "craps", "keno", "bingo",
    "lottery", "sports betting", "betting sites", "online sportsbook",
    "casino USA", "casino UK", "casino Canada", "casino Australia",
    "casino Germany", "casino France", "casino India",
    "mobile casino", "casino apps", "bitcoin casino",
    "crypto casino", "live dealer", "slot machines",
    "progressive slots", "jackpot", "vegas casino",
    "poker tournaments", "poker sites", "betting exchange",
    "football betting", "horse racing betting",
    "casino in goa", "casino in macau", "teen patti",
    "andar bahar", "dragon tiger", "pai gow",
    "3 card poker", "caribbean stud", "sic bo",
    "gambling", "casino", "slots", "blackjack online",
    "roulette online", "baccarat online", "poker online",
    "casino sign up bonus", "welcome bonus", "deposit bonus",
    "casino no deposit", "free casino games",
    "play slots", "play blackjack", "play roulette",
    "online gambling", "casino site", "gambling site",
    "best casino", "trusted casino", "legit casino",
    "new casino", "online casino 2026", "casino 2026",
    "casino review", "casino comparison",
    "live blackjack", "live roulette", "live baccarat",
    "fast payout casino", "instant withdrawal",
    "high roller casino", "vip casino", "low deposit casino",
    "minimum deposit casino", "casino tournament",
    "slot tournament", "poker tournament",
    "high stakes", "high limit", "roulette strategy",
    "blackjack strategy", "poker strategy", "betting strategy",
    "how to play casino", "casino guide", "casino tips",
    "betway", "bet365", "888casino", "pokerstars",
    "partypoker", "draftkings", "fanduel", "bovada",
    "ladbrokes", "william hill", "unibet", "bwin",
    "paddy power", "betfair", "sbobet", "1xbet",
    "22bet", "betonline", "betus",
]

TARGET_DOMAINS = 20000
MAX_WORKERS = 6  # Concurrent searches (increased for speed)

running = True
iteration = 1
session_count = 0

def signal_handler(sig, frame):
    global running
    print(f"\n\n[!] INTERRUPT RECEIVED. Finishing current cycle, then saving...")
    running = False

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.bing.com/",
    }

def extract_domain(url: str) -> str | None:
    try:
        if "google.com" in url:
            parsed_query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            url = parsed_query.get("q", [url])[0]
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        if not domain:
            domain = url.split("/")[0].split("›")[0].split(" ")[0].strip()
        if domain.startswith("www."):
            domain = domain[4:]
        domain = domain.split("›")[0].split("/")[0].strip().lower()
        if not domain or domain.replace(".", "").isdigit():
            return None
        # Skip IP addresses
        if domain.replace(".", "").isdigit():
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
            # Find from citation elements
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
            # Find from anchor links
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("http") and not any(x in href for x in ["bing.com", "microsoft.com"]):
                    domain = extract_domain(href)
                    if domain:
                        domains.add(domain)
        return domains
    except:
        return domains

def search_keyword(keyword: str, num_pages: int = 1) -> tuple:
    """Search a single keyword and return (keyword, found_domains)."""
    global session_count
    all_domains = set()
    for page in range(num_pages):
        first = (page * 10) + 1
        page_domains = search_bing_page(keyword, first)
        all_domains.update(page_domains)
        if page < num_pages - 1:
            time.sleep(random.uniform(0.1, 0.3))  # Faster delay
    session_count += 1
    # Filter: remove IGNORED_DOMAINS + optionally filter by casino pattern
    filtered = []
    for d in all_domains:
        if d in IGNORED_DOMAINS:
            continue
        if d.endswith((".gov", ".edu", ".mil")):
            continue
        # Casino filter is disabled (None) = collect everything
        if CASINO_DOMAIN_REQUIRED is None:
            filtered.append(d)
        elif CASINO_DOMAIN_REQUIRED.search(d):
            filtered.append(d)
    return (keyword, filtered)

def load_existing_domains(filename: str) -> dict:
    domain_map = {}
    if not filename or not os.path.exists(filename):
        return domain_map
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    domain = row[1].strip().lower()
                    found_at = row[2].strip() if len(row) >= 3 else ""
                    domain_map[domain] = found_at
    except:
        pass
    return domain_map

def save_results_csv(domains: set, filename: str, timestamps: dict = None) -> str:
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["#", "Domain", "Found At"])
        sorted_domains = sorted(domains)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for index, domain in enumerate(sorted_domains, 1):
            ts = now
            if timestamps and domain in timestamps and timestamps[domain]:
                ts = timestamps[domain]
            writer.writerow([index, domain, ts])
    return filename

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bulk domain collector")
    parser.add_argument("keywords", nargs="*", help="Keywords to search for")
    parser.add_argument("-p", "--pages", type=int, default=2, help="Pages per keyword (default: 2)")
    parser.add_argument("-o", "--output", type=str, default="domains.csv", help="Output CSV file")
    parser.add_argument("--no-save", action="store_true", help="Do not save to file")
    parser.add_argument("-i", "--interval", type=int, default=2, help="Seconds between rounds (default: 2)")
    parser.add_argument("-t", "--target", type=int, default=TARGET_DOMAINS, help=f"Target domains (default: {TARGET_DOMAINS:,})")
    parser.add_argument("--once", action="store_true", help="Single pass, then stop")
    parser.add_argument("--fresh", action="store_true", help="Start fresh, ignore existing CSV")
    parser.add_argument("--clean", action="store_true", help="Clean existing CSV: remove non-casino domains, then exit")
    args = parser.parse_args()
    args.pages = max(1, min(args.pages, 5))
    return args

def clean_existing_csv(filename: str):
    """Remove non-casino domains from existing CSV."""
    if not os.path.exists(filename):
        print(f"[!] File {filename} does not exist.")
        return
    
    domain_map = load_existing_domains(filename)
    if not domain_map:
        print(f"[!] No domains found in {filename}.")
        return
    
    original_count = len(domain_map)
    cleaned = {}
    removed = 0
    
    for domain, ts in domain_map.items():
        if domain in IGNORED_DOMAINS:
            removed += 1
            continue
        if domain.endswith((".gov", ".edu", ".mil")):
            removed += 1
            continue
        if CASINO_DOMAIN_REQUIRED is None or CASINO_DOMAIN_REQUIRED.search(domain):
            cleaned[domain] = ts
        else:
            removed += 1
    
    # Save cleaned results
    save_results_csv(set(cleaned.keys()), filename, cleaned)
    print(f"\n{'='*60}")
    print(f"  CLEANUP COMPLETE")
    print(f"{'='*60}")
    print(f"  Original domains:  {original_count:,}")
    print(f"  Removed:           {removed:,}")
    print(f"  Remaining:         {len(cleaned):,}")
    print(f"  Saved to:          {filename}")
    print(f"{'='*60}")

def main():
    global running, iteration

    args = parse_arguments()
    if not args.keywords:
        args.keywords = DEFAULT_KEYWORDS

    # Handle clean mode first
    if args.clean:
        clean_existing_csv(args.output)
        return

    signal.signal(signal.SIGINT, signal_handler)

    # Load existing
    all_found_websites: set = set()
    domain_timestamps: dict = {}
    if not args.fresh and not args.no_save:
        existing = load_existing_domains(args.output)
        if existing:
            all_found_websites = set(existing.keys())
            domain_timestamps = existing
            print(f"[i] Loaded {len(existing):,} existing domains from {args.output}")

    random.shuffle(args.keywords)
    keyword_index = 0

    print(f"\n{'='*60}")
    print(f"  BULK DOMAIN COLLECTOR (PARALLEL)")
    print(f"{'='*60}")
    print(f"  Keywords:          {len(args.keywords)}")
    print(f"  Pages per keyword: {args.pages}")
    print(f"  Interval:          {args.interval}s")
    print(f"  Target:            {args.target:,} unique domains")
    print(f"  Output:            {args.output}")
    print(f"  Starting count:    {len(all_found_websites):,} domains")
    print(f"  Parallel searches: {MAX_WORKERS} at a time")
    if args.once:
        print(f"  Mode:              Single pass")
    else:
        print(f"  Mode:              Continuous loop (Ctrl+C to stop)")
    print(f"{'='*60}")

    stuck_count = 0

    # --- MAIN LOOP ---
    while running:
        print(f"\n--- Round {iteration} --- (total: {len(all_found_websites):,} / {args.target:,})")

        # Get next batch of keywords
        batch_size = len(args.keywords) if args.once else min(20, len(args.keywords))
        batch_keywords = []
        for _ in range(batch_size):
            kw = args.keywords[keyword_index % len(args.keywords)]
            keyword_index += 1
            batch_keywords.append(kw)

        # Search in parallel
        new_in_round = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(search_keyword, kw, args.pages): kw for kw in batch_keywords}
            for future in as_completed(futures):
                if not running:
                    executor.shutdown(wait=False)
                    break
                kw, found = future.result()
                added = 0
                for d in found:
                    if d not in all_found_websites:
                        all_found_websites.add(d)
                        added += 1
                new_in_round += added
                if added > 0:
                    print(f"    [{kw[:35]:35s}] +{added:2d} new (total: {len(found):2d} found)")
                else:
                    print(f"    [{kw[:35]:35s}]   no new")

                # Check target
                if len(all_found_websites) >= args.target:
                    print(f"\n{'='*60}")
                    print(f"  ✅ TARGET REACHED! {len(all_found_websites):,} unique domains!")
                    print(f"{'='*60}")
                    running = False
                    break

        # Save
        if not args.no_save and all_found_websites:
            save_results_csv(all_found_websites, args.output, domain_timestamps)
            pct = (len(all_found_websites) / args.target) * 100
            print(f"\n  [{datetime.now().strftime('%H:%M:%S')}] Saved {len(all_found_websites):,}/{args.target:,} ({pct:.1f}%)")

        # Track stuck
        if new_in_round == 0:
            stuck_count += 1
        else:
            stuck_count = 0

        # Reshuffle if stuck
        if stuck_count >= 3:
            random.shuffle(args.keywords)
            print(f"  [!] Reshuffled keywords to find fresh results...")
            stuck_count = 0

        if args.once:
            break

        # Wait
        if running:
            print(f"  Waiting {args.interval}s...")
            for _ in range(args.interval):
                if not running:
                    break
                time.sleep(1)

        iteration += 1

    # --- SUMMARY ---
    sorted_domains = sorted(all_found_websites)
    total = len(sorted_domains)
    print(f"\n{'='*60}")
    print(f"  FINAL: {total:,} domains collected")
    print(f"{'='*60}")
    print(f"  Sample ({min(20, total)} of {total}):")
    for i, d in enumerate(sorted_domains[:20], 1):
        print(f"    {i}. {d}")

    if not args.no_save:
        save_results_csv(all_found_websites, args.output, domain_timestamps)
        print(f"\n  All {total:,} domains saved to: {args.output}")
    print(f"\nDone!")


if __name__ == "__main__":
    main()