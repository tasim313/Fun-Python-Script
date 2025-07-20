#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}"
echo "=============================================="
echo "          SERVER STATUS CHECK REPORT          "
echo "=============================================="
echo -e "${NC}"
echo "Generated on: $(date)"
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Network Information
echo -e "${YELLOW}=== NETWORK INFORMATION ===${NC}"
echo -e "${BLUE}Public IP:${NC} $(curl -s ifconfig.me)"
echo -e "${BLUE}Private IP(s):${NC} $(hostname -I)"
echo ""

# Internet Connection Check
echo -e "${BLUE}Internet Connection:${NC}"
if ping -c 1 8.8.8.8 &> /dev/null; then
    echo -e "${GREEN}Internet connection is working${NC}"
else
    echo -e "${RED}No internet connection${NC}"
fi
echo ""

# 2. Port Status
echo -e "${YELLOW}=== PORT STATUS ===${NC}"
declare -a common_ports=("22" "80" "443" "3000" "3001" "3306" "5432" "8000" "5473")
echo "Checking common ports (${common_ports[*]})..."

for port in "${common_ports[@]}"; do
    if ss -tulnp | grep ":$port " > /dev/null; then
        service_name=$(ss -tulnp | grep ":$port " | awk '{print $7}')
        echo -e "${GREEN}Port $port is OPEN${NC} - Service: $service_name"
    else
        echo -e "${RED}Port $port is CLOSED${NC}"
    fi
done
echo ""

# List all open ports
echo -e "${BLUE}All Open Ports:${NC}"
ss -tulnp | awk '{print $1,$5,$7}' | column -t
echo ""

# 3. Service Status
echo -e "${YELLOW}=== SERVICE STATUS ===${NC}"

# Database Services
check_service() {
    if systemctl is-active --quiet "$1"; then
        echo -e "${GREEN}$1 is RUNNING${NC}"
    else
        echo -e "${RED}$1 is NOT RUNNING${NC}"
    fi
}

echo -e "${BLUE}Database Services:${NC}"
check_service "mysql"
check_service "postgresql"
check_service "mongod"
check_service "redis-server"
echo ""

# Web Servers
echo -e "${BLUE}Web Servers:${NC}"
check_service "nginx"
check_service "apache2"
check_service "httpd"
echo ""

# Other Services
echo -e "${BLUE}Other Services:${NC}"
check_service "ssh"
check_service "docker"
check_service "ufw"
echo ""

# 4. Application Status
echo -e "${YELLOW}=== APPLICATION STATUS ===${NC}"

# Node.js
if command_exists node; then
    echo -e "${GREEN}Node.js is INSTALLED${NC} - Version: $(node -v)"
else
    echo -e "${RED}Node.js is NOT INSTALLED${NC}"
fi

# Python
if command_exists python3; then
    echo -e "${GREEN}Python is INSTALLED${NC} - Version: $(python3 --version 2>&1)"
else
    echo -e "${RED}Python is NOT INSTALLED${NC}"
fi

# Other runtime checks
echo ""
echo -e "${BLUE}Running Node.js Applications:${NC}"
pgrep -lfa node | grep -v "grep"
echo ""

echo -e "${BLUE}Running Python Applications:${NC}"
pgrep -lfa python | grep -v "grep"
echo ""

# 5. Disk Information
echo -e "${YELLOW}=== DISK INFORMATION ===${NC}"
echo -e "${BLUE}Disk Partitions:${NC}"
lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,UUID
echo ""

echo -e "${BLUE}Disk Usage:${NC}"
df -h
echo ""

echo -e "${BLUE}SSD Information:${NC}"
if command_exists lsblk; then
    lsblk -d -o name,rota | grep -v '1' | awk '$2=="0"{print $1" is likely an SSD"}'
fi
echo ""

# 6. System Resources
echo -e "${YELLOW}=== SYSTEM RESOURCES ===${NC}"
echo -e "${BLUE}Memory Usage:${NC}"
free -h
echo ""

echo -e "${BLUE}CPU Information:${NC}"
lscpu | grep -E 'Model name|Socket|Core|Thread|CPU MHz'
echo ""

echo -e "${BLUE}Top Processes:${NC}"
top -b -n 1 | head -n 12
echo ""

# 7. Security Checks
echo -e "${YELLOW}=== SECURITY CHECKS ===${NC}"
echo -e "${BLUE}Failed SSH Logins:${NC}"
journalctl _SYSTEMD_UNIT=ssh.service | grep "Failed password" | tail -n 5
echo ""

echo -e "${BLUE}Active Users:${NC}"
who
echo ""

echo -e "${BLUE}Sudoers:${NC}"
getent group sudo | cut -d: -f4
echo ""

# 8. Port Forwarding Check
echo -e "${YELLOW}=== PORT FORWARDING CHECK ===${NC}"
if command_exists iptables; then
    echo -e "${BLUE}IPTables Port Forwarding Rules:${NC}"
    iptables -t nat -L PREROUTING -n -v
else
    echo "IPTables not available to check port forwarding"
fi
echo ""

# 9. Installed Software
echo -e "${YELLOW}=== INSTALLED SOFTWARE ===${NC}"
echo -e "${BLUE}Important Installed Packages:${NC}"
dpkg -l | grep -E 'nginx|apache|mysql|postgresql|node|python|docker|redis|mongodb'
echo ""

# Footer
echo -e "${BLUE}"
echo "=============================================="
echo "          END OF SERVER STATUS REPORT         "
echo "=============================================="
echo -e "${NC}"
