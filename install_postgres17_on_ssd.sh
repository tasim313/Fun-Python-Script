#!/bin/bash
set -euo pipefail

# Configuration
PG_VERSION="17"
OS_CODENAME=$(lsb_release -cs)
PG_USER="postgres"
PG_GROUP="postgres"
SSD_USER=$(logname)  # Get the actual user running the script (via sudo)
SSD_GROUP=$(id -gn "$SSD_USER")
HOME_DATA_DIR="/home/$SSD_USER/postgresql/$PG_VERSION/main"  # Fallback directory
TEMP_DIR="/tmp/pg_install"
LOG_FILE="/var/log/pg_data_migration.log"

# PostgreSQL Admin Credentials
PG_ADMIN_USER="pgadmin"
PG_ADMIN_PASSWORD=""  # Leave empty to prompt during execution

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Initialize log file
exec > >(tee -a "$LOG_FILE") 2>&1
echo -e "${GREEN}PostgreSQL Data Directory Migration Script - $(date)${NC}"

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}Error: This script must be run as root (use sudo)${NC}" >&2
    exit 1
fi

# Function to display error and exit
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Function to prompt for confirmation
confirm() {
    read -rp "$1 [y/N] " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            true
            ;;
        *)
            false
            ;;
    esac
}

# Function to prompt for password
prompt_password() {
    while true; do
        read -rsp "Enter password for PostgreSQL admin user '$PG_ADMIN_USER': " PG_ADMIN_PASSWORD
        echo
        if [ -z "$PG_ADMIN_PASSWORD" ]; then
            echo -e "${RED}Password cannot be empty${NC}"
            continue
        fi
        read -rsp "Confirm password: " password_confirm
        echo
        if [ "$PG_ADMIN_PASSWORD" != "$password_confirm" ]; then
            echo -e "${RED}Passwords do not match${NC}"
        else
            break
        fi
    done
}

# Function to detect or create data directory
setup_data_directory() {
    echo -e "${YELLOW}Setting up data directory...${NC}"
    
    # First try to find external drives
    local drives=()
    while IFS= read -r line; do
        drives+=("$line")
    done < <(find /media -maxdepth 2 -mindepth 1 -type d | grep -v '/\.')

    if [ ${#drives[@]} -eq 0 ]; then
        echo -e "${YELLOW}No external drives found under /media, using home directory${NC}"
        DATA_DIR="$HOME_DATA_DIR"
    else
        echo -e "${GREEN}Available drives:${NC}"
        for i in "${!drives[@]}"; do
            echo "$((i+1)). ${drives[$i]} (Free space: $(df -h "${drives[$i]}" | awk 'NR==2 {print $4}'))"
        done

        echo -e "${YELLOW}$(( ${#drives[@]} + 1 )). Use home directory (/home/$SSD_USER/postgresql)${NC}"

        local selection=0
        while [[ $selection -lt 1 || $selection -gt $(( ${#drives[@]} + 1 )) ]]; do
            read -rp "Select a location (1-$(( ${#drives[@]} + 1 ))): " selection
            if [[ ! "$selection" =~ ^[0-9]+$ ]]; then
                selection=0
            fi
        done

        if [ "$selection" -le "${#drives[@]}" ]; then
            selected_drive="${drives[$((selection-1))]}"
            echo -e "${GREEN}Selected drive: $selected_drive${NC}"
            read -rp "Enter subdirectory name (default: postgresql/$PG_VERSION/main): " subdir
            subdir=${subdir:-"postgresql/$PG_VERSION/main"}
            DATA_DIR="$selected_drive/$subdir"
        else
            DATA_DIR="$HOME_DATA_DIR"
        fi
    fi

    echo -e "${GREEN}Using data directory: $DATA_DIR${NC}"
}

# Function to set up directory permissions
setup_directory_permissions() {
    echo -e "${YELLOW}Setting up comprehensive directory permissions...${NC}"
    
    # Create parent directory structure
    mkdir -p "$(dirname "$DATA_DIR")"
    
    # Set ownership to SSD user with SGID (so new files inherit group)
    chown "$SSD_USER:$SSD_GROUP" "$(dirname "$DATA_DIR")"
    chmod 2775 "$(dirname "$DATA_DIR")"  # 2 = SGID, 775 for rwx on user/group
    
    # Add postgres user to SSD group if not already
    if ! id "$PG_USER" | grep -q "\b$SSD_GROUP\b"; then
        usermod -aG "$SSD_GROUP" "$PG_USER"
        echo -e "${GREEN}Added postgres user to group $SSD_GROUP${NC}"
    fi

    # Create data directory with strict permissions
    mkdir -p "$DATA_DIR"
    chown "$PG_USER:$PG_GROUP" "$DATA_DIR"
    chmod 700 "$DATA_DIR"

    # Apply ACLs if available
    if command -v setfacl >/dev/null; then
        setfacl -Rm g:"$SSD_GROUP":r-x "$(dirname "$DATA_DIR")"
        setfacl -Rm u:"$PG_USER":rwx "$DATA_DIR"
        setfacl -Rm g:"$PG_GROUP":r-x "$DATA_DIR"
    fi

    # Sticky bit to prevent accidental file deletion by other users
    chmod +t "$(dirname "$DATA_DIR")"

    # Set SELinux context (safe fallback)
    if command -v chcon >/dev/null; then
        chcon -R -t postgresql_db_t "$DATA_DIR" || true
    fi

    # Recursively enforce strict PostgreSQL ownership and permissions
    echo -e "${YELLOW}Finalizing recursive ownership and strict permissions...${NC}"
    chown -R "$PG_USER:$PG_GROUP" "$DATA_DIR"
    chmod -R 700 "$DATA_DIR"

    # Print summary
    echo -e "${GREEN}Comprehensive permissions configured:${NC}"
    echo -e "  Directory: $(dirname "$DATA_DIR")"
    echo -e "  Owner: $(stat -c "%U:%G" "$(dirname "$DATA_DIR")")"
    echo -e "  Permissions: $(stat -c "%a" "$(dirname "$DATA_DIR")")"
    echo -e "  Data Directory: $DATA_DIR"
    echo -e "  Owner: $(stat -c "%U:%G" "$DATA_DIR")"
    echo -e "  Permissions: $(stat -c "%a" "$DATA_DIR")"
    
    if command -v getfacl >/dev/null; then
        echo -e "${BLUE}ACL Information:${NC}"
        getfacl "$(dirname "$DATA_DIR")" | head -5
        getfacl "$DATA_DIR" | head -5
    fi
}


# Function to completely remove existing PostgreSQL installations
remove_existing_postgresql() {
    echo -e "${YELLOW}Removing existing PostgreSQL installations...${NC}"
    
    # Stop all PostgreSQL services (fixed version)
    systemctl list-units --full --all --plain --no-legend \
        | grep -E 'postgresql.*service' \
        | awk '{print $1}' \
        | xargs -r systemctl stop
    
    # Remove packages
    apt-get purge -y postgresql* pgdg* || true
    apt-get autoremove -y
    
    # Remove data directories
    find /var/lib/postgresql /var/log/postgresql /etc/postgresql -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null || true
    
    # Remove configuration files
    rm -rf /etc/postgresql-common /etc/apt/sources.list.d/pgdg.list /usr/share/keyrings/postgresql.gpg
    
    echo -e "${GREEN}Existing PostgreSQL installations removed.${NC}"
}

# Function to install PostgreSQL 17
install_postgresql() {
    echo -e "${YELLOW}Installing PostgreSQL $PG_VERSION...${NC}"
    
    # Add PostgreSQL repository
    apt-get install -y wget gnupg2
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql.gpg
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/postgresql.gpg] https://apt.postgresql.org/pub/repos/apt $OS_CODENAME-pgdg main" > /etc/apt/sources.list.d/pgdg.list
    
    apt-get update
    apt-get install -y "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION"
    
    echo -e "${GREEN}PostgreSQL $PG_VERSION installed successfully.${NC}"
}

# Function to initialize data directory
initialize_data_directory() {
    echo -e "${YELLOW}Initializing data directory at $DATA_DIR...${NC}"
    
    # Stop PostgreSQL service if running
    systemctl stop "postgresql@$PG_VERSION-main" 2>/dev/null || true
    
    # Create and set permissions for data directory
    mkdir -p "$DATA_DIR"
    chown "$PG_USER:$PG_GROUP" "$DATA_DIR"
    chmod 750 "$DATA_DIR"
    
    # Check if directory is empty
    if [ "$(ls -A "$DATA_DIR")" ]; then
        echo -e "${YELLOW}Directory $DATA_DIR is not empty. Creating new directory with timestamp...${NC}"
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        NEW_DATA_DIR="${DATA_DIR}_${TIMESTAMP}"
        mkdir -p "$NEW_DATA_DIR"
        chown "$PG_USER:$PG_GROUP" "$NEW_DATA_DIR"
        chmod 750 "$NEW_DATA_DIR"
        DATA_DIR="$NEW_DATA_DIR"
        echo -e "${GREEN}Using new data directory: $DATA_DIR${NC}"
    fi
    
    # Initialize the database cluster
    if ! sudo -u "$PG_USER" "/usr/lib/postgresql/$PG_VERSION/bin/initdb" -D "$DATA_DIR"; then
        echo -e "${RED}Failed to initialize data directory at $DATA_DIR${NC}"
        echo -e "${YELLOW}Attempting to clean up and retry...${NC}"
        rm -rf "$DATA_DIR"/*
        rm -rf "$DATA_DIR"/.??*
        if ! sudo -u "$PG_USER" "/usr/lib/postgresql/$PG_VERSION/bin/initdb" -D "$DATA_DIR"; then
            error_exit "Could not initialize data directory after cleanup attempt"
        fi
    fi
    
    echo -e "${GREEN}Data directory initialized successfully at $DATA_DIR${NC}"
}

# Function to update configuration
update_configuration() {
    echo -e "${YELLOW}Updating PostgreSQL configuration...${NC}"
    
    # Update data_directory in postgresql.conf
    local config_file="$DATA_DIR/postgresql.conf"
    if [ -f "$config_file" ]; then
        sed -i "s|^#*data_directory = .*|data_directory = '$DATA_DIR'|" "$config_file"
    else
        error_exit "postgresql.conf not found in $DATA_DIR"
    fi
    
    # Update systemd service configuration
    local override_dir="/etc/systemd/system/postgresql@$PG_VERSION-main.service.d"
    mkdir -p "$override_dir"
    cat > "$override_dir/override.conf" <<EOF
[Service]
Environment=PGDATA=$DATA_DIR
EOF
    
    # Update the default cluster configuration
    local old_data_dir="/var/lib/postgresql/$PG_VERSION/main"
    if [ -d "$old_data_dir" ]; then
        echo -e "${YELLOW}Removing old data directory: $old_data_dir${NC}"
        rm -rf "$old_data_dir"
    fi
    
    # Create symlink from default location to new location
    mkdir -p "/etc/postgresql/$PG_VERSION"
    ln -sfn "$DATA_DIR" "/etc/postgresql/$PG_VERSION/main"
    
    systemctl daemon-reload
    
    echo -e "${GREEN}Configuration updated successfully.${NC}"
}

# Function to start and verify PostgreSQL
start_postgresql() {
    echo -e "${YELLOW}Starting PostgreSQL service...${NC}"
    
    systemctl enable "postgresql@$PG_VERSION-main"
    if ! systemctl start "postgresql@$PG_VERSION-main"; then
        journalctl -u "postgresql@$PG_VERSION-main" -n 50 --no-pager
        error_exit "Failed to start PostgreSQL service"
    fi
    
    # Verify data directory
    local active_data_dir=$(sudo -u "$PG_USER" psql -tAc "SHOW data_directory;")
    if [ "$active_data_dir" != "$DATA_DIR" ]; then
        echo -e "${YELLOW}PostgreSQL is not using the correct data directory. Attempting to fix...${NC}"
        
        # Additional verification and fix
        local config_data_dir=$(sudo -u "$PG_USER" psql -tAc "SHOW config_file;" | xargs grep -oP "data_directory\s*=\s*'\K[^']+")
        if [ "$config_data_dir" != "$DATA_DIR" ]; then
            error_exit "Could not verify data directory in config. Expected: $DATA_DIR, Found: $config_data_dir"
        else
            echo -e "${GREEN}Verified data directory in config file. Service may need restart.${NC}"
            systemctl restart "postgresql@$PG_VERSION-main"
            active_data_dir=$(sudo -u "$PG_USER" psql -tAc "SHOW data_directory;")
            if [ "$active_data_dir" != "$DATA_DIR" ]; then
                error_exit "PostgreSQL is still not using the correct data directory. Expected: $DATA_DIR, Actual: $active_data_dir"
            fi
        fi
    fi
    
    echo -e "${GREEN}PostgreSQL is now running from: $active_data_dir${NC}"
}

# Function to create admin user and set password
setup_postgres_admin() {
    echo -e "${YELLOW}Setting up PostgreSQL admin user...${NC}"
    
    # Prompt for admin password if not set
    if [ -z "$PG_ADMIN_PASSWORD" ]; then
        prompt_password
    fi
    
    # Create the admin user
    sudo -u "$PG_USER" psql -d postgres -c "CREATE USER $PG_ADMIN_USER WITH SUPERUSER CREATEDB CREATEROLE PASSWORD '$PG_ADMIN_PASSWORD';"
    
    # Update pg_hba.conf to allow password authentication
    local hba_file="$DATA_DIR/pg_hba.conf"
    if [ -f "$hba_file" ]; then
        sed -i 's/local   all             all                                     peer/local   all             all                                     md5/' "$hba_file"
        # Restart PostgreSQL to apply changes
        systemctl restart "postgresql@$PG_VERSION-main"
    fi
    
    echo -e "${GREEN}PostgreSQL admin user '$PG_ADMIN_USER' created successfully.${NC}"
}

# Main execution
main() {
    echo -e "${GREEN}=== PostgreSQL Data Directory Migration Script ===${NC}"
    echo -e "${YELLOW}Detected user: $SSD_USER (group: $SSD_GROUP)${NC}"
    
    # Setup data directory
    setup_data_directory
    
    if ! confirm "Proceed with migration to $DATA_DIR?"; then
        echo -e "${YELLOW}Migration cancelled by user.${NC}"
        exit 0
    fi
    
    # Setup directory permissions
    setup_directory_permissions
    
    # Clean slate - remove existing installations
    if confirm "Remove all existing PostgreSQL installations for a clean slate?"; then
        remove_existing_postgresql
    else
        echo -e "${YELLOW}Skipping removal of existing installations.${NC}"
    fi
    
    # Install PostgreSQL 17
    install_postgresql
    
    # Initialize data directory
    initialize_data_directory
    
    # Update configuration
    update_configuration
    
    # Start PostgreSQL
    start_postgresql
    
    # Setup admin user
    setup_postgres_admin
    
    echo -e "${GREEN}=== Migration completed successfully ===${NC}"
    echo -e "${GREEN}PostgreSQL data directory: $DATA_DIR${NC}"
    echo -e "${GREEN}PostgreSQL admin user: $PG_ADMIN_USER${NC}"
    echo -e "${GREEN}Directory permissions:${NC}"
    ls -ld "$(dirname "$DATA_DIR")"
    ls -ld "$DATA_DIR"
    echo -e "${GREEN}Service status:${NC}"
    systemctl status "postgresql@$PG_VERSION-main" --no-pager
    echo -e "${GREEN}Log file: $LOG_FILE${NC}"
    # Show PostgreSQL process info
   echo -e "${GREEN}PostgreSQL processes:${NC}"
   ps -ef | grep postgres | grep -v grep
}

main
