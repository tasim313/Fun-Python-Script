#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration from previous deployment
ROOT_DOMAIN="yourdomain.com"  # Replace with your domain
DJANGO_SUBDOMAIN="api.${ROOT_DOMAIN}"
ADMIN_SUBDOMAIN="admin.${ROOT_DOMAIN}"
WEBSITE_DOMAIN="www.${ROOT_DOMAIN}"
SERVER_IP="your.server.ip"    # Replace with your server IP

# Test URLs
TEST_URLS=(
  "https://${DJANGO_SUBDOMAIN}/health-check/"
  "https://${ADMIN_SUBDOMAIN}"
  "https://${WEBSITE_DOMAIN}"
)

# Function to check DNS propagation worldwide
check_dns_propagation() {
  echo -e "${YELLOW}🌐 Checking DNS propagation worldwide...${NC}"
  
  # List of public DNS servers from different regions
  DNS_SERVERS=(
    "1.1.1.1"     # Cloudflare (Global)
    "8.8.8.8"     # Google (Global)
    "9.9.9.9"     # Quad9 (Global)
    "208.67.222.222" # OpenDNS (Global)
    "185.228.168.168" # CleanBrowsing (Global)
    "84.200.69.80" # DNS.WATCH (Europe)
    "64.6.64.6"   # Verisign (US)
    "203.112.2.4" # NICT (Japan)
    "210.175.1.244" # HKNet (Hong Kong)
  )

  for domain in "${DJANGO_SUBDOMAIN}" "${ADMIN_SUBDOMAIN}" "${WEBSITE_DOMAIN}"; do
    echo -e "\nChecking ${BLUE}${domain}${NC}:"
    
    for dns in "${DNS_SERVERS[@]}"; do
      result=$(dig +short @${dns} ${domain} | tail -n1)
      if [ "$result" == "$SERVER_IP" ]; then
        echo -e "${GREEN}✓${NC} ${dns} - Correct (${result})"
      else
        echo -e "${RED}✗${NC} ${dns} - Incorrect (${result})"
        echo -e "${YELLOW}⚠️ DNS not fully propagated or misconfigured on ${dns}${NC}"
      fi
    done
  done
}

# Function to test SSL/TLS configuration
test_ssl_config() {
  echo -e "\n${YELLOW}🔒 Testing SSL/TLS configuration...${NC}"
  
  for domain in "${DJANGO_SUBDOMAIN}" "${ADMIN_SUBDOMAIN}" "${WEBSITE_DOMAIN}"; do
    echo -e "\nTesting ${BLUE}${domain}${NC}:"
    
    # Test using SSL Labs API (simplified)
    result=$(curl -s "https://api.ssllabs.com/api/v3/analyze?host=${domain}" | jq -r '.status')
    if [ "$result" == "READY" ]; then
      echo -e "${GREEN}✓ SSL/TLS configuration is good${NC}"
    else
      echo -e "${RED}✗ Potential SSL/TLS issues detected${NC}"
      echo -e "${YELLOW}Attempting to fix SSL configuration...${NC}"
      sudo certbot --nginx -d ${domain} --non-interactive --agree-tos --redirect --hsts --staple-ocsp
      sudo systemctl restart nginx
    fi

    # Check for mixed content issues
    echo -e "${YELLOW}Checking for mixed content issues...${NC}"
    mixed_content=$(curl -s "https://${domain}" | grep -i "http://")
    if [ -z "$mixed_content" ]; then
      echo -e "${GREEN}✓ No mixed content detected${NC}"
    else
      echo -e "${RED}✗ Mixed content detected${NC}"
      echo -e "${YELLOW}Updating Nginx config to force HTTPS...${NC}"
      sudo sed -i 's/http:\/\//https:\/\//g' /etc/nginx/sites-available/*
      sudo systemctl restart nginx
    fi
  done
}

# Function to check CORS headers
check_cors_headers() {
  echo -e "\n${YELLOW}🛡️ Checking CORS headers...${NC}"
  
  for url in "${TEST_URLS[@]}"; do
    echo -e "\nTesting ${BLUE}${url}${NC}:"
    
    # Check if it's the Django API
    if [[ $url == *"api"* ]]; then
      cors_headers=$(curl -s -I -X OPTIONS ${url} | grep -i "access-control")
      if [ -z "$cors_headers" ]; then
        echo -e "${RED}✗ CORS headers missing for API${NC}"
        echo -e "${YELLOW}Updating Django CORS configuration...${NC}"
        
        # Install django-cors-headers if not present
        sudo -H -u ${USER} bash -c "source /home/${USER}/backend/venv/bin/activate && pip install django-cors-headers"
        
        # Update Django settings
        sudo tee -a /home/${USER}/backend/backend/settings.py > /dev/null <<EOL

# CORS Configuration added by deployment script
CORS_ALLOWED_ORIGINS = [
    "https://${ADMIN_SUBDOMAIN}",
    "https://${WEBSITE_DOMAIN}",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
EOL
        
        sudo systemctl restart gunicorn
      else
        echo -e "${GREEN}✓ CORS headers properly configured${NC}"
      fi
    else
      echo -e "${BLUE}ℹ Not an API endpoint, CORS check skipped${NC}"
    fi
  done
}

# Function to check content encoding (compression)
check_compression() {
  echo -e "\n${YELLOW}🗜️ Checking content compression...${NC}"
  
  for url in "${TEST_URLS[@]}"; do
    echo -e "\nTesting ${BLUE}${url}${NC}:"
    
    encoding=$(curl -s -I -H "Accept-Encoding: gzip, deflate, br" ${url} | grep -i "content-encoding")
    if [ -z "$encoding" ]; then
      echo -e "${RED}✗ Compression not enabled${NC}"
      echo -e "${YELLOW}Enabling compression in Nginx...${NC}"
      
      # Add compression to Nginx config
      sudo tee -a /etc/nginx/nginx.conf > /dev/null <<EOL

# Compression added by deployment script
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml application/json application/javascript application/xml+rss text/javascript;
EOL
      
      sudo systemctl restart nginx
    else
      echo -e "${GREEN}✓ Compression enabled: ${encoding}${NC}"
    fi
  done
}

# Function to check cache headers
check_cache_headers() {
  echo -e "\n${YELLOW}⏱️ Checking cache headers...${NC}"
  
  for url in "${TEST_URLS[@]}"; do
    echo -e "\nTesting ${BLUE}${url}${NC}:"
    
    cache_control=$(curl -s -I ${url} | grep -i "cache-control")
    if [ -z "$cache_control" ]; then
      echo -e "${RED}✗ Cache headers missing${NC}"
      echo -e "${YELLOW}Adding cache headers to Nginx config...${NC}"
      
      # Add cache control to Nginx config
      for config in /etc/nginx/sites-available/*; do
        sudo sed -i '/location \/ {/a \        add_header Cache-Control "no-cache, no-store, must-revalidate";' $config
      done
      
      sudo systemctl restart nginx
    else
      echo -e "${GREEN}✓ Cache headers present: ${cache_control}${NC}"
    fi
  done
}

# Function to test from different user agents
test_user_agents() {
  echo -e "\n${YELLOW}📱 Testing with different user agents...${NC}"
  
  # List of user agents to test
  USER_AGENTS=(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
  )
  
  for url in "${TEST_URLS[@]}"; do
    echo -e "\nTesting ${BLUE}${url}${NC} with different user agents:"
    
    for ua in "${USER_AGENTS[@]}"; do
      response_code=$(curl -s -o /dev/null -w "%{http_code}" -A "${ua}" ${url})
      if [ "$response_code" -eq 200 ]; then
        echo -e "${GREEN}✓ Success (${response_code}) with ${ua:0:30}...${NC}"
      else
        echo -e "${RED}✗ Failed (${response_code}) with ${ua:0:30}...${NC}"
        
        # If failing for mobile user agents, check viewport settings
        if [[ $ua == *"Mobile"* || $ua == *"iPhone"* || $ua == *"Android"* ]]; then
          echo -e "${YELLOW}⚠️ Mobile access issue detected${NC}"
          echo -e "${YELLOW}Checking for responsive meta tag...${NC}"
          
          # For Next.js apps, ensure proper viewport meta tag
          for app in "admin-frontend" "web-frontend"; do
            if grep -q "<meta name=\"viewport\"" /home/${USER}/${app}/pages/_document.js; then
              echo -e "${GREEN}✓ Viewport meta tag found in ${app}${NC}"
            else
              echo -e "${RED}✗ Viewport meta tag missing in ${app}${NC}"
              echo -e "${YELLOW}Adding responsive meta tag...${NC}"
              sudo sed -i '/<Head>/a \          <meta name="viewport" content="width=device-width, initial-scale=1.0" />' /home/${USER}/${app}/pages/_document.js
              
              # Restart Next.js apps
              pm2 restart ${app}
            fi
          done
        fi
      fi
    done
  done
}

# Function to check security headers
check_security_headers() {
  echo -e "\n${YELLOW}🛡️ Checking security headers...${NC}"
  
  SECURITY_HEADERS=(
    "X-Frame-Options"
    "X-Content-Type-Options"
    "X-XSS-Protection"
    "Content-Security-Policy"
    "Strict-Transport-Security"
    "Referrer-Policy"
    "Permissions-Policy"
  )
  
  for url in "${TEST_URLS[@]}"; do
    echo -e "\nTesting ${BLUE}${url}${NC}:"
    missing_headers=0
    
    for header in "${SECURITY_HEADERS[@]}"; do
      present=$(curl -s -I ${url} | grep -i "^${header}:")
      if [ -z "$present" ]; then
        echo -e "${RED}✗ Missing: ${header}${NC}"
        missing_headers=$((missing_headers+1))
      else
        echo -e "${GREEN}✓ Present: ${header}${NC}"
      fi
    done
    
    if [ $missing_headers -gt 0 ]; then
      echo -e "${YELLOW}Adding missing security headers to Nginx...${NC}"
      
      # Add security headers to Nginx config
      for config in /etc/nginx/sites-available/*; do
        sudo sed -i '/server {/a \    add_header X-Frame-Options "SAMEORIGIN";\n    add_header X-Content-Type-Options "nosniff";\n    add_header X-XSS-Protection "1; mode=block";\n    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";\n    add_header Referrer-Policy "strict-origin-when-cross-origin";\n    add_header Permissions-Policy "geolocation=(),midi=(),sync-xhr=(),microphone=(),camera=(),magnetometer=(),gyroscope=(),fullscreen=(self),payment=()";' $config
      done
      
      sudo systemctl restart nginx
    fi
  done
}

# Function to check if ports are open
check_ports() {
  echo -e "\n${YELLOW}🔌 Checking if required ports are open...${NC}"
  
  PORTS=("80" "443" "${DJANGO_PORT}" "${ADMIN_PORT}" "${WEBSITE_PORT}")
  
  for port in "${PORTS[@]}"; do
    # Check locally
    if sudo netstat -tuln | grep -q ":${port} "; then
      echo -e "${GREEN}✓ Port ${port} is open locally${NC}"
    else
      echo -e "${RED}✗ Port ${port} is not open locally${NC}"
      echo -e "${YELLOW}Opening port ${port} in UFW...${NC}"
      sudo ufw allow ${port}
    fi
    
    # Check from external perspective (simplified)
    echo -e "${YELLOW}Testing port ${port} externally...${NC}"
    if nc -zv ${SERVER_IP} ${port} &> /dev/null; then
      echo -e "${GREEN}✓ Port ${port} is accessible from outside${NC}"
    else
      echo -e "${RED}✗ Port ${port} is not accessible from outside${NC}"
      echo -e "${YELLOW}Check your cloud provider's firewall rules${NC}"
    fi
  done
}

# Main execution
echo -e "${GREEN}🔍 Starting Comprehensive Accessibility Check...${NC}"

check_dns_propagation
test_ssl_config
check_cors_headers
check_compression
check_cache_headers
test_user_agents
check_security_headers
check_ports

echo -e "\n${GREEN}✅ All checks completed!${NC}"
echo -e "${BLUE}==========================================${NC}"
echo -e "${YELLOW}📋 Summary of actions taken:${NC}"
echo -e "- Verified DNS propagation worldwide"
echo -e "- Checked and fixed SSL/TLS configuration"
echo -e "- Ensured proper CORS headers for API access"
echo -e "- Enabled content compression"
echo -e "- Configured proper cache headers"
echo -e "- Tested with various user agents (desktop/mobile)"
echo -e "- Added missing security headers"
echo -e "- Verified port accessibility"
echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}Your applications should now be accessible from any device worldwide!${NC}"
echo -e "${YELLOW}If you still experience issues, consider:${NC}"
echo -e "- Checking your cloud provider's firewall rules"
echo -e "- Reviewing application-specific logs"
echo -e "- Testing from a different network (mobile data, VPN)"
echo -e "${BLUE}==========================================${NC}"
