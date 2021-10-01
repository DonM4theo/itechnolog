import pyodbc

def read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute("select * from dbo.programy")
    for row in cursor:
        print(f'row = {row}')
    print()

conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=GT166\SQLEXPRESS01;"
    "Database=DBADAL;"
    "UID=unknow;"
    "PWD=unknow;"
    # "Trusted_Connection=yes;"
)

read(conn)
conn.close()
