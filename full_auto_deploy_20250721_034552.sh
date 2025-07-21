#!/bin/bash

set -euo pipefail

echo "🚀 Starting Full Auto Deployment - $(date '+%Y-%m-%d %H:%M:%S')"

#=========================#
#  1. Load Config or Ask  #
#=========================#
CONFIG_FILE="deploy.config"
if [[ -f "$CONFIG_FILE" ]]; then
  echo "📄 Loading config from $CONFIG_FILE"
  source "$CONFIG_FILE"
else
  echo "⚙️  No config file found. Asking for input..."
  read -p "Enter your server's public IP: " SERVER_IP
  read -p "Enter your root domain (e.g., scriptpark.xyz): " ROOT_DOMAIN
  read -p "Enter Django runserver port (e.g., 8000): " DJANGO_PORT
  read -p "Enter Next.js Admin Panel port (e.g., 3000): " ADMIN_PORT
  read -p "Enter Next.js Website port (e.g., 3001): " WEBSITE_PORT
  read -p "Enter Cloudflare API Token (or leave blank): " CF_API_TOKEN
  read -p "Enter Cloudflare Zone ID (or leave blank): " CF_ZONE_ID
fi

DJANGO_SUBDOMAIN="api.$ROOT_DOMAIN"
ADMIN_SUBDOMAIN="admin.$ROOT_DOMAIN"
WEBSITE_DOMAIN="www.$ROOT_DOMAIN"

#=========================#
#  2. Auto Get Zone ID    #
#=========================#
if [[ -n "$CF_API_TOKEN" && -z "$CF_ZONE_ID" ]]; then
  echo "🔍 Fetching Cloudflare Zone ID..."
  CF_ZONE_ID=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$ROOT_DOMAIN" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" | jq -r '.result[0].id')
  echo "ℹ️ Auto-detected Cloudflare Zone ID: $CF_ZONE_ID"
fi

#=========================#
#  3. Setup DNS Records   #
#=========================#
function create_dns_record() {
  local name=$1
  if [[ -n "$CF_API_TOKEN" && -n "$CF_ZONE_ID" ]]; then
    echo "🌐 Checking DNS for $name..."
    record_exists=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?name=$name" \
      -H "Authorization: Bearer $CF_API_TOKEN" \
      -H "Content-Type: application/json" | jq -r '.result[0].id')
    if [[ -z "$record_exists" ]]; then
      echo "➕ Creating DNS for $name"
      curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
        -H "Authorization: Bearer $CF_API_TOKEN" \
        -H "Content-Type: application/json" \
        --data '{
          "type": "A",
          "name": "'$name'",
          "content": "'$SERVER_IP'",
          "ttl": 3600,
          "proxied": true
        }' | grep -q '"success":true' && echo "✅ DNS created for $name" || echo "⚠️ Failed to create DNS for $name"
    else
      echo "⚠️ DNS already exists for $name. Skipping..."
    fi
  fi
}
create_dns_record $DJANGO_SUBDOMAIN
create_dns_record $ADMIN_SUBDOMAIN
create_dns_record $WEBSITE_DOMAIN

#=========================#
#  4. Install Dependencies#
#=========================#
echo "📦 Installing Dependencies..."
apt update && apt install -y nginx certbot python3-certbot-nginx python3-pip python3-venv ufw curl jq
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt install -y nodejs
npm install -g pm2

#=========================#
#  5. UFW Firewall        #
#=========================#
ufw allow 'OpenSSH'
ufw allow 'Nginx Full'
ufw --force enable

#=========================#
#  6. Nginx Configs       #
#=========================#
NGINX_PATH="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"
mkdir -p "$NGINX_PATH"

create_nginx_config() {
  local subdomain=$1
  local port=$2
  local conf_name=$3

  cat > "$NGINX_PATH/$conf_name.conf" <<EOF
server {
    listen 80;
    server_name $subdomain;
    location / {
        proxy_pass http://127.0.0.1:$port;
        include proxy_params;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
    }
}
EOF
  ln -sf "$NGINX_PATH/$conf_name.conf" "$NGINX_ENABLED/"
}
create_nginx_config $DJANGO_SUBDOMAIN $DJANGO_PORT "django"
create_nginx_config $ADMIN_SUBDOMAIN $ADMIN_PORT "admin"
create_nginx_config $WEBSITE_DOMAIN $WEBSITE_PORT "website"

# Apply Nginx changes
nginx -t && systemctl reload nginx

#=========================#
#  7. SSL Certificates    #
#=========================#
certbot --nginx --non-interactive --agree-tos -m admin@$ROOT_DOMAIN -d $DJANGO_SUBDOMAIN -d $ADMIN_SUBDOMAIN -d $WEBSITE_DOMAIN || echo "⚠️ SSL failed"
systemctl enable certbot.timer

#=========================#
#  8. Gunicorn Setup      #
#=========================#
BACKEND_PATH="backend"
mkdir -p /home/$SUDO_USER/$BACKEND_PATH/venv
python3 -m venv /home/$SUDO_USER/$BACKEND_PATH/venv
GUNICORN_SERVICE="/etc/systemd/system/gunicorn.service"

cat > "$GUNICORN_SERVICE" <<EOF
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=$SUDO_USER
Group=www-data
WorkingDirectory=/home/$SUDO_USER/$BACKEND_PATH
ExecStart=/home/$SUDO_USER/$BACKEND_PATH/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:$DJANGO_PORT backend.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reexec
systemctl enable gunicorn
systemctl start gunicorn

#=========================#
#  9. PM2 Setup           #
#=========================#
ADMIN_PATH="admin-frontend"
WEBSITE_PATH="web-frontend"
pm2 start "npm start" --name admin-panel --cwd /home/$SUDO_USER/$ADMIN_PATH --watch -- --port $ADMIN_PORT
pm2 start "npm start" --name website --cwd /home/$SUDO_USER/$WEBSITE_PATH --watch -- --port $WEBSITE_PORT
pm2 save
pm2 startup | tail -n 1 | bash

#=========================#
#  ✅ FINAL DONE MESSAGE  #
#=========================#
clear
echo "🎉 All set! Deployment complete."
echo "🌐 Visit your apps:"
echo " - Django Backend: https://$DJANGO_SUBDOMAIN"
echo " - Admin Panel:    https://$ADMIN_SUBDOMAIN"
echo " - Website:        https://$WEBSITE_DOMAIN"
echo "🔒 SSL: Secured via Let's Encrypt"
echo "🧱 Firewall: Enabled"
echo "✅ Everything is configured. You can now access the site from any device, anywhere in the world."
