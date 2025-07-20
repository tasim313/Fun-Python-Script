#!/bin/bash

set -e

# Variables
SSD_MOUNT="/media/zero/Database"
SSD_USER="zero"
SSD_PASS="@dmin*#135"
PG_VERSION="16"  # Change if newer version available
PG_CONF="/etc/postgresql"
HOME_DB_FOLDER="$HOME/Database"
POSTGRES_HOME_BASE="$HOME_DB_FOLDER/postgres17"
POSTGRES_HOME_NEW="$HOME_DB_FOLDER/postgres17_new"

# Helper function to detect external drives
detect_external_drives() {
    lsblk -o NAME,MOUNTPOINT,SIZE,TYPE | grep -E 'disk|part' | grep -v '^sda' | grep -v '^nvme0n1'
}

# 0. Detect external SSDs
echo "Detecting external drives..."
EXTERNAL_DRIVES=$(detect_external_drives)
if [[ -z "$EXTERNAL_DRIVES" ]]; then
    echo "No external SSDs found."
    # Fallback: Suggest HOME folder
    if [[ -d "$POSTGRES_HOME_BASE" ]]; then
        echo "Found existing folder: $POSTGRES_HOME_BASE"
        echo "Will create a new folder: $POSTGRES_HOME_NEW"
        PG_DATA="$POSTGRES_HOME_NEW/data"
        PG_LOGS="$POSTGRES_HOME_NEW/logs"
        PG_BACKUPS="$POSTGRES_HOME_NEW/backups"
        mkdir -p "$PG_DATA" "$PG_LOGS" "$PG_BACKUPS"
    else
        echo "No 'postgres17' folder found in $HOME_DB_FOLDER."
        read -p "Would you like to use $POSTGRES_HOME_BASE for PostgreSQL data? (y/n): " use_home
        if [[ "$use_home" == "y" ]]; then
            mkdir -p "$POSTGRES_HOME_BASE/data" "$POSTGRES_HOME_BASE/logs" "$POSTGRES_HOME_BASE/backups"
            PG_DATA="$POSTGRES_HOME_BASE/data"
            PG_LOGS="$POSTGRES_HOME_BASE/logs"
            PG_BACKUPS="$POSTGRES_HOME_BASE/backups"
        else
            echo "Cancelled installation. Exiting."
            exit 1
        fi
    fi
else
    echo "Found external drives:"
    echo "$EXTERNAL_DRIVES"
    read -p "Would you like to use an external SSD for PostgreSQL data? (y/n): " use_ssd
    if [[ "$use_ssd" == "y" ]]; then
        read -p "Enter the mount path for your SSD (e.g. /media/zero/Database): " SSD_MOUNT
        PG_DATA="$SSD_MOUNT/postgres_data"
        PG_LOGS="$SSD_MOUNT/postgres_logs"
        PG_BACKUPS="$SSD_MOUNT/postgres_backups"
    else
        if [[ -d "$POSTGRES_HOME_BASE" ]]; then
            echo "Found existing folder: $POSTGRES_HOME_BASE"
            echo "Will create a new folder: $POSTGRES_HOME_NEW"
            PG_DATA="$POSTGRES_HOME_NEW/data"
            PG_LOGS="$POSTGRES_HOME_NEW/logs"
            PG_BACKUPS="$POSTGRES_HOME_NEW/backups"
            mkdir -p "$PG_DATA" "$PG_LOGS" "$PG_BACKUPS"
        else
            echo "No 'postgres17' folder found in $HOME_DB_FOLDER."
            read -p "Would you like to use $POSTGRES_HOME_BASE for PostgreSQL data? (y/n): " use_home
            if [[ "$use_home" == "y" ]]; then
                mkdir -p "$POSTGRES_HOME_BASE/data" "$POSTGRES_HOME_BASE/logs" "$POSTGRES_HOME_BASE/backups"
                PG_DATA="$POSTGRES_HOME_BASE/data"
                PG_LOGS="$POSTGRES_HOME_BASE/logs"
                PG_BACKUPS="$POSTGRES_HOME_BASE/backups"
            else
                echo "Cancelled installation. Exiting."
                exit 1
            fi
        fi
    fi
fi

echo "PostgreSQL will use:"
echo "  Data directory: $PG_DATA"
echo "  Log files: $PG_LOGS"
echo "  Backups: $PG_BACKUPS"

# 1. Remove existing PostgreSQL
echo "Removing old PostgreSQL installations..."
sudo systemctl stop postgresql || true
sudo apt-get --purge remove -y postgresql* postgresql-client* postgresql-contrib* || true
sudo apt-get autoremove -y
sudo rm -rf /var/lib/postgresql/
sudo rm -rf /etc/postgresql/
sudo rm -rf /etc/postgresql-common/
sudo rm -rf /var/log/postgresql/
sudo rm -rf /usr/lib/postgresql/
sudo deluser postgres || true
sudo delgroup postgres || true

# 2. Install requirements
echo "Installing requirements..."
sudo apt-get update
sudo apt-get install -y wget ca-certificates gnupg lsb-release

# 3. Add PostgreSQL repository
echo "Adding PostgreSQL official repository..."
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

# 4. Install PostgreSQL
echo "Installing PostgreSQL..."
sudo apt-get update
sudo apt-get install -y postgresql-$PG_VERSION postgresql-client-$PG_VERSION

# 5. Mount the SSD if selected
if [[ "$PG_DATA" == "$SSD_MOUNT/postgres_data" ]]; then
    if ! mount | grep -q "$SSD_MOUNT"; then
        echo "Mounting SSD or selected directory..."
        sudo mkdir -p "$SSD_MOUNT"
        sudo apt-get install -y cifs-utils

        # Add credentials file for mounting (if using network mount)
        CRED_FILE="/root/.smbcredentials"
        echo "username=$SSD_USER" | sudo tee $CRED_FILE > /dev/null
        echo "password=$SSD_PASS" | sudo tee -a $CRED_FILE > /dev/null
        sudo chmod 600 $CRED_FILE

        echo "//localhost/Database $SSD_MOUNT cifs credentials=$CRED_FILE,iocharset=utf8,sec=ntlm,rw,file_mode=0777,dir_mode=0777 0 0" | sudo tee -a /etc/fstab

        sudo mount -a
    fi
    sudo chown -R postgres:postgres "$SSD_MOUNT"
    sudo chmod -R 700 "$PG_DATA" "$PG_LOGS" "$PG_BACKUPS"
else
    # Home directory fallback
    sudo chown -R postgres:postgres "$HOME_DB_FOLDER"
    sudo chmod -R 700 "$PG_DATA" "$PG_LOGS" "$PG_BACKUPS"
fi

# 6. Initialize PostgreSQL data directory
echo "Initializing new data directory..."
sudo systemctl stop postgresql
sudo -u postgres /usr/lib/postgresql/$PG_VERSION/bin/initdb -D "$PG_DATA"

# 7. Move/copy config files and update to point to new data directory
echo "Configuring PostgreSQL to use new data directory..."
PG_CONF_FILE="$PG_CONF/$PG_VERSION/main/postgresql.conf"
sudo cp "$PG_CONF_FILE" "$PG_CONF_FILE.bak"

sudo sed -i "s|^data_directory =.*|data_directory = '$PG_DATA'|" "$PG_CONF_FILE"
sudo sed -i "s|^log_directory =.*|log_directory = '$PG_LOGS'|" "$PG_CONF_FILE"

# 8. Update permissions
sudo chown -R postgres:postgres "$PG_DATA" "$PG_LOGS" "$PG_BACKUPS"

# 9. Restart PostgreSQL
echo "Restarting PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 10. Final summary
echo
echo "PostgreSQL has been installed and configured."
echo "All main folders and data have been moved to:"
echo "  Data directory: $PG_DATA"
echo "  Log files: $PG_LOGS"
echo "  Backups: $PG_BACKUPS"
echo "You can now verify your installation with:"
echo "  sudo -u postgres psql"
