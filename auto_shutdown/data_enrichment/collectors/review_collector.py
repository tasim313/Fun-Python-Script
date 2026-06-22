"""
Review Collector
================
Collects casino review data from public review sites and directories.
"""

import asyncio
import aiohttp
import re
import logging
from typing import Optional, Dict, Any, List
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ReviewCollector:
    """Collects casino review data from public sources."""

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    # Casino review directory URLs
    REVIEW_SOURCES = [
        {
            'name': 'askgamblers',
            'search_url': 'https://www.askgamblers.com/search?q={domain}',
            'type': 'search',
        },
        {
            'name': 'casinomeister',
            'search_url': 'https://www.casinomeister.com/search/?q={domain}',
            'type': 'search',
        },
        {
            'name': 'trustpilot',
            'search_url': 'https://www.trustpilot.com/search?query={domain}',
            'type': 'search',
        },
    ]

    def __init__(self, timeout: int = 15):
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    def _extract_rating(self, text: str) -> Optional[float]:
        """Extract numeric rating from text."""
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:out of|\/)\s*(?:5|10|100)',
            r'rating:?\s*(\d+(?:\.\d+)?)',
            r'score:?\s*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*\/\s*(?:5|10)',
            r'(\d+(?:\.\d+)?)\s*stars?',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    score = float(match.group(1))
                    if 0 <= score <= 10:
                        return round(score, 1)
                except ValueError:
                    pass
        return None

    def _extract_review_count(self, text: str) -> Optional[int]:
        """Extract review count from text."""
        patterns = [
            r'(\d+(?:,\d+)*)\s*reviews?',
            r'reviews?:?\s*(\d+(?:,\d+)*)',
            r'(\d+(?:,\d+)*)\s*(?:player|user)\s*(?:reviews?|ratings?)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    count = int(match.group(1).replace(',', ''))
                    if 0 <= count <= 1000000:
                        return count
                except ValueError:
                    pass
        return None

    def _extract_trust_indicators(self, soup: BeautifulSoup, text: str) -> Dict[str, Any]:
        """Extract trust and safety indicators."""
        result = {
            'trust_score': None,
            'rating': None,
            'review_count': None,
        }

        # Look for rating in structured data (JSON-LD)
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if 'aggregateRating' in data:
                        rating_data = data['aggregateRating']
                        if 'ratingValue' in rating_data:
                            result['rating'] = float(rating_data['ratingValue'])
                        if 'reviewCount' in rating_data:
                            result['review_count'] = int(rating_data['reviewCount'])
            except (json.JSONDecodeError, ValueError, KeyError):
                pass

        # Look for meta tags
        for meta in soup.find_all('meta'):
            prop = meta.get('property', '').lower()
            content = meta.get('content', '')
            if 'rating' in prop and content:
                try:
                    result['rating'] = float(content)
                except ValueError:
                    pass

        # Extract from visible text
        if not result['rating']:
            result['rating'] = self._extract_rating(text)

        if not result['review_count']:
            result['review_count'] = self._extract_review_count(text)

        return result

    async def _fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch a page with retry."""
        for attempt in range(3):
            try:
                async with session.get(url, allow_redirects=True, ssl=False) as response:
                    if response.status == 200:
                        return await response.text(errors='ignore')
                    return None
            except asyncio.TimeoutError:
                await asyncio.sleep(1 * (attempt + 1))
            except aiohttp.ClientError:
                await asyncio.sleep(1 * (attempt + 1))
            except Exception:
                await asyncio.sleep(1 * (attempt + 1))
        return None

    async def collect_from_source(self, domain: str, source: Dict) -> Dict[str, Any]:
        """Collect review data from a single source."""
        result = {
            'source': source['name'],
            'trust_score': None,
            'rating': None,
            'review_count': None,
        }

        try:
            url = source['search_url'].format(domain=domain)
            session = aiohttp.ClientSession(timeout=self.timeout, headers=self.HEADERS)
            try:
                html = await self._fetch_page(session, url)
                if html:
                    soup = BeautifulSoup(html, 'lxml')
                    text = soup.get_text(' ', strip=True)
                    trust_data = self._extract_trust_indicators(soup, text)
                    result.update(trust_data)
            finally:
                await session.close()

        except Exception as e:
            logger.debug(f"Error collecting from {source['name']} for {domain}: {e}")

        return result

    async def collect_all_reviews(self, domain: str) -> Dict[str, Any]:
        """Collect review data from all sources."""
        results = {
            'trust_score': None,
            'rating': None,
            'review_count': None,
            'best_source': None,
        }

        tasks = [self.collect_from_source(domain, source) for source in self.REVIEW_SOURCES]
        source_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Find best result (most complete)
        for res in source_results:
            if isinstance(res, dict):
                if res.get('rating') and not results['rating']:
                    results['rating'] = res['rating']
                    results['best_source'] = res.get('source')
                if res.get('review_count') and not results['review_count']:
                    results['review_count'] = res['review_count']
                if res.get('trust_score') and not results['trust_score']:
                    results['trust_score'] = res['trust_score']

        return results

    async def collect_batch(self, domains: List[str], concurrency: int = 10) -> Dict[str, Dict[str, Any]]:
        """Collect review data for multiple domains."""
        semaphore = asyncio.Semaphore(concurrency)
        results = {}

        async def collect_with_semaphore(domain: str):
            async with semaphore:
                result = await self.collect_all_reviews(domain)
                results[domain] = result
                await asyncio.sleep(1)  # Rate limit for review sites

        tasks = [collect_with_semaphore(domain) for domain in domains]
        await asyncio.gather(*tasks, return_exceptions=True)

        return results