import paramiko

# NAS server connection details
NAS_HOST = "192.168.1.10"
NAS_USER = "root"
NAS_PASSWORD = "#8234*fnas"
TARGET_DIRECTORY = "/mnt/aikhanlab-adm-nas/nas_lab_reports/lab_reports/scan_external_report"

try:
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Auto accept host key
    
    # Connect to NAS server
    ssh.connect(NAS_HOST, username=NAS_USER, password=NAS_PASSWORD)
    print("Connected to NAS server successfully!")

    # Run command to list files with full path
    command = f"ls -l {TARGET_DIRECTORY}"
    stdin, stdout, stderr = ssh.exec_command(command)

    # Read output
    files = stdout.readlines()

    if files:
        print(f"\nTotal Files: {len(files) - 1}")  # Subtracting 1 for the total count line
        print("Files in the directory:")
        for file in files[1:]:  # Skip the total count line
            file_name = file.split()[-1]  # Extract filename from `ls -l` output
            file_path = f"{TARGET_DIRECTORY}/{file_name}"
            print(f"- {file_name} | Path: {file_path}")
    else:
        print("No files found in the directory.")

    # Close SSH connection
    ssh.close()
    print("Disconnected from NAS server.")

except Exception as e:
    print(f"Failed to connect or retrieve files: {e}")
