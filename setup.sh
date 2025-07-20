#!/bin/bash

set -e  # Exit on any error

USER_NAME=$(whoami)
USER_GROUP=$(id -gn)
USER_HOME=$(eval echo "~$USER_NAME")
SCRIPT_DIR="$USER_HOME/cups_log_script"
SCRIPT_NAME="print_log_to_db.py"
VENV_DIR="$SCRIPT_DIR/cups_log_env"
SERVICE_NAME="cups_log_$USER_NAME.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"
LOG_FILE="/home/$USER_NAME/cups_log_script/service_debug.log"

# Check if required files exist
if [ ! -f "$SCRIPT_NAME" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Error: $SCRIPT_NAME or requirements.txt not found in current directory."
    exit 1
fi

# --- Ensure user is in 'lp' group ---
if groups "$USER_NAME" | grep -qw "lp"; then
    echo "✅ User $USER_NAME is already in lp group."
else
    echo "➕ Adding user $USER_NAME to lp group..."
    sudo usermod -aG lp "$USER_NAME"
    echo "✅ User added to lp group. Please re-login after this script finishes!"
fi

# Setup project directory
mkdir -p "$SCRIPT_DIR"
sudo chown -R "$USER_NAME":"$USER_GROUP" "$SCRIPT_DIR"
sudo chmod -R 755 "$SCRIPT_DIR"

# Copy files to the project directory
cp -f "$SCRIPT_NAME" "$SCRIPT_DIR/"
cp -f requirements.txt "$SCRIPT_DIR/"
sudo chmod 644 "$SCRIPT_DIR/$SCRIPT_NAME" "$SCRIPT_DIR/requirements.txt"

# Delete previous virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    echo "❌ Virtual environment exists. Removing it."
    rm -rf "$VENV_DIR"
fi

# Setup fresh virtual environment
python3 -m venv "$VENV_DIR"

# Ensure venv has proper permissions
sudo chown -R "$USER_NAME":"$USER_GROUP" "$VENV_DIR"
sudo chmod -R 755 "$VENV_DIR"

# Install requirements inside the virtual environment
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"

# --- Create systemd service file ---
sudo bash -c "cat > $SERVICE_PATH" <<EOF
[Unit]
Description=CUPS Log to DB Service for $USER_NAME
After=network.target

[Service]
ExecStart=/usr/bin/sudo $VENV_DIR/bin/python3 $SCRIPT_DIR/$SCRIPT_NAME
WorkingDirectory=$SCRIPT_DIR
User=$USER_NAME
Group=$USER_GROUP
Environment=PATH=$VENV_DIR/bin
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo chmod 644 "$SERVICE_PATH"

# Reload systemd manager configuration
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable "$SERVICE_NAME"

# Start the service immediately
sudo systemctl restart "$SERVICE_NAME"

echo "✅ Setup complete for user $USER_NAME."
echo "✅ Service name is $SERVICE_NAME."
echo "📢 IMPORTANT: You must log out and log back in for 'lp' group changes to take effect."

sudo systemctl status print_logger.service
