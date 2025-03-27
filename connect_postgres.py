import psycopg2

# Database connection details
HOST = "192.168.1.139"  # Use the IP address of your PostgreSQL server
DB_NAME = "dolibarr"
USER = "root"
PASSWORD = "root"

try:
    # Establish connection
    conn = psycopg2.connect(
        host=HOST,
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD
    )
    print("Connected to PostgreSQL successfully!")

    # Create a cursor object
    cur = conn.cursor()

    # Get PostgreSQL version
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL Version: {version[0]}")

    # Fetch all table names and count them
    cur.execute("""
        SELECT tablename 
        FROM pg_catalog.pg_tables 
        WHERE schemaname = 'public';
    """)
    
    tables = cur.fetchall()
    table_count = len(tables)  # Count total number of tables
    
    if tables:
        print(f"\nTotal Tables: {table_count}")
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found in the database.")

    # Close the connection
    cur.close()
    conn.close()
    print("Database connection closed.")

except psycopg2.Error as e:
    print(f"Failed to connect to PostgreSQL: {e}")

