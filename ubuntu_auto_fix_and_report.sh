#!/bin/bash

# Ubuntu Auto Update, Fix, and Reporting Script
# Author: tasim313
# Date: 2025-07-19
# This script checks and fixes common Ubuntu problems, then generates a report.

REPORT="/tmp/ubuntu_fix_report_$(date +%Y%m%d_%H%M%S).txt"
declare -A STATUS
declare -A ACTIONS

function log_action() {
    local item="$1"
    local status="$2"
    local action="$3"
    STATUS["$item"]="$status"
    ACTIONS["$item"]="$action"
}

echo "Ubuntu System Auto-Fix Script" > "$REPORT"
echo "Started at: $(date)" >> "$REPORT"
echo "---------------------------------------------------" >> "$REPORT"

# 1. Update & Upgrade
echo "Checking for update/upgrade issues..."
sudo apt-get update -y &> /tmp/apt_update.log
if grep -iq "Failed to fetch" /tmp/apt_update.log; then
    log_action "apt-get update" "Problem" "Failed to fetch errors found. Attempting to fix..."
    sudo apt-get clean
    sudo apt-get update --fix-missing -y
else
    log_action "apt-get update" "OK" "No errors found."
fi

sudo apt-get upgrade -y &> /tmp/apt_upgrade.log
if grep -iq "could not be located" /tmp/apt_upgrade.log; then
    log_action "apt-get upgrade" "Problem" "Unable to locate package error found. Attempting to fix..."
    sudo apt-get update
    sudo apt-get upgrade -y
else
    log_action "apt-get upgrade" "OK" "No errors found."
fi

# 2. Fix Broken Packages
echo "Checking for broken packages..."
BROKEN=$(sudo apt-get check 2>&1 | grep -i "broken")
if [[ -n "$BROKEN" ]]; then
    log_action "Broken packages" "Problem" "$BROKEN. Running apt-get install -f..."
    sudo apt-get install -f -y
else
    log_action "Broken packages" "OK" "No broken packages."
fi

# 3. GPG Key Errors
echo "Checking for GPG key errors..."
GPG_ERR=$(grep -r "NO_PUBKEY" /var/log/apt 2>/dev/null)
if [[ -n "$GPG_ERR" ]]; then
    KEYS=$(echo "$GPG_ERR" | grep -oP 'NO_PUBKEY \K[0-9A-F]+')
    log_action "GPG Key Errors" "Problem" "Missing keys: $KEYS. Attempting to fetch keys..."
    for KEY in $KEYS; do
        sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys "$KEY"
    done
    sudo apt-get update -y
else
    log_action "GPG Key Errors" "OK" "No GPG key errors."
fi

# 4. Dependency Errors
echo "Checking for dependency errors..."
DEP_ERR=$(sudo apt-get check 2>&1 | grep -E 'depends|dependency')
if [[ -n "$DEP_ERR" ]]; then
    log_action "Dependency Errors" "Problem" "$DEP_ERR. Running apt-get install -f..."
    sudo apt-get install -f -y
else
    log_action "Dependency Errors" "OK" "No dependency errors."
fi

# 5. File System and Permission Errors
echo "Checking for file system and permission errors..."
FS_ERR=$(dmesg | grep -iE 'EXT4-fs error|permission denied|readonly')
if [[ -n "$FS_ERR" ]]; then
    log_action "File System/Permission" "Problem" "$FS_ERR. Attempting to fix permissions..."
    sudo chmod -R 755 /var/lib/dpkg
    sudo dpkg --configure -a
else
    log_action "File System/Permission" "OK" "No file system or permission errors."
fi

# 6. Hardware and Driver Issues
echo "Checking for hardware/driver issues..."
HW_ERR=$(dmesg | grep -iE 'fail|error|driver|hardware' | grep -vE 'usb|battery|power')
if [[ -n "$HW_ERR" ]]; then
    log_action "Hardware/Driver" "Problem" "$HW_ERR. Recommend checking drivers manually."
else
    log_action "Hardware/Driver" "OK" "No critical hardware/driver issues detected."
fi

# 7. Interrupted System Call
echo "Checking for interrupted system calls..."
INT_ERR=$(dmesg | grep -i "interrupted system call")
if [[ -n "$INT_ERR" ]]; then
    log_action "Interrupted System Call" "Problem" "$INT_ERR. Suggest rebooting if persistent."
else
    log_action "Interrupted System Call" "OK" "No interrupted system call errors."
fi

# 8. Out of Memory
echo "Checking for out of memory errors..."
OOM_ERR=$(dmesg | grep -i "out of memory")
if [[ -n "$OOM_ERR" ]]; then
    log_action "Out of Memory" "Problem" "$OOM_ERR. Attempting to free memory..."
    sudo sync; sudo sysctl -w vm.drop_caches=3
else
    log_action "Out of Memory" "OK" "No out of memory errors."
fi

# 9. Connection Refused
echo "Checking for connection refused errors..."
CONN_ERR=$(dmesg | grep -i "connection refused")
if [[ -n "$CONN_ERR" ]]; then
    log_action "Connection Refused" "Problem" "$CONN_ERR. Check network and restart networking service."
    sudo systemctl restart networking
else
    log_action "Connection Refused" "OK" "No connection refused errors."
fi

# Summarize & Generate Report
echo "---------------------------------------------------" >> "$REPORT"
echo "Final Report:" >> "$REPORT"
for ITEM in "${!STATUS[@]}"; do
    echo "$ITEM: ${STATUS[$ITEM]}" >> "$REPORT"
    echo "Action: ${ACTIONS[$ITEM]}" >> "$REPORT"
    echo "---------------------------------------------------" >> "$REPORT"
done

echo "Report generated at: $REPORT"
cat "$REPORT"
