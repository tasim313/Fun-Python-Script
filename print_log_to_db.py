import psycopg2
import time
import cups
import re
from datetime import datetime

# PostgreSQL connection details
DB_HOST = '192.168.1.139'
DB_PORT = '5432'
DB_NAME = 'dolibarr'
DB_USER = 'root'
DB_PASS = 'root'

# CUPS log file
LOG_FILE = '/var/log/cups/page_log'

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cur = conn.cursor()

# CUPS connection
cups_conn = cups.Connection()

def parse_line(line):
    # Step 1: Clean up line correctly
    line = line.strip()
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1]  # remove outer quotes

    line = line.replace('\\"', '"')  # replace escaped quotes inside the line

    # Step 2: Use regex pattern
    pattern = r'^(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+-\s+-\s+\[([^\]]+)\]\s+"([^"]+)"\s+"(.*?)"$'
    match = re.match(pattern, line)
    if match:
        return {
            'printer': match.group(1),
            'user': match.group(2),
            'job_id': match.group(3),
            'page_count': match.group(4),
            'media': '-',  # Placeholder since it's '-'
            'client_ip': '-',  # Placeholder since it's '-'
            'date_time': match.group(5),
            'host_name': match.group(6),
            'document_name': match.group(7)
        }
    else:
        print(f"Invalid line format: {line}")
        return None


def convert_cups_datetime(cups_dt):
    try:
        dt = datetime.strptime(cups_dt, "%d/%b/%Y:%H:%M:%S %z")
        return dt
    except Exception as e:
        print(f"Date parse error: {e}")
        return None

def get_document_name(job_id):
    try:
        jobs = cups_conn.getJobs()
        for id, job in jobs.items():
            if str(id) == job_id:
                return job.get('job-name', 'Unknown Document')
    except Exception as e:
        print(f"Error fetching document name: {e}")
    return 'Unknown Document'

def follow(logfile):
    logfile.seek(0, 2)  # Go to the end of file
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(1)
            continue
        yield line

with open(LOG_FILE, 'r') as f:
    loglines = follow(f)
    for line in loglines:
        data = parse_line(line)
        if data:
            document_name = data.get('document_name')
            
            # Only fallback if document_name is empty (should rarely happen)
            if not document_name:
                document_name = get_document_name(data['job_id'])

            dt = convert_cups_datetime(data['date_time'])
            if dt:
                print(f"Inserting: {data['user']}, {document_name}, {dt}, {data['page_count']}")
                
                # Updated query with the correct number of placeholders
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
            else:
                print(f"Skipping due to invalid date: {line}")



