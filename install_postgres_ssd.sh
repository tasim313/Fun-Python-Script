#!/bin/bash

set -e

# ------------------------- CONFIG -------------------------
PG_VERSION=17
SSD_MOUNT_DEFAULT="/media/zero/Database"
UBUNTU_CODENAME=$(lsb_release -cs)

# ---------------------- ROOT CHECK -----------------------
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (sudo)."
   exit 1
fi

echo "🔍 Searching for external drives..."

# ------------------ DETECT MOUNTED DRIVES -----------------
AVAILABLE_PATHS=($(lsblk -o MOUNTPOINT -nr | grep '^/media/' || true))

SELECTED_PATH=""
if [ ${#AVAILABLE_PATHS[@]} -eq 0 ]; then
    echo "⚠️  No external SSD found under /media/"
    echo "📁 Available mountable paths:"
    df -h | awk '$1 ~ /^\/dev/ {print $6}' | while read -r line; do
        echo " - $line"
    done
    read -rp "➡️  Enter the path to use as data directory: " SELECTED_PATH
else
    echo "🔍 External drives detected:"
    for i in "${!AVAILABLE_PATHS[@]}"; do
        echo "[$i] ${AVAILABLE_PATHS[$i]}"
    done
    read -rp "✅ Select the drive number to use for PostgreSQL data [0-${#AVAILABLE_PATHS[@]}]: " DRIVE_INDEX
    SELECTED_PATH="${AVAILABLE_PATHS[$DRIVE_INDEX]}"
fi

# --------------------- VALIDATION -------------------------
if [ -z "$SELECTED_PATH" ] || [ ! -d "$SELECTED_PATH" ]; then
    echo "❌ Invalid path. Aborting."
    exit 1
fi

NEW_PG_DIR="$SELECTED_PATH/postgresql/${PG_VERSION}/main"

echo "📦 PostgreSQL data will be moved to: $NEW_PG_DIR"

read -rp "Are you sure you want to continue? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" ]]; then
    echo "❌ Operation cancelled."
    exit 1
fi

# ---------------- REMOVE OLD POSTGRES ---------------------
echo "📦 Removing old PostgreSQL installations..."
systemctl stop postgresql || true
apt-get --purge remove -y postgresql* postgresql-client* postgresql-contrib* || true
apt-get autoremove -y
rm -rf /var/lib/postgresql /etc/postgresql /etc/postgresql-common /var/log/postgresql /usr/lib/postgresql /usr/share/postgresql

echo "✅ PostgreSQL removed."

# ---------------- INSTALL DEPENDENCIES --------------------
echo "🔧 Installing prerequisites..."
apt-get update
apt-get install -y wget gnupg2 ca-certificates lsb-release software-properties-common sudo

# ------------------- ADD PPA REPO -------------------------
echo "📥 Adding PostgreSQL repository..."
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
sh -c "echo 'deb http://apt.postgresql.org/pub/repos/apt ${UBUNTU_CODENAME}-pgdg main' > /etc/apt/sources.list.d/pgdg.list"
apt-get update

# ------------------ INSTALL POSTGRES ----------------------
echo "🧩 Installing PostgreSQL $PG_VERSION..."
apt-get install -y postgresql-$PG_VERSION postgresql-contrib

# ------------------- MOUNT CHECK --------------------------
echo "💾 Checking SSD mount..."
if ! grep -qs "$SELECTED_PATH" /proc/mounts; then
    echo "❌ Selected path not mounted. Please mount it manually and rerun."
    exit 1
fi

# ------------------ PERMISSIONS ---------------------------
echo "🔐 Setting permissions..."
mkdir -p "$NEW_PG_DIR"
chown -R postgres:postgres "$SELECTED_PATH"
chmod -R 700 "$SELECTED_PATH"

# ------------------ INITIALIZE DATA DIR -------------------
echo "📁 Initializing new PostgreSQL data directory..."

systemctl stop postgresql || true
sudo -u postgres /usr/lib/postgresql/$PG_VERSION/bin/initdb -D "$NEW_PG_DIR"

# ------------------- UPDATE CONFIG ------------------------
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
echo "⚙️  Updating PostgreSQL config..."

mkdir -p "/etc/postgresql/$PG_VERSION/main"
cp /usr/share/postgresql/$PG_VERSION/postgresql.conf.sample "$PG_CONF"

sed -i "s|^#data_directory =.*|data_directory = '$NEW_PG_DIR'|" "$PG_CONF"

mkdir -p /var/log/postgresql
chown -R postgres:postgres /var/log/postgresql

mkdir -p /var/run/postgresql
chown -R postgres:postgres /var/run/postgresql

# ------------------ START POSTGRES ------------------------
echo "🚀 Starting PostgreSQL service..."
systemctl restart postgresql
systemctl enable postgresql

# -------------------- VALIDATION --------------------------
echo "🧪 Verifying setup..."
sudo -u postgres psql -c "SHOW data_directory;"

# ------------------- DONE -------------------
echo ""
echo "🎉 DONE: PostgreSQL $PG_VERSION has been fully installed."
echo "📂 Current data directory: $NEW_PG_DIR"
echo "📍 Log file path: /var/log/postgresql/"
echo ""
