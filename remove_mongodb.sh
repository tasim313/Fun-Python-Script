#!/bin/bash
# Focused MongoDB Removal Script

echo "Fixing MongoDB removal issues..."

# Remove corrupted MongoDB repository files
echo "Removing MongoDB repository files..."
sudo rm -f /etc/apt/sources.list.d/mongodb-org-6.0.list 2>/dev/null
sudo rm -f /etc/apt/sources.list.d/mongodb* 2>/dev/null

# Remove MongoDB GPG key
echo "Removing MongoDB GPG key..."
sudo apt-key del "$(sudo apt-key list | grep -B1 MongoDB | head -n1 | cut -d'/' -f2 | cut -d' ' -f1)" 2>/dev/null

# Force remove MongoDB packages
echo "Removing MongoDB packages..."
sudo dpkg --purge --force-all $(dpkg -l | grep mongo | awk '{print $2}') 2>/dev/null

# Remove MongoDB directories
echo "Removing MongoDB directories..."
sudo rm -rf /var/lib/mongodb
sudo rm -rf /var/log/mongodb
sudo rm -rf /tmp/mongodb-*

# Remove MongoDB configuration
echo "Removing MongoDB configuration..."
sudo rm -f /etc/mongod.conf
sudo rm -f /etc/mongodb.conf

# Update APT
echo "Updating package lists..."
sudo apt-get update

# Final cleanup
echo "Performing final cleanup..."
sudo apt-get autoremove -y
sudo apt-get clean

echo "MongoDB removal completed!"
echo "Please verify with: which mongod"
