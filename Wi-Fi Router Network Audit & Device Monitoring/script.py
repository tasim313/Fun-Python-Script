#!/usr/bin/env python3
"""
Wi-Fi Router Network Audit & Device Monitoring Script

This script performs comprehensive network auditing including:
- Router information extraction
- Connected device discovery and monitoring
- Bandwidth usage analysis
- Unknown device detection
- Network security assessment

Usage: python router_audit.py
"""

import requests
import json
import time
import re
import socket
import subprocess
import platform
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from collections import defaultdict
import ipaddress
import threading
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
import argparse
import os

# Disable SSL warnings for router connections
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@dataclass
class Device:
    """Represents a network device"""
    mac: str
    ip: str
    hostname: str = "Unknown"
    vendor: str = "Unknown"
    connection_type: str = "Unknown"
    signal_strength: str = "N/A"
    connected_time: str = "Unknown"
    first_seen: datetime = None
    last_seen: datetime = None
    bytes_sent: int = 0
    bytes_received: int = 0
    is_authorized: bool = False

@dataclass
class RouterInfo:
    """Represents router information"""
    model: str = "Unknown"
    manufacturer: str = "Unknown"
    firmware: str = "Unknown"
    wan_ip: str = "Unknown"
    lan_ip: str = "Unknown"
    subnet_mask: str = "Unknown"
    ssid_24ghz: str = "Unknown"
    ssid_5ghz: str = "Unknown"
    security_type: str = "Unknown"
    uptime: str = "Unknown"
    dhcp_range: str = "Unknown"
    dns_servers: List[str] = None

class RouterAuditor:
    def __init__(self, router_ip="192.168.1.1", username="admin", password="admin"):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.verify = False  # Skip SSL verification for routers
        self.devices = {}
        self.authorized_macs = set()
        self.load_authorized_devices()
        
        # Router-specific parsers (can be extended)
        self.router_parsers = {
            'tp-link': self.parse_tplink,
            'netgear': self.parse_netgear,
            'asus': self.parse_asus,
            'linksys': self.parse_linksys,
            'generic': self.parse_generic
        }
        
    def load_authorized_devices(self):
        """Load authorized MAC addresses from file"""
        auth_file = "authorized_devices.txt"
        if os.path.exists(auth_file):
            with open(auth_file, 'r') as f:
                for line in f:
                    mac = line.strip().upper()
                    if mac and ':' in mac:
                        self.authorized_macs.add(mac)
        else:
            print(f"Creating {auth_file} - add authorized MAC addresses (one per line)")
            with open(auth_file, 'w') as f:
                f.write("# Add authorized MAC addresses, one per line\n")
                f.write("# Example: AA:BB:CC:DD:EE:FF\n")

    def detect_router_type(self) -> str:
        """Detect router manufacturer/type"""
        try:
            response = self.session.get(f"http://{self.router_ip}", timeout=10)
            content = response.text.lower()
            
            if 'tp-link' in content or 'tplink' in content:
                return 'tp-link'
            elif 'netgear' in content:
                return 'netgear'
            elif 'asus' in content:
                return 'asus'
            elif 'linksys' in content:
                return 'linksys'
            else:
                return 'generic'
        except:
            return 'generic'

    def authenticate(self) -> bool:
        """Authenticate with router"""
        try:
            # Try common authentication methods
            auth_methods = [
                self.basic_auth,
                self.form_auth,
                self.digest_auth
            ]
            
            for method in auth_methods:
                if method():
                    print("Authentication successful")
                    return True
            
            print("Authentication failed")
            return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def basic_auth(self) -> bool:
        """Try HTTP Basic Authentication"""
        try:
            response = self.session.get(
                f"http://{self.router_ip}/",
                auth=(self.username, self.password),
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def form_auth(self) -> bool:
        """Try form-based authentication"""
        try:
            # Get login page
            response = self.session.get(f"http://{self.router_ip}/", timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find login form
            form = soup.find('form')
            if not form:
                return False
            
            # Submit credentials
            login_data = {
                'username': self.username,
                'password': self.password,
                'user': self.username,
                'pass': self.password,
                'login': 'Login'
            }
            
            action = form.get('action', '/')
            response = self.session.post(
                f"http://{self.router_ip}{action}",
                data=login_data,
                timeout=10
            )
            
            return 'logout' in response.text.lower() or 'admin' in response.text.lower()
        except:
            return False

    def digest_auth(self) -> bool:
        """Try HTTP Digest Authentication"""
        try:
            from requests.auth import HTTPDigestAuth
            response = self.session.get(
                f"http://{self.router_ip}/",
                auth=HTTPDigestAuth(self.username, self.password),
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def get_router_info(self) -> RouterInfo:
        """Extract router information"""
        router_type = self.detect_router_type()
        parser = self.router_parsers.get(router_type, self.parse_generic)
        return parser()

    def parse_generic(self) -> RouterInfo:
        """Generic router information parser"""
        info = RouterInfo()
        
        try:
            # Try common status pages
            status_urls = [
                "/status.html", "/info.html", "/system.html",
                "/cgi-bin/status", "/admin/status"
            ]
            
            for url in status_urls:
                try:
                    response = self.session.get(f"http://{self.router_ip}{url}", timeout=5)
                    if response.status_code == 200:
                        self.parse_status_page(response.text, info)
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"Error parsing router info: {e}")
            
        return info

    def parse_tplink(self) -> RouterInfo:
        """TP-Link specific parser"""
        info = RouterInfo()
        info.manufacturer = "TP-Link"
        
        try:
            # TP-Link specific endpoints
            endpoints = [
                "/userRpm/StatusRpm.htm",
                "/cgi-bin/luci/admin/status/overview"
            ]
            
            for endpoint in endpoints:
                try:
                    response = self.session.get(f"http://{self.router_ip}{endpoint}")
                    if response.status_code == 200:
                        self.parse_status_page(response.text, info)
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"Error parsing TP-Link info: {e}")
            
        return info

    def parse_netgear(self) -> RouterInfo:
        """Netgear specific parser"""
        info = RouterInfo()
        info.manufacturer = "Netgear"
        return info

    def parse_asus(self) -> RouterInfo:
        """ASUS specific parser"""
        info = RouterInfo()
        info.manufacturer = "ASUS"
        return info

    def parse_linksys(self) -> RouterInfo:
        """Linksys specific parser"""
        info = RouterInfo()
        info.manufacturer = "Linksys"
        return info

    def parse_status_page(self, html_content: str, info: RouterInfo):
        """Parse common status page elements"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text().lower()
            
            # Extract common information using regex
            patterns = {
                'wan_ip': r'wan.*?ip.*?(\d+\.\d+\.\d+\.\d+)',
                'lan_ip': r'lan.*?ip.*?(\d+\.\d+\.\d+\.\d+)',
                'firmware': r'firmware.*?version.*?([0-9\.]+)',
                'uptime': r'uptime.*?(\d+.*?days?\s*\d+.*?hours?)',
                'ssid': r'ssid.*?([a-zA-Z0-9_-]+)'
            }
            
            for field, pattern in patterns.items():
                match = re.search(pattern, text)
                if match:
                    setattr(info, field, match.group(1))
                    
        except Exception as e:
            print(f"Error parsing status page: {e}")

    def scan_connected_devices(self) -> List[Device]:
        """Scan for connected devices using multiple methods"""
        devices = []
        
        # Method 1: Router's device list
        router_devices = self.get_router_device_list()
        devices.extend(router_devices)
        
        # Method 2: ARP table scanning
        arp_devices = self.scan_arp_table()
        devices.extend(arp_devices)
        
        # Method 3: Network ping sweep
        ping_devices = self.ping_sweep()
        devices.extend(ping_devices)
        
        # Merge and deduplicate devices
        return self.merge_devices(devices)

    def get_router_device_list(self) -> List[Device]:
        """Get device list from router's web interface"""
        devices = []
        
        try:
            # Common device list URLs
            device_urls = [
                "/device_list.html", "/devices.html", "/clients.html",
                "/userRpm/AssignedIpAddrListRpm.htm",
                "/cgi-bin/luci/admin/status/overview"
            ]
            
            for url in device_urls:
                try:
                    response = self.session.get(f"http://{self.router_ip}{url}")
                    if response.status_code == 200:
                        devices.extend(self.parse_device_list(response.text))
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"Error getting router device list: {e}")
            
        return devices

    def parse_device_list(self, html_content: str) -> List[Device]:
        """Parse device list from HTML"""
        devices = []
        
        try:
            # Look for MAC addresses in the content
            mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            
            macs = re.findall(mac_pattern, html_content)
            ips = re.findall(ip_pattern, html_content)
            
            # Simple pairing (this could be improved with more sophisticated parsing)
            for i, mac_match in enumerate(macs):
                mac = ''.join(mac_match).upper()
                mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)])
                
                ip = ips[i] if i < len(ips) else "Unknown"
                
                device = Device(
                    mac=mac,
                    ip=ip,
                    first_seen=datetime.now(),
                    last_seen=datetime.now()
                )
                
                devices.append(device)
                
        except Exception as e:
            print(f"Error parsing device list: {e}")
            
        return devices

    def scan_arp_table(self) -> List[Device]:
        """Scan ARP table for connected devices"""
        devices = []
        
        try:
            if platform.system().lower() == "windows":
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            else:
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    # Parse ARP table entries
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+).*?([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', line)
                    if match:
                        ip = match.group(1)
                        mac = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', line).group(0).upper()
                        
                        device = Device(
                            mac=mac,
                            ip=ip,
                            first_seen=datetime.now(),
                            last_seen=datetime.now()
                        )
                        devices.append(device)
                        
        except Exception as e:
            print(f"Error scanning ARP table: {e}")
            
        return devices

    def ping_sweep(self) -> List[Device]:
        """Perform ping sweep to discover active devices"""
        devices = []
        
        try:
            # Get network range
            network = ipaddress.IPv4Network(f"{self.router_ip}/24", strict=False)
            
            # Ping each IP in the network (limited to avoid overwhelming)
            for ip in list(network.hosts())[:50]:  # Limit to first 50 IPs
                try:
                    if platform.system().lower() == "windows":
                        result = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)], 
                                              capture_output=True, text=True)
                    else:
                        result = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], 
                                              capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        # Try to get hostname
                        try:
                            hostname = socket.gethostbyaddr(str(ip))[0]
                        except:
                            hostname = "Unknown"
                        
                        device = Device(
                            mac="Unknown",
                            ip=str(ip),
                            hostname=hostname,
                            first_seen=datetime.now(),
                            last_seen=datetime.now()
                        )
                        devices.append(device)
                        
                except:
                    continue
                    
        except Exception as e:
            print(f"Error in ping sweep: {e}")
            
        return devices

    def merge_devices(self, device_list: List[Device]) -> List[Device]:
        """Merge device information from multiple sources"""
        device_map = {}
        
        for device in device_list:
            key = device.mac if device.mac != "Unknown" else device.ip
            
            if key in device_map:
                # Merge information
                existing = device_map[key]
                if device.hostname != "Unknown" and existing.hostname == "Unknown":
                    existing.hostname = device.hostname
                if device.mac != "Unknown" and existing.mac == "Unknown":
                    existing.mac = device.mac
                if device.ip != "Unknown" and existing.ip == "Unknown":
                    existing.ip = device.ip
            else:
                device_map[key] = device
        
        # Check authorization status
        for device in device_map.values():
            device.is_authorized = device.mac.upper() in self.authorized_macs
            
        return list(device_map.values())

    def get_device_vendor(self, mac: str) -> str:
        """Get device vendor from MAC address (OUI lookup)"""
        try:
            # This would require an OUI database - simplified version
            oui = mac[:8].replace(':', '').upper()
            
            # Common OUI prefixes (can be expanded)
            vendors = {
                '001122': 'Generic Device',
                '00E04C': 'Realtek',
                '001B63': 'Apple',
                '00259D': 'Microsoft',
                # Add more as needed
            }
            
            return vendors.get(oui, "Unknown")
        except:
            return "Unknown"

    def monitor_traffic(self, duration: int = 60) -> Dict[str, Dict]:
        """Monitor network traffic for specified duration"""
        print(f"Monitoring traffic for {duration} seconds...")
        
        traffic_data = defaultdict(lambda: {'bytes_sent': 0, 'bytes_received': 0, 'connections': 0})
        
        # This is a simplified traffic monitoring
        # In practice, you'd need SNMP or router API access for detailed traffic data
        
        start_time = time.time()
        while time.time() - start_time < duration:
            devices = self.scan_connected_devices()
            for device in devices:
                traffic_data[device.ip]['connections'] += 1
            
            time.sleep(5)
        
        return dict(traffic_data)

    def detect_suspicious_activity(self, devices: List[Device]) -> List[str]:
        """Detect potentially suspicious network activity"""
        alerts = []
        
        # Check for unauthorized devices
        unauthorized_devices = [d for d in devices if not d.is_authorized and d.mac != "Unknown"]
        if unauthorized_devices:
            alerts.append(f"Found {len(unauthorized_devices)} unauthorized device(s)")
            for device in unauthorized_devices:
                alerts.append(f"  - Unauthorized: {device.mac} ({device.ip}) - {device.hostname}")
        
        # Check for unusual device names
        suspicious_names = ['android', 'iphone', 'laptop', 'unknown', 'generic']
        for device in devices:
            if any(sus in device.hostname.lower() for sus in suspicious_names):
                if not device.is_authorized:
                    alerts.append(f"Suspicious device name: {device.hostname} ({device.ip})")
        
        # Check for multiple devices from same vendor (potential cloning)
        vendor_counts = defaultdict(int)
        for device in devices:
            vendor = self.get_device_vendor(device.mac)
            if vendor != "Unknown":
                vendor_counts[vendor] += 1
        
        for vendor, count in vendor_counts.items():
            if count > 3:  # Arbitrary threshold
                alerts.append(f"Multiple devices from {vendor}: {count} devices")
        
        return alerts

    def generate_report(self, router_info: RouterInfo, devices: List[Device], 
                       traffic_data: Dict, alerts: List[str]) -> str:
        """Generate comprehensive audit report"""
        report = []
        report.append("=" * 60)
        report.append("NETWORK AUDIT REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Router Information
        report.append("ROUTER INFORMATION")
        report.append("-" * 30)
        report.append(f"Manufacturer: {router_info.manufacturer}")
        report.append(f"Model: {router_info.model}")
        report.append(f"Firmware: {router_info.firmware}")
        report.append(f"WAN IP: {router_info.wan_ip}")
        report.append(f"LAN IP: {router_info.lan_ip}")
        report.append(f"Uptime: {router_info.uptime}")
        report.append("")
        
        # Connected Devices
        report.append("CONNECTED DEVICES")
        report.append("-" * 30)
        report.append(f"Total devices found: {len(devices)}")
        report.append(f"Authorized devices: {len([d for d in devices if d.is_authorized])}")
        report.append(f"Unauthorized devices: {len([d for d in devices if not d.is_authorized and d.mac != 'Unknown'])}")
        report.append("")
        
        for device in sorted(devices, key=lambda x: x.ip):
            status = "✓ AUTHORIZED" if device.is_authorized else "⚠ UNAUTHORIZED"
            report.append(f"Device: {device.hostname}")
            report.append(f"  IP: {device.ip}")
            report.append(f"  MAC: {device.mac}")
            report.append(f"  Status: {status}")
            report.append(f"  Vendor: {self.get_device_vendor(device.mac)}")
            report.append("")
        
        # Security Alerts
        if alerts:
            report.append("SECURITY ALERTS")
            report.append("-" * 30)
            for alert in alerts:
                report.append(f"⚠ {alert}")
            report.append("")
        
        # Traffic Summary
        report.append("TRAFFIC SUMMARY")
        report.append("-" * 30)
        for ip, data in traffic_data.items():
            report.append(f"Device {ip}: {data['connections']} connection checks")
        report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 30)
        report.append("• Review unauthorized devices and remove if necessary")
        report.append("• Update router firmware if outdated")
        report.append("• Change default admin credentials")
        report.append("• Enable WPA3 security if available")
        report.append("• Regularly monitor connected devices")
        report.append("• Consider MAC address filtering for sensitive networks")
        
        return "\n".join(report)

    def run_audit(self, monitor_duration: int = 60) -> str:
        """Run complete network audit"""
        print("Starting network audit...")
        print(f"Target router: {self.router_ip}")
        print("=" * 50)
        
        # Authenticate
        if not self.authenticate():
            return "Failed to authenticate with router"
        
        # Get router information
        print("Gathering router information...")
        router_info = self.get_router_info()
        
        # Scan devices
        print("Scanning for connected devices...")
        devices = self.scan_connected_devices()
        print(f"Found {len(devices)} devices")
        
        # Monitor traffic
        print("Monitoring network traffic...")
        traffic_data = self.monitor_traffic(monitor_duration)
        
        # Detect suspicious activity
        print("Analyzing for suspicious activity...")
        alerts = self.detect_suspicious_activity(devices)
        
        # Generate report
        print("Generating report...")
        report = self.generate_report(router_info, devices, traffic_data, alerts)
        
        return report

def main():
    parser = argparse.ArgumentParser(description="Wi-Fi Router Network Audit Tool")
    parser.add_argument("--router-ip", default="192.168.1.1", help="Router IP address")
    parser.add_argument("--username", default="admin", help="Router admin username")
    parser.add_argument("--password", default="admin", help="Router admin password")
    parser.add_argument("--monitor-time", type=int, default=60, help="Traffic monitoring duration (seconds)")
    parser.add_argument("--output", help="Output file for report")
    
    args = parser.parse_args()
    
    # Create auditor
    auditor = RouterAuditor(
        router_ip=args.router_ip,
        username=args.username,
        password=args.password
    )
    
    # Run audit
    try:
        report = auditor.run_audit(args.monitor_time)
        
        # Output report
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
            
    except KeyboardInterrupt:
        print("\nAudit interrupted by user")
    except Exception as e:
        print(f"Error during audit: {e}")

if __name__ == "__main__":
    main()