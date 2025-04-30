import psycopg2
import paramiko
import os
import re
from datetime import datetime

# Database connection
DB_CONFIG = {
    "host": "192.168.1.139",
    "dbname": "dolibarr",
    "user": "root",
    "password": "root"
}

# NAS connection
NAS_CONFIG = {
    "hostname": "192.168.1.10",
    "username": "root",
    "password": "#8234*fnas",
    "target_dir": "/mnt/aikhanlab-adm-nas/nas_lab_reports/lab_reports/scan_external_report"
}

def get_sales_order_id_from_lab_number(lab_number, cursor):
    try:
        cursor.execute("""
            SELECT rowid 
            FROM llx_commande 
            WHERE ref = %s 
            LIMIT 1
        """, (lab_number,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error finding order for lab {lab_number}: {e}")
        return None

def extract_lab_number(filename):
    match = re.match(r'^(\d{4}-\d{5})_', filename)
    return match.group(1) if match else None

def link_nas_files_to_dolibarr():
    try:
        # PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # NAS
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=NAS_CONFIG['hostname'],
            username=NAS_CONFIG['username'],
            password=NAS_CONFIG['password']
        )
        sftp = ssh.open_sftp()
        files = sftp.listdir(NAS_CONFIG['target_dir'])

        processed_files = 0
        skipped_files = 0

        for filename in files:
            lab_number = extract_lab_number(filename)
            if not lab_number:
                print(f"Skipping file (invalid format): {filename}")
                skipped_files += 1
                continue

            sales_order_id = get_sales_order_id_from_lab_number(lab_number, cur)
            if not sales_order_id:
                print(f"No order found with ref={lab_number} (file: {filename})")
                skipped_files += 1
                continue

            filepath = f"{NAS_CONFIG['target_dir']}/{filename}"
            file_stat = sftp.stat(filepath)

            # Check if already linked
            cur.execute("SELECT rowid FROM llx_ecm_files WHERE fullpath_orig = %s", (filepath,))
            if cur.fetchone():
                print(f"File already linked: {filename}")
                skipped_files += 1
                continue

            # Ensure directory exists
            dir_path = f"orders/{sales_order_id}/lab_reports"
            cur.execute("SELECT rowid FROM llx_ecm_directories WHERE fullpath = %s", (dir_path,))
            dir_row = cur.fetchone()

            if dir_row:
                dir_id = dir_row[0]
            else:
                cur.execute("""
                    INSERT INTO llx_ecm_directories (label, entity, fullpath, description)
                    VALUES (%s, %s, %s, %s)
                    RETURNING rowid
                """, (
                    f"Lab Reports for {sales_order_id}",
                    1,
                    dir_path,
                    f"Directory for lab reports linked to order {sales_order_id}"
                ))
                dir_id = cur.fetchone()[0]

            # Insert file into llx_ecm_files
            cur.execute("""
                INSERT INTO llx_ecm_files (
                    ref, label, entity, filename, filepath, 
                    fullpath_orig, description, keywords,
                    fk_user_c, fk_user_m, date_c, tms, 
                    fk_directory, gen_or_uploaded, src_object_type
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s
                )
                RETURNING rowid
            """, (
                f"LAB-{lab_number}",
                f"Lab Report for {lab_number}",
                1,
                filename,
                f"{dir_path}/{filename}",
                filepath,
                f"Lab Report for order {sales_order_id}",
                'lab_report',
                1,
                1,
                datetime.fromtimestamp(file_stat.st_mtime),
                datetime.fromtimestamp(file_stat.st_mtime),
                dir_id,
                'uploaded',
                'commande'
            ))

            file_id = cur.fetchone()[0]
            processed_files += 1
            print(f"Linked {filename} → order ID {sales_order_id} (lab ref: {lab_number})")

            conn.commit()

        print(f"\n✅ Done. Processed: {processed_files}, Skipped: {skipped_files}")

    except Exception as e:
        print(f"❌ Error linking files: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()
        if 'sftp' in locals(): sftp.close()
        if 'ssh' in locals(): ssh.close()

if __name__ == "__main__":
    link_nas_files_to_dolibarr()