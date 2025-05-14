import cups
import getpass
import time
import psycopg2
from datetime import datetime

# PostgreSQL connection config (Dolibarr DB)
DB_HOST = '192.168.1.139'
DB_PORT = '5432'
DB_NAME = 'dolibarr'
DB_USER = 'root'
DB_PASS = 'root'
ENTITY_ID = 1

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Insert log into table
def insert_log(user_name, printer_name, document_name, printed_at, pages):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO llx_print_logs (user_name, printer_name, document_name, printed_at, pages, entity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_name, printer_name, document_name, printed_at, pages, ENTITY_ID))
        conn.commit()
        print(f"[DB SAVED] {user_name} printed '{document_name}' on '{printer_name}' at {printed_at}, Pages: {pages}")
    except Exception as e:
        print(f"[DB ERROR] {e}")
    finally:
        cursor.close()
        conn.close()

# Monitor CUPS jobs safely
def monitor_print_jobs():
    conn = cups.Connection()
    already_seen = set()

    while True:
        jobs = conn.getJobs(which_jobs='all')  # Include completed, processing, etc.
        for job_id, job in jobs.items():
            if job_id not in already_seen:
                already_seen.add(job_id)

                user = job.get('job-originating-user-name', getpass.getuser())
                printer_uri = job.get('job-printer-uri', '')
                printer_name = printer_uri.split('/')[-1] if printer_uri else 'Unknown_Printer'
                document = job.get('job-name', 'Unknown Document')
                pages = job.get('job-media-sheets-completed', job.get('job-pages', 1))  # Try both attributes
                printed_at = datetime.now()

                insert_log(user, printer_name, document, printed_at, pages)

        time.sleep(5)

if __name__ == '__main__':
    print("[INFO] Starting Local Print Logger (Direct DB Insert)...")
    monitor_print_jobs()


# import time
# import psycopg2
# from datetime import datetime

# DB_HOST = '192.168.1.139'
# DB_PORT = '5432'
# DB_NAME = 'dolibarr'
# DB_USER = 'root'
# DB_PASS = 'root'
# ENTITY_ID = 1

# LOG_FILE = '/var/log/cups/page_log'  # Make sure your user can read this file

# def get_db_connection():
#     return psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         database=DB_NAME,
#         user=DB_USER,
#         password=DB_PASS
#     )

# def insert_log(user_name, printer_name, document_name, printed_at, pages):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             INSERT INTO llx_print_logs (user_name, printer_name, document_name, printed_at, pages, entity)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (user_name, printer_name, document_name, printed_at, pages, ENTITY_ID))
#         conn.commit()
#         print(f"[DB SAVED] {user_name} printed '{document_name}' on '{printer_name}' at {printed_at}, Pages: {pages}")
#     except Exception as e:
#         print(f"[DB ERROR] {e}")
#     finally:
#         cursor.close()
#         conn.close()

# def monitor_page_log():
#     seen_lines = set()
#     print("[INFO] Monitoring /var/log/cups/page_log...")

#     while True:
#         try:
#             with open(LOG_FILE, 'r') as f:
#                 lines = f.readlines()

#             for line in lines:
#                 if line in seen_lines:
#                     continue
#                 seen_lines.add(line)

#                 # Example line format:
#                 # printer-name user job-id pages job-billing info time
#                 # Example:
#                 # HP_LaserJet_1020 root 53 1 - - 0
#                 parts = line.strip().split()
#                 if len(parts) >= 7:
#                     printer_name = parts[0]
#                     user_name = parts[1]
#                     job_id = parts[2]
#                     pages = int(parts[3])
#                     document_name = f"Job_{job_id}"
#                     printed_at = datetime.now()

#                     insert_log(user_name, printer_name, document_name, printed_at, pages)

#         except Exception as e:
#             print(f"[ERROR] Failed to read or process log: {e}")

#         time.sleep(5)

# if __name__ == '__main__':
#     monitor_page_log()

