from flask import Flask, render_template, send_file
import paramiko
import os

app = Flask(__name__)

# NAS server details
NAS_HOST = "192.168.1.10"
NAS_USER = "root"
NAS_PASSWORD = "#8234*fnas"
TARGET_DIRECTORY = "/mnt/aikhanlab-adm-nas/nas_lab_reports/lab_reports/scan_external_report"

def get_files_from_nas():
    """Connect to NAS and retrieve file list."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(NAS_HOST, username=NAS_USER, password=NAS_PASSWORD)

        # Get file list
        command = f"ls -1 {TARGET_DIRECTORY}"
        stdin, stdout, stderr = ssh.exec_command(command)
        files = stdout.read().decode().splitlines()
        
        ssh.close()
        return files
    except Exception as e:
        print(f"Error connecting to NAS: {e}")
        return []

@app.route('/')
def index():
    files = get_files_from_nas()
    return render_template('index2.html', files=files)

@app.route('/view/<filename>')
def view_file(filename):
    """Serve file from NAS."""
    file_path = os.path.join(TARGET_DIRECTORY, filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False)
    return "File not found!", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
