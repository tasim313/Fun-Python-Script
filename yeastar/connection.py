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

# List SMS files
stdin, stdout, stderr = client.exec_command(
    "ls /ysdisk/sms/sendsms"
)
files = stdout.read().decode().splitlines()
print(files)

# Read each SMS file with sudo
for file in files:
    print("FILE:", file)
    
    # Use sudo to read the file
    cmd = f"sudo cat /ysdisk/sms/sendsms/{file}"
    print("CMD:", cmd)
    
    stdin, stdout, stderr = client.exec_command(cmd)
    
    print("CONTENT:")
    print(stdout.read().decode())
    error = stderr.read().decode()
    if error:
        print("ERROR:", error)
    
    print("=" * 50)

client.close()