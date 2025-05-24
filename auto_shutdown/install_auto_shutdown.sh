#!/bin/bash

# Exit on error and log all commands
set -e
set -x

# Define paths
SCRIPT_NAME="auto_shutdown.py"
SERVICE_NAME="auto_shutdown"
VENV_DIR="/opt/${SERVICE_NAME}_venv"
APP_DIR="/opt/${SERVICE_NAME}"
LOG_DIR="/var/log/${SERVICE_NAME}"

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# Create directories
sudo mkdir -p "$APP_DIR" "$LOG_DIR"

# Copy the Python script (assume it's in the same directory as this Bash script)
sudo cp "$SCRIPT_NAME" "$APP_DIR/"
sudo chmod +x "$APP_DIR/$SCRIPT_NAME"

# Create virtual environment
sudo python3 -m venv "$VENV_DIR"
sudo "$VENV_DIR/bin/pip" install pytz

# Create systemd service
sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" > /dev/null <<EOF
[Unit]
Description=Auto Shutdown at 11:30 PM (Bangladesh Time)
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=$VENV_DIR/bin/python3 $APP_DIR/$SCRIPT_NAME
WorkingDirectory=$APP_DIR
StandardOutput=append:$LOG_DIR/auto_shutdown.log
StandardError=append:$LOG_DIR/auto_shutdown.log
Restart=always
RestartSec=60
User=root

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable --now "$SERVICE_NAME.service"

# Set correct permissions for logs
sudo chown root:root "$LOG_DIR"
sudo chmod 644 "$LOG_DIR/auto_shutdown.log"

echo "----------------------------------------"
echo "Installation complete!"
echo "Service: $SERVICE_NAME"
echo "Python script: $APP_DIR/$SCRIPT_NAME"
echo "Logs: $LOG_DIR/auto_shutdown.log"
echo "----------------------------------------"