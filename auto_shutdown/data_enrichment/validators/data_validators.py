"""
Data Validators
===============
Validation utilities for enriched casino data.
"""

import re
from typing import Optional, Any
from urllib.parse import urlparse


class DataValidators:
    """Collection of validation methods for casino data fields."""

    VALID_TLDS = {
        '.com', '.net', '.org', '.io', '.co', '.uk', '.us', '.eu', '.de',
        '.fr', '.es', '.it', '.nl', '.se', '.dk', '.fi', '.no', '.be',
        '.at', '.ch', '.pt', '.pl', '.cz', '.ro', '.bg', '.hr', '.si',
        '.sk', '.hu', '.ie', '.gr', '.cy', '.mt', '.lu', '.ee', '.lv',
        '.lt', '.ru', '.ua', '.kz', '.cn', '.jp', '.kr', '.in', '.au',
        '.nz', '.ca', '.br', '.mx', '.ar', '.cl', '.co.za', '.ng',
        '.ke', '.gh', '.ph', '.th', '.vn', '.id', '.my', '.sg',
    }

    KNOWN_LICENSES = {
        'malta gaming authority': 'MGA',
        'mga': 'MGA',
        'uk gambling commission': 'UKGC',
        'ukgc': 'UKGC',
        'curacao egaming': 'Curaçao',
        'curacao': 'Curaçao',
        'gibraltar gambling commission': 'Gibraltar',
        'gibraltar': 'Gibraltar',
        'isle of man gambling supervision commission': 'Isle of Man',
        'isle of man': 'Isle of Man',
        'alderney gambling control commission': 'Alderney',
        'alderney': 'Alderney',
        'kahnawake gaming commission': 'Kahnawake',
        'kahnawake': 'Kahnawake',
        'philippine amusement and gaming corporation': 'PAGCOR',
        'pagcor': 'PAGCOR',
        'spelinspektionen': 'Spelinspektionen',
        'danish gambling authority': 'Spillemyndigheden',
        'spillemyndigheden': 'Spillemyndigheden',
        'schleswig-holstein': 'Schleswig-Holstein',
        'ams': 'AMS (Netherlands)',
        'kansspelautoriteit': 'AMS (Netherlands)',
        'anb': 'ANB (Belgium)',
        'belgian gaming commission': 'ANB (Belgium)',
        'dgoj': 'DGOJ (Spain)',
        'dirección general de ordenación del juego': 'DGOJ (Spain)',
        'adm': 'ADM (Italy)',
        'agenzia delle dogane e dei monopoli': 'ADM (Italy)',
        'onjn': 'ONJN (Romania)',
        'craioj': 'CRAIOJ (Romania)',
        'svg': 'Curaçao',
        'antillephone': 'Curaçao',
        'cyprus': 'Cyprus',
        ' costa rica': 'Costa Rica',
        'costa rica': 'Costa Rica',
        'panama': 'Panama',
    }

    KNOWN_COUNTRIES = {
        'united kingdom', 'uk', 'gb', 'great britain', 'england',
        'united states', 'us', 'usa', 'united states of america',
        'germany', 'deutschland', 'de',
        'france', 'fr',
        'spain', 'espana', 'es',
        'italy', 'italia', 'it',
        'netherlands', 'holland', 'nl',
        'sweden', 'se',
        'denmark', 'dk',
        'finland', 'suomi', 'fi',
        'norway', 'no',
        'belgium', 'be',
        'austria', 'at',
        'switzerland', 'schweiz', 'ch',
        'portugal', 'pt',
        'poland', 'pl',
        'czech republic', 'czechia', 'cz',
        'romania', 'ro',
        'bulgaria', 'bg',
        'croatia', 'hr',
        'slovenia', 'si',
        'slovakia', 'sk',
        'hungary', 'hu',
        'ireland', 'ie',
        'greece', 'gr',
        'cyprus', 'cy',
        'malta', 'mt',
        'luxembourg', 'lu',
        'estonia', 'ee',
        'latvia', 'lv',
        'lithuania', 'lt',
        'russia', 'ru',
        'ukraine', 'ua',
        'kazakhstan', 'kz',
        'china', 'cn',
        'japan', 'jp',
        'south korea', 'kr',
        'india', 'in',
        'australia', 'au',
        'new zealand', 'nz',
        'canada', 'ca',
        'brazil', 'br',
        'mexico', 'mx',
        'argentina', 'ar',
        'chile', 'cl',
        'colombia', 'co',
        'south africa', 'za',
        'nigeria', 'ng',
        'kenya', 'ke',
        'ghana', 'gh',
        'philippines', 'ph',
        'thailand', 'th',
        'vietnam', 'vn',
        'indonesia', 'id',
        'malaysia', 'my',
        'singapore', 'sg',
        'curacao', 'cw',
        'gibraltar', 'gi',
        'isle of man', 'im',
        'costa rica', 'cr',
        'panama', 'pa',
    }

    COUNTRY标准化_MAP = {
        'uk': 'United Kingdom',
        'gb': 'United Kingdom',
        'great britain': 'United Kingdom',
        'england': 'United Kingdom',
        'us': 'United States',
        'usa': 'United States',
        'united states of america': 'United States',
        'deutschland': 'Germany',
        'de': 'Germany',
        'espana': 'Spain',
        'es': 'Spain',
        'italia': 'Italy',
        'it': 'Italy',
        'holland': 'Netherlands',
        'nl': 'Netherlands',
        'suomi': 'Finland',
        'se': 'Sweden',
        'dk': 'Denmark',
        'fi': 'Finland',
        'no': 'Norway',
        'be': 'Belgium',
        'at': 'Austria',
        'schweiz': 'Switzerland',
        'ch': 'Switzerland',
        'pt': 'Portugal',
        'pl': 'Poland',
        'cz': 'Czech Republic',
        'czechia': 'Czech Republic',
        'ro': 'Romania',
        'bg': 'Bulgaria',
        'hr': 'Croatia',
        'si': 'Slovenia',
        'sk': 'Slovakia',
        'hu': 'Hungary',
        'ie': 'Ireland',
        'gr': 'Greece',
        'cy': 'Cyprus',
        'mt': 'Malta',
        'lu': 'Luxembourg',
        'ee': 'Estonia',
        'lv': 'Latvia',
        'lt': 'Lithuania',
        'ru': 'Russia',
        'ua': 'Ukraine',
        'kz': 'Kazakhstan',
        'cn': 'China',
        'jp': 'Japan',
        'kr': 'South Korea',
        'in': 'India',
        'au': 'Australia',
        'nz': 'New Zealand',
        'ca': 'Canada',
        'br': 'Brazil',
        'mx': 'Mexico',
        'ar': 'Argentina',
        'cl': 'Chile',
        'co': 'Colombia',
        'za': 'South Africa',
        'ng': 'Nigeria',
        'ke': 'Kenya',
        'gh': 'Ghana',
        'ph': 'Philippines',
        'th': 'Thailand',
        'vn': 'Vietnam',
        'id': 'Indonesia',
        'my': 'Malaysia',
        'sg': 'Singapore',
        'cw': 'Curaçao',
        'gi': 'Gibraltar',
        'im': 'Isle of Man',
        'cr': 'Costa Rica',
        'pa': 'Panama',
    }

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate if a string is a proper URL."""
        if not url or not isinstance(url, str):
            return False
        url = url.strip()
        if not url:
            return False
        try:
            result = urlparse(url)
            return all([result.scheme in ('http', 'https'), result.netloc])
        except Exception:
            return False

    @staticmethod
    def validate_domain(domain: str) -> bool:
        """Validate if a string is a proper domain name."""
        if not domain or not isinstance(domain, str):
            return False
        domain = domain.strip().lower()
        if not domain:
            return False
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        if not email or not isinstance(email, str):
            return False
        email = email.strip()
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format."""
        if not phone or not isinstance(phone, str):
            return False
        cleaned = re.sub(r'[\s\-\(\)\+\.]', '', phone)
        return len(cleaned) >= 7 and cleaned.isdigit()

    @staticmethod
    def validate_ip(ip: str) -> bool:
        """Validate IPv4 address."""
        if not ip or not isinstance(ip, str):
            return False
        ip = ip.strip()
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        parts = ip.split('.')
        return all(0 <= int(p) <= 255 for p in parts)

    @staticmethod
    def validate_year(year: Any) -> bool:
        """Validate establishment year."""
        if year is None:
            return False
        try:
            y = int(year)
            return 1900 <= y <= 2025
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_country(country: str) -> Optional[str]:
        """Validate and normalize country name. Returns standardized name or None."""
        if not country or not isinstance(country, str):
            return None
        country = country.strip()
        if not country or country.lower() in ('unknown', 'n/a', 'na', 'none', 'global', ''):
            return None

        lower = country.lower()

        # Direct match
        if lower in DataValidators.COUNTRY标准化_MAP:
            return DataValidators.COUNTRY标准化_MAP[lower]

        # Check if already properly formatted
        for valid in DataValidators.KNOWN_COUNTRIES:
            if lower == valid:
                # Capitalize properly
                return country.title() if len(country) <= 4 else country

        return country.title() if len(country) <= 30 else None

    @staticmethod
    def validate_license_type(license_type: str) -> Optional[str]:
        """Validate and normalize license type."""
        if not license_type or not isinstance(license_type, str):
            return None
        lt = license_type.strip()
        if not lt or lt.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None
        return lt

    @staticmethod
    def validate_language(lang: str) -> Optional[str]:
        """Validate and normalize language name."""
        if not lang or not isinstance(lang, str):
            return None
        lang = lang.strip()
        if not lang or lang.lower() in ('unknown', 'n/a', 'na', 'none', ''):
            return None
        return lang

    @staticmethod
    def validate_currency(currency: str) -> Optional[str]:
        """Validate currency code (ISO 4217)."""
        if not currency or not isinstance(currency, str):
            return None
        currency = currency.strip().upper()
        if not currency or currency in ('UNKNOWN', 'N/A', 'NA', 'NONE', ''):
            return None
        # ISO 4217 codes are 3 letters
        if len(currency) == 3 and currency.isalpha():
            return currency
        return None

    @staticmethod
    def validate_trust_score(score: Any) -> Optional[float]:
        """Validate trust score (0-10 scale)."""
        if score is None:
            return None
        try:
            s = float(score)
            if 0 <= s <= 10:
                return round(s, 1)
        except (ValueError, TypeError):
            pass
        return None

    @staticmethod
    def validate_rating(score: Any) -> Optional[float]:
        """Validate rating score (0-5 or 0-10 scale)."""
        if score is None:
            return None
        try:
            s = float(score)
            if 0 <= s <= 5:
                return round(s, 1)
            elif 0 <= s <= 10:
                return round(s, 1)
        except (ValueError, TypeError):
            pass
        return None

    @staticmethod
    def is_missing_or_invalid(value: Any) -> bool:
        """Check if a value is missing, null, empty, or a placeholder."""
        if value is None:
            return True
        if isinstance(value, float) and (value != value):  # NaN check
            return True
        if isinstance(value, str):
            stripped = value.strip()
            if stripped == '':
                return True
            if stripped.lower() in ('unknown', 'n/a', 'na', 'none', 'null', 'undefined', ''):
                return True
        return False

    @staticmethod
    def validate_payment_methods(methods: str) -> Optional[str]:
        """Validate and clean payment methods string."""
        if DataValidators.is_missing_or_invalid(methods):
            return None
        if isinstance(methods, str):
            cleaned = methods.strip()
            if cleaned:
                return cleaned
        return None