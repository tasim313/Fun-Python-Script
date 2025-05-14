#!/bin/bash

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-psycopg2 python3-cups

# Create application directory
sudo mkdir -p /opt/print_logger
sudo cp print_log_to_db.py /opt/print_logger/
sudo chmod +x /opt/print_logger/print_log_to_db.py

# Create systemd service with more robust boot handling
sudo tee /etc/systemd/system/print_logger.service > /dev/null <<EOF
[Unit]
Description=Print Logger Service
After=network.target network-online.target cups.service
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/print_logger/print_log_to_db.py
WorkingDirectory=/opt/print_logger
StandardOutput=journal
StandardError=journal
Restart=always
RestartSec=5s
User=root

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable --now print_logger.service

echo "Print logger installed and configured to run at boot"
