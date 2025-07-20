#!/bin/bash

set -e

echo "🛠️ Updating system..."
sudo apt update -y
sudo apt upgrade -y
echo "✅ System updated."

echo "🌐 Installing Apache2..."
sudo apt install apache2 -y
sudo systemctl enable apache2
sudo systemctl start apache2
echo "✅ Apache2 installed and running."

echo "📦 Adding PHP 8.2 repository..."
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:ondrej/php -y
sudo apt update -y

echo "🐘 Installing PHP 8.2 and required extensions..."
PHP_PACKAGES=(
    php8.2
    php8.2-cli
    php8.2-common
    php8.2-curl
    php8.2-gd
    php8.2-imap
    php8.2-intl
    php8.2-mbstring
    php8.2-mysql
    php8.2-xml
    php8.2-zip
    php8.2-bz2
    php8.2-ldap
    php8.2-opcache
    php8.2-readline
    libapache2-mod-php8.2
)

for pkg in "${PHP_PACKAGES[@]}"; do
    echo "Installing $pkg..."
    sudo apt install -y "$pkg" || echo "⚠️ Failed to install $pkg"
done

echo "✅ PHP 8.2 extensions installed."

# PHP configuration tuning
PHP_INI_PATH="/etc/php/8.2/apache2/php.ini"
echo "⚙️ Configuring PHP settings..."
if [ -f "$PHP_INI_PATH" ]; then
    sudo sed -i 's/^memory_limit = .*/memory_limit = 512M/' "$PHP_INI_PATH"
    sudo sed -i 's/^max_execution_time = .*/max_execution_time = 300/' "$PHP_INI_PATH"
    sudo sed -i 's/^post_max_size = .*/post_max_size = 64M/' "$PHP_INI_PATH"
    sudo sed -i 's/^upload_max_filesize = .*/upload_max_filesize = 64M/' "$PHP_INI_PATH"
    sudo sed -i 's/^;date.timezone =/date.timezone = UTC/' "$PHP_INI_PATH"
    sudo sed -i 's/^;opcache.enable=1/opcache.enable=1/' "$PHP_INI_PATH"
    echo "✅ PHP configured."
else
    echo "⚠️ $PHP_INI_PATH not found!"
fi

echo "🧰 Installing Git, curl, unzip..."
sudo apt install git curl unzip -y

echo "🔌 Enabling Apache modules..."
sudo a2enmod rewrite headers expires
sudo systemctl restart apache2

echo "🔐 Setting permissions for /var/www/html..."
sudo chown -R www-data:www-data /var/www/html
sudo find /var/www/html -type d -exec chmod 755 {} \;
sudo find /var/www/html -type f -exec chmod 644 {} \;

echo "🧪 Creating PHP info file..."
echo "<?php phpinfo(); ?>" | sudo tee /var/www/html/info.php > /dev/null

# --- ✅ Final Report ---
echo ""
echo "🚀 --- Environment Setup Report ---"

# Apache Status
systemctl is-active --quiet apache2 && echo "Apache2: ✅ Running" || echo "Apache2: ❌ Not Running"

# PHP Version
PHP_VERSION=$(php -v | head -n1 | awk '{print $2}')
echo "PHP Version: $PHP_VERSION"

# PHP Modules Verification
echo "📦 Checking PHP packages..."
for pkg in "${PHP_PACKAGES[@]}"; do
    if dpkg -s "$pkg" &>/dev/null; then
        echo "$pkg: ✅ Installed"
    else
        echo "$pkg: ❌ Not Installed"
    fi
done

# Git Version Check
echo ""
if command -v git &>/dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo "Git: ✅ Installed (Version: $GIT_VERSION)"
else
    echo "Git: ❌ Not Installed"
fi

echo ""
echo "🌍 Visit: http://your-server-ip/info.php to verify PHP installation"
echo "➡️ Next Step: Clone Dolibarr to /var/www/html/ and start installation"
echo "✅ Setup Complete!"

