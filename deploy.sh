#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to validate IP address
validate_ip() {
    local ip=$1
    local stat=1

    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && \
           ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}

# Function to validate domain
validate_domain() {
    local domain=$1
    local stat=1

    if [[ $domain =~ ^([a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.)+[a-zA-Z]{2,}$ ]]; then
        stat=0
    fi
    return $stat
}

# Function to validate port
validate_port() {
    local port=$1
    local stat=1

    if [[ $port =~ ^[0-9]+$ ]] && [ "$port" -ge 1 ] && [ "$port" -le 65535 ]; then
        stat=0
    fi
    return $stat
}

# Function to install packages
install_packages() {
    echo -e "${YELLOW}📦 Updating package lists...${NC}"
    sudo apt update > /dev/null 2>&1

    echo -e "${YELLOW}🛠 Installing required packages...${NC}"
    sudo apt install -y nginx python3-pip python3-venv certbot python3-certbot-nginx ufw curl git > /dev/null 2>&1

    # Install Node.js LTS
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}⬇️ Installing Node.js...${NC}"
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - > /dev/null 2>&1
        sudo apt install -y nodejs > /dev/null 2>&1
    fi

    # Install PM2 globally if not installed
    if ! command -v pm2 &> /dev/null; then
        echo -e "${YELLOW}⬇️ Installing PM2...${NC}"
        sudo npm install -g pm2 > /dev/null 2>&1
    fi

    # Install Gunicorn if not installed
    if ! python3 -m pip show gunicorn &> /dev/null; then
        echo -e "${YELLOW}⬇️ Installing Gunicorn...${NC}"
        sudo python3 -m pip install gunicorn > /dev/null 2>&1
    fi
}

# Function to setup firewall
setup_firewall() {
    echo -e "${YELLOW}🔐 Configuring firewall...${NC}"
    sudo ufw allow OpenSSH > /dev/null 2>&1
    sudo ufw allow 'Nginx Full' > /dev/null 2>&1
    sudo ufw --force enable > /dev/null 2>&1
}

# Function to create Nginx config
create_nginx_config() {
    local domain=$1
    local port=$2
    local config_name=$3
    local is_django=$4

    echo -e "${YELLOW}📝 Creating Nginx config for ${domain}...${NC}"
    
    if [ "$is_django" = true ]; then
        sudo tee /etc/nginx/sites-available/${config_name}.conf > /dev/null <<EOF
server {
    listen 80;
    server_name ${domain};

    location / {
        proxy_pass http://127.0.0.1:${port};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias /home/${USER}/${config_name}/static/;
    }

    location /media/ {
        alias /home/${USER}/${config_name}/media/;
    }
}
EOF
    else
        sudo tee /etc/nginx/sites-available/${config_name}.conf > /dev/null <<EOF
server {
    listen 80;
    server_name ${domain};

    location / {
        proxy_pass http://127.0.0.1:${port};
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Enable compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_min_length 256;
}
EOF
    fi

    # Enable the config
    sudo ln -sf /etc/nginx/sites-available/${config_name}.conf /etc/nginx/sites-enabled/
}

# Function to setup SSL
setup_ssl() {
    local domains=$1

    echo -e "${YELLOW}🔐 Setting up SSL certificates...${NC}"
    sudo certbot --nginx -d ${domains} --non-interactive --agree-tos --redirect --hsts --staple-ocsp --email admin@${ROOT_DOMAIN} > /dev/null 2>&1
}

# Function to create Gunicorn service
create_gunicorn_service() {
    echo -e "${YELLOW}🛠 Creating Gunicorn service...${NC}"
    
    sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=gunicorn daemon for Django
After=network.target

[Service]
User=${USER}
Group=www-data
WorkingDirectory=/home/${USER}/${DJANGO_APP_NAME}
ExecStart=/home/${USER}/${DJANGO_APP_NAME}/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:${DJANGO_PORT} ${DJANGO_APP_NAME}.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn > /dev/null 2>&1
    sudo systemctl start gunicorn
}

# Function to setup PM2
setup_pm2() {
    local app_name=$1
    local port=$2
    local dir_name=$3

    echo -e "${YELLOW}🚀 Setting up PM2 for ${app_name}...${NC}"
    pm2 start "npm run start" --name "${app_name}" --cwd "/home/${USER}/${dir_name}" -- --port ${port} > /dev/null 2>&1
    pm2 save > /dev/null 2>&1
}

# Function to print deployment report
print_report() {
    clear
    echo -e "${GREEN}✅ Deployment Complete!${NC}"
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${YELLOW}🔹 Django Backend (Gunicorn)${NC}"
    echo -e "    Domain : https://${DJANGO_SUBDOMAIN}"
    echo -e "    Port   : ${DJANGO_PORT}"
    echo -e "    Status : $(sudo systemctl is-active gunicorn)"
    echo ""
    echo -e "${YELLOW}🔹 Next.js Admin Panel (PM2)${NC}"
    echo -e "    Domain : https://${ADMIN_SUBDOMAIN}"
    echo -e "    Port   : ${ADMIN_PORT}"
    echo -e "    Status : $(pm2 jlist | jq -r '.[] | select(.name=="admin-panel") | .pm2_env.status')"
    echo ""
    echo -e "${YELLOW}🔹 Next.js Website (PM2)${NC}"
    echo -e "    Domain : https://${WEBSITE_DOMAIN}"
    echo -e "    Port   : ${WEBSITE_PORT}"
    echo -e "    Status : $(pm2 jlist | jq -r '.[] | select(.name=="website") | .pm2_env.status')"
    echo ""
    echo -e "${YELLOW}🔒 SSL Status${NC}"
    echo -e "    HTTPS  : Enabled via Let's Encrypt"
    echo -e "    Renew  : Automatic (certbot.timer)"
    echo ""
    echo -e "${YELLOW}🧱 Firewall Status${NC}"
    echo -e "    UFW    : $(sudo ufw status | grep -i active)"
    echo -e "    Ports  : 22, 80, 443 open"
    echo ""
    echo -e "${YELLOW}📂 Configuration Paths${NC}"
    echo -e "    Nginx  : /etc/nginx/sites-available/"
    echo -e "    Django : /home/${USER}/${DJANGO_APP_NAME}"
    echo -e "    Admin  : /home/${USER}/${ADMIN_APP_NAME}"
    echo -e "    Website: /home/${USER}/${WEBSITE_APP_NAME}"
    echo ""
    echo -e "${YELLOW}📝 Log Locations${NC}"
    echo -e "    Nginx  : /var/log/nginx/access.log"
    echo -e "    Nginx  : /var/log/nginx/error.log"
    echo -e "    Gunicorn: journalctl -u gunicorn -n 50"
    echo -e "    PM2    : pm2 logs"
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${GREEN}📘 Deployment Summary${NC}"
    echo -e "All services have been configured and should be running."
    echo -e "Check the status of each service with:"
    echo -e "  - Django: ${BLUE}sudo systemctl status gunicorn${NC}"
    echo -e "  - PM2 Apps: ${BLUE}pm2 list${NC}"
    echo -e "  - Nginx: ${BLUE}sudo systemctl status nginx${NC}"
    echo -e ""
    echo -e "${RED}⚠️ Important:${NC}"
    echo -e "1. Ensure your DNS records point to your server IP:"
    echo -e "   - ${DJANGO_SUBDOMAIN} → ${SERVER_IP}"
    echo -e "   - ${ADMIN_SUBDOMAIN} → ${SERVER_IP}"
    echo -e "   - ${WEBSITE_DOMAIN} → ${SERVER_IP}"
    echo -e "2. For Django: Set up your database and run migrations"
    echo -e "3. For Next.js: Build your production apps if needed"
    echo -e "${BLUE}==========================================${NC}"
}

# Main script execution
echo -e "${GREEN}🔧 Starting Full Deployment Script...${NC}"

# Step 1: Collect User Input
while true; do
    read -p "Enter your server's public IP: " SERVER_IP
    if validate_ip "$SERVER_IP"; then
        break
    else
        echo -e "${RED}❌ Invalid IP address. Please try again.${NC}"
    fi
done

while true; do
    read -p "Enter your root domain (e.g., example.com): " ROOT_DOMAIN
    if validate_domain "$ROOT_DOMAIN"; then
        break
    else
        echo -e "${RED}❌ Invalid domain format. Please try again.${NC}"
    fi
done

DJANGO_SUBDOMAIN="api.${ROOT_DOMAIN}"
ADMIN_SUBDOMAIN="admin.${ROOT_DOMAIN}"
WEBSITE_DOMAIN="www.${ROOT_DOMAIN}"

while true; do
    read -p "Enter Django runserver port (default: 8000): " DJANGO_PORT
    DJANGO_PORT=${DJANGO_PORT:-8000}
    if validate_port "$DJANGO_PORT"; then
        break
    else
        echo -e "${RED}❌ Invalid port number. Must be between 1-65535.${NC}"
    fi
done

while true; do
    read -p "Enter Next.js Admin Panel port (default: 3000): " ADMIN_PORT
    ADMIN_PORT=${ADMIN_PORT:-3000}
    if validate_port "$ADMIN_PORT"; then
        break
    else
        echo -e "${RED}❌ Invalid port number. Must be between 1-65535.${NC}"
    fi
done

while true; do
    read -p "Enter Next.js Website port (default: 3001): " WEBSITE_PORT
    WEBSITE_PORT=${WEBSITE_PORT:-3001}
    if validate_port "$WEBSITE_PORT"; then
        break
    else
        echo -e "${RED}❌ Invalid port number. Must be between 1-65535.${NC}"
    fi
done

# Set default app names
DJANGO_APP_NAME="backend"
ADMIN_APP_NAME="admin-frontend"
WEBSITE_APP_NAME="web-frontend"

# Step 2: DNS Verification
echo -e "${YELLOW}⚠️ DNS Verification Required${NC}"
echo -e "Before continuing, please ensure you have set up the following DNS records:"
echo -e "  - ${DJANGO_SUBDOMAIN} A record → ${SERVER_IP}"
echo -e "  - ${ADMIN_SUBDOMAIN} A record → ${SERVER_IP}"
echo -e "  - ${WEBSITE_DOMAIN} A record → ${SERVER_IP}"
read -p "Press [Enter] to continue once DNS records are configured..."

# Step 3: Install required packages
install_packages

# Step 4: Setup firewall
setup_firewall

# Step 5: Create Nginx configs
create_nginx_config "$DJANGO_SUBDOMAIN" "$DJANGO_PORT" "django" true
create_nginx_config "$ADMIN_SUBDOMAIN" "$ADMIN_PORT" "admin" false
create_nginx_config "$WEBSITE_DOMAIN" "$WEBSITE_PORT" "website" false

# Test Nginx configuration
echo -e "${YELLOW}🔍 Testing Nginx configuration...${NC}"
sudo nginx -t && sudo systemctl restart nginx

# Step 6: Setup SSL
setup_ssl "${DJANGO_SUBDOMAIN},${ADMIN_SUBDOMAIN},${WEBSITE_DOMAIN}"

# Step 7: Create Gunicorn service
create_gunicorn_service

# Step 8: Setup PM2 for Next.js apps
setup_pm2 "admin-panel" "$ADMIN_PORT" "$ADMIN_APP_NAME"
setup_pm2 "website" "$WEBSITE_PORT" "$WEBSITE_APP_NAME"

# Enable PM2 startup
echo -e "${YELLOW}⏳ Enabling PM2 startup...${NC}"
pm2 startup > /dev/null 2>&1
sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u $USER --hp /home/$USER > /dev/null 2>&1

# Step 9: Enable SSL auto-renewal
echo -e "${YELLOW}⏳ Enabling SSL auto-renewal...${NC}"
sudo systemctl enable certbot.timer > /dev/null 2>&1

# Step 10: Print deployment report
print_report
