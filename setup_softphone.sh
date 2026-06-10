#!/usr/bin/env bash
set -e

# ===== CONFIGURE THESE =====
SIP_USER="1001"               # Your SIP extension
SIP_PASS="yourpassword"       # Your SIP password
SIP_DOMAIN="pbx.example.com"  # Your SIP server/PBX domain or IP
SIP_TRANSPORT="udp"           # udp | tcp | tls
# ===========================

echo "[*] Installing dependencies..."
sudo apt-get update
sudo apt-get install -y baresip libnotify-bin xdotool pulseaudio-utils

echo "[*] Setting up baresip config..."
mkdir -p ~/.baresip
cat > ~/.baresip/accounts <<EOF
<sip:${SIP_USER}@${SIP_DOMAIN}>;auth_user=${SIP_USER};auth_pass=${SIP_PASS};transport=${SIP_TRANSPORT}
EOF

cat > ~/.baresip/config <<EOF
# Minimal baresip config
audio_driver  alsa, pulse
video_source  fake
video_display x11
ausrc_format  s16
ausrc_srate   48000
auplay_format s16
auplay_srate  48000
EOF

# Python helper for notifications
cat > ~/sip_notify.py <<'PYEOF'
#!/usr/bin/env python3
import subprocess, sys, time

CALLER = sys.argv[1] if len(sys.argv) > 1 else "Unknown Caller"

def notify_with_actions():
    subprocess.Popen([
        "notify-send",
        "-u", "critical",
        "-a", "SIP Call",
        "-i", "call-start",
        "📞 Incoming Call",
        f"From: {CALLER}\nAccept or Reject?",
        "-h", "string:desktop-entry:baresip",
        "-A", "Accept",
        "-A", "Reject"
    ])

if __name__ == "__main__":
    notify_with_actions()
PYEOF
chmod +x ~/sip_notify.py

# Wrapper script to run baresip and hook notifications
cat > ~/start_softphone.sh <<'EOF'
#!/usr/bin/env bash
BARESIP_LOG=~/.baresip/baresip.log

# Start baresip in background
baresip -v > "$BARESIP_LOG" 2>&1 &
BARESIP_PID=$!

echo "[*] Baresip running with PID $BARESIP_PID"
echo "[*] Monitoring for calls..."

tail -Fn0 "$BARESIP_LOG" | \
while read -r line; do
    if [[ "$line" == *"call: incoming call from"* ]]; then
        CALLER=$(echo "$line" | sed -n 's/.*from \(sip:[^ ]*\).*/\1/p')
        ~/sip_notify.py "$CALLER" &
    fi

    if [[ "$line" == *"call answered"* ]]; then
        notify-send "✅ Call answered" "Talking to: $CALLER"
    fi

    if [[ "$line" == *"call closed"* ]]; then
        notify-send "☎️ Call ended" "With: $CALLER"
    fi
done

EOF
chmod +x ~/start_softphone.sh

echo
echo "[*] Setup complete."
echo "Run your softphone with:"
echo "   ~/start_softphone.sh"

