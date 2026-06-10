import os
import logging
import psycopg2
import time
import cups
import re
from datetime import datetime
import pwd
import grp
import subprocess

# Setup paths dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_dir, 'service_debug.log')

# Setup logging
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

logging.debug('Script started...')

# PostgreSQL connection details
DB_HOST = '192.168.1.139'
DB_PORT = '5432'
DB_NAME = 'dolibarr'
DB_USER = 'root'
DB_PASS = 'root'

# CUPS log file
LOG_FILE = '/var/log/cups/page_log'

# Function to check file permissions and ACL
def check_logfile_permissions(file_path):
    try:
        st = os.stat(file_path)
        current_user = pwd.getpwuid(os.getuid()).pw_name
        logging.info(f"Current user: {current_user}")
        logging.info(f"File owner: {pwd.getpwuid(st.st_uid).pw_name}, group: {grp.getgrgid(st.st_gid).gr_name}")
        # Try to open to check read permission
        with open(file_path, 'r') as f:
            logging.info("Log file opened successfully. Read permission confirmed.")
    except PermissionError:
        logging.error(f"Permission denied for user '{current_user}' on {file_path}. Trying to suggest ACL fix.")
        logging.error(f"Suggest running: sudo setfacl -m u:{current_user}:r {file_path}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error checking logfile: {e}")
        raise

# Function to parse a line
def parse_line(line):
    line = line.strip()
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1]

    line = line.replace('\\"', '"')

    pattern = r'^(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+-\s+-\s+\[([^\]]+)\]\s+"([^"]+)"\s+"(.*?)"$'
    match = re.match(pattern, line)
    if match:
        return {
            'printer': match.group(1),
            'user': match.group(2),
            'job_id': match.group(3),
            'page_count': match.group(4),
            'media': '-',
            'client_ip': '-',
            'date_time': match.group(5),
            'host_name': match.group(6),
            'document_name': match.group(7)
        }
    else:
        logging.warning(f"Invalid line format: {line}")
        return None

def convert_cups_datetime(cups_dt):
    try:
        dt = datetime.strptime(cups_dt, "%d/%b/%Y:%H:%M:%S %z")
        return dt
    except Exception as e:
        logging.error(f"Date parse error: {e}")
        return None

def get_document_name(job_id, cups_conn):
    try:
        jobs = cups_conn.getJobs()
        for id, job in jobs.items():
            if str(id) == job_id:
                return job.get('job-name', 'Unknown Document')
    except Exception as e:
        logging.error(f"Error fetching document name: {e}")
    return 'Unknown Document'

def follow(logfile):
    logfile.seek(0, 2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(1)
            continue
        yield line

# Main block
try:
    check_logfile_permissions(LOG_FILE)

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    logging.debug('Database connection established.')

    cups_conn = cups.Connection()

    with open(LOG_FILE, 'r') as f:
        loglines = follow(f)
        for line in loglines:
            data = parse_line(line)
            if data:
                document_name = data.get('document_name')
                if not document_name:
                    document_name = get_document_name(data['job_id'], cups_conn)

                dt = convert_cups_datetime(data['date_time'])
                if dt:
                    logging.debug(f"Parsed data: user={data['user']}, doc={document_name}, dt={dt}, pages={data['page_count']}")
                    try:
                        cur.execute("""
                            INSERT INTO llx_print_logs (user_name, document_name, printed_at, pages)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            data['user'],
                            document_name,
                            dt,
                            data['page_count']
                        ))
                        conn.commit()
                        logging.debug("Insert success.")
                    except Exception as e:
                        logging.error(f"DB Insert error: {e}")
                        conn.rollback()
                else:
                    logging.warning(f"Skipping line due to invalid date: {line}")

except Exception as e:
    logging.error(f"Fatal error in main loop: {e}")

finally:
    try:
        if conn:
            conn.close()
            logging.debug("Database connection closed.")
    except:
        pass




