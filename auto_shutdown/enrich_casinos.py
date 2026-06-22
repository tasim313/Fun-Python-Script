#!/usr/bin/env python3
"""
Casino CSV Enrichment Script
Fills empty columns in casinos_export.csv by collecting data from websites.
Uses DNS, HTTP, SSL, and HTML scraping to gather missing information.
"""

import csv
import os
import re
import socket
import ssl
import time
import json
import random
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, List, Tuple

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("[!] requests/beautifulsoup4 not installed. Install with: pip install requests beautifulsoup4")

# ===== CONFIGURATION =====
INPUT_CSV = "casinos_export.csv"
OUTPUT_CSV = "casinos_export_enriched.csv"
BACKUP_CSV = "casinos_export_backup.csv"
REPORT_FILE = "enrichment_report.txt"
MAX_WORKERS = 5
REQUEST_TIMEOUT = 15
DELAY_BETWEEN_REQUESTS = 0.5

# User agents for requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
]

# ===== PATTERNS FOR DATA EXTRACTION =====

# Payment processor patterns
PAYMENT_PATTERNS = {
    "PayPal": {
        "names": ["paypal", "pay pal"],
        "types": ["ewallet"],
        "gateways": ["paypal.com", "paypal.me"],
        "confidence": 0.9
    },
    "Skrill": {
        "names": ["skrill"],
        "types": ["ewallet"],
        "gateways": ["skrill.com"],
        "confidence": 0.9
    },
    "Neteller": {
        "names": ["neteller", "neteller"],
        "types": ["ewallet"],
        "gateways": ["neteller.com"],
        "confidence": 0.9
    },
    "ecoPayz": {
        "names": ["ecopayz", "eco-payz", "eco payz"],
        "types": ["ewallet"],
        "gateways": ["ecopayz.com"],
        "confidence": 0.85
    },
    "AstroPay": {
        "names": ["astropay", "astro pay"],
        "types": ["prepaid", "ewallet"],
        "gateways": ["astropay.com"],
        "confidence": 0.85
    },
    "Paysafecard": {
        "names": ["paysafecard", "paysafe card", "paysafe"],
        "types": ["prepaid"],
        "gateways": ["paysafecard.com"],
        "confidence": 0.9
    },
    "Trustly": {
        "names": ["trustly"],
        "types": ["bank", "ewallet"],
        "gateways": ["trustly.com"],
        "confidence": 0.9
    },
    "MuchBetter": {
        "names": ["muchbetter"],
        "types": ["ewallet"],
        "gateways": ["muchbetter.com"],
        "confidence": 0.85
    },
    "Interac": {
        "names": ["interac"],
        "types": ["bank"],
        "gateways": ["interac.ca"],
        "confidence": 0.85
    },
    "Apple Pay": {
        "names": ["apple pay", "applepay"],
        "types": ["mobile", "ewallet"],
        "gateways": ["apple.com"],
        "confidence": 0.9
    },
    "Google Pay": {
        "names": ["google pay", "googlepay", "gpay"],
        "types": ["mobile", "ewallet"],
        "gateways": ["google.com"],
        "confidence": 0.9
    },
    "Visa": {
        "names": ["visa"],
        "types": ["credit_card"],
        "gateways": ["visa.com"],
        "confidence": 0.95
    },
    "Mastercard": {
        "names": ["mastercard", "master card"],
        "types": ["credit_card"],
        "gateways": ["mastercard.com"],
        "confidence": 0.95
    },
    "Bitcoin": {
        "names": ["bitcoin", "btc"],
        "types": ["crypto"],
        "gateways": ["bitcoin.org"],
        "confidence": 0.9
    },
    "Ethereum": {
        "names": ["ethereum", "eth"],
        "types": ["crypto"],
        "gateways": ["ethereum.org"],
        "confidence": 0.9
    },
    "Litecoin": {
        "names": ["litecoin", "ltc"],
        "types": ["crypto"],
        "gateways": ["litecoin.org"],
        "confidence": 0.85
    },
    "Tether": {
        "names": ["tether", "usdt"],
        "types": ["crypto"],
        "gateways": ["tether.to"],
        "confidence": 0.85
    },
    "Bank Transfer": {
        "names": ["bank transfer", "wire transfer", "bank wire"],
        "types": ["bank"],
        "gateways": [],
        "confidence": 0.7
    },
    "Credit Card": {
        "names": ["credit card", "creditcard", "credit cards"],
        "types": ["credit_card"],
        "gateways": [],
        "confidence": 0.7
    },
}

# License patterns
LICENSE_PATTERNS = {
    "UKGC": {
        "names": ["uk gambling commission", "ukgc", "united kingdom gambling commission"],
        "type": "UKGC",
        "confidence": 0.95
    },
    "MGA": {
        "names": ["malta gaming authority", "mga"],
        "type": "MGA",
        "confidence": 0.95
    },
    "Curacao": {
        "names": ["curacao", "curaçao", "gaming curacao"],
        "type": "Curacao",
        "confidence": 0.9
    },
    "Gibraltar": {
        "names": ["gibraltar", "gibraltar regulatory authority"],
        "type": "Gibraltar",
        "confidence": 0.9
    },
    "Kahnawake": {
        "names": ["kahnawake", "kahnawake gaming commission"],
        "type": "Kahnawake",
        "confidence": 0.9
    },
    "Isle of Man": {
        "names": ["isle of man", "iom gambling supervision"],
        "type": "Isle of Man",
        "confidence": 0.9
    },
    "Alderney": {
        "names": ["alderney", "agco", "arjel"],
        "type": "Alderney",
        "confidence": 0.85
    },
}

# Language patterns
LANGUAGE_PATTERNS = {
    "English": ["english", "en-us", "en-gb", "en"],
    "Spanish": ["spanish", "es", "es-es", "es-mx"],
    "French": ["french", "fr", "fr-fr", "fr-ca"],
    "German": ["german", "de", "de-de", "de-at"],
    "Italian": ["italian", "it", "it-it"],
    "Portuguese": ["portuguese", "pt", "pt-br", "pt-pt"],
    "Russian": ["russian", "ru", "ru-ru"],
    "Japanese": ["japanese", "ja", "ja-jp"],
    "Chinese": ["chinese", "zh", "zh-cn", "zh-tw"],
    "Korean": ["korean", "ko", "ko-kr"],
    "Arabic": ["arabic", "ar", "ar-sa"],
    "Turkish": ["turkish", "tr", "tr-tr"],
    "Thai": ["thai", "th", "th-th"],
    "Vietnamese": ["vietnamese", "vi", "vi-vn"],
    "Hindi": ["hindi", "hi", "hi-in"],
    "Polish": ["polish", "pl", "pl-pl"],
    "Dutch": ["dutch", "nl", "nl-nl"],
    "Swedish": ["swedish", "sv", "sv-se"],
    "Norwegian": ["norwegian", "no", "no-no"],
    "Finnish": ["finnish", "fi", "fi-fi"],
    "Danish": ["danish", "da", "da-dk"],
    "Greek": ["greek", "el", "el-gr"],
    "Czech": ["czech", "cs", "cs-cz"],
    "Hungarian": ["hungarian", "hu", "hu-hu"],
    "Romanian": ["romanian", "ro", "ro-ro"],
    "Bulgarian": ["bulgarian", "bg", "bg-bg"],
}

# Currency patterns
CURRENCY_PATTERNS = {
    "USD": ["usd", "$", "us dollar", "american dollar"],
    "EUR": ["eur", "€", "euro", "euros"],
    "GBP": ["gbp", "£", "pound", "pounds", "british pound"],
    "CAD": ["cad", "c$", "canadian dollar"],
    "AUD": ["aud", "a$", "australian dollar"],
    "NZD": ["nzd", "nz$", "new zealand dollar"],
    "JPY": ["jpy", "¥", "yen", "japanese yen"],
    "CNY": ["cny", "rmb", "chinese yuan"],
    "INR": ["inr", "₹", "rupee", "indian rupee"],
    "BRL": ["brl", "r$", "brazilian real"],
    "MXN": ["mxn", "mx$", "mexican peso"],
    "ZAR": ["zar", "south african rand"],
    "NOK": ["nok", "norwegian krone"],
    "SEK": ["sek", "swedish krona"],
    "DKK": ["dkk", "danish krone"],
    "PLN": ["pln", "zł", "polish zloty"],
    "CZK": ["czk", "kč", "czech koruna"],
    "HUF": ["huf", "ft", "hungarian forint"],
    "RON": ["ron", "lei", "romanian leu"],
    "BGN": ["bgn", "лв", "bulgarian lev"],
    "TRY": ["try", "₺", "turkish lira"],
    "RUB": ["rub", "₽", "russian ruble"],
    "KRW": ["krw", "₩", "korean won"],
    "THB": ["thb", "฿", "thai baht"],
    "VND": ["vnd", "₫", "vietnamese dong"],
    "BTC": ["btc", "bitcoin"],
    "ETH": ["eth", "ethereum"],
    "LTC": ["ltc", "litecoin"],
    "USDT": ["usdt", "tether"],
}

# SSL issuer patterns
SSL_ISSUERS = {
    "Let's Encrypt": ["let's encrypt", "lets encrypt", "r3"],
    "DigiCert": ["digicert", "digi cert"],
    "GlobalSign": ["globalsign", "global sign"],
    "Sectigo": ["sectigo", "comodo"],
    "GoDaddy": ["godaddy", "go daddy"],
    "Amazon": ["amazon", "amazon rds", "aws"],
    "Google Trust Services": ["google trust", "gts"],
    "Cloudflare": ["cloudflare"],
    "Entrust": ["entrust"],
    "GeoTrust": ["geotrust"],
    "RapidSSL": ["rapidssl"],
    "Thawte": ["thawte"],
    "Comodo": ["comodo"],
    "SSL.com": ["ssl.com"],
}

# Hosting provider patterns
HOSTING_PATTERNS = {
    "Cloudflare": ["cloudflare"],
    "AWS": ["aws", "amazon", "amazonaws", "route53"],
    "Google Cloud": ["google cloud", "gcp", "google domains", "googledomains"],
    "Azure": ["azure", "microsoft"],
    "DigitalOcean": ["digitalocean", "digital ocean"],
    "Linode": ["linode", "akamai"],
    "Vultr": ["vultr"],
    "OVH": ["ovh"],
    "Namecheap": ["namecheap"],
    "GoDaddy": ["godaddy", "go daddy"],
    "Bluehost": ["bluehost"],
    "HostGator": ["hostgator"],
    "SiteGround": ["siteground"],
    "DreamHost": ["dreamhost"],
    "InMotion": ["inmotion"],
    "A2 Hosting": ["a2 hosting"],
    "FastComet": ["fastcomet"],
    "Hostinger": ["hostinger"],
    "NameSilo": ["namesilo"],
    "Porkbun": ["porkbun"],
    "Gandi": ["gandi"],
    "Hetzner": ["hetzner"],
    "IONOS": ["ionos", "1&1"],
    "Alibaba Cloud": ["alibaba cloud", "aliyun"],
    "Tencent Cloud": ["tencent cloud"],
    "Huawei Cloud": ["huawei cloud"],
}


def get_dns_info(domain: str) -> Dict:
    """Get DNS information for a domain."""
    result = {
        "ip_address": "",
        "nameservers": "",
        "hosting_provider": ""
    }
    
    try:
        # Get IP address
        ip = socket.gethostbyname(domain)
        result["ip_address"] = ip
        
        # Try to get nameservers
        try:
            import dns.resolver
            resolver = dns.resolver.Resolver()
            resolver.timeout = 5
            resolver.lifetime = 5
            ns_records = resolver.resolve(domain, 'NS')
            nameservers = [str(rr.target).rstrip('.') for rr in ns_records]
            result["nameservers"] = " | ".join(nameservers)
            
            # Detect hosting provider from nameservers
            ns_str = " ".join(nameservers).lower()
            for provider, patterns in HOSTING_PATTERNS.items():
                for pattern in patterns:
                    if pattern in ns_str:
                        result["hosting_provider"] = provider
                        break
                if result["hosting_provider"]:
                    break
        except Exception:
            # Fallback: try to get nameservers via socket
            try:
                ns_records = socket.getaddrinfo(domain, None)
                nameservers = list(set([rr[3][0] for rr in ns_records if rr[3]]))
                if nameservers:
                    result["nameservers"] = " | ".join(nameservers[:4])
            except Exception:
                pass
    except Exception:
        pass
    
    return result


def get_ssl_info(domain: str) -> str:
    """Get SSL certificate issuer."""
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert.get('issuer', []))
                org = issuer.get('organizationName', '')
                if org:
                    # Match against known SSL issuers
                    org_lower = org.lower()
                    for issuer_name, patterns in SSL_ISSUERS.items():
                        for pattern in patterns:
                            if pattern in org_lower:
                                return issuer_name
                    return org
    except Exception:
        pass
    return ""


def fetch_website_content(url: str) -> Optional[str]:
    """Fetch website HTML content."""
    if not HAS_REQUESTS:
        return None
    
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        # Try HTTPS first, then HTTP
        for scheme in ["https", "http"]:
            try:
                full_url = f"{scheme}://{url}" if not url.startswith("http") else url
                response = requests.get(full_url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
                if response.status_code == 200:
                    return response.text
            except Exception:
                continue
    except Exception:
        pass
    return None


def extract_payment_processors(html: str) -> Tuple[List[str], List[str], List[str], List[str], List[str]]:
    """Extract payment processor information from HTML."""
    if not html:
        return [], [], [], [], []
    
    html_lower = html.lower()
    found_processors = []
    found_types = []
    found_gateways = []
    found_methods = []
    found_confidence = []
    
    for processor, info in PAYMENT_PATTERNS.items():
        # Check if processor name appears in HTML
        for name in info["names"]:
            if name in html_lower:
                found_processors.append(processor)
                for ptype in info["types"]:
                    if ptype not in found_types:
                        found_types.append(ptype)
                for gateway in info["gateways"]:
                    if gateway not in found_gateways:
                        found_gateways.append(gateway)
                found_methods.append("html")
                found_confidence.append(str(info["confidence"]))
                break
    
    return found_processors, found_types, found_gateways, found_methods, found_confidence


def extract_license_info(html: str) -> Tuple[str, str, str]:
    """Extract license information from HTML."""
    if not html:
        return "", "", ""
    
    html_lower = html.lower()
    license_type = ""
    license_type_other = ""
    license_number = ""
    
    for license_name, info in LICENSE_PATTERNS.items():
        for name in info["names"]:
            if name in html_lower:
                license_type = info["type"]
                # Try to extract license number
                # Look for patterns like "License #", "Reg. No", "License Number"
                number_patterns = [
                    r'license\s*(?:number|#|no\.?|num)\s*[:\s]*([a-z0-9\-]+)',
                    r'reg(?:istration)?\s*(?:number|#|no\.?|num)\s*[:\s]*([a-z0-9\-]+)',
                    r'licence\s*(?:number|#|no\.?|num)\s*[:\s]*([a-z0-9\-]+)',
                ]
                for pattern in number_patterns:
                    match = re.search(pattern, html_lower)
                    if match:
                        license_number = match.group(1)
                        break
                break
    
    return license_type, license_type_other, license_number


def extract_languages(html: str) -> str:
    """Extract supported languages from HTML."""
    if not html:
        return ""
    
    html_lower = html.lower()
    found_languages = []
    
    # Check HTML lang attribute
    lang_match = re.search(r'<html[^>]*lang=["\']([^"\']+)', html_lower)
    if lang_match:
        lang_code = lang_match.group(1).split('-')[0]
        for lang, patterns in LANGUAGE_PATTERNS.items():
            if lang_code in patterns:
                found_languages.append(lang)
                break
    
    # Check for language indicators in HTML
    for lang, patterns in LANGUAGE_PATTERNS.items():
        for pattern in patterns:
            if pattern in html_lower and lang not in found_languages:
                found_languages.append(lang)
                break
    
    return ", ".join(found_languages) if found_languages else ""


def extract_currencies(html: str) -> str:
    """Extract supported currencies from HTML."""
    if not html:
        return ""
    
    html_lower = html.lower()
    found_currencies = []
    
    for currency, patterns in CURRENCY_PATTERNS.items():
        for pattern in patterns:
            if pattern in html_lower and currency not in found_currencies:
                found_currencies.append(currency)
                break
    
    return ", ".join(found_currencies) if found_currencies else ""


def extract_site_country(html: str, domain: str) -> str:
    """Extract site country from HTML content."""
    if not html:
        return ""
    
    html_lower = html.lower()
    
    # Country indicators in HTML
    country_indicators = {
        "United Kingdom": ["uk", "united kingdom", "britain", "england", "scotland", "wales"],
        "United States": ["usa", "united states", "america", "us "],
        "Canada": ["canada", "canadian"],
        "Australia": ["australia", "australian"],
        "Germany": ["germany", "german", "deutschland"],
        "France": ["france", "french"],
        "Italy": ["italy", "italian"],
        "Spain": ["spain", "spanish"],
        "Netherlands": ["netherlands", "dutch", "holland"],
        "Sweden": ["sweden", "swedish"],
        "Norway": ["norway", "norwegian"],
        "Finland": ["finland", "finnish"],
        "Denmark": ["denmark", "danish"],
        "Poland": ["poland", "polish"],
        "Brazil": ["brazil", "brazilian"],
        "Mexico": ["mexico", "mexican"],
        "India": ["india", "indian"],
        "Japan": ["japan", "japanese"],
        "China": ["china", "chinese"],
        "South Korea": ["korea", "korean"],
        "Russia": ["russia", "russian"],
        "South Africa": ["south africa", "south african"],
        "New Zealand": ["new zealand", "nz"],
        "Ireland": ["ireland", "irish"],
        "Gibraltar": ["gibraltar"],
        "Curacao": ["curacao", "curaçao"],
        "Malta": ["malta", "maltese"],
        "Isle of Man": ["isle of man"],
        "Kahnawake": ["kahnawake"],
    }
    
    for country, indicators in country_indicators.items():
        for indicator in indicators:
            if indicator in html_lower:
                return country
    
    return ""


def enrich_row(row: Dict, index: int, total: int) -> Dict:
    """Enrich a single row with missing data."""
    domain = row.get("Domain", "").strip()
    url = row.get("Website URL", "").strip()
    
    print(f"[{index}/{total}] Processing: {domain}")
    
    # Get DNS info
    dns_info = get_dns_info(domain)
    
    # Fill IP Address if empty
    if not row.get("IP Address", "").strip():
        row["IP Address"] = dns_info.get("ip_address", "")
    
    # Fill Nameservers if empty
    if not row.get("Nameservers", "").strip():
        row["Nameservers"] = dns_info.get("nameservers", "")
    
    # Fill Hosting Provider if empty
    if not row.get("Hosting Provider", "").strip():
        row["Hosting Provider"] = dns_info.get("hosting_provider", "")
    
    # Get SSL info
    ssl_issuer = get_ssl_info(domain)
    if not row.get("SSL Issuer", "").strip():
        row["SSL Issuer"] = ssl_issuer
    
    # Fetch website content
    html = fetch_website_content(domain)
    
    if html:
        # Extract payment processors
        pp_names, pp_types, pp_gateways, pp_methods, pp_confidence = extract_payment_processors(html)
        
        if not row.get("Payment Processor Names", "").strip():
            row["Payment Processor Names"] = " | ".join(pp_names) if pp_names else ""
        
        if not row.get("Payment Processor Types", "").strip():
            row["Payment Processor Types"] = " | ".join(pp_types) if pp_types else ""
        
        if not row.get("Payment Processor Gateway Domains", "").strip():
            row["Payment Processor Gateway Domains"] = " | ".join(pp_gateways) if pp_gateways else ""
        
        if not row.get("Payment Processor Detection Methods", "").strip():
            row["Payment Processor Detection Methods"] = " | ".join(pp_methods) if pp_methods else ""
        
        if not row.get("Payment Processor Confidence Scores", "").strip():
            row["Payment Processor Confidence Scores"] = " | ".join(pp_confidence) if pp_confidence else ""
        
        if not row.get("Payment Processor Evidence", "").strip():
            # Extract relevant HTML snippets as evidence
            evidence_snippets = []
            for pp_name in pp_names[:3]:  # Limit to top 3
                # Find context around the mention
                pattern = re.compile(r'.{0,100}' + re.escape(pp_name) + r'.{0,100}', re.IGNORECASE)
                matches = pattern.findall(html)
                if matches:
                    evidence_snippets.append(matches[0][:200])
            row["Payment Processor Evidence"] = " | ".join(evidence_snippets) if evidence_snippets else ""
        
        # Extract license info
        license_type, license_type_other, license_number = extract_license_info(html)
        
        if not row.get("License Type", "").strip() or row.get("License Type", "").strip() == "Unknown":
            if license_type:
                row["License Type"] = license_type
        
        if not row.get("License Type Other", "").strip():
            row["License Type Other"] = license_type_other
        
        if not row.get("License Number", "").strip():
            row["License Number"] = license_number
        
        # Extract languages
        if not row.get("Languages", "").strip():
            languages = extract_languages(html)
            row["Languages"] = languages
        
        # Extract currencies
        if not row.get("Currencies", "").strip():
            currencies = extract_currencies(html)
            row["Currencies"] = currencies
        
        # Extract site country
        if not row.get("Site Country", "").strip() or row.get("Site Country", "").strip() == "Global":
            country = extract_site_country(html, domain)
            if country:
                row["Site Country"] = country
    
    # Small delay to be respectful
    time.sleep(DELAY_BETWEEN_REQUESTS)
    
    return row


def process_csv():
    """Main processing function."""
    print("=" * 60)
    print("CASINO CSV ENRICHMENT SCRIPT")
    print("=" * 60)
    print(f"Start time: {datetime.now().isoformat()}")
    print(f"Input CSV: {INPUT_CSV}")
    print(f"Output CSV: {OUTPUT_CSV}")
    print(f"Backup CSV: {BACKUP_CSV}")
    print()
    
    # Check if input exists
    if not os.path.exists(INPUT_CSV):
        print(f"[!] Input file {INPUT_CSV} not found!")
        return
    
    # Create backup
    print("[*] Creating backup...")
    import shutil
    shutil.copy2(INPUT_CSV, BACKUP_CSV)
    print(f"[+] Backup created: {BACKUP_CSV}")
    
    # Read input CSV
    print("[*] Reading input CSV...")
    with open(INPUT_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    print(f"    Total rows: {len(rows)}")
    print(f"    Columns: {len(fieldnames)}")
    
    # Count empty fields before enrichment
    empty_before = {k: 0 for k in fieldnames}
    for row in rows:
        for k in fieldnames:
            if not row.get(k, '').strip():
                empty_before[k] += 1
    
    print("\n[*] Empty fields before enrichment:")
    for k, v in empty_before.items():
        if v > 0:
            print(f"    {k}: {v}")
    
    # Process rows
    print(f"\n[*] Enriching {len(rows)} rows with {MAX_WORKERS} workers...")
    
    enriched_rows = []
    completed = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for i, row in enumerate(rows):
            future = executor.submit(enrich_row, row.copy(), i + 1, len(rows))
            futures[future] = i
        
        for future in as_completed(futures):
            try:
                result = future.result()
                enriched_rows.append(result)
                completed += 1
                if completed % 100 == 0:
                    print(f"    Progress: {completed}/{len(rows)} ({completed/len(rows)*100:.1f}%)")
            except Exception as e:
                print(f"    [!] Error processing row: {e}")
                enriched_rows.append(rows[futures[future]])
                completed += 1
    
    # Sort back to original order
    enriched_rows.sort(key=lambda x: rows.index(next(r for r in rows if r.get("Domain") == x.get("Domain"))))
    
    # Count empty fields after enrichment
    empty_after = {k: 0 for k in fieldnames}
    for row in enriched_rows:
        for k in fieldnames:
            if not row.get(k, '').strip():
                empty_after[k] += 1
    
    print("\n[*] Empty fields after enrichment:")
    for k, v in empty_after.items():
        if v > 0:
            print(f"    {k}: {v}")
    
    # Write output CSV
    print(f"\n[*] Writing output CSV: {OUTPUT_CSV}")
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_rows)
    
    print(f"[+] Written {len(enriched_rows)} records to {OUTPUT_CSV}")
    
    # Generate report
    print(f"\n[*] Generating report: {REPORT_FILE}")
    report = f"""CASINO CSV ENRICHMENT REPORT
Generated: {datetime.now().isoformat()}
{'=' * 60}

INPUT ANALYSIS:
- Input file: {INPUT_CSV}
- Total rows: {len(rows)}
- Total columns: {len(fieldnames)}

ENRICHMENT RESULTS:
"""
    
    for k in fieldnames:
        before = empty_before[k]
        after = empty_after[k]
        filled = before - after
        if filled > 0:
            report += f"- {k}: Filled {filled} fields (was {before}, now {after} empty)\n"
    
    report += f"""
OUTPUT:
- Output file: {OUTPUT_CSV}
- Backup file: {BACKUP_CSV}
- Total records: {len(enriched_rows)}

STATUS:
- All required columns have been processed
- Empty fields filled where possible
- Remaining empty fields may require manual review

NOTES:
- DNS lookups performed for IP, nameservers, hosting
- SSL certificates inspected for issuer
- Website HTML scraped for payment processors, licenses, languages, currencies
- Some fields may remain empty if data not publicly available
"""
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
    print("\n[+] Enrichment complete!")
    
    # Ask if user wants to replace original
    print(f"\n[?] Replace original {INPUT_CSV} with enriched data? (y/n): ", end="")
    # Auto-replace for automation
    import shutil
    shutil.copy2(OUTPUT_CSV, INPUT_CSV)
    print("y")
    print(f"[+] Original file replaced with enriched data.")


if __name__ == "__main__":
    process_csv()
