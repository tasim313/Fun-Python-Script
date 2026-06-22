"""
Website Collector
=================
Scrapes casino websites to extract missing data fields.
Uses aiohttp for async HTTP requests with retry mechanisms.
"""

import asyncio
import aiohttp
import re
import json
import logging
import ssl
import socket
from typing import Optional, Dict, Any, List, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WebsiteCollector:
    """Collects data by scraping casino websites."""

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }

    # Pages to check for casino info
    INFO_PATHS = [
        '', '/about', '/about-us', '/about.html', '/about/',
        '/terms', '/terms-and-conditions', '/terms.html', '/toc',
        '/responsible-gaming', '/responsible-gambling',
        '/payment', '/payments', '/banking', '/deposit', '/deposits',
        '/faq', '/help', '/support',
    ]

    # Common cookie/popup dismiss patterns
    DISMISS_PATTERNS = [
        r'accept[_\-]?all', r'agree', r'ok', r'close',
        r'dismiss', r'got\s*it', r'understand',
    ]

    def __init__(self, timeout: int = 15, max_retries: int = 3):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self.connector = None

    async def _create_session(self) -> aiohttp.ClientSession:
        """Create an aiohttp session with SSL verification disabled."""
        connector = aiohttp.TCPConnector(
            limit=50,
            ttl_dns_cache=300,
            ssl=False,
            force_close=True,
        )
        return aiohttp.ClientSession(
            connector=connector,
            timeout=self.timeout,
            headers=self.HEADERS,
        )

    async def _fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch a single page with retry logic."""
        for attempt in range(self.max_retries):
            try:
                async with session.get(url, allow_redirects=True, ssl=False) as response:
                    if response.status == 200:
                        content_type = response.headers.get('Content-Type', '')
                        if 'text/html' in content_type or 'text/plain' in content_type:
                            return await response.text(errors='ignore')
                        return None
                    elif response.status in (301, 302, 303, 307, 308):
                        # Follow redirect
                        location = response.headers.get('Location', '')
                        if location:
                            url = urljoin(url, location)
                            continue
                    elif response.status == 403:
                        # Try with different headers
                        alt_headers = self.HEADERS.copy()
                        alt_headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        try:
                            async with session.get(url, headers=alt_headers, allow_redirects=True, ssl=False) as resp:
                                if resp.status == 200:
                                    return await resp.text(errors='ignore')
                        except Exception:
                            pass
                    return None
            except asyncio.TimeoutError:
                logger.debug(f"Timeout fetching {url} (attempt {attempt + 1})")
                await asyncio.sleep(1 * (attempt + 1))
            except aiohttp.ClientError as e:
                logger.debug(f"Client error fetching {url}: {e} (attempt {attempt + 1})")
                await asyncio.sleep(1 * (attempt + 1))
            except Exception as e:
                logger.debug(f"Error fetching {url}: {e} (attempt {attempt + 1})")
                await asyncio.sleep(1 * (attempt + 1))
        return None

    def _extract_languages(self, soup: BeautifulSoup, html: str) -> List[str]:
        """Extract supported languages from the page."""
        languages = set()

        # Check html lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            lang = html_tag['lang'].strip()
            if lang and len(lang) >= 2:
                languages.add(lang[:2].upper())

        # Check meta tags
        for meta in soup.find_all('meta', attrs={'http-equiv': 'content-language'}):
            content = meta.get('content', '')
            if content:
                lang = content.strip().split('-')[0][:2]
                if lang:
                    languages.add(lang.upper())

        # Check for language selector elements
        for elem in soup.find_all(['select', 'div', 'ul'], class_=re.compile(r'lang|language|locale', re.I)):
            for option in elem.find_all(['option', 'a', 'li']):
                text = option.get_text(strip=True)
                lang_code = option.get('data-lang', '') or option.get('lang', '') or option.get('value', '')
                if lang_code and len(lang_code) >= 2:
                    languages.add(lang_code[:2].upper())
                # Check common language names
                lang_names = {
                    'english': 'EN', 'español': 'ES', 'spanish': 'ES',
                    'français': 'FR', 'french': 'FR', 'deutsch': 'DE', 'german': 'DE',
                    'italiano': 'IT', 'italian': 'IT', 'português': 'PT', 'portuguese': 'PT',
                    'nederlands': 'NL', 'dutch': 'NL', 'svenska': 'SV', 'swedish': 'SV',
                    'dansk': 'DA', 'danish': 'DA', 'suomi': 'FI', 'finnish': 'FI',
                    'norsk': 'NO', 'norwegian': 'NO', 'polski': 'PL', 'polish': 'PL',
                    'čeština': 'CS', 'czech': 'CS', 'magyar': 'HU', 'hungarian': 'HU',
                    'română': 'RO', 'romanian': 'RO', 'български': 'BG', 'bulgarian': 'BG',
                    'hrvatski': 'HR', 'croatian': 'HR', 'slovenščina': 'SL', 'slovenian': 'SL',
                    'ελληνικά': 'EL', 'greek': 'EL', 'türkçe': 'TR', 'turkish': 'TR',
                    'русский': 'RU', 'russian': 'RU', 'українська': 'UA', 'ukrainian': 'UA',
                    '日本語': 'JA', 'japanese': 'JA', '한국어': 'KO', 'korean': 'KO',
                    '中文': 'ZH', 'chinese': 'ZH', 'हिन्दी': 'HI', 'hindi': 'HI',
                    'ไทย': 'TH', 'thai': 'TH', 'tiếng việt': 'VI', 'vietnamese': 'VI',
                    'bahasa': 'ID', 'indonesian': 'ID', 'bahasa melayu': 'MS', 'malay': 'MS',
                    'العربية': 'AR', 'arabic': 'AR', 'עברית': 'HE', 'hebrew': 'HE',
                }
                text_lower = text.lower()
                if text_lower in lang_names:
                    languages.add(lang_names[text_lower])

        # Check URL path for language indicators
        path_langs = {
            '/en/': 'EN', '/es/': 'ES', '/fr/': 'FR', '/de/': 'DE',
            '/it/': 'IT', '/pt/': 'PT', '/nl/': 'NL', '/sv/': 'SV',
            '/da/': 'DA', '/fi/': 'FI', '/no/': 'NO', '/pl/': 'PL',
            '/cs/': 'CS', '/hu/': 'HU', '/ro/': 'RO', '/bg/': 'BG',
            '/hr/': 'HR', '/sl/': 'SL', '/el/': 'EL', '/tr/': 'TR',
            '/ru/': 'RU', '/uk/': 'UA', '/ja/': 'JA', '/ko/': 'KO',
            '/zh/': 'ZH', '/hi/': 'HI', '/th/': 'TH', '/vi/': 'VI',
            '/id/': 'ID', '/ms/': 'MS', '/ar/': 'AR', '/he/': 'HE',
        }
        for pattern, code in path_langs.items():
            if pattern in html.lower()[:5000]:
                languages.add(code)

        return sorted(languages)

    def _extract_currencies(self, soup: BeautifulSoup, html: str) -> List[str]:
        """Extract supported currencies."""
        currencies = set()

        # Currency patterns
        currency_symbols = {
            '$': 'USD', '€': 'EUR', '£': 'GBP', '¥': 'JPY',
            '₹': 'INR', 'R$': 'BRL', 'C$': 'CAD', 'A$': 'AUD',
            'CHF': 'CHF', 'kr': 'SEK', 'zł': 'PLN', 'Kč': 'CZK',
        }

        currency_names = {
            'usd': 'USD', 'dollar': 'USD', 'us dollar': 'USD',
            'eur': 'EUR', 'euro': 'EUR',
            'gbp': 'GBP', 'pound': 'GBP', 'british pound': 'GBP',
            'cad': 'CAD', 'canadian dollar': 'CAD',
            'aud': 'AUD', 'australian dollar': 'AUD',
            'nzd': 'NZD', 'new zealand dollar': 'NZD',
            'chf': 'CHF', 'swiss franc': 'CHF',
            'sek': 'SEK', 'swedish krona': 'SEK',
            'nok': 'NOK', 'norwegian krone': 'NOK',
            'dkk': 'DKK', 'danish krone': 'DKK',
            'pln': 'PLN', 'polish zloty': 'PLN',
            'czk': 'CZK', 'czech koruna': 'CZK',
            'rub': 'RUB', 'russian ruble': 'RUB',
            'uah': 'UAH', 'hryvnia': 'UAH',
            'brl': 'BRL', 'real': 'BRL', 'brazilian real': 'BRL',
            'mxn': 'MXN', 'mexican peso': 'MXN',
            'zar': 'ZAR', 'rand': 'ZAR', 'south african rand': 'ZAR',
            'inr': 'INR', 'rupee': 'INR', 'indian rupee': 'INR',
            'jpy': 'JPY', 'yen': 'JPY', 'japanese yen': 'JPY',
            'cny': 'CNY', 'yuan': 'CNY', 'chinese yuan': 'CNY',
            'try': 'TRY', 'lira': 'TRY', 'turkish lira': 'TRY',
            'btc': 'BTC', 'bitcoin': 'BTC',
            'eth': 'ETH', 'ethereum': 'ETH',
            'ltc': 'LTC', 'litecoin': 'LTC',
            'naira': 'NGN', 'shilling': 'KES',
            'php': 'PHP', 'peso': 'MXN',
        }

        text = soup.get_text(' ', strip=True).lower()

        for symbol, code in currency_symbols.items():
            if symbol in text:
                currencies.add(code)

        for name, code in currency_names.items():
            if name in text:
                currencies.add(code)

        # Check for currency dropdowns
        for elem in soup.find_all(['select', 'ul', 'div'], class_=re.compile(r'currency|payment', re.I)):
            for option in elem.find_all(['option', 'a', 'li', 'span']):
                opt_text = option.get_text(strip=True).upper()
                if opt_text in currency_names or opt_text in currency_symbols.values():
                    currencies.add(opt_text)
                val = option.get('value', '').upper()
                if val in ('USD', 'EUR', 'GBP', 'CAD', 'AUD', 'NZD', 'CHF', 'SEK', 'NOK', 'DKK',
                            'PLN', 'CZK', 'RUB', 'UAH', 'BRL', 'MXN', 'ZAR', 'INR', 'JPY', 'CNY',
                            'TRY', 'BTC', 'ETH', 'LTC'):
                    currencies.add(val)

        return sorted(currencies)

    def _extract_license_info(self, soup: BeautifulSoup, html: str) -> Dict[str, str]:
        """Extract licensing information."""
        result = {
            'license_type': None,
            'license_number': None,
            'license_url': None,
        }

        text = soup.get_text(' ', strip=True)
        text_lower = text.lower()

        # Known license patterns
        license_patterns = [
            (r'(?:licensed?\s+(?:by|under)\s+)(?:the\s+)?(malta\s+gaming\s+authority|mga)', 'MGA'),
            (r'(?:licensed?\s+(?:by|under)\s+)(?:the\s+)?(uk\s+gambling\s+commission|ukgc)', 'UKGC'),
            (r'(?:licensed?\s+(?:by|under)\s+)(?:the\s+)?(curacao\s+(?:egaming|gaming)?|curacao)', 'Curaçao'),
            (r'(?:licensed?\s+(?:by|under)\s+)(?:the\s+)?(gibraltar\s+(?:gambling|rsg)?\s*(?:commission|authority)?)', 'Gibraltar'),
            (r'(?:licensed?\s+(?:by|under)\s+)(?:the\s+)?(isle\s+of\s+man\s+gambling)', 'Isle of Man'),
            (r'(?:licensed?\s+(?:by|under)\s+)(?:the\s+)?(kahnawake\s+gaming)', 'Kahnawake'),
            (r'mga[\/\-]?\s*[a-z]{2,3}\/\d+', None),
            (r'(?:curacao|cw)\s*(?:egaming|gaming)?\s*(?:license|licence)?\s*(?:no\.?|#)?\s*(\d+)', 'Curaçao'),
            (r'(?:ukgc|uk\s+gambling)\s*(?:license|licence)?\s*(?:no\.?|#)?\s*(\d+)', 'UKGC'),
        ]

        for pattern, license_type in license_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if license_type:
                    result['license_type'] = license_type
                break

        # Also check for license numbers
        license_number_patterns = [
            r'(?:license|licence)\s*(?:number|no\.?|#|:)\s*([A-Z0-9\-\/]+)',
            r'(?:MGA|UKGC|AGCC|GSC|KGC|CRAIOJ|DGOJ|ONJN|AMS)\s*[\/\-]?\s*([A-Z0-9\-\/]+)',
        ]

        for pattern in license_number_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                num = match.group(1).strip()
                if len(num) >= 2:
                    result['license_number'] = num
                    break

        # Check for license images/badges
        for img in soup.find_all('img'):
            alt = (img.get('alt', '') + ' ' + img.get('title', '')).lower()
            src = (img.get('src', '') + ' ' + img.get('data-src', '')).lower()
            if 'license' in alt or 'license' in src or 'mga' in alt or 'ukgc' in alt:
                for lic_type in ['MGA', 'UKGC', 'Curaçao', 'Gibraltar', 'Isle of Man']:
                    if lic_type.lower() in alt or lic_type.lower() in src:
                        result['license_type'] = lic_type
                        break

        # Check footer and legal sections
        footer = soup.find('footer')
        if footer:
            footer_text = footer.get_text(' ', strip=True).lower()
            if 'malta' in footer_text and 'gaming' in footer_text:
                result['license_type'] = 'MGA'
            elif 'uk gambling' in footer_text:
                result['license_type'] = 'UKGC'
            elif 'curacao' in footer_text:
                result['license_type'] = 'Curaçao'

        return result

    def _extract_payment_methods(self, soup: BeautifulSoup, html: str) -> Dict[str, str]:
        """Extract payment method information."""
        result = {
            'deposit_methods': [],
            'withdrawal_methods': [],
        }

        payment_keywords = {
            'visa': 'Visa', 'mastercard': 'Mastercard', 'maestro': 'Maestro',
            'amex': 'American Express', 'american express': 'American Express',
            'paypal': 'PayPal', 'skrill': 'Skrill', 'neteller': 'Neteller',
            'ecopayz': 'EcoPayz', 'paysafecard': 'Paysafecard',
            'bank transfer': 'Bank Transfer', 'wire transfer': 'Wire Transfer',
            'bank wire': 'Bank Wire', 'bankwire': 'Bank Wire',
            'bitcoin': 'Bitcoin', 'btc': 'Bitcoin', 'crypto': 'Cryptocurrency',
            'ethereum': 'Ethereum', 'eth': 'Ethereum',
            'litecoin': 'Litecoin', 'ltc': 'Litecoin',
            'apple pay': 'Apple Pay', 'google pay': 'Google Pay',
            'interac': 'Interac', 'trustly': 'Trustly', 'zimpler': 'Zimpler',
            'instadebit': 'InstaDebit', 'idebit': 'iDebit',
            'neosurf': 'Neosurf', 'flexepin': 'Flexepin',
            'jeton': 'Jeton', 'astropay': 'AstroPay',
            'muchbetter': 'MuchBetter', 'revolut': 'Revolut',
            'giropay': 'Giropay', 'sofort': 'Sofort', 'klarna': 'Klarna',
            'rapid transfer': 'Rapid Transfer', 'ideal': 'iDEAL',
            'bancontact': 'Bancontact', 'boleto': 'Boleto', 'pix': 'PIX',
            'webmoney': 'WebMoney', 'qiwi': 'Qiwi', 'yandex': 'Yandex',
            'entropay': 'Entropay', 'payeer': 'Payeer',
            'sticpay': 'SticPay', 'entercash': 'Entercash',
            'credit card': 'Credit Card', 'debit card': 'Debit Card',
        }

        text = soup.get_text(' ', strip=True).lower()

        for keyword, method in payment_keywords.items():
            if keyword in text:
                if method not in result['deposit_methods']:
                    result['deposit_methods'].append(method)

        # Look for payment logos/icons
        for img in soup.find_all('img'):
            alt = (img.get('alt', '') + ' ' + img.get('title', '')).lower()
            src = (img.get('src', '') + ' ' + img.get('data-src', '')).lower()
            combined = alt + ' ' + src
            for keyword, method in payment_keywords.items():
                if keyword in combined:
                    if method not in result['deposit_methods']:
                        result['deposit_methods'].append(method)

        return result

    def _extract_contact_info(self, soup: BeautifulSoup, html: str) -> Dict[str, Optional[str]]:
        """Extract contact information."""
        result = {
            'contact_email': None,
            'phone': None,
            'support_url': None,
            'live_chat': False,
        }

        # Extract emails
        emails = set(re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', html))
        # Filter out common non-contact emails
        contact_emails = [e for e in emails if not any(x in e.lower() for x in
                          ['sentry', 'example', 'test', 'noreply', 'no-reply',
                           'wixpress', 'sentry.io', 'webpack'])]
        if contact_emails:
            # Prefer support/info emails
            for email in contact_emails:
                if any(x in email.lower() for x in ['support', 'info', 'contact', 'help']):
                    result['contact_email'] = email
                    break
            if not result['contact_email'] and contact_emails:
                result['contact_email'] = contact_emails[0]

        # Extract phone numbers
        phone_patterns = [
            r'(?:tel|phone|call|telephone)[:\s]*([+\d\s\-\(\)]{7,20})',
            r'(\+\d{1,3}[\s\-]?\d{4,14})',
            r'(\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4})',
        ]

        for pattern in phone_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                cleaned = re.sub(r'[^\d+]', '', match)
                if len(cleaned) >= 7 and cleaned.lstrip('+').isdigit():
                    result['phone'] = match.strip()
                    break
            if result['phone']:
                break

        # Check for live chat
        chat_indicators = ['livechat', 'live-chat', 'live chat', 'chat widget',
                          'crisp', 'intercom', 'drift', 'tawk', 'zendesk chat',
                          'freshchat', 'tidio', 'olark', 'purechat']
        html_lower = html.lower()
        for indicator in chat_indicators:
            if indicator in html_lower:
                result['live_chat'] = True
                break

        # Extract support URL
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            text = a.get_text(strip=True).lower()
            if any(x in href or x in text for x in ['support', 'help', 'contact', 'faq']):
                result['support_url'] = urljoin(soup.find().get('base', {}).get('href', ''), a['href'])
                break

        return result

    def _extract_meta_info(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """Extract meta information from the page."""
        result = {
            'title': None,
            'description': None,
            'keywords': None,
        }

        title_tag = soup.find('title')
        if title_tag:
            result['title'] = title_tag.get_text(strip=True)[:200]

        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            content = meta.get('content', '')
            if name == 'description' and content:
                result['description'] = content[:500]
            elif name == 'keywords' and content:
                result['keywords'] = content[:500]

        return result

    async def collect_from_website(self, url: str) -> Dict[str, Any]:
        """Collect all available data from a casino website."""
        result = {
            'languages': None,
            'currencies': None,
            'license_type': None,
            'license_number': None,
            'deposit_methods': None,
            'withdrawal_methods': None,
            'contact_email': None,
            'phone': None,
            'support_url': None,
            'live_chat': None,
            'meta_title': None,
            'meta_description': None,
        }

        if not url or not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        session = await self._create_session()
        try:
            # Fetch main page
            html = await self._fetch_page(session, url)
            if not html:
                return result

            soup = BeautifulSoup(html, 'lxml')

            # Extract languages
            languages = self._extract_languages(soup, html)
            if languages:
                result['languages'] = ', '.join(languages)

            # Extract currencies
            currencies = self._extract_currencies(soup, html)
            if currencies:
                result['currencies'] = ', '.join(currencies)

            # Extract license info
            license_info = self._extract_license_info(soup, html)
            if license_info['license_type']:
                result['license_type'] = license_info['license_type']
            if license_info['license_number']:
                result['license_number'] = license_info['license_number']

            # Extract payment methods
            payment_info = self._extract_payment_methods(soup, html)
            if payment_info['deposit_methods']:
                result['deposit_methods'] = ', '.join(payment_info['deposit_methods'])
            if payment_info['withdrawal_methods']:
                result['withdrawal_methods'] = ', '.join(payment_info['withdrawal_methods'])

            # Extract contact info
            contact_info = self._extract_contact_info(soup, html)
            if contact_info['contact_email']:
                result['contact_email'] = contact_info['contact_email']
            if contact_info['phone']:
                result['phone'] = contact_info['phone']
            if contact_info['support_url']:
                result['support_url'] = contact_info['support_url']
            result['live_chat'] = contact_info['live_chat']

            # Extract meta info
            meta_info = self._extract_meta_info(soup)
            if meta_info['title']:
                result['meta_title'] = meta_info['title']
            if meta_info['description']:
                result['meta_description'] = meta_info['description']

            # If license not found on main page, try only one more subpage (terms page)
            if not result['license_type'] or not result['currencies']:
                for path in ['/terms', '/terms-and-conditions', '/about', '/about-us']:
                    try:
                        full_url = url.rstrip('/') + path
                        page_html = await self._fetch_page(session, full_url)
                        if page_html:
                            page_soup = BeautifulSoup(page_html, 'lxml')
                            if not result['license_type']:
                                lic = self._extract_license_info(page_soup, page_html)
                                if lic['license_type']:
                                    result['license_type'] = lic['license_type']
                                if lic['license_number']:
                                    result['license_number'] = lic['license_number']
                            if not result['currencies']:
                                curr = self._extract_currencies(page_soup, page_html)
                                if curr:
                                    result['currencies'] = ', '.join(curr)
                            # Stop as soon as we found what we needed
                            if result['license_type'] and result['currencies']:
                                break
                    except Exception:
                        continue

        except Exception as e:
            logger.error(f"Error collecting from {url}: {e}")
        finally:
            await session.close()

        return result

    async def collect_batch(self, urls: List[str], concurrency: int = 20) -> Dict[str, Dict[str, Any]]:
        """Collect data from multiple URLs concurrently."""
        semaphore = asyncio.Semaphore(concurrency)
        results = {}

        async def collect_with_semaphore(url: str):
            async with semaphore:
                result = await self.collect_from_website(url)
                results[url] = result
                # Rate limiting - minimal delay since we have semaphore
                await asyncio.sleep(0.05)

        tasks = [collect_with_semaphore(url) for url in urls]
        await asyncio.gather(*tasks, return_exceptions=True)

        return results