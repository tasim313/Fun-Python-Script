#!/usr/bin/env python3
"""Quick test of enrichment functions on sample data."""

import sys
sys.path.insert(0, '.')

from enrich_casinos import (
    get_dns_info, get_ssl_info, extract_payment_processors,
    extract_license_info, extract_languages, extract_currencies,
    extract_site_country, fetch_website_content
)

# Test with a few known domains
test_domains = [
    "pokernews.com",
    "casinosonline.com", 
    "cloudbet.com",
    "stake.com",
    "gamblingcommission.gov.uk"
]

print("Testing enrichment functions...")
print("=" * 60)

for domain in test_domains:
    print(f"\nDomain: {domain}")
    print("-" * 40)
    
    # DNS info
    dns = get_dns_info(domain)
    print(f"  IP: {dns['ip_address']}")
    print(f"  Nameservers: {dns['nameservers']}")
    print(f"  Hosting: {dns['hosting_provider']}")
    
    # SSL info
    ssl_issuer = get_ssl_info(domain)
    print(f"  SSL Issuer: {ssl_issuer}")
    
    # Website content
    html = fetch_website_content(domain)
    if html:
        print(f"  HTML length: {len(html)}")
        
        # Payment processors
        pp_names, pp_types, pp_gateways, pp_methods, pp_confidence = extract_payment_processors(html)
        print(f"  Payment Processors: {pp_names}")
        print(f"  Payment Types: {pp_types}")
        
        # License info
        license_type, license_type_other, license_number = extract_license_info(html)
        print(f"  License Type: {license_type}")
        print(f"  License Number: {license_number}")
        
        # Languages
        languages = extract_languages(html)
        print(f"  Languages: {languages}")
        
        # Currencies
        currencies = extract_currencies(html)
        print(f"  Currencies: {currencies}")
        
        # Country
        country = extract_site_country(html, domain)
        print(f"  Country: {country}")
    else:
        print("  No HTML content fetched")

print("\n" + "=" * 60)
print("Test complete!")
