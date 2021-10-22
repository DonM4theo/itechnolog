from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_URL = ("Driver={SQL Server Native Client 11.0};"
    "Server=GT166\SQLEXPRESS01;"
    "Database=DBADAL;"
    "UID=sa;"
    "PWD=czosnek20;"
    # "Trusted_Connection=yes;"
)

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": db_URL})

Serverengine = create_engine(connection_url)

ServerSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Serverengine)

ServerBase = declarative_base()

# def read(conn):
#     print("Read")
#     cursor = conn.cursor()
#     cursor.execute("select * from dbo.programy")
#     for row in cursor:
#         print(f'row = {row}')
#     print()

# conn = pyodbc.connect(db_URL)

# read(conn)
# conn.close()
