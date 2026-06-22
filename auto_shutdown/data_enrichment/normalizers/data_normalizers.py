"""
Data Normalizers
================
Normalization utilities for standardizing casino data formats.
"""

import re
from typing import Optional, List, Any
from urllib.parse import urlparse


class DataNormalizers:
    """Collection of normalization methods for casino data fields."""

    # Common language name mappings
    LANGUAGE_MAP = {
        'en': 'English', 'eng': 'English',
        'es': 'Spanish', 'spa': 'Spanish', 'spanish': 'Spanish',
        'fr': 'French', 'fra': 'French', 'french': 'French',
        'de': 'German', 'deu': 'German', 'german': 'German',
        'it': 'Italian', 'ita': 'Italian', 'italian': 'Italian',
        'pt': 'Portuguese', 'por': 'Portuguese', 'portuguese': 'Portuguese',
        'nl': 'Dutch', 'nld': 'Dutch', 'dutch': 'Dutch',
        'sv': 'Swedish', 'swe': 'Swedish', 'swedish': 'Swedish',
        'da': 'Danish', 'dan': 'Danish', 'danish': 'Danish',
        'fi': 'Finnish', 'fin': 'Finnish', 'finnish': 'Finnish',
        'no': 'Norwegian', 'nor': 'Norwegian', 'norwegian': 'Norwegian',
        'pl': 'Polish', 'pol': 'Polish', 'polish': 'Polish',
        'cs': 'Czech', 'ces': 'Czech', 'czech': 'Czech',
        'hu': 'Hungarian', 'hun': 'Hungarian', 'hungarian': 'Hungarian',
        'ro': 'Romanian', 'ron': 'Romanian', 'romanian': 'Romanian',
        'bg': 'Bulgarian', 'bul': 'Bulgarian', 'bulgarian': 'Bulgarian',
        'hr': 'Croatian', 'hrv': 'Croatian', 'croatian': 'Croatian',
        'sk': 'Slovak', 'slk': 'Slovak', 'slovak': 'Slovak',
        'sl': 'Slovenian', 'slv': 'Slovenian', 'slovenian': 'Slovenian',
        'el': 'Greek', 'ell': 'Greek', 'greek': 'Greek',
        'tr': 'Turkish', 'tur': 'Turkish', 'turkish': 'Turkish',
        'ru': 'Russian', 'rus': 'Russian', 'russian': 'Russian',
        'uk': 'Ukrainian', 'ukr': 'Ukrainian', 'ukrainian': 'Ukrainian',
        'ja': 'Japanese', 'jpn': 'Japanese', 'japanese': 'Japanese',
        'ko': 'Korean', 'kor': 'Korean', 'korean': 'Korean',
        'zh': 'Chinese', 'zho': 'Chinese', 'chinese': 'Chinese',
        'cn': 'Chinese',
        'hi': 'Hindi', 'hin': 'Hindi', 'hindi': 'Hindi',
        'th': 'Thai', 'tha': 'Thai', 'thai': 'Thai',
        'vi': 'Vietnamese', 'vie': 'Vietnamese', 'vietnamese': 'Vietnamese',
        'id': 'Indonesian', 'ind': 'Indonesian', 'indonesian': 'Indonesian',
        'ms': 'Malay', 'msa': 'Malay', 'malay': 'Malay',
        'ar': 'Arabic', 'ara': 'Arabic', 'arabic': 'Arabic',
        'he': 'Hebrew', 'heb': 'Hebrew', 'hebrew': 'Hebrew',
        'et': 'Estonian', 'est': 'Estonian', 'estonian': 'Estonian',
        'lv': 'Latvian', 'lav': 'Latvian', 'latvian': 'Latvian',
        'lt': 'Lithuanian', 'lit': 'Lithuanian', 'lithuanian': 'Lithuanian',
        'sr': 'Serbian', 'srp': 'Serbian', 'serbian': 'Serbian',
        'bs': 'Bosnian', 'bos': 'Bosnian', 'bosnian': 'Bosnian',
        'mk': 'Macedonian', 'mkd': 'Macedonian', 'macedonian': 'Macedonian',
        'is': 'Icelandic', 'isl': 'Icelandic', 'icelandic': 'Icelandic',
        'mt': 'Maltese', 'mlt': 'Maltese', 'maltese': 'Maltese',
        'ga': 'Irish', 'gle': 'Irish', 'irish': 'Irish',
        'cy': 'Welsh', 'cym': 'Welsh', 'welsh': 'Welsh',
        'af': 'Afrikaans', 'afr': 'Afrikaans', 'afrikaans': 'Afrikaans',
        'sw': 'Swahili', 'swa': 'Swahili', 'swahili': 'Swahili',
    }

    # Common currency mappings
    CURRENCY_MAP = {
        'usd': 'USD', '$': 'USD', 'dollars': 'USD', 'us dollar': 'USD', 'us dollars': 'USD',
        'eur': 'EUR', '€': 'EUR', 'euro': 'EUR', 'euros': 'EUR',
        'gbp': 'GBP', '£': 'GBP', 'pound': 'GBP', 'pounds': 'GBP', 'british pound': 'GBP',
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
        'uah': 'UAH', 'ukrainian hryvnia': 'UAH',
        'brl': 'BRL', 'brazilian real': 'BRL',
        'mxn': 'MXN', 'mexican peso': 'MXN',
        'ars': 'ARS', 'argentine peso': 'ARS',
        'clp': 'CLP', 'chilean peso': 'CLP',
        'zar': 'ZAR', 'south african rand': 'ZAR',
        'inr': 'INR', 'indian rupee': 'INR',
        'jpy': 'JPY', '¥': 'JPY', 'japanese yen': 'JPY',
        'cny': 'CNY', 'chinese yuan': 'CNY',
        'krw': 'KRW', 'south korean won': 'KRW',
        'try': 'TRY', 'turkish lira': 'TRY',
        'ngn': 'NGN', 'nigerian naira': 'NGN',
        'kes': 'KES', 'kenyan shilling': 'KES',
        'btc': 'BTC', 'bitcoin': 'BTC',
        'eth': 'ETH', 'ethereum': 'ETH',
        'ltc': 'LTC', 'litecoin': 'LTC',
    }

    # Known payment method keywords
    PAYMENT_KEYWORDS = {
        'visa': 'Visa',
        'mastercard': 'Mastercard',
        'master card': 'Mastercard',
        'maestro': 'Maestro',
        'amex': 'American Express',
        'american express': 'American Express',
        'paypal': 'PayPal',
        'skrill': 'Skrill',
        'neteller': 'Neteller',
        'ecopayz': 'EcoPayz',
        'ecopayz': 'EcoPayz',
        'paysafecard': 'Paysafecard',
        'pay safe card': 'Paysafecard',
        'bank transfer': 'Bank Transfer',
        'wire transfer': 'Wire Transfer',
        'bank wire': 'Bank Wire',
        'bitcoin': 'Bitcoin',
        'btc': 'Bitcoin',
        'ethereum': 'Ethereum',
        'eth': 'Ethereum',
        'litecoin': 'Litecoin',
        'ltc': 'Litecoin',
        'crypto': 'Cryptocurrency',
        'cryptocurrency': 'Cryptocurrency',
        'apple pay': 'Apple Pay',
        'google pay': 'Google Pay',
        'googlepay': 'Google Pay',
        'applepay': 'Apple Pay',
        'interac': 'Interac',
        'trustly': 'Trustly',
        'zimpler': 'Zimpler',
        'instadebit': 'InstaDebit',
        'idebit': 'iDebit',
        'neosurf': 'Neosurf',
        'flexepin': 'Flexepin',
        'jeton': 'Jeton',
        'astropay': 'AstroPay',
        'astro pay': 'AstroPay',
        'muchbetter': 'MuchBetter',
        'much better': 'MuchBetter',
        'revolut': 'Revolut',
        'giropay': 'Giropay',
        'sofort': 'Sofort',
        'klarna': 'Klarna',
        'rapid transfer': 'Rapid Transfer',
        'ideally': 'iDEAL',
        'ideal': 'iDEAL',
        'bancontact': 'Bancontact',
        'boleto': 'Boleto',
        'pix': 'PIX',
        'boleto bancario': 'Boleto',
        'webmoney': 'WebMoney',
        'qiwi': 'Qiwi',
        'yandex': 'Yandex',
        'ukash': 'Ukash',
        'entropay': 'Entropay',
        'payeer': 'Payeer',
        'perfect money': 'Perfect Money',
        'sticpay': 'SticPay',
        'fugopay': 'FugoPay',
        'upaycard': 'UPayCard',
        'entercash': 'Entercash',
        'e-wallet': 'E-Wallet',
        'ewallet': 'E-Wallet',
        'e wallet': 'E-Wallet',
        'prepaid': 'Prepaid Card',
        'debit': 'Debit Card',
        'credit': 'Credit Card',
        'credit card': 'Credit Card',
        'debit card': 'Debit Card',
    }

    # SSL Issuer normalization
    SSL_ISSUER_MAP = {
        'let\'s encrypt': "Let's Encrypt",
        'letsencrypt': "Let's Encrypt",
        "letsencrypt": "Let's Encrypt",
        'cloudflare': 'Cloudflare',
        'digicert': 'DigiCert',
        'digicert inc': 'DigiCert',
        'sectigo': 'Sectigo',
        'comodo': 'Sectigo',
        'comodo ca': 'Sectigo',
        'godaddy': 'GoDaddy',
        'go daddy': 'GoDaddy',
        'godaddy.com': 'GoDaddy',
        'amazon': 'Amazon',
        'amazon web services': 'Amazon AWS',
        'aws': 'Amazon AWS',
        'global sign': 'GlobalSign',
        'globalsign': 'GlobalSign',
        'thawte': 'Thawte',
        'verisign': 'Verisign',
        'symantec': 'Symantec',
        'geo trust': 'GeoTrust',
        'geotrust': 'GeoTrust',
        'rapidssl': 'RapidSSL',
    }

    @classmethod
    def normalize_language(cls, lang: str) -> Optional[str]:
        """Normalize a language name to proper title case."""
        if not lang or not isinstance(lang, str):
            return None
        lang = lang.strip()
        if not lang or lang.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None

        lower = lang.lower()
        if lower in cls.LANGUAGE_MAP:
            return cls.LANGUAGE_MAP[lower]

        # Return title-cased version
        return lang.strip().title()

    @classmethod
    def normalize_languages(cls, languages: str) -> Optional[str]:
        """Normalize a comma/pipe/semicolon-separated list of languages."""
        if not languages or not isinstance(languages, str):
            return None

        # Split on common separators
        parts = re.split(r'[,;|/]', languages)
        normalized = []
        for part in parts:
            result = cls.normalize_language(part.strip())
            if result and result not in normalized:
                normalized.append(result)

        return ', '.join(normalized) if normalized else None

    @classmethod
    def normalize_currency(cls, currency: str) -> Optional[str]:
        """Normalize a currency code or name to ISO 4217 code."""
        if not currency or not isinstance(currency, str):
            return None
        currency = currency.strip()
        if not currency or currency.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None

        lower = currency.lower()
        if lower in cls.CURRENCY_MAP:
            return cls.CURRENCY_MAP[lower]

        # If already a valid 3-letter code
        if len(currency) == 3 and currency.isalpha():
            return currency.upper()

        return None

    @classmethod
    def normalize_currencies(cls, currencies: str) -> Optional[str]:
        """Normalize a comma/pipe-separated list of currencies."""
        if not currencies or not isinstance(currencies, str):
            return None

        parts = re.split(r'[,;|/]', currencies)
        normalized = []
        for part in parts:
            result = cls.normalize_currency(part.strip())
            if result and result not in normalized:
                normalized.append(result)

        return ', '.join(normalized) if normalized else None

    @classmethod
    def normalize_payment_methods(cls, methods: str) -> Optional[str]:
        """Normalize payment methods to standardized names."""
        if not methods or not isinstance(methods, str):
            return None
        methods = methods.strip()
        if not methods or methods.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None

        # Split on common separators
        parts = re.split(r'[,;|/\n]', methods)
        normalized = []
        for part in parts:
            part_lower = part.strip().lower()
            if part_lower in cls.PAYMENT_KEYWORDS:
                name = cls.PAYMENT_KEYWORDS[part_lower]
                if name not in normalized:
                    normalized.append(name)
            elif part.strip():
                # Keep original if no mapping found
                cleaned = part.strip()
                if cleaned and cleaned not in normalized:
                    normalized.append(cleaned)

        return ', '.join(normalized) if normalized else None

    @classmethod
    def normalize_ssl_issuer(cls, issuer: str) -> Optional[str]:
        """Normalize SSL issuer name."""
        if not issuer or not isinstance(issuer, str):
            return None
        issuer = issuer.strip()
        if not issuer or issuer.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None

        lower = issuer.lower()
        for key, normalized in cls.SSL_ISSUER_MAP.items():
            if key in lower:
                return normalized

        return issuer.strip().title()

    @classmethod
    def normalize_country(cls, country: str) -> Optional[str]:
        """Normalize country name to standard format."""
        from ..validators.data_validators import DataValidators
        return DataValidators.validate_country(country)

    @classmethod
    def normalize_domain(cls, url: str) -> Optional[str]:
        """Extract and normalize domain from URL."""
        if not url or not isinstance(url, str):
            return None
        url = url.strip()
        if not url:
            return None

        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except Exception:
            return None

    @classmethod
    def normalize_name(cls, name: str) -> Optional[str]:
        """Normalize casino name to proper title case."""
        if not name or not isinstance(name, str):
            return None
        name = name.strip()
        if not name or name.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None

        # Handle all-caps or all-lowercase names
        words = name.split()
        normalized_words = []
        for word in words:
            # Keep brand-like capitalization
            if word.isupper() and len(word) <= 4:
                normalized_words.append(word)
            else:
                normalized_words.append(word.capitalize())

        return ' '.join(normalized_words)

    @classmethod
    def normalize_ip(cls, ip: str) -> Optional[str]:
        """Validate and normalize IP address."""
        if not ip or not isinstance(ip, str):
            return None
        ip = ip.strip()
        if not ip or ip.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None

        from ..validators.data_validators import DataValidators
        if DataValidators.validate_ip(ip):
            return ip
        return None

    @classmethod
    def normalize_year(cls, year: Any) -> Optional[int]:
        """Normalize establishment year."""
        if year is None:
            return None
        try:
            y = int(float(str(year).strip()))
            if 1900 <= y <= 2025:
                return y
        except (ValueError, TypeError):
            pass
        return None

    @classmethod
    def normalize_license_number(cls, number: str) -> Optional[str]:
        """Normalize license number format."""
        if not number or not isinstance(number, str):
            return None
        number = number.strip()
        if not number or number.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None
        # Remove excessive whitespace
        number = re.sub(r'\s+', ' ', number)
        return number

    @classmethod
    def clean_text(cls, text: str) -> Optional[str]:
        """Generic text cleaner."""
        if not text or not isinstance(text, str):
            return None
        text = text.strip()
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove control characters
        text = re.sub(r'[\x00-\x1f\x7f]', '', text)
        if not text or text.lower() in ('unknown', 'n/a', 'na', 'none', 'null', ''):
            return None
        return text