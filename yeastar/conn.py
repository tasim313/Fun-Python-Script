import paramiko

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

# Try Yeastar specific commands
commands = [
    "sms_tool -h",  # Check if sms_tool exists
    "asterisk -rx 'sms show stats'",  # Asterisk SMS commands
    "cat /ysdisk/sms/recvsms/* 2>/dev/null | head -50",  # Try recvsms instead
]

for cmd in commands:
    print(f"\n=== Testing: {cmd} ===")
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    if output:
        print("OUTPUT:", output)
    if error:
        print("ERROR:", error)

client.close()