#!/bin/bash

set -e

echo "🚀 Starting Production Deployment - $(date '+%Y-%m-%d')"

#=========================#
#  1. Get User Input      #
#=========================#
read -p "Enter your server's public IP: " SERVER_IP
read -p "Enter your root domain (e.g., scriptpark.xyz): " ROOT_DOMAIN
read -p "Enter Django runserver port (e.g., 8000): " DJANGO_PORT
read -p "Enter Next.js Admin Panel port (e.g., 3000): " ADMIN_PORT
read -p "Enter Next.js Website port (e.g., 3001): " WEBSITE_PORT

DJANGO_SUBDOMAIN="api.$ROOT_DOMAIN"
ADMIN_SUBDOMAIN="admin.$ROOT_DOMAIN"
WEBSITE_DOMAIN="www.$ROOT_DOMAIN"

# Optional Cloudflare automation
read -p "Enter your Cloudflare API Token (or leave blank): " CF_API_TOKEN
read -p "Enter your Cloudflare Zone ID (or leave blank): " CF_ZONE_ID

#=========================#
#  2. Setup DNS Records   #
#=========================#
function create_dns_record() {
  local name=$1
  if [[ -n "$CF_API_TOKEN" && -n "$CF_ZONE_ID" ]]; then
    echo "🌐 Creating Cloudflare DNS record for $name..."
    curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
      -H "Authorization: Bearer $CF_API_TOKEN" \
      -H "Content-Type: application/json" \
      --data '{
        "type": "A",
        "name": "'$name'",
        "content": "'$SERVER_IP'",
        "ttl": 3600,
        "proxied": true
      }' | grep -q '"success":true' || echo "⚠️ Failed to create DNS record for $name"
  fi
}
create_dns_record $DJANGO_SUBDOMAIN
create_dns_record $ADMIN_SUBDOMAIN
create_dns_record $WEBSITE_DOMAIN

#=============================#
#  3. Install Requirements    #
#=============================#
echo "📦 Installing Required Packages..."
apt update && apt install -y nginx certbot python3-certbot-nginx python3-pip python3-venv ufw curl

# Node.js + PM2
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt install -y nodejs
npm install -g pm2

#=============================#
#  4. Firewall Rules          #
#=============================#
ufw allow 'OpenSSH'
ufw allow 'Nginx Full'
ufw --force enable

#=============================#
#  5. Nginx Configs           #
#=============================#
NGINX_PATH="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

mkdir -p "$NGINX_PATH"

create_nginx_config() {
  local subdomain=$1
  local port=$2
  local conf_name=$3

  local file="$NGINX_PATH/$conf_name.conf"
  if [[ -f "$file" ]]; then
    echo "✅ $conf_name.conf already exists. Skipping."
    return
  fi

  cat > "$file" <<EOF
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

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";

    limit_req zone=one burst=10 nodelay;
}
EOF

  ln -sf "$file" "$NGINX_ENABLED/"
}

# Add rate limiting
if ! grep -q 'limit_req_zone' /etc/nginx/nginx.conf; then
  sed -i '/http {/a \\tlimit_req_zone \$binary_remote_addr zone=one:10m rate=5r/s;' /etc/nginx/nginx.conf
fi

create_nginx_config $DJANGO_SUBDOMAIN $DJANGO_PORT "django"
create_nginx_config $ADMIN_SUBDOMAIN $ADMIN_PORT "admin"
create_nginx_config $WEBSITE_DOMAIN $WEBSITE_PORT "website"

nginx -t && systemctl reload nginx

#=============================#
#  6. SSL Configuration      #
#=============================#
certbot_installed=$(which certbot)
if [[ -n "$certbot_installed" ]]; then
  certbot --nginx --non-interactive --agree-tos -m admin@$ROOT_DOMAIN -d $DJANGO_SUBDOMAIN -d $ADMIN_SUBDOMAIN -d $WEBSITE_DOMAIN || echo "⚠️ SSL issue. Check DNS setup."
  systemctl enable certbot.timer
fi

#=============================#
#  7. Gunicorn Systemd       #
#=============================#
GUNICORN_SERVICE="/etc/systemd/system/gunicorn.service"
if [[ ! -f "$GUNICORN_SERVICE" ]]; then
  echo "🛠 Creating Gunicorn service..."
  cat > "$GUNICORN_SERVICE" <<EOF
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=$SUDO_USER
Group=www-data
WorkingDirectory=/home/$SUDO_USER/backend
ExecStart=/home/$SUDO_USER/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:$DJANGO_PORT backend.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reexec
  systemctl enable gunicorn
  systemctl start gunicorn
else
  echo "✅ Gunicorn service already exists."
fi

#=============================#
#  8. PM2 Setup              #
#=============================#
pm2 status | grep -q "admin-panel" || pm2 start "npm start" --name admin-panel --cwd /home/$SUDO_USER/admin-frontend --watch -- --port $ADMIN_PORT
pm2 status | grep -q "website" || pm2 start "npm start" --name website --cwd /home/$SUDO_USER/web-frontend --watch -- --port $WEBSITE_PORT
pm2 save
pm2 startup | tail -n 1 | bash

#=============================#
#  9. Deployment Report      #
#=============================#
clear
echo "✅ Deployment Complete - $(date '+%Y-%m-%d')"
echo "------------------------------------------"
echo "🔹 Django Backend (Gunicorn)"
echo "    Domain : https://$DJANGO_SUBDOMAIN"
echo "    Port   : $DJANGO_PORT"
echo ""
echo "🔹 Next.js Admin Panel (PM2)"
echo "    Domain : https://$ADMIN_SUBDOMAIN"
echo "    Port   : $ADMIN_PORT"
echo ""
echo "🔹 Next.js Website (PM2)"
echo "    Domain : https://$WEBSITE_DOMAIN"
echo "    Port   : $WEBSITE_PORT"
echo ""
echo "🔒 SSL     : Enabled via Let's Encrypt"
echo "🧱 Firewall: UFW enabled (Ports 22, 80, 443 open)"
echo "🧩 Nginx   : Configs at $NGINX_PATH"
echo "📝 Logs    : /var/log/nginx/access.log, /var/log/nginx/error.log"
echo "📦 Services:"
echo "   - Gunicorn: systemctl status gunicorn"
echo "   - PM2 Apps: pm2 list"
echo "📅 Auto SSL Renewal: Enabled via certbot.timer"
echo "------------------------------------------"
