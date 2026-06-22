"""
SSL Collector
=============
Collects SSL certificate information for casino domains.
"""

import asyncio
import ssl
import socket
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class SSLCollector:
    """Collects SSL certificate information for casino domains."""

    def __init__(self):
        pass

    def get_ssl_info(self, domain: str) -> Dict[str, Optional[str]]:
        """Get SSL certificate information for a domain."""
        result = {
            'ssl_issuer': None,
            'ssl_subject': None,
            'ssl_valid_from': None,
            'ssl_valid_until': None,
        }

        if not domain:
            return result

        # Clean domain
        clean_domain = domain.strip().lower()
        if clean_domain.startswith('www.'):
            clean_domain = clean_domain[4:]
        if clean_domain.startswith(('http://', 'https://')):
            try:
                parsed = urlparse(clean_domain)
                clean_domain = parsed.netloc
            except Exception:
                pass

        # Remove port if present
        if ':' in clean_domain:
            clean_domain = clean_domain.split(':')[0]

        try:
            # Create SSL context that doesn't verify certificates
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with socket.create_connection((clean_domain, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=clean_domain) as ssock:
                    cert = ssock.getpeercert(binary_form=True)

                    if cert:
                        # Parse the binary certificate using cryptography library
                        try:
                            from cryptography import x509

                            cert_obj = x509.load_der_x509_certificate(cert)

                            # Extract issuer - prefer Organization Name over Common Name
                            org_name = None
                            common_name = None
                            for attr in cert_obj.issuer:
                                if attr.oid == x509.oid.NameOID.ORGANIZATION_NAME:
                                    org_name = attr.value
                                elif attr.oid == x509.oid.NameOID.COMMON_NAME:
                                    common_name = attr.value

                            # Use org name as issuer if available, otherwise common name
                            result['ssl_issuer'] = org_name or common_name

                            # Extract subject
                            for attr in cert_obj.subject:
                                if attr.oid == x509.oid.NameOID.COMMON_NAME:
                                    result['ssl_subject'] = attr.value
                                    break

                            # Validity dates
                            result['ssl_valid_from'] = cert_obj.not_valid_before_utc.strftime('%Y-%m-%d')
                            result['ssl_valid_until'] = cert_obj.not_valid_after_utc.strftime('%Y-%m-%d')

                        except ImportError:
                            # cryptography not available, fall back to basic cert dict
                            cert_dict = ssock.getpeercert()
                            if cert_dict:
                                issuer = cert_dict.get('issuer', ())
                                for rdn in issuer:
                                    for attr in rdn:
                                        if attr[0] == 'organizationName':
                                            result['ssl_issuer'] = attr[1]
                                        elif attr[0] == 'commonName' and not result['ssl_issuer']:
                                            result['ssl_issuer'] = attr[1]
                                subject = cert_dict.get('subject', ())
                                for rdn in subject:
                                    for attr in rdn:
                                        if attr[0] == 'commonName':
                                            result['ssl_subject'] = attr[1]
                                not_before = cert_dict.get('notBefore', '')
                                not_after = cert_dict.get('notAfter', '')
                                if not_before:
                                    result['ssl_valid_from'] = not_before
                                if not_after:
                                    result['ssl_valid_until'] = not_after

        except ImportError:
            # cryptography module not available, try basic SSL
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

                with socket.create_connection((clean_domain, 443), timeout=10) as sock:
                    with ctx.wrap_socket(sock, server_hostname=clean_domain) as ssock:
                        cert_dict = ssock.getpeercert()
                        if cert_dict:
                            # Extract issuer from cert dict
                            issuer = cert_dict.get('issuer', ())
                            for rdn in issuer:
                                for attr in rdn:
                                    if attr[0] == 'organizationName':
                                        result['ssl_issuer'] = attr[1]
                                    elif attr[0] == 'commonName' and not result['ssl_issuer']:
                                        result['ssl_issuer'] = attr[1]

                            # Extract subject
                            subject = cert_dict.get('subject', ())
                            for rdn in subject:
                                for attr in rdn:
                                    if attr[0] == 'commonName':
                                        result['ssl_subject'] = attr[1]

                            # Validity dates
                            not_before = cert_dict.get('notBefore', '')
                            not_after = cert_dict.get('notAfter', '')
                            if not_before:
                                result['ssl_valid_from'] = not_before
                            if not_after:
                                result['ssl_valid_until'] = not_after

            except Exception as e:
                logger.debug(f"SSL connection error for {domain}: {e}")

        except ssl.SSLCertVerificationError:
            logger.debug(f"SSL verification error for {domain}")
        except socket.timeout:
            logger.debug(f"SSL timeout for {domain}")
        except socket.gaierror:
            logger.debug(f"DNS resolution error for {domain}")
        except ConnectionRefusedError:
            logger.debug(f"Connection refused for {domain}")
        except OSError as e:
            logger.debug(f"OS error connecting to {domain}: {e}")
        except Exception as e:
            logger.debug(f"Error getting SSL info for {domain}: {e}")

        return result

    async def collect_ssl_info(self, domain: str) -> Dict[str, Optional[str]]:
        """Async wrapper for SSL info collection."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.get_ssl_info, domain)

    async def collect_batch(self, domains: list, concurrency: int = 30) -> Dict[str, Dict[str, Optional[str]]]:
        """Collect SSL info for multiple domains concurrently."""
        semaphore = asyncio.Semaphore(concurrency)
        results = {}

        async def collect_with_semaphore(domain: str):
            async with semaphore:
                result = await self.collect_ssl_info(domain)
                results[domain] = result
                await asyncio.sleep(0.05)

        tasks = [collect_with_semaphore(domain) for domain in domains]
        await asyncio.gather(*tasks, return_exceptions=True)

        return results