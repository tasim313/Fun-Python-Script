"""
DNS Collector
=============
Collects DNS-related information: IP address, hosting provider, nameservers.
"""

import asyncio
import socket
import logging
import re
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

# Known hosting providers mapped by nameserver patterns
HOSTING_PROVIDER_MAP = {
    'bluehost': 'Bluehost',
    'godaddy': 'GoDaddy',
    'namecheap': 'Namecheap',
    'dreamhost': 'DreamHost',
    'hostgator': 'HostGator',
    'siteground': 'SiteGround',
    'wpengine': 'WP Engine',
    'cloudflare': 'Cloudflare',
    'amazonaws': 'Amazon AWS',
    'akamai': 'Akamai',
    'fastly': 'Fastly',
    'digitalocean': 'DigitalOcean',
    'linode': 'Linode',
    'vultr': 'Vultr',
    'heroku': 'Heroku',
    'netlify': 'Netlify',
    'vercel': 'Vercel',
    'google': 'Google Cloud',
    'azure': 'Microsoft Azure',
    'rackspace': 'Rackspace',
    'ovh': 'OVH',
    'hetzner': 'Hetzner',
    'ionos': 'IONOS',
    '1and1': 'IONOS',
    'gandi': 'Gandi',
    'porkbun': 'Porkbun',
    'hover': 'Hover',
    'domaincontrol': 'GoDaddy',
    'dotster': 'Dotster',
    'enom': 'eNom',
    'netsol': 'Network Solutions',
    'register': 'Register.com',
    'registrar': 'Generic Registrar',
    'dns': 'DNS Provider',
    'cloudfront': 'Amazon CloudFront',
    'incapsula': 'Incapsula',
    'imperva': 'Imperva',
    'sucuri': 'Sucuri',
    'wordfence': 'Wordfence',
}

# Nameserver to hosting provider mapping
NS_HOSTING_MAP = {
    'ns1.bluehost.com': 'Bluehost',
    'ns2.bluehost.com': 'Bluehost',
    'ns1.godaddy.com': 'GoDaddy',
    'ns2.godaddy.com': 'GoDaddy',
    'ns3.godaddy.com': 'GoDaddy',
    'ns4.godaddy.com': 'GoDaddy',
    'ns1.namecheap.com': 'Namecheap',
    'ns2.namecheap.com': 'Namecheap',
    'dns1.namecheaphosting.com': 'Namecheap',
    'dns2.namecheaphosting.com': 'Namecheap',
    'ns1.siteground.com': 'SiteGround',
    'ns2.siteground.com': 'SiteGround',
    'ns1.dreamhost.com': 'DreamHost',
    'ns2.dreamhost.com': 'DreamHost',
    'ns3.dreamhost.com': 'DreamHost',
    'ns1.hostgator.com': 'HostGator',
    'ns2.hostgator.com': 'HostGator',
    'ns1.wpengine.com': 'WP Engine',
    'ns2.wpengine.com': 'WP Engine',
    'ns1.cloudflare.com': 'Cloudflare',
    'ns2.cloudflare.com': 'Cloudflare',
    'ns3.cloudflare.com': 'Cloudflare',
    'ns4.cloudflare.com': 'Cloudflare',
    'ns1.dotster.com': 'Dotster',
    'ns2.dotster.com': 'Dotster',
    'ns19.domaincontrol.com': 'GoDaddy',
    'ns20.domaincontrol.com': 'GoDaddy',
    'ns21.domaincontrol.com': 'GoDaddy',
    'ns22.domaincontrol.com': 'GoDaddy',
    'ns1.enom.com': 'eNom',
    'ns2.enom.com': 'eNom',
    'dns1.p01.nsone.net': 'NS1',
    'dns2.p01.nsone.net': 'NS1',
    'a.dns.hostedzone.com': 'Amazon Route53',
    'b.dns.hostedzone.com': 'Amazon Route53',
}


class DNSCollector:
    """Collects DNS information for casino domains."""

    def __init__(self):
        pass

    def get_ip_address(self, domain: str) -> Optional[str]:
        """Resolve domain to IP address."""
        try:
            # Remove www. prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            ip = socket.gethostbyname(domain)
            return ip
        except socket.gaierror:
            return None
        except Exception as e:
            logger.debug(f"DNS resolution error for {domain}: {e}")
            return None

    def get_nameservers(self, domain: str) -> Optional[str]:
        """Get nameservers for a domain using dig/nslookup."""
        import subprocess

        try:
            if domain.startswith('www.'):
                domain = domain[4:]

            # Try dig first
            result = subprocess.run(
                ['dig', '+short', 'NS', domain],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                ns_list = [ns.strip().rstrip('.') for ns in result.stdout.strip().split('\n') if ns.strip()]
                if ns_list:
                    return ' | '.join(ns_list[:4])

            # Fallback to nslookup
            result = subprocess.run(
                ['nslookup', '-type=NS', domain],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                ns_list = []
                for line in result.stdout.split('\n'):
                    if 'nameserver' in line.lower():
                        ns = line.split('=')[-1].strip() if '=' in line else line.split(':')[-1].strip()
                        if ns:
                            ns_list.append(ns.rstrip('.'))
                if ns_list:
                    return ' | '.join(ns_list[:4])

        except subprocess.TimeoutExpired:
            logger.debug(f"DNS lookup timeout for {domain}")
        except FileNotFoundError:
            # dig not available, try host command
            try:
                result = subprocess.run(
                    ['host', '-t', 'NS', domain],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    ns_list = []
                    for line in result.stdout.split('\n'):
                        if 'name server' in line.lower():
                            ns = line.split()[-1].strip().rstrip('.')
                            if ns:
                                ns_list.append(ns)
                    if ns_list:
                        return ' | '.join(ns_list[:4])
            except Exception:
                pass
        except Exception as e:
            logger.debug(f"Nameserver lookup error for {domain}: {e}")

        return None

    def detect_hosting_provider(self, domain: str, nameservers: Optional[str] = None) -> Optional[str]:
        """Detect hosting provider from nameservers."""
        if nameservers:
            ns_lower = nameservers.lower()
            for ns_key, provider in NS_HOSTING_MAP.items():
                if ns_key in ns_lower:
                    return provider

            # Fuzzy matching
            for key, provider in HOSTING_PROVIDER_MAP.items():
                if key in ns_lower:
                    return provider

        # Try to detect from IP (basic check)
        if domain:
            ip = self.get_ip_address(domain)
            if ip:
                # Check common IP ranges for major providers
                # This is a simplified check
                pass

        return None

    async def collect_dns_info(self, domain: str) -> Dict[str, Optional[str]]:
        """Collect all DNS information for a domain."""
        result = {
            'ip_address': None,
            'nameservers': None,
            'hosting_provider': None,
        }

        if not domain:
            return result

        # Clean domain
        clean_domain = domain.strip().lower()
        if clean_domain.startswith('www.'):
            clean_domain = clean_domain[4:]
        if clean_domain.startswith(('http://', 'https://')):
            from urllib.parse import urlparse
            try:
                parsed = urlparse(clean_domain)
                clean_domain = parsed.netloc
            except Exception:
                pass

        # Get IP
        ip = self.get_ip_address(clean_domain)
        if ip:
            result['ip_address'] = ip

        # Get nameservers
        nameservers = self.get_nameservers(clean_domain)
        if nameservers:
            result['nameservers'] = nameservers

        # Detect hosting provider
        hosting = self.detect_hosting_provider(clean_domain, nameservers)
        if hosting:
            result['hosting_provider'] = hosting

        return result

    async def collect_batch(self, domains: List[str], concurrency: int = 30) -> Dict[str, Dict[str, Optional[str]]]:
        """Collect DNS info for multiple domains concurrently."""
        semaphore = asyncio.Semaphore(concurrency)
        results = {}

        async def collect_with_semaphore(domain: str):
            async with semaphore:
                result = await self.collect_dns_info(domain)
                results[domain] = result
                # Small delay to avoid overwhelming DNS
                await asyncio.sleep(0.05)

        tasks = [collect_with_semaphore(domain) for domain in domains]
        await asyncio.gather(*tasks, return_exceptions=True)

        return results